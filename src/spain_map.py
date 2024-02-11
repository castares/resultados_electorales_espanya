import geopandas as gpd
from area_processor import Area


def get_spain_map(area: Area):
    map_file: dict = {
        area.CCAA: "./data/spain_geojson/gadm41_ESP_1.json.zip",
        area.PROVINCIA : "./data/spain_geojson/gadm41_ESP_2.json.zip",
        area.MUNICIPIO : "./data/spain_geojson/gadm41_ESP_3.json.zip",
    }
    gdf_spain = gpd.read_file(map_file[area], encoding="utf-8", driver="GeoJSON")
    if area == area.CCAA:
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
    return gdf_spain
