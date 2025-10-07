# SWE_FoodFusion
SWE Group Project : FoodFusion 

# Recipe Recommendation Web Application
Overview
This is a simple web application that recommends recipes based on user input such as available ingredients, dietary preferences, and cuisine type. 
The system uses a JSON dataset and a lightweight ML/AI filtering engine implemented in Python.

# Features

- Enter available ingredients to get recipe suggestions
- Filter recipes by dietary choice (vegetarian, vegan, etc.)
- View full recipe details (ingredients, steps, cooking time) using AI

# Simple web interface built with Flask

# Project Structure
```
recipe_recommendation/
│
├── main.py                   # Main Flask app
├── requirements.txt         # Dependencies for libary 
├── dataset/
│   └── recipes.json         # Recipe dataset
│   └── recipes_cusine.csv   # Recipe dataset
├── templates/
│   ├── index.html           # Home page with form
│   └── results.html         # Show recipe results
└── utils/
    └── recommender.py       # Simple recommendation logic


(more file will be added after discussion with group)

```

# Installation
```
Clone this repository
Install dependencies:
pip install -r requirements.txt

```


# Open in browser: localhost by running main.py 
```
python main.py

```

# TECH USING 
- Python (Flask)
- JSON (dataset storage)
- HTML, CSS (frontend)
