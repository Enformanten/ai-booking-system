from abc import ABC, abstractmethod


class Heater(ABC):
    def __init__(self, max_heat: float):
        """
        Parent class for all heaters.
        Args:
            max_heat (float): maximum heat a heater can output
        """
        self.max_heat = max_heat

    def _realistic_output(self, heat: float) -> float:
        """
        Produce a realistic output
        """
        if heat < 0.0:
            return 0.0
        elif heat >= self.max_heat:
            return self.max_heat
        return heat

    @abstractmethod
    def _thermostat(self, T: float, target: float, t: float) -> float:
        pass

    def thermostat(self, T: float, target: float, t: float) -> float:
        """
        Output the amout of heat the thermostat requires the heater to output.
        Args:
            T (float): current temperature
            target (float): target temperature
            t (float): time
        Returns:
            heat (float): the amount of energy it is returned as an output
        """
        heat = self._thermostat(T=T, target=target, t=t)
        heat = self._realistic_output(heat)
        return heat
