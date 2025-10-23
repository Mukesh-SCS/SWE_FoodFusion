# ================================================================================
# DESCRIPTION:
#     This Flask web application recommends recipes based on user-input ingredients,
#     diet preferences, difficulty, and cooking time. It loads recipe data from a
#     local CSV dataset (with image paths) and displays matching recipes.
#
# USAGE:
#     Run the app:
#         python main.py
#     Open your browser and visit:
#         http://127.0.0.1:5000
#
# OUTPUTS:
#     - Web interface (index.html, results.html, view.html)
#     - Displays recipe recommendations and details
#
# ARGUMENTS:
#     No CLI arguments required. User input is handled through web forms.
#
# Author Info: Code written by SWE_FOODFUSION Team
# ================================================================================

from flask import Flask, render_template, request
from utils.data_loader import load_recipes_csv
from utils.recommender import recommend
import random, datetime

# ------------------------------------------------------------------------------
# Initialize the Flask web application
# ------------------------------------------------------------------------------
app = Flask(__name__)

# ------------------------------------------------------------------------------
# Load recipes from the Kaggle dataset (CSV file)
# This occurs once when the app starts to avoid reloading on each request.
# ------------------------------------------------------------------------------
recipes = load_recipes_csv("dataset/Food_Ingredients_and_Recipe_Dataset_with_Image_Name_Mapping.csv")


# ------------------------------------------------------------------------------
# Route: Home page
# Displays the homepage and today's specials.
# ------------------------------------------------------------------------------
@app.route("/")
def index():
    specials = get_today_specials()
    return render_template("index.html", specials=specials)


# ------------------------------------------------------------------------------
# Route: /search
# Handles search form submissions.
# Collects user filters (ingredients, diet, difficulty, time) and returns
# a list of matching recipes ranked by text similarity.
# ------------------------------------------------------------------------------
@app.route("/search", methods=["POST"])
def search():
    # --- Collect form inputs ---
    query = request.form.get("ingredients", "")
    diet = request.form.get("diet", "")
    difficulty = request.form.get("difficulty", "")
    time_limit = request.form.get("time", "")
   
    # --- Step 1: Generate recommendations using text similarity (TF-IDF + cosine) ---
    results = recommend(query, recipes)

    # --- Step 2: Apply user-selected filters ---
    if diet:
        results = [r for r in results if r.get("diet", "").lower() == diet.lower()]
    if difficulty:
        results = [r for r in results if r.get("difficulty") == difficulty]
    if time_limit:
        try:
            tl = int(time_limit)
            results = [r for r in results if r.get("time", 9999) <= tl]
        except ValueError:
            pass

    # Step 4: Display results in the template
    return render_template("results.html", recipes=results)


# ------------------------------------------------------------------------------
# Route: /view/<recipe_id>
# Displays full recipe details (ingredients, instructions, image) for a given recipe.
# ------------------------------------------------------------------------------
@app.route("/view/<int:recipe_id>")
def view_recipe(recipe_id):
    # Validate index to avoid out-of-range errors
    if recipe_id < 0 or recipe_id >= len(recipes):
        return "Recipe not found", 404

    recipe = recipes[recipe_id]
    return render_template("view.html", recipe=recipe)


# ------------------------------------------------------------------------------
# Helper Function: get_today_specials
# Selects a random subset of recipes to feature as today's specials.
# The selection is deterministic for the same date.
# ------------------------------------------------------------------------------
def get_today_specials(n=5):
    today = datetime.date.today()
    random.seed(today.toordinal())
    sample = random.sample(recipes, min(n, len(recipes)))
    return sample


# ------------------------------------------------------------------------------
# Application entry point
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
