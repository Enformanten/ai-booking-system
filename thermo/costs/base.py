from abc import ABC, abstractmethod

from numpy.typing import NDArray


class CostModel(ABC):
    @abstractmethod
    def run(self, state: NDArray, **kwargs) -> NDArray:
        pass
