import streamlit as st
from pandas import DataFrame

from main import main

data: DataFrame = main()

st.dataframe(data)

st.bar_chart(
    data, y=["PSOE", "PP"], x="Nombre de Comunidad", color=["#ff2d00", "#0400ff"]
)
