from abc import ABC, abstractmethod

from numpy.typing import NDArray


class CostModel(ABC):
    """
    Base class to simulate all the costs of using a room.
    For example:
        - HeatingCost for the heating
        - CapacityCost for the capacity of the room
        - etc.
    """

    @abstractmethod
    def run(self, state: NDArray, **kwargs) -> NDArray:
        """
        Base method, that computes the cost given the current
        state of bookings and some internal parameters.

        Args:
            state: a flat array containing 1 if the room is booked
                at that time a zero otherwise.
            kwargs: other possible arguments to the run method.

        Returns:
            An array of the same shape as the state, containing the costs.
        """
        pass
