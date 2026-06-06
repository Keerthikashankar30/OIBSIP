# Task 7: Fraud Detection System

## Project Overview

This project is an advanced interactive Streamlit-based Machine Learning web application that detects fraudulent credit card transactions using multiple classification models and provides deep analytical insights into transaction patterns and anomalies.

The system is designed to simulate a real-world AI-powered financial intelligence platform where users can explore transaction data, compare different machine learning models, evaluate performance metrics, simulate real-time transaction streams, and receive instant fraud risk assessments with probability-based confidence scores.

The application integrates an end-to-end machine learning workflow including data loading, preprocessing, multi-model training, evaluation, explainability, and interactive visualization.

---

## Objective

The main objectives of this project are:

- To build a predictive binary classification model for identifying fraudulent transactions
- To compare multiple classification algorithms and analyse their performance on highly imbalanced data
- To preprocess and clean real-world anonymised credit card transaction data
- To develop an interactive multi-tab dashboard using Streamlit
- To visualise model predictions, probability distributions, and evaluation results
- To provide explainable AI through feature importance and permutation importance
- To simulate a real-time transaction monitoring stream with configurable fraud thresholds
- To apply advanced analytics including anomaly radar charts, ROC/PR curves, and outlier detection

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Multi-tab web application and dashboard framework |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical computations |
| Plotly | Interactive charts, animations, and radar visualizations |
| Scikit-learn | Machine learning models, preprocessing, and evaluation |

---

## Dataset Description

The dataset used in this project is **creditcard.csv**, which contains anonymised credit card transactions made by European cardholders, labelled as fraudulent or legitimate.

Features include:

| Feature | Description |
|---|---|
| Time | Seconds elapsed between a transaction and the first transaction |
| V1 – V28 | Principal components obtained via PCA (anonymised features) |
| Amount | Transaction amount in USD |
| Class | Target label — 0 = Legitimate, 1 = Fraudulent |

**Data preprocessing steps include:**

- Filtering transactions by configurable amount range via the sidebar
- Undersampling the majority class (legitimate transactions) to balance training data
- Feature scaling using `StandardScaler` for Logistic Regression and SVC models
- Raw features passed to tree-based models for optimal performance
- Automatic synthetic data generation if no CSV is uploaded (demo mode)

---

## Features

### 🛡️ 1. Live Transaction Metrics — KPI Dashboard

The landing section provides a high-level real-time summary of the entire dataset.

Users can see:

- 5 live KPI metric cards: total transactions, fraud cases, legitimate transactions, fraud rate %, and total fraud exposure ($)
- Each card features an animated neon scan-line effect and colour-coded values
- Sidebar controls for dataset upload, detection threshold, amount range filter, and model toggle

---

### 📊 2. Overview — Distribution Analysis

A high-level visual overview of the transaction dataset.

Includes:

- Donut chart showing class distribution with fraud rate annotated at centre
- Overlapping histogram comparing transaction amounts for legitimate vs fraudulent transactions
- Dual-axis time series bar + line chart showing legitimate transaction volume and fraud case frequency by hour of day

---

### 🔬 3. Deep Analysis — Anomaly Exploration

A comprehensive interactive exploration of fraud patterns in feature space.

Includes:

- **Feature Anomaly Radar** — Spider chart comparing the mean absolute values of V1–V14 for fraud vs legitimate transactions, revealing which PCA components carry the strongest anomaly signals
- **Feature Distribution Comparison** — Interactive violin plot with box and mean line for any selected feature (V1–V28 or Amount), split by class
- **Correlation Heatmap** — Pearson correlation matrix for the top 10 PCA components plus Amount and Class, rendered as an annotated interactive heatmap

---

### 🤖 4. ML Models — Multi-Model Comparison

Trains and evaluates three classification algorithms simultaneously on balanced data.

**Models included:**

- **Logistic Regression** — Linear baseline classifier (scaled input)
- **Random Forest** — Ensemble of decision trees (raw features)
- **Gradient Boosting** — Sequential boosting classifier (raw features)

**Performance metrics displayed:**

- ROC-AUC, PR-AUC, Precision, Recall, F1 Score — in a styled comparison table
- Best model highlighted automatically
- ROC curves and Precision-Recall curves plotted for all three models simultaneously
- Per-model confusion matrix heatmaps with annotation
- Ranked feature importance horizontal bar chart from Random Forest (top 15 features)

---

### ⚡ 5. Real-Time Simulation — Live Transaction Stream

An animated real-time transaction monitoring simulator.

Users can:

- Select stream speed: Slow / Normal / Fast
- Click **START STREAM** to process 20 synthetic transactions sequentially
- Watch the risk score chart build live with colour-coded fraud/legitimate markers

Output includes:

- Animated scatter-line chart of fraud risk scores per transaction with a configurable detection threshold line
- Red shaded zone above threshold indicating the fraud alert region
- Post-stream summary alert card (fraud detected / stream clear)
- Flagged transactions table showing transaction number, amount, risk score, and status

---

### 📋 6. Data Explorer — Dataset Inspection

A structured view of the raw dataset with statistical summaries.

Includes:

- Dataset shape, missing value check with pass/fail indicator
- Transaction amount statistics grouped by class (mean, median, std, max)
- Full descriptive statistics table for all V1–V28 and Amount features
- Optional raw data viewer with class filter (All / Fraud Only / Legitimate Only), toggled from the sidebar

---

## Methodology

### 1. Data Loading
`creditcard.csv` is loaded using Pandas. If no file is uploaded, a synthetic 15,000-row demo dataset is automatically generated with realistic fraud patterns for immediate exploration.

### 2. Data Preprocessing
- Transactions are filtered by the user-defined amount range from the sidebar
- The dataset is undersampled: all fraud records are retained and up to 5,000 legitimate transactions are randomly sampled to create a balanced training set
- An 80/20 train/test split is applied with a fixed random seed (42)
- `StandardScaler` is fitted on training features and applied consistently to test data

### 3. Model Training
All three models are trained once on startup using `@st.cache_data`, ensuring fast load times and no redundant re-fitting across user interactions.

### 4. Prediction Pipeline
- Synthetic transaction features are generated based on statistical properties of the loaded dataset
- Risk scores are computed using model probability outputs
- Transactions exceeding the user-defined threshold are flagged as fraudulent

### 5. Model Evaluation
Each model is evaluated on the held-out test set using:

- ROC-AUC Score
- Average Precision Score (PR-AUC)
- Weighted Precision, Recall, and F1 Score
- Confusion Matrix
- Full Classification Report

### 6. Explainability
- Random Forest native feature importances are extracted and ranked for the top 15 PCA components
- Feature anomaly radar charts provide visual explainability by comparing mean feature profiles of fraud vs legitimate transactions

### 7. Real-Time Stream Engine
- Synthetic transactions are generated on-the-fly using dataset statistics
- Fraud transactions are sampled from distributions centred on the fraud cluster mean
- Risk scores are assigned probabilistically and evaluated against the configurable detection threshold

---

## Key Insights

- **V17, V14, V12, and V10** exhibit the strongest separation between fraud and legitimate transactions in PCA space
- **Transaction amount** alone is insufficient to classify fraud — fraud spans a wide range of amounts
- **Random Forest and Gradient Boosting** significantly outperform Logistic Regression on this imbalanced dataset
- **PR-AUC** is a more informative metric than ROC-AUC for highly imbalanced fraud datasets
- The fraud rate of ~0.17% creates extreme class imbalance that must be addressed through sampling strategies
- Fraud activity does not follow a uniform time distribution — certain hours show elevated fraud frequency

---

## Project Structure

```
Keerthika_Task7/
├── Keerthika_Task7.py
├── creditcard.csv
├── requirements.txt
└── README.md
```

---

## How to Run

**1. Install dependencies:**
```bash
pip install -r requirements.txt
```

**2. Launch the application:**
```bash
streamlit run Keerthika_Task7.py
```

**3. Upload your dataset:**
Use the sidebar file uploader to load `creditcard.csv`. The app runs in demo mode with synthetic data if no file is provided.

---


## Conclusion

This project demonstrates a complete end-to-end Machine Learning binary classification pipeline integrated into a six-tab interactive web application.

It showcases how fraud detection models can be applied to real-world anonymised financial data while combining imbalanced data handling, multi-model evaluation, explainable AI, and advanced statistical analytics.

The Real-Time Simulation module bridges the gap between offline model evaluation and live deployment scenarios by animating transaction-by-transaction risk scoring with an adjustable detection threshold.

The project highlights how well-designed interactive dashboards can make machine learning systems more interpretable, trustworthy, and operationally useful for both data scientists and financial analysts.

**Future improvements may include:**

- Integration with live payment gateway APIs for real transaction streaming
- Support for white-label card networks and multi-currency transactions
- Advanced models such as XGBoost, LightGBM, Autoencoders, or Graph Neural Networks
- SHAP (SHapley Additive exPlanations) values for individual transaction explainability
- Deployment on Streamlit Cloud or AWS with user authentication
- Saved fraud investigation history and case management dashboard
- Network graph analysis to detect coordinated fraud rings

---

## Author

**Keerthika.S**  
B.Tech Artificial Intelligence and Data Science,
Oasis Infobyte Data Analyst Internship (OIBSIP)
