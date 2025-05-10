import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image
from utils.llm_parser import smart_extract_with_llm  # updated import

# Set Tesseract path if not in PATH
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Poppler path
POPPLER_PATH = r"C:\Program Files\poppler-24.08.0\Library\bin"

st.set_page_config(page_title="Document Extractor", layout="wide")
st.title("📄 Gas Station Document OCR + LLM Extraction")
st.markdown("---")

uploaded_file = st.file_uploader("Upload a scanned PDF or image", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file:
    st.info("Processing and extracting text...")

    images = convert_from_bytes(uploaded_file.read(), poppler_path=POPPLER_PATH) if uploaded_file.name.endswith(".pdf") else [Image.open(uploaded_file)]

    for i, img in enumerate(images):
        st.subheader(f"📄 Page {i + 1}")
        col1, col2 = st.columns([1, 2])

        with col1:
            st.image(img, caption="Scanned Page", use_column_width=True)

        with col2:
            text = pytesseract.image_to_string(img)
            st.text_area("🧾 Extracted Text", text, height=400)

            st.markdown("### 🤖 Smart Extracted Fields (LLM)")
            with st.spinner("Extracting structured fields..."):
                structured = smart_extract_with_llm(text)
            st.json(structured)
