import h5py
import os
from PIL import Image
import numpy as np

h5_path = "dataset/food_c101_n1000_r384x384x3.h5"
output_dir = "dataset/extracted_images"
os.makedirs(output_dir, exist_ok=True)

with h5py.File(h5_path, "r") as f:
    images = f["images"]
    categories = f["category"][:]           # shape (1000, 101)
    category_names = [name.decode("utf-8") for name in f["category_names"][:]]

    print("Extracting images...")
    for i in range(len(images)):
        # Convert one-hot to index
        class_index = np.argmax(categories[i])
        class_name = category_names[class_index].strip()

        # Create directory per class
        class_dir = os.path.join(output_dir, class_name)
        os.makedirs(class_dir, exist_ok=True)

        # Save image
        img = Image.fromarray(images[i].astype(np.uint8))
        img_path = os.path.join(class_dir, f"{class_name}_{i}.jpg")
        img.save(img_path)

print("Extraction complete. Images saved under:", output_dir)
