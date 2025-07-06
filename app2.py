import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Data
df = pd.DataFrame({
    'Sample': ['F1', 'F2', 'F3', 'F4'],
    'SPR Peak': [0.757776, 0.013993, 0.017494, 0.493593],
    'Water Peak': [0.021374, 0.050313, 0.031369, 0.009161]
})

# Plotly grouped bar chart with dotted pattern
fig = go.Figure()

fig.add_trace(go.Bar(
    name='SPR Peak',
    x=df['Sample'],
    y=df['SPR Peak'],
    marker=dict(
        color='rgba(0,102,255,0.6)',
        pattern=dict(
            shape="dot",
            fgcolor="rgba(0,0,0,0.4)",
            size=6,
            solidity=0.1
        ),
        line=dict(color='black', width=1)
    )
))

fig.add_trace(go.Bar(
    name='Water Peak',
    x=df['Sample'],
    y=df['Water Peak'],
    marker=dict(
        color='rgba(0,204,102,0.6)',
        pattern=dict(
            shape="dot",
            fgcolor="rgba(0,0,0,0.4)",
            size=6,
            solidity=0.1
        ),
        line=dict(color='black', width=1)
    )
))

fig.update_layout(
    barmode='group',
    title='Bar Chart with Dotted Pattern: SPR vs Water Peak',
    xaxis_title='Sample',
    yaxis_title='Average Value',
    width=800,
    height=500,
    showlegend=True
)

# Streamlit display
st.set_page_config(layout="centered")
st.title("Bar Chart with Dot Pattern Fill")
st.dataframe(df.set_index('Sample'))
st.plotly_chart(fig, use_container_width=True)
