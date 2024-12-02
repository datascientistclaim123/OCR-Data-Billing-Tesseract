import streamlit as st
from PIL import Image
import easyocr
import numpy as np
import re

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="OCR dengan EasyOCR", layout="centered")

# Judul aplikasi
st.title("OCR Sederhana untuk Ekstraksi Teks dari Gambar")

st.write("""
1. Unggah file gambar dari komputer Anda.  
2. Teks akan diekstraksi secara otomatis.
""")

# Pilihan unggah dari file
st.subheader("Input Gambar")
uploaded_file = st.file_uploader("Unggah gambar dari file", type=["png", "jpg", "jpeg"])

# Fungsi untuk menggabungkan baris
def merge_lines(lines):
    merged_text = []
    for i, line in enumerate(lines):
        if i == 0:  # Baris pertama langsung ditambahkan
            merged_text.append(line)
        else:
            # Gabungkan dengan baris sebelumnya jika baris sebelumnya tidak diakhiri tanda baca
            if not re.search(r"[.!?]$", merged_text[-1]):  
                merged_text[-1] += " " + line
            else:
                merged_text.append(line)
    return merged_text

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
        # Gabungkan teks hasil OCR
        raw_text = [res[1] for res in results]
        processed_text = "\n".join(merge_lines(raw_text))  # Proses penggabungan baris
        st.text_area("Hasil Teks Ekstraksi", processed_text, height=200)
    else:
        st.error("Tidak ada teks yang terdeteksi.")
