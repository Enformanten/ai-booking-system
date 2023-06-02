from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from thermo.config import WORKDIR
from thermo.utils.logger import ml_logger as logger


def from_csv(file_path: str | Path, municipality: str, year: int) -> pd.DataFrame:
    logger.info(f"Loading data from file {file_path.name}")
    # Read DataFrame and keep only info for correct municipality
    dataf = pd.read_csv(file_path, engine="pyarrow").loc[
        lambda x: x["MUNICIPALITY"].eq(municipality)
    ]

    DATECOL = "DATE" if "DATE" in dataf.columns else "DATO"
    LOCATIONCOLS = [
        column
        for column in dataf.columns
        if column.startswith("MUNICIPALITY") or column.startswith("SCHOOL")
    ]
    # Create a timestamp from date and time, keep only the target year
    dataf = (
        dataf.assign(
            TIMESTAMP=lambda x: pd.to_datetime(
                np.vectorize(datetime.combine)(x[DATECOL], x["TIME"])
            )
        )
        .drop(columns=[DATECOL, "TIME"] + LOCATIONCOLS)
        .loc[lambda x: x["TIMESTAMP"].dt.year.eq(year)]
    )

    return dataf


@dataclass
class RawDataFile:
    name: str
    file_path: str
    parse_params: dict[str, Any] = field(default_factory=dict)


def select_data(
    dataf: pd.DataFrame, name: str, **parse_params: dict[str, Any]
) -> pd.DataFrame:
    logger.debug(f"Select and transform {name} data")
    match name:
        case "energy":
            return select_energy_data(dataf, **parse_params)
        case "bookings":
            return select_bookings_data(dataf, **parse_params)
        case _:
            raise NotImplementedError(f"Handler for file name {name} not implemented")


def select_energy_data(
    dataf: pd.DataFrame, **parse_params: dict[str, Any]
) -> pd.DataFrame:
    measure_points = parse_params.get("measure_points", dataf["MEASURE_POINT"].unique())
    measure_types = parse_params.get("measure_types", dataf["MEASURE_TYPE"].unique())
    if len(measure_points) != 1 or len(measure_types) != 1:
        raise NotImplementedError("Handling for more than one measure point or type.")
    return (
        dataf.loc[lambda x: x["MEASURE_POINT"].isin(measure_points)]
        .loc[lambda x: x["MEASURE_TYPE"].isin(measure_types)]
        .set_index("TIMESTAMP")
        .rename(columns={"VALUE": "electricity"})[["electricity"]]
    )


def select_bookings_data(
    dataf: pd.DataFrame, **parse_params: dict[str, Any]
) -> pd.DataFrame:
    if parse_params.get("drop_empty_rooms", False):
        non_empty_rooms = (
            dataf.groupby("ROOM_ID")["BOOKED"]
            .sum()
            .loc[lambda x: x.gt(0)]
            .index.to_list()
        )
        dataf = dataf.loc[lambda x: x["ROOM_ID"].isin(non_empty_rooms)]

    match parse_params.get("aggregation_method", "binary"):
        case "binary":
            dataf = dataf.pipe(binary_aggregate_bookings)
        case "fractional":
            dataf = dataf.pipe(fractional_aggregate_bookings)
        case other:
            raise NotImplementedError(f"Aggregation method {other}.")

    return dataf.pivot(index="TIMESTAMP", columns="ROOM_ID", values="BOOKED").rename(
        columns=lambda name: name + "_booked"
    )


def binary_aggregate_bookings(dataf: pd.DataFrame) -> pd.DataFrame:
    return (
        dataf.groupby(["TIMESTAMP", "ROOM_ID"])["BOOKED"]
        .sum()
        .clip(upper=1)
        .reset_index()
    )


def fractional_aggregate_bookings(dataf: pd.DataFrame) -> pd.DataFrame:
    return (
        dataf.assign(
            BOOKED=np.where(
                dataf["TIME_LEFT_OF_BOOKING"].gt(1),
                dataf["BOOKED"],
                dataf["TIME_LEFT_OF_BOOKING"],
            )
        )
        .groupby(["TIMESTAMP", "ROOM_ID"])["BOOKED"]
        .sum()
        .clip(upper=1)
        .reset_index()
    )


def get_data(
    building_name: str, municipality: str, year: int, files: list[dict[str, Any]]
) -> None:
    logger.info(f"Getting data for building {building_name}")
    logger.debug(f"Data for municipality {municipality} on year {year}.")

    dataf = pd.DataFrame(
        index=pd.date_range(f"{year}-01-01", f"{year}-12-31", freq="H")
    )
    for fileinfo in map(lambda x: RawDataFile(**x), files):
        dataf = dataf.join(
            how="inner",
            other=(
                from_csv(
                    file_path=WORKDIR / fileinfo.file_path,
                    municipality=municipality,
                    year=year,
                ).pipe(select_data, fileinfo.name, **fileinfo.parse_params)
            ),
        )

    return dataf


if __name__ == "__main__":
    import dvc.api

    params = dvc.api.params_show()

    # Get school name
    building = params["building"]
    municipality = params["municipality"]
    year = params["year"]
    files = params["get_data"]["files"]

    # Get data
    dataf = get_data(
        building_name=building, municipality=municipality, year=year, files=files
    )

    logger.debug("Saving raw data to data/raw_data.pkl")
    DATADIR = Path("data")
    DATADIR.mkdir(parents=True, exist_ok=True)
    dataf.to_pickle(DATADIR / "raw_data.pkl")
