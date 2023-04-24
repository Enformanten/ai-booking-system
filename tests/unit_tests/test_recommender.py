from datetime import date

import numpy as np
import pytest
from numpy.typing import NDArray

from tests.conftest import powerset
from thermo.costs import CostName, make_cost
from thermo.ranker import Ranker, make_ranker
from thermo.recommender import Recommendation, Recommender


class MockRanker(Ranker):
    def __init__(self):
        super().__init__(costs=[])

    def run(self, state: NDArray, seed: int = 42, **kwargs) -> NDArray:
        rng = np.random.default_rng(seed)
        return state + rng.random(state.shape)


@pytest.fixture
def recommender(demo_building):
    return Recommender(
        building=demo_building,
        ranker=MockRanker(),
    )


def test_recommendation(recommender):
    recommendation = recommender.run(date(2023, 4, 20))
    assert isinstance(recommendation, Recommendation)
    assert recommendation.shape == (8, 10)


@pytest.mark.parametrize(
    "day, room, score",
    [(date(2023, 10, 1), "Room D", 0.0058), (date(2023, 12, 5), "Room B", 0.0012)],
)
def test_top_recommendation(recommender, day, room, score):
    # by using 2 different dates I test that I get different results :)
    recommendation = recommender.run(day, seed=day.day)
    top = recommendation.top_recommendations().iloc[0]
    assert top["Room"] == room
    assert np.isclose(top["Score"], score, rtol=1e-2)


@pytest.mark.parametrize("costs", powerset(CostName.__args__))
def test_multiple_costs(costs, demo_building):
    """Validates that the recommender can handle
    multiple costs. Runs through the powerset of all
    cost models implemented (listed in costs.CostName).
    """
    _costs = [make_cost(cost_name=c, **demo_building.__dict__) for c in costs]
    recommender = Recommender(
        building=demo_building,
        ranker=make_ranker(demo_building.ranker, _costs),
    )
    recommendation = recommender.run(date(2023, 4, 20))
    assert isinstance(recommendation, Recommendation)
    assert recommendation.shape == (8, 10)
