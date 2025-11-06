# ================================================================================
# DESCRIPTION:
#     This script trains a MobileNetV2-based deep learning model to classify food
#     images into their corresponding recipe names. It uses image paths and labels
#     defined in the CSV dataset and performs data augmentation, training, and
#     model saving.
#
# USAGE:
#     python utils/train_from_csv.py
#
# INPUTS:
#     - CSV file: dataset/Food_Ingredients_and_Recipe_Dataset_with_Image_Name_Mapping.csv
#     - Images: static/food_images/
#
# OUTPUTS:
#     - Trained model: models/foodfusion_mnv2.h5
#     - Label file: models/labels.txt
#
# DEPENDENCIES:
#     pandas, tensorflow, sklearn, Pillow
#
# Author Info: SWE_FOODFUSION Team
# ================================================================================

import os
import pandas as pd
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split

# --- Paths ---
CSV_PATH = "dataset/Food_Ingredients_and_Recipe_Dataset_with_Image_Name_Mapping.csv"
IMAGE_DIR = "static/food_images"

# --- Load CSV ---
df = pd.read_csv(CSV_PATH)

# --- Clean ---
df = df.dropna(subset=["Image_Name", "Title"])
df["Image_Path"] = df["Image_Name"].apply(lambda x: os.path.join(IMAGE_DIR, f"{x}.jpg"))
df = df[df["Image_Path"].apply(os.path.exists)]
print(f" Loaded {len(df)} valid image samples")


# Keep only existing images
df = df[df["Image_Path"].apply(os.path.exists)]
print(f" Loaded {len(df)} valid image samples")

# --- Remove rare classes (appear only once) ---
label_counts = df["Title"].value_counts()
df = df[df["Title"].isin(label_counts[label_counts > 1].index)]
print(f" After filtering, {len(df)} samples remain across {df['Title'].nunique()} classes")


# --- Train/test split ---
train_df, val_df = train_test_split(
    df,
    test_size=0.2,
    random_state=42
)

# --- Data generators ---
img_size = (224, 224)
batch_size = 32

datagen = ImageDataGenerator(
    rescale=1./255,
    horizontal_flip=True,
    rotation_range=10
)

train_gen = datagen.flow_from_dataframe(
    train_df,
    x_col="Image_Path",
    y_col="Title",
    target_size=img_size,
    batch_size=batch_size,
    class_mode="categorical"
)

val_gen = datagen.flow_from_dataframe(
    val_df,
    x_col="Image_Path",
    y_col="Title",
    target_size=img_size,
    batch_size=batch_size,
    class_mode="categorical",
    classes=list(train_gen.class_indices.keys())
)


# --- Build model ---
base = MobileNetV2(weights="imagenet", include_top=False, input_shape=img_size + (3,))
base.trainable = False

x = layers.GlobalAveragePooling2D()(base.output)
x = layers.Dropout(0.3)(x)
num_classes = len(train_gen.class_indices)
out = layers.Dense(num_classes, activation="softmax")(x)


model = models.Model(inputs=base.input, outputs=out)
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# --- Train ---
model.fit(train_gen, validation_data=val_gen, epochs=5)

# --- Save model ---
os.makedirs("models", exist_ok=True)
model.save("models/foodfusion_mnv2.h5")

with open("models/labels.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(train_gen.class_indices.keys()))

print(" Training complete — model saved to models/foodfusion_mnv2.h5")
