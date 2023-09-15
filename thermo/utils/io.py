import json
from io import TextIOWrapper
from pathlib import Path
from typing import Any

import yaml
from numpy import load as npload
from numpy.typing import NDArray

from thermo.config import BUILDINGS_DIR
from thermo.utils.building import Building


def get_building_path(building_name: str) -> Path:
    """
    Validates and returns the path to the building
    config dir. Raises an error if the dir does
    not exist.

    Args:
        building_name: name of the building.

    Returns:
        pathlib.Path: path to the building config dir.
    """
    building_path = BUILDINGS_DIR / building_name
    if not building_path.exists():
        raise FileExistsError(f"Building '{building_name}' does not exist.")
    return building_path


def load_yaml(config: TextIOWrapper, **kwargs) -> dict[str, Any]:
    """Loads a yaml file from the given path."""
    return yaml.safe_load(config, **kwargs)


def load_json(config: TextIOWrapper, **kwargs) -> dict[str, Any]:
    """Loads a json file from the given path."""
    return json.load(config, **kwargs)


def load_npy(building_path: Path, filename: str, **kwargs) -> NDArray:
    return npload(building_path / filename)


def load_file(building_path: Path, file_name: str, **kwargs) -> dict[str, Any]:
    """Loads a file from the given path. Pathlib
    handles context management for us."""
    p = Path(building_path / file_name)
    config = p.open("r")

    match p.suffix:
        case ".yaml":
            return load_yaml(config, **kwargs)
        case ".json":
            return load_json(config, **kwargs)
        case _:
            raise ValueError(f"File type {p.suffix} not supported.")


def load_building(building_path: Path) -> Building:
    """Loads relevant files from building config dir.
    and loads them into a Building object."""

    _adjacency = {"adjacency": load_npy(building_path, "adjacency.npy")}
    _specs = load_file(building_path, "specifications.yaml")
    _config = load_file(building_path, "config.yaml")

    data = _adjacency | _specs | _config
    return Building(**data)  # type: ignore[arg-type]


def load_all_buildings() -> list[Building]:
    """
    Returns a list of all buildings found in the
    BUILDINGS_DIR as Building objects.
    Returns:
        list[Building]: list of all buildings.
    """
    return [
        load_building(building_dir)
        for building_dir in BUILDINGS_DIR.glob("*")
        if building_dir.is_dir()
    ]
