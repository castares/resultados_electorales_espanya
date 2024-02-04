import geopandas as gpd

def get_spain_map():
    gdf_spain = gpd.read_file(
        "./data/spain_geojson/gadm41_ESP_1.json.zip", encoding="utf-8", driver="GeoJSON"
    )
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
