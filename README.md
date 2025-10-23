# SWE_FoodFusion
SWE Group Project : FoodFusion 

## 🍽️ Recipe Recommendation Web Application
A Flask-based recipe recommender that suggests dishes based on your available ingredients, dietary preferences, and cooking time.  
It uses a **Kaggle recipe dataset (with real images)** and a lightweight AI-powered recommendation engine (TF-IDF + cosine similarity).

## Features
- Search recipes by ingredients  
- Filter by **Diet Type** (Vegan, Vegetarian, Non-Vegetarian, etc.)  
- Filter by **Cooking Time**  
- View full recipe details with real images  
- “Today’s Specials” carousel  
- AI-enhanced dataset processing (auto diet + time detection)
- Uploadimage to get food name ( AI train Mobilenet CNN model)


# Project Structure
```
recipe_recommendation/
│
├── main.py                         # Main Flask app
├── requirements.txt                # Dependencies
├── CHANGELOG.md                    # CHANGELOG
├── dataset/                 
│ └── recipes.json                  # Recipe dataset (text)
│ └── food_c101_n1000_r384x384x3.h5 # Image dataset (auto-downloaded)
├── templates/
│ ├── index.html                # Search form
│ ├── results.html              # Search results
│ └── recipe.html               # Single recipe page
│ └── upload.html               # Image upload and AI prediction page 
├── static/
│ └── style.css                 # Styling
└── utils/
  └──data_loader.py            # JSON/HDF5 loaders
  └──recommender.py            # Recommendation logic
  └── image_predictor.py       # AI model for dish prediction 
  └── train_model.py           # Trains CNN on Food-41 and saves model.h5

```

# Installation

1. **Clone the repository**
```bash
   git clone https://github.com/Mukesh-SCS/SWE_FoodFusion.git
   cd SWE_FoodFusion
```

2. **Create and activate a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate       # Windows
# or
source venv/bin/activate    # macOS/Linux

```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

#  Dataset Setup (Manual Download)

This project uses the “Food Ingredients and Recipe Dataset with Images” from Kaggle.
To keep the GitHub repo lightweight, images are not included.

# Download from Google Drive
- Download the zipped image dataset from Google Drive:
  Link:https://drive.google.com/drive/folders/16xwFuG0FliCA_xMUbknFCk-VeJ-cVT23?usp=sharing
- Extract it.
- Move the extracted folder into:
```
SWE_FoodFusion/static/food_images/
```

# Run the Application
```bash
python main.py

```
- Open your browser at: http://127.0.0.1:5000/


# TECH USING 
- Backend: Python (Flask, pandas, numpy, scikit-learn)
- Frontend: HTML, CSS
- Data: CSV dataset from Kaggle
- Model: TF-IDF + Cosine Similarity


# License
For academic and educational use only.
Dataset © Kaggle / Original creators.
Food Ingredients and Recipes Dataset with Images: Link (https://www.kaggle.com/datasets/pes12017000148/food-ingredients-and-recipe-dataset-with-images/data)
Code © SWE_FoodFusion Team.