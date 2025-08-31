class Ingredient:
    # Constructor to initialize the ingredient attributes
    def __init__(self, name: str, quantity: float, unit: str, calories_100_g: int = 0, protein_100_g: float = 0.0, carbs_100_g: float = 0.0, fat_100_g: float = 0.0):
        self.name = name
        self.quantity = quantity
        self.unit = unit
        self.calories_100_g = calories_100_g
        self.protein_100_g = protein_100_g
        self.carbs_100_g = carbs_100_g
        self.fat_100_g = fat_100_g

    # repr method for easier debugging and logging
    def __repr__(self):
        return f"Ingredient(name={self.name}, quantity={self.quantity}, unit={self.unit}, calories_100_g={self.calories_100_g}, protein_100_g={self.protein_100_g}, carbs_100_g={self.carbs_100_g}, fat_100_g={self.fat_100_g})"

class Meal:
    # Constructor to initialize the meal attributes
    # assuming every ingredient quantity is in grams
    def __init__(self, name: str, ingredients: dict[Ingredient, float]):
        self.name = name
        self.ingredients = ingredients
        self.total_calories = sum(ing.calories_100_g * qty / 100 for ing, qty in ingredients.items())
        self.total_protein = sum(ing.protein_100_g * qty / 100 for ing, qty in ingredients.items())
        self.total_carbs = sum(ing.carbs_100_g * qty / 100 for ing, qty in ingredients.items())
        self.total_fat = sum(ing.fat_100_g * qty / 100 for ing, qty in ingredients.items())

    # repr method for easier debugging and logging
    def __repr__(self):
        return f"Meal(name={self.name}, total_calories={self.total_calories}, total_protein={self.total_protein}, total_carbs={self.total_carbs}, total_fat={self.total_fat})"
    
class Day:
    # Constructor to initialize the day attributes
    def __init__(self, meals: list[Meal]):
        self.meals = meals
        self.total_calories = sum(meal.total_calories for meal in meals)
        self.total_protein = sum(meal.total_protein for meal in meals)
        self.total_carbs = sum(meal.total_carbs for meal in meals)
        self.total_fat = sum(meal.total_fat for meal in meals)

    # repr method for easier debugging and logging
    def __repr__(self):
        return f"Day(total_calories={self.total_calories}, total_protein={self.total_protein}, total_carbs={self.total_carbs}, total_fat={self.total_fat})"
    
class Plan:
    # Constructor to initialize the plan attributes
    def __init__(self, days: list[Day]):
        self.days = days
        self.total_calories = sum(day.total_calories for day in days)
        self.total_protein = sum(day.total_protein for day in days)
        self.total_carbs = sum(day.total_carbs for day in days)
        self.total_fat = sum(day.total_fat for day in days)

    # repr method for easier debugging and logging
    def __repr__(self):
        return f"Plan(total_calories={self.total_calories}, total_protein={self.total_protein}, total_carbs={self.total_carbs}, total_fat={self.total_fat})"