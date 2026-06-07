# Task 8: Unveiling the Android App Market – Analyzing Google Play Store Data

## 📌 Project Overview

**Play Store Intelligence** is an advanced Streamlit-based data analytics dashboard designed to explore, visualize, and analyze the Google Play Store ecosystem.

The dashboard provides comprehensive insights into app categories, ratings, installs, monetization strategies, user sentiments, and market trends using interactive visualizations and Natural Language Processing (NLP).

This project transforms raw Google Play Store datasets into actionable business intelligence through data cleaning, exploratory data analysis (EDA), sentiment analysis, and trend detection.

---

## 🎯 Objectives

* Analyze Google Play Store applications.
* Explore app ratings, reviews, installs, and pricing.
* Identify top-performing app categories.
* Perform sentiment analysis on user reviews.
* Study app monetization strategies.
* Discover market trends and Android version adoption.
* Build an interactive business intelligence dashboard.

---

## 🛠 Technologies Used

* Python
* Streamlit
* Pandas
* NumPy
* Plotly
* Matplotlib
* WordCloud
* TextBlob
* Natural Language Processing (NLP)

---

## 📂 Dataset

This project uses the Google Play Store datasets:

### 1. apps.csv

Contains information about applications such as:

* App Name
* Category
* Rating
* Reviews
* Installs
* Size
* Price
* Content Rating
* Android Version
* Last Updated

### 2. user_reviews.csv

Contains user review data including:

* App
* User Reviews
* Sentiment Information

---

## ✨ Features

### 📊 Dashboard Overview

* Total Apps
* Average Rating
* Total Installs
* Average Paid App Price

---

### 📂 Category Analysis

* Apps by Category
* Category Rating Distribution
* Content Rating Breakdown
* Category-wise Performance

---

### 🔥 Top Apps Analysis

* Top Installed Applications
* Install Funnel by Category
* Install vs Review Relationship
* Category Treemap Visualization

---

### 💰 Monetization Analysis

* Free vs Paid Apps
* Price Distribution
* Average Price by Category
* Estimated Revenue Analysis

---

### 😊 Sentiment Analysis

Natural Language Processing is performed using TextBlob.

Features include:

* Positive Reviews
* Negative Reviews
* Neutral Reviews
* Polarity Analysis
* Subjectivity Analysis
* Sentiment Distribution Charts
* Word Cloud Visualization

---

### 📈 Trend Analysis

* App Updates Across Years
* Android Version Support
* Category Evolution
* Animated Install Race

---

### 🔍 Deep Dive Exploration

* Search Specific Applications
* Dataset Preview
* Export Filtered Data
* Interactive Data Exploration

---

## 📊 Data Cleaning Steps

The following preprocessing operations are performed:

### Duplicate Removal

* Removes duplicate applications.

### Install Conversion

Converts:

1,000,000+

into numeric values.

### Price Cleaning

Converts:

$4.99

into numeric format.

### Rating Conversion

Converts ratings into numeric values.

### Size Conversion

Converts:

* MB → Megabytes
* KB → Megabytes

for analysis.

### Date Processing

Extracts:

* Last Updated Date
* Update Year

### Android Version Extraction

Extracts minimum Android version requirements.

---

## 📈 Key Insights Generated

* Most popular app categories.
* Highest installed applications.
* Relationship between reviews and installs.
* Free vs Paid market distribution.
* Revenue opportunities across categories.
* User sentiment toward applications.
* Android ecosystem evolution over time.

---

## 🖥️ Dashboard Sections

### 1️⃣ Overview

Provides high-level insights into:

* Categories
* Ratings
* Content Ratings
* Distribution Analysis

---

### 2️⃣ Top Apps

Displays:

* Top Installed Apps
* Install Funnels
* Treemap Visualizations

---

### 3️⃣ Monetization

Analyzes:

* Pricing Models
* Revenue Potential
* Paid App Market

---

### 4️⃣ Sentiment Analysis

Uses NLP techniques to understand:

* User Satisfaction
* Positive Feedback
* Negative Feedback
* Review Trends

---

### 5️⃣ Trends

Analyzes:

* Update Frequency
* Category Growth
* Android Version Adoption

---

### 6️⃣ Deep Dive

Allows:

* App Search
* Data Exploration
* Dataset Export

---

## 📷 Screenshots

The screenshots folder contains images of:

* Dashboard Overview
* KPI Cards
* Category Analysis
* Top Apps Dashboard
* Monetization Dashboard
* Sentiment Analysis Dashboard
* Word Cloud Visualization
* Trend Analysis Dashboard
* Deep Dive Search
* Dataset Export Feature

---

## 📁 Project Structure

```text
Keerthika_Task8/
│
├── Keerthika_Task8.py
├── apps.csv
├── user_reviews.csv
├── requirements.txt
├── README.md
│
└── screenshots/
```

---

## ▶️ How to Run

### Clone Repository

```bash
git clone <repository-url>
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Streamlit App

```bash
streamlit run app.py
```

---

## 📌 Note

* Ensure both datasets (`apps.csv` and `user_reviews.csv`) are placed in the same folder as `app.py`.
* Internet connection may be required for loading external fonts used in the dashboard theme.
* Sentiment analysis results are generated using TextBlob polarity scores.

---

## 🎓 Learning Outcomes

Through this project, the following concepts were applied:

* Data Cleaning
* Exploratory Data Analysis (EDA)
* Data Visualization
* Business Intelligence Dashboards
* Sentiment Analysis
* Natural Language Processing
* Interactive Analytics using Streamlit

---

## 👩‍💻 Author

**Keerthika S**

Artificial Intelligence and Data Science Student

Task 8 – Oasis Infobyte Data Analytics Internship
