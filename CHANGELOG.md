# CHANGELOG.md  
**Project:** Recipe Recommendation Web App  

```bash
## Format
## vX.X.X  - YYYY-MM-DD
### Added 
### Changed 
### Fixed
- ( short bullet points )
```
----------------------------------------------------------------------------------------
## v1.8.1 – 2025-11-15
### Fixed 
- Fixed the main.py code for uploading and analyze the AI result page 

## v1.8.0 – 2025-11-07
### Added 
- @Leon

## v1.7.0 – 2025-11-07
### Changed
- Changed `recommender.py`includes preprocessing, caching for performance, and weighted scoring for diet, difficulty, and cooking time filters.

## v1.6.1 – 2025-11-06
### Changed
- Changed the layout for the `Today's Special` feature , make it responsive according to screen size
- Add the neon light around circle to look more attractive 

## v1.6.0 – 2025-11-05
### Added
- Added `train_from_csv.py` for CSV-based image training using MobileNetV2
- Added `convert_to_onnx.py` to export .h5 → .onnx for ONNX Runtime inference
- Added `image_predictor.py` for fast ONNX-based predictions
- Added responsive Upload Food Image button and Font Awesome camera icon to homepage

## Fixed
- Added .jpg extension handling for image paths
- Filtered out single-sample classes to prevent stratify errors
- Synced label mappings between training and validation generators
- Replaced deprecated train_gen.num_classes with len(train_gen.class_indices)
- Fixed the Diet and time display for recipe view.

## Updated
- Improved responsive CSS layout with media queries
- Cleaned and documented all scripts with clear headers and usage details
- Updated requirements.txt with stable versions and comments

## v1.5.0  - 2025-10-25
### Added 
- Added Download as PDF to view page
- Updated header to add logo. onclick logo returns to homepage
- Removed Save button from results page

## v1.4.0  - 2025-10-23
### Added 
- Added view recipe detail using csv datafile
- Added recipe data with real image mapping

### Changed
- Changed the dataset from .json to .csv.


## v1.3.0  - 2025-10-22
### Added 
- Added get_today_specials() in main.py to show 5 random daily recipes.
- Updated / route to pass specials list to template, update the style.css and index.html
- Added the logo for SWE_FoodFusion

## v1.2.0 - 2025-10-07
### Added
- Improved `recommender.py` with text cleaning, lemmatization, and better matching.
- Added detailed comments and file headers for learning clarity.
- Added similarity score output for each recommended recipe.
- Added `/dataset/<filename>` route to serve images from dataset.

### Changed
- Now uses only local data files (`recipes.json`, `.h5`).
- Cleaned up `main.py`
- Updated `README.md` for simpler setup.

### Fixed
- Recipe detail page image loading issue.
- Filters for diet, difficulty, and time not applying correctly.

---

## v1.1.0 - 2025-9-30
### Added
- `view.html` page for viewing full recipe details.
- Random image loading per recipe.
- Basic filters for diet, difficulty, and cooking time.

### Changed
- Switched from CSV to JSON dataset.
- Updated homepage with dropdown filters.

---

## v1.0.0 - 2025-09-15
### Initial Release
- Basic Flask web app with recipe search by ingredients.
- Simple TF-IDF recommender.
- HTML frontend (`index.html`, `results.html`).
- JSON dataset for recipes.

---


