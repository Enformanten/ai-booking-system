import time
from argparse import ArgumentParser
from functools import wraps
from typing import Any, Callable

import numpy as np
import pandas as pd

from thermo.config import WEEKDAY_HOUR_START, WEEKEND_HOUR_START, WORKDIR
from thermo.utils.io import get_building_path, load_file
from thermo.utils.logger import ml_logger as logger
from thermo.utils.time import is_schoolday


def log_transformation(
    func: Callable[[pd.DataFrame, Any], pd.DataFrame]
) -> Callable[[pd.DataFrame, Any], pd.DataFrame]:
    """
    Time logger for preprocessing transformations
    """

    @wraps(func)
    def wrapper(dataf: pd.DataFrame, **kwargs) -> pd.DataFrame:
        params = ", ".join(f"{key}={value}" for key, value in kwargs.items())
        logger.debug(f"{func.__name__} running \t parameters: {params}.")
        tic = time.perf_counter()
        result = func(dataf, **kwargs)
        time_taken = round(time.perf_counter() - tic, 3)

        logger.info(
            f"{func.__name__} completed \t shape {result.shape} \t time {time_taken}s"
        )

        if not result.shape[0]:
            logger.error(f"{func.__name__} emptied the DataFrame")
        return result

    return wrapper


@log_transformation
def drop_unfrequent_rooms(dataf: pd.DataFrame, threshold: int | None) -> pd.DataFrame:
    if not threshold:
        return dataf

    room_columns = [col for col in dataf.columns if col.endswith("booked")]
    to_drop = (
        dataf[room_columns].sum(axis=0).loc[lambda x: x.lt(threshold)].index.to_list()
    )
    return dataf.drop(columns=to_drop)


@log_transformation
def drop_unused_days(dataf: pd.DataFrame) -> pd.DataFrame:
    room_columns = [col for col in dataf.columns if col.endswith("booked")]
    is_used = np.vectorize(
        dataf[room_columns]
        .groupby([dataf.index.date])
        .sum()
        .sum(axis=1)
        .astype(bool)
        .to_dict()
        .__getitem__
    )
    return dataf.loc[lambda x: is_used(x.index.date)]


@log_transformation
def drop_nights_and_school(dataf: pd.DataFrame, drop: bool = True) -> pd.DataFrame:
    if not drop:
        return dataf
    schoolday = np.vectorize(is_schoolday)(dataf.index.date)
    hour = dataf.index.hour
    return dataf.loc[
        (schoolday & (hour >= WEEKDAY_HOUR_START))
        | (~schoolday & (hour >= WEEKEND_HOUR_START))  # noqa W503
    ]


@log_transformation
def mock_ventilation(
    dataf: pd.DataFrame, params: dict[str, Any] | None
) -> pd.DataFrame:
    if not params:
        return dataf

    room_columns = [col for col in dataf.columns if col.endswith("booked")]
    bookings = dataf.copy()[room_columns]

    # Add is_day column per room
    if params.get("is_day", True):
        dataf = dataf.join(
            how="inner",
            other=(
                (
                    bookings.groupby([bookings.index.date])
                    .apply(lambda x: x.iloc[::-1, :].cummax().iloc[::-1, :])
                    .reset_index(level=0)
                    .drop(columns="level_0")
                )
                - bookings  # noqa W503
            ).rename(columns={col: col.split("_")[0] + "_day" for col in room_columns}),
        )

    return dataf


def preprocess(dataf: pd.DataFrame, params: dict[str, Any]) -> pd.DataFrame:
    return (
        dataf.pipe(drop_unused_days)
        .pipe(drop_unfrequent_rooms, threshold=params.get("booking_hours_threshold"))
        .pipe(
            drop_nights_and_school,
            drop=params.get("drop_nights_and_school_hours", False),
        )
        .pipe(mock_ventilation, params=params.get("ventilation"))
    )


if __name__ == "__main__":
    # Get school name
    parser = ArgumentParser(description="Get the raw data for user-defined building.")
    parser.add_argument(
        "-b", "--building", help="name of the building", default="strandskolen"
    )
    args = parser.parse_args()

    logger.info("Running preprocessing script")
    # Get preprocessing params:
    params = load_file(
        building_path=get_building_path(args.building), file_name="regression.yaml"
    ).get("preprocessing", {})

    # Load data
    logger.info("Loading raw data...")
    dataf = pd.read_pickle(WORKDIR / "data" / "raw_data.pkl")

    # Preprocess the data
    dataf = dataf.pipe(preprocess, params=params)

    # Save to disk
    logger.info("Saving preprocessed data...")
    dataf.to_pickle(WORKDIR / "data" / "preprocessed_data.pkl")
