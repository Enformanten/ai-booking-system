import pytest

from thermo.graph.adjacency import is_connected, is_symmetric, no_self_interactions
from thermo.utils.building import Building
from thermo.utils.io import load_all_buildings


@pytest.mark.parametrize("building", load_all_buildings(), ids=lambda x: x.name)
def test_symmetric_adjacencies(building: Building) -> None:
    """
    Checks if the matrix representing the rooms stored in every
    `buildings/<building_name>/adjacency.json` is symmetric.
    Symmetric means that the matrix is squared (has the same number
    of rows and columns) and that if one folded it along the diagonal
    from top left to bottom right, values would match.

    If it was not symmetric, it would mean that room 3 has a wall with room
    4 but 4 does not have a wall with room 3, which is nonsense.

    If this fails, please correct the file :)
    """
    msg = f"Adjacency of {building.name} is not symmetric."
    assert is_symmetric(building.adjacency), msg


@pytest.mark.parametrize("building", load_all_buildings(), ids=lambda x: x.name)
def test_connected_adjacencies(building: Building) -> None:
    """
    Checks if that the matrix representing the rooms stored in every
    `buildings/<building_name>/adjacency.json` cannot be divided into
    two sub graphs without breaking a wall.

    If this test fails, it means that your adjacency probably represents
    two buildings or that you forgot a wall. While the rest of the code
    will still work if this fails, it will be slower, because you are
    building a lot of zeros for no good reason.

    If this fails, please correct the file :)
    """
    msg = f"The graph of {building.name} could be split into two graphs."
    assert is_connected(building.adjacency), msg


@pytest.mark.parametrize("building", load_all_buildings(), ids=lambda x: x.name)
def test_valid_adjacency(building: Building) -> None:
    """
    Checks if that the matrix representing the rooms stored in every
    `buildings/<building_name>/adjacency.json` is that of a non-weighted
    graph with no self interactions.

    This translates to checking that all entries are zero or one (this is, wall
    or not wall, we don't judge on the quality of the walls) and that a room does
    not have walls with itself.

    The underlying code is not prepared to take any of these cases right now,
    so please correct the file :) .
    """
    a = building.adjacency
    msg = f"The graph of {building.name} includes self-interactions."
    assert no_self_interactions(a), msg
    msg = f"The graph of {building.name} is a weighted graph."
    assert ((a == 0) | (a == 1)).all(), msg
