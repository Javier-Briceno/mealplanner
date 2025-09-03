import argparse
import os
from logic import create_plan, plan_to_json, Plan, add_ingredient_interactive, load_csv_to_table, init_unit_db, init_brand_db, init_product_db, init_ingredient_db

def create_parser():
    parser = argparse.ArgumentParser(
        prog="mealplanner",
        description="A meal planning application that helps you organize your weekly meals"
    )
    
    # optional arguments
    parser.add_argument(
        "-d", "--days",
        type=int,
        default=7,
        help="Number of days to plan (default: 7)"
    )
    
    parser.add_argument(
        "-m", "--meals-per-day",
        type=int,
        default=3,
        help="meals per day (e.g., 3 = breakfast, lunch, dinner)"
    )
    
    parser.add_argument(
        "-k", "--calories",
        type=int,
        default=2200,
        help="target daily calories (default: 2200)"
    )
    
    parser.add_argument(
        "-p", "--protein",
        type=int,
        default=150,
        help="target protein per day (default: 150g)"
    )
    
    parser.add_argument(
        "-c", "--carbs",
        type=int,
        default=250,
        help="target carbs per day (default: 250g)"
    )
    
    parser.add_argument(
        "-f", "--fat",
        type=int,
        default=67,
        help="target fat per day (default: 67g)"
    )
    
    parser.add_argument(
        "--format",
        type=str,
        default="csv",
        choices=["csv", "json", "md"],
        help="output format (csv, json, md)"
    )
    
    parser.add_argument(
        "-s", "--shopping-list",
        action="store_true",
        help="generate a shopping list CSV for the meal plan"
    )

    parser.add_argument(
        "-r", "--add-recipe",
        action="store_true",
        help="add a new recipe to the database"
    )
    
    parser.add_argument(
        "-i", "--add-ingredient",
        action="store_true",
        help="add a new ingredient to the database"
    )
    
    parser.add_argument(
        "-o", "--out",
        type=str,
        default="../outputs/mealplan",
        help="output file path (default: ../outputs/mealplan)"
    )

    return parser

def get_output_path(args):
    # default output path based on format
    extensions = {
        "csv": ".csv",
        "json": ".json",
        "md": ".md"
    }
    
    if args.out:
        # check if the provided path ends with any of the valid extensions
        if not any(args.out.lower().endswith(ext) for ext in extensions.values()):
            # if not, append the extension based on the format
            return f"{args.out}{extensions[args.format]}"
        return args.out
    
    #create outputs directory if it doesn't exist
    os.makedirs("../outputs", exist_ok=True)
    
    return f"../outputs/mealplan{extensions[args.format]}"

def main():
    # create parser and parse arguments
    parser = create_parser()
    args = parser.parse_args()
    
    # get output path
    output = get_output_path(args)
    
    # seed database tables with CSV files
    init_unit_db()
    load_csv_to_table("../assets/seeds/units_seed.csv", "unit")
    init_brand_db()
    load_csv_to_table("../assets/seeds/brands_seed.csv", "brand")
    init_ingredient_db()
    load_csv_to_table("../assets/seeds/ingredients_seed.csv", "ingredient")
    init_product_db()
    load_csv_to_table("../assets/seeds/products_seed.csv", "product")
    
    """plan: Plan = create_plan(
        days=args.days,
        meals_per_day=args.meals_per_day,
        goal_cals_per_day=args.calories,
        goal_protein_per_day=args.protein,
        goal_carbs_per_day=args.carbs,
        goal_fat_per_day=args.fat
    )

    plan_to_json(plan, output)
    """

if __name__ == "__main__":
    main()