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


