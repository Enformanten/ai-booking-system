import numpy as np
from numpy.typing import NDArray

from thermo.costs.base import CostModel
from thermo.utils.room import Room


class CapacityCost(CostModel):
    def __init__(
        self,
        room_descriptions: list[Room],
        n_time_slots: int,
        big_number: float = 1e5,
        coefficent: float = 1.0,
    ):
        """
        Class to simulate the capacity cost of a room:
        Room capacity cost is intuitively based on a Lennard-Jones
        potential function with a minimum at the required capacity.
        Rooms with capacity < required capacity have very high cost,
        while the cost for rooms with capacity >= required capacity
        scales with the difference between the room capacity and
        required capacity.

        Note: We assume that room capacities are fixed across time.

        Args:
            room_descriptions: list of Room objects describing the
                rooms in the building
            n_time_slots: number of time slots to consider
            big_number: number associated to the room already
                being booked
            coefficent: coefficient for adjusting the cost function
                to be more or less steep

        """
        self.room_descriptions = room_descriptions
        self.n_time_slots = n_time_slots
        self.big_number = big_number
        self.coeff = coefficent

    @property
    def capacities(self) -> list[int]:
        """Capacities of all rooms"""
        return [room.capacity for room in self.room_descriptions]

    def _explode_capacities(
        self, capacities: list[int], shape: tuple[int, int]
    ) -> NDArray:
        """Explode capacities to match state shape"""
        return np.repeat(capacities, shape[1]).reshape(shape).T.flatten()

    def _calculate_costs(
        self, rt_capacities: NDArray, required_capacity: int
    ) -> NDArray:
        """Calculate costs for each room-time combination"""
        return self.coeff * (rt_capacities - required_capacity) / rt_capacities

    def run(self, state: NDArray, required_capacity: int = 10) -> NDArray:
        """
        Calculate the capacity cost for each room-time combination,
        setting the cost to a very high number if the room is too small
        or already booked.

        Args:
            state: ones and zeros representing bookings
                shape = (n_rooms, n_time_slots)
            required_capacity: required room capacity to
                hold the party of the booker.

        Returns:
            cost: where the lower the better and very high if room
                is too small or already booked.
                shape = (n_rooms*n_time_slots,)
        """

        rt_capacities = self._explode_capacities(
            self.capacities, shape=(len(self.capacities), self.n_time_slots)
        )
        capacity_costs = self._calculate_costs(rt_capacities, required_capacity)

        # check if room is too small or already booked
        _filter = rt_capacities < required_capacity | (state == 1)
        costs = np.where(_filter, self.big_number, capacity_costs)

        return costs.flatten()
