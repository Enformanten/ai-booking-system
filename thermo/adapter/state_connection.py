import datetime

import numpy as np
from numpy.typing import NDArray

from thermo.utils.time import get_time_slots


def mock_api(
    date: datetime.date,
    timeslots: int | None = None,
    rooms: int = 10,
    n_booked: int = 5,
) -> NDArray:
    """Mock API for testing purposes. Initializes a random state.
    using date as the seed.

    date: date in the format YYYY-MM-DD.
    timeslots: timeslots to account for.
    rooms: number of rooms to initialize.
    n_booked: number of rooms to simulate as booked.

    Returns:
        np.ndarray: a random flat array containing 1
        if the room is booked at that time, 0 otherwise.
    """
    timeslots = get_time_slots(date) if not timeslots else timeslots
    # Set random seed to date to get reproducible results
    np.random.seed(int(date.isoformat().replace("-", "")))

    # initialize state, fetch n random values, sets values to 1
    state = np.zeros((timeslots, rooms))
    indices = np.random.randint(0, state.size, size=n_booked)
    state.flat[indices] = 1
    return state.flatten()


def get_state(day: datetime.date, timeslots: int | None = None) -> NDArray:
    """Get a state from external API.
    Open booking URI for Favrskov Kommune
    - https://book01.webbook.dk/favrskov/_rapporter/
    simpel_dagsoversigt_output.php?gruppe=30&type=json

    For a building with 10 rooms and three timeslots,
    we assume the following format,
        - array([
            0., 0., 1., 1., 0., 0., 0., 0., 0., 0.,
            0., 0., 0., 0., 1., 0., 0., 0., 0., 0.,
            0., 0., 0., 0., 0., 0., 1., 0., 0., 0.
        ])
        s.t.
        - Room 2 is occupied at time t_0
        - Room 4 is occupied at time t_0
        - Room 5 is occupied at time t_1
        - Room 6 is occupied at time t_2

    Args:
        day: day for which we get booking state.
        timeslots: only useful for testing purposes.

    Returns:
        np.ndarray: a flat array (1 if the room is booked)
    """

    # NOTE: This is a mock API for testing purposes.
    return mock_api(day, timeslots)
