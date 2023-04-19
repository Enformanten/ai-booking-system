from typing import Literal

from thermo.costs.base import CostModel  # noqa
from thermo.costs.heating import HeatingCost

CostName = Literal["HeatingCost"]


def make_cost(name: CostName, **kwargs):
    match name:
        case "HeatingCost":
            return HeatingCost(**kwargs)
        case _:
            raise NotImplementedError(f"CostModel {name} not implemented.")
