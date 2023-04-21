from typing import Literal

from thermo.costs.base import CostModel
from thermo.costs.capacity import CapacityCost
from thermo.costs.heating import HeatingCost

CostName = Literal["HeatingCost", "CapacityCost"]


def make_cost(name: CostName, **kwargs) -> CostModel:
    match name:
        case "HeatingCost":
            return HeatingCost(**kwargs)
        case "CapacityCost":
            return CapacityCost(**kwargs)
        case _:
            raise NotImplementedError(f"CostModel {name} not implemented.")
