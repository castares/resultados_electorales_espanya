from data_selector import DataSelector, Election
from area_processor import Area, AreaProcessor
from results_calculator import ResultsCalculator, ElectoralSystem, TotalSeats
from spain_map import get_spain_map

from pandas import DataFrame
from geopandas import GeoDataFrame


def main():
    data_selector: DataSelector = DataSelector()
    area_processor: AreaProcessor = AreaProcessor()
    results_calculator: ResultsCalculator = ResultsCalculator()

    data: DataFrame = data_selector.select_data(Election.CONGRESO_2019)
    data = area_processor.data_by_area(data, Area.CCAA)
    data: DataFrame = results_calculator.compute_results(
        data, ElectoralSystem.LARGEST_REMAINDER, TotalSeats.CONGRESO
    )

    # TODO: extract to a module
    spain_map: GeoDataFrame = get_spain_map()
    data = data.drop(data[data["Nombre de Comunidad"] == "Ciudad de Ceuta"].index)
    data = data.drop(data[data["Nombre de Comunidad"] == "Ciudad de Melilla"].index)
    data.sort_values(by=["Nombre de Comunidad"], ascending=False)
    data["Nombre de Comunidad"] = data["Nombre de Comunidad"].str.replace(" ", "")
    data = GeoDataFrame(
        data.merge(
            spain_map, how="left", left_on="Nombre de Comunidad", right_on="NAME_1"
        )
    )
    data = data.drop(columns="NAME_1")

    return data


if __name__ == "__main__":
    main()
