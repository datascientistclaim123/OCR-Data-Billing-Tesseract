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

# Fungsi untuk memisahkan baris berdasarkan jarak antar koordinat
def split_by_spacing(results, threshold=20):
    """
    Memisahkan baris berdasarkan jarak antar koordinat y hasil OCR.
    """
    lines = []
    current_line = [results[0][1]]  # Mulai dari teks pertama
    prev_bottom = results[0][0][2][1]  # Koordinat y dari baris pertama

    for box, text, _ in results[1:]:
        top = box[0][1]  # Koordinat y atas dari baris berikutnya
        if top - prev_bottom > threshold:  # Jika jaraknya melebihi ambang batas
            lines.append(" ".join(current_line))
            current_line = [text]  # Mulai baris baru
        else:
            current_line.append(text)  # Gabungkan ke baris yang sama
        prev_bottom = box[2][1]  # Perbarui koordinat y bawah

    # Tambahkan baris terakhir
    if current_line:
        lines.append(" ".join(current_line))

    return lines

# Fungsi untuk memperbaiki format angka list (1., 2., 3., dst.)
def restore_numbering(lines):
    numbered_lines = []
    for line in lines:
        # Menambahkan kembali angka list jika terdeteksi hilang
        line = re.sub(r"(?<!\d\.)\b(\d)\b", r"\1.", line)  # Menambahkan titik setelah angka
        numbered_lines.append(line)
    return numbered_lines

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
        # Pisahkan baris berdasarkan jarak antar baris
        lines = split_by_spacing(results)

        # Perbaiki format angka list
        final_text = "\n".join(restore_numbering(lines))

        # Tampilkan hasil akhir di Streamlit
        st.text_area("Hasil Teks Ekstraksi", final_text, height=200)
    else:
        st.error("Tidak ada teks yang terdeteksi.")
