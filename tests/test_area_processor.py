import pytest
from src.area_processor import AreaProcessor, Area
from src.data_selector import DataSelector, Election
from pandas import DataFrame


@pytest.fixture(scope="module")
def data() -> DataSelector:
    data_selector = DataSelector()
    return data_selector.select_data(Election.CONGRESO_2019)


@pytest.fixture(scope="module")
def area_processor() -> AreaProcessor:
    return AreaProcessor()


@pytest.fixture()
def index_by_area() -> dict:
    return {
        Area.CCAA: [
            "Andalucía                     ",
            "Aragón                        ",
            "Canarias                      ",
            "Cantabria                     ",
            "Castilla - La Mancha          ",
            "Castilla y León               ",
            "Cataluña                      ",
            "Ciudad de Ceuta               ",
            "Ciudad de Melilla             ",
            "Comunidad Foral de Navarra    ",
            "Comunidad de Madrid           ",
            "Comunitat Valenciana          ",
            "Extremadura                   ",
            "Galicia                       ",
            "Illes Balears                 ",
            "La Rioja                      ",
            "País Vasco                    ",
            "Principado de Asturias        ",
            "Región de Murcia              ",
        ]
    }


def test_area_processor(area_processor, data, index_by_area):
    for area in Area:
        data_by_area: DataFrame = area_processor.data_by_area(data, area)
        if area == Area.CCAA:
            assert list(data_by_area.index) == index_by_area.get(area)
