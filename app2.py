import streamlit as st
import streamlit.components.v1 as components

# Streamlit setup
st.set_page_config(layout="wide")
st.title("Microscope Images with Hover Zoom")

# Tab layout
tab1, tab2 = st.tabs(["📊 Chart (Coming Soon)", "🔬 Microscope Images"])

# Image filenames
image_paths = {
    "F1": "F1.png.jpg",
    "F2": "F2.png.jpg",
    "F3": "F3.png.jpg",
    "F4": "F4.png.jpg"
}

# CSS + JS magnifier template
def magnifier_html(img_src, label):
    return f"""
    <div style="text-align:center; margin: 20px;">
        <h4>{label}</h4>
        <div style="position: relative; display: inline-block;">
            <img id="{label}" src="{img_src}" width="300" style="border: 2px solid #ccc; border-radius: 10px;">
            <div id="lens-{label}" style="
                position: absolute;
                border: 2px solid #000;
                border-radius: 50%;
                width: 100px;
                height: 100px;
                visibility: hidden;
                background-repeat: no-repeat;
                background-size: 600px auto;
                z-index: 10;">
            </div>
        </div>
    </div>

    <script>
    const img_{label} = document.getElementById("{label}");
    const lens_{label} = document.getElementById("lens-{label}");

    img_{label}.addEventListener("mousemove", moveLens_{label});
    lens_{label}.addEventListener("mousemove", moveLens_{label});
    img_{label}.addEventListener("mouseenter", () => lens_{label}.style.visibility = "visible");
    img_{label}.addEventListener("mouseleave", () => lens_{label}.style.visibility = "hidden");

    function moveLens_{label}(e) {{
        const rect = img_{label}.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        lens_{label}.style.left = (x - 50) + "px";
        lens_{label}.style.top = (y - 50) + "px";
        lens_{label}.style.backgroundImage = "url('{img_src}')";
        lens_{label}.style.backgroundPosition = `-${x * 2 - 50}px -${y * 2 - 50}px`;
    }}
    </script>
    """

with tab2:
    st.markdown("### Hover over the images to zoom into microscope details")

    col1, col2 = st.columns(2)

    with col1:
        components.html(magnifier_html(image_paths["F1"], "F1"), height=400)
        components.html(magnifier_html(image_paths["F3"], "F3"), height=400)

    with col2:
        components.html(magnifier_html(image_paths["F2"], "F2"), height=400)
        components.html(magnifier_html(image_paths["F4"], "F4"), height=400)
