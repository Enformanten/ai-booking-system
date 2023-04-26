import numpy as np
from numpy.typing import NDArray

from thermo.costs.base import CostModel
from thermo.utils.room import Room


class AmenityCost(CostModel):
    def __init__(
        self,
        room_descriptions: list[Room],
        big_number: float = 1e5,
        coefficent: float = 1.0,
        **kwargs
    ):
        """
        Class to simulate the amenity cost of a room:

        Room amenities are functionalities inherent to each room, such
        as a screen projector, a whiteboard, musical instruments etc.
        Rooms without the amenities listed in `required amenities` have
        very  high cost. Conversely, the amenity cost of rooms with all
        or some of the amenities listed  in `required amenities` is given
        by cost=high_cost * (needed_amenities_in_room / all_amenities_in_room)

        Note: We assume that room amenities are fixed across time.

        Args:
            room_description: list of Room objects describing the
                rooms in the building
            big_number: number associated to the room already
                being booked
            coefficent: coefficient for adjusting the cost function
                to be more or less steep

        """
        self.room_descriptions = room_descriptions
        self.big_number = big_number
        self.coeff = coefficent
        self.len_map = np.vectorize(len)

    @property
    def room_amenities(self) -> list[int]:
        """Amenities of all rooms"""
        return [room.amenities for room in self.room_descriptions]

    @staticmethod
    def _explode_to_shape(values: list[int], shape: tuple[int, int]) -> NDArray:
        """Explode values to match state shape"""
        return np.repeat(values, shape[1]).reshape(shape).T.flatten()

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

        costs = np.where(useful_rooms, utilization, self.big_number)

        rt_costs = self._explode_to_shape(costs, shape=(len(costs), n_time_slots))
        return rt_costs
