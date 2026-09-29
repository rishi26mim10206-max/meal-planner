"""
recipe_manager.py
Handles all recipe-related operations: adding, listing, searching, and viewing.
Each recipe is stored as a dictionary with keys such as name, cuisine,
ingredients, prep_time, and steps.
"""

import storage
import utils
import suggestion_engine


def display_recipe(r):
    """Print full details of a single recipe dictionary."""
    # A recipe is expected to look like:
    # {
    #   "name": "Pasta",
    #   "cuisine": "Italian",
    #   "prep_time": "30 mins",
    #   "ingredients": [...],
    #   "steps": [...]
    # }a
    print(f"=== {r['name']} ===")
    print(f"Cuisine: {r['cuisine']} | Prep Time: {r['prep_time']}")

    # Optional fields are checked with .get() to avoid KeyError.
    if r.get('difficulty'):
        print(f"Difficulty: {r['difficulty']}")
    if r.get('servings'):
        print(f"Servings: {r['servings']}")

    print("\nIngredients:")
    for ing in r['ingredients']:
        print(f"  - {ing}")

    print("\nSteps:")
    for i, step in enumerate(r['steps'], 1):
        print(f"  {i}. {step}")
    print()


def add_recipe():
    """Collect recipe information from the user and save it to storage."""
    utils.clear_screen()
    print("=== Add New Recipe ===")

    # Prompt for required fields one by one.
    name = utils.prompt_string("Recipe Name: ")
    cuisine = utils.prompt_string("Cuisine (e.g., Italian, Mexican): ")
    prep_time = utils.prompt_string("Prep Time (e.g., 30 mins): ")
    ingredients = utils.prompt_list("Enter Ingredients")
    steps = utils.prompt_list("Enter Steps")

    # Build a recipe dictionary.
    recipe = {
        "name": name,
        "ingredients": ingredients,
        "steps": steps,
        "cuisine": cuisine,
        "prep_time": prep_time
    }

    # Load all existing recipes, append the new one, then save back.
    recipes = storage.load_recipes()
    recipes.append(recipe)
    storage.save_recipes(recipes)

    utils.print_success(f"Recipe '{name}' added successfully!")


def list_recipes():
    """Display every saved recipe in a numbered list."""
    utils.clear_screen()
    print("=== All Recipes ===")
    recipes = storage.load_recipes()

    if not recipes:
        print("No recipes found.")
        return

    for idx, r in enumerate(recipes, 1):
        print(f"{idx}. {r['name']} ({r['cuisine']}) - {r['prep_time']}")


def search_recipes():
    """Find recipes matching a name or ingredient query."""
    utils.clear_screen()
    print("=== Search Recipes ===")

    # Lowercase the search term so the comparison is case-insensitive.
    query = utils.prompt_string("Search by name or ingredient: ").lower()
    recipes = storage.load_recipes()
    results = []

    # Check each recipe name and ingredient list for a match.
    for r in recipes:
        searchable = [r['name']] + r['ingredients']
        if any(query in val.lower() for val in searchable):
            results.append(r)

    if not results:
        print("No matching recipes found.")
        return

    print(f"\nFound {len(results)} matching recipe(s):")
    for idx, r in enumerate(results, 1):
        print(f"{idx}. {r['name']} ({r['cuisine']}) - {r['prep_time']}")


def view_full_recipe():
    """Show the full recipe details for a selected recipe number."""
    list_recipes()
    recipes = storage.load_recipes()

    if not recipes:
        return

    try:
        # required=False means the user may leave it blank, which becomes 0.
        choice = int(utils.prompt_string(
            "\nEnter recipe number to view (or 0 to cancel): ", required=False) or 0)

        if choice == 0:
            return

        if 1 <= choice <= len(recipes):
            utils.clear_screen()
            display_recipe(recipes[choice - 1])
        else:
            utils.print_error("Invalid recipe number.")
    except ValueError:
        # int(...) raises ValueError if the text is not a valid number.
        utils.print_error("Please enter a valid number.")


def suggest_recipes_from_ingredients():
    """Suggest recipes that best match the ingredients the user has."""
    utils.clear_screen()
    print("=== Suggest Recipes from Available Ingredients ===")

    ingredients = utils.prompt_comma_separated_list("Enter available ingredients")
    recipes = storage.load_recipes()

    if not recipes:
        utils.print_error("No recipes in database.")
        return

    # Ask the suggestion engine to rank recipes based on match quality.
    suggestions = suggestion_engine.suggest_recipes(ingredients, recipes)
    suggestion_engine.display_suggestions(suggestions)

    try:
        # Use a number to choose one of the displayed suggestions.
        choice = int(utils.prompt_string(
            "\nEnter recipe number to view full details (or 0 to cancel): ",
            required=False) or 0)

        if choice == 0:
            return

        if 1 <= choice <= len(suggestions):
            utils.clear_screen()
            display_recipe(suggestions[choice - 1]['recipe'])
        else:
            utils.print_error("Invalid recipe number.")
    except ValueError:
        utils.print_error("Please enter a valid number.")
