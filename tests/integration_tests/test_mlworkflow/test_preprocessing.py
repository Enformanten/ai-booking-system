import pandas as pd
import pytest

from thermo.utils.room import Room


@pytest.mark.ml_integration
def test_drop_nights(preprocessed_dataf: pd.DataFrame) -> None:
    # then we lost some data
    assert len(preprocessed_dataf) == 111  # not 240 as raw data


@pytest.mark.ml_integration
def test_columns(demo_rooms: list[Room], preprocessed_dataf: pd.DataFrame) -> None:
    # given
    room_names = {room.name[-1] for room in demo_rooms}  # Room A, Room B,...
    booked_rooms = {
        col.split("_")[0][-1]
        for col in preprocessed_dataf.columns
        if col.endswith("_booked")
    }  # Room-A_booked, Room-B_booked, ...
    day_rooms = {
        col.split("_")[0][-1]
        for col in preprocessed_dataf.columns
        if col.endswith("_day")
    }  # Room-A_day, Room-B_day, ...

    # then
    assert room_names == booked_rooms
    assert room_names == day_rooms
