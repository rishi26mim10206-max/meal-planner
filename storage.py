"""
storage.py
This module handles reading and writing project data to JSON files in the
/data folder. It keeps the app state persistent across runs.
"""

import json
import os
import utils

# File paths for the app’s persisted data.
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
RECIPES_FILE = os.path.join(DATA_DIR, 'recipes.json')
INGREDIENTS_FILE = os.path.join(DATA_DIR, 'ingredients.json')
MEAL_PLAN_FILE = os.path.join(DATA_DIR, 'meal_plan.json')


def _load_json(path, default):
    """Load JSON from a file. Return a default value if it does not exist or is invalid."""
    # Ensure the data directory exists before reading or writing files.
    os.makedirs(DATA_DIR, exist_ok=True)

    # If the file does not exist, just return the default empty value.
    if not os.path.exists(path):
        return default

    try:
        # Open the file in text mode with UTF-8 encoding.
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        # Log a problem and fall back to a safe default.
        utils.log_error(f"Failed to load {path}: {e}")
        return default


def _save_json(path, data, message):
    """Save a Python object as JSON and log the result."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        # indent=4 makes the JSON easier to read in a text editor.
        json.dump(data, f, indent=4)
    utils.log_info(message)


def load_recipes():
    """Return the full list of saved recipes."""
    return _load_json(RECIPES_FILE, [])


def save_recipes(recipes):
    """Store the recipe list to the recipes.json file."""
    _save_json(RECIPES_FILE, recipes, f"Saved {len(recipes)} recipes")


def load_ingredients():
    """Return the saved ingredient inventory, if any."""
    return _load_json(INGREDIENTS_FILE, [])


def load_meal_plan():
    """Return the current meal plan dictionary."""
    return _load_json(MEAL_PLAN_FILE, {})


def save_meal_plan(plan):
    """Save the meal plan dictionary to disk."""
    _save_json(MEAL_PLAN_FILE, plan, "Saved meal plan")
