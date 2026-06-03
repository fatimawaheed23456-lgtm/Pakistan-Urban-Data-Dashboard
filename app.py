import streamlit as st
import pandas as pd
from filters import load_data, apply_filters
from charts import (pie_chart, histogram, line_chart, bar_chart,
                    scatter_plot, box_plot, heatmap, area_chart,
                    count_plot, violin_plot)

# ── Page Configuration ─────────────────────────────────────
st.set_page_config(
    page_title="World Cities Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ─────────────────────────────────────────────
st.markdown("""
    <style>
    .main { background-color: #0f1117; }
    .block-container { padding-top: 1rem; }
    .kpi-card {
        background-color: #1e2130;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        border: 1px solid #4C72B0;
    }
    .kpi-value {
        font-size: 28px;
        font-weight: bold;
        color: #4C72B0;
    }
    .kpi-label {
        font-size: 13px;
        color: #aaaaaa;
        margin-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# ── Load Data ──────────────────────────────────────────────
df = load_data()

# ── Header ─────────────────────────────────────────────────
st.markdown("""
    <h1 style='text-align:center; color:#4C72B0;'>
        🌍 World Cities Data Dashboard
    </h1>
    <p style='text-align:center; color:#aaaaaa;'>
        Exploratory Data Analysis of 40,000+ World Cities
        | Population · Geography · Urban Insights
    </p>
    <hr style='border-color:#4C72B0;'>
""", unsafe_allow_html=True)

# ── Sidebar Filters ────────────────────────────────────────
st.sidebar.markdown("## 🔧 Dashboard Filters")
st.sidebar.markdown("---")

# 1. Search Filter
search_text = st.sidebar.text_input("🔍 Search City", value="")

# 2. Country Multi-Select Filter
all_countries = sorted(df["country"].dropna().unique().tolist())
selected_countries = st.sidebar.multiselect(
    "🌐 Select Countries",
    options=all_countries,
    default=[]
)

# 3. Capital Filter
all_capitals = sorted(df["capital"].dropna().unique().tolist())
selected_capitals = st.sidebar.multiselect(
    "🏛️ Capital Status",
    options=all_capitals,
    default=[]
)

# 4. Population Range Slider
min_pop = int(df["population"].min())
max_pop = int(df["population"].max())
pop_range = st.sidebar.slider(
    "👥 Population Range",
    min_value=min_pop,
    max_value=max_pop,
    value=(min_pop, max_pop),
    step=100000
)

# 5. Reset Filters Button
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Reset All Filters"):
    search_text = ""
    selected_countries = []
    selected_capitals = []
    pop_range = (min_pop, max_pop)
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<p style='color:#aaaaaa; font-size:12px;'>"
    "Dashboard by SAP ID: 70177415<br>"
    "Course: Exploratory Data Analysis</p>",
    unsafe_allow_html=True
)

# ── Apply Filters ──────────────────────────────────────────
filtered_df = apply_filters(
    df,
    selected_countries,
    selected_capitals,
    pop_range,
    search_text
)

# ── KPI Cards ──────────────────────────────────────────────
st.markdown("### 📊 Key Metrics")
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-value'>{len(filtered_df):,}</div>
            <div class='kpi-label'>Total Cities</div>
        </div>""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-value'>
                {filtered_df['country'].nunique():,}
            </div>
            <div class='kpi-label'>Countries</div>
        </div>""", unsafe_allow_html=True)

with k3:
    avg_pop = int(filtered_df["population"].mean())
    st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-value'>{avg_pop:,}</div>
            <div class='kpi-label'>Avg Population</div>
        </div>""", unsafe_allow_html=True)

with k4:
    max_city = filtered_df.loc[
        filtered_df["population"].idxmax(), "city"
    ]
    st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-value' style='font-size:18px;'>
                {max_city}
            </div>
            <div class='kpi-label'>Most Populous City</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts Row 1 ───────────────────────────────────────────
st.markdown("### 📈 Chart Analysis")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.pyplot(pie_chart(filtered_df))
with col2:
    st.pyplot(histogram(filtered_df))

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts Row 2 ───────────────────────────────────────────
col3, col4 = st.columns(2)
with col3:
    st.pyplot(line_chart(filtered_df))
with col4:
    st.pyplot(bar_chart(filtered_df))

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts Row 3 ───────────────────────────────────────────
col5, col6 = st.columns(2)
with col5:
    st.pyplot(scatter_plot(filtered_df))
with col6:
    st.pyplot(box_plot(filtered_df))

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts Row 4 ───────────────────────────────────────────
col7, col8 = st.columns(2)
with col7:
    st.pyplot(heatmap(filtered_df))
with col8:
    st.pyplot(area_chart(filtered_df))

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts Row 5 ───────────────────────────────────────────
col9, col10 = st.columns(2)
with col9:
    st.pyplot(count_plot(filtered_df))
with col10:
    st.pyplot(violin_plot(filtered_df))

st.markdown("<br>", unsafe_allow_html=True)

# ── Raw Data Table ─────────────────────────────────────────
st.markdown("### 📋 Raw Data Preview")
st.markdown("---")
st.dataframe(
    filtered_df.head(100).style.background_gradient(
        cmap="Blues", subset=["population"]
    ),
    use_container_width=True
)

st.markdown(
    "<p style='text-align:center; color:#aaaaaa; font-size:12px;'>"
    "World Cities Dashboard | EDA Project | SAP ID: 70177415"
    "</p>",
    unsafe_allow_html=True
)