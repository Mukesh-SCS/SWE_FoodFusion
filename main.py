# ================================================================================
# DESCRIPTION:
#     This Flask web application recommends recipes based on user-input ingredients,
#     diet preferences, difficulty, and cooking time. It loads recipe data from a
#     local JSON dataset and displays matching recipes along with random local images.
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
from flask import send_from_directory
from utils.data_loader import load_recipes_json
from utils.recommender import recommend
import os, random

# Initialize the Flask application
app = Flask(__name__)

# --- Load all Food-101 based recipes ---
recipes = load_recipes_json("dataset/recipes.json")



@app.route('/dataset/<path:filename>')
def serve_dataset(filename):
    """
    Function: serve_dataset
    Purpose: Serve static files (like images) from the 'dataset' directory.
    Input: filename (string) - requested file path.
    Output: Sends the file back to the browser.
    """
    return send_from_directory('dataset', filename)

# --- Helper: pick correct local image per recipe ---
def get_local_image(recipe_name):
    """
    Function: get_local_image
    Purpose: Pick a random image from a folder matching the recipe name.
    Input: recipe_name (string) - name of the recipe.
    Output: Returns a relative image path string or None if not found.
    """
    folder = os.path.join("dataset", "extracted_images", recipe_name)
    if not os.path.exists(folder):
        return None
    # Find image files in the folder
    files = [f for f in os.listdir(folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    if not files:
        return None
    chosen = random.choice(files)
    return f"/dataset/extracted_images/{recipe_name}/{chosen}"

@app.route("/")
def index():
    """
    Function: index
    Purpose: Render the home page where users can search recipes.
    Output: Returns index.html template.
    """
    return render_template("index.html")

@app.route("/view/<int:recipe_id>")
def view_recipe(recipe_id):
    """
    Function: view_recipe
    Purpose: Display full recipe details for a given recipe ID.
    Input: recipe_id (int) - unique recipe identifier.
    Output: Renders view.html with full recipe info.
    """
    recipe = next((r for r in recipes if r["id"] == recipe_id), None)
    if not recipe:
        return "Recipe not found", 404

    #Load image for the specific recipe
    from main import get_local_image  # only if outside function scope
    recipe["image"] = get_local_image(recipe["name"])

    return render_template("view.html", recipe=recipe)

@app.route("/search", methods=["POST"])
def search():
    """
    Function: search
    Purpose: Handle recipe search requests from the form input.
    Steps:
      1. Collect user inputs (ingredients, diet, difficulty, time)
      2. Call recommend() to find similar recipes
      3. Attach corresponding images
      4. Apply filters for diet, difficulty, and time
    Output: Renders results.html with a list of filtered recipes.
    """
    query = request.form.get("ingredients", "")
    diet = request.form.get("diet", "")
    difficulty = request.form.get("difficulty", "")
    time_limit = request.form.get("time", "")

   # Step 1: Recommend recipes using text similarity
    results = recommend(query, recipes)

    # Step 2: Attach random local images to each result
    for r in results:
        r["image"] = get_local_image(r["name"])

     # Step 3: Apply user-selected filters
    if diet:
        results = [r for r in results if r.get("diet") == diet]
    if difficulty:
        results = [r for r in results if r.get("difficulty") == difficulty]
    if time_limit:
        results = [r for r in results if r.get("time", 9999) <= int(time_limit)]
    
    # Step 4: Display results in the template
    return render_template("results.html", recipes=results)


if __name__ == "__main__":
    # Run Flask server in debug mode for local development
    app.run(debug=True)
