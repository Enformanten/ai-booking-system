import numpy as np
from numpy.typing import NDArray

from thermo.config import UNAVAILABLE_COST
from thermo.costs import adjacency
from thermo.costs.base import CostModel


class HeatingCost(CostModel):
    def __init__(
        self,
        *,
        adjacency: NDArray,
        t_weight: float = 1.0,
        message_importance: float = 0.5,
        heat_cost: NDArray | None = None,
        unavailable_cost: float = UNAVAILABLE_COST,
        **kwargs
    ):
        """
        Class to simulate the heating cost of a room.
        Args:
            adjacency: Adjacency matrix for space (n_rooms x n_rooms)
                tb_added.
            unavailable_cost: number associated to the room already
                being booked
            t_weight: weight of time in the adjacency matrix
            message_importance: weight of the message in the cost
                function
            heat_cost: cost of heating each room
        """
        self.As = adjacency
        self.n_rooms = self.As.shape[0]
        self.t_weight = t_weight
        self.message_importance = message_importance
        self.heat_cost = heat_cost if heat_cost else np.ones(self.n_rooms)
        self.unavailable_cost = unavailable_cost

    def _get_full_graph(self, n_time_slots: int):
        return adjacency.get_time_adjacency(
            A=self.As, n_times=n_time_slots, time_weight=self.t_weight
        )

    def _get_full_cost(self, n_time_slots: int):
        return np.hstack([self.heat_cost] * n_time_slots)

    def run(self, state: NDArray, n_time_slots: int, **kwargs) -> NDArray:
        """
        Compute the cost of each possible booking given the current state
        of the booking.

        Args:
            state: ones and zeros representing bookings
                shape = (n_rooms*n_time_slots,),
            n_time_slots: number of time slots in the schedule
                (per day)

        Returns:
            cost_vector: where the lower the better.
                shape = (n_rooms*n_time_slots,),
                if room already booked, its np.nan
        """
        if not hasattr(self, "A"):
            self.A = self._get_full_graph(n_time_slots=n_time_slots)

        if not hasattr(self, "_full_heat_cost"):
            self._full_heat_cost = self._get_full_cost(n_time_slots=n_time_slots)

        out = self._full_heat_cost - self.message_importance * np.matmul(self.A, state)
        return self.unavailable_cost * state + out
