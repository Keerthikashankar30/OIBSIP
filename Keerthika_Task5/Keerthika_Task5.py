import streamlit as st
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Geo AI House Price", page_icon="🏠", layout="wide")

st.title("🏠 Geo AI House Price Prediction System")

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("housing.csv")

df = df.dropna()
df = df.replace({"yes": 1, "no": 0})
df = pd.get_dummies(df, drop_first=True)

# =========================
# NAVIGATION
# =========================
page = st.sidebar.radio(
    "📌 Navigation",
    ["🏠 Prediction", "📊 Analytics", "🌍 Geo Map"]
)

# =========================
# TARGET SELECTION
# =========================
target = st.sidebar.selectbox("🎯 Select Target Column", df.columns)

X = df.drop(target, axis=1)
y = df[target]

# =========================
# MODEL SELECTION
# =========================
model_choice = st.sidebar.radio(
    "🤖 Choose Model",
    ["Linear Regression", "Ridge Regression", "Lasso Regression"]
)

if model_choice == "Linear Regression":
    model = LinearRegression()
elif model_choice == "Ridge Regression":
    model = Ridge(alpha=1.0)
else:
    model = Lasso(alpha=0.01)

# =========================
# SCALING + TRAINING
# =========================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# =========================
# INR FORMAT FUNCTION
# =========================
def format_inr(value):
    value = int(value)
    s = str(value)

    if len(s) <= 3:
        return f"₹ {s}"

    last3 = s[-3:]
    rest = s[:-3]

    rest = ",".join([rest[max(i-2, 0):i] for i in range(len(rest), 0, -2)][::-1])

    return f"₹ {rest},{last3}" if rest else f"₹ {last3}"

# =========================================================
# 🏠 PREDICTION PAGE (FIXED INTEGER INPUTS)
# =========================================================
if page == "🏠 Prediction":

    st.subheader("🔮 Predict House Price")

    input_data = {}

    # Columns that must NOT have decimals
    int_cols = [
        "area",
        "bedrooms",
        "furnishingstatus_semi-furnished",
        "furnishingstatus_unfurnished",
        "prefarea",
        "parking",
        "airconditioning",
        "hotwaterheating",
        "basement",
        "guestroom",
        "mainroad",
        "stories"
    ]

    for col in X.columns:

        if col in int_cols:
            input_data[col] = st.number_input(
                col,
                min_value=int(X[col].min()),
                max_value=int(X[col].max()),
                value=int(X[col].mean()),
                step=1
            )
        else:
            input_data[col] = st.number_input(
                col,
                float(X[col].min()),
                float(X[col].max()),
                float(X[col].mean())
            )

    input_df = pd.DataFrame([input_data])
    input_df = input_df[X.columns]
    input_scaled = scaler.transform(input_df)

    if st.button("🏠 Predict Price"):

        prediction = model.predict(input_scaled)[0]
        prediction = int(round(max(prediction, 0)))

        st.success(f"🏠 Predicted Price: {format_inr(prediction)}")

    else:
        st.info("👉 Enter values and click Predict")

# =========================================================
# 📊 ANALYTICS PAGE
# =========================================================
elif page == "📊 Analytics":

    st.subheader(f"📈 Model Performance ({model_choice})")

    st.write("R² Score:", round(r2_score(y_test, y_pred), 3))
    st.write("MSE:", round(mean_squared_error(y_test, y_pred), 2))

    st.subheader("📉 Actual vs Predicted")

    fig, ax = plt.subplots()
    ax.scatter(y_test, y_pred, alpha=0.6)
    ax.set_xlabel("Actual")
    ax.set_ylabel("Predicted")
    st.pyplot(fig)

    st.subheader("🔥 Feature Importance")

    importance = pd.Series(model.coef_, index=X.columns).sort_values()

    fig2, ax2 = plt.subplots()
    importance.plot(kind="barh", ax=ax2)
    st.pyplot(fig2)

# =========================================================
# 🌍 GEO MAP PAGE
# =========================================================
elif page == "🌍 Geo Map":

    st.subheader("🌍 Real Estate Heatmap (Geo AI)")

    np.random.seed(42)

    map_df = pd.DataFrame({
        "lat": np.random.uniform(12.85, 13.15, len(y_test)),
        "lon": np.random.uniform(80.10, 80.30, len(y_test)),
        "price": y_test.values
    })

    m = folium.Map(location=[13.08, 80.27], zoom_start=11)

    heat_data = []

    for _, row in map_df.iterrows():
        heat_data.append([row["lat"], row["lon"], row["price"]])

        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=5,
            popup=f"Price: {format_inr(int(row['price']))}",
            color="red",
            fill=True,
            fill_opacity=0.6
        ).add_to(m)

    HeatMap(heat_data).add_to(m)

    st_folium(m, width=900, height=500)