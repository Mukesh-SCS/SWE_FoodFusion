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
from utils.data_loader import suggest_no_results
from PIL import Image
from utils.image_predictor import predict_topk
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
# Route: /upload
# Displays the image upload page.
# ------------------------------------------------------------------------------
@app.route("/upload")
def upload():
    return render_template("upload.html")  



# ------------------------------------------------------------------------------
# Route: /search
# Handles search form submissions.
# Collects user filters (ingredients, diet, difficulty, time) and returns
# a list of matching recipes ranked by text similarity.
# ------------------------------------------------------------------------------
@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("ingredients", "").strip()

    # Each of these becomes a list if multiple were chosen; empty list if none
    diets = [d.lower() for d in request.form.getlist("diet") if d]
    difficulties = [d.lower() for d in request.form.getlist("difficulty") if d]
    times = [t for t in request.form.getlist("time") if t] 

    # Step 1: run the recommender
    results = recommend(query, recipes)

    # Step 2: apply diet filter(s)
    if diets:
        results = [
            r for r in results
            if r.get("diet", "").lower() in diets
        ]

    # Step 3: apply difficulty filter(s)
    if difficulties:
        results = [
            r for r in results
            if r.get("difficulty", "").lower() in difficulties
        ]

    # Step 4: apply time limits (multiple options can be handled too)
    if times:
        allowed_times = []
        for t in times:
            try:
                allowed_times.append(int(t))
            except ValueError:
                pass
        if allowed_times:
            min_allowed = min(allowed_times)
            results = [
                r for r in results
                if isinstance(r.get("time"), (int, float)) and r.get("time") <= min_allowed
            ]
    # Step 4: Display results in the template
    no_results_message = None
    if not results:
        no_results_message = suggest_no_results(ingredients=query, filters={"diet": diets, "max_time": times})

    return render_template("results.html", recipes=results, no_results_message=no_results_message)


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
# Route: /predict
# Handles image upload and predicts the recipe using a pre-trained model.
# ------------------------------------------------------------------------------
@app.route("/predict", methods=["POST"])
def predict():
    f = request.files.get("image")
    if not f:
        return ("No file", 400)
    pil = Image.open(f.stream)
    preds = predict_topk(pil, k=3)
    best, conf = preds[0]
    result = {"top3": preds, "label": best, "confidence": conf}
    if conf < 0.06:
        result["label"] = "Unknown"
    return render_template("prediction.html", result=result)


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
