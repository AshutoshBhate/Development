# File: streamlit_app/app.py

import streamlit as st
import requests
from PIL import Image
import io
from datetime import datetime

# --- Configuration ---
# These URLs should point to your running FastAPI application.
# The '/login' endpoint comes from your auth.py router.
# The '/predictions' endpoint comes from your prediction.py router.
API_BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{API_BASE_URL}/login"
PREDICTIONS_URL = f"{API_BASE_URL}/predictions"

# --- Page Configuration ---
st.set_page_config(
    page_title="Potato Disease Classifier",
    page_icon="🥔",
    layout="wide"
)

# --- Session State Initialization ---
# We use st.session_state to store the authentication token
# so the user stays logged in as they navigate the app.
if 'token' not in st.session_state:
    st.session_state.token = None
if 'username' not in st.session_state:
    st.session_state.username = None

# --- Main App ---
st.title("🥔 Potato Disease Classification Portal")
st.markdown("---")

# --- Authentication UI (Sidebar) ---
st.sidebar.title("👤 User Authentication")

# Display Login form if user is not logged in
if st.session_state.token is None:
    st.sidebar.subheader("Please Log In")
    email = st.sidebar.text_input("Email", key="login_email")
    password = st.sidebar.text_input("Password", type="password", key="login_password")
    
    if st.sidebar.button("Login"):
        # FastAPI's OAuth2PasswordRequestForm expects form data, not JSON
        login_data = {'username': email, 'password': password}
        try:
            response = requests.post(LOGIN_URL, data=login_data)
            
            if response.status_code == 200:
                # If login is successful, store the token and username
                st.session_state.token = response.json()['access_token']
                st.session_state.username = email
                st.sidebar.success("Login successful!")
                st.rerun() # Rerun the app to show the main content
            else:
                st.sidebar.error(f"Login Failed: {response.json().get('detail', 'Invalid credentials')}")
        except requests.exceptions.RequestException:
            st.sidebar.error("Connection failed. Is the API server running?")

# --- Main Content and Logout (if user is logged in) ---
if st.session_state.token:
    st.sidebar.success(f"Logged in as: {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.session_state.username = None
        st.rerun() # Rerun to go back to the login screen

    # Use columns for a better layout
    col1, col2 = st.columns([1, 1])

    # --- Column 1: Prediction ---
    with col1:
        st.header("🔬 Make a New Prediction")
        uploaded_file = st.file_uploader("Choose a potato leaf image...", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image.', use_column_width=True)
            
            if st.button("Classify Image"):
                with st.spinner('Analyzing the leaf...'):
                    img_byte_arr = io.BytesIO()
                    image.convert('RGB').save(img_byte_arr, format='JPEG')
                    files = {'file': (uploaded_file.name, img_byte_arr.getvalue(), "image/jpeg")}
                    
                    # This is the crucial part: add the Authorization header
                    headers = {"Authorization": f"Bearer {st.session_state.token}"}

                    try:
                        response = requests.post(PREDICTIONS_URL, files=files, headers=headers)
                        if response.status_code == 200:
                            result = response.json()
                            st.success(f"**Prediction: {result['predicted_class']}**")
                            # The confidence in your API is a float from 0 to 1
                            confidence_percent = result['confidence'] * 100
                            st.info(f"**Confidence:** {confidence_percent:.2f}%")
                        else:
                            st.error(f"Prediction failed: {response.json().get('detail')}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"API Error: {e}")

    # --- Column 2: History ---
    with col2:
        st.header("📜 Your Prediction History")
        
        # We add a button to manually refresh the history
        if st.button("Refresh History"):
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            try:
                response = requests.get(PREDICTIONS_URL, headers=headers)
                if response.status_code == 200:
                    history = response.json()
                    if not history:
                        st.info("You have no predictions yet.")
                    else:
                        # Display each history item in a neat, expandable box
                        for item in reversed(history): # Show newest first
                            dt_object = datetime.fromisoformat(item['timestamp'])
                            formatted_date = dt_object.strftime("%B %d, %Y at %I:%M %p")
                            with st.expander(f"Prediction from {formatted_date}"):
                                st.write(f"**Result:** {item['predicted_class']}")
                                st.write(f"**Confidence:** {item['confidence']*100:.2f}%")
                                st.write(f"**Original Filename:** {item['filename']}")
                else:
                    st.error(f"Failed to fetch history: {response.json().get('detail')}")
            except requests.exceptions.RequestException as e:
                st.error(f"API Error: {e}")

else:
    # This message is shown when the user is not logged in
    st.info("👋 Welcome! Please log in using the sidebar to access the classifier.")