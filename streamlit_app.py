import base64
import streamlit as st
from openai import OpenAI
from PIL import Image
import io

st.set_page_config(page_title="Care & Cheer App", page_icon="🌟", layout="centered")
st.title("🌟 Care & Cheer App")
st.write("Upload your selfie or photo to receive an encouraging message tailored to the image!")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Your uploaded image", use_container_width=True)

    # Convert image to base64 string
    img_buffer = io.BytesIO()
    image.save(img_buffer, format="PNG")
    img_str = base64.b64encode(img_buffer.getvalue()).decode("utf-8")

    with st.spinner("Analyzing your image with AI... 🌈"):
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # or "gpt-4o"
            messages=[
                {
                    "role": "system",
                    "content": "You are a warm, friendly assistant that gives positive and encouraging messages based on an image."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Look at this image and write a short, uplifting message that relates to what you see."},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{img_str}"}
                        },
                    ],
                },
            ],
            max_tokens=100,
        )

    message = response.choices[0].message.content.strip()
    st.success(message)
