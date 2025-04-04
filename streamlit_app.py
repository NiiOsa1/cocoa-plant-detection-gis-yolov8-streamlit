import streamlit as st
from ultralytics import YOLO
from PIL import Image
import os
import tempfile

# 🔍 Correct model path
MODEL_PATH = "/home/nii-osa/Projects/YOLO8/runs/cocoa_yolov8s_phase4_refined/weights/best.pt"

st.set_page_config(page_title="Cocoa Plant + Hole Detector", layout="centered")

st.markdown("## 🧠 Cocoa Plant + Hole Detector")
st.markdown("Upload a single image tile from your field dataset and run YOLOv8 detection live.")

uploaded_file = st.file_uploader("📁 Upload tile (.tif)", type=["tif", "tiff", "jpg", "jpeg", "png"])

if uploaded_file:
    st.success(f"📥 Image uploaded: {uploaded_file.name}")

    # Save to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".tif") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_image_path = tmp_file.name

    # 🔘 Detection Button
    if st.button("🚀 Run Detection"):
        with st.spinner("Running YOLOv8 detection..."):
            model = YOLO(MODEL_PATH)
            results = model.predict(source=tmp_image_path, conf=0.05, iou=0.73, save=False)

            # Plot annotated results
            annotated = results[0].plot()
            st.image(annotated, caption="✅ Detected: Cocoa Plants + Holes", use_container_width=True)

        # 🧹 Clean temp
        os.remove(tmp_image_path)

st.markdown("---")
st.markdown("⚙️ Powered by YOLOv8 + Streamlit | Built by **Michael Ofeor**")
