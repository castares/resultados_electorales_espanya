from dataclasses import dataclass
from typing import Protocol

from pandas import DataFrame


class SupportsComputeResultsPerAlgorithm(Protocol):
    def compute_results_per_algorithm(
        self, votes_per_party: DataFrame
    ) -> DataFrame:
        ...


@dataclass
class Algorithm:
    area_split: str

    def compute_results_per_algorithm(self):
        ...


def build_electoral_algorithm(electoral_system):
    ...
