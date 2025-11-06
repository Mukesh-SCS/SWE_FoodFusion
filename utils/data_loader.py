# ================================================================================
# DESCRIPTION:
#     This module handles loading recipe data and images for the Recipe Recommendation
#     Web Application. It provides helper functions to read recipe datasets in JSON or
#     CSV format and prepares them for use in the recommender engine.
#     Modified version for Google Drive image hosting.
#     Reads recipe CSV and maps Image_Name to public Drive URLs instead of local static files.
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


# --- Google Drive folder link here ---
DRIVE_FOLDER_LINK = "PASTE_YOUR_DRIVE_LINK_HERE"

# Convert shared folder link into base file URL format
def make_drive_url(file_name):
    """
    Creates a public 'view' link for a file hosted in Google Drive.
    This assumes files are accessible via anyone-with-link permission.
    Example output:
        https://drive.google.com/uc?export=view&id=<FILE_ID>
    """
    base_link = DRIVE_FOLDER_LINK.replace("drive/folders", "uc?export=view&id=")
    return f"{base_link}/{file_name}"


def load_recipes_csv(path="dataset/Food_Ingredients_and_Recipe_Dataset_with_Image_Name_Mapping.csv"):
    df = pd.read_csv(path)
    df["Image_Name"] = df["Image_Name"].astype(str).str.strip()

    if "Time" in df.columns:
        df["Time"] = pd.to_numeric(df["Time"], errors="coerce").fillna(9999)

    # Replace local static paths with Google Drive URLs
    df["image"] = df["Image_Name"].apply(make_drive_url)

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