import streamlit as st
from ultralytics import YOLO
from PIL import Image
import os
import tempfile
import requests

# ✅ Model URL on Google Drive (ensure shared link is public)
MODEL_URL = "https://drive.google.com/uc?id=1-YJ9n4eoUO-JBcg4BYBmbogrA56F-9FN"
MODEL_PATH = "best.pt"

# 📥 Download model if not already present
def download_model():
    if not os.path.exists(MODEL_PATH):
        st.info("🔄 Downloading YOLOv8 model weights...")
        response = requests.get(MODEL_URL)
        with open(MODEL_PATH, "wb") as f:
            f.write(response.content)
        st.success("✅ Model downloaded successfully!")

# ⚙️ Streamlit page setup
st.set_page_config(page_title="Cocoa Plant + Hole Detector", layout="centered")

st.title("🧠 Cocoa Plant + Hole Detector")
st.markdown("Upload a single aerial image tile and run live YOLOv8 detection on cocoa plants and planting holes.")

# 📥 Download model
download_model()

# 📁 Image uploader
uploaded_file = st.file_uploader("📂 Upload Tile Image", type=["tif", "tiff", "jpg", "jpeg", "png"])

if uploaded_file:
    st.success(f"📥 Uploaded: {uploaded_file.name}")

    # Save file to temp path
    with tempfile.NamedTemporaryFile(delete=False, suffix=".tif") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_image_path = tmp_file.name

    # 🧠 Detection trigger
    if st.button("🚀 Run Detection"):
        with st.spinner("Running YOLOv8 model..."):
            model = YOLO(MODEL_PATH)
            results = model.predict(source=tmp_image_path, conf=0.05, iou=0.73, save=False)
            annotated = results[0].plot()
            st.image(annotated, caption="✅ Detected: Cocoa Plants + Planting Holes", use_container_width=True)

        # Cleanup
        os.remove(tmp_image_path)

st.markdown("---")
st.markdown("🔬 Built with **YOLOv8 + Streamlit**  |  🚀 Project by **Michael Ofeor**")
