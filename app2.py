import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Data
df = pd.DataFrame({
    'Sample': ['F1', 'F2', 'F3', 'F4'],
    'SPR Peak': [0.757776, 0.013993, 0.017494, 0.493593],
    'Water Peak': [0.021374, 0.050313, 0.031369, 0.009161]
})

# Normalize values for color intensity (optional but nice for gradient logic)
def normalize(values):
    min_val = min(values)
    max_val = max(values)
    return [(val - min_val) / (max_val - min_val) for val in values]

spr_norm = normalize(df['SPR Peak'])
water_norm = normalize(df['Water Peak'])

# Gradient color scale for each bar (blue for SPR, green for Water)
spr_colors = [f'rgba(0, 102, 255, {0.4 + 0.6 * alpha})' for alpha in spr_norm]
water_colors = [f'rgba(0, 204, 102, {0.4 + 0.6 * alpha})' for alpha in water_norm]

# Plotly grouped bar chart
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
    title='Gradient Bar Chart per Column: SPR vs Water Peak',
    xaxis_title='Sample',
    yaxis_title='Average Value',
    width=800,
    height=500,
    showlegend=True
)

# Streamlit display
st.set_page_config(layout="centered")
st.title("Gradient Bar Chart: Per Column")
st.dataframe(df.set_index('Sample'))
st.plotly_chart(fig, use_container_width=True)
