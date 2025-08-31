from config import client

def generate_meal_day_plan(meals_per_day:int, goal_cals:int, goal_protein:int, goal_carbs:int, goal_fat:int) -> str:
    system = f"""
You are a meal planning assistant that outputs STRICT JSON only.
Follow nutrition targets and constraints exactly.
Never include commentary, markdown, or code blocks—return JSON only.
    """
    
    user = f"""
Create a one-day meal plan with exactly {meals_per_day} meals.

Targets (per day):
- calories_kcal: {goal_cals}
- protein_g: {goal_protein}
- carbs_g: {goal_carbs}
- fat_g: {goal_fat}

Constraints:
- Avoid unrealistic recipes; keep ingredients simple and common.
- Keep per-meal titles short and clear.
- Totals should be within ±10% of each target. If you deviate, keep it minimal and balanced.

Output JSON schema (STRICT):
{{
  "dayCalories": number,
  "dayProtein": number,
  "dayCarbs": number,
  "dayFat": number,
  "meals": [
    {{
      "slot": "Breakfast" | "Lunch" | "Dinner" | "Snack",
      "title": string,
      "mealCalories": number,
      "mealProtein": number,
      "mealCarbs": number,
      "mealFat": number,
      "ingredients": [
        {{
          "name": string,
          "quantity": number,
          "unit": string,
          "kcal": number,
          "protein": number,
          "carbs": number,
          "fat": number,
          "allergens": [string]
        }}
      ],
      "instructions": string
    }}
    // ... exactly {meals_per_day} meals total
  ]
}}

Rules:
- Sum of all ingredient macros in each meal must equal the meal macros.
- Sum of all meal macros must equal the day macros.
- Use units like "g", "ml", "tbsp", "cup", "pcs".
- If unsure of exact macros, use reasonable typical values and stay consistent.
- Return only valid JSON. No trailing commas, no comments.
    """.strip()
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": system
            },
            {
                "role": "user", 
                "content": user
            }
        ],
        temperature=0.2,
        max_tokens=1500
    )