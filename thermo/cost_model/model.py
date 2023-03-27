import numpy as np
from numpy.typing import NDArray


class HeatModel:
    def __init__(
        self,
        As: NDArray,
        n_time_slots: int,
        t_weight: float = 1,
        heat_cost: NDArray | None = None,
    ):
        self.As = As
        self.n_time_slots = n_time_slots
        self.t_weight = t_weight
        self.heat_cost = heat_cost if heat_cost else np.ones(As.shape[0])

    def run(s: NDArray) -> NDArray:
        pass
