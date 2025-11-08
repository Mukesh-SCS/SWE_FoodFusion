# SWE_FoodFusion – Test Execution Guide

This document explains how to set up and run all unit tests for the **Recipe Recommendation Web Application**.  
Tests cover both UC-001 and UC-006

---

## Test Coverage
```bash
-----------------------------------------------------------------------------------------------------
| Area               | File                   |        Purpose                                      |
|--------------------|------------------------|-----------------------------------------------------| 
| UC-001             | `test_recommender.py`  | UC001: Ingredient-based search (recommend function) |
| UC-006             | `test_routes.py`       | UC006 Viewing recommended recipes (Flask routes)    |
| Data Loader        | `test_data_loader.py`  | Verifies dataset loading and structure              |
-----------------------------------------------------------------------------------------------------
```
---

## ⚙️ 1. Environment Setup

1. **Activate the virtual environment**
```bash
   venv\Scripts\activate

   (macOS/Linux: source venv/bin/activate)

```

2. **Install project dependencies**
```bash
    pip install -r requirements.txt
```


Note: No external testing tools required, Uses Python’s built-in unittest module.

- Flask-Testing can be installed for route checks.
```bash
pip install Flask-Testing
```

3. **How to Run Tests**

```bash 
python -m unittest discover -s tests
```


4. **Notes**
- Before running tests, ensure the dataset file `Food_Ingredients_and_Recipe_Dataset_with_Image_Name_Mapping.csv` exists inside the dataset/ folder.
- The Flask app (main.py) should not be running while tests execute.
- The tests use Flask’s test_client() internally.
- After each code change, re-run all tests to confirm stability.


**Author: SWE_FoodFusion Team**
**Course: COSC612 – Software Engineering 1**
**Version: Test Guide v1.0**