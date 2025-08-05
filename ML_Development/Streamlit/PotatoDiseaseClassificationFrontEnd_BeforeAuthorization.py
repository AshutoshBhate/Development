import streamlit as st
import requests
from PIL import Image
import numpy as np
import io
import os

# FastAPI Endpoint URL
FASTAPI_URL = "http://localhost:8000/predict" # Assuming FastAPI runs on 8000

#When deploying on Render, we'll get the public URL of deployed FastAPI service after deploying FastAPI backend
# Get the FastAPI URL from an environment variable, with a fallback for local dev
#FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000/predict")

# Set page configuration
st.set_page_config(
    page_title="Potato Disease Classifier",
    page_icon="🥔",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- Background Image (Optional) ---
# To use a background image, place your image (e.g., farmland.jpg) in streamlit_app/assets/
def set_background_image(image_path):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{base64.b64encode(open(image_path, "rb").read()).decode()}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .css-fg4btx {{ /* Targeting specific Streamlit containers for better readability on busy backgrounds */
            background-color: rgba(255, 255, 255, 0.85); /* Slightly transparent white */
            padding: 20px;
            border-radius: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
import base64
try:
    set_background_image("assets/farmland.jpg")
except FileNotFoundError:
    st.warning("Background image 'assets/farmland.jpg' not found. Please place it in the 'streamlit_app/assets/' directory.")


# --- Title and Description ---
st.markdown(
    """
    <div style='display: inline-block; background-color: rgba(0, 0, 0, 0.7); padding: 10px 20px; border-radius: 10px; color: white;'>
        <h1 style='text-align: center; margin-bottom: 5px;'>🥔 Potato Disease Classification</h1>
        <p style='text-align: center; margin: 0;'>Upload an image of a potato leaf to predict if it's healthy or has Early Blight or Late Blight.</p>
    </div>
    """,
    unsafe_allow_html=True
)
st.write("---")

# --- File Uploader ---
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image')
    st.write("")
    st.write("Classifying...")

    # Prepare image for sending to FastAPI
    # Ensure the image is in RGB format if it's not already (e.g., PNGs can be RGBA)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Save image to a BytesIO object
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG') # Use JPEG for consistency and smaller size
    img_byte_arr = img_byte_arr.getvalue()

    # Send image to FastAPI for prediction
    files = {'file': (uploaded_file.name, img_byte_arr, "image/jpeg")}
    try:
        with st.spinner('Making prediction...'):
            response = requests.post(FASTAPI_URL, files=files)
            response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
            json_response = response.json()

        predicted_class = json_response.get("class")
        confidence = json_response.get("confidence")

        if predicted_class and confidence is not None:
            st.success(f"**Prediction: {predicted_class}**")
            st.info(f"**Confidence: {confidence}**")
        else:
            st.error("Invalid response from the API. Missing 'class' or 'confidence'.")

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the FastAPI server. Please ensure FastAPI is running.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with the FastAPI server: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred during prediction: {e}")

st.write("---")
st.markdown("Developed by Ashutosh Bhate")