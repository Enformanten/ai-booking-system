from typing import Generator

import numpy as np
import pytest
from numpy.typing import NDArray

from tests.unit_tests.test_costs.test_cases import AMENITY_TEST_CASES
from thermo.costs.amenity import AmenityCost
from thermo.utils.room import Room


@pytest.mark.parametrize(
    "amenities, coeff, expected",
    *AMENITY_TEST_CASES,
)
def test_amenity(
    timeslots: Generator[int, None, None],
    demo_rooms: Generator[list[Room], None, None],
    demo_state: Generator[NDArray, None, None],
    amenities: set[str],
    coeff: float,
    expected: NDArray,
) -> None:
    """Test that amenity cost is calculated deterministically."""

    model = AmenityCost(demo_rooms, amenity_utilization_coeff=coeff)

    costs = (
        model.run(
            demo_state,
            n_time_slots=timeslots,
            required_amenities=amenities,
        )
        .round(2)
        .reshape(timeslots, -1)
    )
    assert np.allclose(costs, expected, atol=1e-5)


def test_homogenity(
    timeslots: Generator[int, None, None],
    demo_rooms: Generator[list[Room], None, None],
    demo_state: Generator[NDArray, None, None],
) -> None:
    """Since the amenity cost is state independent,
    the row-wise cost should be the same for all time slots."""

    model = AmenityCost(demo_rooms, amenity_utilization_coeff=0.1)
    costs = (
        model.run(
            demo_state,
            n_time_slots=timeslots,
            required_amenities={"projector"},
        )
        .round(2)
        .reshape(timeslots, -1)
    )
    assert np.unique(costs, axis=0).shape == (1, len(demo_rooms))
