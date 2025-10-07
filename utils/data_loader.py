# ================================================================================
# DESCRIPTION:
#     This module handles loading recipe data and images for the Recipe Recommendation
#     Web Application. It provides helper functions to read JSON files and extract
#     images from HDF5 datasets in a browser-displayable format.
#
# USAGE:
#     Import the functions into other scripts such as main.py:
#         from utils.data_loader import load_recipes_json, load_image_from_h5
#
# OUTPUTS:
#     - Returns Python data structures (lists/dictionaries)
#     - Returns base64-encoded image strings for HTML rendering
#
# ARGUMENTS:
#     - path: File path to JSON or HDF5 datasets
#     - index: Image index within the HDF5 dataset
#
# Author Info: Code written by SWE_FOODFUSION Team
# ================================================================================

import json
import pandas as pd
import h5py
import numpy as np
from PIL import Image
import io
import base64


def load_recipes_json(path="dataset/recipes.json"):
    """
    Function: load_recipes_json
    Purpose: Load recipe information stored in JSON format.
    Input:
        path (str): Path to the recipes JSON file.
    Output:
        Returns a list of dictionaries containing recipe data.
    """
    with open(path, "r") as f:
        return json.load(f)

def load_image_from_h5(h5_path, index):
    """
    Function: load_image_from_h5
    Purpose: Load one image from an HDF5 dataset and convert it to a
             base64-encoded string so it can be embedded directly in HTML.
    Inputs:
        h5_path (str): Path to the HDF5 (.h5) file containing images.
        index (int): Index position of the image within the dataset.
    Outputs:
        Returns a string formatted as:
            "data:image/jpeg;base64,<encoded_image_data>"
    Steps:
        1. Open the HDF5 file.
        2. Access the 'images' dataset and retrieve the image at the given index.
        3. Convert the NumPy array into a Pillow Image object.
        4. Encode the image as base64 for web display.
    """
    with h5py.File(h5_path, 'r') as f:
        dataset = f['images']
        img_array = dataset[index]   # Extract the specific image as a NumPy array
        img = Image.fromarray(img_array.astype('uint8'))
        
         # Convert image to an in-memory byte buffer
        buf = io.BytesIO()
        img.save(buf, format="JPEG")

        # Encode the image in base64 for HTML embedding
        img_str = base64.b64encode(buf.getvalue()).decode("utf-8")
        return f"data:image/jpeg;base64,{img_str}"
