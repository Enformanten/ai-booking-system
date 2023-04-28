from pathlib import Path
from typing import Generator

import numpy as np
import pytest
from numpy.typing import NDArray
from scipy.linalg import issymmetric

from thermo.utils import io
from thermo.utils.building import Building


def test_config_dont_exist() -> None:
    """Tests that an error is raised if the building
    does not exist"""
    with pytest.raises(FileExistsError):
        _ = io.get_building_path("non_existent_building")


def test_config_exists(demo_building_name: Generator[str, None, None]) -> None:
    """Tests that the config exists for the given building."""
    building_path = io.get_building_path(demo_building_name)
    assert isinstance(building_path, Path)


def test_building_specs(
    core_building_specs: Generator[set, None, None],
    all_buildings: Generator[list[Building], None, None],
) -> None:
    """Tests that the correct properties, in the correct
    formats, are present in all building specs files.
    args:
        core_building_specs: list of properties that must
            be present in all building specs.
        all_buildings: list of all building dirs found in
            the buildings directory.
    """
    for building in all_buildings:
        assert core_building_specs <= building.specifications.keys()
        assert issymmetric(building.adjacency)
        assert len(building.room_descriptions) == building.adjacency.shape[0]
        assert all(isinstance(a, set) for a in building.get_room_attr("amenities"))


def test_load_adjacency(
    demo_building_from_config: Generator[Building, None, None],
    demo_graph: Generator[NDArray, None, None],
) -> None:
    """Tests that the loaded adjacency matrix is the same as the
    static demo adjacency matrix."""
    assert np.allclose(demo_building_from_config.adjacency, demo_graph)


@pytest.mark.parametrize(
    "file_name", ["adjacency.json", "specifications.yaml", "config.yaml"]
)
def test_file_loader(
    file_name: str, demo_building_name: Generator[str, None, None]
) -> None:
    """Tests that the file loader returns a dict."""
    building_path = io.get_building_path(demo_building_name)
    _data = io.load_file(building_path, file_name)
    assert isinstance(_data, dict)


def test_file_loader_error(demo_building_name: Generator[str, None, None]) -> None:
    """Tests that an error is raised if the file type is not supported."""
    building_path = io.get_building_path(demo_building_name)
    with pytest.raises(FileNotFoundError):
        _ = io.load_file(building_path, "adjacency.csv")


def test_load_building(demo_building_name: Generator[str, None, None]) -> None:
    """Tests that the building loader returns a Building object."""
    building_path = io.get_building_path(demo_building_name)
    building = io.load_building(building_path)
    assert isinstance(building, Building)
