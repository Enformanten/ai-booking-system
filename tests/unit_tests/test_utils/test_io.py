from pathlib import Path

import numpy as np
import pytest
from numpy.typing import NDArray
from scipy.linalg import issymmetric

from thermo.utils import io
from thermo.utils.building import Building


class TestBuilding:
    @pytest.fixture(autouse=True)
    def load_building_config(self, tmp_path) -> None:
        yield

    def test_config_dont_exist(self) -> None:
        """Tests that an error is raised if the building
        does not exist"""
        with pytest.raises(FileExistsError):
            _ = io.get_building_path("non_existent_building")

    def test_config_exists(self, demo_building_name: str) -> None:
        """Tests that the config exists for the given building."""
        building_path = io.get_building_path(demo_building_name)
        assert isinstance(building_path, Path)

    def test_building_specs(
        self, core_building_specs: set, all_buildings: list[Building]
    ) -> None:
        """Tests that the correct properties, in the correct
        formats, are present in all building specs.
        args:
           core_building_specs: list of properties that must
               be present in all building specs.
           all_buildings: list of all building dirs found in
               the buildings directory.
        """
        for building in all_buildings:
            assert core_building_specs <= building.__dict__.keys()
            assert issymmetric(building.adjacency)
            assert len(building.room_descriptions) == building.adjacency.shape[0]

    def test_load_adjacency(
        self, demo_building_specs: set, demo_graph: NDArray
    ) -> None:
        """Tests that the loaded adjacency matrix is the same as the
        static demo adjacency matrix."""
        assert np.allclose(demo_building_specs.adjacency, demo_graph)
