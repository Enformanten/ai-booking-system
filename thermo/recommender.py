from datetime import date

import pandas as pd
from numpy.typing import NDArray

from thermo.adapter.state_connection import get_state
from thermo.costs import make_cost
from thermo.ranker import Ranker, make_ranker
from thermo.utils import io
from thermo.utils.postprocessing import (
    list_recommendations,
    show_recommendations,
    to_frame,
)
from thermo.utils.room import Room
from thermo.utils.time import get_time_slots


class Recommendation:
    def __init__(self, ranking: NDArray, room_names: list[str]):
        self.ranking = to_frame(ranking, room_names=room_names)

    def show(self):
        return show_recommendations(self.ranking)

    def __repr__(self) -> str:
        return self.ranking.fillna("BOOKED").__repr__()

    def top_recommendations(self) -> pd.DataFrame:
        return list_recommendations(self.ranking)


class Recommender:
    """
    Interface for GUI or API to interact with the rest of thermo.
    """

    def __init__(
        self,
        building_name: str,
        room_description: list[Room],
        ranker: Ranker,
    ):
        self.building_name = building_name
        self.room_description = room_description
        self._room_names = [room.name for room in room_description]
        self.ranker = ranker

    @classmethod
    def from_config(cls, building_name: str) -> "Recommender":
        building_path = io.get_building_path(building_name)
        building = io.get_building_specs(building_path)

        costs = [
            make_cost(
                name=key,
                adjacency=building.adjacency,
                room_description=building.room_descriptions,
                **values,
            )
            for key, values in building.costs.items()
        ]
        ranker = make_ranker(ranker_name=building.ranker, costs=costs)

        return cls(
            building_name=building_name,
            room_description=building.room_descriptions,
            ranker=ranker,
        )

    def run(self, day: date, **kwargs) -> Recommendation:
        state = get_state(day)
        n_time_slots = get_time_slots(day)
        recommendation = self.ranker.run(state, n_time_slots=n_time_slots, **kwargs)
        return Recommendation(recommendation, room_names=self._room_names)
