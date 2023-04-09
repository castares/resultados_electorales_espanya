from pandas import DataFrame
import pytest
from src.results_calculator import compute_largest_remainder


@pytest.fixture(scope="module")
def input_data():
    return DataFrame.from_dict(
        {
            "Yellows": {
                "Votos válidos": 47000.0,
            },
            "Whites": {
                "Votos válidos": 16000.0,
            },
            "Reds": {
                "Votos válidos": 15800.0,
            },
            "Greens": {
                "Votos válidos": 12000.0,
            },
            "Blues": {
                "Votos válidos": 6100.0,
            },
            "Pinks": {
                "Votos válidos": 3100.0,
            },
        }
    )


@pytest.fixture(scope="module")
def expected_results():
    return DataFrame.from_dict(
        {
            "Yellows": {
                "Votos válidos": 47000.0,
                "seats": 0.0,
                "hare quota": 0.0,
                "votes/quota": 4.7,
                "automatic_seats": 4.0,
                "remainder": 0.7,
                "highest_remainder_seats": 1.0,
                "total_seats": 5.0,
            },
            "Whites": {
                "Votos válidos": 16000.0,
                "seats": 0.0,
                "hare quota": 0.0,
                "votes/quota": 1.6,
                "automatic_seats": 1.0,
                "remainder": 0.6,
                "highest_remainder_seats": 1.0,
                "total_seats": 2.0,
            },
            "Reds": {
                "Votos válidos": 15800.0,
                "seats": 0.0,
                "hare quota": 0.0,
                "votes/quota": 1.58,
                "automatic_seats": 1.0,
                "remainder": 0.58,
                "highest_remainder_seats": 0.0,
                "total_seats": 1.0,
            },
            "Greens": {
                "Votos válidos": 12000.0,
                "seats": 0.0,
                "hare quota": 0.0,
                "votes/quota": 1.2,
                "automatic_seats": 1.0,
                "remainder": 0.2,
                "highest_remainder_seats": 0.0,
                "total_seats": 1.0,
            },
            "Blues": {
                "Votos válidos": 6100.0,
                "seats": 0.0,
                "hare quota": 0.0,
                "votes/quota": 0.61,
                "automatic_seats": 0.0,
                "remainder": 0.61,
                "highest_remainder_seats": 1.0,
                "total_seats": 1.0,
            },
            "Pinks": {
                "Votos válidos": 3100.0,
                "seats": 0.0,
                "hare quota": 0.0,
                "votes/quota": 0.31,
                "automatic_seats": 0.0,
                "remainder": 0.31,
                "highest_remainder_seats": 0.0,
                "total_seats": 0.0,
            },
        }
    )


def test_compute_largest_remainder(input_data, expected_results):
    results: DataFrame = compute_largest_remainder(input_data, total_seats=10)
    results = results[expected_results.columns]

    assert results.loc["total_seats"].equals(expected_results.loc["total_seats"])
