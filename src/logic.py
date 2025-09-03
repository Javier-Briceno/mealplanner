from pathlib import Path
from models import IngredientSpec, Meal, Day, Plan
from prompts import generate_meal_day_plan
import json
from config import engine
import pandas as pd
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

def create_ingredient(name:str, unit:str, calories_100_g:int=0, protein_100_g:float=0.0, carbs_100_g:float=0.0, fat_100_g:float=0.0) -> IngredientSpec:
    return IngredientSpec(name, unit, calories_100_g, protein_100_g, carbs_100_g, fat_100_g)

# quantity must be in grams
def create_meal(name:str, ingredients:dict[IngredientSpec, float], slot:str) -> Meal:
    return Meal(name, ingredients, slot)

def create_day(meals_per_day:int, goal_cals:int, goal_protein:int, goal_carbs:int, goal_fat:int) -> Day:
    # Create a list to hold the meals for the day
    meals: list[Meal] = []
    response: str = generate_meal_day_plan(meals_per_day, goal_cals, goal_protein, goal_carbs, goal_fat)
    data: dict | None = response_to_dict(response)
    export_response_to_json(response, "../outputs/last_response.json")  # for debugging purposes
    if data:
        for meal_data in data.get("meals", []):
            print(f"\n=== Processing meal: {meal_data['title']} ===")
            
            meal_ingredients = {}
            for ing in meal_data["ingredients"]:
                print(f"\n--- Processing ingredient: {ing['name']} ---")
                print(f"Original values from JSON:")
                print(f"Quantity: {ing['quantity']} {ing['unit']}")
                print(f"Total macros for {ing['quantity']} {ing['unit']}:")
                print(f"Calories: {ing['kcal']}, Protein: {ing['protein']}, Carbs: {ing['carbs']}, Fat: {ing['fat']}")
                print(f"1 {ing['unit']} = {ing['unit_in_grams']}g")
                
                # Calculate total grams
                total_grams = ing['unit_in_grams'] * ing['quantity']
                print(f"Total grams: {ing['unit_in_grams']} * {ing['quantity']} = {total_grams}g")
                
                # Calculate per 100g values
                calories_100g = (100 * ing['kcal']) / total_grams
                protein_100g = (100 * ing['protein']) / total_grams
                carbs_100g = (100 * ing['carbs']) / total_grams
                fat_100g = (100 * ing['fat']) / total_grams
                
                print(f"Calculated values per 100g:")
                print(f"Calories: {calories_100g:.2f}")
                print(f"Protein: {protein_100g:.2f}")
                print(f"Carbs: {carbs_100g:.2f}")
                print(f"Fat: {fat_100g:.2f}")
                
                spec = create_ingredient(
                    name=ing["name"],
                    unit=ing["unit"],
                    calories_100_g=calories_100g,
                    protein_100_g=protein_100g,
                    carbs_100_g=carbs_100g,
                    fat_100_g=fat_100g
                )
                meal_ingredients[spec] = total_grams
            
            meal: Meal = create_meal(
                name=meal_data["title"],
                ingredients=meal_ingredients,
                slot=meal_data["slot"]
            )
            print(f"\nMeal totals:")
            print(f"Calories: {meal.total_cals:.2f}")
            print(f"Protein: {meal.total_protein:.2f}")
            print(f"Carbs: {meal.total_carbs:.2f}")
            print(f"Fat: {meal.total_fat:.2f}")
            meals.append(meal)
    day = Day(meals, goal_cals, goal_protein, goal_carbs, goal_fat)
    print(f"\n=== Day Totals ===")
    print(f"Calories: {day.total_cals:.2f}")
    print(f"Protein: {day.total_protein:.2f}")
    print(f"Carbs: {day.total_carbs:.2f}")
    print(f"Fat: {day.total_fat:.2f}")
    return day

def create_plan(days:int, meals_per_day:int, goal_cals_per_day:int, goal_protein_per_day:int, goal_carbs_per_day:int, goal_fat_per_day:int) -> Plan:
    # Create a list to hold the days
    plan_days: list[Day] = []
    for _ in range(days):
        # Create a new day with the specified parameters
        day: Day = create_day(meals_per_day, goal_cals_per_day, goal_protein_per_day, goal_carbs_per_day, goal_fat_per_day)
        plan_days.append(day)
    # return the plan with the created days
    return Plan(plan_days)

def response_to_dict(response:str) -> dict | None:
    try:
        data = json.loads(response)
    except json.JSONDecodeError as e:
        print("Failed to parse JSON:", e)
        data = None
    return data

def plan_to_json(plan: Plan, output_path: str) -> None:
    with open(output_path, "w") as f:
        json.dump(plan.to_dict(), f, indent=4)
    print(f"Plan saved to {output_path}")
    
# for debugging reasons
def export_response_to_json(response:str, output_path:str) -> None:
    data = response_to_dict(response)
    if data:
        with open(output_path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Response saved to {output_path}")
    else:
        print("No valid data to save.")

def add_ingredient_interactive() ->  None:
    name = input("Enter ingredient name: ").strip()
    unit = input("Enter unit (e.g., g, ml, cup): ").strip()
    try:
        calories_100_g = float(input("Enter calories per 100g: ").strip())
        protein_100_g = float(input("Enter protein per 100g: ").strip())
        carbs_100_g = float(input("Enter carbs per 100g: ").strip())
        fat_100_g = float(input("Enter fat per 100g: ").strip())
    except ValueError:
        print("Invalid input. Please enter numeric values for macros.")
        return None
    ingredient = create_ingredient(name, unit, calories_100_g, protein_100_g, carbs_100_g, fat_100_g)
    print(f"Created ingredient: {ingredient}")
    add_ingredient_to_db(ingredient)
    return ingredient

def add_ingredient_to_db(ingredient: IngredientSpec) -> None:
    print(f"Adding ingredient to database: {ingredient}")
    with engine.begin() as conn:
        conn.execute(text(
            """
            INSERT INTO ingredients (name, unit, calories_100_g, protein_100_g, carbs_100_g, fat_100_g)
            VALUES (:name, :unit, :calories_100_g, :protein_100_g, :carbs_100_g, :fat_100_g)
            ON CONFLICT (name) DO NOTHING;
            """),
            {
                "name": ingredient.name,
                "unit": ingredient.unit,
                "calories_100_g": ingredient.calories_100_g,
                "protein_100_g": ingredient.protein_100_g,
                "carbs_100_g": ingredient.carbs_100_g,
                "fat_100_g": ingredient.fat_100_g
            }
        )

def init_ingredient_db() -> None:
    try:
        with engine.begin() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS ingredient (
                    ingredient_id       SERIAL PRIMARY KEY,
                    name                VARCHAR(255) UNIQUE NOT NULL,
                    category            VARCHAR(80)
                );
            """))
            print("Ingredient table created or already exists.")
    except SQLAlchemyError as e:
        print(f"Error creating ingredient table: {e}")
        raise
    
def init_brand_db() -> None:
    try:
        with engine.begin() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS brand (
                    brand_id           SERIAL PRIMARY KEY,
                    name                VARCHAR(255) UNIQUE NOT NULL
                );
            """))
            print("Brand table created or already exists.")
    except SQLAlchemyError as e:
        print(f"Error creating brand table: {e}")
        raise
    
def init_product_db() -> None:
    try:
        with engine.begin() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS product (
                    product_id          SERIAL PRIMARY KEY,
                    ingredient_id       INT NOT NULL REFERENCES ingredient(ingredient_id),
                    brand_id            INT NOT NULL REFERENCES brand(brand_id),
                    unit_id            INT NOT NULL REFERENCES unit(unit_id),
                    label               VARCHAR(255) NOT NULL,     -- z.B. "Spaghetti n.5"
                    barcode             VARCHAR(64),               -- optional EAN/UPC
                    package_size        NUMERIC(10,2) NOT NULL,    -- z.B. 500.00
                    calories_per_100g  NUMERIC(10,2),           -- optional
                    fat_per_100g       NUMERIC(10,2),           -- optional
                    carbs_per_100g     NUMERIC(10,2),           -- optional
                    protein_per_100g   NUMERIC(10,2),           -- optional
                    calories_per_100ml NUMERIC(10,2),         -- optional, for liquids
                    fat_per_100ml      NUMERIC(10,2),         -- optional, for liquids
                    carbs_per_100ml    NUMERIC(10,2),         -- optional, for liquids
                    protein_per_100ml  NUMERIC(10,2),         -- optional, for liquids
                    notes               TEXT
                );
            """))
            print("Product table created or already exists.")
    except SQLAlchemyError as e:
        print(f"Error creating product table: {e}")
        raise

def init_unit_db() -> None:
    try:
        with engine.begin() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS unit (
                    unit_id             SERIAL PRIMARY KEY,
                    name                VARCHAR(50) NOT NULL,      -- "gram", "piece", "cup"
                    abbreviation        VARCHAR(12) NOT NULL,      -- "g", "pc", "cup"
                    kind                VARCHAR(16) NOT NULL       -- "mass" | "volume" | "count"
                );
            """))
            print("Unit table created or already exists.")
    except SQLAlchemyError as e:
        print(f"Error creating unit table: {e}")
        raise

def load_csv_to_table(csv_path: str, table_name: str) -> None:
    csv_path = Path(csv_path) # ensure it's a Path object, returns the same object if already a Path
    df = pd.read_csv(csv_path)
    with engine.begin() as conn:
        for _, row in df.iterrows(): # iterate over DataFrame rows as (index, Series) pairs.
            columns = ', '.join(row.index) # get column names
            placeholders = ', '.join([f":{col}" for col in row.index]) # create placeholders for values
            # create the insert query, avoid duplicates
            query = text(f"""
                INSERT INTO {table_name} ({columns})
                VALUES ({placeholders})
                ON CONFLICT DO NOTHING; -- avoid duplicates
            """)
            conn.execute(query, row.to_dict()) # execute query with row data (is inserted in the placeholders)