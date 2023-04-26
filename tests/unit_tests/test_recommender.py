from datetime import date
from typing import Iterable

import numpy as np
import pytest
from numpy.typing import NDArray

from tests.conftest import powerset
from thermo.costs import CostName, make_cost
from thermo.ranker import Ranker, make_ranker
from thermo.recommender import Recommendation, Recommender
from thermo.utils.building import Building


class MockRanker(Ranker):
    def __init__(self):
        super().__init__(costs=[])

    def run(self, state: NDArray, seed: int = 42, **kwargs) -> NDArray:
        rng = np.random.default_rng(seed)
        return state + rng.random(state.shape)


@pytest.fixture
def demo_recommender(demo_building: Building) -> Recommender:
    return Recommender(
        building=demo_building,
        ranker=MockRanker(),
    )


def test_recommendation(demo_recommender: Recommender) -> None:
    recommendation = demo_recommender.run(date(2023, 4, 20))
    assert isinstance(recommendation, Recommendation)
    assert recommendation.shape == (8, 10)


@pytest.mark.parametrize(
    "day, room, score",
    [(date(2023, 10, 1), "Room D", 0.0058), (date(2023, 12, 5), "Room B", 0.0012)],
)
def test_top_recommendation(
    demo_recommender: Recommender, day: date, room: str, score: float
) -> None:
    """Tests that Recommender yields deterministic results
    for a given day."""
    recommendation = demo_recommender.run(day, seed=day.day)
    top = recommendation.top_recommendations().iloc[0]
    assert top["Room"] == room
    assert np.isclose(top["Score"], score, rtol=1e-2)


@pytest.mark.parametrize("cost_names", powerset(CostName.__args__))
def test_multiple_costs(
    cost_names: Iterable[set[str]], demo_building: Building
) -> None:
    """Validates that the recommender can handle
    multiple costs. Runs through the powerset of all
    implemented cost models, listed in costs.CostName.
    """
    del demo_building.name  # conflict w/ make_cost name
    _costs = [make_cost(name=c, **demo_building.specifications) for c in cost_names]
    recommender = Recommender(
        building=demo_building,
        ranker=make_ranker(demo_building.ranker, _costs),
    )
    recommendation = recommender.run(date(2023, 4, 20))
    assert isinstance(recommendation, Recommendation)
    assert recommendation.shape == (8, 10)
