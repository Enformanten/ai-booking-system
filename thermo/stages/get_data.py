from argparse import ArgumentParser
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from thermo.config import WORKDIR
from thermo.utils.io import get_building_path, load_file
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


def get_data(building_name: str) -> None:
    params = load_file(
        building_path=get_building_path(building_name), file_name="regression.yaml"
    ).get("get_data", {})

    municipality = params.get("municipality")
    year = params.get("year")
    logger.info(f"Getting data for building {building_name}")
    logger.debug(f"Data for municipality {municipality} on year {year}.")

    if "files" in params:
        dataf = pd.DataFrame(
            index=pd.date_range(f"{year}-01-01", f"{year}-12-31", freq="H")
        )
        for fileinfo in map(lambda x: RawDataFile(**x), params["files"]):
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
    else:
        raise ValueError(f"Origin of data not found in {building_name}/regression.yaml")

    return dataf


if __name__ == "__main__":
    # Get school name
    parser = ArgumentParser(description="Get the raw data for user-defined building.")
    parser.add_argument("-b", "--building", help="name of the building")
    args = parser.parse_args()

    # Get data
    dataf = get_data(args.building)

    logger.debug("Saving raw data to data/raw_data.pkl")
    dataf.to_pickle(WORKDIR / "data" / "raw_data.pkl")
