from typing import Literal

from thermo.costs.base import CostModel
from thermo.ranker.base import Ranker  # noqa
from thermo.ranker.full import FullRanker

RankerName = Literal["FullRanker"]


def make_ranker(ranker_name: RankerName, costs: list[CostModel], **kwargs):
    match ranker_name:
        case "FullRanker":
            ranker = FullRanker
        case _:
            raise NotImplementedError(f"Ranker {ranker_name} not implemented")

    return ranker(costs=costs, **kwargs)
