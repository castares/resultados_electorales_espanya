from enum import Enum
from typing import Optional

from pandas import DataFrame


class Area(str, Enum):
    CCAA = "Comunidad Autónoma"
    PROVINCIA = "Provincia"
    MUNICIPIO = "Municipio"


# CCAA = {
#     "name": "Comunidad Autónoma",
#     "field_value": "Nombre de Comunidad",
#     "map_file": "./data/spain_geojson/gadm41_ESP_1.json.zip",
# }
# PROVINCIA = {
#     "name": "Provincia",
#     "field_value": "Nombre de Provincia",
#     "map_file": "./data/spain_geojson/gadm41_ESP_2.json.zip",
#         }
# MUNICIPIO = {
#     "name": "Municipio",
#     "field_value": "Nombre de Municipio",
#     "map_file": "./data/spain_geojson/gadm41_ESP_3.json.zip",
#         }


class AreaProcessor:
    def data_by_area(self, data: DataFrame, area: Area):
        if area == Area.CCAA:
            # TODO: Separate Ceuta & Melilla multipolygons
            data = data.drop(
                data[data["Nombre de Comunidad"] == "Ciudad de Ceuta"].index
            )
            data = data.drop(
                data[data["Nombre de Comunidad"] == "Ciudad de Melilla"].index
            )
            data.sort_values(by=["Nombre de Comunidad"], ascending=False)
            data["Nombre de Comunidad"] = data["Nombre de Comunidad"].str.replace(
                " ", ""
            )
            data = data.rename(
                columns={"Nombre de Comunidad": "Comunidad Autónoma"},
                errors="raise",
            )
        elif area == Area.PROVINCIA:
            data = data.rename(
                columns={"Nombre de Provincia": "Provincia"},
                errors="raise",
            )
        elif area == Area.MUNICIPIO:
            data = data.rename(
                columns={"Nombre de Municipio": "Municipio"},
                errors="raise",
            )
        else:
            raise NameError("Area is not valid. Please select valid area.")

        data_by_area = data.groupby(by=[area.value]).sum(numeric_only=True)
        return data_by_area
