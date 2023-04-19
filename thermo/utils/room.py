from dataclasses import dataclass


@dataclass
class Room:
    name: str
    index: int = None
    capacity: int = None
    # tags: list[str]
