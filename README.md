# RecipeRover - A recipe recommender tool

## Overview

This project aims to provide personalized recipe recommendations based on the user's preferences and the content of the recipes. It utilizes a content-based recommendation system to suggest similar recipes based on their features such as cuisine, course, diet, preparation time, cooking time, total time, servings, ingredients, and equipment. The project is also available to view and interact.

[🍵🧆🍲 Recipe Rover 🥘🥣🥧](https://reciperover.streamlit.app)


## Files

- **Data Scraping**: Jupyter notebook to crawl every page and scrape the recipes information for the dataset.
- **Data Cleaning and Preprocessing**: Jupyter Notebook containing the code for cleaning and preprocessing the recipe dataset.
- **Data Modelling**: Jupyter notebook for building a content-based recommendation model and saving it.
- **Model**: Directory containing the saved recommendation model (`model_pickle.pkl`).
- **Data**: Directory containing the raw and cleaned recipe datasets (`Recipes.csv` and `Recipes_Clean.csv`).
- **App**: Python script for Streamlit web application code to deploy the recommendation model.


## Overview

The project consists of the following components:

1. **Data Scraping (`Data Scraping.ipynb`)**:
   - This Jupyter Notebook scrapes recipe data from archanaskitchen.com
   - It extracts all the information such as recipe names, ingredients, cooking time, etc from all the recipes.
   - The scraped data is saved in a CSV file for further processing.

2. **Data Cleaning and Preprocessing (`Data Cleaning and Preprocessing.ipynb`)**:
   - This notebook focuses on cleaning and preprocessing the scraped recipe data.
   - It removes irrelevant columns, handles missing values, merging similar cuisines, and standardizes the format of features.
   - The cleaned data is saved in another CSV file for modeling.

3. **Data Modeling (`Data Modeling.ipynb`)**:
   - This Python script builds a content-based recommendation model for recipes.
   - It utilizes TF-IDF vectorization and cosine similarity to recommend similar recipes based on the selected relevant features.
   - The model is trained on the cleaned dataset and saved using pickle.

4. **Recipe Recommender Web App (`app.py`)**:
   - The trained model is deployed as a web application using Streamlit.
   - Users can input a recipe name, and the app will recommend similar recipes based on the model.
   - The web application is hosted [here](https://reciperover.streamlit.app).