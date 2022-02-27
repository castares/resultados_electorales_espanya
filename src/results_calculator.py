from dataclasses import dataclass

import pandas as pd

from election_data_filter import (
    SupportsFilterElectionData,
    build_election_data,
)
from area_type_processor import (
    SupportsSumVotesPerArea,
    build_area_processor,
)
from electoral_system_processor import (
    SupportsComputeResultsPerAlgorithm,
    build_electoral_algorithm,
)


# TODO: Convert all area_types, parties and electoral algorithms to Enums


@dataclass
class ResultsCalculator:
    election_data: SupportsFilterElectionData
    area_processor: SupportsSumVotesPerArea
    electoral_system: SupportsComputeResultsPerAlgorithm

    def compute_results(self):
        ...


def build_results_calculator(election, area_split, electoral_system):
    return ResultsCalculator(
        election_data=build_election_data(election),
        area_processor=build_area_processor(area_split),
        electoral_system=build_electoral_algorithm(electoral_system),
    )


if __name__ == "__main__":
    x = build_results_calculator("asdf", "asdf", "asdf")
