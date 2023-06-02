import pytest

from thermo.stages.get_data import select_bookings_data


@pytest.mark.parametrize(
    "method, expected",
    [
        ("binary", [0, 1, 1, 0, 1, 0, 0, 0, 0]),
        ("fractional", [0, 1, 0.5, 0, 1, 0, 0, 0, 0]),
    ],
)
def test_select_bookings(mock_raw_booking1, method, expected):
    result = select_bookings_data(mock_raw_booking1, aggregation_method=method)

    assert result["ROOM_A_booked"].to_list() == expected
    assert result.shape == (9, 1)
