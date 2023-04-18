import numpy as np


def mock_api(date: str, timeslots: int = 3, rooms: int = 10, n_booked=5) -> np.ndarray:
    """Mock API for testing purposes. Initializes a random state.
    using date as the seed.

    Args:
        date (str): date in the format YYYY-MM-DD.
        timeslots (int) - Default 3: timeslots to account for.
        rooms (int) - Default 10: number of rooms to initialize.
        n_booked (int) - Default 5: number of rooms to simulate as booked.
    Returns:
        np.ndarray: a random flat array containing 1 if the room is booked
            at that time a zero otherwise.
    """

    # Set random seed to date to get reproducible results
    np.random.seed(int(date.replace("-", "")))

    # initialize state, fetch n random values, sets values to 1
    state = np.zeros((timeslots, rooms))
    indices = np.random.randint(0, state.size, size=n_booked)
    state.flat[indices] = 1
    return state.flatten()


def get_state(day: str) -> np.ndarray:
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

    :rtype: :class:`thermo.models.state.State`
    """

    # NOTE: This is a mock API for testing purposes.
    return mock_api(day)
