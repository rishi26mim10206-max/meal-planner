"""
storage.py
This module handles reading and writing project data in the /data folder.
Recipes use JSON, and the weekly meal plan uses a simple CSV file.
"""

import csv
import json

# Run the app from its project folder so these paths point into data/.
DATA_DIR = 'data'
RECIPES_FILE = 'data/recipes.json'
INGREDIENTS_FILE = 'data/ingredients.json'
MEAL_PLAN_FILE = 'data/meal_plan.csv'


def _load_json(path, default):
    """Load JSON from a file. Return a default value if it does not exist or is invalid."""
    # If the file does not exist, just return the default empty value.
    try:
        # Open the file in text mode with UTF-8 encoding.
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default


def _save_json(path, data):
    """Save a Python object as JSON."""
    with open(path, 'w', encoding='utf-8') as f:
        # indent=4 makes the JSON easier to read in a text editor.
        json.dump(data, f, indent=4)


def load_recipes():
    """Return the full list of saved recipes."""
    return _load_json(RECIPES_FILE, [])


def save_recipes(recipes):
    """Store the recipe list to the recipes.json file."""
    _save_json(RECIPES_FILE, recipes)


def load_ingredients():
    """Return the saved ingredient inventory, if any."""
    return _load_json(INGREDIENTS_FILE, [])


def load_meal_plan():
    """Return the current meal plan as a day-to-meal dictionary."""
    plan = {}
    try:
        with open(MEAL_PLAN_FILE, 'r', newline='', encoding='utf-8') as file:
            for row in csv.DictReader(file):
                day = row.get('day', '').strip()
                if day:
                    plan[day] = row.get('meal', '').strip()
    except (OSError, csv.Error):
        return {}
    return plan


def save_meal_plan(plan):
    """Save the meal plan dictionary as day and meal columns in a CSV file."""
    with open(MEAL_PLAN_FILE, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['day', 'meal'])
        for day, meal in plan.items():
            writer.writerow([day, meal])
