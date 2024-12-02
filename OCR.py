import os
import numpy as np
from PIL import Image, ImageGrab
import easyocr
import streamlit as st
import platform

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
            st.warning("Clipboard tidak didukung secara langsung di Linux tanpa wl-paste atau xclip.")
        else:
            try:
                clipboard_image = ImageGrab.grabclipboard()
                if clipboard_image is not None:
                    st.success("Gambar berhasil ditempel dari clipboard!")
                    image = clipboard_image
                else:
                    st.error("Tidak ada gambar di clipboard. Silakan coba lagi.")
            except Exception as e:
                st.error(f"Terjadi kesalahan saat mengakses clipboard: {e}")

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
