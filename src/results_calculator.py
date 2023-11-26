from collections.abc import Callable
from enum import Enum, auto
from typing import Literal

from pandas import DataFrame


class TotalSeats(int, Enum):
    CONGRESO = 350


class ElectoralSystem(str, Enum):
    LARGEST_REMAINDER = auto()
    DHONDT = auto()


def compute_largest_remainder(
    data: DataFrame, total_seats: TotalSeats = TotalSeats.CONGRESO
) -> DataFrame:
    total_votes: int = data.loc[:, "Votos válidos"].sum()
    hare_quota: float = total_votes / total_seats
    data["votes/quota"] = data.loc[:, "Votos válidos"] / hare_quota
    data["automatic_seats"] = data.loc[:, "votes/quota"].astype("int")
    data["remainder"] = data.loc[:, "votes/quota"] - data.loc[:, "automatic_seats"]

    remainder_seats = total_seats - data.loc[:, "automatic_seats"].sum()

    data = data.sort_values(by="remainder", axis=0, ascending=False)
    data["highest_remainder_seats"] = 0
    for idx in range(0, int(remainder_seats)):
        district = data.index[idx]
        data.loc[district, "highest_remainder_seats"] += 1
    data["total_seats"] = (
        data.loc[:, "automatic_seats"] + data.loc[:, "highest_remainder_seats"]
    )
    return data


def compute_dhondt(data: DataFrame) -> DataFrame:
    return data


class ResultsCalculator:

    _algorithm: dict[ElectoralSystem, Callable] = {
        ElectoralSystem.LARGEST_REMAINDER: compute_largest_remainder,
        ElectoralSystem.DHONDT: compute_dhondt,
    }

    def compute_results(
        self,
        data: DataFrame,
        electoral_system: ElectoralSystem,
        total_seats: Literal[TotalSeats.CONGRESO],
    ):
        algorithm = self._algorithm.get(electoral_system)
        if not algorithm:
            raise NameError("Invalid Electoral System. Please choose a valid one.")
        results: DataFrame = algorithm(data, total_seats=total_seats)
        return results.sort_values(
            by="total_seats", axis=0, ascending=False
        ).reset_index()
