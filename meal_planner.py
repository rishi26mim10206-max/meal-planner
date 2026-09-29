"""
meal_planner.py
This file handles a weekly meal plan and exports a shopping list from the
planned recipes.
"""

import os
import storage
import utils

# The meal plan is organized by weekday.
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def view_meal_plan():
    """Display the current weekly meal plan in a readable format."""
    utils.clear_screen()
    print("=== 7-Day Meal Plan ===")
    plan = storage.load_meal_plan()

    # Loop through each day and print the assigned meal or a placeholder.
    for day in DAYS:
        print(f"{day}: {plan.get(day, 'No meal planned')}")
    print()


def create_meal_plan():
    """Let the user assign recipes to each day of the week."""
    utils.clear_screen()
    print("=== Create/Edit Meal Plan ===")

    recipes = storage.load_recipes()
    if not recipes:
        utils.print_error("No recipes available. Please add recipes first.")
        return

    print("Available Recipes:")
    for idx, r in enumerate(recipes, 1):
        print(f"{idx}. {r['name']}")
    print()

    # Load the existing plan so we can update it instead of replacing it entirely.
    plan = storage.load_meal_plan()

    # For each day, ask the user to select a recipe number or clear it.
    for day in DAYS:
        current = plan.get(day, 'None')
        choice = utils.prompt_string(
            f"Select recipe # for {day} (blank=keep '{current}', c=clear): ",
            required=False)

        if choice.lower() == 'c':
            # Set the day to an empty string to clear the assignment.
            plan[day] = ""
        elif choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(recipes):
                # Store the selected recipe name in the plan dictionary.
                plan[day] = recipes[idx - 1]['name']
            else:
                utils.print_error("Invalid number, skipping...")

    storage.save_meal_plan(plan)
    utils.print_success("Meal plan updated successfully!")


def generate_shopping_list():
    """Combine all ingredients used in the meal plan into a shopping list."""
    utils.clear_screen()
    print("=== Generate Shopping List ===")

    plan = storage.load_meal_plan()
    recipes = storage.load_recipes()

    # Create a quick lookup: recipe name -> full recipe dictionary.
    recipe_dict = {r['name']: r for r in recipes}

    # Keep only non-empty meal names.
    planned_names = {name for name in plan.values() if name}

    if not planned_names:
        utils.print_error("Meal plan is empty. Please create a meal plan first.")
        return

    all_ingredients = []
    for name in planned_names:
        if name in recipe_dict:
            # Add all ingredients from each planned recipe.
            all_ingredients.extend(recipe_dict[name]['ingredients'])
        else:
            print(f"[Warning] Recipe '{name}' not found in database.")

    # Remove duplicates and normalize formatting.
    unique = sorted({ing.strip().capitalize() for ing in all_ingredients if ing.strip()})

    if not unique:
        utils.print_error("No ingredients found for the planned meals.")
        return

    print("Shopping List:")
    for ing in unique:
        print(f"- {ing}")

    # Save the list to a text file in the data folder.
    output_file = os.path.join(storage.DATA_DIR, 'shopping_list.txt')
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=== Shopping List ===\n")
            for ing in unique:
                f.write(f"- {ing}\n")
        utils.print_success(f"\nShopping list exported to {output_file}")
    except IOError as e:
        utils.print_error(f"Failed to export shopping list: {e}")
