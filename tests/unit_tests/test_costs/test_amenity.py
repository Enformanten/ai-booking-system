import numpy as np
import pytest
from numpy.typing import NDArray

from thermo.costs.amenity import AmenityCost
from thermo.utils.room import Room


@pytest.mark.parametrize(
    "amenities,coeff,expected",
    [
        (
            {"projector"},
            0.4,
            np.array(
                [
                    [
                        0.4,
                        100000.0,
                        0.0,
                        0.4,
                        100000.0,
                        100000.0,
                        100000.0,
                        100000.0,
                        0.8,
                        100000.0,
                    ],
                ]
                * 3  # noqa: W503
            ),
        ),
        (
            {"projector", "whiteboard"},
            0.1,
            np.array(
                [
                    [
                        0.0,
                        100000.0,
                        100000.0,
                        0.0,
                        100000.0,
                        100000.0,
                        100000.0,
                        100000.0,
                        0.1,
                        100000.0,
                    ],
                ]
                * 3  # noqa: W503
            ),
        ),
        (
            {"projector", "whiteboard", "screen"},
            0.05,
            np.array(
                [
                    [
                        100000.0,
                        100000.0,
                        100000.0,
                        100000.0,
                        100000.0,
                        100000.0,
                        100000.0,
                        100000.0,
                        0.0,
                        100000.0,
                    ]
                ]
                * 3  # noqa: W503
            ),
        ),
        (
            set(),
            0.1,
            np.array([[0.2, 0.1, 0.1, 0.2, 0, 0.1, 0.2, 0.1, 0.3, 0]] * 3),
        ),
    ],
)
def test_capacity(
    timeslots: int,
    demo_rooms: list[Room],
    demo_state: NDArray,
    amenities: set[str],
    coeff: float,
    expected: NDArray,
) -> None:
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
    timeslots: int, demo_rooms: list[Room], demo_state: NDArray
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
