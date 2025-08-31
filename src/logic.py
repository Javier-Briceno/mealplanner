from models import IngredientSpec, Meal, Day, Plan
from prompts import generate_meal_day_plan
import json

def create_ingredient(name:str, unit:str, calories_100_g:int=0, protein_100_g:float=0.0, carbs_100_g:float=0.0, fat_100_g:float=0.0) -> IngredientSpec:
    return IngredientSpec(name, unit, calories_100_g, protein_100_g, carbs_100_g, fat_100_g)

# quantity must be in grams
def create_meal(name:str, ingredients:dict[IngredientSpec, float]) -> Meal:
    return Meal(name, ingredients)

def create_day(meals_per_day:int, goal_cals:int, goal_protein:int, goal_carbs:int, goal_fat:int) -> Day:
    # Create a list to hold the meals for the day
    meals: list[Meal] = []
    response: str = generate_meal_day_plan(meals_per_day, goal_cals, goal_protein, goal_carbs, goal_fat)
    data: dict | None = response_to_dict(response)
    if data:
        for meal_data in data.get("meals", []):
            meal: Meal = create_meal(
                name=meal_data["title"],
                ingredients={
                    create_ingredient(
                        name=ing["name"],
                        unit=ing["unit"],
                        calories_100_g=ing["kcal"],
                        protein_100_g=ing["protein"],
                        carbs_100_g=ing["carbs"],
                        fat_100_g=ing["fat"]
                    ): ing["quantity"] for ing in meal_data["ingredients"]
                },
                slot=meal_data["slot"]
            )
            meals.append(meal)
    return Day(meals, goal_cals, goal_protein, goal_carbs, goal_fat)

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