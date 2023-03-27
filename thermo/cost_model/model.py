import numpy as np
from numpy.typing import NDArray

from thermo.cost_model import adjacency


class HeatModel:
    def __init__(
        self,
        As: NDArray,
        n_time_slots: int,
        t_weight: float = 1.0,
        message_importance: float = 1.0,
        heat_cost: NDArray | None = None,
    ):
        """
        Args:
            As: Adjacency matrix for space (n_rooms x n_rooms)
            n_time_slots: number of time slots in the schedule
                (per day)
            tb_added.
        """
        self.As = As
        self.n_rooms = As.shape[0]
        self.n_time_slots = n_time_slots
        self.t_weight = t_weight
        self.heat_cost = heat_cost if heat_cost else np.ones(self.n_rooms)

        self.A = None

    def _get_full_graph(self):
        self.A = adjacency.get_time_adjacency(
            A=self.As, n_times=self.n_time_slots, time_weight=self.t_weight
        )
        # adjacency.validate_adjacency(self.A)

    def run(self, state: NDArray) -> NDArray:
        """
        Args:
            state: ones and zeros represnting bookings
                shape = (n_rooms*n_time_slots,), Its 1D!!

        Returns:
            cost_vector: where the lower the better.
                shape = (n_rooms*n_time_slots,), Its 1D!!
                if room already booked, its np.nan
        """
        if not self.A:
            self.A = self._get_full_graph()
        # TODO: to be completed.
        return np.nan * state
