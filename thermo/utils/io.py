from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray

from thermo.utils.room import Room


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
    # TODO: This is a placeholder, the correct implementation
    # TODO: must be added here. :)

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


def load_config(path: Path) -> dict[str, Any]:
    """
    Loads school-specific configuration from a file.
    Args:
        path: path to the subscription
            where the adjacency matrix is.

    Returns:
        The configuration defined by the user.
    """
    # TODO: This is a placeholder, the correct implementation
    # TODO: must be added here. :)
    return {
        "ranker": "FullRanker",
        "costs": {"HeatingCost": {"t_weight": 1.0, "message_importance": 0.5}},
    }


def load_room_description(path: Path) -> list[Room]:
    """
    Loads a description of each room from a file.
    Args:
        path: path to the subscription where the adjacency matrix is.
    Returns:
        a list of rooms with the same indexing as the adjacency.
    """
    # TODO: This is a placeholder, the correct implementation
    # TODO: must be added here. :)
    room_descriptions = [
        {"name": "Room A", "capacity": 30},
        {"name": "Room B", "capacity": 20},
        {"name": "Room C", "capacity": 10},
        {"name": "Room D", "capacity": 30},
        {"name": "Room E", "capacity": 15},
        {"name": "Room F", "capacity": 30},
        {"name": "Room G", "capacity": 15},
        {"name": "Room H", "capacity": 30},
        {"name": "Room I", "capacity": 10},
        {"name": "Room J", "capacity": 30},
    ]
    return [Room(index=index, **specs) for index, specs in enumerate(room_descriptions)]
