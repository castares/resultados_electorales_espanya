from enum import Enum
import streamlit as st
from pandas import DataFrame
from geopandas import GeoDataFrame
import altair as alt
import plotly.express as px

from data_selector import DataSelector, Election
from area_processor import Area, AreaProcessor
from results_calculator import ResultsCalculator, ElectoralSystem, TotalSeats
from spain_map import get_spain_map


def _display_enum_value(option: Enum) -> str:
    return option.value


left_sidebar = st.sidebar

with left_sidebar:

    option_elecciones = st.selectbox(
        label="Selecciona unas elecciones",
        options=(election for election in Election),
        format_func=_display_enum_value,
    )
    option_area = st.selectbox(
        label="Selecciona una granularidad",
        options=(area for area in Area),
        format_func=_display_enum_value,
    )
    option_algorithm = st.selectbox(
        label="Selecciona un sistema electoral",
        options=(algorithm for algorithm in ElectoralSystem),
        format_func=_display_enum_value,
    )

data_selector: DataSelector = DataSelector()
area_processor: AreaProcessor = AreaProcessor()
results_calculator: ResultsCalculator = ResultsCalculator()

election_data: DataFrame = data_selector.select_data(option_elecciones)
area_data = area_processor.data_by_area(election_data, option_area)
data: DataFrame = results_calculator.compute_results(
    area_data, option_algorithm, TotalSeats.CONGRESO
)

area_field_value = area_processor.area_field_value

# TODO: extract to a module
spain_map: GeoDataFrame = get_spain_map(option_area)

if option_area == Area.CCAA:
    data = data.drop(data[data["Nombre de Comunidad"] == "Ciudad de Ceuta"].index)
    data = data.drop(data[data["Nombre de Comunidad"] == "Ciudad de Melilla"].index)
    data.sort_values(by=["Nombre de Comunidad"], ascending=False)
    data["Nombre de Comunidad"] = data["Nombre de Comunidad"].str.replace(" ", "")

data = GeoDataFrame(
    data.merge(
        spain_map,
        how="left",
        left_on=area_field_value,
        right_on="NAME_1",
    )
)
data = data.drop(columns="NAME_1")

dimensions_columns = [
    "Nombre de Comunidad",
    "Nombre de Provincia",
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

with left_sidebar:

    selected_candidatures = st.multiselect(
        "Selecciona Candidaturas", candidatures_columns, default=candidatures_columns
    )


st.header("Resultados por Candidatura")

st.dataframe(data[candidatures_columns], use_container_width=True)

# st.bar_chart(
#     data,
#     y=selected_candidatures,
#     x=area_field_value,  # color=["#ff2d00", "#0400ff"]
# )


st.header(f"Ganadores por {option_area}")

breakpoint()

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
        color=alt.Color(field=area_field_value, type="nominal"),
    )
    .properties(title="PSOE por Comunidad")
)


st.altair_chart(arc, use_container_width=True, theme="streamlit")
