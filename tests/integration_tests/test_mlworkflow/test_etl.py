import pandas as pd
import pytest

from thermo.utils.room import Room


@pytest.mark.ml_integration
def test_datasize(raw_dataf: pd.DataFrame) -> None:
    assert raw_dataf.shape == (240, 11)


@pytest.mark.ml_integration
def test_column_names(raw_dataf: pd.DataFrame, demo_rooms: list[Room]) -> None:
    # given
    room_cols = {col for col in raw_dataf.columns if col.startswith("Room")}

    # then
    assert "electricity" in raw_dataf.columns  # there is an electricity col
    assert len(demo_rooms) == len(room_cols)  # all rooms are present


@pytest.mark.ml_integration
def test_binary_bookings(raw_dataf: pd.DataFrame):
    # given
    room_cols = [col for col in raw_dataf.columns if col.startswith("Room")]
    bookings = raw_dataf[room_cols].to_numpy()

    # then
    assert ((bookings == 0) | (bookings) == 1).all()  # check it is binary
