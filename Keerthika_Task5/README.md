# Task 5: House Price Prediction System

# Project Overview
* This project is an interactive Streamlit-based Machine Learning web application that predicts house prices using multiple regression models and provides geospatial visualization of real estate data.
* The system is designed to simulate a real-world AI-powered real estate analytics platform where users can input housing parameters, compare different machine learning models, evaluate performance metrics, and visualize property price distribution on a geographic map.
* The application integrates end-to-end machine learning workflow including data preprocessing, feature engineering, model training, evaluation, and interactive visualization.

# Objective
The main objectives of this project are:

* To build a predictive model for estimating house prices
* To compare multiple regression algorithms and analyze their performance
* To preprocess and clean real-world structured housing data
* To develop an interactive dashboard using Streamlit
* To visualize model predictions and evaluation results
* To integrate geospatial visualization using Folium heatmaps
* To enhance user understanding of real estate price patterns

# Technologies Used
* Python – Core programming language
* Streamlit – Web application framework for dashboard
* Pandas – Data manipulation and analysis
* NumPy – Numerical computations
* Matplotlib – Data visualization
* Seaborn – Statistical visualizations
* Scikit-learn – Machine learning models and preprocessing
* Folium – Geospatial mapping and heatmaps
* Streamlit-Folium – Embedding interactive maps in Streamlit

# Dataset Description
The dataset used in this project is housing.csv, which contains various features influencing house prices.

### Typical features include:
Area (square footage)
Number of bedrooms
Parking availability
Furnishing status
Location-based attributes
Other structural and lifestyle-related features

### Data preprocessing steps include:
Removal of missing values
Conversion of categorical variables into numerical format
One-hot encoding for categorical columns
Feature scaling using StandardScaler

# Features
### 🏠 1. House Price Prediction Module
This module allows users to input property details through an interactive form.

Users can:
Enter numerical values such as area, bedrooms, and parking
Select binary/categorical attributes (yes/no encoded features)
Adjust values using sliders and number inputs
Get instant prediction results

Output:
Predicted house price in INR (₹) formatted using Indian numbering system (lakhs/crores style)

### 🤖 2. Machine Learning Model Selection
Users can choose between multiple regression models:

Linear Regression – Baseline model for prediction
Ridge Regression – Regularized model to reduce overfitting
Lasso Regression – Feature selection-based regression model

Each model is trained dynamically and evaluated in real-time based on user selection.

### 📊 3. Model Evaluation & Analytics
The analytics module provides:

R² Score – Measures how well the model explains variance
Mean Squared Error (MSE) – Measures prediction error
Actual vs Predicted Plot – Visual comparison of model performance
Feature Importance Plot – Shows influence of each feature on price prediction

This helps users understand model behavior and reliability.

### 🔥 4. Feature Importance Analysis
The system extracts coefficients from regression models to identify:

Most influential features (positive impact on price)
Least influential or negatively correlated features
Relative importance of each variable

This is visualized using horizontal bar charts.

### 🌍 5. Geospatial Visualization Module
A simulated geo-visualization layer is created using latitude and longitude values.

Features include:
Interactive Folium map centered on a specific region
Heatmap showing density of high and low-priced properties
Circle markers representing individual houses
Popups displaying predicted/actual house prices

This helps in understanding spatial distribution of real estate prices.

### 📈 6. Data Handling & Preprocessing Pipeline
The dataset undergoes multiple preprocessing steps:

Missing Value Handling:
Rows with null values are removed for clean modeling

Categorical Encoding:
Yes/No values → 1/0 conversion
One-hot encoding applied for multi-class categorical variables

Feature Scaling:
StandardScaler is applied to normalize features
Ensures all variables contribute equally to model training

# Methodology

### 1. Data Loading
The housing dataset is loaded using Pandas and inspected for missing or inconsistent values.

### 2. Data Cleaning
Null values are removed to ensure model stability
Categorical variables are converted into numerical format
One-hot encoding is applied to transform categorical columns

### 3. Feature Engineering
Irrelevant or redundant features are removed
Binary variables are standardized
Feature set is prepared for machine learning models

### 4. Data Scaling
StandardScaler is applied to normalize all features
This ensures uniform contribution of variables in regression models

### 5. Model Training
Dataset is split into training (80%) and testing (20%) sets
Multiple regression models are trained separately
User selects model dynamically from dashboard

### 6. Prediction System
User inputs are collected through Streamlit UI
Inputs are transformed using trained scaler
Model predicts house price in real-time

### 7. Model Evaluation
Performance is evaluated using:
R² Score
Mean Squared Error
Visual comparison plots (Actual vs Predicted)

### 8. Geospatial Visualization
Synthetic latitude and longitude values are generated
Heatmap is created using Folium
Price intensity is visualized geographically

# Key Insights
* House area is one of the strongest predictors of price
* Location-based visualization improves interpretation of price distribution
* Ridge and Lasso models help control overfitting and improve generalization
* Feature engineering significantly impacts model accuracy
* Interactive dashboards improve accessibility and understanding of ML systems
* Geospatial representation adds real-world context to predictions

# Project Structure

```
Keerthika_Task5/
├── Keerthika_Task5.py
├── housing.csv
├── requirements.txt
├── README.md
├── screenshots/
```

# Conclusion
* This project demonstrates a complete end-to-end Machine Learning pipeline integrated into an interactive web application.
* It showcases how regression models can be used for real-world prediction tasks while combining data preprocessing, model evaluation, and geospatial visualization.
* The project also highlights the importance of interactive dashboards in making machine learning systems more interpretable and user-friendly.

# Future improvements may include:
Integration with real estate APIs for live data
Advanced models like XGBoost or Random Forest
Deployment on cloud platforms like Streamlit Cloud or AWS
Improved geographic accuracy using real coordinates

# Author
**Keerthika.S**
B.Tech Artificial Intelligence and Data Science,
Oasis Infobyte Data Analyst Internship (OIBSIP)

