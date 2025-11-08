import unittest
from main import app

class TestUC006ViewRecommendedRecipes(unittest.TestCase):
    """
    UC-006: View Recommended Recipes
    Tests that main Flask routes render correctly and contain expected content.
    """

    def setUp(self):
        self.client = app.test_client()
        print("\n[Setup] Flask test client created for UC-006.")
        print("=" * 60)

    def test_homepage_status_ok(self):
        print("\n[Test] Homepage Status Check")
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertTrue(len(r.data) > 0)
        print("- Homepage loaded successfully with status 200 and non-empty content.")
        print("-" * 60)

    def test_search_post_with_ingredient(self):
        print("\n[Test] Search Route Check")
        r = self.client.post("/search", data={"ingredients": "chicken"})
        self.assertEqual(r.status_code, 200)
        self.assertIn(b"recipe", r.data.lower())
        print("- Search POST handled successfully, recipe content displayed.")
        print("-" * 60)

    def test_view_recipe_by_id(self):
        print("\n[Test] View Recipe by ID Check")
        r = self.client.get("/view/0")
        self.assertIn(r.status_code, [200, 404])
        if r.status_code == 200:
            self.assertIn(b"ingredients", r.data.lower())
            print("- Recipe page loaded with ingredient details.")
        else:
            print("- Recipe not found (404) handled correctly.")
        print("-" * 60)

if __name__ == "__main__":
    unittest.main()
