import streamlit as st
from PIL import Image, ImageGrab
import easyocr
import numpy as np
import re

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="OCR dengan EasyOCR", layout="centered")

# Judul aplikasi
st.title("OCR Sederhana untuk Ekstraksi Teks dari Gambar")

st.write("""
1. Screenshot teks menggunakan tombol `PrtSc` atau upload file gambar dari local.  
2. **Tempel gambar** hasil Screenshot menggunakan tombol `Tempel Gambar dari Clipboard` di bawah secara langsung atau `Unggah Gambar dari File Local`.
3. Teks akan diekstraksi secara otomatis.
""")

# Tombol untuk menangkap gambar dari clipboard
st.subheader("Input Gambar")
col1, col2 = st.columns(2)

# Variabel untuk menyimpan gambar
image = None

# Pilihan upload dari file
with col1:
    uploaded_file = st.file_uploader("Unggah gambar dari file", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)

# Pilihan tempel dari clipboard
with col2:
    if st.button("Tempel Gambar dari Clipboard"):
        try:
            # Mengambil gambar dari clipboard
            clipboard_image = ImageGrab.grabclipboard()
            if clipboard_image is not None:
                st.success("Gambar berhasil ditempel dari clipboard!")
                image = clipboard_image
            else:
                st.error("Tidak ada gambar di clipboard. Silakan coba lagi.")
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

# Fungsi untuk memperbaiki pemisahan kalimat berdasarkan newline yang tidak diinginkan
def fix_newlines(text):
    # Pisahkan teks berdasarkan newline
    lines = text.split('\n')

    # Gabungkan baris jika baris berikutnya tidak memiliki tanda baca akhir
    for i in range(len(lines) - 1):
        if lines[i][-1] not in ['.', '?', '!'] and lines[i+1][0].islower():
            lines[i] += ' ' + lines[i+1]
            lines[i+1] = ''
    
    # Gabungkan kembali menjadi teks
    return ' '.join([line for line in lines if line])

# Proses OCR jika ada gambar
if image:
    # Menampilkan gambar yang diunggah atau ditempel
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
        
        # Memperbaiki pemisahan kalimat yang tidak diinginkan
        cleaned_text = fix_newlines(extracted_text)

        # Tampilkan hasil teks yang sudah dibersihkan
        st.text_area("Hasil Teks Ekstraksi", cleaned_text, height=200)
    else:
        st.error("Tidak ada teks yang terdeteksi.")
