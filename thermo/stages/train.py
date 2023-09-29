from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.base import RegressorMixin
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

from thermo.utils.logger import ml_logger as logger


def get_estimator(name: str) -> RegressorMixin:
    """
    Returns a sklearn estimator based on the given name.

    Note: this function is ready to take other linear models
        but we havent implemented that yet.

    Args:
        name: The name of the estimator.

    Returns:
        The corresponding sklearn estimator.

    Raises:
        NameError: If the estimator name is not supported.
    """
    match name:
        case "RidgeRegression":
            from sklearn.linear_model import Ridge

            return Ridge(positive=True)
        case _:
            raise NameError(f"Estimator {name} is not supported")


def get_feature_targets(
    dataf: pd.DataFrame, target: str
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Splits the DataFrame into feature matrix X and target vector y.

    Args:
        dataf: The input DataFrame.
        target: The name of the target column.

    Returns:
        tuple: A tuple containing the feature matrix X
            and the target vector y.
    """
    dataf = dataf.sample(frac=1, random_state=42)  # Shuffle
    y = dataf[target]
    X = dataf.drop(columns=target)
    return X, y


@dataclass
class CVResult:
    """Class representing the results of cross-validation.

    Attributes:
        name (str): The name of the model.
        estimator (RegressorMixin): The fitted estimator.
        cv_results (pd.DataFrame): The cross-validation results.
        r2_score (float): The R-squared score.
        l2_weight (float): The L2 weight.

    Methods:
        __repr__(): Returns a string representation of the CVResult object.
    """

    name: str
    estimator: RegressorMixin
    cv_results: pd.DataFrame
    r2_score: float
    l2_weight: float

    def __repr__(self) -> str:
        return (
            f"model\t\t{self.name}\n"
            f"r2 score\t{round(self.r2_score,2)}\n"
            f"l2 weight\t{self.l2_weight}\n"
        )


def train_cv(
    X: pd.DataFrame,
    y: pd.Series,
    estimator_name: str = "RidgeRegression",
    cv_folds: int = 5,
    alpha_min: float = 0.001,
    alpha_max: float = 1,
    **_,
) -> CVResult:
    """
    Trains a ML regression model and finds the optimal L2 regularization coefficient
    (alpha) using cross-validation.

    Args:
        X: The feature matrix.
        y: The target vector.
        estimator_name: The name of the estimator to use. Defaults to "RidgeRegression".
        cv_folds: The number of cross-validation folds. Defaults to 5.
        alpha_min: The minimum alpha value for hyperparameter search. Defaults to 0.001.
        alpha_max: The maximum alpha value for hyperparameter search. Defaults to 1.
        **_: Optional additional keyword arguments (ignored).

    Returns:
        CVResult: The cross-validation results.

    Note:
        The function performs a grid search to find the best
        hyperparameters for the specified estimator.
    """
    # Get hyperparameters range
    log_min, log_max = tuple(map(np.log10, (alpha_min, alpha_max)))
    alphas = 10 ** np.linspace(
        log_min, log_max, 1 + 4 * int(log_max - log_min), endpoint=True
    )

    # Find parameters and hyperparameters
    cv = GridSearchCV(
        estimator=Pipeline(steps=[("regression", get_estimator(name=estimator_name))]),
        param_grid={"regression__alpha": alphas},
        cv=cv_folds,
        scoring=["r2", "neg_root_mean_squared_error"],
        refit="r2",
        return_train_score=True,
        n_jobs=-1,
        verbose=1,
    )

    cv.fit(X, y)

    return CVResult(
        estimator=cv.best_estimator_,
        cv_results=pd.DataFrame(cv.cv_results_),
        r2_score=cv.best_score_,
        l2_weight=cv.best_params_["regression__alpha"],
        name=estimator_name,
    )


if __name__ == "__main__":
    from pathlib import Path

    import dvc.api
    import joblib

    from thermo.utils.formatting import prettyparams

    logger.info("Running training script")
    # Get preprocessing params:
    params = dvc.api.params_show()["train"]

    target = params["target"]

    # Load data:
    logger.info("Loading data...")
    dataf = pd.read_pickle(Path("data") / "preprocessed_data.pkl")

    # Train by cross_validation:
    logger.info("Training model...")
    logger.debug(f"\n{prettyparams(params)}")
    X, y = get_feature_targets(dataf, target)
    result = train_cv(X, y, **params)

    logger.info(f"Model training successful, with r2 score {result.r2_score:.2f}")

    # Save cross-validation results:
    logger.info("Saving model...")
    MODELDIR = Path("model")
    MODELDIR.mkdir(parents=True, exist_ok=True)
    result.cv_results.to_csv(MODELDIR / "cross_validation.csv", index=False)

    # Save result
    with open(MODELDIR / "model.joblib", "wb") as f:
        joblib.dump(result.estimator, f)

    (MODELDIR / "model.metadata").write_text(str(result))
