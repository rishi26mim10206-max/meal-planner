"""
main.py
This is the app entry point. It controls the main menu loop and connects
user input to the relevant feature functions.
"""

# Import the project modules we need.
import utils
import recipe_manager
import meal_planner


def display_menu():
    """Print the list of available actions for the user."""
    # Each print() call displays a menu option in the console.
    print("=== Recipe Manager & Meal Planner ===")
    print("1. Add Recipe")
    print("2. View All Recipes")
    print("3. Search Recipes")
    print("4. View Full Recipe Details")
    print("5. Create / Edit Meal Plan")
    print("6. Suggest Recipes from Available Ingredients")
    print("7. View Meal Plan")
    print("8. Generate Shopping List")
    print("9. Exit")


def main():
    """Run the interactive menu loop until the user exits."""
    # A dictionary maps the menu choice string to its function.
    # Example: '1' triggers recipe_manager.add_recipe.
    actions = {
        '1': recipe_manager.add_recipe,
        '2': recipe_manager.list_recipes,
        '3': recipe_manager.search_recipes,
        '4': recipe_manager.view_full_recipe,
        '5': meal_planner.create_meal_plan,
        '6': recipe_manager.suggest_recipes_from_ingredients,
        '7': meal_planner.view_meal_plan,
        '8': meal_planner.generate_shopping_list,
    }

    # while True creates an infinite loop until break is reached.
    while True:
        # Clear the screen before displaying the menu again.
        utils.clear_screen()
        display_menu()

        # Prompt for the user’s selection and store it as a string.
        choice = utils.prompt_string("\nSelect an option (1-9): ")

        # If the user chooses 9, exit the loop and end the program.
        if choice == '9':
            print("Exiting program. Goodbye!")
            break

        # Look up the function for the chosen option.
        action = actions.get(choice)

        # If the option exists, call that function.
        if action:
            action()
        else:
            # If no valid action matches, show an error.
            utils.print_error("Invalid option. Please try again.")

        # Wait for the user to press Enter before returning to the menu.
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    # This block runs only when the file is executed directly.
    main()
