# SWE_FoodFusion
SWE Group Project : FoodFusion 

# Recipe Recommendation Web Application
Overview
A recipe recommendation web application built with **Flask** and **Python**.  
It suggests recipes based on user-provided ingredients, dietary preferences, and cooking time.  
The app also displays real food images from the **Food-41** dataset (downloaded manually from Kaggle).

# Features

- Search recipes by ingredients  
- Filter by diet type (vegetarian, vegan, etc.) and time  
- View detailed recipe pages with images  
- Automatically loads Food-41 image dataset from Kaggle  
- Lightweight recommendation engine using TF-IDF and cosine similarity 
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
   git clone https://github.com/<your-username>/SWE_FoodFusion.git
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
# Open in browser: localhost by running main.py 
```
python main.py

```

# 🔑 Dataset Setup (Manual Download)

- This app uses the Food-41 dataset for food images.

1. Go to Food-41 Dataset on Kaggle
2. Click Download (requires a Kaggle account).
3. Extract the downloaded archive and locate the file:
   - ./dataset/food_c101_n1000_r384x384x3.h5
   

- 🛑 Notes: The .h5 dataset file is large (~600 MB). Do not push it to GitHub.
            Add this line to your .gitignore:
```bash
dataset/*.h5
```
- Used extract_imagesFromh5.py to extract all image from .h5 to appear corectly.
# Run the Application
```bash
python main.py

```
- Open your browser at: http://127.0.0.1:5000/


# TECH USING 
- Python: Flask, pandas, numpy, scikit-learn
- Frontend: HTML, CSS
- KaggleHub: dataset 
- h5py: image reading
- TF-IDF + Cosine Similarity: recommendation algorithm


# License
For educational use only.
Dataset © Kaggle / Food-41