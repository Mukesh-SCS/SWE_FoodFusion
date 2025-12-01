# ================================================================================
# DESCRIPTION:
#     This script converts a trained TensorFlow/Keras model (.h5) to the ONNX
#     format for faster inference using ONNX Runtime in production.
#
# USAGE:
#     python convert_to_onnx.py
#
# INPUTS:
#     - Trained Keras model: models/foodfusion_mnv2.h5
#
# OUTPUTS:
#     - Converted ONNX model: models/foodfusion_mnv2.onnx
#
# DEPENDENCIES:
#     tensorflow, tf2onnx
#
# Author Info: SWE_FOODFUSION Team
# ================================================================================


import tensorflow as tf
import tf2onnx
import os

# --- Paths ---
MODEL_H5 = "models/foodfusion_mnv2.h5"
MODEL_ONNX = "models/foodfusion_mnv2.onnx"

# --- Verify source model exists ---
if not os.path.exists(MODEL_H5):
    raise FileNotFoundError(f"TensorFlow model not found: {MODEL_H5}")

# --- Load the trained .h5 model ---
print(f"Loading model from {MODEL_H5} ...")
model = tf.keras.models.load_model(MODEL_H5)

# --- Define input spec (224x224 RGB) ---
spec = (tf.TensorSpec((None, 224, 224, 3), tf.float32, name="input"),)

# --- Convert to ONNX ---
print("Converting model to ONNX format...")
model_proto, _ = tf2onnx.convert.from_keras(model, input_signature=spec, output_path=MODEL_ONNX)

print(f"Conversion complete — ONNX model saved to: {MODEL_ONNX}")
