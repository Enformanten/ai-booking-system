from pathlib import Path

import numpy as np
from numpy.typing import NDArray


def load_adjacency(path: Path) -> NDArray:
    """
    Loads adjacency matrix from file.
    Args:
        path: path to the subscription
            where the adjacency matrix is.

    Returns:
        a (N_rooms, N_rooms) matrix where 0 represents
        two rooms not sharing a wall and 1 represents
        said rooms sharing a wall.
    """
    # This is a placeholder, the correct implementation
    # must be added here. :)

    return np.array(
        [
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [0, 1, 1, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
            [0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        ]
    )
