import numpy as np
import pytest
from numpy.typing import NDArray

from thermo.config import UNAVAILABLE_COST
from thermo.costs import CostModel, CostName, make_cost
from thermo.utils.room import Room


@pytest.mark.parametrize("cost_name", list(CostName.__args__))
def test_make_costs(
    cost_name: str,
    demo_graph: NDArray,
    demo_rooms: list[Room],
) -> None:
    """
    Check make cost produces the right instance and that the
    init method of all implemented costs classes accept
    additional arguments as **kwargs
    """
    cost = make_cost(
        cost_name,
        adjacency=demo_graph,
        room_descriptions=demo_rooms,
        foo=True,  # this is an arbitrary kwarg
    )
    assert isinstance(cost, CostModel)


def test_costs(
    cost: CostModel,
    demo_state: NDArray,
) -> None:
    """
    Chect that cost.run produces the right output and that
    the run methods of all implemented costs classes accept
    additional arguments as **kwargs
    """
    result = cost.run(demo_state, n_time_slots=3, bar=True)  # bar is an arbitrary kwarg
    assert isinstance(result, np.ndarray)


def test_unavailable_cost(
    cost: CostModel,
    demo_state: NDArray,
    T=10,
) -> None:
    """Checks that all costs for available rooms are below T and that
    unavailable rooms have a cost ≈equal to config.UNAVAILABLE_COST

    args:
        cost_name: name of the cost to test
        demo_state: demo state
        demo_graph: demo adjacency matrix
        demo_rooms: demo room descriptions
        T: Arbitrary threshold that should be above all costs
            associated with available rooms. This is used to
            check that unavailable rooms have a cost ≈equal to
            config.UNAVAILABLE_COST

    """
    result = cost.run(
        demo_state,
        n_time_slots=3,
        required_capacity=20,  # trigger unavailable cost for capacity
        required_amenities={"whiteboard"},  # trigger unavailable cost for amenities
    )
    assert np.allclose(result[np.argwhere(result > T)], UNAVAILABLE_COST, atol=1e-10)
