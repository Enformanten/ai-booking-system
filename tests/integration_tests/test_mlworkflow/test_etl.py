from pathlib import Path

import pandas as pd
import pytest


@pytest.mark.ml_integration
def test_datasize(DATADIR: Path) -> None:
    # given
    dataf = pd.read_pickle(DATADIR / "raw_data.pkl")

    # then
    assert dataf.shape == (240, 11)
