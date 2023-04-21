import numpy as np
import pytest
from numpy.typing import NDArray

from thermo.graph.generate_random import generate_adjacency_matrix


@pytest.mark.parametrize("n_rooms", [10, 20, 30])
def test_random_graph_format(n_rooms: int) -> None:
    """Test that the random graph generator returns
    a matrix of the correct shape and with only 0s and 1s.

    """
    assert generate_adjacency_matrix(n_rooms).shape == (n_rooms, n_rooms)
    assert np.all(np.isin(generate_adjacency_matrix(n_rooms), [0, 1]))


@pytest.mark.parametrize(
    "n_rooms,seed,expected",
    [
        (4, 42, np.array([[0, 0, 1, 1], [0, 0, 1, 0], [1, 1, 0, 0], [1, 0, 0, 0]])),
        (
            10,
            84,
            np.array(
                [
                    [0, 0, 0, 1, 1, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
                    [1, 0, 0, 0, 0, 0, 1, 1, 0, 1],
                    [1, 0, 1, 0, 0, 1, 1, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
                    [0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                    [1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
                    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                ]
            ),
        ),
    ],
)
def test_random_graph_seed(n_rooms: int, seed: int, expected: NDArray) -> None:
    """Test that the random graph generator returns
    the same graph for the same seed.
    """

    assert np.allclose(generate_adjacency_matrix(n_rooms, seed=seed), expected)
