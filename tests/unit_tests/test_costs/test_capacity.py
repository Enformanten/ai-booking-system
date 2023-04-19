import numpy as np

from thermo.costs.capacity import CapacityCost


def test_heating(timeslots, room_description, state):
    model = CapacityCost(room_description, n_time_slots=timeslots)
    expected = np.array(
        [
            [0.57, 0.35, 100000.0, 0.57, 0.13, 0.57, 0.13, 0.57, 100000.0, 0.57],
            [0.57, 0.35, 100000.0, 0.57, 0.13, 0.57, 0.13, 0.57, 100000.0, 0.57],
            [0.57, 0.35, 100000.0, 0.57, 0.13, 0.57, 0.13, 0.57, 100000.0, 0.57],
        ]
    )
    costs = model.run(state, required_capacity=13).round(2).reshape(timeslots, -1)
    assert np.allclose(costs, expected)
