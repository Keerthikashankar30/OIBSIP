import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pickle
import streamlit.components.v1 as components
from io import BytesIO
import warnings
warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split, cross_val_score, learning_curve
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score, f1_score, confusion_matrix,
    classification_report, roc_auc_score, precision_score, recall_score
)
from sklearn.decomposition import PCA
from sklearn.inspection import permutation_importance

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Wine Quality AI System",
    page_icon="🍷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root palette ── */
:root {
    --wine:       #7f1d1d;
    --wine-mid:   #991b1b;
    --wine-light: #fef2f2;
    --gold:       #b45309;
    --gold-light: #fef3c7;
    --green:      #166534;
    --surface:    #fff8f6;
    --border:     rgba(127,29,29,0.15);
    --text:       #1c1917;
    --muted:      #78716c;
}

/* ── Base ── */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--surface) !important;
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
}
[data-testid="stSidebar"] {
    background: #1c0a0a !important;
    border-right: 1px solid rgba(255,255,255,0.06);
}
[data-testid="stSidebar"] * { color: #f5e6e6 !important; }
[data-testid="stSidebar"] .stRadio label { 
    font-family: 'DM Sans', sans-serif; 
    font-size: 0.9rem;
    padding: 6px 0;
}

/* ── Hero header ── */
.hero {
    background: linear-gradient(135deg, #7f1d1d 0%, #450a0a 60%, #1c0a0a 100%);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute; inset: 0;
    background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Ccircle cx='30' cy='30' r='20'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    pointer-events: none;
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    font-weight: 900;
    color: #fff;
    margin: 0 0 0.4rem;
    line-height: 1.1;
}
.hero .tagline {
    font-size: 0.9rem;
    color: rgba(255,255,255,0.55);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    font-weight: 500;
}

/* ── KPI cards ── */
.kpi-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; }
.kpi {
    flex: 1;
    background: #fff;
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    display: flex; flex-direction: column; gap: 0.3rem;
    box-shadow: 0 2px 12px rgba(127,29,29,0.06);
}
.kpi .kpi-label { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--muted); font-weight: 600; }
.kpi .kpi-value { font-family: 'Playfair Display', serif; font-size: 2rem; font-weight: 700; color: var(--wine); line-height: 1; }
.kpi .kpi-sub   { font-size: 0.75rem; color: var(--muted); }

/* ── Section headers ── */
.section-head {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--wine);
    border-left: 4px solid var(--wine);
    padding-left: 0.8rem;
    margin: 1.8rem 0 1rem;
}

/* ── Glass card ── */
.glass {
    background: rgba(127,29,29,0.05);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.6rem 2rem;
    margin: 1rem 0;
}

/* ── Prediction result card ── */
.pred-card {
    background: linear-gradient(135deg, #fff8f6, #fff);
    border: 2px solid var(--wine);
    border-radius: 20px;
    padding: 2rem 2.5rem;
    text-align: center;
    box-shadow: 0 8px 32px rgba(127,29,29,0.12);
}
.pred-card .score { 
    font-family: 'Playfair Display', serif; 
    font-size: 5rem; font-weight: 900; 
    color: var(--wine); line-height: 1;
}
.pred-card .category { font-size: 1.1rem; font-weight: 600; color: var(--muted); margin-top: 0.3rem; }

/* ── Tip cards ── */
.tip {
    background: #f0fdf4;
    border-left: 4px solid #16a34a;
    border-radius: 8px;
    padding: 0.75rem 1.1rem;
    margin: 0.5rem 0;
    font-size: 0.9rem;
    color: #14532d;
}
.tip.warn {
    background: #fffbeb; border-left-color: #d97706; color: #78350f;
}
.tip.danger {
    background: #fef2f2; border-left-color: #dc2626; color: #7f1d1d;
}

/* ── Radar chart wrapper ── */
.radar-wrap { background: #fff; border-radius: 16px; border: 1px solid var(--border); padding: 1rem; }

/* ── Plotly overrides ── */
.js-plotly-plot .plotly .modebar { display: none !important; }

/* ── Stmetric override ── */
[data-testid="metric-container"] {
    background: #fff;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.8rem 1rem;
    box-shadow: 0 2px 8px rgba(127,29,29,0.05);
}

/* ── Table styling ── */
thead tr th { background: var(--wine) !important; color: #fff !important; font-family: 'DM Sans', sans-serif; }

/* ── Sidebar logo strip ── */
.sidebar-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    color: #fff;
    text-align: center;
    padding: 1.2rem 0 1.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 1rem;
    letter-spacing: 0.05em;
}
</style>
""", unsafe_allow_html=True)


# ── Data loading ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("WineQT.csv")
    if "Id" in df.columns:
        df = df.drop(columns=["Id"])
    return df

df = load_data()
X = df.drop("quality", axis=1)
y = df["quality"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)


# ── Model training ─────────────────────────────────────────────────────────────
@st.cache_resource
def get_trained_models():
    models = {
        "Random Forest":       RandomForestClassifier(n_estimators=200, random_state=42),
        "Gradient Boosting":   GradientBoostingClassifier(n_estimators=150, random_state=42),
        "SGD Classifier":      SGDClassifier(max_iter=1000, tol=1e-3, random_state=42),
        "SVC":                 SVC(probability=True, random_state=42),
        "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=7),
    }
    for name, m in models.items():
        if name in ("Random Forest", "Gradient Boosting"):
            m.fit(X_train, y_train)
        else:
            m.fit(X_train_scaled, y_train)
    return models

models = get_trained_models()


# ── Helpers ────────────────────────────────────────────────────────────────────
def categorize(q):
    if q <= 4:  return "Low Quality",   "#dc2626"
    if q <= 6:  return "Medium Quality","#d97706"
    return "High Quality", "#16a34a"

def predict(model_name, arr):
    m = models[model_name]
    if model_name in ("Random Forest", "Gradient Boosting"):
        return m.predict(arr)[0], m.predict_proba(arr)[0]
    scaled = scaler.transform(arr)
    pred = m.predict(scaled)[0]
    prob = m.predict_proba(scaled)[0] if hasattr(m, "predict_proba") else None
    return pred, prob

def wine_tips(features, prediction):
    tips = []
    label, _ = categorize(prediction)
    if features["volatile acidity"] > 0.6:
        tips.append(("danger", "⚠️ Volatile acidity is high (>0.6). Reduce it to improve taste stability and avoid vinegar notes."))
    if features["alcohol"] < 10:
        tips.append(("warn",   "🍶 Alcohol content is low (<10%). A slight increase can add richness and body."))
    if features["sulphates"] < 0.5:
        tips.append(("warn",   "🧪 Sulphates are below 0.5 g/dm³. Raising them slightly boosts preservation and aroma."))
    if features["density"] > 1.0:
        tips.append(("warn",   "⚖️ High density (>1.0) may indicate excess residual sugar — can affect smoothness."))
    if features["citric acid"] < 0.1:
        tips.append(("warn",   "🍋 Citric acid is very low. Increasing it adds freshness and complexity."))
    if features["pH"] > 3.6:
        tips.append(("warn",   "🔬 pH is on the high side. Lower pH wines are generally more stable and age better."))
    if features["residual sugar"] > 8:
        tips.append(("warn",   "🍬 High residual sugar (>8 g/dm³). Consider balance with acidity."))
    if not tips:
        tips.append(("tip",    "✅ Chemical profile looks well-balanced. Keep up the excellent work!"))
    if prediction <= 4:
        tips.append(("danger", "🔴 Quality score is critically low. Major formulation changes are recommended."))
    elif prediction <= 6:
        tips.append(("warn",   "🟡 Decent baseline — targeted adjustments should push quality into the High tier."))
    else:
        tips.append(("tip",    "🟢 Outstanding profile! Maintain current parameters for consistent excellence."))
    return tips

def radar_chart(feature_vals, col_names, title="Chemical Profile"):
    """Matplotlib polar radar chart."""
    vals = list(feature_vals) + [feature_vals[0]]
    angles = np.linspace(0, 2*np.pi, len(col_names), endpoint=False).tolist()
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor('none')
    ax.set_facecolor('#fff8f6')
    ax.plot(angles, vals, color='#7f1d1d', linewidth=2.5)
    ax.fill(angles, vals, color='#7f1d1d', alpha=0.18)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(col_names, fontsize=7.5, color='#44403c')
    ax.set_yticklabels([])
    ax.grid(color='#d6d3d1', linestyle='--', linewidth=0.7)
    ax.spines['polar'].set_color('#d6d3d1')
    ax.set_title(title, fontsize=12, color='#7f1d1d',
                 fontfamily='serif', pad=18, fontweight='bold')
    return fig

def quality_gauge(pred):
    if pred <= 4:   target, color, level = 13, "#ef4444", "LOW QUALITY"
    elif pred <= 6: target, color, level = 50, "#f59e0b", "MEDIUM QUALITY"
    else:           target, color, level = 88, "#22c55e", "HIGH QUALITY"
    components.html(f"""
    <style>
    body{{margin:0;background:transparent;font-family:'DM Sans',Arial,sans-serif}}
    .wrap{{width:88%;margin:0 auto;padding-top:10px}}
    .labels{{display:flex;justify-content:space-between;font-size:11px;color:#78716c;margin-bottom:4px}}
    .track{{position:relative;height:22px;border-radius:30px;overflow:hidden;
            background:linear-gradient(to right,#ef4444 0%,#ef4444 33%,#f59e0b 33%,#f59e0b 66%,#22c55e 66%,#22c55e 100%);
            box-shadow:inset 0 2px 6px rgba(0,0,0,0.18)}}
    .thumb{{position:absolute;top:-14px;width:50px;height:50px;border-radius:50%;
            background:{color};box-shadow:0 0 18px {color},0 0 40px {color}55;
            transform:translateX(-50%);transition:left 0.05s linear;border:3px solid #fff}}
    .result{{text-align:center;margin-top:22px;font-size:22px;font-weight:700;
             color:{color};letter-spacing:0.08em;text-transform:uppercase}}
    .score-badge{{text-align:center;font-size:13px;color:#78716c;margin-top:4px}}
    </style>
    <div class="wrap">
      <div class="labels"><span>Low</span><span>Medium</span><span>High</span></div>
      <div class="track"><div class="thumb" id="th"></div></div>
      <div class="result">{level}</div>
      <div class="score-badge">Quality Score: {pred} / 10</div>
    </div>
    <script>
    var c=0,t={target};
    var th=document.getElementById('th');
    var iv=setInterval(function(){{
        c=Math.min(c+1,t);
        th.style.left=c+'%';
        if(c>=t)clearInterval(iv);
    }},18);
    </script>""", height=145)

def confusion_heatmap(model_name):
    m = models[model_name]
    if model_name in ("Random Forest","Gradient Boosting"):
        pred = m.predict(X_test)
    else:
        pred = m.predict(X_test_scaled)
    cm = confusion_matrix(y_test, pred)
    labels = sorted(y_test.unique())
    fig, ax = plt.subplots(figsize=(6, 4.5))
    fig.patch.set_facecolor('none')
    sns.heatmap(cm, annot=True, fmt='d', cmap='Reds',
                xticklabels=labels, yticklabels=labels, ax=ax,
                linewidths=0.5, linecolor='#f5f5f4',
                cbar_kws={"shrink": 0.75})
    ax.set_xlabel("Predicted", fontsize=10, color='#44403c')
    ax.set_ylabel("Actual",    fontsize=10, color='#44403c')
    ax.set_title(f"Confusion Matrix — {model_name}", fontsize=11,
                 color='#7f1d1d', fontweight='bold')
    ax.tick_params(colors='#44403c')
    plt.tight_layout()
    return fig

def learning_curve_plot(model_name):
    m = models[model_name]
    estimator = RandomForestClassifier(n_estimators=50, random_state=42) \
                if model_name in ("Random Forest","Gradient Boosting") else \
                SGDClassifier(max_iter=500, tol=1e-3, random_state=42)
    Xd = X_train if model_name in ("Random Forest","Gradient Boosting") else X_train_scaled
    sizes, tr_scores, cv_scores = learning_curve(
        estimator, Xd, y_train,
        cv=5, n_jobs=-1,
        train_sizes=np.linspace(0.1, 1.0, 8),
        scoring='accuracy')
    tr_mean = tr_scores.mean(axis=1)
    cv_mean = cv_scores.mean(axis=1)
    tr_std  = tr_scores.std(axis=1)
    cv_std  = cv_scores.std(axis=1)
    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_facecolor('none')
    ax.fill_between(sizes, tr_mean-tr_std, tr_mean+tr_std, alpha=0.15, color='#7f1d1d')
    ax.fill_between(sizes, cv_mean-cv_std, cv_mean+cv_std, alpha=0.15, color='#b45309')
    ax.plot(sizes, tr_mean, 'o-', color='#7f1d1d', label='Training score',  linewidth=2)
    ax.plot(sizes, cv_mean, 's-', color='#b45309', label='CV score',        linewidth=2)
    ax.set_xlabel("Training samples", fontsize=10, color='#44403c')
    ax.set_ylabel("Accuracy",          fontsize=10, color='#44403c')
    ax.set_title("Learning Curve",     fontsize=11, color='#7f1d1d', fontweight='bold')
    ax.legend(fontsize=9)
    ax.set_facecolor('#fff8f6')
    ax.tick_params(colors='#44403c')
    for spine in ax.spines.values(): spine.set_color('#e7e5e4')
    plt.tight_layout()
    return fig

def pca_scatter():
    pca = PCA(n_components=2)
    Xp = pca.fit_transform(X_train_scaled)
    ev = pca.explained_variance_ratio_
    fig, ax = plt.subplots(figsize=(7, 5))
    fig.patch.set_facecolor('none')
    ax.set_facecolor('#fff8f6')
    classes = sorted(y_train.unique())
    cmap = plt.cm.get_cmap('RdYlGn', len(classes))
    for i, cls in enumerate(classes):
        mask = y_train == cls
        ax.scatter(Xp[mask, 0], Xp[mask, 1], s=18, alpha=0.65,
                   color=cmap(i), label=f"Q={cls}", edgecolors='none')
    ax.set_xlabel(f"PC1 ({ev[0]*100:.1f}% var)", fontsize=9, color='#44403c')
    ax.set_ylabel(f"PC2 ({ev[1]*100:.1f}% var)", fontsize=9, color='#44403c')
    ax.set_title("PCA — 2D Wine Space", fontsize=11, color='#7f1d1d', fontweight='bold')
    ax.legend(fontsize=8, ncol=2, framealpha=0.7)
    for spine in ax.spines.values(): spine.set_color('#e7e5e4')
    ax.tick_params(colors='#78716c', labelsize=8)
    plt.tight_layout()
    return fig

def distribution_grid():
    feat = X.columns.tolist()
    cols = 3
    rows = (len(feat) + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(13, rows * 2.8))
    fig.patch.set_facecolor('none')
    axes = axes.flatten()
    palette = {q: plt.cm.RdYlGn((q-3)/5) for q in sorted(df["quality"].unique())}
    for i, f in enumerate(feat):
        ax = axes[i]
        ax.set_facecolor('#fff8f6')
        for q, grp in df.groupby("quality"):
            ax.hist(grp[f], bins=18, alpha=0.55, color=palette[q], label=f"Q{q}", edgecolor='none')
        ax.set_title(f, fontsize=9, color='#44403c', fontweight='600')
        ax.tick_params(labelsize=7, colors='#78716c')
        for spine in ax.spines.values(): spine.set_color('#e7e5e4')
    for j in range(i+1, len(axes)): axes[j].set_visible(False)
    handles = [mpatches.Patch(color=c, label=f"Q{q}") for q, c in palette.items()]
    fig.legend(handles=handles, loc='lower right', fontsize=8, ncol=len(palette),
               framealpha=0.8, title="Quality", title_fontsize=8)
    plt.suptitle("Feature Distributions by Quality Score", y=1.01,
                 fontsize=13, color='#7f1d1d', fontweight='bold', fontfamily='serif')
    plt.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════
st.sidebar.markdown("<div class='sidebar-logo'>🍷 WineAI</div>", unsafe_allow_html=True)
menu = st.sidebar.radio(
    "Navigate",
    ["🏠 Dashboard",
     "📊 Deep EDA",
     "🤖 Model Arena",
     "🔮 Prediction Lab",
     "🍷 Wine Advisor",
     "📈 Feature Intelligence",
     "🔬 Advanced Analytics"],
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<div style='font-size:0.75rem;color:#a8a29e;padding:0.5rem 0'>Dataset: WineQT.csv<br>"
    "Models: 5 ML classifiers<br>Framework: Streamlit + scikit-learn</div>",
    unsafe_allow_html=True
)


# ═══════════════════════════════════════════════════════════════
#  HERO HEADER (every page)
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <h1>🍷 Wine Quality AI System</h1>
  <div class="tagline">Machine Learning &nbsp;•&nbsp; Explainable Insights &nbsp;•&nbsp; Wine Intelligence</div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  PAGE 1 — DASHBOARD
# ═══════════════════════════════════════════════════════════════
if menu == "🏠 Dashboard":
    # KPI row
    avg_q   = df["quality"].mean()
    top_pct = (df["quality"] >= 7).mean() * 100
    low_pct = (df["quality"] <= 4).mean() * 100
    best_alc = df.loc[df["quality"]==df["quality"].max(), "alcohol"].mean()

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("📋 Total Samples",    f"{df.shape[0]:,}")
    col2.metric("🧪 Features",         df.shape[1] - 1)
    col3.metric("⭐ Avg Quality",       f"{avg_q:.2f}")
    col4.metric("🏆 High Quality %",   f"{top_pct:.1f}%")
    col5.metric("⚠️ Low Quality %",    f"{low_pct:.1f}%")

    st.markdown("<div class='section-head'>Quality Distribution</div>", unsafe_allow_html=True)
    c1, c2 = st.columns([1.4, 1])

    with c1:
        fig, ax = plt.subplots(figsize=(8, 3.8))
        fig.patch.set_facecolor('none')
        ax.set_facecolor('#fff8f6')
        counts = df["quality"].value_counts().sort_index()
        colors_bar = ['#ef4444' if q<=4 else '#f59e0b' if q<=6 else '#22c55e'
                      for q in counts.index]
        bars = ax.bar(counts.index, counts.values, color=colors_bar,
                      width=0.6, edgecolor='white', linewidth=1.5)
        for bar, val in zip(bars, counts.values):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+8,
                    str(val), ha='center', va='bottom', fontsize=9, color='#44403c', fontweight='600')
        ax.set_xlabel("Quality Score", fontsize=10, color='#44403c')
        ax.set_ylabel("Count",         fontsize=10, color='#44403c')
        ax.set_title("Wine Count by Quality Score", fontsize=11, color='#7f1d1d', fontweight='bold')
        ax.tick_params(colors='#78716c')
        for spine in ax.spines.values(): spine.set_color('#e7e5e4')
        plt.tight_layout()
        st.pyplot(fig)

    with c2:
        fig2, ax2 = plt.subplots(figsize=(4.5, 4.5))
        fig2.patch.set_facecolor('none')
        tier_map = {"Low (≤4)": (df["quality"]<=4).sum(),
                    "Medium (5–6)": ((df["quality"]>=5)&(df["quality"]<=6)).sum(),
                    "High (≥7)": (df["quality"]>=7).sum()}
        wedge_colors = ['#ef4444','#f59e0b','#22c55e']
        wedges, texts, autotexts = ax2.pie(
            tier_map.values(), labels=tier_map.keys(),
            autopct='%1.1f%%', colors=wedge_colors,
            startangle=140, pctdistance=0.78,
            wedgeprops=dict(edgecolor='white', linewidth=2.5))
        for t in texts: t.set_color('#44403c'); t.set_fontsize(9)
        for at in autotexts: at.set_fontsize(8); at.set_color('#fff'); at.set_fontweight('bold')
        ax2.set_title("Quality Tier Breakdown", fontsize=11, color='#7f1d1d', fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig2)

    st.markdown("<div class='section-head'>Correlation Heatmap</div>", unsafe_allow_html=True)
    fig3, ax3 = plt.subplots(figsize=(11, 6))
    fig3.patch.set_facecolor('none')
    corr = df.corr(numeric_only=True)
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='RdYlGn',
                center=0, vmin=-1, vmax=1, ax=ax3,
                linewidths=0.5, linecolor='#f5f5f4',
                annot_kws={"size": 8},
                cbar_kws={"shrink": 0.8})
    ax3.set_title("Feature Correlation Matrix (lower triangle)", fontsize=12,
                  color='#7f1d1d', fontweight='bold')
    ax3.tick_params(colors='#44403c', labelsize=8)
    plt.tight_layout()
    st.pyplot(fig3)


# ═══════════════════════════════════════════════════════════════
#  PAGE 2 — DEEP EDA
# ═══════════════════════════════════════════════════════════════
elif menu == "📊 Deep EDA":
    st.markdown("<div class='section-head'>Dataset Preview</div>", unsafe_allow_html=True)
    st.dataframe(df.head(10), use_container_width=True)

    st.markdown("<div class='section-head'>Descriptive Statistics</div>", unsafe_allow_html=True)
    st.dataframe(df.describe().T.style.background_gradient(cmap='RdYlGn', axis=1),
                 use_container_width=True)

    st.markdown("<div class='section-head'>Feature Distributions by Quality</div>", unsafe_allow_html=True)
    st.pyplot(distribution_grid())

    st.markdown("<div class='section-head'>Box Plots — Feature vs Quality</div>", unsafe_allow_html=True)
    feat_sel = st.selectbox("Choose feature", X.columns.tolist(), index=10)
    fig, ax = plt.subplots(figsize=(9, 4))
    fig.patch.set_facecolor('none')
    ax.set_facecolor('#fff8f6')
    sns.boxplot(data=df, x="quality", y=feat_sel, palette="RdYlGn", ax=ax,
                linewidth=1.5, flierprops=dict(marker='o', markersize=3, alpha=0.5))
    ax.set_title(f"{feat_sel} by Quality Score", fontsize=11, color='#7f1d1d', fontweight='bold')
    ax.tick_params(colors='#44403c')
    for spine in ax.spines.values(): spine.set_color('#e7e5e4')
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("<div class='section-head'>Scatter — Any Two Features</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    fx = c1.selectbox("X-axis", X.columns.tolist(), index=10)
    fy = c2.selectbox("Y-axis", X.columns.tolist(), index=1)
    fig2, ax2 = plt.subplots(figsize=(8, 4.5))
    fig2.patch.set_facecolor('none')
    ax2.set_facecolor('#fff8f6')
    scatter = ax2.scatter(df[fx], df[fy], c=df["quality"],
                          cmap='RdYlGn', s=18, alpha=0.7, edgecolors='none')
    plt.colorbar(scatter, ax=ax2, label='Quality')
    ax2.set_xlabel(fx, fontsize=10, color='#44403c')
    ax2.set_ylabel(fy, fontsize=10, color='#44403c')
    ax2.set_title(f"{fx}  vs  {fy}  (coloured by Quality)", fontsize=11,
                  color='#7f1d1d', fontweight='bold')
    ax2.tick_params(colors='#78716c')
    for sp in ax2.spines.values(): sp.set_color('#e7e5e4')
    plt.tight_layout()
    st.pyplot(fig2)


# ═══════════════════════════════════════════════════════════════
#  PAGE 3 — MODEL ARENA
# ═══════════════════════════════════════════════════════════════
elif menu == "🤖 Model Arena":
    st.markdown("<div class='section-head'>All-Model Performance Comparison</div>", unsafe_allow_html=True)

    results = []
    for name, m in models.items():
        pred = m.predict(X_test if name in ("Random Forest","Gradient Boosting") else X_test_scaled)
        acc  = accuracy_score(y_test, pred)
        f1   = f1_score(y_test, pred, average="weighted")
        prec = precision_score(y_test, pred, average="weighted", zero_division=0)
        rec  = recall_score(y_test, pred, average="weighted", zero_division=0)
        results.append({"Model": name, "Accuracy": round(acc,4),
                         "F1 Score": round(f1,4),
                         "Precision": round(prec,4),
                         "Recall": round(rec,4)})

    res_df = pd.DataFrame(results).sort_values("Accuracy", ascending=False).reset_index(drop=True)
    st.dataframe(res_df.style.background_gradient(subset=["Accuracy","F1 Score","Precision","Recall"],
                                                   cmap="RdYlGn"),
                 use_container_width=True)

    best = res_df.iloc[0]["Model"]
    st.success(f"🏆 Best Model: **{best}** — Accuracy {res_df.iloc[0]['Accuracy']*100:.2f}%")

    c1, c2 = st.columns(2)
    with c1:
        fig, ax = plt.subplots(figsize=(6, 3.8))
        fig.patch.set_facecolor('none')
        ax.set_facecolor('#fff8f6')
        colors = ['#7f1d1d' if m==best else '#d6d3d1' for m in res_df["Model"]]
        bars = ax.barh(res_df["Model"], res_df["Accuracy"], color=colors,
                       edgecolor='white', height=0.55)
        for bar, val in zip(bars, res_df["Accuracy"]):
            ax.text(val+0.003, bar.get_y()+bar.get_height()/2,
                    f"{val*100:.1f}%", va='center', fontsize=9, color='#44403c', fontweight='600')
        ax.set_xlim(0, res_df["Accuracy"].max() * 1.12)
        ax.set_xlabel("Accuracy", fontsize=10, color='#44403c')
        ax.set_title("Model Accuracy Comparison", fontsize=11, color='#7f1d1d', fontweight='bold')
        ax.tick_params(colors='#44403c')
        for sp in ax.spines.values(): sp.set_color('#e7e5e4')
        plt.tight_layout()
        st.pyplot(fig)

    with c2:
        model_cm = st.selectbox("Confusion Matrix for:", list(models.keys()))
        st.pyplot(confusion_heatmap(model_cm))

    st.markdown("<div class='section-head'>Learning Curve</div>", unsafe_allow_html=True)
    lc_model = st.selectbox("Learning curve for:", list(models.keys()), key="lc")
    st.pyplot(learning_curve_plot(lc_model))

    st.markdown("<div class='section-head'>Full Classification Report</div>", unsafe_allow_html=True)
    cr_model = st.selectbox("Report for:", list(models.keys()), key="cr")
    m = models[cr_model]
    pred = m.predict(X_test if cr_model in ("Random Forest","Gradient Boosting") else X_test_scaled)
    report_str = classification_report(y_test, pred, output_dict=True)
    st.dataframe(pd.DataFrame(report_str).T.style.background_gradient(cmap="RdYlGn", subset=["precision","recall","f1-score"]),
                 use_container_width=True)


# ═══════════════════════════════════════════════════════════════
#  PAGE 4 — PREDICTION LAB
# ═══════════════════════════════════════════════════════════════
elif menu == "🔮 Prediction Lab":
    st.markdown("<div class='section-head'>Configure Wine Parameters</div>", unsafe_allow_html=True)

    model_choice = st.selectbox("🤖 Select Model", list(models.keys()))

    # 3-column sliders for a cleaner layout
    col_groups = [X.columns[i:i+4] for i in range(0, len(X.columns), 4)]
    values = []
    for group in col_groups:
        cols = st.columns(len(group))
        for col, feature in zip(cols, group):
            mn, mx, mean = float(X[feature].min()), float(X[feature].max()), float(X[feature].mean())
            v = col.slider(feature, min_value=round(mn,3), max_value=round(mx,3),
                           value=round(mean,3), step=round((mx-mn)/200, 4))
            values.append(v)

    if st.button("🔮 Run Prediction", type="primary"):
        arr = np.array(values).reshape(1, -1)
        pred_val, probas = predict(model_choice, arr)
        label, color = categorize(pred_val)

        c1, c2 = st.columns([1, 1.6])
        with c1:
            st.markdown(f"""
            <div class="pred-card">
              <div style="font-size:0.85rem;color:#78716c;margin-bottom:0.5rem;letter-spacing:0.1em;text-transform:uppercase">Quality Score</div>
              <div class="score">{pred_val}</div>
              <div class="category" style="color:{color}">{label}</div>
            </div>""", unsafe_allow_html=True)
            quality_gauge(pred_val)

        with c2:
            if probas is not None:
                classes = models[model_choice].classes_
                prob_df = pd.DataFrame({"Quality": classes, "Probability": probas}) \
                            .sort_values("Quality")
                fig, ax = plt.subplots(figsize=(6, 3.8))
                fig.patch.set_facecolor('none')
                ax.set_facecolor('#fff8f6')
                bar_colors = ['#ef4444' if q<=4 else '#f59e0b' if q<=6 else '#22c55e'
                              for q in prob_df["Quality"]]
                ax.bar(prob_df["Quality"].astype(str), prob_df["Probability"],
                       color=bar_colors, edgecolor='white', linewidth=1.5)
                ax.set_xlabel("Quality Score", fontsize=10, color='#44403c')
                ax.set_ylabel("Probability",   fontsize=10, color='#44403c')
                ax.set_title("Prediction Probability Distribution",
                             fontsize=11, color='#7f1d1d', fontweight='bold')
                ax.tick_params(colors='#44403c')
                for sp in ax.spines.values(): sp.set_color('#e7e5e4')
                plt.tight_layout()
                st.pyplot(fig)

        # Radar chart — normalise to 0-1
        norm_vals = [(v - float(X[f].min())) / max(float(X[f].max()-X[f].min()), 1e-6)
                     for v, f in zip(values, X.columns)]
        st.pyplot(radar_chart(norm_vals, X.columns.tolist(), "Normalised Chemical Profile"))

        # Download
        report = pd.DataFrame([values], columns=X.columns)
        report["Predicted Quality"] = pred_val
        report["Category"] = label
        st.download_button("📥 Download Prediction Report",
                           report.to_csv(index=False).encode(),
                           "wine_prediction.csv", "text/csv")


# ═══════════════════════════════════════════════════════════════
#  PAGE 5 — WINE ADVISOR
# ═══════════════════════════════════════════════════════════════
elif menu == "🍷 Wine Advisor":
    st.markdown("""
    <div class="glass">
      <b>How it works:</b> Enter your wine's chemical parameters below.
      The AI will predict quality and give you personalised improvement tips
      based on expert thresholds for each chemical property.
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='section-head'>Wine Parameters</div>", unsafe_allow_html=True)

    values = []
    col_groups = [X.columns[i:i+4] for i in range(0, len(X.columns), 4)]
    for group in col_groups:
        cols = st.columns(len(group))
        for col, feature in zip(cols, group):
            mn  = float(X[feature].min())
            mx  = float(X[feature].max())
            mean = float(X[feature].mean())
            v = col.number_input(feature, min_value=round(mn,3), max_value=round(mx,3),
                                 value=round(mean,3), step=round((mx-mn)/200,4), key=f"adv_{feature}")
            values.append(v)

    if st.button("🍷 Analyse My Wine", type="primary"):
        arr  = np.array(values).reshape(1, -1)
        pred_val, _ = predict("Random Forest", arr)
        label, color = categorize(pred_val)

        c1, c2 = st.columns([1, 1.8])
        with c1:
            st.markdown(f"""
            <div class="pred-card">
              <div style="font-size:0.8rem;color:#78716c;letter-spacing:0.1em;text-transform:uppercase">Predicted Quality</div>
              <div class="score">{pred_val}</div>
              <div class="category" style="color:{color}">{label}</div>
            </div>""", unsafe_allow_html=True)
            quality_gauge(pred_val)

        with c2:
            st.markdown("<div class='section-head'>🧑‍🔬 Expert Tips</div>", unsafe_allow_html=True)
            feature_dict = dict(zip(X.columns, values))
            for kind, tip in wine_tips(feature_dict, pred_val):
                st.markdown(f"<div class='tip {kind}'>{tip}</div>", unsafe_allow_html=True)

        # Radar
        norm_vals = [(v - float(X[f].min())) / max(float(X[f].max()-X[f].min()), 1e-6)
                     for v, f in zip(values, X.columns)]
        st.markdown("<div class='section-head'>Chemical Profile Radar</div>", unsafe_allow_html=True)
        st.pyplot(radar_chart(norm_vals, X.columns.tolist()))


# ═══════════════════════════════════════════════════════════════
#  PAGE 6 — FEATURE INTELLIGENCE
# ═══════════════════════════════════════════════════════════════
elif menu == "📈 Feature Intelligence":
    rf = models["Random Forest"]
    imp = pd.DataFrame({"Feature": X.columns,
                        "Importance": rf.feature_importances_}) \
            .sort_values("Importance", ascending=False).reset_index(drop=True)
    imp["Rank"] = range(1, len(imp)+1)

    st.markdown("<div class='section-head'>Random Forest Feature Importance</div>", unsafe_allow_html=True)
    st.dataframe(imp[["Rank","Feature","Importance"]].style.background_gradient(
                     subset=["Importance"], cmap="RdYlGn"),
                 use_container_width=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor('none')
    ax.set_facecolor('#fff8f6')
    colors_imp = ['#7f1d1d' if i==0 else '#b45309' if i<=2 else '#d6d3d1' for i in range(len(imp))]
    bars = ax.barh(imp["Feature"], imp["Importance"], color=colors_imp,
                   edgecolor='white', height=0.65)
    for bar, val in zip(bars, imp["Importance"]):
        ax.text(val+0.002, bar.get_y()+bar.get_height()/2,
                f"{val*100:.2f}%", va='center', fontsize=8.5, color='#44403c', fontweight='600')
    ax.invert_yaxis()
    ax.set_xlabel("Importance", fontsize=10, color='#44403c')
    ax.set_title("Feature Importance — Random Forest", fontsize=11, color='#7f1d1d', fontweight='bold')
    ax.tick_params(colors='#44403c')
    for sp in ax.spines.values(): sp.set_color('#e7e5e4')
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("<div class='section-head'>Permutation Importance (Model-agnostic)</div>", unsafe_allow_html=True)
    perm_model = st.selectbox("Compute for:", list(models.keys()))
    with st.spinner("Calculating permutation importance…"):
        pm = models[perm_model]
        Xp_use = X_test if perm_model in ("Random Forest","Gradient Boosting") else X_test_scaled
        r = permutation_importance(pm, Xp_use, y_test, n_repeats=10, random_state=42, n_jobs=-1)
        perm_df = pd.DataFrame({"Feature": X.columns,
                                 "Mean Decrease": r.importances_mean,
                                 "Std": r.importances_std}) \
                    .sort_values("Mean Decrease", ascending=False).reset_index(drop=True)
    st.dataframe(perm_df.style.background_gradient(subset=["Mean Decrease"], cmap="RdYlGn"),
                 use_container_width=True)

    pickle.dump(rf, open("wine_model.pkl", "wb"))
    st.success("✅ Best model (Random Forest) saved as wine_model.pkl")
    with open("wine_model.pkl","rb") as f:
        st.download_button("📥 Download Model (.pkl)", f, "wine_model.pkl")


# ═══════════════════════════════════════════════════════════════
#  PAGE 7 — ADVANCED ANALYTICS
# ═══════════════════════════════════════════════════════════════
elif menu == "🔬 Advanced Analytics":
    st.markdown("<div class='section-head'>PCA — 2D Wine Landscape</div>", unsafe_allow_html=True)
    st.markdown("""<div class='glass'>Principal Component Analysis reduces all 11 chemical features
    into two dimensions, revealing how quality classes cluster in chemical space.</div>""",
    unsafe_allow_html=True)
    st.pyplot(pca_scatter())

    st.markdown("<div class='section-head'>Cross-Validation Scores (5-Fold)</div>", unsafe_allow_html=True)
    cv_results = []
    with st.spinner("Running 5-fold CV on all models…"):
        for name, m in models.items():
            Xcv = X if name in ("Random Forest","Gradient Boosting") else \
                  pd.DataFrame(scaler.transform(X), columns=X.columns)
            scores = cross_val_score(m, Xcv, y, cv=5, scoring='accuracy', n_jobs=-1)
            cv_results.append({"Model": name,
                                "CV Mean": round(scores.mean(), 4),
                                "CV Std":  round(scores.std(), 4),
                                "CV Min":  round(scores.min(), 4),
                                "CV Max":  round(scores.max(), 4)})
    cv_df = pd.DataFrame(cv_results).sort_values("CV Mean", ascending=False).reset_index(drop=True)
    st.dataframe(cv_df.style.background_gradient(subset=["CV Mean"], cmap="RdYlGn"),
                 use_container_width=True)

    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_facecolor('none')
    ax.set_facecolor('#fff8f6')
    x_pos = np.arange(len(cv_df))
    ax.bar(x_pos, cv_df["CV Mean"], yerr=cv_df["CV Std"],
           color=['#7f1d1d' if i==0 else '#d6d3d1' for i in range(len(cv_df))],
           capsize=6, edgecolor='white', width=0.55)
    ax.set_xticks(x_pos); ax.set_xticklabels(cv_df["Model"], rotation=15, ha='right', fontsize=9)
    ax.set_ylabel("CV Accuracy", fontsize=10, color='#44403c')
    ax.set_title("5-Fold Cross-Validation Accuracy", fontsize=11, color='#7f1d1d', fontweight='bold')
    ax.tick_params(colors='#44403c')
    for sp in ax.spines.values(): sp.set_color('#e7e5e4')
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("<div class='section-head'>Feature Correlation with Quality</div>", unsafe_allow_html=True)
    corr_q = df.corr(numeric_only=True)["quality"].drop("quality").sort_values()
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    fig2.patch.set_facecolor('none')
    ax2.set_facecolor('#fff8f6')
    colors_c = ['#ef4444' if v<0 else '#22c55e' for v in corr_q]
    ax2.barh(corr_q.index, corr_q.values, color=colors_c, edgecolor='white', height=0.6)
    ax2.axvline(0, color='#44403c', linewidth=1, linestyle='--')
    ax2.set_xlabel("Pearson Correlation with Quality", fontsize=10, color='#44403c')
    ax2.set_title("Feature → Quality Correlation", fontsize=11, color='#7f1d1d', fontweight='bold')
    ax2.tick_params(colors='#44403c')
    for sp in ax2.spines.values(): sp.set_color('#e7e5e4')
    plt.tight_layout()
    st.pyplot(fig2)

    st.markdown("<div class='section-head'>Outlier Detection — IQR Method</div>", unsafe_allow_html=True)
    outlier_counts = {}
    for col in X.columns:
        Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        IQR = Q3 - Q1
        outlier_counts[col] = ((df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)).sum()
    out_df = pd.DataFrame({"Feature": list(outlier_counts.keys()),
                            "Outliers": list(outlier_counts.values())}) \
               .sort_values("Outliers", ascending=False)
    st.dataframe(out_df.style.background_gradient(subset=["Outliers"], cmap="Reds"),
                 use_container_width=True)