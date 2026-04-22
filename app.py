import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Judul Aplikasi
st.title("King's Vision: Image Processor")
st.subheader("Aplikasi pengolah gambar sederhana dengan OpenCV")

# Widget Upload Gambar
uploaded_file = st.file_uploader("Pilih gambar...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Mengonversi file upload ke format yang dimengerti OpenCV
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    
    # OpenCV menggunakan format BGR, sedangkan PIL menggunakan RGB
    # Kita perlu konversi agar warnanya tidak aneh
    img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    col1, col2 = st.columns(2)

    with col1:
        st.image(image, caption="Gambar Asli", use_container_width=True)

    # Logika Pengolahan Gambar
    st.sidebar.header("Pengaturan")
    mode = st.sidebar.selectbox("Pilih Efek:", ["Original", "Grayscale", "Canny Edge Detection"])

    if mode == "Grayscale":
        processed_img = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        st_image = processed_img # Streamlit bisa baca grayscale langsung
    elif mode == "Canny Edge Detection":
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        processed_img = cv2.Canny(gray, 100, 200)
        st_image = processed_img
    else:
        st_image = image

    with col2:
        st.image(st_image, caption=f"Hasil: {mode}", use_container_width=True)
        
    st.success("Proses Berhasil!")