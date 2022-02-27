from dataclasses import dataclass
from typing import Protocol

import pandas as pd
from pandas import DataFrame


class SupportsSumVotesPerArea(Protocol):
    def sum_votes_per_area(self) -> DataFrame:
        ...


@dataclass
class AreaCalculator:
    area_split: str

    def sum_votes_per_area(self):
        ...


def build_area_processor(area_split):
    ...
