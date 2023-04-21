from datetime import date

import numpy as np
import pytest
from numpy.typing import NDArray

from thermo.ranker import Ranker
from thermo.recommender import Recommendation, Recommender


class MockRanker(Ranker):
    def __init__(self):
        super().__init__(costs=[])

    def run(self, state: NDArray, seed: int = 42, **kwargs) -> NDArray:
        rng = np.random.default_rng(seed)
        return state + rng.random(state.shape)


@pytest.fixture
def recommender(demo_room_description):
    return Recommender(
        building_name="mock",
        room_description=demo_room_description,
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
