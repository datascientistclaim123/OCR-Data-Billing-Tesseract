import os
import subprocess
import numpy as np
from PIL import Image
import easyocr
import streamlit as st
import platform
from io import BytesIO

# Periksa platform
is_linux = platform.system() == "Linux"

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="OCR dengan EasyOCR", layout="centered")
st.title("OCR Sederhana untuk Ekstraksi Teks dari Gambar")

st.write("""
1. Screenshot teks menggunakan tombol `PrtSc` atau upload file gambar dari local.  
2. **Tempel gambar** hasil Screenshot menggunakan tombol `Tempel Gambar dari Clipboard` di bawah secara langsung atau `Unggah Gambar dari File Local`.
3. Teks akan diekstraksi secara otomatis.
""")

# Tombol untuk menangkap gambar dari clipboard
st.subheader("Input Gambar")
col1, col2 = st.columns(2)

image = None  # Variabel untuk menyimpan gambar

# Pilihan upload dari file
with col1:
    uploaded_file = st.file_uploader("Unggah gambar dari file", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)

# Pilihan tempel dari clipboard
with col2:
    if st.button("Tempel Gambar dari Clipboard"):
        if is_linux:
            try:
                # Jalankan xclip untuk membaca clipboard
                result = subprocess.run(
                    ["xclip", "-selection", "clipboard", "-t", "image/png", "-o"],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                if result.returncode == 0:
                    clipboard_image = BytesIO(result.stdout)
                    image = Image.open(clipboard_image)
                    st.success("Gambar berhasil ditempel dari clipboard!")
                else:
                    st.error(f"Gagal membaca clipboard: {result.stderr.decode('utf-8')}")
            except FileNotFoundError:
                st.error("xclip tidak ditemukan. Silakan instal dengan `sudo apt-get install xclip`.")
        else:
            st.error("Clipboard hanya didukung di Linux dengan xclip.")

# OCR jika ada gambar
if image:
    st.subheader("Gambar yang Diproses")
    st.image(image, caption="Gambar Anda", use_column_width=True)

    # OCR menggunakan EasyOCR
    st.subheader("Hasil OCR")
    with st.spinner("Sedang memproses..."):
        reader = easyocr.Reader(['en'])  # Tambahkan bahasa lain jika diperlukan
        results = reader.readtext(np.array(image))

    # Menampilkan hasil OCR
    if results:
        extracted_text = "\n".join([res[1] for res in results])  # Gabungkan semua teks
        st.text_area("Hasil Teks Ekstraksi", extracted_text, height=200)
    else:
        st.error("Tidak ada teks yang terdeteksi.")
