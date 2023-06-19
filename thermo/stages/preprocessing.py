import time
from functools import wraps
from typing import Any, Callable

import numpy as np
import pandas as pd

from thermo.config import WEEKDAY_HOUR_START, WEEKEND_HOUR_START
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
        time_taken = time.perf_counter() - tic

        logger.info(
            f"{func.__name__} completed \t shape {result.shape}"
            f"\t time {time_taken:.3f}s"
        )

        if not result.shape[0]:
            logger.error(f"{func.__name__} emptied the DataFrame")
        return result

    return wrapper


@log_transformation
def drop_unfrequent_rooms(dataf: pd.DataFrame, threshold: int | None) -> pd.DataFrame:
    """
    Drops the columns for rooms with low booking frequency from the DataFrame.

    Args:
        dataf: The input DataFrame.
        threshold: Rooms with less bookings than this threshold will be dropped.
            If None, no rooms are dropped.

    Returns:
        The DataFrame with the columns with infrequent rooms dropped.
    """
    if not threshold:
        return dataf

    room_columns = [col for col in dataf.columns if col.endswith("booked")]
    to_drop = (
        dataf[room_columns].sum(axis=0).loc[lambda x: x.lt(threshold)].index.to_list()
    )
    return dataf.drop(columns=to_drop)


@log_transformation
def drop_unused_days(dataf: pd.DataFrame) -> pd.DataFrame:
    """
    Drops the rows corresponding to days where no room was used from the DataFrame.

    Args:
        dataf: The input DataFrame.

    Returns:
        The DataFrame with the days where no room was used dropped.
    """
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
    """Drops nights and school hours from the DataFrame.

    Args:
        dataf: The input DataFrame.
        drop: Indicates whether to drop nights and school days.
            If False, no data is dropped. Defaults to True.

    Returns:
        The processed DataFrame.
    """
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
    """Mocks ventilation data based on booking information.

    Args:
        dataf: The input DataFrame.
        params: Parameters for ventilation mocking.
            If None, no mocking is performed.

    Returns:
        The DataFrame with mocked ventilation data.
    """
    if not params:
        return dataf

    room_columns = [col for col in dataf.columns if col.endswith("booked")]
    bookings = dataf[room_columns].copy()

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
            ).rename(
                columns={col: col.split("_booked")[0] + "_day" for col in room_columns}
            ),
        )

    return dataf


def preprocess(dataf: pd.DataFrame, params: dict[str, Any]) -> pd.DataFrame:
    """
    Preprocesses the data based on the given parameters.

    Args:
        dataf: The input DataFrame.
        params: Parameters for data preprocessing.

    Returns:
        pd.DataFrame: The preprocessed DataFrame.
    """
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
    from pathlib import Path

    import dvc.api

    logger.info("Running preprocessing script")
    params = dvc.api.params_show()["preprocessing"]

    # Load data
    logger.info("Loading raw data...")
    DATADIR = Path("data")
    dataf = pd.read_pickle(DATADIR / "raw_data.pkl")

    # Preprocess the data
    dataf = dataf.pipe(preprocess, params=params)

    # Save to disk
    logger.info("Saving preprocessed data...")
    dataf.to_pickle(DATADIR / "preprocessed_data.pkl")
