import pandas as pd
from numpy.typing import NDArray
from pandas.io.formats.style import Styler


def to_frame(
    recommendations: NDArray, room_names: list[str], nan_threshold: float = 1e4
) -> pd.DataFrame:
    """Convert recommendations to DataFrame format.
    Replace high values above nan_threshold with NaN,
    since these are already booket / not valid
    recommendations.

    Args:
        recommendations: array of cost scores for each
            room time, where the lower the better, of
            shape (n_time_slots * n_rooms,)
        room_names: list of room names
        nan_threshold: threshold for replacing values with NaN
    """
    opt = recommendations.reshape(-1, len(room_names))
    time_index = timeslot_to_hours(opt.shape[0])

    return pd.DataFrame(
        opt,
        columns=room_names,
        index=time_index,
    ).where(lambda x: x < nan_threshold)


def show_recommendations(df: pd.DataFrame) -> Styler:
    """Convert DataFrame of booking recommendations
    to a styled DataFrame with a color gradient.
    Formats the DataFrame to 1 decimal place and
    replaces NaN values with a blank space, meaning
    that the room is either booked or not bookable
    with the given booking specifications.

    Returns:
        pandas.io.formats.style.Styler: styled DataFrame
    """
    return df.style.background_gradient(
        cmap="viridis", high=1, low=0, axis=None
    ).format(precision=1, na_rep=" ")


def list_recommendations(df: pd.DataFrame) -> pd.DataFrame:
    """Converts broad dataframe of shape (time_slots, rooms)
    to long format, where each row is a room-time combination.
    Renames columns to "Time Slot", "Room", "Score", and sorts
    by score and time slot. Lastly, removes rows with NaN values,
    i.e. already booked/not bookable rooms.
    """
    return (
        df.reset_index()
        .melt(id_vars="index")
        .rename(columns={"index": "Time Slot", "variable": "Room", "value": "Score"})
        .sort_values(by=["Score", "Time Slot"])[lambda d: d["Score"].notna()]
    )


def timeslot_to_hours(timeslots: int) -> list[str]:
    """Convert timeslots to hour strings. We differentiate
    between workday and weekend days. If timeslots > 8,
    we assume that the day is a weekend day, and we start
    the range start af 8. Else, we assume that the day is
    a workday, and the range starts at 15.
    """
    _start = 8 if timeslots > 8 else 15
    return [f"{_start + i}:00" for i in range(timeslots)]
