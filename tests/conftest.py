import numpy as np
import pytest

from thermo.utils import io
from thermo.utils.building import Building
from thermo.utils.room import Room


@pytest.fixture
def all_buildings():
    return io.get_all_buildings()


@pytest.fixture
def core_building_specs():
    return {"name", "municipality", "ranker", "costs", "room_descriptions", "adjacency"}


@pytest.fixture
def timeslots():
    return 3


@pytest.fixture
def demo_building_name():
    return "demo_school"


@pytest.fixture
def demo_graph():
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
def demo_state(timeslots, demo_graph):
    out = np.zeros((timeslots, demo_graph.shape[0]))
    out[0, 2] = 1  # Room C is occupied at time t_0 (time slots t_0, t_1, t_2)
    out[0, 3] = 1  # Room D is occupied at time t_0 (time slots t_0, t_1, t_2)
    out[1, 4] = 1  # Room E is occupied at time t_1 (time slots t_0, t_1, t_2)
    out[2, 6] = 1  # Room G is occupied at time t_2 (time slots t_0, t_1, t_2)
    out = out.flatten()
    return out


@pytest.fixture
def demo_config():
    return {
        "ranker": "FullRanker",
        "costs": {"HeatingCost": {"t_weight": 1.0, "message_importance": 0.5}},
    }


@pytest.fixture
def demo_room_description():
    """Returns a list of room descriptions as dicts"""
    return [
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


@pytest.fixture
def demo_rooms(demo_room_description):
    """Returns a list of room descriptions as Room objects"""
    return [
        Room(index=index, **specs) for index, specs in enumerate(demo_room_description)
    ]


@pytest.fixture
def demo_building(demo_building_name, demo_config, demo_room_description, demo_graph):
    """Returns a demo building object made from the fixtures above"""
    return Building(
        name=demo_building_name,
        municipality="demo_municipality",
        ranker=demo_config["ranker"],
        costs=demo_config["costs"],
        room_descriptions=demo_room_description,
        adjacency=demo_graph,
    )


@pytest.fixture
def demo_building_from_config(demo_building_name):
    building_path = io.get_building_path(demo_building_name)
    return io.get_building_specs(building_path)
