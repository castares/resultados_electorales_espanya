import streamlit as st
from pandas import DataFrame

from main import main

data: DataFrame = main()

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

candidatures_columns = [
    column
    for column in data.columns
    if column not in dimensions_columns + global_metrics_columns
]


st.dataframe(data)

selected_columns = st.sidebar.multiselect('Select Columns', candidatures_columns)

st.bar_chart(
    data, y=selected_columns, x="Nombre de Comunidad", #color=["#ff2d00", "#0400ff"]
)
