import numpy as np
from numpy.typing import NDArray


class InvalidAdjacency(ValueError):
    """
    Error class to show the adjacency matrix is not
    compatible with the model.
    """

    def __init__(self, message):
        super().__init__(message)


def is_symmetric(A: NDArray) -> bool:
    """
    Function to check if an adjacency matrix A is symmetric.

    We are using undirected graphs, so A not being symmetric
    would mean that room 1 shares a wall with room 2 but 2 doesn't
    share a wall with room 1.
    """
    return np.allclose(A, A.T)


def no_self_interactions(A: NDArray) -> bool:
    """
    Function to check that the adjacency matrix does not contain
    self-interactions.

    We effectively check that all diagonal terms are 0. If the
    terms of the diagonal were non-zero, it would mean that a room
    shares a wall with itself.
    """
    return np.sum(np.diag(A) ** 2) == 0.0


def get_degree_vector(A: NDArray) -> NDArray:
    """
    Given an adjacency matrix A of size NxN, returns
    a vector of size N with the degree of each node.

    The degree of a node is the number of neighbors it has.
    """
    return A.sum(axis=1)


def get_laplacian(A: NDArray) -> NDArray:
    """
    Given an adjacency matrix A of size NxN, returns its
    Laplacian matrix L of size NxN.

    https://en.wikipedia.org/wiki/Laplacian_matrix

    Intuitively, the Laplacian matrix
    is something of the sort "Share with your neighbors" operation
    (that is why it is called Laplacian). The following operation:
    v += L*v (where * is matrix multiplication),
    if done repeatedly, results in all the entries of v having the
    same value if there is a path that connects any pair of them.
    """
    D = np.diag(get_degree_vector(A))
    return D - A


def is_connected(A: NDArray) -> bool:
    """
    Checks if there is a path connecting any pair of nodes.
    If there is not, then the graph can be split into two subgraphs.

    It is done by looking at the eigenvalues of the Laplacian matrix
    (there are other ways to do this).

    Since the eigenvalues are computed numerically, they will not be exactly
    zero. So to check that, we check that the eigenvalue that should be zero
    divided by the largest eigenvalue are similar to machine precision
    (which for double floats is about 1e-16).
    """
    L = get_laplacian(A)
    # Get the eigenvalues of the Laplacian matrix.
    # Use that the laplacian is symmetric to speed-up the computation.
    v = np.linalg.eigvalsh(L)  # sorted in ascending order
    # Check the Laplacian has one zero eigenvalue and the others are >= 0
    # This should be fulfilled by all Laplacians, otherwise A is wrong in some way.
    is_laplacian = np.abs(v[0] / v[-1]) < 1e-14 and np.all(v[1:] >= 0)
    # Check that the laplacian has no other zero eigenvalues.
    # If it had other zero eigenvalues, it would mean the graph can be split.
    fieldler_icond = v[1] / v[-1]
    return is_laplacian and (fieldler_icond >= 1e-14)


def validate_adjacency(A: NDArray) -> None:
    """
    Validates the adjacency matrix. If it is not valid, it raises
    an InvalidAdjacency exception.

    Currently, the following criteria are checked:
    - its symmetric
    - it does not contain self-interactions
    - the graph cannot be split into two graphs.
    """
    if not no_self_interactions(A):
        raise InvalidAdjacency("Adjacency matrix has non-zero diagonal elements.")
    if not is_symmetric(A):
        raise InvalidAdjacency("Adjacency matrix is not symmetric.")
    if not is_connected(A):
        raise InvalidAdjacency(
            "The graph represented by A can be split into two graphs."
        )


def get_time_adjacency(A: NDArray, n_times: int, time_weight: float = 1.0) -> NDArray:
    """
    Get the adjacency matrix of the graph that contains a copy of the school
    for each time slot and where rooms are connected to themselves in the past
    and in the future (see documentation).

    Args:
        A: Adjacency matrix of the school, where 1 represents two rooms share
            a wall and 0 represents they don't.
        n_times: number of time slots.
        time_weight: Relative weight between the time and spatial components.
            (In the documentation it's called lambda).

    Returns:
        The time-space adjacency matrix for the graph representing the bookings
        of a school.
    """
    n = A.shape[0]
    eye = time_weight * np.eye(n)
    zero = np.zeros((n, n))

    def choose_block(i: int, j: int) -> NDArray:
        if i == j:
            return A
        elif i - 1 == j or i + 1 == j:
            return eye
        else:
            return zero

    return np.block(
        [[choose_block(i, j) for i in range(n_times)] for j in range(n_times)]
    )
