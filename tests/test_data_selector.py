import pytest
from src.data_selector import DataSelector, Election
from pandas import DataFrame


@pytest.fixture(scope="module")
def data_selector() -> DataSelector:
    return DataSelector()


@pytest.fixture()
def data_shapes() -> dict[Election, tuple]:
    return {
        Election.CONGRESO_2019: (8131, 80),
    }


def test_data_selector(data_selector, data_shapes):
    for election in Election:
        data: DataFrame = data_selector.select_data(election)
        assert data.shape == data_shapes.get(election)
