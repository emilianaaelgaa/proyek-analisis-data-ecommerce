import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set(style="whitegrid")

st.set_page_config(
    page_title="E-Commerce Dashboard",
    page_icon="🛒",
    layout="wide"
)

# Mengatur path agar file CSV tetap terbaca meskipun dashboard dijalankan dari folder berbeda
BASE_DIR = Path(__file__).resolve().parent

# Custom CSS untuk mempercantik tampilan dashboard
st.markdown(
    """
    <style>
    .main {
        background-color: #f8fafc;
    }

    h1 {
        color: #1e3a8a;
        font-weight: 700;
    }

    h2, h3 {
        color: #1f2937;
    }

    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 18px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        border: 1px solid #e5e7eb;
    }

    div[data-testid="stMetricValue"] {
        color: #2563eb;
        font-size: 28px;
        font-weight: 700;
    }

    div[data-testid="stMetricLabel"] {
        color: #4b5563;
        font-size: 15px;
    }

    .dashboard-description {
        text-align: center;
        color: #4b5563;
        font-size: 17px;
        margin-bottom: 30px;
    }

    .section-note {
        background-color: #eff6ff;
        padding: 14px 18px;
        border-radius: 12px;
        color: #1f2937;
        border-left: 5px solid #2563eb;
        margin-bottom: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h1 style='text-align: center;'>
        🛒 E-Commerce Public Dataset Dashboard
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p class='dashboard-description'>
        Dashboard ini menampilkan hasil analisis data e-commerce, mulai dari tren pesanan,
        pendapatan, kategori produk, hingga segmentasi pelanggan berdasarkan RFM Analysis.
    </p>
    """,
    unsafe_allow_html=True
)


@st.cache_data
def load_data():
    main_data = pd.read_csv(BASE_DIR / "main_data.csv")
    monthly_orders = pd.read_csv(BASE_DIR / "monthly_orders.csv")
    category_revenue = pd.read_csv(BASE_DIR / "category_revenue.csv")
    rfm_data = pd.read_csv(BASE_DIR / "rfm_data.csv")
    segment_count = pd.read_csv(BASE_DIR / "segment_count.csv")

    return main_data, monthly_orders, category_revenue, rfm_data, segment_count


main_data, monthly_orders, category_revenue, rfm_data, segment_count = load_data()

main_data["order_purchase_timestamp"] = pd.to_datetime(main_data["order_purchase_timestamp"])

min_date = main_data["order_purchase_timestamp"].min()
max_date = main_data["order_purchase_timestamp"].max()

with st.sidebar:
    st.header("🔎 Filter Data")

    date_range = st.date_input(
        label="Pilih Rentang Tanggal",
        min_value=min_date.date(),
        max_value=max_date.date(),
        value=[min_date.date(), max_date.date()]
    )

    st.caption(
        "Gunakan filter ini untuk melihat ringkasan performa berdasarkan rentang tanggal tertentu."
    )

if len(date_range) == 2:
    start_date, end_date = date_range

    filtered_data = main_data[
        (main_data["order_purchase_timestamp"].dt.date >= start_date) &
        (main_data["order_purchase_timestamp"].dt.date <= end_date)
    ]
else:
    filtered_data = main_data.copy()


# Ringkasan performa
st.subheader("📌 Ringkasan Performa E-Commerce")

total_orders = filtered_data["order_id"].nunique()
total_revenue = filtered_data["payment_value"].sum()
total_customers = filtered_data["customer_unique_id"].nunique()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Pesanan", f"{total_orders:,}")

with col2:
    st.metric("Total Pendapatan", f"{total_revenue:,.2f}")

with col3:
    st.metric("Total Pelanggan", f"{total_customers:,}")

st.markdown(
    """
    <div class='section-note'>
        Ringkasan ini menampilkan total pesanan, total pendapatan, dan total pelanggan
        berdasarkan rentang tanggal yang dipilih pada sidebar.
    </div>
    """,
    unsafe_allow_html=True
)


# Tren bulanan
st.divider()

st.subheader("📈 Tren Jumlah Pesanan dan Pendapatan per Bulan")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(10, 5))

    sns.lineplot(
        data=monthly_orders,
        x="month",
        y="order_count",
        marker="o",
        color="#2563eb",
        ax=ax
    )

    ax.set_title("Tren Jumlah Pesanan per Bulan")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Pesanan")
    ax.tick_params(axis="x", rotation=45)

    plt.tight_layout()
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(10, 5))

    sns.lineplot(
        data=monthly_orders,
        x="month",
        y="total_revenue",
        marker="o",
        color="#16a34a",
        ax=ax
    )

    ax.set_title("Tren Total Pendapatan per Bulan")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Total Pendapatan")
    ax.tick_params(axis="x", rotation=45)

    plt.tight_layout()
    st.pyplot(fig)


# Analisis kategori produk
st.divider()

st.subheader("🛍️ Analisis Kategori Produk")

top_category = category_revenue.head(10)

bottom_category = category_revenue.tail(10).sort_values(
    by="total_revenue",
    ascending=True
)

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.barplot(
        data=top_category,
        x="total_revenue",
        y="product_category",
        color="#3b82f6",
        ax=ax
    )

    ax.set_title("10 Kategori Produk dengan Pendapatan Tertinggi")
    ax.set_xlabel("Total Pendapatan")
    ax.set_ylabel("Kategori Produk")

    plt.tight_layout()
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.barplot(
        data=bottom_category,
        x="total_revenue",
        y="product_category",
        color="#f97316",
        ax=ax
    )

    ax.set_title("10 Kategori Produk dengan Pendapatan Terendah")
    ax.set_xlabel("Total Pendapatan")
    ax.set_ylabel("Kategori Produk")

    plt.tight_layout()
    st.pyplot(fig)

st.markdown(
    """
    <div class='section-note'>
        Analisis kategori produk membantu melihat kategori mana yang memberikan kontribusi
        pendapatan paling besar dan kategori mana yang masih memiliki pendapatan rendah.
    </div>
    """,
    unsafe_allow_html=True
)


# RFM Analysis
st.divider()

st.subheader("👥 Segmentasi Pelanggan Berdasarkan RFM Analysis")

fig, ax = plt.subplots(figsize=(10, 6))

sns.barplot(
    data=segment_count.sort_values(by="customer_count", ascending=False),
    x="customer_count",
    y="customer_segment",
    color="#8b5cf6",
    ax=ax
)

ax.set_title("Jumlah Pelanggan Berdasarkan Segmen RFM")
ax.set_xlabel("Jumlah Pelanggan")
ax.set_ylabel("Segmen Pelanggan")

plt.tight_layout()
st.pyplot(fig)

st.markdown(
    """
    <div class='section-note'>
        RFM Analysis digunakan untuk mengelompokkan pelanggan berdasarkan Recency,
        Frequency, dan Monetary. Segmentasi ini dapat membantu menentukan strategi
        retensi dan pemasaran yang lebih tepat.
    </div>
    """,
    unsafe_allow_html=True
)


# Tabel RFM
st.subheader("📋 Data RFM Pelanggan")

st.dataframe(
    rfm_data,
    use_container_width=True
)