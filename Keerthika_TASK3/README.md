# Task 3: Twitter Sentiment Analysis Dashboard

## Project Overview

The Twitter Sentiment Analysis Dashboard is an interactive machine learning application that analyzes and classifies sentiments expressed in tweets. Using Natural Language Processing (NLP) and Machine Learning techniques, the system automatically categorizes tweets as Positive, Negative, or Neutral.

This project helps understand public opinion, customer feedback, and social media trends by transforming textual data into meaningful insights.

## Objective

* Analyze sentiments expressed in Twitter posts.
* Perform text preprocessing and cleaning.
* Convert text into numerical features using NLP techniques.
* Train a machine learning model for sentiment classification.
* Develop an interactive dashboard for real-time sentiment prediction.
* Visualize sentiment distribution and analysis results.

## Dataset

The project uses a Twitter sentiment dataset containing tweets labeled with sentiment categories:

* Positive
* Negative
* Neutral

The dataset is used to train and evaluate the sentiment classification model.

## Technologies Used

* Python
* Streamlit
* Pandas
* NumPy
* Scikit-learn
* NLTK
* TF-IDF Vectorizer
* Matplotlib

## Features

### Text Preprocessing

* Lowercase conversion
* Removal of punctuation and special characters
* Stopword removal
* Text cleaning and normalization

### Feature Engineering

* TF-IDF Vectorization
* Text-to-numeric transformation

### Machine Learning Model

* Train-Test Split
* Sentiment Classification
* Model Evaluation

### Interactive Dashboard

* User-friendly interface
* Real-time tweet sentiment prediction
* Instant sentiment results

## Methodology

### 1. Data Collection

The Twitter sentiment dataset was loaded and inspected to understand the structure and distribution of sentiment classes.

### 2. Data Cleaning

Unnecessary characters, symbols, URLs, and noise were removed from tweets to improve data quality.

### 3. Text Preprocessing

Natural Language Processing techniques were applied to prepare text data for machine learning.

### 4. Feature Extraction

TF-IDF Vectorization was used to convert tweets into numerical feature vectors.

### 5. Model Training

A machine learning classification model was trained using the processed dataset.

### 6. Model Evaluation

The model's performance was evaluated using appropriate classification metrics.

### 7. Dashboard Development

A Streamlit dashboard was developed to provide real-time sentiment analysis for user-entered tweets.

## Sample Predictions

### Positive

"Absolutely loved this product! Highly recommended."

### Negative

"The service was very disappointing and slow."

### Neutral

"The package was delivered yesterday."

## Key Insights

* Social media data can be effectively analyzed using NLP techniques.
* Sentiment classification helps understand customer opinions and trends.
* Text preprocessing significantly improves model performance.
* Real-time sentiment analysis supports data-driven decision-making.

## Project Structure

```text
Keerthika_Task3/
├── Keerthika_TASK3.py
├── Twitter_Data.csv
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
streamlit run Keerthika_TASK3.py
```

## Screenshots

Screenshots of the dashboard and sentiment prediction results are available in the screenshots folder.

## Conclusion

The Twitter Sentiment Analysis Dashboard successfully demonstrates the application of Natural Language Processing and Machine Learning techniques for sentiment classification. The project provides an effective way to analyze public opinions, customer feedback, and social media discussions through an interactive dashboard.

## Author

**Keerthika**
B.Tech Artificial Intelligence and Data Science
Oasis Infobyte Data Analyst Internship (OIBSIP)
