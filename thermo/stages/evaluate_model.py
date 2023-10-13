"""
This script validates the results of the rest of the
workflow and produces plots and charts so that the quality
can be further evaluated by the user.
"""
import json
from math import sqrt
from pathlib import Path
from typing import Any

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.base import RegressorMixin

from thermo.utils.logger import ml_logger as logger


def get_metrics(
    dataf: pd.DataFrame, nfolds: int, which: str = "test"
) -> dict[str, Any]:
    """
    Returns metrics of the best model from grid search results.

    Args:
        dataf: Grid search results.
        nfolds: Number of cross-validation folds in dataf.
        which: The type of metrics to retrieve ("test" or "train").
        Defaults to "test".

    Returns:
        dict: Dictionary containing the metrics.
    """

    idx = dataf["mean_test_r2"].argmax()
    best_model = dataf.iloc[idx]

    return {
        "r2": best_model[f"mean_{which}_r2"],
        "r2_err": best_model[f"std_{which}_r2"] / sqrt(nfolds),
        "rmse": -best_model[f"mean_{which}_neg_root_mean_squared_error"],
        "rmse_err": best_model[f"std_{which}_neg_root_mean_squared_error"]
        / sqrt(nfolds),  # noqa W503
    }


def plot_gridsearch(dataf: pd.DataFrame, nfolds: int, figpath: Path) -> None:
    """Plots the results of the grid search for the L2 regularization.

    Args:
        dataf: Grid search results.
        nfolds: Number of cross-validation folds in dataf.
        figpath: Filepath to save the plot.
    """
    x = dataf["param_regression__alpha"]
    y = dataf["mean_test_r2"]
    y_err = dataf["std_test_r2"] / sqrt(nfolds)
    plt.errorbar(x, y, y_err)
    plt.xscale("log")
    plt.ylabel("r2 score")
    plt.xlabel("L2 regularization")
    plt.title("Grid search on the test set")
    plt.savefig(figpath)


def extract_coefficients(dataf: pd.DataFrame, model: RegressorMixin) -> pd.DataFrame:
    """
    Extracts the cost coefficients for different room from the model.

    Args:
        dataf: The training set.
        model: Fitted regression model.

    Returns:
        DataFrame with the cost coefficients of the rooms given their status.
    """
    names = [
        col for col in dataf.columns if col.endswith("booked") or col.endswith("day")
    ]
    return pd.DataFrame(
        {
            "room": map(lambda x: x.split("_")[0], names),
            "status": map(lambda x: x.split("_")[1], names),
            "cost": model.named_steps["regression"].coef_[: len(names)],
        }
    ).pivot(columns="status", index="room", values="cost")


def plot_error_distribution(
    model: RegressorMixin, dataf: pd.DataFrame, target: str, figpath: Path
) -> None:
    """
    Creates the scatter plot showing the relationship between
    the true and predicted values.

    Args:
        model: Fitted regression model.
        dataf: training set.
        target: Name of the target column.
        figpath: Filepath to save the plot.
    """
    y_true = dataf[target]
    X = dataf.drop(columns=target)
    y_pred = model.predict(X)
    rmse = np.sqrt((y_true - y_pred).pow(2).mean())

    x = np.linspace(y_pred.min(), y_pred.max(), 100)
    fig = sns.jointplot(x=y_pred, y=y_true, alpha=0.3)
    fig.ax_joint.plot(x, x, "k-", alpha=0.5)
    fig.ax_joint.plot(x, x + rmse, "k--", alpha=0.5)
    fig.ax_joint.plot(x, x - rmse, "k--", alpha=0.5)
    fig.ax_joint.set_xlabel("prediction (kWh)")
    fig.ax_joint.set_ylabel("consumption (kWh)")
    fig.savefig(figpath)


if __name__ == "__main__":
    import dvc.api

    params = dvc.api.params_show()

    nfolds = params["train"]["cv_folds"]
    target = params["train"]["target"]

    logger.info("Evaluating ml model...")
    MODELDIR = Path("model")
    DATADIR = Path("data")

    # Metrics
    logger.info("Extracting metrics")
    scores = pd.read_csv(MODELDIR / "cross_validation.csv")

    for partition in ("train", "test"):
        logger.debug(f"Extracting {partition} metrics ...")
        with open(MODELDIR / f"{partition}.json", "w", encoding="utf-8") as f:
            json.dump(get_metrics(dataf=scores, nfolds=nfolds, which=partition), f)

    # Hyperparmeters
    logger.info("Saving regularization plot to 'model/regularization.png' ")
    plot_gridsearch(
        dataf=scores, nfolds=nfolds, figpath=MODELDIR / "regularization.png"
    )

    # Coefficients
    model = joblib.load(MODELDIR / "model.joblib")
    dataf = pd.read_pickle(DATADIR / "preprocessed_data.pkl")
    coefs = extract_coefficients(dataf=dataf, model=model)
    coefs.to_csv(MODELDIR / "costs.csv", index=True)

    nvalid = coefs.apply(lambda x: x[0] > x[1], axis=1).sum()
    with open(MODELDIR / "costs.csv", "a") as f:
        f.write(f"valid costs\t{nvalid}/{coefs.shape[0]}\n")

    plot_error_distribution(
        model=model,
        dataf=dataf,
        target=target,
        figpath=MODELDIR / "error_distribution.png",
    )
