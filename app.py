import streamlit as st
import pandas as pd
import altair as alt

# Sample data
data = {
    'F1': pd.DataFrame({
        'SPR Peak': [0.756670413, 0.758881526, 0.75777597],
        'Wavelength': [392.7, 392.7, 'F1'],
        'Water Peak': [0.021538112, 0.02120939, 0.021373751],
        'Label': ['Trial 1', 'Trial 2', 'Average']
    }),
    'F2': pd.DataFrame({
        'SPR Peak': [0.009333486, 0.018653165, 0.013993325],
        'Wavelength': [392.7, 392.7, 'F2'],
        'Water Peak': [0.049883022, 0.050742997, 0.050313009],
        'Label': ['Trial 1', 'Trial 2', 'Average']
    }),
    'F3': pd.DataFrame({
        'SPR Peak': [0.018995943, 0.015992615, 0.017494279],
        'Wavelength': [392.7, 392.7, 'F3'],
        'Water Peak': [0.031731754, 0.031005745, 0.031368749],
        'Label': ['Trial 1', 'Trial 2', 'Average']
    }),
    'F4': pd.DataFrame({
        'SPR Peak': [0.496515963, 0.49066994, 0.493592952],
        'Wavelength': [392.7, 392.7, 'F4'],
        'Water Peak': [0.009061191, 0.009259863, 0.009160527],
        'Label': ['Trial 1', 'Trial 2', 'Average']
    }),
}

st.set_page_config(layout="wide")
st.title("SPR and Water Peak Measurements")

# Create tabs for each sample
tabs = st.tabs([f"Sample {key}" for key in data.keys()])

for tab, key in zip(tabs, data.keys()):
    with tab:
        df = data[key]

        st.subheader(f"Sample {key} Data")
        st.dataframe(df.drop(columns=['Wavelength']), use_container_width=True)

        # Plot chart comparing SPR and Water Peak
        df_long = df.melt(id_vars='Label', value_vars=['SPR Peak', 'Water Peak'],
                          var_name='Measurement', value_name='Value')

        chart = alt.Chart(df_long).mark_bar().encode(
            x=alt.X('Label:N', title="Trial"),
            y=alt.Y('Value:Q'),
            color='Measurement:N',
            column='Measurement:N'
        ).properties(
            width=150,
            height=300
        )

        st.altair_chart(chart)

        # Display average values
        avg_row = df[df['Label'] == 'Average']
        st.info(f"**Averages for {key}** — SPR Peak: {avg_row['SPR Peak'].values[0]:.6f}, "
                f"Water Peak: {avg_row['Water Peak'].values[0]:.6f}")
