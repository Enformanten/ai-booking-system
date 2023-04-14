from abc import ABC, abstractmethod
from typing import Any

from numpy.typing import NDArray

from thermo.costs import CostModel


class Ranker(ABC):
    def __init__(self, costs: list[CostModel], config: dict[str, Any] | None = None):
        self.costs = costs
        self.config = config

    @abstractmethod
    def run(self, state: NDArray, **kwargs) -> NDArray:
        pass
