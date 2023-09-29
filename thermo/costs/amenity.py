from functools import cached_property

import numpy as np
from numpy.typing import NDArray

from thermo.config import UNAVAILABLE_COST
from thermo.costs.base import CostModel
from thermo.utils.room import Room


class AmenityCost(CostModel):
    def __init__(
        self,
        room_descriptions: list[Room],
        unavailable_cost: float = UNAVAILABLE_COST,
        amenity_utilization_coeff: float = 0.15,
        **kwargs
    ):
        """
        Class to calculate the amenity cost of all rooms:

        Room amenities are functionalities inherent to each room,
        such as a screen projector, a whiteboard, musical instruments
        etc. Rooms without the amenities listed in `required amenities`
        have very high cost (denoted unavailable_cost). Conversely, the
        amenity cost of rooms with all or some of the amenities listed
        in `required amenities` scales with the difference between the
        number of amenities in the room and the number of required
        amenities.

        Note: We assume that room amenities are fixed across time.

        Args:
            room_descriptions: list of Room objects describing the
                rooms in the building
            unavailable_cost: number assigned to a room w/o the
                needed amenities.
            coefficent: coefficient for adjusting the cost function
                to be more or less steep

        """
        self.room_descriptions = room_descriptions
        self.unavailable_cost = unavailable_cost
        self.coeff = amenity_utilization_coeff
        self.len_map = np.vectorize(len)

    @cached_property
    def room_amenities(self) -> list[set[str]]:
        """Amenities of all rooms"""
        return [room.amenities for room in self.room_descriptions]

    def _calculate_costs(self, required_amenities: set[str]) -> NDArray:
        """Calculate costs for each room-time combination"""
        return self.coeff * self.len_map(
            np.array(self.room_amenities) - required_amenities
        )

    def run(
        self,
        state: NDArray,
        n_time_slots: int,
        required_amenities: set[str] = set(),  # noqa: B006
        **kwargs
    ) -> NDArray:
        """
        Calculate the amenity cost for each room-time combination,
        setting the cost to a very high number if the room does not
        have the required amenities, i.e. is not useful.
        Rooms are 'useful' when 'required_amenities' is a subset of
        the room amenities. For useful rooms, the cost is given by
        a parameterized discrepancy between of the number of amenities
        in the room and the number of required amenities.

        Args:
            state: ones and zeros representing bookings
                shape = (n_rooms, n_time_slots)
            n_time_slots: number of time slots to consider
            required_amenities: required amenities for the
                booking, e.g. {"projector", "whiteboard"}

        Returns:
            cost: where the lower the better and very high if room
                does not have required amenities
                shape = (n_rooms*n_time_slots,)
        """
        useful_rooms = [*map(required_amenities.issubset, self.room_amenities)]
        utilization = self._calculate_costs(required_amenities)

        costs = np.where(useful_rooms, utilization, self.unavailable_cost)

        # return exploded values to match state's shape
        return np.tile(costs, n_time_slots)
