import streamlit as st
from geopandas import GeoDataFrame
import altair as alt
import plotly.express as px

from main import main

data: GeoDataFrame = main()

dimensions_columns = [
    "Nombre de Comunidad",
    "Código de Provincia",
    "Código de Municipio",
    "Población",
    "Número de mesas",
    "Total censo electoral",
    "Total votantes",
    "Votos válidos",
    "Votos a candidaturas",
    "Votos en blanco",
    "Votos nulos",
]

global_metrics_columns = [
    "Número de mesas",
    "Total censo electoral",
    "Total votantes",
    "Votos válidos",
    "Votos a candidaturas",
    "Votos en blanco",
    "Votos nulos",
]

algorithm_columns = [
    "votes/quota",
    "automatic_seats",
    "remainder",
    "highest_remainder_seats",
    "total_seats",
]

geom_columns = ["geometry"]

candidatures_columns = [
    column
    for column in data.columns
    if column
    not in dimensions_columns
    + global_metrics_columns
    + algorithm_columns
    + geom_columns
]


st.title("Resultados Electorales de España. Elecciones Generales 2019")

with st.sidebar:
    selected_candidatures = st.multiselect(
        "Selecciona Candidaturas", candidatures_columns, default=candidatures_columns
    )


st.header("Resultados por Candidatura")

st.dataframe(data[candidatures_columns], use_container_width=True)

st.bar_chart(
    data,
    y=selected_candidatures,
    x="Nombre de Comunidad",  # color=["#ff2d00", "#0400ff"]
)


st.header("Ganadores por Comunidad Autónoma")

data["Winner"] = data[selected_candidatures].idxmax(axis=1)

geojson = data._to_geo()

winners_map = px.choropleth_mapbox(
    data[["Winner"]].reset_index(),
    geojson=geojson,
    locations="index",
    color="Winner",
    color_continuous_scale="Viridis",
    range_color=(0, 12),
    mapbox_style="carto-positron",
    zoom=4,
    center={"lat": 40.416775, "lon": -3.703790},
    opacity=0.8,
    labels={"unemp": "unemployment rate"},
)
winners_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

st.plotly_chart(winners_map)

data_wo_geometry = data.drop(columns="geometry")

arc = (
    alt.Chart(data_wo_geometry)
    .mark_arc(
        innerRadius=50,
    )
    .encode(
        theta=alt.Theta(field="PSOE", type="quantitative"),
        color=alt.Color(field="Nombre de Comunidad", type="nominal"),
    )
    .properties(title="PSOE por Comunidad")
)


st.altair_chart(arc, use_container_width=True, theme="streamlit")
