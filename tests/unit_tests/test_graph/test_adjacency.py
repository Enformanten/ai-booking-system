import numpy as np

from thermo.graph.adjacency import is_symmetric


def test_is_symmetric(demo_graph):
    assert is_symmetric(demo_graph)


def test_is_not_symmetric():
    A = np.array([[0, 1], [0, 0]])
    assert not is_symmetric(A)
