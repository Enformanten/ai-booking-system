import numpy as np
import pytest

from thermo.utils.io import load_adjacency


class TestSubscription:
    @pytest.fixture(autouse=True)
    def subscription_path(self, tmp_path):
        self.path = tmp_path
        # TODO: Save the adjacency for graph to a file in self.path
        # TODO: Save a config to a file in self.path
        yield

    def test_load_adjacency(self, graph):
        adjacency = load_adjacency(self.path)
        assert np.all(adjacency == graph)
