# ================================================================================
# DESCRIPTION:
#     This module implements a simple recipe recommendation system based on
#     text similarity. It compares user-provided ingredients with recipe data
#     using TF-IDF (Term Frequency–Inverse Document Frequency) and cosine similarity.
#
# USAGE:
#     Import and call the recommend() function:
#         from utils.recommender import recommend
#         recommendations = recommend("chicken tomato", recipes)
#
# OUTPUTS:
#     - Returns a list of recipe dictionaries ranked by similarity score.
#
# ARGUMENTS:
#     - query (str): User input ingredients.
#     - recipes (list): List of recipe dictionaries.
#     - top_n (int): Number of top recommendations to return.
#
# Author Info: Code written by SWE_FOODFUSION Team
# ================================================================================


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend(query, recipes, top_n=5):
    """
    Function: recommend
    Purpose: Suggest top recipes based on ingredient similarity.
    Inputs:
        query (str): User input ingredients (e.g., "chicken onion garlic").
        recipes (list): List of recipe dictionaries from the dataset.
        top_n (int): Maximum number of recipes to return (default = 5).
    Outputs:
        Returns a list of recipe dictionaries most similar to the user's query.
    Steps:
        1. Combine ingredients from each recipe into text strings.
        2. Append the user's query as a new document.
        3. Use TF-IDF vectorization to represent all text numerically.
        4. Compute cosine similarity between the query and all recipes.
        5. Rank recipes by similarity score and return the top matches.
    """

    # Step 1: Create a list of ingredient strings for each recipe
    docs = [" ".join(r.get("ingredients", [])) for r in recipes]
    docs.append(query)

    # Step 2: Convert all text into TF-IDF vectors
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(docs)
    
    # Step 3: Compute cosine similarity between user query and recipes
    cos_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    scores = cos_sim.flatten()

    # Step 4: Sort recipes by similarity (highest first)
    ranked_indices = scores.argsort()[::-1]
    
    # Step 5: Select top N results with positive similarity scores
    results = [recipes[i] for i in ranked_indices[:top_n] if scores[i] > 0]
    return results
