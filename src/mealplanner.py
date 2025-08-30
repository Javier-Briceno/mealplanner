import argparse

def create_parser():
    parser = argparse.ArgumentParser(
        prog="mealplanner",
        description="A meal planning application that helps you organize your weekly meals"
    )
    
    # required arguments
    parser.add_argument("filename", help="Path to the meal plan file")
    
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
        help="target daily calories (e.g., 2200)"
    )
    
    parser.add_argument(
        "-p", "--protein",
        type=int,
        default=150,
        help="target protein per day (g)"
    )
    
    parser.add_argument(
        "-c", "--carbs",
        type=int,
        default=250,
        help="target carbs per day (g)"
    )
    
    parser.add_argument(
        "-f", "--fat",
        type=int,
        default=67,
        help="target fat per day (g)"
    )
    
    parser.add_argument(
        "--format",
        type=str,
        default="csv",
        help="output format (csv, json, md)"
    )
    
    parser.add_argument(
        "-s", "--shopping-list",
        action="store_true",
        help="generate a shopping list CSV for the meal plan"
    )

    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    
if __name__ == "__main__":
    main()