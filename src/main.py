from data_selector import DataSelector, Election
from area_processor import Area, AreaProcessor
from protocols import SupportsComputeResults
from results_calculator import ResultsCalculator, ElectoralSystem, Total

from pandas import DataFrame


if __name__ == "__main__":
    data_selector: DataSelector = DataSelector()
    area_processor: AreaProcessor = AreaProcessor()
    results_calculator: ResultsCalculator = ResultsCalculator()

    data: DataFrame = data_selector.select_data(Election.CONGRESO_2019)
    data = area_processor.data_by_area(data, Area.CCAA)
    results: DataFrame = results_calculator.compute_results(
        data, ElectoralSystem.LARGEST_REMAINDER, Total.CONGRESO
    )
    __import__("pdb").set_trace()
