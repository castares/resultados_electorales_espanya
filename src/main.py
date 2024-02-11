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


    return data


if __name__ == "__main__":
    main()
