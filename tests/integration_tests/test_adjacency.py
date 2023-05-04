import pytest

from thermo.costs.adjacency import is_connected, is_symmetric, no_self_interactions
from thermo.utils.io import load_all_buildings


@pytest.mark.parametrize("building", load_all_buildings(), ids=lambda x: x.name)
def test_symmetric_adjacencies(building):
    msg = f"Adjacency of {building.name} is not symmetric"
    assert is_symmetric(building.adjacency), msg


@pytest.mark.parametrize("building", load_all_buildings(), ids=lambda x: x.name)
def test_connected_adjacencies(building):
    msg = f"The graph of {building.name} could be split into two graphs"
    assert is_connected(building.adjacency), msg


@pytest.mark.parametrize("building", load_all_buildings(), ids=lambda x: x.name)
def test_valid_adjacency(building):
    a = building.adjacency
    msg = f"The graph of {building.name} includes self-interactions"
    assert no_self_interactions(a), msg
    msg = f"The graph of {building.name} has edges with weight greater than 1"
    assert ((a == 0) | (a == 1)).all(), msg
