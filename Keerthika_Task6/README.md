# Task 6: Wine Quality Prediction System

# Project Overview
* This project is an advanced interactive Streamlit-based Machine Learning web application that predicts wine quality using multiple classification models and provides deep analytical insights into the chemical composition of wines.
* The system is designed to simulate a real-world AI-powered wine intelligence platform where users can input chemical parameters, compare different machine learning models, evaluate performance metrics, explore feature importance, and receive personalised wine improvement recommendations.
* The application integrates an end-to-end machine learning workflow including data loading, preprocessing, multi-model training, evaluation, explainability, and interactive visualization — all wrapped in a polished, production-grade dashboard UI.

# Objective
The main objectives of this project are:

* To build a predictive classification model for estimating wine quality scores
* To compare multiple classification algorithms and analyse their performance
* To preprocess and clean real-world structured wine chemistry data
* To develop an interactive multi-page dashboard using Streamlit
* To visualise model predictions, probability distributions, and evaluation results
* To provide explainable AI through feature importance and permutation importance
* To give actionable wine improvement recommendations based on chemical thresholds
* To apply advanced analytics including PCA, cross-validation, and outlier detection

# Technologies Used
* Python – Core programming language
* Streamlit – Multi-page web application and dashboard framework
* Pandas – Data manipulation and analysis
* NumPy – Numerical computations
* Matplotlib – Custom data visualizations and radar charts
* Seaborn – Statistical heatmaps and distribution plots
* Scikit-learn – Machine learning models, preprocessing, and evaluation
* Pickle – Model serialization and export

# Dataset Description
The dataset used in this project is **WineQT.csv**, which contains physicochemical measurements of red wine samples along with a quality score assigned by wine experts.

### Features include:
| Feature | Description |
|---|---|
| fixed acidity | Tartaric acid concentration |
| volatile acidity | Acetic acid — high levels lead to vinegar taste |
| citric acid | Adds freshness and flavour complexity |
| residual sugar | Sugar remaining after fermentation |
| chlorides | Salt content in wine |
| free sulfur dioxide | Free SO₂ — prevents microbial growth |
| total sulfur dioxide | Total SO₂ present |
| density | Density relative to water |
| pH | Acidity/alkalinity level |
| sulphates | Contributes to SO₂ levels and preservation |
| alcohol | Percentage alcohol by volume |
| quality | Expert quality score (target, range: 3–8) |

### Data preprocessing steps include:
* Removal of the non-feature `Id` column present in WineQT.csv
* Train/test split (80% training, 20% testing) with a fixed random seed
* Feature scaling using `StandardScaler` for distance-based and linear models
* Raw (unscaled) features passed to tree-based models for optimal performance

# Features

### 🏠 1. Dashboard — Overview & KPIs
The landing page provides a high-level summary of the entire dataset at a glance.

Users can see:
* 5 live KPI metrics: total samples, feature count, average quality, high quality %, low quality %
* Annotated bar chart of wine count by quality score (3–8), colour-coded by tier
* Pie chart showing the proportion of Low / Medium / High quality wines
* Full lower-triangle correlation heatmap with Pearson coefficients for all features

### 📊 2. Deep EDA — Exploratory Data Analysis
A comprehensive interactive exploration of the dataset.

Includes:
* Styled dataset preview and descriptive statistics table with gradient highlighting
* Feature distribution grid — all 11 chemical features plotted as overlapping histograms, colour-coded by quality class
* Interactive box plot — select any feature to see its distribution across quality scores
* Interactive scatter plot — choose any two features to plot, coloured by quality score

### 🤖 3. Model Arena — Multi-Model Comparison
Trains and evaluates five classification algorithms simultaneously.

Models included:
* **Random Forest** — Ensemble of decision trees (no scaling required)
* **Gradient Boosting** — Sequential boosting classifier (no scaling required)
* **SGD Classifier** — Stochastic gradient descent (scaled input)
* **SVC** — Support Vector Classifier with probability output (scaled input)
* **K-Nearest Neighbors** — Instance-based learning (scaled input)

Performance metrics displayed:
* Accuracy, F1 Score, Precision, Recall — all in a gradient-styled comparison table
* Best model highlighted automatically with accuracy percentage
* Per-model confusion matrix selector with annotated heatmap
* Learning curve visualisation showing training vs cross-validation score
* Full `classification_report` as a styled interactive dataframe

### 🔮 4. Prediction Lab — Real-Time Prediction
An interactive lab for predicting quality from custom wine parameters.

Users can:
* Select any of the 5 trained models for prediction
* Adjust all 11 chemical parameters using range sliders
* Click "Run Prediction" to instantly see results

Output includes:
* Large styled quality score card with colour-coded category label
* Animated quality gauge (Low / Medium / High) with smooth pointer animation
* **Probability distribution bar chart** — shows model confidence across all quality classes
* **Radar chart** — normalised chemical profile of the entered wine
* Download the full prediction as a CSV report

### 🍷 5. Wine Advisor — Expert Improvement Tips
An AI-powered consultant that analyses a wine's chemical profile and gives actionable feedback.

Expert thresholds checked:
* Volatile acidity > 0.6 — vinegar risk warning
* Alcohol < 10% — low body alert
* Sulphates < 0.5 — preservation concern
* Density > 1.0 — smoothness impact
* Citric acid < 0.1 — freshness deficit
* pH > 3.6 — stability risk
* Residual sugar > 8 — sweetness balance check

Output includes:
* Severity-coded tip cards (🟢 green / 🟡 amber / 🔴 red)
* Predicted quality score with animated gauge
* Chemical profile radar chart

### 📈 6. Feature Intelligence — Explainability
Explains which chemical features drive wine quality predictions.

Includes:
* Ranked feature importance table from Random Forest (gradient-styled)
* Horizontal bar chart with top feature highlighted in wine red
* **Permutation importance** — model-agnostic importance computed for any selected model
* One-click download of the trained Random Forest model as `wine_model.pkl`

### 🔬 7. Advanced Analytics — Deep Science
Research-grade analysis for deeper understanding.

Includes:
* **PCA scatter plot** — 11 features compressed to 2D, quality classes visualised in chemical space with explained variance labels
* **5-fold cross-validation** for all 5 models — mean accuracy with ± standard deviation error bars
* **Feature → quality correlation chart** — Pearson correlation of each feature with the quality score (red = negative, green = positive)
* **Outlier detection** using the IQR method for every feature, ranked by outlier count

# Methodology

### 1. Data Loading
WineQT.csv is loaded using Pandas. The non-feature `Id` column is dropped automatically if present.

### 2. Data Preprocessing
* The dataset is split 80/20 into training and testing sets using a fixed random seed (42)
* `StandardScaler` is fitted on the training set and applied to the test set
* Tree-based models (Random Forest, Gradient Boosting) use raw features; all others use scaled features

### 3. Model Training
All five models are trained once on startup using `@st.cache_resource`, ensuring fast load times and no redundant re-fitting across user interactions.

### 4. Prediction Pipeline
* User inputs are collected via sliders or number inputs
* Inputs are scaled (if required by the chosen model) using the pre-fitted scaler
* The model returns a quality score and probability distribution

### 5. Model Evaluation
Each model is evaluated on the held-out test set using:
* Accuracy Score
* Weighted F1 Score
* Weighted Precision and Recall
* Confusion Matrix
* Full Classification Report
* 5-Fold Cross-Validation

### 6. Explainability
* Random Forest native feature importances are extracted and ranked
* Permutation importance is computed model-agnostically using `sklearn.inspection.permutation_importance`
* PCA is applied to the scaled training set for 2D visualisation

### 7. Advisory Engine
Chemical properties of the user-submitted wine are compared against expert-defined thresholds. Tip severity is determined by the magnitude of deviation from the optimal range.

# Key Insights
* Alcohol content has the strongest positive correlation with wine quality
* Volatile acidity is the most negatively correlated feature with quality
* Random Forest and Gradient Boosting consistently outperform linear models on this dataset
* PCA reveals significant overlap between adjacent quality classes, explaining classification difficulty
* Permutation importance provides a more reliable signal than native feature importances for scaled models
* Interactive dashboards significantly improve interpretability of machine learning results for non-technical users

# Project Structure

```
Keerthika_Task6/
├── Keerthika_Task6.py
├── WineQT.csv
├── wine_model.pkl          ← generated at runtime
├── requirements.txt
├── README.md
└── screenshots/
```


# Conclusion
* This project demonstrates a complete end-to-end Machine Learning classification pipeline integrated into a seven-page interactive web application.
* It showcases how classification models can be applied to real-world sensory prediction tasks while combining data preprocessing, multi-model evaluation, explainable AI, and advanced statistical analytics.
* The Wine Advisor module bridges the gap between data science and domain expertise by translating model predictions into actionable chemical improvement recommendations.
* The project highlights how well-designed interactive dashboards can make machine learning systems more interpretable, trustworthy, and useful for both technical and non-technical audiences.

### Future improvements may include:
* Integration with wine databases or APIs for live data
* Support for white wine and rosé datasets
* Advanced models such as XGBoost, LightGBM, or Neural Networks
* SHAP (SHapley Additive exPlanations) values for individual prediction explainability
* Deployment on Streamlit Cloud or AWS
* User authentication and saved prediction history

# Author
**Keerthika.S**
B.Tech Artificial Intelligence and Data Science,
Oasis Infobyte Data Analyst Internship (OIBSIP)
