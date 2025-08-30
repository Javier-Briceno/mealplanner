# Architecture

## Components
- CLI (mealplanner.py): parse args, orchestrate
- logic.py: validation, core rules, IO
- prompts.py: LLM prompt builders
- data/: static refs
- outputs/: artifacts
- .env: secrets

## Data Model
ClassDiagram:


    class Plan {
        +uuid id
        +date startDate
        +int days
        +int mealsPerDay
        +float totalCalories
        +float totalProtein
        +float totalCarbs
        +float totalFat
    }

    class Day {
        +int dayNumber
        +float dayCalories
        +float dayProtein
        +float dayCarbs
        +float dayFat
    }

    class Meal {
        +uuid id
        +string slot  // Breakfast, Lunch, Dinner
        +string title
        +float mealCalories
        +float mealProtein
        +float mealCarbs
        +float mealFat
    }

    class Ingredient {
        +string name
        +float quantity
        +string unit
        +float kcal
        +float protein
        +float carbs
        +float fat
        +string[] allergens
    }

    Plan "1" --> "*" Day : groups
    Day "1" --> "*" Meal : contains
    Meal "*" --> "*" Ingredient : uses


## Flows
flowchart TD


    A[User runs CLI\n(e.g. python mealplanner.py --days 7 --diet vegetarian)] --> B[Parse args in mealplanner.py]
    B --> C{Valid args?}
    C -- No --> C1[Show help & exit]
    C -- Yes --> D[Load config & .env]

    D --> E[logic.py: Validate inputs\n(diet, avoid, ingredients)]
    E --> F[prompts.py: Build AI request\n(Generate meals with macros)]
    F --> G[OpenAI API call\n→ JSON/text response]

    G --> H[logic.py: Parse response\n→ Meals & Ingredients with macros]
    H --> I[Aggregate macros\nper Meal, per Day, per Plan]
    I --> J[Write outputs/plan.csv\n(meals+macros)]
    I --> K[Write outputs/shopping_list.csv\n(ingredients+quantities+macros)]
    I --> L[Optional Markdown report]

    J & K & L --> M[Program exit code 0]


## Error Handling & Observability
- Retries, timeouts, input validation
- Logs: INFO for steps, WARN for recoverable, ERROR for exit>0
