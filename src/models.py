class IngredientSpec:
    # Constructor to initialize the ingredient attributes
    def __init__(self, name: str, unit: str = "g", calories_100_g: float = 0.0, protein_100_g: float = 0.0, carbs_100_g: float = 0.0, fat_100_g: float = 0.0):
        self.name = name
        self.unit = unit
        self.calories_100_g = calories_100_g
        self.protein_100_g = protein_100_g
        self.carbs_100_g = carbs_100_g
        self.fat_100_g = fat_100_g

    # repr method for easier debugging and logging
    def __repr__(self):
        return f"Ingredient(name={self.name}, unit={self.unit}, calories_100_g={self.calories_100_g}, protein_100_g={self.protein_100_g}, carbs_100_g={self.carbs_100_g}, fat_100_g={self.fat_100_g})"

class IngredientAmount:
    # Constructor to initialize the ingredient amount attributes
    def __init__(self, spec: IngredientSpec, quantity: float):
        self.spec = spec
        self.quantity = quantity  # quantity in grams

    # repr method for easier debugging and logging
    def __repr__(self):
        return f"IngredientAmount(spec={self.spec}, quantity={self.quantity})"

class Meal:
    # Constructor to initialize the meal attributes
    def __init__(self, name: str, ingredients: dict[IngredientSpec, float], slot: str):    # assuming every ingredient (key) quantity (value)  is in grams
        self.name = name
        self.ingredients = ingredients
        self.slot = slot
        self.total_cals = sum(ing.calories_100_g * qty / 100 for ing, qty in ingredients.items())
        self.total_protein = sum(ing.protein_100_g * qty / 100 for ing, qty in ingredients.items())
        self.total_carbs = sum(ing.carbs_100_g * qty / 100 for ing, qty in ingredients.items())
        self.total_fat = sum(ing.fat_100_g * qty / 100 for ing, qty in ingredients.items())

    # repr method for easier debugging and logging
    def __repr__(self):
        return f"Meal(name={self.name}, total_cals={self.total_cals}, total_protein={self.total_protein}, total_carbs={self.total_carbs}, total_fat={self.total_fat})"

class Day:
    # Constructor to initialize the day attributes
    def __init__(self, meals: list[Meal], goal_cals: float = 0.0, goal_protein: float = 0.0, goal_carbs: float = 0.0, goal_fat: float = 0.0):
        # List of meals for the day
        self.meals = meals
        # Calculate total macros for the day
        self.total_cals = sum(meal.total_cals for meal in meals)
        self.total_protein = sum(meal.total_protein for meal in meals)
        self.total_carbs = sum(meal.total_carbs for meal in meals)
        self.total_fat = sum(meal.total_fat for meal in meals)
        # Goals for the day
        self.goal_cals = goal_cals
        self.goal_protein = goal_protein
        self.goal_carbs = goal_carbs
        self.goal_fat = goal_fat

    # repr method for easier debugging and logging
    def __repr__(self):
        return f"Day(total_cals={self.total_cals}, total_protein={self.total_protein}, total_carbs={self.total_carbs}, total_fat={self.total_fat})"
    
class Plan:
    # Constructor to initialize the plan attributes
    def __init__(self, days: list[Day]):
        self.days = days