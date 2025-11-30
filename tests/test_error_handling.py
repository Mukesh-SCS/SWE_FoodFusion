import unittest
from utils.data_loader import suggest_no_results


class TestUC008ErrorHandling(unittest.TestCase):

    def test_no_ingredients_no_filters(self):
        """
        If no ingredients and no filters are provided, we should get
        the broad 'add ingredients or remove filters' message.
        """
        msg = suggest_no_results(ingredients=None, filters=None)

        self.assertIn("No recipes found.", msg)
        self.assertIn("Try adding 1–3 ingredients", msg)
        self.assertIn("Check spelling", msg)

    def test_many_ingredients(self):
        """
        If 5 or more ingredients are provided, we should be told to remove some.
        """
        msg = suggest_no_results(
            ingredients=["chicken", "tomato", "onion", "garlic", "basil"],
            filters=None
        )

        self.assertIn("No recipes found.", msg)
        self.assertIn("Try removing some ingredients", msg)
        self.assertIn("Check spelling", msg)

    def test_some_ingredients_with_filters(self):
        """
        For 1–4 ingredients + filters, we should see the 'add a few more' text
        AND guidance about disabling filters.
        """
        msg = suggest_no_results(
            ingredients="chicken, tomato",   # also tests string input
            filters={"diet": "vegetarian", "max_time": 15}
        )

        self.assertIn("No recipes found.", msg)
        self.assertIn("Try adding a few more ingredients", msg)
        self.assertIn("Also try disabling strict dietary/time filters", msg)
        self.assertIn("Check spelling", msg)


if __name__ == "__main__":
    unittest.main()
