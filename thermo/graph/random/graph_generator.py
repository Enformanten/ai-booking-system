import networkx as nx
from numpy.typing import NDArray


def generate_adjacency_matrix(
    n_rooms: int = 10, p: float | None = None, seed: None | int = None
) -> NDArray:
    """Generate a random adjacency matrix for a
    graph with n_rooms nodes. The probability of
    an edge between two nodes is p.

    Can be used in conjunction with the 'mock_api'
    function to generate a random state afterwards.

    Args:
        n_rooms: number of rooms.
        p: probability of an edge between two nodes.
            If None, p is set to n_rooms**-0.5 to ensure
            that fewer rooms are more likely to be connected.
        seed: seed for random number generator.

    Example:
    >>> from thermo.graph.random.graph_generator import generate_adjacency_matrix
    >>> generate_adjacency_matrix(n_rooms=5, seed=4)
    array([
        [0, 1, 1, 1, 1],
        [1, 0, 1, 1, 0],
        [1, 1, 0, 0, 0],
        [1, 1, 0, 0, 1],
        [1, 0, 0, 1, 0]
    ])

    Returns:
        NDArray: a random adjacency matrix of shape
        (n_rooms, n_rooms)
    """

    p = p if p else n_rooms**-0.5
    G = nx.generators.random_graphs.gnp_random_graph(n_rooms, p=p, seed=seed)
    return nx.adjacency_matrix(G).todense()
