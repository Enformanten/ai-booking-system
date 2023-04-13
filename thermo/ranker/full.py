from numpy.typing import NDArray

from thermo.ranker.base import Ranker


class FullRanker(Ranker):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

    def run(self, schedule: NDArray, **kwargs) -> NDArray:
        return sum(cost.run(schedule, **kwargs) for cost in self.costs)
