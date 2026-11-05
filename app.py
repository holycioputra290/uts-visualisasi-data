import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman & Tema UI
st.set_page_config(
    page_title="Dashboard Customer Shopping Trends - UTS",
    page_icon="🛍️",
    layout="wide"
)

# ---------------------------------------------------------
# CUSTOM CSS: STYLING macOS MODERN (DARK & LIGHT FRIENDLY)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Font global ala Apple */
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    # Custom Card KPI (Frosted Glass / Translucent Look)
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px 24px;
        border-radius: 16px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: rgba(255, 255, 255, 0.25);
    }

    div[data-testid="stMetricLabel"] {
        font-weight: 500;
        opacity: 0.8;
        font-size: 0.95rem;
    }

    div[data-testid="stMetricValue"] {
        font-weight: 700;
        font-size: 1.8rem;
    }

    # Style Expander / Insight Card
    .streamlit-expanderHeader {
        font-weight: 600;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* Accent color pada slider */
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
# SIDEBAR: Control Center (macOS Style)
# ---------------------------------------------------------
st.sidebar.title("🎛️ Control Center")
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

# Filter Data
df_filtered = df[
    (df['Category'].isin(selected_category)) &
    (df['Gender'].isin(selected_gender)) &
    (df['Age'].between(selected_age[0], selected_age[1]))
]

# ---------------------------------------------------------
# HEADER & STORYTELLING
# ---------------------------------------------------------
st.title("🛍️ Shopping Trends Analytics")
st.caption("Visualisasi Data | UTS Project-Based")

with st.expander("📌 Executive Summary & Key Insights", expanded=True):
    st.write("""
    * **Kategori Dominan:** Produk *Clothing* & *Accessories* merupakan penggerak utama total pendapatan.
    * **Demografi Pembeli:** Segmen usia muda hingga pertengahan (18–50 tahun) memiliki frekuensi belanja paling stabil.
    * **Skor Kepuasan:** Rata-rata rating ulasan berada pada angka **3.75 / 5.0**, menunjukkan kepuasan layanan yang baik secara menyeluruh.
    """)

st.write("")

# ---------------------------------------------------------
# KOMPONEN 1: KPI Cards (Widget macOS Frosted Glass)
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
    st.metric(label="Avg Review Rating", value=f"⭐ {avg_rating:.2f}")

st.write("")
st.write("")

# ---------------------------------------------------------
# KOMPONEN 2: Visualisasi Data (Plotly Dark Theme Adaptation)
# ---------------------------------------------------------
st.subheader("📊 Analytics Overview")

row1_col1, row1_col2 = st.columns(2)

# Color palette Apple (iOS Vibrant)
apple_palette = ['#0A84FF', '#30D158', '#FF9F0A', '#BF5AF2', '#FF453A', '#64D2FF']

with row1_col1:
    st.write("**Total Revenue per Category**")
    cat_sales = df_filtered.groupby('Category')['Purchase Amount (USD)'].sum().reset_index()
    fig_bar = px.bar(
        cat_sales,
        x='Category',
        y='Purchase Amount (USD)',
        color='Category',
        text_auto='.2s',
        color_discrete_sequence=apple_palette
    )
    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_title="",
        yaxis_title="Revenue ($)"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with row1_col2:
    st.write("**Payment Method Share**")
    payment_counts = df_filtered['Payment Method'].value_counts().reset_index()
    payment_counts.columns = ['Payment Method', 'Count']
    fig_pie = px.pie(
        payment_counts,
        names='Payment Method',
        values='Count',
        hole=0.5,
        color_discrete_sequence=apple_palette
    )
    fig_pie.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig_pie, use_container_width=True)

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.write("**Customer Age Distribution**")
    fig_hist = px.histogram(
        df_filtered,
        x='Age',
        nbins=15,
        color_discrete_sequence=['#0A84FF']
    )
    fig_hist.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_title="Age",
        yaxis_title="Count"
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with row2_col2:
    st.write("**Age vs Purchase Amount**")
    fig_scatter = px.scatter(
        df_filtered,
        x='Age',
        y='Purchase Amount (USD)',
        color='Category',
        color_discrete_sequence=apple_palette,
        hover_data=['Item Purchased']
    )
    fig_scatter.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_title="Age",
        yaxis_title="Purchase Amount ($)"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
