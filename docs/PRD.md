# Project Requirement Doc (PRD)

## 1. Overview
- Problem: Takes too much time to make meals manually that reach the calories and macros diary goal. Once a day that reaches the goal is made, it cannot be edited because that implies changing everything -> is not flexible. Also the creation of many different meal day plans is needed, otherwise the same meal day would repeat several times.
- Goal/Outcome (demo, artifact): The goal is to facilitate the creation of meal day plans with AI, making them flexible (The AI has already alternatives for each meal of the day in case its not possible to follow it completely)
- Users/Context: For now, everything runs on the CLI. 
- Non-Goals: Make the most efficient meal plan (Same use of ingredients and try to maximize the use of the groceries shopped). Store ingredients with calories and macros. User create meals. 

## 2. Requirements
### Functional (MoSCoW)
- Must: User give goal calories and macros and it should create a meal day plan where every meal has the amount of ingredients and its recipe.
- Should: Create different alternatives to choose from
- Could: Track ingredients and create additional Shopping List
### Non-Functional
- Performance: Meal planner should create results in less than 10 seconds
- Security/Privacy: .env file
- i18n/Locale: Only english
- OS/Runtime: Windows

## 3. Constraints
- Time/Budget: for v1 1 day
- Data/API limits: OpenAI API (5 usd monthly)
- Libraries: Python 3.10, argparse, dotenv, pytest (updating by need)

## 4. Definition of Done
- [ ] Runs via single command example:
- [ ] Validates inputs and prints helpful errors
- [ ] Deterministic output format (CSV/JSON/MD)
- [ ] README with install & usage
- [ ] 5+ test cases pass (incl. 2 error cases)
