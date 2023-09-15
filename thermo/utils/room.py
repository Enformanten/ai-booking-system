from dataclasses import dataclass, field


@dataclass
class Room:
    name: str
    index: int | None = None
    capacity: int | None = None
    amenities: set[str] = field(default_factory=set)

    def __post_init__(self) -> None:
        """Perform post-initialization tasks
        1. YAML does not support sets, so we convert
        the amenities from dict keys to sets.
        """
        if not isinstance(self.amenities, set):
            self.amenities = set(self.amenities)
