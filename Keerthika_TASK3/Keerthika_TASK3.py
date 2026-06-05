import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)

from wordcloud import WordCloud

# Page Configuration
st.set_page_config(
    page_title="Twitter Sentiment Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>

.stApp {
    background-color: white;
}

h1, h2, h3 {
    color: black;
}

div[data-testid="metric-container"] {
    border: 2px solid black;
    border-radius: 10px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# Title
st.title("📊 Twitter Sentiment Analysis Dashboard")
st.markdown("Analyze Twitter sentiments using Machine Learning")

# Sidebar
st.sidebar.title("Navigation")

menu = st.sidebar.radio(
    "Select Page",
    ["Dataset", "Visualization", "Model", "Prediction"]
)

uploaded_file = st.sidebar.file_uploader(
    "Upload Twitter_Data.csv",
    type=["csv"]
)

# No file uploaded
if uploaded_file is None:
    st.info("Please upload Twitter_Data.csv from the sidebar.")
    st.stop()

# Load Dataset
try:
    df = pd.read_csv(uploaded_file)
except Exception as e:
    st.error(f"Error loading file: {e}")
    st.stop()

# Show detected columns
st.sidebar.write("Detected Columns:")
st.sidebar.write(df.columns.tolist())

# Validate columns
if "clean_text" not in df.columns or "category" not in df.columns:
    st.error(
        f"""
        Required columns not found.

        Detected Columns:
        {df.columns.tolist()}
        """
    )
    st.stop()

# Clean data
df = df[["clean_text", "category"]].copy()

df["clean_text"] = df["clean_text"].astype(str)

df["category"] = pd.to_numeric(
    df["category"],
    errors="coerce"
)

df.dropna(inplace=True)

df["category"] = df["category"].astype(int)

# Create sentiment labels
df["sentiment"] = df["category"].replace({
    -1: "Negative",
     0: "Neutral",
     1: "Positive"
})

# DATASET PAGE
if menu == "Dataset":

    st.subheader("Dataset Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Rows", len(df))
    col2.metric("Columns", len(df.columns))
    col3.metric("Sentiment Classes", df["sentiment"].nunique())

    st.dataframe(df.head(20))

    st.subheader("Dataset Information")

    info_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str)
    })

    st.dataframe(info_df)

# VISUALIZATION PAGE
elif menu == "Visualization":

    st.subheader("Sentiment Distribution")

    sentiment_counts = df["sentiment"].value_counts()

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(7, 4))

        sentiment_counts.plot(
            kind="bar",
            ax=ax
        )

        ax.set_title("Sentiment Count")
        ax.set_xlabel("Sentiment")
        ax.set_ylabel("Count")

        st.pyplot(fig)

    with col2:
        fig2, ax2 = plt.subplots(figsize=(6, 6))

        ax2.pie(
            sentiment_counts,
            labels=sentiment_counts.index,
            autopct="%1.1f%%"
        )

        ax2.set_title("Sentiment Share")

        st.pyplot(fig2)

    st.subheader("Word Cloud")

    sample_text = " ".join(
        df["clean_text"]
        .sample(min(10000, len(df)), random_state=42)
        .astype(str)
    )

    wc = WordCloud(
        width=1200,
        height=600,
        background_color="white"
    ).generate(sample_text)

    fig3, ax3 = plt.subplots(figsize=(12, 6))

    ax3.imshow(wc)
    ax3.axis("off")

    st.pyplot(fig3)

# MODEL PAGE
elif menu == "Model":

    st.subheader("Model Training")

    X = df["clean_text"]
    y = df["sentiment"]

    vectorizer = TfidfVectorizer(
        max_features=5000
    )

    X_vectorized = vectorizer.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_vectorized,
        y,
        test_size=0.2,
        random_state=42
    )

    model = MultinomialNB()

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Accuracy",
        f"{accuracy * 100:.2f}%"
    )

    col2.metric(
        "Test Samples",
        len(y_test)
    )

    st.subheader("Classification Report")

    report = classification_report(
        y_test,
        y_pred,
        output_dict=True
    )

    st.dataframe(
        pd.DataFrame(report).transpose()
    )

    st.subheader("Confusion Matrix")

    cm = confusion_matrix(
        y_test,
        y_pred
    )

    fig4, ax4 = plt.subplots(figsize=(6, 5))

    image = ax4.imshow(cm)

    plt.colorbar(image)

    ax4.set_title("Confusion Matrix")
    ax4.set_xlabel("Predicted")
    ax4.set_ylabel("Actual")

    st.pyplot(fig4)

# PREDICTION PAGE
elif menu == "Prediction":

    st.subheader("Live Sentiment Prediction")

    X = df["clean_text"]
    y = df["sentiment"]

    vectorizer = TfidfVectorizer(
        max_features=5000
    )

    X_vec = vectorizer.fit_transform(X)

    model = MultinomialNB()

    model.fit(X_vec, y)

    user_text = st.text_area(
        "Enter Tweet Text"
    )

    if st.button("Predict Sentiment"):

        if user_text.strip() == "":
            st.warning("Please enter some text.")

        else:

            test_vector = vectorizer.transform(
                [user_text]
            )

            prediction = model.predict(
                test_vector
            )[0]

            if prediction == "Positive":
                st.success(f"😊 Sentiment: {prediction}")

            elif prediction == "Negative":
                st.error(f"😞 Sentiment: {prediction}")

            else:
                st.info(f"😐 Sentiment: {prediction}")