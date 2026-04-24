# Proyek Analisis Data: E-Commerce Public Dataset

Proyek ini dibuat untuk menganalisis E-Commerce Public Dataset. Analisis dilakukan untuk memahami tren jumlah pesanan dan pendapatan, kontribusi kategori produk, serta segmentasi pelanggan menggunakan RFM Analysis.

## Struktur Folder

```text
submission
├── dashboard
│   ├── dashboard.py
│   ├── main_data.csv
│   ├── monthly_orders.csv
│   ├── category_revenue.csv
│   ├── rfm_data.csv
│   └── segment_count.csv
├── data
│   └── E-Commerce Public Dataset
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## Setup Environment

Install library yang dibutuhkan dengan menjalankan perintah berikut:

```bash
pip install -r requirements.txt
```

## Run Streamlit App

Jalankan dashboard dengan perintah berikut:

```bash
streamlit run dashboard/dashboard.py
```

## Dashboard

Dashboard menampilkan beberapa informasi utama, yaitu:

- Ringkasan total pesanan, total pendapatan, dan total pelanggan.
- Tren jumlah pesanan dan total pendapatan per bulan.
- Kategori produk dengan pendapatan tertinggi dan terendah.
- Segmentasi pelanggan berdasarkan RFM Analysis.

## Link Dashboard

Link dashboard Streamlit dapat dilihat pada file `url.txt`.