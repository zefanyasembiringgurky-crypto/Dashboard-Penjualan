import streamlit as st
import datetime
import random

# Konfigurasi Halaman
st.set_page_config(
    page_title="Untuk Kamu yang Dirindukan 🤍",
    page_icon="💌",
    layout="centered"
)

# Custom CSS untuk nuansa aesthetic/romantis
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #fff0f5 0%, #ffd1dc 50%, #ffc0cb 100%); }
    .romantic-title { text-align: center; color: #b03060; font-family: 'Georgia', serif; font-weight: 300; }
    .subtitle { text-align: center; color: #6d4c41; font-style: italic; margin-bottom: 30px; }
    .love-card { background: rgba(255, 255, 255, 0.75); padding: 24px; border-radius: 20px; box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.08); text-align: center; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# Header Utama
st.markdown("<h1 class='romantic-title'>For My Favorite Person 🤍</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Kasih sayang yang tidak punya tombol 'off'</p>", unsafe_allow_html=True)

# 1. Hari / Waktu Bersama (Counter)
st.markdown("<div class='love-card'><h3>⏳ Menghitung Waktu Berharga</h3>", unsafe_allow_html=True)
start_date = st.date_input("Kapan hari spesial/mulai dekat kita?", datetime.date(2023, 1, 1))
days_count = (datetime.date.today() - start_date).days
st.metric(label="Hari penuh cerita terukir:", value=f"{days_count:,} Hari")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='love-card'><h3>💌 Lagi Kangen Ya?</h3>", unsafe_allow_html=True)
pesan = [
    "Hei... jangan lupa makan, jangan terlalu kecapekan. Aku di sini.",
    "Rindu ini ibarat ombak, kadang tenang kadang kencang, tapi tujuannya tetap ke pantai yang sama: kamu.",
    "Walaupun gak ngabarin 24 jam, pikiranku sempat mampir ke senyummu hari ini kok."
]
if st.button("Pencet Kalau Lagi Kangen 🥺", use_container_width=True):
    st.balloons()
    st.success(random.choice(pesan))
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; font-size: 0.85em;'>Web ini online 24/7 buat kamu buka kapan saja rindu datang 🤍</p>", unsafe_allow_html=True)
