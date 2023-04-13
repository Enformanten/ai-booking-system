import numpy as np

from thermo.cost_model.model import HeatModel


def test_heating(graph, timeslots, state):
    model = HeatModel(graph, n_time_slots=timeslots)
    expected = np.array(
        [
            [1.0, 0.5, 100000.5, 100000.5, 0.5, 1.0, 0.5, 1.0, 1.0, 0.5],
            [1.0, 1.0, 0.5, 0.5, 100001.0, 0.5, 0.0, 0.5, 1.0, 1.0],
            [1.0, 0.5, 1.0, 0.5, 0.0, 1.0, 100001.0, 1.0, 1.0, 1.0],
        ]
    )
    assert np.allclose(model.run(state).reshape(timeslots, -1), expected)
