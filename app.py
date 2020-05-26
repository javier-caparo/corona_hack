import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px

url_filename = 'https://aws-corona-hack-fallecidos-cdc.s3.amazonaws.com/fallecidos_cdc_con_ubigeo_normalizado.csv'
df = pd.read_csv(url_filename)
st.title("LIMA: Total de fallecidos x CoViD-19")
st.markdown("Fecha de Recopilacion: 25-05-2020")
st.markdown("Fuente: https://www.datosabiertos.gob.pe/search/field_topic/covid-19-917")
st.markdown('---')
if st.checkbox("Mostrar 5 primeros datos", False):
    st.write(df.head(5))

df_lima = df[df['provincia'] == 'LIMA']
#df = df.dropna(subset=['LAT_DEP', 'LON_DEP'], inplace=True)
#st.write(df.head())

try:
    ALL_LAYERS = {
        "Total Fallecidos x LIMA METRO": pdk.Layer(
            "HexagonLayer",
            data=df_lima[['provincia','distrito','latitud','longitud']],
            get_position=["longitud", "latitud"],
            auto_highlight=True,
            elevation_scale=100,
            radius=500,
            pickable=True,
           elevation_range=[0, 1000],
            extruded=True,
            coverage=1
                ),
    }

except urllib.error.URLError as e:
    st.error("""
        **This demo requires internet access.**

        Connection error: %s
    """ % e.reason)

lima_view_state = pdk.ViewState(
    longitude=-77.044,
    latitude=-12.020,
    zoom=8,
    min_zoom=6,
    max_zoom=20,
    pitch=40.5,
    bearing=-27.36)

st.sidebar.markdown('### Map Layers')
selected_layers = [
    layer for layer_name, layer in ALL_LAYERS.items()
    if st.sidebar.checkbox(layer_name, True)]
if selected_layers:
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v9",
        initial_view_state= lima_view_state,
        layers=selected_layers,
    ))
    st.write(df_lima.groupby('provincia')['distrito'].value_counts())
    
    st.header("Histograma x  Distrito y Sexo - fallecidos")
    fig = px.histogram  (df_lima, x="distrito", y='sexo', histfunc="count", color="sexo", template="plotly_dark" )
    st.write(fig)
else
    st.error("Please choose at least one layer above.")


st.markdown('---')
st.markdown("Developer: javier.caparo@gmail.com")