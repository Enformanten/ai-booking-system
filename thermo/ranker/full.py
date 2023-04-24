from numpy.typing import NDArray

from thermo.costs import CostModel
from thermo.ranker.base import Ranker


class FullRanker(Ranker):
    """
    Calculates the cost for the full schedule:
    i.e. all rooms for all time slots.
    The total cost is computed as the sum of individual costs.
    Args:
        costs: list of instances of costs models to compute the costs from.
    """

    def __init__(self, costs: list[CostModel]):
        super().__init__(costs=costs)

    def run(self, state: NDArray, **kwargs) -> NDArray:
        """
        Adds up costs from individual cost sources, to return
        the cost of booking a given room for a given time slot.
        Args:
            state: state: a flat array containing 1 if the room is booked
                at that time a zero otherwise.
            kwargs: other possible arguments to the run method.

        Returns:
            An array of the same shape as the state, containing the costs.
        """
        return sum(cost.run(state, **kwargs) for cost in self.costs)
