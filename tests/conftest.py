from typing import Any, Generator

import numpy as np
import pytest
from numpy.typing import NDArray

from thermo.costs import CostName, make_cost
from thermo.utils import io
from thermo.utils.building import Building
from thermo.utils.room import Room


@pytest.fixture
def all_buildings() -> Generator[list[Building], None, None]:
    yield io.load_all_buildings()


@pytest.fixture
def core_building_specs() -> Generator[dict[str, Any], None, None]:
    yield {"name", "municipality", "ranker", "costs", "room_descriptions", "adjacency"}


@pytest.fixture
def timeslots() -> Generator[int, None, None]:
    yield 3


@pytest.fixture
def demo_building_name() -> Generator[str, None, None]:
    yield "demo_school"


@pytest.fixture
def demo_graph() -> Generator[NDArray, None, None]:
    yield np.array(
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
def demo_state(
    timeslots: int, demo_graph: Generator[NDArray, None, None]
) -> Generator[NDArray, None, None]:
    out = np.zeros((timeslots, demo_graph.shape[0]))
    out[0, 2] = 1  # Room C is occupied at time t_0 (time slots t_0, t_1, t_2)
    out[0, 3] = 1  # Room D is occupied at time t_0 (time slots t_0, t_1, t_2)
    out[1, 4] = 1  # Room E is occupied at time t_1 (time slots t_0, t_1, t_2)
    out[2, 6] = 1  # Room G is occupied at time t_2 (time slots t_0, t_1, t_2)
    out = out.flatten()
    yield out


@pytest.fixture
def demo_config() -> Generator[dict[str, Any], None, None]:
    yield {
        "ranker": "FullRanker",
        "costs": {"HeatingCost": {"t_weight": 1.0, "message_importance": 0.5}},
    }


@pytest.fixture
def demo_room_descriptions() -> Generator[list[dict[str, Any]], None, None]:
    """Yields a list of room descriptions as dicts"""
    yield [
        {"name": "Room A", "capacity": 30, "amenities": {"whiteboard", "projector"}},
        {"name": "Room B", "capacity": 20, "amenities": {"whiteboard"}},
        {"name": "Room C", "capacity": 10, "amenities": {"projector"}},
        {"name": "Room D", "capacity": 30, "amenities": {"whiteboard", "projector"}},
        {"name": "Room E", "capacity": 15},
        {"name": "Room F", "capacity": 30, "amenities": {"whiteboard"}},
        {"name": "Room G", "capacity": 15, "amenities": {"whiteboard", "screen"}},
        {"name": "Room H", "capacity": 30, "amenities": {"screen"}},
        {
            "name": "Room I",
            "capacity": 10,
            "amenities": {"whiteboard", "projector", "screen"},
        },
        {"name": "Room J", "capacity": 30},
    ]


@pytest.fixture
def demo_rooms(
    demo_room_descriptions: Generator[dict[str, Any], None, None]
) -> Generator[list[Room], None, None]:
    """Yields a list of room descriptions as Room objects"""
    yield [
        Room(index=index, **specs) for index, specs in enumerate(demo_room_descriptions)
    ]


@pytest.fixture
def demo_building(
    demo_building_name: Generator[str, None, None],
    demo_config: Generator[dict[str, Any], None, None],
    demo_room_descriptions: Generator[list[dict[str, Any]], None, None],
    demo_graph: Generator[NDArray, None, None],
) -> Generator[Building, None, None]:
    """yields a demo building object made from the fixtures above"""
    yield Building(
        name=demo_building_name,
        municipality="demo_municipality",
        ranker=demo_config["ranker"],
        costs=demo_config["costs"],
        room_descriptions=demo_room_descriptions,
        adjacency=demo_graph,
    )


@pytest.fixture
def demo_building_from_config(
    demo_building_name: Generator[str, None, None]
) -> Generator[Building, None, None]:
    building_path = io.get_building_path(demo_building_name)
    yield io.load_building(building_path)


@pytest.fixture(params=list(CostName.__args__))
def cost(request, demo_graph, demo_rooms):
    """Yields a CostModel instance for each cost name"""
    yield make_cost(
        request.param,
        adjacency=demo_graph,
        room_descriptions=demo_rooms,
    )
