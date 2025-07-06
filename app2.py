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

        components.html(f"""
            <style>
                .container {{
                    position: relative;
                    display: flex;
                    align-items: center;
                    gap: 30px;
                }}
                .zoom-img {{
                    width: 400px;
                    height: 300px;
                    border: 2px solid #ccc;
                }}
                .lens {{
                    position: absolute;
                    border: 2px solid #000;
                    border-radius: 50%;
                    width: 100px;
                    height: 100px;
                    pointer-events: none;
                    overflow: hidden;
                }}
                .result {{
                    border: 2px solid #000;
                    border-radius: 50%;
                    width: 200px;
                    height: 200px;
                    overflow: hidden;
                }}
                .result img {{
                    position: absolute;
                    transform: scale(2);
                }}
            </style>

            <div class="container">
                <div style="position:relative;">
                    <img src="{data_url}" id="img" class="zoom-img">
                    <div class="lens" id="lens"></div>
                </div>
                <div class="result" id="result">
                    <img src="{data_url}" id="zoomed">
                </div>
            </div>

            <script>
                const img = document.getElementById("img");
                const lens = document.getElementById("lens");
                const zoomed = document.getElementById("zoomed");
                const result = document.getElementById("result");

                img.addEventListener("mousemove", moveLens);
                lens.addEventListener("mousemove", moveLens);
                img.addEventListener("mouseleave", () => lens.style.display = "none");

                function moveLens(e) {{
                    const rect = img.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;

                    lens.style.display = "block";
                    lens.style.left = (x - 50) + "px";
                    lens.style.top = (y - 50) + "px";

                    zoomed.style.left = -(x * 2 - 100) + "px";
                    zoomed.style.top = -(y * 2 - 100) + "px";
                }}
            </script>
        """, height=400)


    for img_name in ["F1.png.jpg", "F2.png.jpg", "F3.png.jpg", "F4.png.jpg"]:
        display_zoom_image(img_name)
