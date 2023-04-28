from typing import Generator

import numpy as np
import pytest
from numpy.typing import NDArray

from thermo.config import UNAVAILABLE_COST
from thermo.costs import CostModel, CostName, make_cost
from thermo.utils.room import Room


@pytest.mark.parametrize("cost_name", list(CostName.__args__))
def test_costs(
    cost_name: str,
    demo_state: Generator[NDArray, None, None],
    demo_graph: Generator[NDArray, None, None],
    demo_rooms: Generator[list[Room], None, None],
) -> None:
    """
    Check make cost produces the right instance and that both the
    init and run methods of all implemented costs classes accept
    additional arguments as **kwargs
    """
    cost = make_cost(
        cost_name,
        adjacency=demo_graph,
        room_descriptions=demo_rooms,
        foo=True,  # this is an arbitrary kwarg
    )
    result = cost.run(demo_state, n_time_slots=3, bar=True)  # bar is an arbitrary kwarg
    assert isinstance(cost, CostModel)
    assert isinstance(result, np.ndarray)


@pytest.mark.parametrize("cost_name", list(CostName.__args__))
def test_unavailable_cost(
    cost_name: str,
    demo_state: Generator[NDArray, None, None],
    demo_graph: Generator[NDArray, None, None],
    demo_rooms: Generator[list[Room], None, None],
) -> None:
    """Checks that all costs for available rooms are below 10 and that
    unavailable rooms have a cost equal/close to config.UNAVAILABLE_COST"""

    cost = make_cost(
        cost_name,
        adjacency=demo_graph,
        room_descriptions=demo_rooms,
    )
    result = cost.run(
        demo_state,
        n_time_slots=3,
        required_capacity=20,  # trigger unavailable cost for capacity
        required_amenities={"whiteboard"},  # trigger unavailable cost for amenities
    )
    assert np.allclose(result[np.argwhere(result > 5)], UNAVAILABLE_COST, atol=1e-10)
