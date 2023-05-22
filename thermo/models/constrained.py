import cvxpy as cp
import numpy as np
from numpy.typing import NDArray
from scipy import sparse
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.exceptions import FitFailedWarning
from sklearn.utils.validation import check_is_fitted


class ConstrainedRidge(RegressorMixin, BaseEstimator):
    def __init__(
        self,
        alpha: float = 1.0,
        G: NDArray | None = None,
        h: NDArray | None = None,
        A: NDArray | None = None,
        b: NDArray | None = None,
    ):
        """
        Minimizes the mean squared error with regularization alpha under constraints:
        G @ w >= h
        A @ w == b
        """
        self.alpha = alpha
        self.G = G
        self.h = h
        self.A = A
        self.b = b

    @staticmethod
    def _validate_constraints(A: NDArray, b: NDArray) -> None:
        if len(A.shape) != 2:
            raise ValueError(
                f"G must be a 2D numpy array, but shape {A.shape} was given."
            )
        if b is not None:  # if b is ambiguous
            if len(b.shape) != 1:
                raise ValueError(
                    f"G must be a 1D numpy array, but shape {b.shape} was given."
                )
            elif b.shape[0] != A.shape[0]:
                raise ValueError(
                    f"The dimensions of G {A.shape} and h {b.shape} do not match."
                )
            else:
                return b
        else:
            return np.zeros(A.shape[0])

    def fit(self, X: NDArray, y: NDArray) -> "ConstrainedRidge":
        y = y.to_numpy().flatten()

        # Add a 1 padding to X to model for intercept
        if isinstance(X, sparse.csr_matrix):
            X_ = sparse.hstack((X, np.ones((X.shape[0], 1))))
        else:
            X_ = np.c_[X, np.ones(X.shape[0])]

        # Define variables for Quadratic programming
        w = cp.Variable(X_.shape[1])
        P = X_.T @ X_
        P += self.alpha * np.eye(P.shape[0])  # L2 regularization
        q = X_.T @ y

        # Constraints
        constraints = []
        if self.G is not None:  # if G is ambiguous
            self.h = self._validate_constraints(self.G, self.h)
            constraints.append(self.G @ w >= self.h)
        if self.A is not None:
            self.b = self._validate_constraints(self.A, self.b)
            constraints.append(self.A @ w == self.b)

        # Quadratic programming problem
        problem = cp.Problem(
            cp.Minimize(0.5 * cp.quad_form(w, P) - q.T @ w), constraints
        )
        problem.solve()

        self.status_ = problem.status

        # Extract coefficients
        if self.status_ == "optimal":
            self.fitted_ = True
        else:
            self.fitted_ = False
            msg = (
                "cvxpy failed to solve quadratic programming problem,"
                f" with status {self.status_}"
            )
            raise FitFailedWarning(msg)

        self.coef_ = w.value[:-1]
        self.intercept_ = w.value[-1]

        return self

    def predict(self, X: NDArray) -> NDArray:
        check_is_fitted(self, "fitted_")
        return X @ self.coef_ + self.intercept_
