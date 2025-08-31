import argparse
import os

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
        choices=["csv", "json", "md"],
        help="output format (csv, json, md)"
    )
    
    parser.add_argument(
        "-s", "--shopping-list",
        action="store_true",
        help="generate a shopping list CSV for the meal plan"
    )
    
    parser.add_argument(
        "-o", "--out",
        type=str,
        help="output file path (default: outputs/plan.[format])"
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
    
    
if __name__ == "__main__":
    main()