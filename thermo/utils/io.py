import json
from io import TextIOWrapper
from pathlib import Path
from typing import Any

import yaml

from thermo.config import BUILDINGS_DIR
from thermo.utils.building import Building


def get_building_path(building_name: str) -> Path:
    """
    Validates and returns the path to the building
    config dir. Raises an error if the dir does
    not exist.

    Args:
        building_name: name of the building.

    Returns:
        pathlib.Path: path to the building config dir.
    """
    building_path = BUILDINGS_DIR / building_name
    if not building_path.exists():
        raise FileExistsError(f"Building '{building_name}' does not exist.")
    return building_path


def load_yaml(config: TextIOWrapper, **kwargs) -> dict[str, Any]:
    """Loads a yaml file from the given path."""
    return yaml.safe_load(config, **kwargs)


def load_json(config: TextIOWrapper, **kwargs) -> dict[str, Any]:
    """Loads a json file from the given path."""
    return json.load(config, **kwargs)


def load_file(building_path: str, file_name: str, **kwargs) -> dict[str, Any]:
    """Loads a file from the given path. Pathlib
    handles context management for us."""
    p = Path(building_path / file_name)
    config = p.open("r")

    match p.suffix:
        case ".yaml":
            return load_yaml(config, **kwargs)
        case ".json":
            return load_json(config, **kwargs)
        case _:
            raise ValueError(f"File type {p.suffix} not supported.")


def load_building(building_path: str) -> Building:
    """Loads relevant files from building config dir.
    and loads them into a Building object."""

    _adjacency = load_file(building_path, "adjacency.json")
    _specs = load_file(building_path, "specifications.yaml")
    _config = load_file(building_path, "config.yaml")

    data = _adjacency | _specs | _config
    return Building(**data)


def load_all_buildings() -> list[Building]:
    """
    Returns a list of all buildings found in the
    BUILDINGS_DIR as Building objects.
    Returns:
        list[Building]: list of all buildings.
    """
    return [
        load_building(building_dir)
        for building_dir in BUILDINGS_DIR.glob("*")
        if building_dir.is_dir()
    ]


# def load_adjacency(path: Path) -> NDArray:
#     """
#     Loads adjacency matrix from file.
#     Args:
#         path: path to the subscription
#             where the adjacency matrix is.

#     Returns:
#         a (N_rooms, N_rooms) matrix where 0 represents
#         two rooms not sharing a wall and 1 represents
#         said rooms sharing a wall.
#     """
#     # TODO: This is a placeholder, the correct implementation
#     # TODO: must be added here. :)

#     return np.array(
#         [
#             [0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
#             [1, 0, 0, 1, 0, 1, 1, 0, 0, 0],
#             [0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
#             [0, 1, 1, 0, 0, 0, 1, 0, 0, 0],
#             [0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
#             [0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
#             [0, 1, 0, 1, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
#             [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
#             [1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
#         ]
#     )


# def load_config(path: Path) -> dict[str, Any]:
#     """
#     Loads school-specific configuration from a file.
#     Args:
#         path: path to the subscription
#             where the adjacency matrix is.

#     Returns:
#         The configuration defined by the user.
#     """
#     # TODO: This is a placeholder, the correct implementation
#     # TODO: must be added here. :)
#     return {
#         "ranker": "FullRanker",
#         "costs": {"HeatingCost": {"t_weight": 1.0, "message_importance": 0.5}},
#     }


# def load_room_descriptions(path: Path) -> list[Room]:
#     """
#     Loads a description of each room from a file.
#     Args:
#         path: path to the subscription where the adjacency matrix is.
#     Returns:
#         a list of rooms with the same indexing as the adjacency.
#     """
#     # TODO: This is a placeholder, the correct implementation
#     # TODO: must be added here. :)
#     room_descriptions = [
#         {"name": "Room A", "capacity": 30},
#         {"name": "Room B", "capacity": 20},
#         {"name": "Room C", "capacity": 10},
#         {"name": "Room D", "capacity": 30},
#         {"name": "Room E", "capacity": 15},
#         {"name": "Room F", "capacity": 30},
#         {"name": "Room G", "capacity": 15},
#         {"name": "Room H", "capacity": 30},
#         {"name": "Room I", "capacity": 10},
#         {"name": "Room J", "capacity": 30},
#     ]
#     return [Room(index=index, **specs)
#           for index, specs in enumerate(room_descriptions)
#       ]
