from datetime import date

import numpy as np
import pytest
from numpy.typing import NDArray

from thermo.adapter.state_connection import get_state


def test_format_state():
    state = get_state(date(2023, 1, 11), timeslots=3)
    assert isinstance(state, np.ndarray)
    assert state.shape == (3 * 10,)


@pytest.mark.parametrize(
    "day,state",
    [
        (
            date(2021, 12, 2),
            np.array(
                [
                    0.0,
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    1.0,
                    1.0,
                    0.0,
                    0.0,
                ]
            ),
        ),
        (
            date(2021, 12, 12),
            np.array(
                [
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    1.0,
                    1.0,
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    1.0,
                    1.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                ]
            ),
        ),
    ],
)
def test_state_api(day: str, state: NDArray):
    assert all(get_state(day, timeslots=3) == state)
