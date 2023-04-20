from datetime import date, timedelta

from workalendar.europe import Denmark


def is_schoolday(day: date) -> bool:
    week = day.isocalendar.week

    if week in [7, 27, 28, 29, 42]:
        # These are school holidays known to DTU
        return False

    if day.month == 12 and day.day > 24:
        # Days between Christmas and New Years
        return False

    calendar = Denmark(day.year)

    if day == (calendar.get_ascension_thursday(day.year) + timedelta(1)):
        # Friday after ascension day
        return False

    return calendar.is_working_day(day)


def time_slots(day: date) -> int:
    if is_schoolday(day):
        return 8  # 23-15
    return 15  # 23-8
