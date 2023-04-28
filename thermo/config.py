from pathlib import Path

WORKDIR = Path(__file__).parents[1]
BUILDINGS_DIR = WORKDIR / "buildings"

# Default cost for unavailable room-time slots
UNAVAILABLE_COST = 1e5

# default start of daily schedule
WEEKDAY_HOUR_START = 15
WEEKEND_HOUR_START = 8
