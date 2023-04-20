import numpy as np
import pandas as pd
from numpy.typing import NDArray


def to_frame(recommendations: NDArray, room_names: list[str]) -> pd.DataFrame:
    """
    Take recommendations as a numpy array and display them as a DataFrame.
    """
    opt = recommendations.reshape(-1, len(room_names))
    return (
        pd.DataFrame(
            opt,
            columns=room_names,
            index=(f"t_{i}" for i in range(opt.shape[0])),
        )
        .replace(100001, np.nan)
        .replace(100000.5, np.nan)
    )


def show_recommendations(df: pd.DataFrame) -> pd.DataFrame:
    """Color code recommendations in table."""
    return df.style.background_gradient(
        cmap="viridis", high=1, low=0, axis=None
    ).format(precision=1, na_rep="BOOKED")


def list_recommendations(df: pd.DataFrame) -> pd.DataFrame:
    """List recommendations in table."""
    return (
        df.reset_index()
        .melt(id_vars="index")
        .rename(columns={"index": "Time Slot", "variable": "Room", "value": "Score"})
        .sort_values(by=["Score", "Time Slot"])[lambda d: d["Score"].notna()]
    )
