from typing import Literal

from thermo.costs.amenity import AmenityCost
from thermo.costs.base import CostModel
from thermo.costs.capacity import CapacityCost
from thermo.costs.heating import HeatingCost

CostName = Literal["HeatingCost", "CapacityCost", "AmenityCost"]
"""Names of all CostModel classes in `thermo`:
`HeatingCost`, `CapacityCost`"""


def make_cost(name: CostName, **kwargs) -> CostModel:
    """
    Creates a CostModel object given its name, and parameters.

    Args:
        name: Name of the CostModel class
        kwargs: other possible arguments to the init method of the
            CostModel.

    Returns:
        an instance of the `name` class.
    """
    match name:
        case "HeatingCost":
            return HeatingCost(**kwargs)
        case "CapacityCost":
            return CapacityCost(**kwargs)
        case "AmenityCost":
            return AmenityCost(**kwargs)
        case _:
            raise NotImplementedError(f"CostModel {name} not implemented.")
