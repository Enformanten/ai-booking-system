import numpy as np

from thermo.ranker.full import FullRanker


def test_fullranker(state, mock_heatingcost, mock_occupationcost):
    ranker = FullRanker(costs=[mock_occupationcost, mock_heatingcost])
    ranking = ranker.run(state=state)
    expected = np.array(
        [
            1.22604395,
            1.56112156,
            2001.14140,
            2001.30263,
            1.90582265,
            1.02437765,
            1.23886030,
            1.21393569,
            1.87188637,
            1.54961406,
            1.62920198,
            1.07323501,
            1.35613488,
            1.17723839,
            2001.55659,
            1.77276128,
            1.44541521,
            1.93618274,
            1.17236883,
            1.36833560,
            1.24191226,
            1.64547403,
            1.02930198,
            1.10687888,
            1.22161650,
            1.80536129,
            2001.53328,
            1.95619623,
            1.84571051,
            1.31695105,
        ]
    )
    assert ranking.shape == state.shape
    assert np.allclose(ranking, expected)
