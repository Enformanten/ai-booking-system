from pathlib import Path

import pandas as pd
import pytest

from thermo.utils.room import Room


@pytest.fixture
def raw_dataf(DATADIR: Path) -> pd.DataFrame:
    yield pd.read_pickle(DATADIR / "raw_data.pkl")


@pytest.mark.ml_integration
def test_datasize(raw_dataf: pd.DataFrame) -> None:
    assert raw_dataf.shape == (240, 11)


@pytest.mark.ml_integration
def test_column_names(raw_dataf: pd.DataFrame, demo_rooms: list[Room]) -> None:
    # given
    room_cols = {col for col in raw_dataf.columns if col.startswith("Room")}

    # then
    assert "electricity" in raw_dataf.columns
    assert len(demo_rooms) == len(room_cols)
