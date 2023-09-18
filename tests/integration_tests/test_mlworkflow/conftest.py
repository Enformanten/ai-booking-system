from pathlib import Path

import pandas as pd
import pytest

from thermo.config import WORKDIR


@pytest.fixture
def SCHOOLDIR() -> Path:
    yield WORKDIR / "buildings" / "demo_school"


@pytest.fixture
def MODELSDIR(SCHOOLDIR: Path) -> Path:
    yield SCHOOLDIR / "model"


@pytest.fixture
def DATADIR(SCHOOLDIR: Path) -> Path:
    yield SCHOOLDIR / "data"


@pytest.fixture
def raw_dataf(DATADIR: Path) -> pd.DataFrame:
    yield pd.read_pickle(DATADIR / "raw_data.pkl")


@pytest.fixture
def preprocessed_dataf(DATADIR: Path) -> pd.DataFrame:
    yield pd.read_pickle(DATADIR / "preprocessed_data.pkl")
