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
