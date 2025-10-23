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

    df["image"] = df["Image_Name"].apply(get_image)

    recipes = []
    for i, row in df.iterrows():
        recipes.append({
            "id": i,
            "name": row.get("Title", "Unknown Recipe"),
            "ingredients": str(row.get("Cleaned_Ingredients", "")).split(", "),
            "instructions": row.get("Instructions", "No instructions provided."),
            "image": row["image"],
            "diet": row.get("Diet", "Mixed"),
            "time": "-"
        })
    return recipes