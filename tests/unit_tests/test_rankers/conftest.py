import numpy as np
import pytest

from thermo.costs.base import CostModel


class MockCost(CostModel):
    def __init__(self, seed: int = 42):
        self.rng = np.random.default_rng(42)

    def run(self, state: np.typing.NDArray, **kwargs) -> np.typing.NDArray:
        return state * 1000 + 1 - 0.5 * self.rng.random(state.shape)


@pytest.fixture
def mock_heatingcost():
    return MockCost(42)


@pytest.fixture
def mock_occupationcost():
    return MockCost(30)
