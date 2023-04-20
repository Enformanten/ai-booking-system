from datetime import date

import pandas as pd
from numpy.typing import NDArray

from thermo.adapter.state_connection import get_state
from thermo.config import WORKDIR
from thermo.costs import make_cost
from thermo.ranker import Ranker, make_ranker
from thermo.utils import io
from thermo.utils.postprocessing import (
    list_recommendations,
    show_recommendations,
    to_frame,
)
from thermo.utils.room import Room


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
        school_name: str,
        n_time_slots: int,  # TODO: check its not dead
        room_description: list[Room],
        ranker: Ranker,
    ):
        self.school_name = school_name
        self.room_description = room_description
        self._room_names = [room.name for room in room_description]
        self.ranker = ranker

    @classmethod
    def from_config(cls, school_name: str, n_time_slots) -> "Recommender":
        school_path = WORKDIR / "schools" / school_name
        if school_name != "demo_school":
            if not school_path.exists():
                raise FileExistsError(f"School {school_name} does not exist.")

        adjacency = io.load_adjacency(school_path)
        config = io.load_config(school_path)
        room_description = io.load_room_description(school_path)
        costs = [
            make_cost(
                name=key,
                adjacency=adjacency,
                room_description=room_description,
                n_time_slots=n_time_slots,
                **values,
            )
            for key, values in config.get("costs", {}).items()
        ]
        ranker = make_ranker(ranker_name=config["ranker"], costs=costs)

        return cls(
            school_name=school_name,
            n_time_slots=n_time_slots,
            room_description=room_description,
            ranker=ranker,
        )

    def run(self, day: date, **kwargs) -> Recommendation:
        state = get_state(day=day.isoformat())
        recommendation = self.ranker.run(state, **kwargs)
        return Recommendation(recommendation, room_names=self._room_names)
