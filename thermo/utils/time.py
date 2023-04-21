from datetime import date, timedelta

from workalendar.europe import Denmark


def is_schoolday(day: date) -> bool:
    """
    Checks if a date is a school date or not based on some
    naive assumptions.

    These include: bank holidays, the days
    between Christmas and new years, the day after ascension
    day, and weeks 7 (winter vacation), 27,28 29 (summer vacation)
    and 42 (autumn vacation).

    Args:
        day: the day we want to know if it is a school day.

    Returns:
        True if it is a school day, False otherwise
    """
    week = day.isocalendar().week

    if week in [7, 27, 28, 29, 42]:
        # These are school holidays known to DTU
        return False

    if day.month == 12 and day.day > 24:
        # Days between Christmas and New Years
        return False

    calendar = Denmark()

    if day == (calendar.get_ascension_thursday(day.year) + timedelta(1)):
        # Friday after ascension day
        return False

    return calendar.is_working_day(day)


def get_time_slots(day: date) -> int:
    """
    Compute number of time slots for a given day.
    These are hourly time slots from 15 to 23 for school
    days and from 8 to 23 for school holidays.

    School holidays include: bank holidays, the days
    between Christmas and new years, the day after ascension
    day, and weeks 7 (winter vacation), 27,28 29 (summer vacation)
    and 42 (autumn vacation).

    Args:
        day: the day for which we compute the time slots.

    Returns:
        the number of time slots
    """
    if is_schoolday(day):
        return 8  # 23-15
    return 15  # 23-8
