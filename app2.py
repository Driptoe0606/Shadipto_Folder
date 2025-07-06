import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Data
df = pd.DataFrame({
    'Sample': ['F1', 'F2', 'F3', 'F4'],
    'SPR Peak': [0.757776, 0.013993, 0.017494, 0.493593],
    'Water Peak': [0.021374, 0.050313, 0.031369, 0.009161]
})

# Normalize for color intensity
def normalize(values):
    min_val = min(values)
    max_val = max(values)
    return [(val - min_val) / (max_val - min_val) for val in values]

spr_norm = normalize(df['SPR Peak'])
water_norm = normalize(df['Water Peak'])

spr_colors = [f'rgba(0, 102, 255, {0.4 + 0.6 * alpha})' for alpha in spr_norm]
water_colors = [f'rgba(0, 204, 102, {0.4 + 0.6 * alpha})' for alpha in water_norm]

# Streamlit setup
st.set_page_config(layout="wide")
st.title("Nanoparticles SPR Analysis")

# Create tabs
tab1, tab2 = st.tabs(["📊 Bar Chart", "🔬 Microscope Images"])

# ========== TAB 1 ==========
with tab1:
    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='SPR Peak',
        x=df['Sample'],
        y=df['SPR Peak'],
        marker_color=spr_colors,
        marker_line_width=1,
        marker_line_color='black'
    ))

    fig.add_trace(go.Bar(
        name='Water Peak',
        x=df['Sample'],
        y=df['Water Peak'],
        marker_color=water_colors,
        marker_line_width=1,
        marker_line_color='black'
    ))

    fig.update_layout(
        barmode='group',
        title='SPR vs Water Peak',
        xaxis_title='Sample',
        yaxis_title='Value',
        width=800,
        height=500
    )

    st.dataframe(df.set_index('Sample'))
    st.plotly_chart(fig, use_container_width=True)

# ========== TAB 2 ==========
with tab2:
    st.subheader("Microscope Images of Formulations")

    cols = st.columns(4)

    with cols[0]:
        st.image("F1.png.jpg", caption="F1", use_column_width=True)

    with cols[1]:
        st.image("F2.png.jpg", caption="F2", use_column_width=True)

    with cols[2]:
        st.image("F3.png.jpg", caption="F3", use_column_width=True)

    with cols[3]:
        st.image("F4.png.jpg", caption="F4", use_column_width=True)
