import unittest
from io import BytesIO
from PIL import Image

from utils.image_predictor import predict_topk
from main import app


class TestUC015ImagePrediction(unittest.TestCase):
    """
    UC-015: Image-Based Recipe Identification
    Tests model inference and the /predict upload route.
    """

    def setUp(self):
        self.client = app.test_client()
        print("\n[Setup] Flask test client created for UC-015.")
        print("=" * 60)

    # ----------------------------------------------
    # UNIT-LEVEL TESTS (image_predictor.py)
    # ----------------------------------------------
    def test_predict_topk_with_dummy_image(self):
        """
        Ensures predict_topk() runs end-to-end on a synthetic image.
        Confirms model loads, preprocesses, and returns top-k predictions.
        """
        print("\n[Test] predict_topk() with dummy generated image")

        # Create a solid-color 224x224 RGB image
        img = Image.new("RGB", (224, 224), color=(200, 150, 100))

        preds = predict_topk(img, k=3)

        self.assertIsInstance(preds, list)
        self.assertEqual(len(preds), 3)
        self.assertIsInstance(preds[0][0], str)       # label
        self.assertIsInstance(preds[0][1], float)     # probability

        print("- ONNX model executed successfully.")
        print(f"- Returned top-3 predictions: {preds}")
        print("-" * 60)

    # ----------------------------------------------
    # ROUTE-LEVEL TESTS (main.py /predict)
    # ----------------------------------------------
    def test_predict_route_with_valid_image(self):
        print("\n[Test] /predict route with valid uploaded image")
      
        img = Image.new("RGB", (224, 224), color="red")
        buf = BytesIO()
        img.save(buf, format="JPEG")
        buf.seek(0)
      
        response = self.client.post(
            "/predict",
            data={"image": (buf, "test.jpg")},
            content_type="multipart/form-data"
        )
      
        self.assertEqual(response.status_code, 200)
      
        # Accept either "top 3" section or "unknown"
        self.assertTrue(
            b"top 3" in response.data.lower() or b"unknown" in response.data.lower()
        )
      
        print("- /predict accepted file and returned prediction page successfully.")
        print("-" * 60)
      

    def test_predict_route_missing_file(self):
        """
        Ensures /predict returns 400 when no file is uploaded.
        """
        print("\n[Test] /predict route missing file")

        response = self.client.post("/predict", data={})
        self.assertEqual(response.status_code, 400)

        print("- Missing file handled correctly (400 returned).")
        print("-" * 60)


if __name__ == "__main__":
    unittest.main()
