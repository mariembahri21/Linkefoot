import streamlit as st
import cv2
import numpy as np
from PIL import Image
from keras_facenet import FaceNet
import joblib

# Charger le modèle et l'extracteur d'embeddings une seule fois
def charger_modele_et_embedder():
    embedder = FaceNet()
    modele = joblib.load("models/facial_recognition_svm.pkl")
    return embedder, modele

embedder, modele = charger_modele_et_embedder()

def display():
    st.title("🧠 Reconnaissance Faciale : Identifier un Joueur de Football")
    st.markdown("Téléversez une image avec un **visage bien visible de face** pour identifier le joueur.")

    fichier_televerse = st.file_uploader("📤 Téléverser une image", type=["jpg", "jpeg", "png"])

    if fichier_televerse is not None:
        # Afficher l'image téléversée
        image = Image.open(fichier_televerse).convert("RGB")
        st.image(image, caption="Image Téléversée", use_column_width=True)

        # Conversion en format OpenCV
        img_cv = np.array(image)
        img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)

        # Extraire le visage et prédire
        visages = embedder.extract(img_cv, threshold=0.95)

        if not visages:
            st.error("❌ Aucun visage détecté. Veuillez téléverser une image plus claire.")
        else:
            embedding = visages[0]['embedding']
            prediction = modele.predict([embedding])[0]
            proba = modele.predict_proba([embedding])[0]
            confiance = np.max(proba)

            st.success(f"✅ Joueur identifié : **{prediction}**")
            st.write(f"Confiance : **{confiance*100:.2f}%**")
