import streamlit as st
import cv2
import numpy as np
from PIL import Image
from keras_facenet import FaceNet
import joblib

# Load model and embedder once
def load_model_and_embedder():
    embedder = FaceNet()
    model = joblib.load("models/facial_recognition_svm.pkl")
    return embedder, model

embedder, model = load_model_and_embedder()

def display():
    st.title("🧠 Facial Recognition: Identify Football Players")
    st.markdown("Upload an image with a **clear front-facing face** to identify the football player.")

    uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Show the uploaded image
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Convert to OpenCV format
        img_cv = np.array(image)
        img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)

        # Extract face and predict
        faces = embedder.extract(img_cv, threshold=0.95)

        if not faces:
            st.error("❌ No face detected. Please upload a clearer image.")
        else:
            embedding = faces[0]['embedding']
            prediction = model.predict([embedding])[0]
            proba = model.predict_proba([embedding])[0]
            confidence = np.max(proba)

            st.success(f"✅ Identified: **{prediction}**")
            st.write(f"Confidence: **{confidence*100:.2f}%**")
