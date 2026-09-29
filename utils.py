"""
utils.py
Shared helper functions for the app.
These are small utility tools used by multiple modules to keep the project
consistent and easier to maintain.
"""

def clear_screen():
    """Add blank lines before displaying the next screen."""
    print('\n' * 50)


def prompt_string(prompt, required=True):
    """Ask the user for a text input. Keeps asking if required and empty."""
    # This loops until the user enters a valid value.
    while True:
        val = input(prompt).strip()
        if not val and required:
            print("Error: This field is required.")
        else:
            return val


def prompt_list(prompt):
    """Ask user to enter items one by one. Blank line finishes input."""
    print(f"{prompt} (enter a blank line to finish):")
    items = []

    # Continue until the user enters a blank line and there is at least one item.
    while True:
        val = input("> ").strip()
        if not val:
            if not items:
                print("Error: List cannot be empty.")
                continue
            break
        items.append(val)
    return items


def prompt_comma_separated_list(prompt):
    """Ask user for comma-separated items. Keeps asking until valid."""
    while True:
        # Example input: 'tomato, onion, garlic'
        val = input(f"{prompt} (comma-separated): ").strip()
        # Split on commas, remove blanks, and keep only real items.
        items = [i.strip() for i in val.split(',') if i.strip()] if val else []
        if items:
            return items
        print("Error: Please enter at least one item.")


def print_error(msg):
    """Display a red-style error message format."""
    print(f"[ERROR] {msg}")


def print_success(msg):
    """Display a success message."""
    print(f"[SUCCESS] {msg}")
