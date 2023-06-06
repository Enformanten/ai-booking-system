import pytest

from thermo.stages.get_data import select_bookings_data


@pytest.mark.parametrize(
    "method, expected",
    [
        ("binary", "mock_binary_booking"),
        ("fractional", "mock_fractional_booking"),
    ],
)
def test_select_bookings(mock_raw_booking1, method, expected, request):
    expected = request.getfixturevalue(expected)
    result = select_bookings_data(mock_raw_booking1, aggregation_method=method)

    assert (result == expected).all(axis=None)
    assert result.shape == (9, 1)
