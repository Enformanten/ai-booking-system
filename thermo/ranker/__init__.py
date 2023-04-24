from typing import Literal

from thermo.costs.base import CostModel
from thermo.ranker.base import Ranker
from thermo.ranker.full import FullRanker

RankerName = Literal["FullRanker"]
"""Names of all Ranker classes in `thermo`: `FullRanker`"""


def make_ranker(ranker_name: RankerName, costs: list[CostModel], **kwargs) -> Ranker:
    """
    Creates a Ranker object given its name, and the costs that it ranks.

    Args:
        ranker_name: Name of the ranker
        costs: Cost instances to compute the cost of each room.
        kwargs: other possible arguments to the init method of the
            ranker.

    Returns:
        an instance of the `ranker_name` class.
    """
    match ranker_name:
        case "FullRanker":
            ranker = FullRanker
        case _:
            raise NotImplementedError(f"Ranker {ranker_name} not implemented")

    return ranker(costs=costs, **kwargs)
