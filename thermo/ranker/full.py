from numpy.typing import NDArray

from thermo.costs import CostModel
from thermo.ranker.base import Ranker


class FullRanker(Ranker):
    def __init__(self, costs=list[CostModel]):
        super().__init__(costs=costs)

    def run(self, state: NDArray, **kwargs) -> NDArray:
        return sum(cost.run(state, **kwargs) for cost in self.costs)
