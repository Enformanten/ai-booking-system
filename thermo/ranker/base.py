from abc import ABC, abstractmethod
from typing import Any

from numpy.typing import NDArray

from thermo.costs import CostModel


class Ranker(ABC):
    """
    Abstract class to make rankers from.
    Args:
        costs: list of instances of costs models to compute the costs from.
        config: user defined configuration.
    """

    def __init__(self, costs: list[CostModel], config: dict[str, Any] | None = None):
        self.costs = costs
        self.config = config

    @abstractmethod
    def run(self, state: NDArray, **kwargs) -> NDArray:
        """
        Base method, that computes the cost given the current
        state of bookings and some internal parameters.

        Args:
            state: a flat array containing 1 if the room is booked
                at that time a zero otherwise.
            kwargs: other possible arguments to the run method.

        Returns:
            An array of the same shape as the state, containing the costs.
        """
        pass
