from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.base import RegressorMixin
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

from thermo.utils.logger import ml_logger as logger


def get_estimator(name: str) -> RegressorMixin:
    match name:
        case "RidgeRegression":
            from sklearn.linear_model import Ridge

            return Ridge(positive=True)
        case "ConstrainedRidge":
            from thermo.models.constrained import ConstrainedRidge

            logger.warning("Constraints not implemented for ConstrainedRidge")
            return ConstrainedRidge()
        case _:
            raise NameError(f"Estimator {name} is not supported")


def get_feature_targets(
    dataf: pd.DataFrame, target: str
) -> tuple[pd.DataFrame, pd.Series]:
    dataf = dataf.sample(frac=1, random_state=42)  # Shuffle
    y = dataf[target]
    X = dataf.drop(columns=target)
    return X, y


@dataclass
class CVResult:
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
):
    # Get hyperparameters range
    log_alpha = tuple(map(np.log10, (alpha_min, alpha_max)))
    alphas = 10 ** np.linspace(
        *log_alpha, 1 + 4 * int(log_alpha[1] - log_alpha[0]), endpoint=True
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

    logger.info("Running training script")
    # Get preprocessing params:
    params = dvc.api.params_show()["train"]

    target = params["target"]

    # Load data:
    logger.info("Loading data...")
    dataf = pd.read_pickle(Path("data") / "preprocessed_data.pkl")

    # Train by cross_validation:
    logger.info("Training model...")
    X, y = get_feature_targets(dataf, target)
    result = train_cv(X, y, **params)

    logger.info(f"Model training succesful, with r2 score {round(result.r2_score, 2)}")

    # Save cross-validation results:
    logger.info("Saving model...")
    MODELDIR = Path("model")
    MODELDIR.mkdir(parents=True, exist_ok=True)
    result.cv_results.to_csv(MODELDIR / "cross_validation.csv", index=False)

    # Save result
    with open(MODELDIR / "model.joblib", "wb") as f:
        joblib.dump(result.estimator, f)

    (MODELDIR / "model.metadata").write_text(str(result))
