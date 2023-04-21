import numpy as np
import pytest

from thermo.costs import CostModel, CostName, make_cost


@pytest.mark.parametrize("cost_name", list(CostName.__args__))
def test_costs(cost_name, state, graph, room_description):
    """
    Check make cost produces the right instance and that both the
    init and run methods of all implemented costs classes accept
    additional arguments as **kwargs
    """
    cost = make_cost(
        cost_name, adjacency=graph, room_description=room_description, foo=True
    )
    result = cost.run(state, n_time_slots=3, waz=True)
    assert isinstance(cost, CostModel)
    assert isinstance(result, np.ndarray)