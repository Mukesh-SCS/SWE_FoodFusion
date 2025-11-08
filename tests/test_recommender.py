import unittest
from utils.data_loader import load_recipes_csv
from utils.recommender import recommend

class TestUC001IngredientSearch(unittest.TestCase):
    """
    UC-001: Ingredient-Based Search
    Ensures the recommender returns valid results for given ingredients.
    """

    @classmethod
    def setUpClass(cls):
        cls.recipes = load_recipes_csv("dataset/Food_Ingredients_and_Recipe_Dataset_with_Image_Name_Mapping.csv")
        print("\n[Setup] Loaded", len(cls.recipes), "recipes for UC-001 tests.")
        print("=" * 60)

    def test_search_with_real_ingredient(self):
        print("\n[Test] Search with Valid Ingredient")
        q = "chicken"
        results = recommend(q, self.recipes)
        self.assertTrue(len(results) >= 1, "Should return at least one recipe")
        print(f"- Found {len(results)} recipes for query '{q}'.")
        print(f"Top recipe: {results[0]['name']}")
        print("-" * 60)

    def test_search_with_empty_string(self):
        print("\n[Test] Search with Empty Input")
        q = ""
        results = recommend(q, self.recipes)
        self.assertEqual(results, [], "Empty query should return an empty list")
        print("- Empty query handled correctly, no results returned.")
        print("-" * 60)

    def test_search_with_unknown_word(self):
        print("\n[Test] Search with Unknown Word")
        q = "asdfghjkl"
        results = recommend(q, self.recipes)
        self.assertEqual(results, [], "Unknown term should return empty list")
        print("- Unknown word handled correctly, no matches found.")
        print("-" * 60)

if __name__ == "__main__":
    unittest.main()
