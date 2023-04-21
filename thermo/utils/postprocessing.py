import pandas as pd
from numpy.typing import NDArray


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
    return pd.DataFrame(
        opt,
        columns=room_names,
        index=(f"t_{i}" for i in range(opt.shape[0])),
    ).where(lambda x: x < nan_threshold)


def show_recommendations(df: pd.DataFrame) -> pd.io.formats.style.Styler:
    """Convert DataFrame of booking recommendations
    to a styled DataFrame with a color gradient.
    Formats the DataFrame to 1 decimal place and
    replaces NaN values with "BOOKED".

    Returns:
        pandas.io.formats.style.Styler: styled DataFrame
    """
    return df.style.background_gradient(
        cmap="viridis", high=1, low=0, axis=None
    ).format(precision=1, na_rep="BOOKED")


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
