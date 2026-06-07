import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import time

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Play Store Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# ADVANCED CUSTOM CSS — CYBERPUNK NEON THEME
# ==========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&family=Share+Tech+Mono&display=swap');

/* ── Root Variables ── */
:root {
    --neon-cyan:    #00f5ff;
    --neon-pink:    #ff006e;
    --neon-green:   #39ff14;
    --neon-purple:  #bf00ff;
    --neon-orange:  #ff6600;
    --bg-deep:      #020408;
    --bg-card:      rgba(0,245,255,0.04);
    --border-glow:  rgba(0,245,255,0.25);
    --text-primary: #e8f4f8;
    --text-dim:     #7ba4b0;
}

/* ── Background & Base ── */
.stApp {
    background: var(--bg-deep) !important;
    font-family: 'Rajdhani', sans-serif !important;
}

.main .block-container {
    padding-top: 2rem !important;
    background: transparent !important;
}

/* Animated gradient background */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background:
        radial-gradient(ellipse at 20% 50%, rgba(0,245,255,0.08) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 20%, rgba(191,0,255,0.08) 0%, transparent 50%),
        radial-gradient(ellipse at 60% 80%, rgba(255,0,110,0.06) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
    animation: bgPulse 8s ease-in-out infinite alternate;
}

@keyframes bgPulse {
    0%   { opacity: 0.6; }
    100% { opacity: 1.0; }
}

/* Moving grid lines */
.stApp::after {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-image:
        linear-gradient(rgba(0,245,255,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,245,255,0.04) 1px, transparent 1px);
    background-size: 50px 50px;
    pointer-events: none;
    z-index: 0;
    animation: gridMove 20s linear infinite;
}

@keyframes gridMove {
    0%   { transform: translateY(0); }
    100% { transform: translateY(50px); }
}

/* ── Hero Title ── */
.hero-container {
    position: relative;
    text-align: center;
    padding: 3rem 0 2rem;
    z-index: 1;
}

.hero-title {
    font-family: 'Orbitron', monospace;
    font-weight: 900;
    font-size: clamp(2rem, 5vw, 4.5rem);
    letter-spacing: 0.08em;
    background: linear-gradient(135deg, var(--neon-cyan) 0%, var(--neon-purple) 50%, var(--neon-pink) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: titleGlow 3s ease-in-out infinite alternate, slideDown 0.8s ease-out;
    text-shadow: none;
    margin: 0;
}

@keyframes titleGlow {
    0%   { filter: drop-shadow(0 0 20px rgba(0,245,255,0.8)); }
    100% { filter: drop-shadow(0 0 40px rgba(191,0,255,0.9)); }
}

@keyframes slideDown {
    from { opacity:0; transform: translateY(-40px); }
    to   { opacity:1; transform: translateY(0); }
}

.hero-subtitle {
    font-family: 'Share Tech Mono', monospace;
    color: var(--text-dim);
    font-size: 1rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    margin-top: 0.75rem;
    animation: fadeIn 1.5s ease-out 0.4s both;
}

@keyframes fadeIn {
    from { opacity:0; transform: translateY(10px); }
    to   { opacity:1; transform: translateY(0); }
}

.hero-divider {
    width: 60%;
    margin: 1.5rem auto 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--neon-cyan), var(--neon-purple), var(--neon-pink), transparent);
    animation: scanLine 2s ease-in-out infinite;
}

@keyframes scanLine {
    0%, 100% { opacity: 0.4; transform: scaleX(0.8); }
    50%       { opacity: 1.0; transform: scaleX(1.0); }
}

/* ── KPI Cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.2rem;
    margin: 1.5rem 0;
    z-index: 1;
    position: relative;
}

.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border-glow);
    border-radius: 12px;
    padding: 1.5rem 1.2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(12px);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    animation: cardReveal 0.6s ease-out both;
}

.kpi-card:nth-child(1) { animation-delay: 0.1s; --accent: var(--neon-cyan);   }
.kpi-card:nth-child(2) { animation-delay: 0.2s; --accent: var(--neon-green);  }
.kpi-card:nth-child(3) { animation-delay: 0.3s; --accent: var(--neon-pink);   }
.kpi-card:nth-child(4) { animation-delay: 0.4s; --accent: var(--neon-orange); }

@keyframes cardReveal {
    from { opacity:0; transform: translateY(30px) scale(0.95); }
    to   { opacity:1; transform: translateY(0)   scale(1); }
}

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent);
    animation: shimmer 3s infinite;
}

@keyframes shimmer {
    0%   { left: -100%; }
    100% { left:  200%; }
}

.kpi-card:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0 0 30px var(--accent, var(--neon-cyan)), 0 0 60px rgba(0,245,255,0.1);
    border-color: var(--accent, var(--neon-cyan));
}

.kpi-icon {
    font-size: 2rem;
    display: block;
    margin-bottom: 0.5rem;
    filter: drop-shadow(0 0 8px var(--accent, var(--neon-cyan)));
}

.kpi-value {
    font-family: 'Orbitron', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--accent, var(--neon-cyan));
    text-shadow: 0 0 15px var(--accent, var(--neon-cyan));
    display: block;
    margin: 0.25rem 0;
}

.kpi-label {
    font-family: 'Share Tech Mono', monospace;
    color: var(--text-dim);
    font-size: 0.72rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
}

/* ── Section Headers ── */
.section-header {
    font-family: 'Orbitron', monospace;
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--neon-cyan);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    border-left: 4px solid var(--neon-cyan);
    padding-left: 1rem;
    margin: 2rem 0 1rem;
    text-shadow: 0 0 10px rgba(0,245,255,0.5);
    position: relative;
    z-index: 1;
}

/* ── Ticker Banner ── */
.ticker-wrap {
    width: 100%;
    overflow: hidden;
    background: rgba(0,245,255,0.08);
    border-top: 1px solid var(--border-glow);
    border-bottom: 1px solid var(--border-glow);
    padding: 8px 0;
    margin-bottom: 1.5rem;
    position: relative;
    z-index: 1;
}

.ticker {
    display: flex;
    white-space: nowrap;
    animation: tickerScroll 35s linear infinite;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.8rem;
    color: var(--neon-cyan);
    letter-spacing: 0.15em;
}

.ticker span { margin: 0 3rem; opacity: 0.75; }

@keyframes tickerScroll {
    0%   { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}

/* ── Insight Callout Cards ── */
.insight-card {
    background: rgba(191,0,255,0.07);
    border: 1px solid rgba(191,0,255,0.35);
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin: 0.75rem 0;
    font-family: 'Rajdhani', sans-serif;
    color: var(--text-primary);
    font-size: 1rem;
    position: relative;
    z-index: 1;
}

.insight-card strong {
    color: var(--neon-purple);
    font-family: 'Orbitron', monospace;
    font-size: 0.85rem;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: rgba(2,4,8,0.95) !important;
    border-right: 1px solid var(--border-glow) !important;
    backdrop-filter: blur(20px) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(0,245,255,0.05) !important;
    border-radius: 8px !important;
    padding: 4px !important;
    border: 1px solid var(--border-glow) !important;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Orbitron', monospace !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.1em !important;
    color: var(--text-dim) !important;
    border-radius: 6px !important;
}

.stTabs [aria-selected="true"] {
    background: rgba(0,245,255,0.15) !important;
    color: var(--neon-cyan) !important;
    box-shadow: 0 0 15px rgba(0,245,255,0.3) !important;
}

/* ── Progress Bars ── */
.stProgress > div > div {
    background: linear-gradient(90deg, var(--neon-cyan), var(--neon-purple)) !important;
    box-shadow: 0 0 10px rgba(0,245,255,0.5) !important;
    border-radius: 4px !important;
}

/* ── Multiselect Tags ── */
.stMultiSelect [data-baseweb="tag"] {
    background: rgba(0,245,255,0.2) !important;
    border: 1px solid var(--neon-cyan) !important;
    color: var(--neon-cyan) !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* ── Download Button ── */
.stDownloadButton button {
    background: linear-gradient(135deg, rgba(0,245,255,0.2), rgba(191,0,255,0.2)) !important;
    border: 1px solid var(--neon-cyan) !important;
    color: var(--neon-cyan) !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.1em !important;
    border-radius: 8px !important;
    transition: all 0.3s ease !important;
}
.stDownloadButton button:hover {
    box-shadow: 0 0 20px rgba(0,245,255,0.5) !important;
    transform: translateY(-2px) !important;
}

/* ── Success box ── */
.stSuccess {
    background: rgba(57,255,20,0.08) !important;
    border: 1px solid var(--neon-green) !important;
    border-radius: 8px !important;
    color: var(--neon-green) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb { background: var(--neon-cyan); border-radius: 3px; }

</style>
""", unsafe_allow_html=True)

# ==========================================
# PLOTLY THEME HELPER
# ==========================================

PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Rajdhani, sans-serif', color='#e8f4f8', size=12),
    title_font=dict(family='Orbitron, monospace', color='#00f5ff', size=15),
    colorway=['#00f5ff','#ff006e','#bf00ff','#39ff14','#ff6600','#ffdd00','#00bfff','#ff4466'],
    xaxis=dict(
        gridcolor='rgba(0,245,255,0.08)',
        zerolinecolor='rgba(0,245,255,0.2)',
        tickfont=dict(color='#7ba4b0'),
        title_font=dict(color='#00f5ff'),
    ),
    yaxis=dict(
        gridcolor='rgba(0,245,255,0.08)',
        zerolinecolor='rgba(0,245,255,0.2)',
        tickfont=dict(color='#7ba4b0'),
        title_font=dict(color='#00f5ff'),
    ),
    hoverlabel=dict(
        bgcolor='rgba(2,4,8,0.9)',
        bordercolor='#00f5ff',
        font=dict(family='Share Tech Mono, monospace', color='#00f5ff'),
    ),
    legend=dict(
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(0,245,255,0.2)',
        borderwidth=1,
        font=dict(color='#7ba4b0'),
    ),
    margin=dict(l=40, r=20, t=50, b=40),
)

def apply_theme(fig, title=None):
    fig.update_layout(**PLOTLY_LAYOUT)
    if title:
        fig.update_layout(title_text=title)
    return fig

# ==========================================
# LOAD DATA  — with auto path detection
# ==========================================

@st.cache_data
def load_data():
    # Look for CSVs next to this script file
    base_dir     = os.path.dirname(os.path.abspath(__file__))
    apps_path    = os.path.join(base_dir, "apps.csv")
    reviews_path = os.path.join(base_dir, "user_reviews.csv")

    if not os.path.exists(apps_path):
        st.error(
            f"❌ **googleplaystore.csv** not found in: `{base_dir}`\n\n"
            "Download it from https://www.kaggle.com/datasets/lava18/google-play-store-apps "
            "and place both CSV files in the same folder as this script."
        )
        st.stop()

    if not os.path.exists(reviews_path):
        st.error(
            f"❌ **googleplaystore_user_reviews.csv** not found in: `{base_dir}`\n\n"
            "Download it from https://www.kaggle.com/datasets/lava18/google-play-store-apps "
            "and place both CSV files in the same folder as this script."
        )
        st.stop()

    apps    = pd.read_csv(apps_path)
    reviews = pd.read_csv(reviews_path)
    return apps, reviews

apps, reviews = load_data()

# ==========================================
# DATA CLEANING
# ==========================================

apps = apps.drop_duplicates()

apps['Installs'] = (
    apps['Installs'].astype(str)
    .str.replace('+', '', regex=False)
    .str.replace(',', '', regex=False)
)
apps['Installs'] = pd.to_numeric(apps['Installs'], errors='coerce')
apps['Price']    = pd.to_numeric(
    apps['Price'].astype(str).str.replace('$', '', regex=False), errors='coerce'
)
apps['Reviews']  = pd.to_numeric(apps['Reviews'], errors='coerce')
apps['Rating']   = pd.to_numeric(apps['Rating'],  errors='coerce')

def convert_size(size):
    if pd.isna(size): return np.nan
    size = str(size)
    if "M" in size: return float(size.replace("M", ""))
    if "k" in size: return float(size.replace("k", "")) / 1024
    return np.nan

apps['Size_MB']     = apps['Size'].apply(convert_size)
apps['Last Updated'] = pd.to_datetime(apps['Last Updated'], errors='coerce')
apps['Update_Year']  = apps['Last Updated'].dt.year
apps['Min_Android']  = (
    apps['Android Ver'].astype(str)
    .str.extract(r'(\d+\.\d+|\d+)')[0]
    .astype(float)
)

# ==========================================
# SIDEBAR — CONTROL PANEL
# ==========================================

with st.sidebar:
    st.markdown("""
    <div style="font-family:'Orbitron',monospace; color:#00f5ff;
                font-size:1.1rem; font-weight:700; letter-spacing:0.1em;
                text-align:center; padding:1rem 0 0.5rem;
                text-shadow:0 0 12px rgba(0,245,255,0.7);">
        ⚡ CONTROL PANEL
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    all_cats = sorted(apps['Category'].dropna().unique())
    category = st.multiselect(
        "📂 Category Filter", all_cats, default=all_cats[:8],
        help="Select one or more app categories"
    )
    st.markdown("---")

    rating_range = st.slider("⭐ Rating Range", 0.0, 5.0, (3.0, 5.0), 0.1)
    st.markdown("---")

    app_type = st.radio("💳 App Type", ["All", "Free", "Paid"], index=0)
    st.markdown("---")

    min_installs = st.select_slider(
        "📥 Min Installs",
        options=[0, 1_000, 10_000, 100_000, 1_000_000, 10_000_000, 100_000_000],
        value=0,
        format_func=lambda x: f"{x:,}"
    )
    st.markdown("---")
    st.markdown("""
    <div style="font-family:'Share Tech Mono',monospace; color:#7ba4b0;
                font-size:0.7rem; letter-spacing:0.1em; text-align:center; padding-bottom:1rem;">
        KEERTHIKA.S<br>Data Analyst Project
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# FILTER DATA
# ==========================================

filtered = apps[apps['Category'].isin(category)].copy()
filtered = filtered[filtered['Rating'].between(*rating_range, inclusive='both')]
if app_type != "All":
    filtered = filtered[filtered['Type'] == app_type]
filtered = filtered[filtered['Installs'].fillna(0) >= min_installs]

# ==========================================
# HERO HEADER
# ==========================================

st.markdown("""
<div class="hero-container">
    <h1 class="hero-title">🚀 PLAY STORE INTELLIGENCE</h1>
    <p class="hero-subtitle">Advanced Analytics &nbsp;·&nbsp; Real-time Insights &nbsp;·&nbsp; Market Intelligence</p>
    <div class="hero-divider"></div>
</div>
""", unsafe_allow_html=True)

# ── Live Ticker Banner ──
top_app  = apps.sort_values('Installs', ascending=False)['App'].iloc[0]
top_cat  = apps['Category'].value_counts().idxmax()
avg_r    = round(apps['Rating'].mean(), 2)
free_pct = round(100 * (apps['Type'] == 'Free').mean())

ticker_items = (
    f"▶ TOTAL APPS IN STORE: {apps.shape[0]:,} &nbsp;"
    f"◆ GLOBAL AVG RATING: {avg_r} &nbsp;"
    f"▶ TOP CATEGORY: {top_cat} &nbsp;"
    f"◆ MOST INSTALLED: {top_app} &nbsp;"
    f"▶ FREE APP SHARE: {free_pct}% &nbsp;"
    f"◆ CURRENT FILTER: {len(filtered):,} APPS &nbsp;"
)

st.markdown(f"""
<div class="ticker-wrap">
  <div class="ticker">{ticker_items * 4}</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# KPI CARDS
# ==========================================

total_apps_f    = filtered.shape[0]
avg_rating_f    = round(filtered['Rating'].mean(), 2) if not filtered.empty else 0
total_installs  = int(filtered['Installs'].sum())
avg_price_paid  = round(
    filtered[filtered['Type'] == 'Paid']['Price'].mean(), 2
) if (filtered['Type'] == 'Paid').any() else 0.0

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card">
        <span class="kpi-icon">📱</span>
        <span class="kpi-value">{total_apps_f:,}</span>
        <span class="kpi-label">Total Apps</span>
    </div>
    <div class="kpi-card">
        <span class="kpi-icon">⭐</span>
        <span class="kpi-value">{avg_rating_f}</span>
        <span class="kpi-label">Avg Rating</span>
    </div>
    <div class="kpi-card">
        <span class="kpi-icon">📥</span>
        <span class="kpi-value">{total_installs:,}</span>
        <span class="kpi-label">Total Installs</span>
    </div>
    <div class="kpi-card">
        <span class="kpi-icon">💰</span>
        <span class="kpi-value">${avg_price_paid}</span>
        <span class="kpi-label">Avg Paid Price</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# TAB NAVIGATION
# ==========================================

tabs = st.tabs([
    "📊 OVERVIEW",
    "🔥 TOP APPS",
    "💰 MONETIZATION",
    "😊 SENTIMENT",
    "📈 TRENDS",
    "🗺️ DEEP DIVE",
])

# ─────────────────────────────────────────
# TAB 1 — OVERVIEW
# ─────────────────────────────────────────
with tabs[0]:

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown('<div class="section-header">APP DISTRIBUTION BY CATEGORY</div>', unsafe_allow_html=True)
        cat_counts = filtered['Category'].value_counts().reset_index()
        cat_counts.columns = ['Category', 'Count']
        fig = px.bar(
            cat_counts, x='Category', y='Count',
            color='Count',
            color_continuous_scale=['#00f5ff', '#bf00ff', '#ff006e']
        )
        fig.update_traces(marker_line_width=0)
        apply_theme(fig, "Apps per Category")
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">CONTENT RATING SHARE</div>', unsafe_allow_html=True)
        cr = filtered['Content Rating'].value_counts().reset_index()
        cr.columns = ['Rating_Label', 'Count']
        fig = px.pie(
            cr, names='Rating_Label', values='Count', hole=0.6,
            color_discrete_sequence=['#00f5ff', '#bf00ff', '#ff006e', '#39ff14', '#ff6600']
        )
        fig.update_traces(
            textfont=dict(family='Share Tech Mono', color='white'),
            marker=dict(line=dict(color='#020408', width=2))
        )
        apply_theme(fig, "Content Rating")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-header">RATING DISTRIBUTION</div>', unsafe_allow_html=True)
    rating_clean = filtered['Rating'].dropna()

    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=rating_clean, nbinsx=40,
        marker=dict(
            color='rgba(0,245,255,0.5)',
            line=dict(color='rgba(0,245,255,0.9)', width=1)
        ),
        name='Count',
    ))
    if len(rating_clean) > 0:
        fig.add_vline(
            x=rating_clean.mean(), line_dash='dash',
            line_color='#ff006e', line_width=2,
            annotation_text=f"Mean: {rating_clean.mean():.2f}",
            annotation_font=dict(color='#ff006e', family='Orbitron', size=11)
        )
    apply_theme(fig, "Rating Distribution")
    st.plotly_chart(fig, use_container_width=True)

    if len(rating_clean) > 0:
        high_rated = (rating_clean >= 4.5).sum()
        pct_high   = round(100 * high_rated / len(rating_clean), 1)
        st.markdown(f"""
        <div class="insight-card">
            <strong>💡 INSIGHT —</strong>
            {pct_high}% of apps in the current selection have a rating ≥ 4.5.
            The mean rating is {rating_clean.mean():.2f}, indicating a
            {'strong' if rating_clean.mean() > 4 else 'moderate'} overall quality
            signal across this cohort.
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">CATEGORY RATING LANDSCAPE</div>', unsafe_allow_html=True)
    fig = px.box(
        filtered, x='Category', y='Rating', color='Category',
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig.update_traces(marker_size=3, line_width=1.5)
    apply_theme(fig, "Rating by Category")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────
# TAB 2 — TOP APPS
# ─────────────────────────────────────────
with tabs[1]:

    st.markdown('<div class="section-header">TOP 20 MOST INSTALLED</div>', unsafe_allow_html=True)
    top20 = (
        filtered.dropna(subset=['Installs'])
        .sort_values('Installs', ascending=False)
        .head(20)
    )

    fig = go.Figure(go.Bar(
        x=top20['App'],
        y=top20['Installs'],
        marker=dict(
            color=top20['Installs'],
            colorscale=[[0, '#bf00ff'], [0.5, '#00f5ff'], [1, '#39ff14']],
            line=dict(color='rgba(0,0,0,0)', width=0),
        ),
        text=[
            f"{int(v/1e6)}M" if v >= 1e6 else f"{int(v/1e3)}K"
            for v in top20['Installs']
        ],
        textposition='outside',
        textfont=dict(family='Share Tech Mono', color='#00f5ff', size=9),
    ))
    apply_theme(fig, "Most Installed Apps")
    fig.update_layout(height=420)
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="section-header">TOP CATEGORIES BY TOTAL INSTALLS</div>', unsafe_allow_html=True)
        cat_installs = (
            filtered.groupby('Category')['Installs'].sum()
            .sort_values(ascending=False).head(15).reset_index()
        )
        fig = px.funnel(
            cat_installs, x='Installs', y='Category',
            color_discrete_sequence=['#00f5ff']
        )
        apply_theme(fig, "Category Install Funnel")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<div class="section-header">INSTALLS VS REVIEWS MATRIX</div>', unsafe_allow_html=True)
        scatter_df = filtered.dropna(subset=['Installs', 'Reviews', 'Rating']).copy()
        scatter_df = scatter_df[scatter_df['Installs'] > 0]
        fig = px.scatter(
            scatter_df.head(500),
            x='Reviews', y='Installs',
            color='Rating', size='Rating',
            hover_name='App',
            color_continuous_scale='Plasma',
            log_x=True, log_y=True
        )
        fig.update_traces(marker_opacity=0.7, marker_line_width=0)
        apply_theme(fig, "Reviews vs Installs (log scale)")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-header">CATEGORY INSTALL TREEMAP</div>', unsafe_allow_html=True)
    treemap_df = filtered.groupby('Category')['Installs'].sum().reset_index()
    fig = px.treemap(
        treemap_df, path=['Category'], values='Installs',
        color='Installs',
        color_continuous_scale=['#020408', '#00f5ff', '#bf00ff', '#ff006e']
    )
    apply_theme(fig, "Install Distribution Treemap")
    fig.update_traces(
        textfont=dict(family='Orbitron', size=11),
        marker=dict(line=dict(color='#020408', width=2))
    )
    st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────
# TAB 3 — MONETIZATION
# ─────────────────────────────────────────
with tabs[2]:

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown('<div class="section-header">FREE VS PAID</div>', unsafe_allow_html=True)
        fig = px.pie(
            filtered, names='Type', hole=0.6,
            color_discrete_sequence=['#00f5ff', '#ff006e']
        )
        fig.update_traces(
            textfont=dict(family='Share Tech Mono', color='white'),
            marker=dict(line=dict(color='#020408', width=3))
        )
        apply_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<div class="section-header">PRICE BUCKETS</div>', unsafe_allow_html=True)
        paid_df = filtered[filtered['Type'] == 'Paid'].dropna(subset=['Price']).copy()
        if not paid_df.empty:
            bins   = [0, 1, 2, 5, 10, 20, 50, 500]
            labels = ['<$1', '$1-2', '$2-5', '$5-10', '$10-20', '$20-50', '$50+']
            paid_df['Price_Bucket'] = pd.cut(paid_df['Price'], bins=bins, labels=labels)
            pb = paid_df['Price_Bucket'].value_counts().sort_index().reset_index()
            pb.columns = ['Price Range', 'Count']
            fig = px.bar(
                pb, x='Price Range', y='Count',
                color='Count',
                color_continuous_scale=['#39ff14', '#00f5ff', '#ff006e']
            )
            apply_theme(fig, "Paid App Price Distribution")
            fig.update_coloraxes(showscale=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No paid apps in current filter.")

    with c3:
        st.markdown('<div class="section-header">AVG PRICE BY CATEGORY</div>', unsafe_allow_html=True)
        if not paid_df.empty:
            apc = (
                paid_df.groupby('Category')['Price'].mean()
                .sort_values(ascending=False).head(10).reset_index()
            )
            fig = px.bar(
                apc, x='Price', y='Category', orientation='h',
                color='Price',
                color_continuous_scale=['#bf00ff', '#ff006e']
            )
            apply_theme(fig, "Avg Price by Category (Top 10)")
            fig.update_coloraxes(showscale=False)
            st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-header">ESTIMATED REVENUE BY CATEGORY (PAID APPS)</div>', unsafe_allow_html=True)
    paid_rev = filtered[filtered['Type'] == 'Paid'].dropna(subset=['Price', 'Installs']).copy()
    if not paid_rev.empty:
        paid_rev['Est_Revenue'] = paid_rev['Price'] * paid_rev['Installs']
        rev_cat = (
            paid_rev.groupby('Category')['Est_Revenue'].sum()
            .sort_values(ascending=False).head(12).reset_index()
        )
        fig = px.bar(
            rev_cat, x='Category', y='Est_Revenue',
            color='Est_Revenue',
            color_continuous_scale=['#bf00ff', '#00f5ff', '#39ff14']
        )
        fig.update_traces(marker_line_width=0)
        apply_theme(fig, "Est. Revenue = Installs × Price")
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div class="insight-card">
        <strong>⚠️ NOTE —</strong>
        Estimated revenue is computed as <em>Installs × Price</em> and represents a rough
        upper-bound approximation. Actual revenue will differ due to refunds, promotions,
        regional pricing, and in-app purchase dynamics.
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────
# TAB 4 — SENTIMENT
# ─────────────────────────────────────────
with tabs[3]:

    @st.cache_data
    def compute_sentiment(rev_df):
        rev_df = rev_df.dropna(subset=['Translated_Review']).copy()

        def get_sentiment(text):
            score = TextBlob(str(text)).sentiment.polarity
            if score > 0.1:    return "Positive"
            elif score < -0.1: return "Negative"
            else:              return "Neutral"

        def get_score(text):
            return TextBlob(str(text)).sentiment.polarity

        def get_subjectivity(text):
            return TextBlob(str(text)).sentiment.subjectivity

        rev_df['Sentiment']      = rev_df['Translated_Review'].apply(get_sentiment)
        rev_df['Polarity_Score'] = rev_df['Translated_Review'].apply(get_score)
        rev_df['Subjectivity']   = rev_df['Translated_Review'].apply(get_subjectivity)
        return rev_df

    with st.spinner("⚡ Running NLP sentiment engine..."):
        reviews_clean = compute_sentiment(reviews)

    color_map = {'Positive': '#39ff14', 'Negative': '#ff006e', 'Neutral': '#00f5ff'}

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="section-header">SENTIMENT DISTRIBUTION</div>', unsafe_allow_html=True)
        sc = reviews_clean['Sentiment'].value_counts().reset_index()
        sc.columns = ['Sentiment', 'Count']
        fig = px.pie(
            sc, names='Sentiment', values='Count', hole=0.55,
            color='Sentiment', color_discrete_map=color_map
        )
        fig.update_traces(
            textfont=dict(family='Share Tech Mono', color='white'),
            marker=dict(line=dict(color='#020408', width=3))
        )
        apply_theme(fig, "Review Sentiments")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<div class="section-header">POLARITY SCORE DISTRIBUTION</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fill_map = {'Positive': 'rgba(57,255,20,0.15)', 'Negative': 'rgba(255,0,110,0.15)', 'Neutral': 'rgba(0,245,255,0.15)'}
        for sent, grp in reviews_clean.groupby('Sentiment'):
            fig.add_trace(go.Violin(
                y=grp['Polarity_Score'], name=sent,
                line_color=color_map.get(sent, '#00f5ff'),
                fillcolor=fill_map.get(sent, 'rgba(0,245,255,0.15)'),
                box_visible=True, meanline_visible=True,
            ))
        apply_theme(fig, "Polarity Score by Sentiment")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-header">POLARITY × SUBJECTIVITY SPACE</div>', unsafe_allow_html=True)
    sample = reviews_clean.sample(min(1500, len(reviews_clean)), random_state=42)
    fig = px.scatter(
        sample, x='Polarity_Score', y='Subjectivity',
        color='Sentiment', color_discrete_map=color_map,
        opacity=0.6, hover_data=['Translated_Review']
    )
    fig.update_traces(marker_size=4, marker_line_width=0)
    apply_theme(fig, "NLP Space: Polarity vs Subjectivity")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-header">WORD CLOUD — TOP REVIEW TERMS</div>', unsafe_allow_html=True)
    wc_col1, wc_col2, wc_col3 = st.columns(3)
    wc_targets = [('Positive', '#39ff14'), ('Negative', '#ff006e'), ('Neutral', '#00f5ff')]

    for col, (sentiment_label, color_hex) in zip([wc_col1, wc_col2, wc_col3], wc_targets):
        with col:
            st.markdown(
                f"<p style='font-family:Orbitron,monospace;color:{color_hex};"
                f"font-size:0.8rem;text-align:center;letter-spacing:0.15em;'>"
                f"{sentiment_label.upper()} REVIEWS</p>",
                unsafe_allow_html=True
            )
            subset = reviews_clean[reviews_clean['Sentiment'] == sentiment_label]['Translated_Review']
            text   = " ".join(subset.astype(str))
            r_int, g_int, b_int = tuple(int(color_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

            r_val, g_val, b_val = r_int, g_int, b_int

            def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
                # PIL only accepts rgb(...) not rgba(...)
                brightness = np.random.randint(180, 256)
                r_out = min(255, int(r_val * brightness / 255))
                g_out = min(255, int(g_val * brightness / 255))
                b_out = min(255, int(b_val * brightness / 255))
                return f"rgb({r_out},{g_out},{b_out})"

            wordcloud_img = WordCloud(
                width=400, height=250,
                background_color=None, mode='RGBA',
                color_func=color_func,
                max_words=80, prefer_horizontal=0.7
            ).generate(text)

            fig, ax = plt.subplots(figsize=(5, 3))
            fig.patch.set_alpha(0)
            ax.set_facecolor('none')
            ax.imshow(wordcloud_img, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)
            plt.close()


# ─────────────────────────────────────────
# TAB 5 — TRENDS
# ─────────────────────────────────────────
with tabs[4]:

    st.markdown('<div class="section-header">APP UPDATES OVER THE YEARS</div>', unsafe_allow_html=True)
    yearly = (
        filtered.dropna(subset=['Update_Year'])
        .groupby('Update_Year')['App'].count().reset_index()
    )
    yearly.columns = ['Year', 'Count']
    yearly = yearly[yearly['Year'] >= 2010]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=yearly['Year'], y=yearly['Count'],
        mode='lines+markers',
        line=dict(color='#00f5ff', width=3),
        marker=dict(color='#bf00ff', size=8, line=dict(color='#00f5ff', width=2)),
        fill='tozeroy',
        fillcolor='rgba(0,245,255,0.07)',
        name='Apps Updated',
    ))
    apply_theme(fig, "Apps Updated Per Year")
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="section-header">CATEGORY EVOLUTION (STACKED)</div>', unsafe_allow_html=True)
        top_cats = filtered['Category'].value_counts().head(6).index
        cat_year = (
            filtered.dropna(subset=['Update_Year', 'Category'])
            .groupby(['Update_Year', 'Category'])['App'].count().reset_index()
        )
        cat_year = cat_year[
            (cat_year['Update_Year'] >= 2013) & (cat_year['Category'].isin(top_cats))
        ]
        fig = px.area(
            cat_year, x='Update_Year', y='App', color='Category',
            color_discrete_sequence=['#00f5ff', '#bf00ff', '#ff006e', '#39ff14', '#ff6600', '#ffdd00']
        )
        apply_theme(fig, "Top Categories by Update Year")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<div class="section-header">ANDROID VERSION SUPPORT</div>', unsafe_allow_html=True)
        android_ver = (
            filtered.dropna(subset=['Min_Android'])
            .groupby('Min_Android')['App'].count().reset_index()
        )
        android_ver.columns = ['Android Version', 'Count']
        fig = px.bar(
            android_ver.sort_values('Android Version'),
            x='Android Version', y='Count',
            color='Count',
            color_continuous_scale=['#00f5ff', '#bf00ff']
        )
        apply_theme(fig, "Min Android Version Required")
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-header">🎬 ANIMATED INSTALL RACE BY CATEGORY</div>', unsafe_allow_html=True)
    anim_df = (
        filtered.dropna(subset=['Update_Year', 'Installs'])
        .groupby(['Update_Year', 'Category'])['Installs'].sum().reset_index()
    )
    anim_df = anim_df[anim_df['Update_Year'].between(2013, 2018)]

    if not anim_df.empty:
        fig = px.bar(
            anim_df, x='Installs', y='Category',
            animation_frame='Update_Year',
            orientation='h', color='Installs',
            color_continuous_scale=['#bf00ff', '#00f5ff', '#39ff14'],
            range_x=[0, anim_df['Installs'].max() * 1.1]
        )
        fig.update_layout(
            updatemenus=[dict(
                type='buttons', showactive=False,
                buttons=[dict(
                    label='▶  PLAY', method='animate',
                    args=[None, dict(frame=dict(duration=800, redraw=True), fromcurrent=True)]
                )]
            )],
            sliders=[dict(currentvalue=dict(
                font=dict(family='Orbitron', color='#00f5ff', size=11),
                prefix='YEAR: '
            ))]
        )
        apply_theme(fig, "Install Race — Category vs Year")
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Not enough data for animation with current filters.")


# ─────────────────────────────────────────
# TAB 6 — DEEP DIVE
# ─────────────────────────────────────────
with tabs[5]:

    st.markdown('<div class="section-header">🔍 APP LOOKUP</div>', unsafe_allow_html=True)
    search_term = st.text_input("Search for an app", placeholder="e.g. Facebook, Spotify, Camera ...")
    if search_term:
        result = filtered[filtered['App'].str.contains(search_term, case=False, na=False)]
        if not result.empty:
            st.dataframe(
                result[['App', 'Category', 'Rating', 'Reviews', 'Installs',
                         'Type', 'Price', 'Size_MB', 'Content Rating']]
                .sort_values('Installs', ascending=False)
                .head(20),
                use_container_width=True,
            )
        else:
            st.warning("No apps found matching that query in the current filter set.")

    st.markdown('<div class="section-header">DATASET PREVIEW</div>', unsafe_allow_html=True)
    st.dataframe(filtered.head(50), use_container_width=True)

    csv = filtered.to_csv(index=False)
    st.download_button(
        "⬇  EXPORT FILTERED DATA (.CSV)",
        csv,
        file_name="play_store_filtered.csv",
        mime="text/csv"
    )

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")
st.markdown("""
<div style="text-align:center; padding:1.5rem 0 0.5rem;">
    <div style="font-family:'Orbitron',monospace; color:#00f5ff; font-size:0.85rem;
                letter-spacing:0.2em; text-shadow:0 0 10px rgba(0,245,255,0.5);">
        PLAY STORE INTELLIGENCE ·KEERTHIKA.S
    </div>
    <div style="font-family:'Share Tech Mono',monospace; color:#7ba4b0;
                font-size:0.7rem; letter-spacing:0.15em; margin-top:0.4rem;">
        NLP · SENTIMENT ANALYSIS · TREND DETECTION · MARKET INTELLIGENCE
    </div>
</div>
""", unsafe_allow_html=True)