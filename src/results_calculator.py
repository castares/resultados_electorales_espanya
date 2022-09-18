from collections.abc import Callable
from enum import Enum, auto

from pandas import DataFrame, Series


class Total(int, Enum):
    CONGRESO = 350


class ElectoralSystem(str, Enum):
    LARGEST_REMAINDER = auto()
    DHONDT = auto()


def compute_largest_remainder(
    data: DataFrame, total_seats: Total = Total.CONGRESO
) -> DataFrame:
    __import__("pdb").set_trace()
    total_votes: int = data.loc["Votos válidos"].sum()
    hare_quota: float = total_votes / total_seats
    # TODO: from here computation should be applied to each row.
    data.loc["votes/quota"] = data.loc["Votos válidos"] / hare_quota
    data.loc["automatic_seats"] = data.loc["votes/quota"].astype("int")
    data.loc["remainder"] = (
        data.loc["votes/quota"] - data.loc["automatic_seats"]
    )
    remainder_seats = total_seats - data.loc["automatic_seats"].sum()
    data = data.sort_values(by="remainder", axis=1, ascending=False)
    data.loc["highest_remainder_seats"] = 0
    for idx in range(0, int(remainder_seats)):
        column = data.columns[idx]
        data.loc["highest_remainder_seats", column] += 1
    data.loc["total_seats"] = (
        data.loc["automatic_seats"] + data.loc["highest_remainder_seats"]
    )
    return data


def compute_dhondt(data: DataFrame) -> DataFrame:
    pass


class ResultsCalculator:

    _algorithm: dict[ElectoralSystem, Callable] = {
        ElectoralSystem.LARGEST_REMAINDER: compute_largest_remainder,
        ElectoralSystem.DHONDT: compute_dhondt,
    }

    def compute_results(
        self,
        data,
        electoral_system: ElectoralSystem,
        total_seats: Total.CONGRESO,
    ):
        algorithm = self._algorithm.get(electoral_system)
        if not algorithm:
            raise NameError(
                "Invalid Electoral System. Please choose a valid one."
            )
        results: DataFrame = algorithm(data, total_seats=total_seats)
        return results
