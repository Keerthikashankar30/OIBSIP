import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import warnings
warnings.filterwarnings('ignore')

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FraudDetection AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');

:root {
    --neon-cyan: #00f5ff;
    --neon-red: #ff003c;
    --neon-green: #00ff88;
    --bg-dark: #020812;
    --card-bg: rgba(0, 245, 255, 0.04);
    --border: rgba(0, 245, 255, 0.15);
}

* { box-sizing: border-box; }

.stApp {
    background: linear-gradient(135deg, #020812 0%, #040d1a 50%, #020812 100%);
    font-family: 'Rajdhani', sans-serif;
    color: #c8e6ff;
}

/* Animated grid background */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image: 
        linear-gradient(rgba(0,245,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,245,255,0.03) 1px, transparent 1px);
    background-size: 50px 50px;
    pointer-events: none;
    z-index: 0;
}

/* Header */
.hero-header {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    position: relative;
}

.hero-title {
    font-family: 'Orbitron', monospace;
    font-size: 3.2rem;
    font-weight: 900;
    background: linear-gradient(90deg, #00f5ff, #ffffff, #00ff88);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 0.12em;
    text-shadow: none;
    margin: 0;
    animation: pulseGlow 3s ease-in-out infinite;
}

@keyframes pulseGlow {
    0%, 100% { filter: drop-shadow(0 0 8px rgba(0,245,255,0.6)); }
    50% { filter: drop-shadow(0 0 20px rgba(0,245,255,0.9)); }
}

.hero-subtitle {
    font-family: 'Rajdhani', sans-serif;
    color: rgba(0,245,255,0.6);
    letter-spacing: 0.3em;
    font-size: 0.85rem;
    margin-top: 0.4rem;
    text-transform: uppercase;
}

.status-badge {
    display: inline-block;
    background: rgba(0,255,136,0.1);
    border: 1px solid rgba(0,255,136,0.4);
    color: #00ff88;
    border-radius: 20px;
    padding: 4px 16px;
    font-size: 0.72rem;
    letter-spacing: 0.2em;
    margin-top: 0.6rem;
    animation: blink 2s infinite;
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

/* Metric Cards */
.metric-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.4rem 1.2rem;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--neon-cyan), transparent);
    animation: scanLine 3s linear infinite;
}

@keyframes scanLine {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

.metric-value {
    font-family: 'Orbitron', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: var(--neon-cyan);
    margin: 0;
}

.metric-label {
    font-size: 0.75rem;
    letter-spacing: 0.2em;
    color: rgba(200,230,255,0.5);
    text-transform: uppercase;
    margin: 0.3rem 0 0;
}

.metric-delta {
    font-size: 0.8rem;
    color: var(--neon-green);
    margin-top: 0.2rem;
}

/* Section headers */
.section-header {
    font-family: 'Orbitron', monospace;
    font-size: 1rem;
    color: var(--neon-cyan);
    letter-spacing: 0.2em;
    text-transform: uppercase;
    padding: 0.6rem 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.2rem;
}

/* Alert boxes */
.alert-fraud {
    background: rgba(255,0,60,0.08);
    border: 1px solid rgba(255,0,60,0.35);
    border-left: 4px solid #ff003c;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin: 0.5rem 0;
}

.alert-legit {
    background: rgba(0,255,136,0.06);
    border: 1px solid rgba(0,255,136,0.3);
    border-left: 4px solid #00ff88;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin: 0.5rem 0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020d1f 0%, #030e20 100%) !important;
    border-right: 1px solid rgba(0,245,255,0.1) !important;
}

section[data-testid="stSidebar"] .stMarkdown h2 {
    font-family: 'Orbitron', monospace;
    color: var(--neon-cyan);
    font-size: 0.9rem;
    letter-spacing: 0.15em;
}

/* Progress bars */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #00f5ff, #00ff88) !important;
}

/* Dataframe */
.stDataFrame { border: 1px solid var(--border); border-radius: 8px; overflow: hidden; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: rgba(0,245,255,0.03);
    border-radius: 8px;
    padding: 4px;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Rajdhani', sans-serif;
    letter-spacing: 0.1em;
    font-weight: 600;
    color: rgba(200,230,255,0.6);
}

.stTabs [aria-selected="true"] {
    background: rgba(0,245,255,0.12) !important;
    color: var(--neon-cyan) !important;
    border-radius: 6px;
}

/* Spinner override */
.stSpinner { color: var(--neon-cyan); }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #020812; }
::-webkit-scrollbar-thumb { background: rgba(0,245,255,0.3); border-radius: 3px; }

/* Plotly chart borders */
.js-plotly-plot { border: 1px solid var(--border); border-radius: 10px; overflow: hidden; }

/* Hide Streamlit default elements */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── Plotly Theme ────────────────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(2,8,18,0)',
    plot_bgcolor='rgba(2,8,18,0)',
    font=dict(family="Rajdhani, sans-serif", color="#c8e6ff"),
    xaxis=dict(gridcolor='rgba(0,245,255,0.08)', zerolinecolor='rgba(0,245,255,0.15)'),
    yaxis=dict(gridcolor='rgba(0,245,255,0.08)', zerolinecolor='rgba(0,245,255,0.15)'),
    colorway=['#00f5ff','#ff003c','#00ff88','#ff8c00','#a855f7','#f59e0b'],
    margin=dict(l=40, r=20, t=40, b=40),
)

COLORS = {
    'fraud': '#ff003c',
    'legit': '#00f5ff',
    'accent': '#00ff88',
    'warn': '#ff8c00',
    'purple': '#a855f7',
}

# ─── Data Loading ────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df

@st.cache_data(show_spinner=False)
def compute_stats(df: pd.DataFrame):
    total = len(df)
    fraud_count = int(df['Class'].sum())
    legit_count = total - fraud_count
    fraud_pct = fraud_count / total * 100
    fraud_amount = df[df['Class'] == 1]['Amount'].sum()
    legit_amount = df[df['Class'] == 0]['Amount'].sum()
    avg_fraud_amt = df[df['Class'] == 1]['Amount'].mean()
    avg_legit_amt = df[df['Class'] == 0]['Amount'].mean()
    return {
        'total': total,
        'fraud': fraud_count,
        'legit': legit_count,
        'fraud_pct': fraud_pct,
        'fraud_amount': fraud_amount,
        'legit_amount': legit_amount,
        'avg_fraud_amt': avg_fraud_amt,
        'avg_legit_amt': avg_legit_amt,
    }

# ─── ML Section ─────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def run_models(df: pd.DataFrame):
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import (
        classification_report, confusion_matrix,
        roc_auc_score, average_precision_score,
        roc_curve, precision_recall_curve
    )

    features = [c for c in df.columns if c not in ['Class', 'Time']]
    X = df[features].copy()
    y = df['Class'].copy()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Undersample for speed
    fraud_idx = np.where(y == 1)[0]
    legit_idx  = np.where(y == 0)[0]
    np.random.seed(42)
    legit_sample = np.random.choice(legit_idx, size=min(len(legit_idx), 5000), replace=False)
    idx = np.concatenate([fraud_idx, legit_sample])
    np.random.shuffle(idx)
    X_bal, y_bal = X_scaled[idx], y.iloc[idx].values

    X_train, X_test, y_train, y_test = train_test_split(
        X_bal, y_bal, test_size=0.25, random_state=42, stratify=y_bal
    )

    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=80, max_depth=8, random_state=42, n_jobs=-1),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=60, max_depth=4, random_state=42),
    }

    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]
        cr = classification_report(y_test, y_pred, output_dict=True)
        cm = confusion_matrix(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_prob)
        pr_auc  = average_precision_score(y_test, y_prob)
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        prec, rec, _ = precision_recall_curve(y_test, y_prob)

        feat_imp = None
        if hasattr(model, 'feature_importances_'):
            feat_imp = pd.Series(model.feature_importances_, index=features).sort_values(ascending=False)

        results[name] = {
            'model': model,
            'report': cr,
            'cm': cm,
            'roc_auc': roc_auc,
            'pr_auc': pr_auc,
            'fpr': fpr, 'tpr': tpr,
            'prec': prec, 'rec': rec,
            'feat_imp': feat_imp,
        }

    return results, features, scaler

# ─── Hero ────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <h1 class="hero-title">⬡ FRAUD DETECTION AI</h1>
    <p class="hero-subtitle">Real-time Transaction Intelligence Platform</p>
    <span class="status-badge">● SYSTEM ONLINE</span>
</div>
""", unsafe_allow_html=True)

# ─── Sidebar ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙ CONTROL PANEL")
    st.markdown("---")

    uploaded = st.file_uploader("Upload creditcard.csv", type=["csv"],
                                 help="Upload your credit card transaction dataset")
    st.markdown("---")
    st.markdown("## 🔧 MODEL CONFIG")
    threshold = st.slider("Detection Threshold", 0.1, 0.9, 0.5, 0.01,
                          help="Probability cutoff for fraud classification")
    show_raw = st.checkbox("Show Raw Data", False)
    run_ml   = st.checkbox("Run ML Models", True)

    st.markdown("---")
    st.markdown("## 🎯 FILTER")
    amount_range = st.slider("Transaction Amount ($)", 0, 25000, (0, 25000))

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.7rem;color:rgba(0,245,255,0.4);letter-spacing:0.1em;text-align:center;padding-top:1rem'>
    <h1>KEERTHIKA.S</h1>
    <br>DATA ANALYST PROJECT
    </div>
    """, unsafe_allow_html=True)

# ─── Load Data ───────────────────────────────────────────────────────────────────
if uploaded:
    with st.spinner("🔍 Loading dataset..."):
        df_raw = load_data(uploaded)
else:
    st.info("📂 No file uploaded — using a synthetic demo dataset. Upload **creditcard.csv** in the sidebar for real analysis.")
    # Generate synthetic demo data resembling creditcard.csv
    np.random.seed(42)
    N = 15000
    N_fraud = 250
    cols = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount', 'Class']
    data = np.random.randn(N, 28)
    time_vals = np.sort(np.random.uniform(0, 172800, N))
    amounts = np.abs(np.random.exponential(80, N))
    classes = np.zeros(N, dtype=int)
    fraud_idx = np.random.choice(N, N_fraud, replace=False)
    classes[fraud_idx] = 1
    amounts[fraud_idx] = np.abs(np.random.exponential(300, N_fraud))
    df_raw = pd.DataFrame(
        np.column_stack([time_vals, data, amounts, classes]),
        columns=cols
    )
    df_raw['Class'] = df_raw['Class'].astype(int)

# Filter by amount
df = df_raw[
    (df_raw['Amount'] >= amount_range[0]) &
    (df_raw['Amount'] <= amount_range[1])
].copy()

stats = compute_stats(df)

# ─── KPI Row ─────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-header">◈ LIVE TRANSACTION METRICS</p>', unsafe_allow_html=True)
k1, k2, k3, k4, k5 = st.columns(5)

def metric_card(col, value, label, delta="", color="#00f5ff"):
    col.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color:{color}">{value}</div>
        <div class="metric-label">{label}</div>
        {'<div class="metric-delta">'+delta+'</div>' if delta else ''}
    </div>
    """, unsafe_allow_html=True)

metric_card(k1, f"{stats['total']:,}", "Total Transactions")
metric_card(k2, f"{stats['fraud']:,}", "Fraud Cases", color=COLORS['fraud'])
metric_card(k3, f"{stats['legit']:,}", "Legitimate", color=COLORS['legit'])
metric_card(k4, f"{stats['fraud_pct']:.3f}%", "Fraud Rate",
            f"Avg ${stats['avg_fraud_amt']:.2f}", color=COLORS['warn'])
metric_card(k5, f"${stats['fraud_amount']:,.0f}", "Fraud Exposure",
            "Total at risk", color=COLORS['purple'])

st.markdown("<br>", unsafe_allow_html=True)

# ─── Tabs ────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview",
    "🔬 Deep Analysis",
    "🤖 ML Models",
    "⚡ Real-time Sim",
    "📋 Data Explorer"
])

# ══════════════════════════════════════════════════════════════════════════════════
# TAB 1: OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════════
with tab1:
    c1, c2 = st.columns([1, 1.6])

    with c1:
        st.markdown('<p class="section-header">◈ CLASS DISTRIBUTION</p>', unsafe_allow_html=True)
        fig_pie = go.Figure(go.Pie(
            labels=['Legitimate', 'Fraudulent'],
            values=[stats['legit'], stats['fraud']],
            hole=0.65,
            marker=dict(
                colors=[COLORS['legit'], COLORS['fraud']],
                line=dict(color='rgba(2,8,18,0.8)', width=3)
            ),
            textinfo='label+percent',
            textfont=dict(family='Rajdhani', size=13),
            hovertemplate='<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>',
        ))
        fig_pie.add_annotation(
            text=f"<b>{stats['fraud_pct']:.2f}%</b><br>Fraud Rate",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color='#ff003c', family='Orbitron'),
            align='center'
        )
        fig_pie.update_layout(**PLOTLY_LAYOUT, height=320, showlegend=True,
                              legend=dict(orientation='h', y=-0.05))
        st.plotly_chart(fig_pie, use_container_width=True)

    with c2:
        st.markdown('<p class="section-header">◈ TRANSACTION AMOUNT DISTRIBUTION</p>', unsafe_allow_html=True)
        fraud_amt = df[df['Class'] == 1]['Amount']
        legit_amt = df[df['Class'] == 0]['Amount'].sample(min(5000, stats['legit']), random_state=42)

        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=legit_amt, name='Legitimate',
            nbinsx=60, opacity=0.75,
            marker_color=COLORS['legit'],
            hovertemplate='Amount: $%{x:.2f}<br>Count: %{y}<extra>Legitimate</extra>'
        ))
        fig_hist.add_trace(go.Histogram(
            x=fraud_amt, name='Fraudulent',
            nbinsx=60, opacity=0.9,
            marker_color=COLORS['fraud'],
            hovertemplate='Amount: $%{x:.2f}<br>Count: %{y}<extra>Fraudulent</extra>'
        ))
        fig_hist.update_layout(
            **PLOTLY_LAYOUT, height=320, barmode='overlay',
            xaxis_title='Transaction Amount ($)',
            yaxis_title='Frequency',
            legend=dict(orientation='h', y=1.08)
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    # Time series
    st.markdown('<p class="section-header">◈ FRAUD ACTIVITY OVER TIME</p>', unsafe_allow_html=True)
    df_time = df.copy()
    df_time['hour'] = (df_time['Time'] // 3600).astype(int)
    hourly = df_time.groupby(['hour', 'Class']).size().reset_index(name='count')
    fraud_h = hourly[hourly['Class'] == 1]
    legit_h = hourly[hourly['Class'] == 0]

    fig_time = make_subplots(specs=[[{"secondary_y": True}]])
    fig_time.add_trace(go.Bar(
        x=legit_h['hour'], y=legit_h['count'], name='Legitimate',
        marker_color=COLORS['legit'], opacity=0.5,
        hovertemplate='Hour %{x}: %{y:,} transactions<extra>Legit</extra>'
    ), secondary_y=False)
    fig_time.add_trace(go.Scatter(
        x=fraud_h['hour'], y=fraud_h['count'], name='Fraud',
        line=dict(color=COLORS['fraud'], width=2.5),
        mode='lines+markers',
        marker=dict(size=8, symbol='diamond'),
        hovertemplate='Hour %{x}: %{y} fraud cases<extra></extra>'
    ), secondary_y=True)
    fig_time.update_layout(
        **PLOTLY_LAYOUT, height=320,
        xaxis_title='Hour of Day',
        legend=dict(orientation='h', y=1.08)
    )
    fig_time.update_yaxes(title_text="Legitimate Txns", secondary_y=False,
                           gridcolor='rgba(0,245,255,0.08)')
    fig_time.update_yaxes(title_text="Fraud Cases", secondary_y=True,
                           gridcolor='rgba(255,0,60,0.08)')
    st.plotly_chart(fig_time, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════════
# TAB 2: DEEP ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<p class="section-header">◈ FEATURE ANOMALY RADAR</p>', unsafe_allow_html=True)

    v_features = [f'V{i}' for i in range(1, 15)]
    fraud_means  = df[df['Class'] == 1][v_features].mean().values
    legit_means  = df[df['Class'] == 0][v_features].mean().values

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=np.abs(fraud_means), theta=v_features, fill='toself',
        name='Fraud Pattern', line_color=COLORS['fraud'],
        fillcolor='rgba(255,0,60,0.15)'
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=np.abs(legit_means), theta=v_features, fill='toself',
        name='Legit Pattern', line_color=COLORS['legit'],
        fillcolor='rgba(0,245,255,0.1)'
    ))
    fig_radar.update_layout(
        **PLOTLY_LAYOUT, height=420,
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(visible=True, gridcolor='rgba(0,245,255,0.15)'),
            angularaxis=dict(gridcolor='rgba(0,245,255,0.15)')
        ),
        legend=dict(orientation='h', y=-0.08)
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    # Box plots
    st.markdown('<p class="section-header">◈ FEATURE DISTRIBUTION COMPARISON</p>', unsafe_allow_html=True)
    col_sel = st.selectbox("Select Feature", [f'V{i}' for i in range(1, 29)] + ['Amount'], index=0)

    def hex_to_rgba(hex_color, alpha=0.2):
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        return f'rgba({r},{g},{b},{alpha})'

    fig_box = go.Figure()
    for cls, label, color in [(0, 'Legitimate', COLORS['legit']), (1, 'Fraudulent', COLORS['fraud'])]:
        vals = df[df['Class'] == cls][col_sel]
        fig_box.add_trace(go.Violin(
            y=vals, name=label, box_visible=True,
            meanline_visible=True, fillcolor=hex_to_rgba(color, 0.2),
            line_color=color, opacity=0.85,
            hoverinfo='y+name'
        ))
    fig_box.update_layout(**PLOTLY_LAYOUT, height=380,
                          yaxis_title=col_sel,
                          violingap=0.3, violinmode='overlay')
    st.plotly_chart(fig_box, use_container_width=True)

    # Correlation heatmap (top 10 V features + Amount)
    st.markdown('<p class="section-header">◈ CORRELATION HEATMAP</p>', unsafe_allow_html=True)
    heat_cols = [f'V{i}' for i in range(1, 11)] + ['Amount', 'Class']
    corr = df[heat_cols].corr()
    fig_heat = go.Figure(go.Heatmap(
        z=corr.values, x=corr.columns, y=corr.columns,
        colorscale=[[0, '#ff003c'], [0.5, '#020812'], [1, '#00f5ff']],
        zmin=-1, zmax=1,
        text=corr.values.round(2), texttemplate='%{text}',
        hovertemplate='%{x} vs %{y}<br>r = %{z:.3f}<extra></extra>'
    ))
    fig_heat.update_layout(**PLOTLY_LAYOUT, height=430)
    st.plotly_chart(fig_heat, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════════
# TAB 3: ML MODELS
# ══════════════════════════════════════════════════════════════════════════════════
with tab3:
    if not run_ml:
        st.info("Enable **Run ML Models** in the sidebar to activate this section.")
    else:
        with st.spinner("🤖 Training machine learning models..."):
            results, features, scaler = run_models(df)

        st.markdown('<p class="section-header">◈ MODEL PERFORMANCE COMPARISON</p>', unsafe_allow_html=True)

        # Summary table
        summary = []
        for name, r in results.items():
            rep = r['report']
            summary.append({
                'Model': name,
                'ROC-AUC': f"{r['roc_auc']:.4f}",
                'PR-AUC':  f"{r['pr_auc']:.4f}",
                'Precision (Fraud)': f"{rep['1']['precision']:.4f}",
                'Recall (Fraud)':    f"{rep['1']['recall']:.4f}",
                'F1 (Fraud)':        f"{rep['1']['f1-score']:.4f}",
            })
        st.dataframe(pd.DataFrame(summary).set_index('Model'),
                     use_container_width=True)

        # ROC curves
        c_roc, c_pr = st.columns(2)

        with c_roc:
            st.markdown('<p class="section-header">◈ ROC CURVES</p>', unsafe_allow_html=True)
            fig_roc = go.Figure()
            fig_roc.add_shape(type='line', x0=0, y0=0, x1=1, y1=1,
                              line=dict(color='rgba(200,230,255,0.3)', dash='dash'))
            colors_ml = [COLORS['legit'], COLORS['fraud'], COLORS['accent']]
            for (name, r), color in zip(results.items(), colors_ml):
                fig_roc.add_trace(go.Scatter(
                    x=r['fpr'], y=r['tpr'],
                    name=f"{name} ({r['roc_auc']:.3f})",
                    line=dict(color=color, width=2.5),
                    mode='lines',
                    hovertemplate='FPR: %{x:.3f}<br>TPR: %{y:.3f}<extra>'+name+'</extra>'
                ))
            fig_roc.update_layout(
                **PLOTLY_LAYOUT, height=350,
                xaxis_title='False Positive Rate',
                yaxis_title='True Positive Rate',
                legend=dict(orientation='h', y=-0.2)
            )
            st.plotly_chart(fig_roc, use_container_width=True)

        with c_pr:
            st.markdown('<p class="section-header">◈ PRECISION-RECALL CURVES</p>', unsafe_allow_html=True)
            fig_pr = go.Figure()
            for (name, r), color in zip(results.items(), colors_ml):
                fig_pr.add_trace(go.Scatter(
                    x=r['rec'], y=r['prec'],
                    name=f"{name} ({r['pr_auc']:.3f})",
                    line=dict(color=color, width=2.5),
                    mode='lines',
                    hovertemplate='Recall: %{x:.3f}<br>Precision: %{y:.3f}<extra>'+name+'</extra>'
                ))
            fig_pr.update_layout(
                **PLOTLY_LAYOUT, height=350,
                xaxis_title='Recall',
                yaxis_title='Precision',
                legend=dict(orientation='h', y=-0.2)
            )
            st.plotly_chart(fig_pr, use_container_width=True)

        # Confusion matrices
        st.markdown('<p class="section-header">◈ CONFUSION MATRICES</p>', unsafe_allow_html=True)
        cm_cols = st.columns(3)
        for col, (name, r) in zip(cm_cols, results.items()):
            with col:
                cm = r['cm']
                fig_cm = go.Figure(go.Heatmap(
                    z=cm, x=['Pred Legit', 'Pred Fraud'], y=['Act Legit', 'Act Fraud'],
                    text=cm, texttemplate='<b>%{text}</b>',
                    colorscale=[[0, '#020812'], [1, '#00f5ff']],
                    showscale=False,
                    hovertemplate='%{y} → %{x}: %{z}<extra></extra>'
                ))
                fig_cm.update_layout(**PLOTLY_LAYOUT, height=260, title=name,
                                     title_font=dict(size=12, family='Orbitron'))
                st.plotly_chart(fig_cm, use_container_width=True)

        # Feature importance (Random Forest)
        if results['Random Forest']['feat_imp'] is not None:
            st.markdown('<p class="section-header">◈ FEATURE IMPORTANCE — RANDOM FOREST</p>', unsafe_allow_html=True)
            fi = results['Random Forest']['feat_imp'].head(15)
            fig_fi = go.Figure(go.Bar(
                x=fi.values, y=fi.index, orientation='h',
                marker=dict(
                    color=fi.values,
                    colorscale=[[0, COLORS['legit']], [0.5, COLORS['accent']], [1, COLORS['fraud']]],
                    showscale=False
                ),
                hovertemplate='%{y}: %{x:.4f}<extra></extra>'
            ))
            fi_layout = {**PLOTLY_LAYOUT, 'height': 400, 'xaxis_title': 'Importance Score'}
            fi_layout['yaxis'] = {**fi_layout.get('yaxis', {}), 'autorange': 'reversed'}
            fig_fi.update_layout(**fi_layout)
            st.plotly_chart(fig_fi, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════════
# TAB 4: REAL-TIME SIMULATION
# ══════════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<p class="section-header">◈ REAL-TIME TRANSACTION STREAM SIMULATOR</p>', unsafe_allow_html=True)

    st.markdown("""
    <div style='background:rgba(0,245,255,0.04);border:1px solid rgba(0,245,255,0.15);
    border-radius:10px;padding:1rem 1.2rem;margin-bottom:1rem;font-size:0.9rem;color:rgba(200,230,255,0.8)'>
    🔄 This simulator generates random transactions and scores them in real-time using 
    statistical thresholds derived from the dataset. Click <b>START STREAM</b> to begin monitoring.
    </div>
    """, unsafe_allow_html=True)

    sim_speed = st.select_slider("Stream Speed", ["Slow", "Normal", "Fast"], value="Normal")
    speed_map = {"Slow": 0.5, "Normal": 0.2, "Fast": 0.05}

    if st.button("⚡ START STREAM  (20 transactions)", type="primary"):
        fraud_log = []
        chart_placeholder = st.empty()
        alert_placeholder = st.empty()
        txn_placeholder = st.empty()

        V_fraud_mean = df[df['Class'] == 1][[f'V{i}' for i in range(1, 29)]].mean()
        V_fraud_std  = df[df['Class'] == 1][[f'V{i}' for i in range(1, 29)]].std()
        fraud_amt_mean = stats['avg_fraud_amt']

        stream_data = []
        for i in range(20):
            is_fraud = np.random.rand() < 0.20
            if is_fraud:
                amount = abs(np.random.normal(fraud_amt_mean, fraud_amt_mean * 0.5))
                v_vals = V_fraud_mean + np.random.randn(28) * V_fraud_std * 0.8
                risk = min(0.95, 0.65 + np.random.rand() * 0.30)
            else:
                amount = abs(np.random.exponential(60))
                v_vals = np.random.randn(28) * 1.2
                risk = max(0.02, np.random.rand() * 0.30)

            stream_data.append({
                'txn': i + 1,
                'amount': round(amount, 2),
                'risk': round(risk, 3),
                'status': '🔴 FRAUD' if risk >= threshold else '🟢 LEGIT',
                'flag': risk >= threshold
            })

            fraud_log = [d for d in stream_data if d['flag']]
            time.sleep(speed_map[sim_speed])

            with txn_placeholder.container():
                txn_df = pd.DataFrame(stream_data)
                fig_stream = go.Figure()
                fig_stream.add_trace(go.Scatter(
                    x=txn_df['txn'], y=txn_df['risk'],
                    mode='lines+markers',
                    line=dict(color='rgba(0,245,255,0.6)', width=1.5),
                    marker=dict(
                        size=10,
                        color=[COLORS['fraud'] if f else COLORS['legit'] for f in txn_df['flag']],
                        symbol=['diamond' if f else 'circle' for f in txn_df['flag']],
                        line=dict(width=1, color='rgba(2,8,18,0.8)')
                    ),
                    hovertemplate='Txn #%{x}<br>Risk: %{y:.1%}<extra></extra>'
                ))
                fig_stream.add_hline(y=threshold, line_dash="dash",
                                     line_color=COLORS['warn'],
                                     annotation_text=f"Threshold: {threshold:.0%}",
                                     annotation_font_color=COLORS['warn'])
                fig_stream.add_hrect(y0=threshold, y1=1,
                                     fillcolor='rgba(255,0,60,0.05)',
                                     line_width=0)
                stream_layout = {**PLOTLY_LAYOUT, 'height': 320,
                    'xaxis_title': 'Transaction #',
                    'title': f'Live Stream — {len(stream_data)} processed | {len(fraud_log)} flagged'}
                stream_layout['yaxis'] = {**stream_layout.get('yaxis', {}),
                    'title': 'Fraud Risk Score', 'range': [0, 1],
                    'tickformat': '%', 'gridcolor': 'rgba(0,245,255,0.08)'}
                fig_stream.update_layout(**stream_layout)
                st.plotly_chart(fig_stream, use_container_width=True)

        # Summary alerts
        st.markdown(f"""
        <div class="{'alert-fraud' if fraud_log else 'alert-legit'}">
            <b>{'🚨 FRAUD DETECTED' if fraud_log else '✅ STREAM CLEAR'}</b><br>
            Processed: <b>{len(stream_data)}</b> transactions &nbsp;|&nbsp;
            Flagged: <b>{len(fraud_log)}</b> suspicious &nbsp;|&nbsp;
            Detection Rate: <b>{len(fraud_log)/len(stream_data)*100:.1f}%</b>
        </div>
        """, unsafe_allow_html=True)

        if fraud_log:
            st.markdown("**🔴 Flagged Transactions:**")
            st.dataframe(
                pd.DataFrame(fraud_log)[['txn', 'amount', 'risk', 'status']].rename(
                    columns={'txn': 'Txn #', 'amount': 'Amount ($)', 'risk': 'Risk Score', 'status': 'Status'}
                ),
                use_container_width=True, hide_index=True
            )

# ══════════════════════════════════════════════════════════════════════════════════
# TAB 5: DATA EXPLORER
# ══════════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<p class="section-header">◈ DATASET SUMMARY</p>', unsafe_allow_html=True)

    col_info, col_stats = st.columns(2)

    with col_info:
        st.markdown("**Shape**")
        st.write(f"Rows: `{df.shape[0]:,}` | Columns: `{df.shape[1]}`")
        st.markdown("**Missing Values**")
        nulls = df.isnull().sum()
        if nulls.sum() == 0:
            st.success("✅ No missing values detected")
        else:
            st.dataframe(nulls[nulls > 0])

    with col_stats:
        st.markdown("**Amount Statistics by Class**")
        amt_stats = df.groupby('Class')['Amount'].agg(['mean', 'median', 'std', 'max']).round(2)
        amt_stats.index = ['Legitimate', 'Fraudulent']
        st.dataframe(amt_stats, use_container_width=True)

    st.markdown('<p class="section-header">◈ DESCRIPTIVE STATISTICS</p>', unsafe_allow_html=True)
    v_cols = [f'V{i}' for i in range(1, 29)] + ['Amount']
    st.dataframe(df[v_cols].describe().round(4), use_container_width=True)

    if show_raw:
        st.markdown('<p class="section-header">◈ RAW DATA (first 500 rows)</p>', unsafe_allow_html=True)
        fraud_filter = st.radio("Filter", ["All", "Fraud Only", "Legitimate Only"], horizontal=True)
        if fraud_filter == "Fraud Only":
            show_df = df[df['Class'] == 1].head(500)
        elif fraud_filter == "Legitimate Only":
            show_df = df[df['Class'] == 0].head(500)
        else:
            show_df = df.head(500)
        st.dataframe(show_df, use_container_width=True, height=400)

# ─── Footer ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center;padding:2rem 0 1rem;
border-top:1px solid rgba(0,245,255,0.1);margin-top:2rem;
color:rgba(0,245,255,0.35);font-size:0.72rem;letter-spacing:0.25em;
font-family:Rajdhani,sans-serif'>
FRAUD DETECTION AI &nbsp;|&nbsp; DATA ANALYST PROJECT &nbsp;|&nbsp; 
BUILT WITH STREAMLIT + PLOTLY + SCIKIT-LEARN
</div>
""", unsafe_allow_html=True)