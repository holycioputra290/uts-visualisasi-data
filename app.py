import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman Web App
st.set_page_config(
    page_title="Shopping Trends Dashboard - macOS",
    page_icon="💻",
    layout="wide"
)

# ---------------------------------------------------------
# CUSTOM CSS: DESAIN WEB APPLICATION ALA macOS / APPLE UI
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Font Apple SF Pro Look */
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Background Utama Aplikasi Web */
    .stApp {
        background-color: #0f1117;
    }
    
    /* Styling Sidebar ala Control Center / Finder macOS */
    [data-testid="stSidebar"] {
        background-color: #161922;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    /* Box Transparan / Frosted Glass Container untuk Grafik & Modul */
    .css-card {
        background: #1e2230;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    }
    
    /* KPI Card Style ala Widget iOS / macOS */
    div[data-testid="stMetric"] {
        background: #1e2230;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 18px 22px;
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        border-color: #0A84FF;
    }

    div[data-testid="stMetricLabel"] {
        color: #8e8e93;
        font-weight: 500;
        font-size: 0.9rem;
    }

    div[data-testid="stMetricValue"] {
        color: #ffffff;
        font-weight: 700;
        font-size: 1.7rem;
    }

    /* Expander Storytelling Card */
    .streamlit-expanderHeader {
        background-color: #1e2230 !important;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        color: #ffffff !important;
    }
    
    /* Slider Warna Accent Apple Blue */
    .stSlider > div > div > div > div {
        background-color: #0A84FF !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Load Dataset
@st.cache_data
def load_data():
    df = pd.read_csv('shopping_trends_updated.csv')
    df = df.drop_duplicates()
    df = df.dropna()
    return df

df = load_data()

# ---------------------------------------------------------
# SIDEBAR: Control Center Web
# ---------------------------------------------------------
st.sidebar.markdown("### 🎛️ Control Center")
st.sidebar.caption("Filter Dashboard Interaktif")
st.sidebar.markdown("---")

list_category = df['Category'].unique().tolist()
selected_category = st.sidebar.multiselect(
    "Kategori Produk:",
    options=list_category,
    default=list_category
)

list_gender = df['Gender'].unique().tolist()
selected_gender = st.sidebar.multiselect(
    "Gender Pelanggan:",
    options=list_gender,
    default=list_gender
)

min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
selected_age = st.sidebar.slider(
    "Rentang Usia:",
    min_value=min_age,
    max_value=max_age,
    value=(min_age, max_age)
)

# Apply Filter
df_filtered = df[
    (df['Category'].isin(selected_category)) &
    (df['Gender'].isin(selected_gender)) &
    (df['Age'].between(selected_age[0], selected_age[1]))
]

# ---------------------------------------------------------
# HEADER WEB & TOP NAVBAR LOOK
# ---------------------------------------------------------
st.markdown("""
    <div style="background-color: #161922; padding: 20px 25px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.08); margin-bottom: 25px;">
        <h2 style="margin:0; color: #ffffff; font-weight: 700;">🛍️ Customer Shopping Analytics App</h2>
        <p style="margin: 4px 0 0 0; color: #8e8e93; font-size: 0.95rem;">Web Dashboard Visualisasi Data — UTS System Information Project</p>
    </div>
""", unsafe_allow_html=True)

# Storytelling Component
with st.expander("📌 Executive Summary & Data Insights", expanded=True):
    st.write("""
    * **Pendapatan Utama:** Sektor *Clothing* & *Accessories* memberikan kontribusi nilai penjualan tertinggi.
    * **Demografi Pembeli:** Mayoritas pelanggan aktif berada pada rentang usia 18 hingga 50 tahun.
    * **Tingkat Kepuasan:** Rata-rata kepuasan konsumen mencapai **3.75 / 5.0**, tergolong positif namun tetap membutuhkan optimasi pada lini produk tertentu.
    """)

st.write("")

# ---------------------------------------------------------
# MODUL 1: KPI WIDGETS
# ---------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_revenue = df_filtered['Purchase Amount (USD)'].sum()
    st.metric(label="Total Revenue", value=f"${total_revenue:,.0f}")

with col2:
    total_customers = len(df_filtered)
    st.metric(label="Total Orders", value=f"{total_customers:,}")

with col3:
    avg_purchase = df_filtered['Purchase Amount (USD)'].mean()
    st.metric(label="Avg Order Value", value=f"${avg_purchase:,.2f}")

with col4:
    avg_rating = df_filtered['Review Rating'].mean()
    st.metric(label="Avg Rating", value=f"⭐ {avg_rating:.2f}")

st.write("")

# ---------------------------------------------------------
# MODUL 2: WEB CONTAINER CHARTS (KARTU KACA SEPARATE)
# ---------------------------------------------------------
st.markdown("### 📊 Analytics Overview")

apple_colors = ['#0A84FF', '#30D158', '#FF9F0A', '#BF5AF2', '#FF453A', '#64D2FF']

# Row 1 Grafik
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.markdown("**Total Revenue per Category**")
    cat_sales = df_filtered.groupby('Category')['Purchase Amount (USD)'].sum().reset_index()
    fig_bar = px.bar(
        cat_sales,
        x='Category',
        y='Purchase Amount (USD)',
        color='Category',
        text_auto='.2s',
        color_discrete_sequence=apple_colors
    )
    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ffffff"),
        showlegend=False,
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(title="", showgrid=False),
        yaxis=dict(title="Revenue ($)", showgrid=True, gridcolor="rgba(255,255,255,0.05)")
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row1_col2:
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.markdown("**Payment Method Share**")
    payment_counts = df_filtered['Payment Method'].value_counts().reset_index()
    payment_counts.columns = ['Payment Method', 'Count']
    fig_pie = px.pie(
        payment_counts,
        names='Payment Method',
        values='Count',
        hole=0.55,
        color_discrete_sequence=apple_colors
    )
    fig_pie.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ffffff"),
        margin=dict(l=10, r=10, t=30, b=10)
    )
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Row 2 Grafik
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.markdown("**Customer Age Distribution**")
    fig_hist = px.histogram(
        df_filtered,
        x='Age',
        nbins=15,
        color_discrete_sequence=['#0A84FF']
    )
    fig_hist.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ffffff"),
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(title="Age", showgrid=False),
        yaxis=dict(title="Count", showgrid=True, gridcolor="rgba(255,255,255,0.05)")
    )
    st.plotly_chart(fig_hist, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row2_col2:
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.markdown("**Age vs Purchase Amount**")
    fig_scatter = px.scatter(
        df_filtered,
        x='Age',
        y='Purchase Amount (USD)',
        color='Category',
        color_discrete_sequence=apple_colors,
        hover_data=['Item Purchased']
    )
    fig_scatter.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ffffff"),
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(title="Age", showgrid=False),
        yaxis=dict(title="Purchase Amount ($)", showgrid=True, gridcolor="rgba(255,255,255,0.05)")
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
