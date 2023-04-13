from abc import ABC, abstractmethod
from typing import Any


class Ranker(ABC):
    def __init__(self, costs: list, config: dict[str, Any]):
        self.costs = costs

    @abstractmethod
    def run(self, schedule: Any) -> list:
        pass
