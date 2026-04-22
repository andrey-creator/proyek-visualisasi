import streamlit as st
import cv2
import numpy as np

st.title("Aplikasi Visi Komputer King")
st.write("Streamlit dan OpenCV sudah aktif!")

# Contoh menampilkan versi
st.text(f"Versi OpenCV: {cv2.__version__}")
