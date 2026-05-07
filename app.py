import streamlit as st
from PIL import Image
import numpy as np
from paddleocr import PaddleOCR

ocr = PaddleOCR(lang='en')

result = ocr.ocr("image.png")

for line in result[0]:
    print(line[1][0])

st.title("Разпознаване на вредни съставки в храни")

st.write("""
Качи снимка на етикет или направи снимка с камера.
Приложението ще разпознае текста и ще потърси вредни съставки.
""")

harmful_ingredients = {
    "E621": "Мононатриев глутамат",
    "E102": "Тартразин",
    "E250": "Натриев нитрит",
    "палмово масло": "Съдържа наситени мазнини",
    "palm oil": "Contains saturated fats",
    "aspartame": "Изкуствен подсладител",
    "E951": "Аспартам"
}

uploaded_file = st.file_uploader(
    "Качи изображение",
    type=["jpg", "jpeg", "png"]
)

camera_image = st.camera_input("Или направи снимка")

image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)

elif camera_image is not None:
    image = Image.open(camera_image)

if image is not None:

    st.image(image, caption="Избрано изображение", use_container_width=True)

    image_np = np.array(image)

    reader = easyocr.Reader(['bg', 'en'])

    results = reader.readtext(image_np, detail=0)

    extracted_text = " ".join(results)

    st.subheader("Разпознат текст:")
    st.write(extracted_text)

    found = []

    text_lower = extracted_text.lower()

    for ingredient, description in harmful_ingredients.items():
        if ingredient.lower() in text_lower:
            found.append((ingredient, description))

    st.subheader("Открити вредни съставки:")

    if found:
        for ingredient, description in found:
            st.error(f"{ingredient} -> {description}")
    else:
        st.success("Не са открити известни вредни съставки.")
