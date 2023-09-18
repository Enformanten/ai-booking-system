import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import pytest
from sklearn.base import check_is_fitted
from sklearn.pipeline import Pipeline


@pytest.mark.ml_integration
def test_isfitted(MODELDIR: Path) -> None:
    """
    Check the `model.joblib` file contains a model that is fitted
    and can be used for prediction
    """
    # given
    model = joblib.load(MODELDIR / "model.joblib")

    # then
    if isinstance(model, Pipeline):
        check_is_fitted(model.steps[-1][-1], "coef_")
    else:
        check_is_fitted(model, "coef_")


@pytest.mark.ml_integration
def test_good_metrics(MODELDIR: Path) -> None:
    """
    Check the metrics of the workflow on demo data
    are sufficiently high
    """
    # given
    with open(MODELDIR / "test.json", "rb") as f:
        metrics = json.load(f)

    # then
    assert metrics.get("r2") >= 0.999
    assert np.isclose(metrics.get("rmse"), 0.17, atol=0.02)


@pytest.mark.ml_integration
def test_good_coeff(MODELDIR: Path) -> None:
    """
    Check that, the model of the workflow on demo_data
    predicts that using a room is more expensive than
    simply keeping it warm.
    """
    # given
    dataf = pd.read_csv(
        MODELDIR / "costs.csv", skipfooter=1, index_col="room", engine="python"
    )
    # then
    assert np.all(dataf["booked"] > dataf["day"])
