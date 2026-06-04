# Task 2: Customer Segmentation Dashboard

## Project Overview

This project focuses on customer segmentation using Machine Learning and data visualization techniques. An interactive Streamlit dashboard was developed to analyze customer purchasing behavior and group customers into meaningful segments using the K-Means Clustering algorithm.

Customer segmentation helps businesses identify different customer groups, understand their spending patterns, and design targeted marketing strategies to improve customer engagement and business performance.

## Objective

* Analyze customer demographic and spending data.
* Identify customer segments using clustering techniques.
* Visualize customer behavior through an interactive dashboard.
* Support data-driven marketing and business decisions.

## Dataset

The project uses the **Mall Customers Dataset**, which contains the following attributes:

* Customer ID
* Gender
* Age
* Annual Income (k$)
* Spending Score (1–100)

## Technologies Used

* Python
* Streamlit
* Pandas
* NumPy
* Matplotlib
* Plotly
* Scikit-learn

## Features

### Data Exploration

* Dataset preview
* Dataset statistics
* Missing value analysis

### Customer Analysis

* Gender distribution
* Age distribution
* Annual income analysis
* Spending score analysis

### Customer Segmentation

* K-Means Clustering
* Optimal cluster identification
* Customer cluster visualization

### Interactive Dashboard

* Dynamic visualizations
* Real-time data insights
* User-friendly interface

## Methodology

### 1. Data Loading

The customer dataset was loaded into the application and inspected for completeness and consistency.

### 2. Data Preprocessing

Data cleaning and preparation were performed to ensure accurate analysis and clustering.

### 3. Exploratory Data Analysis

Customer demographics and purchasing behavior were analyzed using statistical summaries and visualizations.

### 4. Feature Selection

Annual Income and Spending Score were selected as the primary features for customer segmentation.

### 5. Cluster Optimization

The Elbow Method was applied to determine the optimal number of clusters.

### 6. K-Means Clustering

Customers were grouped into distinct segments based on similarities in spending behavior and income levels.

### 7. Dashboard Development

An interactive Streamlit dashboard was created to present customer insights and clustering results effectively.

## Key Insights

* Identified high-value customer segments.
* Recognized customers with high income but low spending patterns.
* Discovered potential target groups for personalized marketing campaigns.
* Improved understanding of customer purchasing behavior.

## Project Structure

```text
Keerthika_Task2/
├── app.py
├── Mall_Customers.csv
├── requirements.txt
├── README.md
└── screenshots/
```

## How to Run

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app.py
```

## Screenshots

Screenshots of the dashboard and visualizations are available in the screenshots folder.

## Conclusion

The Customer Segmentation Dashboard successfully demonstrates the application of Machine Learning and Data Analytics techniques to classify customers into meaningful groups. The insights generated can help businesses improve customer targeting, marketing effectiveness, and overall decision-making.

## Author

**Keerthika**
B.Tech Artificial Intelligence and Data Science
Oasis Infobyte Data Analyst Internship (OIBSIP)
