import geopandas as gpd
from area_processor import Area


def get_spain_map(area: Area):
    map_file: dict = {
        area.CCAA: "./data/spain_geojson/gadm41_ESP_1.json.zip",
        area.PROVINCIA: "./data/spain_geojson/gadm41_ESP_2.json.zip",
        # area.COMARCA: "./data/spain_geojson/gadm41_ESP_3.json.zip",
        area.MUNICIPIO: "./data/spain_geojson/gadm41_ESP_4.json.zip",
    }
    gdf_spain = gpd.read_file(map_file[area], encoding="utf-8", driver="GeoJSON")
    if area == Area.CCAA:
        gdf_spain.sort_values(by=["NAME_1"])
        gdf_spain = gdf_spain.drop(
            gdf_spain[gdf_spain["NAME_1"] == "CeutayMelilla"].index
        ).reset_index()
        gdf_spain = gdf_spain[["NAME_1", "geometry"]]
        gdf_spain = gdf_spain.replace(
            {
                "IslasCanarias": "Canarias",
                "IslasBaleares": "IllesBalears",
                "ComunidadValenciana": "ComunitatValenciana",
            }
        )

        gdf_spain = gdf_spain[["NAME_1", "geometry"]]
        gdf_spain = gdf_spain.rename(
            columns={"NAME_1": "Comunidad Autónoma"},
            errors="raise",
        )
    elif area == Area.PROVINCIA:
        gdf_spain = gdf_spain[["NAME_2", "geometry"]]
        gdf_spain = gdf_spain.rename(
            columns={"NAME_2": "Provincia"},
            errors="raise",
        )
    elif area == Area.MUNICIPIO:
        gdf_spain = gdf_spain[["NAME_3", "geometry"]]
        gdf_spain = gdf_spain.rename(
            columns={"NAME_3": "Municipio"},
            errors="raise",
        )
    else:
        raise NameError("Area is not valid. Please select valid area.")

    return gdf_spain
