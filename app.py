import streamlit as st
from PIL import Image
import numpy as np
import easyocr

st.set_page_config(page_title="Разпознаване на вредни съставки")

st.title("Разпознаване на вредни съставки в храни")

st.write("""
Качи снимка на етикет или направи снимка с камера.
Приложението ще разпознае текста и ще потърси вредни съставки.
""")

harmful_ingredients = {
    "e621": "Мононатриев глутамат",
    "e102": "Тартразин",
    "e250": "Натриев нитрит",
    "палмово масло": "Съдържа наситени мазнини",
    "palm oil": "Contains saturated fats",
    "aspartame": "Изкуствен подсладител",
    "e951": "Аспартам"
}

@st.cache_resource
def load_reader():
    return easyocr.Reader(['bg', 'en'])

reader = load_reader()

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

    image = image.convert("RGB")

    st.image(
        image,
        caption="Избрано изображение",
        use_container_width=True
    )

    image_np = np.array(image)

    with st.spinner("Разпознаване на текста..."):

        try:
            results = reader.readtext(image_np, detail=0)

            extracted_text = " ".join(results)

            st.subheader("Разпознат текст:")
            st.write(extracted_text)

            found = []

            text_lower = extracted_text.lower()

            for ingredient, description in harmful_ingredients.items():
                if ingredient in text_lower:
                    found.append((ingredient, description))

            st.subheader("Открити вредни съставки:")

            if found:
                for ingredient, description in found:
                    st.error(f"{ingredient.upper()} → {description}")
            else:
                st.success("Не са открити известни вредни съставки.")

        except Exception as e:
            st.error(f"Възникна грешка: {e}")
