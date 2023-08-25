import numpy as np

from thermo.graph import adjacency


def test_is_symmetric(demo_graph):
    assert adjacency.is_symmetric(demo_graph)


def test_is_not_symmetric():
    A = np.array([[0, 1], [0, 0]])  # This matrix is not symmetric
    assert not adjacency.is_symmetric(A)


def test_no_self_interactions(demo_graph):
    assert adjacency.no_self_interactions(demo_graph)


def test_fails_self_interactions():
    # Test that the identity matrix represents self interactions
    # that is, rooms with walls with themselves.
    assert not adjacency.no_self_interactions(np.eye(2))


def test_get_degree_vector(demo_graph):
    degree_vector = np.array([2, 4, 2, 3, 3, 2, 3, 2, 1, 2])
    assert np.all(adjacency.get_degree_vector(demo_graph) == degree_vector)


def test_get_laplacian():
    A = np.array([[0, 1, 1], [1, 0, 0], [1, 0, 0]])
    L = np.array([[2, -1, -1], [-1, 1, 0], [-1, 0, 1]])
    assert np.all(adjacency.get_laplacian(A) == L)


def test_is_connected(demo_graph):
    assert adjacency.is_connected(demo_graph)


def test_is_not_connected():
    # Make a graph where (0,1) and (2,3) are connected,
    # but not with each other. This graph would represent
    # two separate buildings with two rooms each.
    A = np.array([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
    assert not adjacency.is_connected(A)
