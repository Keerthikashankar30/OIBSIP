# Task 4: NYC Airbnb Data Cleaning Dashboard

## Project Overview

This project is an interactive **Streamlit dashboard** designed for data cleaning and exploratory data analysis of the NYC Airbnb dataset. It focuses on identifying and handling missing values, detecting outliers, removing duplicates, and improving overall data quality.

The dashboard provides an intuitive interface to explore data quality issues and visualize cleaning steps before and after preprocessing.

## Objective

* Perform data cleaning and preprocessing on Airbnb dataset
* Identify and handle missing values
* Detect and analyze outliers
* Remove duplicate records
* Evaluate dataset quality
* Compare data before and after cleaning
* Build an interactive dashboard using Streamlit

## Technologies Used

* Python
* Streamlit
* Pandas
* NumPy
* Plotly

## Features

### Dataset Overview

* View dataset structure
* Check number of rows and columns
* Identify missing values and duplicates

### Data Quality Analysis

* Data quality score calculation
* Visualization of valid vs missing data

### Missing Values Analysis

* Column-wise missing value detection
* Bar chart visualization

### Outlier Detection

* Box plot visualization for numeric features
* Interactive column selection

### Data Explorer

* Search functionality across dataset
* Filtered data view
* Summary statistics

### Data Cleaning

* Missing value imputation
* Duplicate removal
* Clean dataset preview
* Download cleaned dataset option

### Before vs After Cleaning

* Comparison of dataset quality
* Visual and tabular comparison of key metrics

## Methodology

### 1. Data Loading

The Airbnb dataset is uploaded by the user and loaded into the application using Pandas.

### 2. Data Filtering

Optional filters are applied for borough and room type selection.

### 3. Data Cleaning

* Missing numeric values are replaced with median values
* Categorical missing values are replaced with "Unknown"
* Duplicate records are removed

### 4. Data Quality Assessment

A quality score is calculated based on missing values and total dataset size.

### 5. Exploratory Data Analysis

Outliers, missing values, and data distributions are analyzed using visualizations.

### 6. Interactive Dashboard

A Streamlit-based interface allows users to explore data dynamically.

## Key Insights

* Significant missing values were identified in multiple columns
* Data cleaning improved dataset quality significantly
* Outliers were detected in numerical variables
* Filtering helps focus on specific regions and room types
* Cleaned dataset is more suitable for analysis and modeling

## Project Structure

```text id="airbnb-structure"
Keerthika_Task4/
├── Keerthika_TASK4.py
├── Airbnb_Dataset.csv
├── requirements.txt
├── README.md
└── screenshots/
```

## How to Run

Install dependencies:

```bash id="run-airbnb"
pip install -r requirements.txt
```

Run the Streamlit app:

```bash id="run-airbnb2"
streamlit run app.py
```

## Screenshots

Screenshots of the dashboard (overview, cleaning, outliers, and before/after comparison) are available in the screenshots folder.

## Conclusion

This project demonstrates a complete data cleaning workflow using an interactive Streamlit dashboard. It helps in understanding data quality issues and applying preprocessing techniques effectively before analysis or machine learning.

## Author

**Keerthika**
B.Tech Artificial Intelligence and Data Science,
Oasis Infobyte Data Analyst Internship (OIBSIP)
