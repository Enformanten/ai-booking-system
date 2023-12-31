import pytest

from thermo.stages.preprocessing import mock_ventilation


@pytest.mark.parametrize(
    "dataf, expected",
    [
        ("mock_binary_booking", [1, 0, 0, 1, 0, 0, 0, 0, 0]),
        ("mock_fractional_booking", [1, 0, 0.5, 1, 0, 0, 0, 0, 0]),
        ("mock_unused", 9 * [0]),
        ("mock_morning_weekend", [0] + 7 * [1] + [0, 0, 1, 0, 0, 0, 0, 0]),
        # ("mock_evening_weekend", 10*[0] +[1, 0, 0, 0, 0, 0]),
    ],
)
def test_ventilation(dataf, expected, request):
    """
    Test that mock_ventilation is in day mode the correct
    hours for different inputs.
    """
    dataf = request.getfixturevalue(dataf)
    result = mock_ventilation(dataf, params={"is_day": True})
    assert result.shape == (len(expected), 2)
    assert result["ROOM_A_day"].to_list() == expected
