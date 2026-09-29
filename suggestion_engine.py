=
"""
suggestion_engine.py
This module ranks recipes by how well they match the ingredients the user has.
It compares ingredient sets, calculates a compatibility percentage, and prints
an ordered list of the best suggestions.
"""
 
def calculate_match(recipe_ingredients, available):
    """
    Compare a recipe's ingredient list to the user's available ingredients.
 
    Return values:
        - match_percent: percent of recipe ingredients already available
        - matched: ingredients found in both lists
        - missing: ingredients the user still needs
        - matched_count: number of matching ingredients
        - total_ingredients: total ingredients in the recipe
    """
    # Normalize everything to lowercase and strip spaces so comparisons are stable.
    recipe_set = {ing.lower().strip() for ing in recipe_ingredients if ing.strip()}
    available_set = {ing.lower().strip() for ing in available if ing.strip()}
 
    if not recipe_set:
        return {
            "match_percent": 0.0,
            "matched": [],
            "missing": [],
            "matched_count": 0,
            "total_ingredients": 0
        }
 
    # Set intersection: ingredients present in both lists.
    matched = recipe_set & available_set
 
    # Set difference: ingredients in the recipe but not available.
    missing = recipe_set - available_set
 
    # Percentage match = matched items / total recipe ingredients.
    match_percent = (len(matched) / len(recipe_set)) * 100
 
    return {
        "match_percent": round(match_percent, 1),
        "matched": sorted(list(matched)),
        "missing": sorted(list(missing)),
        "matched_count": len(matched),
        "total_ingredients": len(recipe_set)
    }
 
 
def sort_key(item):
    """Return the value used to rank one suggestion (smaller = shown earlier)."""
    # Negative match_percent is used because Python's sort() is ascending by default.
    return (-item["match_percent"], len(item["missing"]))
 
 
def suggest_recipes(available_ingredients, recipes, top_n=8):
    """
    Evaluate each recipe and pick the best matches based on ingredient overlap.
    The function builds a list of results, each containing the recipe object and
    metrics such as match percentage and missing ingredients. It then sorts the
    results so the strongest matches appear first.
    """
    if not available_ingredients:
        return []
 
    results = []
 
    # Check every recipe against the user's available ingredients.
    for recipe in recipes:
        match_info = calculate_match(recipe['ingredients'], available_ingredients)
 
        # Skip recipes that share no ingredient with what the user has.
        if match_info["match_percent"] > 0:
            results.append({
                "recipe": recipe,
                "match_percent": match_info["match_percent"],
                "matched": match_info["matched"],
                "missing": match_info["missing"],
                "matched_count": match_info["matched_count"],
                "total_ingredients": match_info["total_ingredients"]
            })
 
    # Sort by highest match percentage first, then by fewer missing ingredients.
    results.sort(key=sort_key)
 
    return results[:top_n]
 
 
def display_suggestions(suggestions):
    """Display the ranked recipe suggestions in a readable format."""
    if not suggestions:
        print("\nNo matching recipes found. Try adding more ingredients.")
        return
 
    print("\n" + "="*60)
    print("           TOP RECIPE SUGGESTIONS FOR YOU")
    print("="*60)
 
    for idx, item in enumerate(suggestions, 1):
        recipe = item["recipe"]
        print(f"\n{idx}. {recipe['name']}  ({recipe['cuisine']})")
        print(f"   Match      : {item['match_percent']}% "
              f"({item['matched_count']}/{item['total_ingredients']} ingredients)")
        print(f"   Prep Time  : {recipe['prep_time']} mins")
 
        if item["matched"]:
            print(f"   You have   : {', '.join(item['matched'])}")
        if item["missing"]:
            print(f"   You need   : {', '.join(item['missing'])}")
        else:
            print("   You need   : None (You can cook this now!)")
 
    print("\n" + "="*60)
 
