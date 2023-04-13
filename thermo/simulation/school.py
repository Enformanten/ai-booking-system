from typing import List

import numpy as np

from thermo.simulation.heater import Heater


class School:
    def __init__(self, adjacency_matrix: np.ndarray, k_out: float, k_int: float):
        """
        School class to contain school parameters
        Args:
            adjacency_matrix (np.ndarray): matrix representing the connectivity
                of the rooms in the school.
            k_out: heat transfer coefficient with the outside world.
            k_int: heat transfer coefficient between rooms in the school.
        """
        self.A = adjacency_matrix
        self.D = len(self.A)
        self.k_out = k_out
        self.k_int = k_int
        self.heaters = None

    def set_heaters(self, heaters: List[Heater]):
        """
        Set the heaters the school needs
        Args:
            heaters: list of heater objects, one in each room
        """
        assert len(heaters) == self.D
        self.heaters = heaters

    def inner_heat_transfer(self, T: np.ndarray) -> np.ndarray:
        """
        Compute the heat transferred from the rooms of the school to each other
        This is a simplified version of Fourier's law
        Args:
            T: array containing the temperatures of each room
        """
        assert len(T) == self.D
        Tdiff = np.array([[Ti - Tj for Tj in T] for Ti in T])
        return self.k_int * np.einsum("ij,ij->ij", self.A, Tdiff)

    def outer_heat_transfer(self, T: np.ndarray, T_out: float) -> np.ndarray:
        """
        Compute the heat transferred by every room to the outside
        Args:
            T: array containing the temperatures of each room
            T_out (float): Outdoors temperature
        """
        assert len(T) == self.D
        return np.multiply(self.k_out, (T - T_out))

    def heat_sources(self, T: np.ndarray, targets: np.ndarray, t: float) -> np.ndarray:
        return np.array(
            [
                heater.thermostat(temp, target, t)
                for heater, temp, target in zip(self.heaters, T, targets)
            ]
        )
