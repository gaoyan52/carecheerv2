import streamlit as st
from openai import OpenAI
from PIL import Image
import io, base64

st.title("🌟 Care & Cheer App")

client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY"))

uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    # Auto-fix orientation from phone photos
    try:
        image = Image.open(uploaded_file)
        image = image.transpose(Image.Transpose.EXIF)
    except Exception:
        pass
    from PIL import ImageOps
    image = ImageOps.exif_transpose(image)
    st.image(image, caption="Your uploaded image", use_container_width=True)

    img_buffer = io.BytesIO()
    image.save(img_buffer, format="PNG")
    img_str = base64.b64encode(img_buffer.getvalue()).decode("utf-8")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a warm, encouraging assistant."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Look at this image and write a short, uplifting message."},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_str}"}},
                    ],
                },
            ],
            max_tokens=100,
        )
        message = response.choices[0].message.content.strip()
        st.success(message)

    except Exception as e:  # catch all errors from OpenAI API
        st.error(
            "Sorry, we couldn't process your image right now. "
            "You may have reached your usage limit or there was a network/API error."
        )
        print("Error:", e)
