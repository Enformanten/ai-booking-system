from dataclasses import dataclass
from typing import Any

import numpy as np

from thermo.utils.room import Room


@dataclass
class Building:

    """A dataclass that represents a building.
    Holds the static information about a given
    building.
    """

    name: str
    muncipality: str
    ranker: str
    costs: dict[str, Any]
    room_descriptions: list[dict[str, Any]]
    adjacency: list[list[int]]

    def __post_init__(self) -> None:
        """Perform some post-initialization tasks.
        1. Room descriptions are converted to Room objects
        2. The adjacency matrix is converted to a NDArray."""
        self.room_descriptions = [
            Room(index=index, **specs)
            for index, specs in enumerate(self.room_descriptions)
        ]
        self.adjacency = np.array(self.adjacency)
