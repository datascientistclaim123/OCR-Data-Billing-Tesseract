import os
import subprocess
import streamlit as st
from PIL import Image
import pytesseract

# Set page config (harus dipanggil pertama)
st.set_page_config(page_title="OCR dengan Tesseract", layout="centered")

# Set path ke executable Tesseract (Linux - Streamlit Cloud)
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Konfigurasi halaman Streamlit
st.title("OCR Sederhana untuk Ekstraksi Teks dari Gambar")

st.write("""
1. Screenshot teks menggunakan tombol `PrtSc` atau upload file gambar dari local.  
2. **Unggah gambar** hasil Screenshot atau file gambar lokal.
3. Teks akan diekstraksi secara otomatis.
""")

# Variabel untuk menyimpan gambar
image = None

# Kolom untuk upload gambar
col1 = st.columns(1)

with col1:
    uploaded_file = st.file_uploader("Unggah Gambar dari File Local", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)

# Jika gambar ada, lakukan OCR
if image:
    st.subheader("Gambar yang Diproses")
    st.image(image, caption="Gambar Anda", use_column_width=True)

    # OCR
    st.subheader("Hasil OCR")
    with st.spinner("Sedang memproses..."):
        try:
            # Proses OCR dengan tesseract
            extracted_text = pytesseract.image_to_string(image)
            st.text_area("Hasil Teks Ekstraksi", extracted_text, height=200)
        except Exception as e:
            st.error(f"Terjadi kesalahan saat OCR: {e}")

