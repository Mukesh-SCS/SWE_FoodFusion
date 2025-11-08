import unittest
from utils.data_loader import load_recipes_csv

class TestDataLoader(unittest.TestCase):
    """
    Tests for the CSV data loader function.
    Checks file loading, structure, and error handling.
    """

    def setUp(self):
        # Load data once for all tests
        self.recipes = load_recipes_csv("dataset/Food_Ingredients_and_Recipe_Dataset_with_Image_Name_Mapping.csv")
        print("\n[Setup] Loaded", len(self.recipes), "recipes for data loader tests.")
        print("=" * 60)

    def test_returns_list(self):
        print("\n[Test] Data Loader Return Type")
        self.assertIsInstance(self.recipes, list)
        print("- Data loader returned a list successfully.")
        print("-" * 60)

    def test_each_item_is_dict(self):
        print("\n[Test] Data Structure Validation")
        self.assertTrue(all(isinstance(r, dict) for r in self.recipes))
        print("- All recipes are stored as dictionaries.")
        print("-" * 60)

    def test_recipe_fields_exist(self):
        print("\n[Test] Field Existence Check")
        keys = ["id", "name", "ingredients", "instructions", "image"]
        sample = self.recipes[0]
        for k in keys:
            self.assertIn(k, sample)
        print("- Sample recipe contains all required fields:", ", ".join(keys))
        print("-" * 60)

    def test_image_field_not_empty(self):
        print("\n[Test] Image Field Check")
        images = [r["image"] for r in self.recipes]
        self.assertTrue(all(isinstance(img, str) and len(img) > 0 for img in images))
        print("- All recipes have valid (non-empty) image paths.")
        print("-" * 60)

    def test_handles_missing_file(self):
        print("\n[Test] Missing File Handling")
        with self.assertRaises(FileNotFoundError):
            load_recipes_csv("dataset/non_existing.csv")
        print("- Correctly raised FileNotFoundError for missing dataset file.")
        print("-" * 60)

if __name__ == "__main__":
    unittest.main()
