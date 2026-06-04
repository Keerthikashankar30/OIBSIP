import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------
# CUSTOM CSS
# ---------------------------------
st.markdown("""
<style>

.main {
    background-color: #F8F9FA;
}

div[data-testid="metric-container"] {
    border: 1px solid #E6E6E6;
    padding: 15px;
    border-radius: 15px;
    background-color: white;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
}

h1 {
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------
# LOAD DATA
# ---------------------------------
df = pd.read_csv("Mall_Customers.csv")

# ---------------------------------
# K-MEANS CLUSTERING
# ---------------------------------
X = df[['Annual Income (k$)',
        'Spending Score (1-100)']]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(
    n_clusters=5,
    random_state=42,
    n_init=10
)

df['Cluster'] = kmeans.fit_predict(X_scaled)

# ---------------------------------
# HEADER
# ---------------------------------
st.title("📊 Customer Segmentation Analysis Dashboard")

st.markdown("""
Analyze customer purchasing behavior using
**Machine Learning (K-Means Clustering)**.
""")

# ---------------------------------
# SIDEBAR
# ---------------------------------
st.sidebar.header("Dashboard Filters")

selected_clusters = st.sidebar.multiselect(
    "Select Cluster",
    options=sorted(df['Cluster'].unique()),
    default=sorted(df['Cluster'].unique())
)

filtered_df = df[df['Cluster'].isin(selected_clusters)]

# ---------------------------------
# KPI SECTION
# ---------------------------------
st.subheader("📌 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Customers",
        len(filtered_df)
    )

with col2:
    st.metric(
        "Average Age",
        round(filtered_df['Age'].mean(), 1)
    )

with col3:
    st.metric(
        "Average Income",
        f"${filtered_df['Annual Income (k$)'].mean():.1f}k"
    )

with col4:
    st.metric(
        "Average Spending",
        round(filtered_df['Spending Score (1-100)'].mean(), 1)
    )

st.divider()

# ---------------------------------
# SCATTER PLOT
# ---------------------------------
st.subheader("🎯 Customer Segments")

fig_scatter = px.scatter(
    filtered_df,
    x="Annual Income (k$)",
    y="Spending Score (1-100)",
    color="Cluster",
    size="Age",
    hover_data=["CustomerID", "Gender"],
    title="Income vs Spending Score"
)

st.plotly_chart(fig_scatter, use_container_width=True)

# ---------------------------------
# BAR + PIE CHART
# ---------------------------------
col1, col2 = st.columns(2)

with col1:

    cluster_count = (
        filtered_df['Cluster']
        .value_counts()
        .reset_index()
    )

    cluster_count.columns = [
        'Cluster',
        'Customers'
    ]

    fig_bar = px.bar(
        cluster_count,
        x='Cluster',
        y='Customers',
        text='Customers',
        title="Customers Per Cluster"
    )

    st.plotly_chart(fig_bar,
                    use_container_width=True)

with col2:

    gender_count = (
        filtered_df['Gender']
        .value_counts()
        .reset_index()
    )

    gender_count.columns = [
        'Gender',
        'Count'
    ]

    fig_pie = px.pie(
        gender_count,
        names='Gender',
        values='Count',
        title='Gender Distribution'
    )

    st.plotly_chart(fig_pie,
                    use_container_width=True)

# ---------------------------------
# 3D VISUALIZATION
# ---------------------------------
st.subheader("🌐 3D Customer Segmentation")

fig3d = px.scatter_3d(
    filtered_df,
    x='Age',
    y='Annual Income (k$)',
    z='Spending Score (1-100)',
    color='Cluster',
    hover_data=['Gender']
)

st.plotly_chart(fig3d,
                use_container_width=True)

# ---------------------------------
# AGE DISTRIBUTION
# ---------------------------------
st.subheader("📈 Age Distribution")

fig_age = px.histogram(
    filtered_df,
    x='Age',
    nbins=20,
    title='Customer Age Distribution'
)

st.plotly_chart(fig_age,
                use_container_width=True)

# ---------------------------------
# CORRELATION HEATMAP
# ---------------------------------
st.subheader("🔥 Correlation Heatmap")

corr = filtered_df[
    ['Age',
     'Annual Income (k$)',
     'Spending Score (1-100)']
].corr()

heatmap = ff.create_annotated_heatmap(
    z=corr.values,
    x=list(corr.columns),
    y=list(corr.index),
    annotation_text=round(corr, 2).values
)

st.plotly_chart(
    heatmap,
    use_container_width=True
)

# ---------------------------------
# ELBOW METHOD
# ---------------------------------
st.subheader("📉 Elbow Method")

wcss = []

for i in range(1, 11):

    model = KMeans(
        n_clusters=i,
        random_state=42,
        n_init=10
    )

    model.fit(X_scaled)

    wcss.append(model.inertia_)

fig_elbow = px.line(
    x=list(range(1, 11)),
    y=wcss,
    markers=True,
    labels={
        "x": "Number of Clusters",
        "y": "WCSS"
    },
    title="Optimal Cluster Selection"
)

st.plotly_chart(
    fig_elbow,
    use_container_width=True
)

# ---------------------------------
# CLUSTER SUMMARY
# ---------------------------------
st.subheader("📋 Cluster Summary")

summary = filtered_df.groupby(
    'Cluster'
).agg({
    'Age': 'mean',
    'Annual Income (k$)': 'mean',
    'Spending Score (1-100)': 'mean'
}).round(2)

st.dataframe(
    summary,
    use_container_width=True
)

# ---------------------------------
# CUSTOMER SEARCH
# ---------------------------------
st.subheader("🔍 Search Customer")

customer = st.text_input(
    "Enter Customer ID"
)

if customer:

    result = filtered_df[
        filtered_df['CustomerID']
        .astype(str)
        .str.contains(customer)
    ]

    st.dataframe(result)

# ---------------------------------
# CLUSTER INSIGHTS
# ---------------------------------
st.subheader("💡 Business Insights")

for cluster in sorted(
        filtered_df['Cluster'].unique()):

    temp = filtered_df[
        filtered_df['Cluster'] == cluster
    ]

    st.info(
        f"""
        Cluster {cluster}

        • Customers: {len(temp)}

        • Average Age: {temp['Age'].mean():.1f}

        • Average Income:
        {temp['Annual Income (k$)'].mean():.1f}k

        • Average Spending Score:
        {temp['Spending Score (1-100)'].mean():.1f}
        """
    )

# ---------------------------------
# DOWNLOAD DATA
# ---------------------------------
st.subheader("📥 Download Dataset")

csv = filtered_df.to_csv(index=False)

st.download_button(
    "Download Segmented Dataset",
    csv,
    file_name="Customer_Segmentation_Output.csv",
    mime="text/csv"
)