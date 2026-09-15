import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime

# --- CONFIG & LAYOUT ---
st.set_page_config(
    page_title="Dashboard Analisis Data Penjualan",
    page_icon="📊",
    layout="wide"
)

# Custom CSS ala Dashboard gelap/elegan
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f5;
    }
    .metric-box {
        background-color: white;
        padding: 16px;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center;
    }
    .callout-cyan {
        background-color: #00838f;
        color: white;
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 12px;
    }
    .callout-dark {
        background-color: #263238;
        color: white;
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 12px;
    }
    .callout-pink {
        background-color: #e91e63;
        color: white;
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER UTAMA ---
st.markdown("""
<div style="background-color: #263238; color: white; padding: 15px 25px; border-radius: 12px; display: flex; align-items: center; margin-bottom: 20px;">
    <h2 style="margin:0; font-size: 24px;">📊 Dashboard Analisis Data Penjualan</h2>
</div>
""", unsafe_allow_html=True)

# --- GENERATE / UPLOAD DATA ---
with st.sidebar:
    st.header("📁 Sumber Data")
    uploaded_file = st.file_uploader("Upload Excel (.xlsx) / CSV", type=["xlsx", "csv"])

@st.cache_data
def get_sample_data():
    np.random.seed(42)
    dates = pd.date_range(start='2021-01-01', end='2022-12-31', freq='D')
    products = [
        'Yoyic Bluebery', 'Pocky', 'Golda Coffee', 'Nyam-nyam', 
        'Lotte Chocopie', 'Beng beng', 'Lifebuoy Cair 900ml', 
        'Oreo Wafer Sandwich', 'Tipe X Joyko', 'Pepsodent 120 gr'
    ]
    categories = ['Perawatan Tubuh', 'Minuman', 'Makanan', 'Alat Tulis']
    jenis_penjualan = ['Eceran', 'Grosir', 'Online']
    pembayaran = ['Cash', 'Kredit']
    
    n = 1500
    df = pd.DataFrame({
        'Tanggal': np.random.choice(dates, n),
        'Produk': np.random.choice(products, n, p=[0.18, 0.12, 0.11, 0.1, 0.09, 0.09, 0.08, 0.08, 0.08, 0.07]),
        'Kategori': np.random.choice(categories, n, p=[0.35, 0.3, 0.2, 0.15]),
        'Jenis_Penjualan': np.random.choice(jenis_penjualan, n, p=[0.4, 0.36, 0.24]),
        'Pembayaran': np.random.choice(pembayaran, n, p=[0.85, 0.15]),
        'Qty': np.random.randint(1, 10, n),
        'Harga_Satuan': np.random.choice([15000, 25000, 35000, 50000], n)
    })
    df['Tahun'] = df['Tanggal'].dt.year
    df['Bulan'] = df['Tanggal'].dt.month
    df['Total_Penjualan'] = df['Qty'] * df['Harga_Satuan']
    df['Profit'] = df['Total_Penjualan'] * 0.19  # asumsi margin 19%
    return df

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        if 'Tanggal' in df.columns: df['Tanggal'] = pd.to_datetime(df['Tanggal'])
        if 'Tahun' not in df.columns and 'Tanggal' in df.columns: df['Tahun'] = df['Tanggal'].dt.year
        if 'Bulan' not in df.columns and 'Tanggal' in df.columns: df['Bulan'] = df['Tanggal'].dt.month
    except:
        df = get_sample_data()
else:
    df = get_sample_data()

# --- SIDEBAR FILTERS (TAHUN, PEMBAYARAN, BULAN) ---
with st.sidebar:
    st.markdown("---")
    st.subheader("🗓️ FILTER TAHUN")
    all_years = sorted(df['Tahun'].unique())
    selected_tahun = st.multiselect("Pilih Tahun:", all_years, default=all_years)

    st.subheader("💳 FILTER PEMBAYARAN")
    all_pay = sorted(df['Pembayaran'].unique())
    selected_pay = st.multiselect("Pilih Pembayaran:", all_pay, default=all_pay)

    st.subheader("📅 FILTER BULAN")
    bulan_dict = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
    selected_bulan = st.multiselect("Pilih Bulan:", options=list(bulan_dict.keys()), format_func=lambda x: bulan_dict[x], default=list(bulan_dict.keys()))

# Filter DataFrame
df_f = df[
    df['Tahun'].isin(selected_tahun) & 
    df['Pembayaran'].isin(selected_pay) & 
    df['Bulan'].isin(selected_bulan)
]

# --- MAIN LAYOUT 3 KOLOM: [SIDEBAR PANEL], [MAIN CONTENT], [BULAN PANEL] ---
col_left_panel, col_main, col_right_panel = st.columns([1.2, 5, 1.2])

with col_left_panel:
    # 1. Produk Terlaris Callout
    top_prod = df_f.groupby('Produk')['Qty'].sum().idxmax() if not df_f.empty else "N/A"
    top_prod_qty = df_f.groupby('Produk')['Qty'].sum().max() if not df_f.empty else 0
    st.markdown(f"""
    <div class="callout-cyan">
        <small style="opacity:0.8;">Produk Terlaris</small>
        <h4 style="margin:2px 0; font-size:16px;">{top_prod}</h4>
        <h2 style="margin:0;">{top_prod_qty:,}</h2>
        <small>Pcs</small>
    </div>
    """, unsafe_allow_html=True)

    # 2. Kategori Terlaris Callout
    top_cat = df_f.groupby('Kategori')['Total_Penjualan'].sum().idxmax() if not df_f.empty else "N/A"
    top_cat_val = df_f.groupby('Kategori')['Total_Penjualan'].sum().max() if not df_f.empty else 0
    st.markdown(f"""
    <div class="callout-dark">
        <small style="opacity:0.8;">Kategori Terlaris</small>
        <h4 style="margin:2px 0; font-size:15px;">{top_cat}</h4>
        <h3 style="margin:0;">Rp {top_cat_val/1e6:.1f} jt</h3>
    </div>
    """, unsafe_allow_html=True)

    # 3. Kontribusi Nilai Penjualan
    st.markdown("""
    <div class="callout-pink">
        <h4 style="margin:0 0 10px 0; font-size:15px;">Kontribusi Nilai Penjualan</h4>
    """, unsafe_allow_html=True)
    cat_contrib = df_f.groupby('Kategori')['Total_Penjualan'].sum() if not df_f.empty else pd.Series(dtype=float)
    total_rev_all = cat_contrib.sum() if cat_contrib.sum() > 0 else 1
    for c, v in cat_contrib.items():
        pct = (v / total_rev_all) * 100
        st.markdown(f"<div style='display:flex; justify-content:space-between; font-size:13px;'><span>{c}</span><b>{pct:.0f}%</b></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


with col_main:
    # --- TOP 3 METRICS CARDS ---
    tot_penjualan = df_f['Total_Penjualan'].sum() if not df_f.empty else 0
    tot_profit = df_f['Profit'].sum() if not df_f.empty else 0
    tot_qty = df_f['Qty'].sum() if not df_f.empty else 0

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""
        <div class="metric-box">
            <small style="color:gray;">Total Penjualan</small>
            <h2 style="margin:5px 0 0 0; color:#263238;">{tot_penjualan:,.0f}</h2>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-box">
            <small style="color:gray;">Total Profit</small>
            <h2 style="margin:5px 0 0 0; color:#263238;">{tot_profit:,.0f}</h2>
            <small style="color:green;">19%</small>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-box">
            <small style="color:gray;">Total Produk Terjual</small>
            <h2 style="margin:5px 0 0 0; color:#263238;">{tot_qty:,.0f}</h2>
            <small>Pcs</small>
        </div>
        """, unsafe_allow_html=True)

    st.write("") # spasi

    # --- ROW 1 GRAFIK: BULANAN & JENIS PENJUALAN ---
    c_graf1, c_graf2 = st.columns([2.2, 1.8])
    with c_graf1:
        st.subheader("📅 Bulanan")
        monthly = df_f.groupby('Bulan')['Total_Penjualan'].sum().reindex(range(1,13), fill_value=0)
        df_m = pd.DataFrame({'Bulan': [bulan_dict[i] for i in monthly.index], 'Nilai': monthly.values})
        fig_m = px.bar(df_m, x='Bulan', y='Nilai', color_discrete_sequence=['#ffa726'])
        fig_m.update_layout(height=280, margin=dict(l=20,r=20,t=20,b=20), xaxis_title="", yaxis_title="")
        st.plotly_chart(fig_m, use_container_width=True)

    with c_graf2:
        st.subheader("🛒 Jenis Penjualannya")
        jp = df_f.groupby('Jenis_Penjualan')['Total_Penjualan'].sum() if not df_f.empty else pd.Series(dtype=float)
        fig_jp = px.pie(names=jp.index, values=jp.values, hole=0.5, color_discrete_sequence=['#ffa726', '#8d6e63', '#d7ccc8'])
        fig_jp.update_layout(height=280, margin=dict(l=20,r=20,t=20,b=20), showlegend=True)
        st.plotly_chart(fig_jp, use_container_width=True)

    # --- ROW 2 GRAFIK: PENJUALAN/TAHUN, KATEGORI, PEMBAYARAN ---
    c_r2_1, c_r2_2, c_r2_3 = st.columns([1.5, 1.8, 1.7])
    with c_r2_1:
        st.subheader("💲 Penjualan/Tahun")
        yt = df_f.groupby('Tahun')['Total_Penjualan'].sum() if not df_f.empty else pd.Series(dtype=float)
        fig_yt = px.bar(x=yt.values/1e6, y=[str(t) for t in yt.index], orientation='h', color_discrete_sequence=['#ffa726'])
        fig_yt.update_layout(height=240, margin=dict(l=20,r=20,t=20,b=20), xaxis_title="Jt", yaxis_title="")
        st.plotly_chart(fig_yt, use_container_width=True)

    with c_r2_2:
        st.subheader("📦 Penjualan/Kategori")
        cat_s = df_f.groupby('Kategori')['Total_Penjualan'].sum() if not df_f.empty else pd.Series(dtype=float)
        fig_cat = px.bar(x=cat_s.index, y=cat_s.values, color_discrete_sequence=['#8d6e63'])
        fig_cat.update_layout(height=240, margin=dict(l=20,r=20,t=20,b=20), xaxis_title="", yaxis_title="")
        st.plotly_chart(fig_cat, use_container_width=True)

    with c_r2_3:
        st.subheader("💳 Cara Pembayaran")
        pay_s = df_f.groupby('Pembayaran')['Total_Penjualan'].sum() if not df_f.empty else pd.Series(dtype=float)
        fig_pay = px.pie(names=pay_s.index, values=pay_s.values, hole=0.5, color_discrete_sequence=['#ffa726', '#8d6e63'])
        fig_pay.update_layout(height=240, margin=dict(l=20,r=20,t=20,b=20))
        st.plotly_chart(fig_pay, use_container_width=True)


with col_right_panel:
    # 4. Panel Kanan: 10 Produk Terlaris Horizontal Bar
    st.subheader("📦 10 Produk Terlaris")
    top10 = df_f.groupby('Produk')['Qty'].sum().nlargest(10) if not df_f.empty else pd.Series(dtype=float)
    df_top10 = pd.DataFrame({'Produk': top10.index, 'Qty': top10.values}).sort_values(by='Qty', ascending=True)
    fig_top10 = px.bar(df_top10, x='Qty', y='Produk', orientation='h', color_discrete_sequence=['#ffa726'])
    fig_top10.update_layout(height=580, margin=dict(l=10,r=10,t=20,b=20), xaxis_title="", yaxis_title="")
    st.plotly_chart(fig_top10, use_container_width=True)

# Expander data mentah di bawah
with st.expander("📄 Lihat Data Transaksi Lengkap"):
    st.dataframe(df_f, use_container_width=True)
