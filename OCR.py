import os
import subprocess
import streamlit as st
from PIL import Image, ImageGrab

# Install tesseract OCR if not available
def install_tesseract():
    try:
        subprocess.run(['sudo', 'apt-get', 'update'], check=True)
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'tesseract-ocr'], check=True)
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'tesseract-ocr-eng'], check=True)
    except Exception as e:
        print("Error installing tesseract:", e)

install_tesseract()

import pytesseract

# Set page config harus dipanggil pertama
st.set_page_config(page_title="OCR dengan Tesseract", layout="centered")

# Set path ke executable Tesseract (Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\NIV\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Set path ke folder tessdata
tessdata_dir = r'C:\Users\NIV\AppData\Local\Programs\Tesseract-OCR\tessdata'  # Sesuaikan dengan lokasi tessdata Anda
tess_config = f'--tessdata-dir {tessdata_dir}'

# # Debugging Path
# st.write("Path ke Tesseract:", pytesseract.pytesseract.tesseract_cmd)
# st.write("Path ke tessdata:", tessdata_dir)

# # Cek apakah file eng.traineddata tersedia
# if os.path.exists(os.path.join(tessdata_dir, 'eng.traineddata')):
#     st.write("File eng.traineddata ditemukan.")
# else:
#     st.error("File eng.traineddata tidak ditemukan. Periksa lokasi path tessdata Anda.")

# Konfigurasi halaman Streamlit
st.title("OCR Sederhana untuk Ekstraksi Teks dari Gambar")

st.write("""
1. Screenshot teks menggunakan tombol `PrtSc` atau upload file gambar dari local.  
2. **Tempel gambar** hasil Screenshot menggunakan tombol `Tempel Gambar dari Clipboard` di bawah secara langsung atau `Unggah Gambar dari File Local`.
3. Teks akan diekstraksi secara otomatis.
""")

# Variabel untuk menyimpan gambar
image = None

# Kolom untuk upload dan paste gambar
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Unggah Gambar dari File Local", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)

with col2:
    if st.button("Tempel Gambar dari Clipboard"):
        clipboard_image = ImageGrab.grabclipboard()
        if clipboard_image is not None:
            st.success("Gambar berhasil ditempel dari clipboard!")
            image = clipboard_image
        else:
            st.error("Tidak ada gambar di clipboard. Coba lagi.")

# Jika gambar ada, lakukan OCR
if image:
    st.subheader("Gambar yang Diproses")
    st.image(image, caption="Gambar Anda", use_column_width=True)

    # OCR
    st.subheader("Hasil OCR")
    with st.spinner("Sedang memproses..."):
        try:
            # Proses OCR dengan tesseract
            extracted_text = pytesseract.image_to_string(image, config=tess_config)
            st.text_area("Hasil Teks Ekstraksi", extracted_text, height=200)
        except Exception as e:
            st.error(f"Terjadi kesalahan saat OCR: {e}")
