from datetime import date

import pandas as pd
from numpy.typing import NDArray

from thermo.adapter.state_connection import get_state
from thermo.costs import make_cost
from thermo.ranker import Ranker, make_ranker
from thermo.utils import io
from thermo.utils.building import Building
from thermo.utils.postprocessing import (
    list_recommendations,
    show_recommendations,
    to_frame,
)
from thermo.utils.time import get_time_slots


class Recommendation:
    """
    Class to contain the postprocessing of recommendations.
    Args:
        ranking: the output of a Ranker.run call.
        room_names: names of the rooms for display
    """

    def __init__(self, ranking: NDArray, room_names: list[str]):
        self.ranking = to_frame(ranking, room_names=room_names)

    def show(self) -> pd.DataFrame:
        """
        Returns a styled DataFrame with a color gradient.
        Formats the DataFrame to 1 decimal place and
        replaces NaN values with "BOOKED".

        Returns:
            pandas.io.formats.style.Styler: styled DataFrame
        """
        return show_recommendations(self.ranking)

    def __repr__(self) -> str:
        return self.ranking.fillna("BOOKED").__repr__()

    @property
    def shape(self) -> tuple[int]:
        return self.ranking.shape

    def top_recommendations(self) -> pd.DataFrame:
        """
        Returns a sorted list of recommendations, with columns
        "Time Slot", "Room", "Score"
        """
        return list_recommendations(self.ranking)


class Recommender:
    """
    Interface for GUI or API to interact with the rest of thermo.
    """

    def __init__(
        self,
        building: Building,
        ranker: Ranker,
    ):
        """
        Init method, intended for testing purposes and not for human
        use. We recommend instantiating recommenders from config files
        by calling Recommender.from_config(school_name).

        Args:
            building: Building object containing the adjacency matrix,
                room descriptions and costs etc.
            ranker: Object to orchestrate the different costs and how they are
                combined. Examples of costs are `thermo.costs.HeatingCost` or
                `thermo.costs.CapacityCost`.
        """

        self.building = building
        self._room_names = building.get_room_attr("name")
        self.ranker = ranker

    @classmethod
    def from_config(cls, building_name: str) -> "Recommender":
        """
        Creates a Recommender from the config files of a building.

        Args:
            building_name: Name of the building, as in the path to its config
                files.

        Returns:
            A recommender based on the configuration for that building found in
            `buildings/building_name`.
        """
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
            building=building,
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
