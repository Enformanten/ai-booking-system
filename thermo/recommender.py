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
        school_name: str,
        room_description: list[Room],
        ranker: Ranker,
    ):
        """
        Init method, intended for testing purposes and not for human
        use. We recommend instantiating recommenders from config files
        by calling Recommender.from_config(school_name).

        Args:
            school_name: Name of the school, as in the path to its config
                files.
            room_description: List of rooms containing their characteristics
                such as name, capacity or index.
            ranker: Object to orchestrate the different costs and how they are
                combined. Examples of costs are `thermo.costs.HeatingCost` or
                `thermo.costs.CapacityCost`.
        """

        self.school_name = school_name
        self.room_description = room_description
        self._room_names = [room.name for room in room_description]
        self.ranker = ranker

    @classmethod
    def from_config(cls, school_name: str) -> "Recommender":
        """
        Creates a Recommender from the config files of a school.

        Args:
            school_name: Name of the school, as in the path to its config
                files.

        Returns:
            A recommender based on the configuration for that school found in
            `schools/school_name`.
        """
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
                **values,
            )
            for key, values in config.get("costs", {}).items()
        ]
        ranker = make_ranker(ranker_name=config["ranker"], costs=costs)

        return cls(
            school_name=school_name,
            room_description=room_description,
            ranker=ranker,
        )

    def run(self, day: date, **kwargs) -> Recommendation:
        """
        Produces a recommendation of which rooms to book given a date.
        The method calls internally the schools API to determine which
        books have been already booked.

        It then calls all the costs and combines them according to the
        ranker, to return an instance of Recommendation, with all
        the costs for the rooms.

        Args:
            day: date for which the user desires make a booking.
            kwargs: other possible run-time parameters for the costs.

        Returns:
            The costs of the recommended possible bookings.
        """
        state = get_state(day)
        n_time_slots = get_time_slots(day)
        recommendation = self.ranker.run(state, n_time_slots=n_time_slots, **kwargs)
        return Recommendation(recommendation, room_names=self._room_names)
