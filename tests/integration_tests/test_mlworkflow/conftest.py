from pathlib import Path

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
