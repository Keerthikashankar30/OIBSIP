import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="NYC Airbnb Data Cleaning Dashboard",
    page_icon="🏠",
    layout="wide"
)

# ==========================================
# LIGHT THEME
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #F8FAFC;
}

[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E5E7EB;
}

[data-testid="metric-container"] {
    background-color: white;
    border: 1px solid #E5E7EB;
    border-radius: 15px;
    padding: 15px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
}

h1,h2,h3,h4 {
    color: #1E3A8A !important;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================

st.markdown("""
<h1 style='text-align:center'>
🏠 NYC Airbnb Data Cleaning Dashboard
</h1>
<p style='text-align:center'>
Data Quality • Missing Values • Outliers • Cleaning
</p>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("🧹 Dashboard")

uploaded_file = st.sidebar.file_uploader(
    "Upload Airbnb Dataset",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    # ======================================
    # QUICK FILTERS
    # ======================================

    filtered_df = df.copy()

    st.sidebar.markdown("---")
    st.sidebar.subheader("📍 Quick Filters")

    if "neighbourhood_group" in filtered_df.columns:

        boroughs = st.sidebar.multiselect(
            "Borough",
            sorted(
                filtered_df["neighbourhood_group"]
                .dropna()
                .unique()
            )
        )

        if boroughs:
            filtered_df = filtered_df[
                filtered_df["neighbourhood_group"]
                .isin(boroughs)
            ]

    if "room_type" in filtered_df.columns:

        room_types = st.sidebar.multiselect(
            "Room Type",
            sorted(
                filtered_df["room_type"]
                .dropna()
                .unique()
            )
        )

        if room_types:
            filtered_df = filtered_df[
                filtered_df["room_type"]
                .isin(room_types)
            ]

    # ======================================
    # MENU
    # ======================================

    menu = st.sidebar.radio(
        "Navigation",
        [
            "Overview",
            "Data Quality",
            "Missing Values",
            "Outliers",
            "Data Explorer",
            "Cleaning",
            "Before vs After"
        ]
    )

    # ======================================
    # CLEAN DATASET
    # ======================================

    clean_df = filtered_df.copy()

    for col in clean_df.columns:

        if pd.api.types.is_numeric_dtype(clean_df[col]):

            clean_df[col] = clean_df[col].fillna(
                clean_df[col].median()
            )

        else:

            clean_df[col] = clean_df[col].fillna(
                "Unknown"
            )

    clean_df.drop_duplicates(inplace=True)

    # ======================================
    # OVERVIEW
    # ======================================

    if menu == "Overview":

        st.header("Dataset Overview")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Rows", f"{filtered_df.shape[0]:,}")
        c2.metric("Columns", filtered_df.shape[1])
        c3.metric(
            "Missing Values",
            int(filtered_df.isnull().sum().sum())
        )
        c4.metric(
            "Duplicates",
            int(filtered_df.duplicated().sum())
        )

        st.dataframe(
            filtered_df.head(20),
            use_container_width=True
        )

    # ======================================
    # DATA QUALITY
    # ======================================

    elif menu == "Data Quality":

        st.header("Data Quality Report")

        total_cells = (
            filtered_df.shape[0] *
            filtered_df.shape[1]
        )

        missing = (
            filtered_df.isnull()
            .sum()
            .sum()
        )

        score = (
            (total_cells - missing)
            / total_cells
        ) * 100

        st.metric(
            "Quality Score %",
            round(score, 2)
        )

        fig = px.pie(
            values=[
                total_cells - missing,
                missing
            ],
            names=[
                "Valid",
                "Missing"
            ]
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ======================================
    # MISSING VALUES
    # ======================================

    elif menu == "Missing Values":

        st.header("Missing Values Analysis")

        miss = filtered_df.isnull().sum()

        miss_df = pd.DataFrame({
            "Column": miss.index,
            "Missing": miss.values
        })

        miss_df = miss_df[
            miss_df["Missing"] > 0
        ]

        if not miss_df.empty:

            fig = px.bar(
                miss_df,
                x="Column",
                y="Missing"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.dataframe(miss_df)

        else:
            st.success("No Missing Values")

    # ======================================
    # OUTLIERS
    # ======================================

    elif menu == "Outliers":

        st.header("Outlier Detection")

        numeric_cols = filtered_df.select_dtypes(
            include=np.number
        ).columns

        if len(numeric_cols) > 0:

            selected_col = st.selectbox(
                "Select Column",
                numeric_cols
            )

            fig = px.box(
                filtered_df,
                y=selected_col
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # ======================================
    # DATA EXPLORER
    # ======================================

    elif menu == "Data Explorer":

        st.header("Advanced Data Explorer")

        explorer_df = filtered_df.copy()

        search = st.text_input(
            "Search Entire Dataset"
        )

        if search:

            mask = explorer_df.astype(str).apply(
                lambda x: x.str.contains(
                    search,
                    case=False,
                    na=False
                )
            ).any(axis=1)

            explorer_df = explorer_df[mask]

        st.write(
            f"Records Found: {len(explorer_df)}"
        )

        if not explorer_df.empty:

            st.dataframe(
                explorer_df,
                use_container_width=True
            )

            st.subheader("Statistics")

            try:
                st.dataframe(
                    explorer_df.describe(
                        include="all"
                    )
                )
            except:
                pass

        else:
            st.warning("No matching records.")

    # ======================================
    # CLEANING
    # ======================================

    elif menu == "Cleaning":

        st.header("Cleaned Dataset")

        st.dataframe(
            clean_df.head(20),
            use_container_width=True
        )

        csv = clean_df.to_csv(
            index=False
        )

        st.download_button(
            "📥 Download Cleaned Dataset",
            csv,
            "cleaned_airbnb.csv",
            "text/csv"
        )

    # ======================================
    # BEFORE VS AFTER
    # ======================================

    elif menu == "Before vs After":

        st.header(
            "Before vs After Cleaning"
        )

        comparison = pd.DataFrame({

            "Metric": [
                "Rows",
                "Missing Values",
                "Duplicates"
            ],

            "Before": [
                len(filtered_df),
                filtered_df.isnull()
                .sum()
                .sum(),
                filtered_df.duplicated()
                .sum()
            ],

            "After": [
                len(clean_df),
                clean_df.isnull()
                .sum()
                .sum(),
                clean_df.duplicated()
                .sum()
            ]
        })

        st.dataframe(
            comparison,
            use_container_width=True
        )

        fig = px.bar(
            comparison,
            x="Metric",
            y=["Before", "After"],
            barmode="group"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

else:

    st.info(
        "Upload a CSV file from the sidebar to begin."
    )