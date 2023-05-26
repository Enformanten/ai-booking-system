from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import NDArray

from thermo.costs import CostName
from thermo.ranker import RankerName
from thermo.utils.room import Room


@dataclass
class Building:

    """A dataclass that represents a building.
    Holds the static information about a given
    building.
    """

    name: str
    municipality: str
    ranker: RankerName
    costs: dict[CostName, Any]
    room_descriptions: list[dict[str, Any]]
    adjacency: list[list[int]] | NDArray

    def __post_init__(self) -> None:
        """Perform some post-initialization tasks
        1. Room descriptions are converted to Room objects
        2. The adjacency matrix is converted to a NDArray."""
        if not isinstance(self.room_descriptions[0], Room):
            self.room_descriptions = [
                Room(index=index, **specs)
                for index, specs in enumerate(self.room_descriptions)
            ]

        if not isinstance(self.adjacency, np.ndarray):
            self.adjacency = np.array(self.adjacency)

    def get_room_attr(self, attr: str) -> list[Any]:
        """Returns a list of the given attribute for all rooms."""
        return [getattr(room, attr) for room in self.room_descriptions]

    @property
    def specifications(self) -> dict[str, Any]:
        """Returns a dictionary of the building's specifications."""
        return self.__dict__
