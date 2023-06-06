import pytest

from thermo.stages.get_data import select_bookings_data


@pytest.mark.parametrize(
    "method, expected",
    [
        ("binary", "mock_binary_booking"),
        ("fractional", "mock_fractional_booking"),
    ],
)
def test_select_bookings(mock_raw_booking, method, expected, request):
    """
    Test that the bookings for a particular room are aggregated correctly,
    and the time stamp is used accordingly.
    """
    expected = request.getfixturevalue(expected)
    result = select_bookings_data(mock_raw_booking, aggregation_method=method)

    assert (result == expected).all(axis=None)
    assert result.shape == (9, 1)
