import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman & Tema UI
st.set_page_config(
    page_title="Dashboard Customer Shopping Trends - UTS",
    page_icon="🛍️",
    layout="wide"
)

# 2. Load Dataset
@st.cache_data
def load_data():
    # Mengambil dataset dari folder data/
    df = pd.read_csv('shopping_trends_updated.csv')
    
    # Data Cleaning Dasar
    df = df.drop_duplicates()
    df = df.dropna()
    return df

df = load_data()

# ---------------------------------------------------------
# SIDEBAR: Filter Interaktif (Wajib Minimal 2 Filter)
# ---------------------------------------------------------
st.sidebar.header("🔍 Filter Interaktif")

# Filter 1: Dropdown Kategori Barang
list_category = df['Category'].unique().tolist()
selected_category = st.sidebar.multiselect(
    "Pilih Kategori Produk:",
    options=list_category,
    default=list_category
)

# Filter 2: Dropdown Jenis Kelamin
list_gender = df['Gender'].unique().tolist()
selected_gender = st.sidebar.multiselect(
    "Pilih Gender Pelanggan:",
    options=list_gender,
    default=list_gender
)

# Filter 3: Slicer Rentang Umur
min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
selected_age = st.sidebar.slider(
    "Rentang Umur Pelanggan:",
    min_value=min_age,
    max_value=max_age,
    value=(min_age, max_age)
)

# Penerapan Filter ke Dataframe
df_filtered = df[
    (df['Category'].isin(selected_category)) &
    (df['Gender'].isin(selected_gender)) &
    (df['Age'].between(selected_age[0], selected_age[1]))
]

# ---------------------------------------------------------
# HEADER & STORYTELLING / INSIGHT
# ---------------------------------------------------------
st.title("🛍️ Dashboard Analisis Tren Belanja Pelanggan")
st.markdown("**Mata Kuliah:** Visualisasi Data | **Proyek:** UTS Project-Based")

# Storytelling / Key Insights (Komponen Wajib UTS)
with st.expander("📌 Narasi & Wawasan Utama (Data Storytelling)", expanded=True):
    st.write("""
    1. **Dominasi Kategori:** Produk kategori *Clothing* dan *Accessories* menjadi penyumbang pendapatan terbesar dibandingkan kategori lainnya.
    2. **Demografi Pelanggan:** Kelompok usia dewasa muda hingga menengah menunjukkan frekuensi transaksi dan nilai rata-rata belanja yang paling stabil.
    3. **Evaluasi Rating:** Distribusi kepuasan pelanggan rata-rata berada pada nilai **3.7 - 3.8 / 5.0**, mengindikasikan kualitas layanan secara umum sudah memadai namun masih membutuhkan peningkatan pada beberapa lini produk.
    """)

st.divider()

# ---------------------------------------------------------
# KOMPONEN 1: Ringkasan Utama (KPI Cards - Minimal 3 Cards)
# ---------------------------------------------------------
st.subheader("🎯 Indikator Kinerja Utama (KPI)")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_revenue = df_filtered['Purchase Amount (USD)'].sum()
    st.metric(label="Total Pendapatan ($)", value=f"${total_revenue:,.0f}")

with col2:
    total_customers = len(df_filtered)
    st.metric(label="Total Transaksi", value=f"{total_customers:,}")

with col3:
    avg_purchase = df_filtered['Purchase Amount (USD)'].mean()
    st.metric(label="Rata-Rata Belanja ($)", value=f"${avg_purchase:,.2f}")

with col4:
    avg_rating = df_filtered['Review Rating'].mean()
    st.metric(label="Rata-Rata Rating Ulasan", value=f"⭐ {avg_rating:.2f} / 5.0")

st.divider()

# ---------------------------------------------------------
# KOMPONEN 2: Variasi Bagan (Minimal 4 Jenis Grafik Berbeda)
# ---------------------------------------------------------
st.subheader("📈 Visualisasi Data Interaktif")

row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.write("#### 1. Bar Chart (Total Belanja per Kategori)")
    cat_sales = df_filtered.groupby('Category')['Purchase Amount (USD)'].sum().reset_index()
    fig_bar = px.bar(
        cat_sales,
        x='Category',
        y='Purchase Amount (USD)',
        color='Category',
        text_auto='.2s',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    fig_bar.update_layout(showlegend=False, xaxis_title="Kategori", yaxis_title="Total Belanja ($)")
    st.plotly_chart(fig_bar, use_container_width=True)

with row1_col2:
    st.write("#### 2. Pie / Donut Chart (Proporsi Metode Pembayaran)")
    payment_counts = df_filtered['Payment Method'].value_counts().reset_index()
    payment_counts.columns = ['Payment Method', 'Count']
    fig_pie = px.pie(
        payment_counts,
        names='Payment Method',
        values='Count',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig_pie, use_container_width=True)

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.write("#### 3. Histogram (Distribusi Umur Pelanggan)")
    fig_hist = px.histogram(
        df_filtered,
        x='Age',
        nbins=15,
        color_discrete_sequence=['#2E86AB']
    )
    fig_hist.update_layout(xaxis_title="Umur (Tahun)", yaxis_title="Jumlah Pelanggan")
    st.plotly_chart(fig_hist, use_container_width=True)

with row2_col2:
    st.write("#### 4. Scatter Plot (Korelasi Rating vs Nilai Belanja)")
    fig_scatter = px.scatter(
        df_filtered,
        x='Age',
        y='Purchase Amount (USD)',
        color='Category',
        hover_data=['Item Purchased', 'Payment Method']
    )
    fig_scatter.update_layout(xaxis_title="Umur Pelanggan", yaxis_title="Nilai Transaksi ($)")
    st.plotly_chart(fig_scatter, use_container_width=True)
