from functools import lru_cache

import numpy as np
from numpy.typing import NDArray

from thermo.config import UNAVAILABLE_COST
from thermo.costs.base import CostModel
from thermo.utils.room import Room


class CapacityCost(CostModel):
    def __init__(
        self,
        room_descriptions: list[Room],
        capacity_utilization_coeff: float = 1.0,
        unavailable_cost: float = UNAVAILABLE_COST,
        **kwargs
    ):
        """
        Class to simulate the capacity cost of a room:

        Room capacity cost is intuitively based on a Lennard-Jones
        potential function with a minimum at the required capacity.
        Rooms with `capacity` < `required capacity` have very high cost
        (unavailable_cost), while the cost for rooms with `capacity`
        >= `required capacity` scales with the difference between the
        room capacity and required capacity.

        Note: We assume that room capacities are fixed across time.

        Args:
            room_descriptions: list of Room objects describing the
                rooms in the building
            unavailable_cost: number associated to the room already
                being booked
            coefficent: coefficient for adjusting the cost function
                to be more or less steep

        """
        self.room_descriptions = room_descriptions
        self.coeff = capacity_utilization_coeff
        self.unavailable_cost = unavailable_cost

    @property
    def room_capacities(self) -> NDArray:
        """Capacities of all rooms"""
        return np.array([room.capacity for room in self.room_descriptions], dtype=int)

    @property
    def n_rooms(self) -> int:
        """Number of rooms"""
        return self.room_capacities.shape[0]

    @staticmethod
    @lru_cache(maxsize=5)
    def _explode_to_shape(capacities: tuple[int], shape: tuple[int, int]) -> NDArray:
        """Explode capacities to match state shape"""
        return np.repeat(capacities, shape[1]).reshape(shape).T

    def _calculate_costs(self, capacities: NDArray, required_capacity: int) -> NDArray:
        """Calculate costs for each room-time combination"""
        return self.coeff * (capacities - required_capacity) / capacities

    def run(
        self, state: NDArray, n_time_slots: int, required_capacity: int = 10, **kwargs
    ) -> NDArray:
        """
        Calculate the capacity cost for each room-time combination,
        setting the cost to a very high number if the room is too small.

        Args:
            state: ones and zeros representing bookings
                shape = (n_rooms, n_time_slots)
            n_time_slots: number of time slots to consider
            required_capacity: required room capacity to
                hold the party of the booker.

        Returns:
            cost: where the lower the better and very high if room
                is too small. Shape = (n_rooms*n_time_slots,)
        """

        _filter = self.room_capacities < required_capacity
        capacity_costs = self._calculate_costs(self.room_capacities, required_capacity)
        room_costs = np.where(_filter, self.unavailable_cost, capacity_costs)

        room_time_capacities = self._explode_to_shape(
            tuple(room_costs),  # cast to tuple for hashability
            shape=(self.n_rooms, n_time_slots),
        )
        return room_time_capacities.flatten()
