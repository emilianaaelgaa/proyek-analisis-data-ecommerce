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

BASE_DIR = Path(__file__).resolve().parent

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
        Dashboard ini menampilkan hasil analisis data e-commerce secara interaktif.
        Pengguna dapat memilih rentang tanggal untuk melihat perubahan ringkasan performa,
        tren pesanan, pendapatan, kategori produk, dan segmentasi pelanggan.
    </p>
    """,
    unsafe_allow_html=True
)


@st.cache_data
def load_data():
    main_data = pd.read_csv(BASE_DIR / "main_data.csv")
    main_data["order_purchase_timestamp"] = pd.to_datetime(main_data["order_purchase_timestamp"])
    return main_data


main_data = load_data()

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
        "Filter tanggal ini akan memengaruhi ringkasan performa, tren bulanan, kategori produk, dan segmentasi pelanggan."
    )

if len(date_range) == 2:
    start_date, end_date = date_range

    filtered_data = main_data[
        (main_data["order_purchase_timestamp"].dt.date >= start_date) &
        (main_data["order_purchase_timestamp"].dt.date <= end_date)
    ].copy()
else:
    filtered_data = main_data.copy()

if filtered_data.empty:
    st.warning("Tidak ada data pada rentang tanggal yang dipilih.")
    st.stop()


# Menghapus duplikasi order agar total order dan payment_value tidak terhitung berulang
order_filtered_df = filtered_data.drop_duplicates(subset="order_id").copy()


st.subheader("📌 Ringkasan Performa E-Commerce")

total_orders = order_filtered_df["order_id"].nunique()
total_revenue = order_filtered_df["payment_value"].sum()
total_customers = order_filtered_df["customer_unique_id"].nunique()

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
        Ringkasan performa dihitung ulang berdasarkan rentang tanggal yang dipilih pada sidebar.
    </div>
    """,
    unsafe_allow_html=True
)


st.divider()

st.subheader("📈 Tren Jumlah Pesanan dan Pendapatan per Bulan")

monthly_filtered_df = order_filtered_df.resample(
    rule="M",
    on="order_purchase_timestamp"
).agg({
    "order_id": "nunique",
    "payment_value": "sum"
})

monthly_filtered_df.index = monthly_filtered_df.index.strftime("%Y-%m")
monthly_filtered_df = monthly_filtered_df.reset_index()

monthly_filtered_df.rename(columns={
    "order_purchase_timestamp": "month",
    "order_id": "order_count",
    "payment_value": "total_revenue"
}, inplace=True)

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(10, 5))

    sns.lineplot(
        data=monthly_filtered_df,
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
        data=monthly_filtered_df,
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

st.markdown(
    """
    <div class='section-note'>
        Visualisasi tren bulanan berubah sesuai filter tanggal, sehingga pengguna dapat mengeksplorasi
        performa pesanan dan pendapatan pada periode tertentu.
    </div>
    """,
    unsafe_allow_html=True
)


st.divider()

st.subheader("🛍️ Analisis Kategori Produk")

category_filtered_df = filtered_data.groupby("product_category").agg({
    "revenue": "sum",
    "order_id": "nunique"
}).reset_index()

category_filtered_df.rename(columns={
    "revenue": "total_revenue",
    "order_id": "order_count"
}, inplace=True)

category_filtered_df = category_filtered_df.sort_values(
    by="total_revenue",
    ascending=False
)

top_category = category_filtered_df.head(10)

bottom_category = category_filtered_df.tail(10).sort_values(
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
        Analisis kategori produk dihitung ulang berdasarkan filter tanggal. Dengan demikian,
        pengguna dapat melihat kategori yang paling berkontribusi pada periode tertentu.
    </div>
    """,
    unsafe_allow_html=True
)


st.divider()

st.subheader("👥 Segmentasi Pelanggan Berdasarkan RFM Analysis")

recent_date = order_filtered_df["order_purchase_timestamp"].max() + pd.Timedelta(days=1)

rfm_filtered_df = order_filtered_df.groupby("customer_unique_id").agg({
    "order_purchase_timestamp": lambda x: (recent_date - x.max()).days,
    "order_id": "nunique",
    "payment_value": "sum"
}).reset_index()

rfm_filtered_df.rename(columns={
    "order_purchase_timestamp": "recency",
    "order_id": "frequency",
    "payment_value": "monetary"
}, inplace=True)

if len(rfm_filtered_df) >= 4:
    rfm_filtered_df["r_score"] = pd.qcut(
        rfm_filtered_df["recency"].rank(method="first"),
        4,
        labels=[4, 3, 2, 1]
    )

    rfm_filtered_df["f_score"] = pd.qcut(
        rfm_filtered_df["frequency"].rank(method="first"),
        4,
        labels=[1, 2, 3, 4]
    )

    rfm_filtered_df["m_score"] = pd.qcut(
        rfm_filtered_df["monetary"].rank(method="first"),
        4,
        labels=[1, 2, 3, 4]
    )

    rfm_filtered_df["total_score"] = (
        rfm_filtered_df["r_score"].astype(int)
        + rfm_filtered_df["f_score"].astype(int)
        + rfm_filtered_df["m_score"].astype(int)
    )

    def customer_segment(score):
        if score >= 10:
            return "High Value Customer"
        elif score >= 7:
            return "Potential Customer"
        elif score >= 4:
            return "Need Attention"
        else:
            return "At Risk Customer"

    rfm_filtered_df["customer_segment"] = rfm_filtered_df["total_score"].apply(customer_segment)

    segment_filtered_df = rfm_filtered_df.groupby("customer_segment").agg({
        "customer_unique_id": "nunique",
        "recency": "mean",
        "frequency": "mean",
        "monetary": "mean"
    }).reset_index()

    segment_filtered_df.rename(columns={
        "customer_unique_id": "customer_count",
        "recency": "avg_recency",
        "frequency": "avg_frequency",
        "monetary": "avg_monetary"
    }, inplace=True)

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.barplot(
        data=segment_filtered_df.sort_values(by="customer_count", ascending=False),
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

    st.subheader("📋 Data RFM Pelanggan")
    st.dataframe(
        rfm_filtered_df,
        use_container_width=True
    )

else:
    st.warning("Data pada rentang tanggal yang dipilih terlalu sedikit untuk membuat segmentasi RFM.")

st.markdown(
    """
    <div class='section-note'>
        Segmentasi RFM dihitung ulang berdasarkan filter tanggal, sehingga hasil segmentasi
        dapat berubah sesuai periode analisis yang dipilih pengguna.
    </div>
    """,
    unsafe_allow_html=True
)