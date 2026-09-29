# Recipe Manager & Meal Planner

A fully working,Python application that lets you manage recipes, build a 7-day meal plan, and automatically generate a combined shopping list.

## Setup
1. Make sure you have **Python 3.8+** installed.
2. Clone or download this project.
3. No external packages required! This runs entirely on the Python Standard Library.

## Running the Application
Open a command prompt or terminal in the project directory and run:

```bash
python main.py
```

## Features
- **Add Recipe:** Add a new recipe with name, ingredients, steps, cuisine, and prep time.
- **View All Recipes:** List all stored recipes.
- **Search Recipes:** Search for recipes by name or ingredient.
- **View Full Recipe:** Show complete details for a specific recipe.
- **Suggest Recipes:** Intelligently suggest recipes based on ingredients you have available.
- **Create Meal Plan:** Assign recipes to Monday-Sunday.
- **Generate Shopping List:** Generates a deduplicated `.txt` shopping list based on your meal plan.

## Storage
All data is saved locally in `data/recipes.json` and `data/meal_plan.json`. It will persist after you close the program. Shopping lists are exported to `data/shopping_list.txt`.
