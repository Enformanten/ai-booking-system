from datetime import date

import pytest

from thermo.utils.time import is_schoolday


@pytest.mark.parametrize(
    "day, expected",
    [
        (date(2023, 4, 20), True),
        (date(2023, 4, 22), False),  # Saturday
        (date(2023, 2, 16), False),  # Winter holiday
        (date(2023, 5, 18), False),  # Ascension day
        (date(2023, 5, 19), False),  # Ascension Friday
    ],
)
def test_is_schoolday(day, expected):
    assert expected == is_schoolday(day)
