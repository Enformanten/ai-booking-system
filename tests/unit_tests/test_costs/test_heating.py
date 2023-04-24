import numpy as np

from thermo.costs.heating import HeatingCost


def test_heating(demo_graph, timeslots, demo_state):
    model = HeatingCost(adjacency=demo_graph)
    expected = np.array(
        [
            [1.0, 0.5, 100000.5, 100000.5, 0.5, 1.0, 0.5, 1.0, 1.0, 0.5],
            [1.0, 1.0, 0.5, 0.5, 100001.0, 0.5, 0.0, 0.5, 1.0, 1.0],
            [1.0, 0.5, 1.0, 0.5, 0.0, 1.0, 100001.0, 1.0, 1.0, 1.0],
        ]
    )
    assert np.allclose(
        model.run(demo_state, n_time_slots=timeslots).reshape(timeslots, -1), expected
    )
