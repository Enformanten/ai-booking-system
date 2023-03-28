import numpy as np
from numpy.typing import NDArray


class InvalidAdjacency(ValueError):
    def __init__(self, message):
        super().__init__(message)


def is_symmetric(A: NDArray) -> bool:
    return np.allclose(A, A.T)


def no_self_interactions(A: NDArray) -> bool:
    return np.sum(np.diag(A) ** 2) == 0.0


def get_degree_vector(A: NDArray) -> bool:
    return A.sum(axis=1)


def get_laplacian(A: NDArray) -> bool:
    D = np.diag(get_degree_vector(A))
    return D - A


def is_connected(A: NDArray) -> bool:
    L = get_laplacian(A)
    v = np.linalg.eigvalsh(L)  # sorted in ascending order
    is_laplacian = np.abs(v[0] / v[-1]) < 1e-14 and np.all(v[1:] >= 0)
    # inverse cond p-2 number orthogonal complement to 1
    fieldler_icond = v[1] / v[-1]
    return is_laplacian and (fieldler_icond >= 1e-14)


def validate_adjacency(A: NDArray) -> None:
    if not no_self_interactions(A):
        raise InvalidAdjacency("Adjancency matrix has non-zero diagonal elements.")
    if not is_symmetric(A):
        raise InvalidAdjacency("Adjacency matrix is not symmetric.")
    if not is_connected(A):
        raise InvalidAdjacency(
            "The graph represented by A can be split into two graphs."
        )


def get_time_adjacency(A: NDArray, n_times: int, time_weight: float = 1.0) -> NDArray:
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
