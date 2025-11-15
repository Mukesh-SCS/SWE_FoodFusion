# ================================================================================
# DESCRIPTION:
#     This module handles loading recipe data and images for the Recipe Recommendation
#     Web Application. It provides helper functions to read recipe datasets in JSON or
#     CSV format and prepares them for use in the recommender engine.
#
# USAGE:
#     Import functions into other scripts such as main.py:
#         from utils.data_loader import load_recipes_csv, load_recipes_json
#
# OUTPUTS:
#     - Returns Python data structures (lists/dictionaries)
#     - Returns image file paths for HTML rendering
#
# ARGUMENTS:
#     - path: File path to JSON or CSV datasets
#
# Author Info: Code written by SWE_FOODFUSION Team
# ================================================================================

import pandas as pd
import os


def load_recipes_csv(path="dataset/Food_Ingredients_and_Recipe_Dataset_with_Image_Name_Mapping.csv"):
    df = pd.read_csv(path)
    df["Image_Name"] = df["Image_Name"].astype(str).str.strip()

    if "Time" in df.columns:
        df["Time"] = pd.to_numeric(df["Time"], errors="coerce").fillna(9999)

    # Build a fast lookup set of available images
    image_dir = os.path.join("static", "food_images")
    all_images = {f.lower() for f in os.listdir(image_dir) if f.lower().endswith(".jpg")}

    def get_image(name):
        # Normalize
        base = name.strip()
        jpg = base if base.lower().endswith(".jpg") else base + ".jpg"
        lower = jpg.lower()
        # Direct match
        if lower in all_images:
            return f"food_images/{jpg}"
        # Try with dash prefix if needed
        dash = "-" + lower
        if dash in all_images:
            return f"food_images/{dash}"
        # fallback
        return "food_images/default.jpg"
    
    def get_difficulty(t):
        try:
            t = float(t)
        except:
            return "Unknown"
        if t <= 30:
            return "Easy"
        elif 30 <= t < 60:
            return "Medium"
        else:
            return "Hard"

    df["image"] = df["Image_Name"].apply(get_image)


    recipes = []
    for i, row in df.iterrows():
        time_val = float(row.get("Time", 0)) if not pd.isna(row.get("Time")) else 0
        recipes.append({
            "id": i,
            "name": row.get("Title", "Unknown Recipe"),
            "ingredients": str(row.get("Cleaned_Ingredients", "")).split(", "),
            "instructions": row.get("Instructions", "No instructions provided."),
            "image": row["image"],
            "diet": row.get("Diet", "Mixed"),
            "time": time_val,
            "difficulty": get_difficulty(time_val)
        })
    return recipes


def suggest_no_results(ingredients=None, filters=None):
    """
    Return a short suggestion message when a search yields no results.

    - ingredients: iterable of searched ingredients (can be list or comma-separated string)
    - filters: dict of applied filters (diet, time, etc.)
    """
    if ingredients is None:
        ingredients = []
    elif isinstance(ingredients, str):
        # split common comma/space separated input
        ingredients = [s.strip() for s in ingredients.split(",") if s.strip()]

    ingredients = list(ingredients)
    filters = filters or {}

    suggestions = []

    n = len(ingredients)
    if n == 0:
        suggestions.append("No recipes found. Try adding 1–3 ingredients or removing filters to broaden results.")
    elif n >= 5:
        suggestions.append("No recipes found. Try removing some ingredients to widen results.")
    else:
        # 1-4 ingredients
        suggestions.append("No recipes found. Try adding a few more ingredients to narrow results, or remove filters to broaden them.")

    if filters:
        suggestions.append("Also try disabling strict dietary/time filters or increasing maximum cook time.")

    suggestions.append("Check spelling and use common ingredient names (e.g., 'tomato' not 'tomatoes').")

    return " ".join(suggestions)