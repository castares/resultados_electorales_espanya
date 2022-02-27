from dataclasses import dataclass
from typing import Protocol
from pandas import DataFrame


class SupportsFilterElectionData(Protocol):
    def filter_election_data(self) -> DataFrame:
        ...


@dataclass
class ElectionDataFilter:
    raw_data: DataFrame

    def filter_election_data(self) -> DataFrame:
        return self.raw_data


def build_election_data(election):
    return ElectionDataFilter
