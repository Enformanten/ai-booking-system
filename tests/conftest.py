import numpy as np
import pytest

from thermo.utils.room import Room


@pytest.fixture
def graph():
    return np.array(
        [
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [0, 1, 1, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
            [0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        ]
    )


@pytest.fixture
def timeslots():
    return 3


@pytest.fixture
def state(timeslots, graph):
    out = np.zeros((timeslots, graph.shape[0]))
    out[0, 2] = 1  # Room C is occupied at time t_0 (time slots t_0, t_1, t_2)
    out[0, 3] = 1  # Room D is occupied at time t_0 (time slots t_0, t_1, t_2)
    out[1, 4] = 1  # Room E is occupied at time t_1 (time slots t_0, t_1, t_2)
    out[2, 6] = 1  # Room G is occupied at time t_2 (time slots t_0, t_1, t_2)
    out = out.flatten()
    return out


@pytest.fixture
def config():
    return {
        "ranker": "FullRanker",
        "costs": [{"HeatingCost": {"t_weight": 1.0, "message_importance": 0.5}}],
    }


@pytest.fixture
def room_description():
    room_names = (
        "Room A",
        "Room B",
        "Room C",
        "Room D",
        "Room E",
        "Room F",
        "Room G",
        "Room H",
        "Room I",
        "Room J",
    )
    return [Room(name=name) for name in enumerate(room_names)]
