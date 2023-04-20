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
    room_descriptions = [
        {"name": "Room A", "capacity": 30},
        {"name": "Room B", "capacity": 20},
        {"name": "Room C", "capacity": 10},
        {"name": "Room D", "capacity": 30},
        {"name": "Room E", "capacity": 15},
        {"name": "Room F", "capacity": 30},
        {"name": "Room G", "capacity": 15},
        {"name": "Room H", "capacity": 30},
        {"name": "Room I", "capacity": 10},
        {"name": "Room J", "capacity": 30},
    ]
    return [Room(index=index, **specs) for index, specs in enumerate(room_descriptions)]
