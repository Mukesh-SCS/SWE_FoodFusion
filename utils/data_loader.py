# ================================================================================
# DESCRIPTION:
#     This module handles loading recipe data and images for the Recipe Recommendation
#     Web Application. It provides helper functions to read recipe datasets in JSON or
#     CSV format and prepares them for use in the recommender engine.
#     Modified version for Google Drive image hosting using dynamic drive_map.json.
#
# USAGE:
#     Import functions into other scripts such as main.py:
#         from utils.data_loader import load_recipes_csv
#
# OUTPUTS:
#     - Returns list of recipe dictionaries with Google Drive image URLs
#
# DEPENDENCIES:
#     Requires: dataset/drive_map.json
#     Format:
#     {
#       "apple_pie.jpg": "1AbCdEfGhIjKlmNoPqR",
#       "chicken_curry.jpg": "2XyZlMnOpQrStUvWxYz"
#     }
#
# Author Info: Code written by SWE_FOODFUSION Team
# ================================================================================

import pandas as pd
import os
import json

# --- Path to the image ID mapping file ---
DRIVE_MAP_PATH = "dataset/drive_map.json"

# --- Load mapping once ---
def load_drive_map():
    if os.path.exists(DRIVE_MAP_PATH):
        with open(DRIVE_MAP_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        print(" Warning: drive_map.json not found. Using default placeholder images.")
        return {}

# --- Convert local image name to Google Drive view URL ---
def make_drive_url(file_name, file_id_map):
    """Match CSV names to JSON keys even if missing .jpg"""
    name = file_name.strip()
    if not name.lower().endswith(".jpg"):
        name_jpg = name + ".jpg"
    else:
        name_jpg = name
    file_id = file_id_map.get(name_jpg) or file_id_map.get(name)
    if file_id:
        return f"/image/{file_id}"
    return "/static/default.jpg"


# --- Main loader function ---
def load_recipes_csv(path="dataset/Food_Ingredients_and_Recipe_Dataset_with_Image_Name_Mapping.csv"):
    df = pd.read_csv(path)
    df["Image_Name"] = df["Image_Name"].astype(str).str.strip()

    if "Time" in df.columns:
        df["Time"] = pd.to_numeric(df["Time"], errors="coerce").fillna(9999)

    # Load the Drive ID map
    file_id_map = load_drive_map()

    # Build full Google Drive URLs
    df["image"] = df["Image_Name"].apply(lambda x: make_drive_url(x, file_id_map))

    # Determine difficulty level from time
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

    # Build recipe list
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