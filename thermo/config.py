from pathlib import Path

WORKDIR = Path(__file__).parents[1]
BUILDINGS_DIR = WORKDIR / "buildings"

# Default cost for unavailable room-time slots
UNAVAILABLE_COST = 1e5

# default start of daily schedule
WEEKDAY_HOUR_START = 15
WEEKEND_HOUR_START = 8

# names of all buildings
BUILDING_NAMES = [b.name for b in BUILDINGS_DIR.iterdir() if b.is_dir()]

# names of all amenities
AMENITIES = ("screen", "projector", "whiteboard", "speaker", "instruments")
