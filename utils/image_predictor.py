# ================================================================================
# DESCRIPTION:
#     This module loads a trained ONNX model and performs image-based food
#     classification. It preprocesses uploaded dish images, runs inference
#     with ONNX Runtime, and returns the top-k predicted dish names.
#
# USAGE:
#     from utils.image_predictor import predict_topk
#     preds = predict_topk(PIL.Image.open("sample.jpg"), k=3)
#
# INPUTS:
#     - Trained ONNX model: models/foodfusion_mnv2.onnx
#     - Label file: models/labels.txt
#
# OUTPUTS:
#     - List of (label, probability) pairs for top-k predictions.
#
# DEPENDENCIES:
#     onnxruntime, numpy, Pillow
#
# Author Info: SWE_FOODFUSION Team
# ================================================================================

import os
import numpy as np
from PIL import Image
import onnxruntime as ort

# --- Paths ---
MODEL_PATH = "models/foodfusion_mnv2.onnx"
LABELS_PATH = "models/labels.txt"

# --- Internal cached objects ---
_session = None
_input_name = None
_labels = None


def _init():
    """Initialize ONNX session and load labels once."""
    global _session, _input_name, _labels
    if _session is not None:
        return

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"ONNX model not found: {MODEL_PATH}")
    if not os.path.exists(LABELS_PATH):
        raise FileNotFoundError(f"Labels file not found: {LABELS_PATH}")

    _session = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])

    # Get model input name automatically
    try:
        _input_name = _session.get_inputs()[0].name
    except Exception:
        _input_name = "input"

    # Load label list
    with open(LABELS_PATH, "r", encoding="utf-8") as f:
        _labels = [line.strip() for line in f if line.strip()]

    print(f"✅ ONNX model loaded ({len(_labels)} classes)")


def _preprocess(pil_img, size=(224, 224)):
    """Convert a PIL image to model input array."""
    img = pil_img.resize(size).convert("RGB")
    arr = np.asarray(img, dtype=np.float32) / 255.0
    arr = np.expand_dims(arr, 0)  # shape: [1, H, W, C]
    return arr


def predict_topk(pil_img: Image.Image, k: int = 3):
    """
    Predict the top-k class labels for a PIL image.

    Returns:
        List of (label:str, probability:float)
    """
    _init()
    x = _preprocess(pil_img)
    preds = _session.run(None, {_input_name: x})[0][0]  # output shape: [num_classes]
    idxs = preds.argsort()[-k:][::-1]
    return [(_labels[i], float(preds[i])) for i in idxs]
