import streamlit as st
from PIL import Image
import easyocr
import numpy as np

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="OCR dengan EasyOCR", layout="centered")

# Judul aplikasi
st.title("OCR Sederhana untuk Ekstraksi Teks dari Gambar")

st.write("""
1. Unggah file gambar dari local Anda.  
2. Teks akan diekstraksi secara otomatis.
""")

# Pilihan unggah dari file
st.subheader("Input Gambar")
uploaded_file = st.file_uploader("Unggah gambar dari file", type=["png", "jpg", "jpeg"])

# Proses OCR jika ada gambar
if uploaded_file is not None:
    # Membaca gambar
    image = Image.open(uploaded_file)
    
    # Menampilkan gambar yang diunggah
    st.subheader("Gambar yang Diproses")
    st.image(image, caption="Gambar Anda", use_column_width=True)

    # Konversi gambar ke numpy array
    image_np = np.array(image)

    # OCR menggunakan EasyOCR
    st.subheader("Hasil OCR")
    with st.spinner("Sedang memproses..."):
        reader = easyocr.Reader(['en'])  # Ganti 'en' jika Anda ingin bahasa lain
        results = reader.readtext(image_np)

    # Menampilkan hasil OCR
    if results:
        extracted_text = "\n".join([res[1] for res in results])  # Gabungkan semua teks
        st.text_area("Hasil Teks Ekstraksi", extracted_text, height=200)
    else:
        st.error("Tidak ada teks yang terdeteksi.")
