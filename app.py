
import re
import numpy as np
import streamlit as st
from PIL import Image, ImageEnhance
from papaddleocr import PaddleOCR

st.set_page_config(page_title="Food Ingredients Analyzer", layout="centered")

translations = {
    "bg": {
        "title": "AI Анализатор на Хранителни Съставки",
        "upload": "Качи снимка на етикет",
        "camera": "Снимай с камера",
        "analyze": "Анализирай",
        "detected": "Разпознат текст",
        "harmful": "Открити потенциално вредни съставки",
        "none": "Няма открити вредни съставки",
        "error": "Не беше открит текст",
        "language": "Изберете език"
    },
    "en": {
        "title": "AI Food Ingredients Analyzer",
        "upload": "Upload food label image",
        "camera": "Take a photo",
        "analyze": "Analyze",
        "detected": "Detected text",
        "harmful": "Potentially harmful ingredients found",
        "none": "No harmful ingredients detected",
        "error": "No text detected",
        "language": "Choose language"
    }
}

harmful_ingredients = {
    "E102": "Tartrazine",
    "E110": "Sunset Yellow",
    "E124": "Ponceau 4R",
    "E129": "Allura Red",
    "E211": "Sodium Benzoate",
    "E220": "Sulfur Dioxide",
    "E250": "Sodium Nitrite",
    "E621": "Monosodium Glutamate",
    "palm oil": "Palm Oil",
    "high fructose corn syrup": "High Fructose Corn Syrup",
    "aspartame": "Aspartame",
    "ацесулфам": "Acesulfame",
    "палмово масло": "Palm Oil",
    "аспартам": "Aspartame",
    "натриев нитрит": "Sodium Nitrite",
    "мононатриев глутамат": "MSG"
}

language = st.selectbox("Language / Език", ["bg", "en"])
text_data = translations[language]

st.title(text_data["title"])

uploaded_file = st.file_uploader(text_data["upload"], type=["png", "jpg", "jpeg"])
camera_image = st.camera_input(text_data["camera"])

image_source = None

if uploaded_file is not None:
    image_source = uploaded_file
elif camera_image is not None:
    image_source = camera_image

@st.cache_resource

def load_reader():
    return paddleocrCR(use_angle_cls=True, lang="en")

reader = load_reader()

if image_source is not None:
    image = Image.open(image_source).convert("RGB")

    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)

    st.image(image, caption="Image", use_container_width=True)

    if st.button(text_data["analyze"]):
        image_np = np.array(image)
        results = reader.ocr(image_np, cls=True)

        extracted = []

        for line in results:
            for item in line:
                extracted.append(item[1][0])

        extracted_text = " ".join(extracted)

        if extracted_text.strip() == "":
            st.error(text_data["error"])
        else:
            st.subheader(text_data["detected"])
            st.text_area("", extracted_text, height=200)

            found = []
            lower_text = extracted_text.lower()

            for ingredient, description in harmful_ingredients.items():
                pattern = re.escape(ingredient.lower())
                if re.search(pattern, lower_text):
                    found.append(f"{ingredient} - {description}")

            st.subheader(text_data["harmful"])

            if found:
                for item in found:
                    st.warning(item)
            else:
                st.success(text_data["none"])
