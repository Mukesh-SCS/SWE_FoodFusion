# ================================================================================
# DESCRIPTION:
#     Hybrid Recipe Recommender System
#     --------------------------------
#     This module suggests top recipes by comparing user-input ingredients
#     with recipe data using TF-IDF (Term Frequency–Inverse Document Frequency)
#     and cosine similarity. It includes preprocessing, caching for performance,
#     and weighted scoring for diet, difficulty, and cooking time filters.
#     (TF-IDF converts words into importance scores so the computer can understand which ingredients actually define a dish.)
#
# USAGE:
#     from utils.recommender import recommend
#     results = recommend("chicken tomato", recipes, top_n=5, diet="Non-Vegetarian")
#
# OUTPUT:
#     Returns a list of recipe dictionaries ranked by similarity score,
#     each including an additional "similarity" field (0–1 float).
#
# ARGUMENTS:
#     query (str)        : User's ingredient input string.
#     recipes (list)     : List of recipe dictionaries.
#     top_n (int)        : Number of results to return (default=5).
#     diet (str)         : Optional diet filter (e.g., "Vegan", "Vegetarian").
#     difficulty (str)   : Optional difficulty filter.
#     time_limit (int)   : Optional max cooking time in minutes.
#
# PERFORMANCE NOTES:
#     - TF-IDF matrix is cached using @lru_cache for faster repeated searches.
#     - Text is normalized for cleaner token matching.
#     - Weighted adjustments improve recommendation relevance.
#
# Author Info: SWE_FOODFUSION Team
# ================================================================================

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from functools import lru_cache


# ------------------------------------------------------------------------------
# TEXT CLEANING
# ------------------------------------------------------------------------------
def clean_text(text):
    """
    Normalize text for TF-IDF processing.
    - Converts to lowercase
    - Removes punctuation and non-alphabetic characters
    - Strips extra spaces
    """
    text = re.sub(r"[^a-zA-Z\s]", "", str(text).lower())
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ------------------------------------------------------------------------------
# TF-IDF CACHING
# ------------------------------------------------------------------------------
@lru_cache(maxsize=1)
def get_vectorizer(recipes_joined):
    """
    Cache the TF-IDF model to avoid recomputation on every search.
    Input: tuple of cleaned recipe ingredient strings
    Output: fitted vectorizer and TF-IDF matrix
    """
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(recipes_joined)
    return vectorizer, tfidf_matrix


# ------------------------------------------------------------------------------
# MAIN RECOMMENDER
# ------------------------------------------------------------------------------
def recommend(query, recipes, top_n=5, diet=None, difficulty=None, time_limit=None):
    """
    Generate top recipe recommendations using text similarity and user filters.
    Combines:
        - Ingredient-based cosine similarity
        - Optional weighted adjustments for diet, difficulty, and time
    """
    # Handle invalid or empty input
    if not isinstance(query, str):
        return []
    query = query.strip()
    # --------------------------------------------------------------------------
    # STEP 1: Prepare and clean recipe ingredient text
    # --------------------------------------------------------------------------
    docs = [" ".join(r.get("ingredients", [])) for r in recipes]
    docs = [clean_text(d) for d in docs]

    # --------------------------------------------------------------------------
    # STEP 2: Build or reuse TF-IDF representation
    # --------------------------------------------------------------------------
    vectorizer, tfidf_matrix = get_vectorizer(tuple(docs))

    # --------------------------------------------------------------------------
    # STEP 3: Transform user query and compute cosine similarity
    # --------------------------------------------------------------------------
    query_vec = vectorizer.transform([clean_text(query)])
    sim_scores = cosine_similarity(query_vec, tfidf_matrix).flatten()

    # --------------------------------------------------------------------------
    # STEP 4: Apply weight adjustments based on filters
    # --------------------------------------------------------------------------
    results = []
    for i, r in enumerate(recipes):
        score = sim_scores[i]

        # Diet match adds +10%
        if diet and r.get("diet", "").lower() == diet.lower():
            score *= 1.10

        # Difficulty match adds +5%
        if difficulty and r.get("difficulty", "").lower() == difficulty.lower():
            score *= 1.05

        # Time match: closer times get up to +10%
        if time_limit:
            try:
                t = int(r.get("time", 9999))
                if t <= int(time_limit):
                    score *= 1.10 - (t / int(time_limit)) * 0.05
            except Exception:
                pass

        # Keep only positively scored recipes
        if query.strip() == "" or score > 0:
            recipe = r.copy()
            recipe["similarity"] = round(float(score), 3)
            results.append(recipe)


    # --------------------------------------------------------------------------
    # STEP 5: Rank and return top N recipes
    # --------------------------------------------------------------------------
    results = sorted(results, key=lambda x: x["similarity"], reverse=True)
    return results[:top_n]
