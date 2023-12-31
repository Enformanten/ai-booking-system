import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def mock_raw_booking():
    yield pd.DataFrame(
        {
            "BOOKED": [0, 1, 1, 0, 1, 0, 0, 0, 0],
            "ROOM_ID": 9 * ["ROOM_A"],
            "START_TIME": [
                None,
                "16:00:00",
                "16:00:00",
                None,
                "19:00:00",
                None,
                None,
                None,
                None,
            ],
            "END_TIME": [
                None,
                "17:30:00",
                "17:30:00",
                None,
                "20:00:00",
                None,
                None,
                None,
                None,
            ],
            "TIME_LEFT_OF_BOOKING": [np.nan, 1.5, 0.5, 0, 1, 0, 0, 0, 0],
            "TIMESTAMP": pd.period_range(
                start="2022-01-06 15:00:00", end="2022-01-06 23:00:00", freq="H"
            ).to_timestamp(),
        }
    )


@pytest.fixture
def mock_binary_booking():
    yield pd.DataFrame(
        {
            "ROOM_A_booked": [0, 1, 1, 0, 1, 0, 0, 0, 0],
            "TIMESTAMP": pd.period_range(
                start="2022-01-06 15:00:00", end="2022-01-06 23:00:00", freq="H"
            ).to_timestamp(),
        }
    ).set_index("TIMESTAMP")


@pytest.fixture
def mock_fractional_booking():
    yield pd.DataFrame(
        {
            "ROOM_A_booked": [0, 1, 0.5, 0, 1, 0, 0, 0, 0],
            "TIMESTAMP": pd.period_range(
                start="2022-01-06 15:00:00", end="2022-01-06 23:00:00", freq="H"
            ).to_timestamp(),
        }
    ).set_index("TIMESTAMP")


@pytest.fixture
def mock_morning_weekend():
    yield pd.DataFrame(
        {
            "ROOM_A_booked": [1] + 7 * [0] + [1, 1, 0, 1, 0, 0, 0, 0],
            "TIMESTAMP": pd.period_range(
                start="2022-01-06 08:00:00", end="2022-01-06 23:00:00", freq="H"
            ).to_timestamp(),
        }
    ).set_index("TIMESTAMP")


@pytest.fixture
def mock_evening_weekend():
    yield pd.DataFrame(
        {
            "ROOM_A_booked": 8 * [0] + [1, 1, 0, 1, 0, 0, 0, 0],
            "TIMESTAMP": pd.period_range(
                start="2022-01-06 08:00:00", end="2022-01-06 23:00:00", freq="H"
            ).to_timestamp(),
        }
    ).set_index("TIMESTAMP")


@pytest.fixture
def mock_unused():
    yield pd.DataFrame(
        {
            "ROOM_A_booked": 9 * [0],
            "TIMESTAMP": pd.period_range(
                start="2022-01-06 15:00:00", end="2022-01-06 23:00:00", freq="H"
            ).to_timestamp(),
        }
    ).set_index("TIMESTAMP")
