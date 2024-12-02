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

# Fungsi untuk menggabungkan baris dengan jarak
def process_ocr_results(results):
    processed_lines = []
    previous_bottom = None

    for res in results:
        text, bbox = res[1], res[0]  # Hasil teks dan bounding box
        _, _, _, bottom = bbox[0][1], bbox[1][1], bbox[2][1], bbox[3][1]
        
        # Jika jarak antar baris jauh, tambahkan baris baru
        if previous_bottom and (bottom - previous_bottom) > 15:  # Sesuaikan threshold 15 sesuai kebutuhan
            processed_lines.append("")  # Tambahkan baris kosong untuk memisah paragraf
        
        # Pastikan angka di awal baris tetap
        if re.match(r"^\d+\.\s*", text):
            processed_lines.append(text)
        else:
            # Gabungkan ke baris sebelumnya jika tidak ada jarak antar baris
            if processed_lines and processed_lines[-1]:
                processed_lines[-1] += " " + text
            else:
                processed_lines.append(text)

        previous_bottom = bottom

    return processed_lines

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
        # Proses hasil OCR dengan jarak antar baris
        processed_lines = process_ocr_results(results)
        final_text = "\n".join(processed_lines)
        st.text_area("Hasil Teks Ekstraksi", final_text, height=200)
    else:
        st.error("Tidak ada teks yang terdeteksi.")
