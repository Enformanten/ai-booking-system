from abc import ABC, abstractmethod
from typing import Any

from costs import CostModel
from numpy.typing import NDArray


class Ranker(ABC):
    def __init__(self, costs: list[CostModel], config: dict[str, Any]):
        self.costs = costs

    @abstractmethod
    def run(self, schedule: NDArray) -> list:
        pass
