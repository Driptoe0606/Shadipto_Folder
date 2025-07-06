import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import streamlit.components.v1 as components
import base64
from io import BytesIO

# Set page config
st.set_page_config(page_title="SPR Data Viewer", layout="wide")

# Prepare data
data = {
    'Sample': ['F1', 'F2', 'F3', 'F4'],
    'SPR Peak Avg': [0.757775970, 0.013993325, 0.017494279, 0.493592952],
    'Water Peak Avg': [0.021373751, 0.050313009, 0.031368749, 0.009160527]
}
df_avg = pd.DataFrame(data)

# Tab structure
tab1, tab2 = st.tabs(["📊 SPR Data", "🖼️ Zoomable Images"])

with tab1:
    st.subheader("SPR vs Water Peaks – Averaged")
    fig = px.bar(df_avg, x='Sample', y=['SPR Peak Avg', 'Water Peak Avg'],
                 barmode='group', labels={'value': 'Peak Intensity', 'variable': 'Type'},
                 title="SPR vs Water Peaks")

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Raw Data Table")
    # Construct raw data
    raw_data = {
        'Sample': ['F1', 'F1', 'F1', 'F2', 'F2', 'F2', 'F3', 'F3', 'F3', 'F4', 'F4', 'F4'],
        'SPR Peak': [
            0.756670413, 0.758881526, 0.757775970,
            0.009333486, 0.018653165, 0.013993325,
            0.018995943, 0.015992615, 0.017494279,
            0.496515963, 0.490669940, 0.493592952
        ],
        'Water Peak': [
            0.021538112, 0.02120939, 0.021373751,
            0.049883022, 0.050742997, 0.050313009,
            0.031731754, 0.031005745, 0.031368749,
            0.009061191, 0.009259863, 0.009160527
        ],
        'Wavelength': [392.7]*12
    }
    df_raw = pd.DataFrame(raw_data)
    st.dataframe(df_raw, use_container_width=True)

with tab2:
    st.subheader("Zoomable SPR Images")

    def display_zoom_image(image_path):
        st.markdown(f"#### {image_path}")
        image = Image.open(image_path)
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        data_url = f"data:image/jpeg;base64,{img_str}"
        width, height = image.size  # Get original size

        components.html(f"""
        <style>
            .zoom-container {{
                display: flex;
                align-items: flex-start;
                gap: 40px;
            }}

            .image-box {{
                position: relative;
                display: inline-block;
            }}

            .image-box img {{
                max-width: 100%;
                height: auto;
                display: block;
            }}

            .lens {{
                position: absolute;
                border: 2px solid #000;
                border-radius: 50%;
                width: 120px;
                height: 120px;
                pointer-events: none;
                background: rgba(255, 255, 255, 0.3);
                display: none;
            }}

            .result {{
                border: 2px solid #000;
                border-radius: 50%;
                width: 240px;
                height: 240px;
                overflow: hidden;
                position: relative;
            }}

            .result img {{
                position: absolute;
                transform: scale(2);
                transform-origin: top left;
            }}
        </style>

        <div class="zoom-container">
            <div class="image-box">
                <img id="main-img" src="{data_url}">
                <div class="lens" id="lens"></div>
            </div>
            <div class="result" id="result">
                <img id="zoomed" src="{data_url}">
            </div>
        </div>

        <script>
            const img = document.getElementById("main-img");
            const lens = document.getElementById("lens");
            const zoomed = document.getElementById("zoomed");
            const result = document.getElementById("result");

            img.addEventListener("mousemove", moveLens);
            img.addEventListener("mouseenter", () => lens.style.display = "block");
            img.addEventListener("mouseleave", () => lens.style.display = "none");

            function moveLens(e) {{
                const rect = img.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;

                const lensSize = lens.offsetWidth / 2;
                let lensX = x - lensSize;
                let lensY = y - lensSize;

                lens.style.left = lensX + "px";
                lens.style.top = lensY + "px";

                const scale = 2;
                zoomed.style.left = -(x * scale - result.offsetWidth / 2) + "px";
                zoomed.style.top = -(y * scale - result.offsetHeight / 2) + "px";
            }}
        </script>
        """, height=height // 2 + 260)  # Adjust height dynamically



    for img_name in ["F1.png.jpg", "F2.png.jpg", "F3.png.jpg", "F4.png.jpg"]:
        display_zoom_image(img_name)
