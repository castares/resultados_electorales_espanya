from enum import Enum

from pandas import DataFrame
import pandas as pd


class Election(str, Enum):
    CONGRESO_2019 = "Congreso 2019"


class DataSelector:
    _elections: dict[Election, str] = {
        Election.CONGRESO_2019: "./data/csv/congreso_2019.csv",
    }

    def select_data(self, election: Election) -> DataFrame:
        election_file: str = self._elections.get(election, "")
        return pd.read_csv(election_file)
