"""Assignment - making a sklearn estimator.

The goal of this assignment is to implement by yourself a scikit-learn
estimator for the OneNearestNeighbor and check that it is working properly.

The nearest neighbor classifier predicts for a point X_i the target y_k of
the training sample X_k which is the closest to X_i. We measure proximity with
the Euclidean distance. The model will be evaluated with the accuracy (average
number of samples corectly classified). You need to implement the `fit`,
`predict` and `score` methods for this class. The code you write should pass
the test we implemented. You can run the tests by calling at the root of the
repo `pytest test_sklearn_questions.py`.

We also ask to respect the pep8 convention: https://pep8.org. This will be
enforced with `flake8`. You can check that there is no flake8 errors by
calling `flake8` at the root of the repo.

Finally, you need to write docstring similar to the one in `numpy_questions`
for the methods you code and for the class. The docstring will be checked using
`pydocstyle` that you can also call at the root of the repo.
"""
import numpy as np
from collections import Counter
from sklearn.base import BaseEstimator
from sklearn.base import ClassifierMixin
from sklearn.utils.validation import check_X_y
from sklearn.utils.validation import check_array
from sklearn.utils.validation import check_is_fitted
from sklearn.utils.multiclass import check_classification_targets


class OneNearestNeighbor(BaseEstimator, ClassifierMixin):
    """OneNearestNeighbor classifier."""

    def __init__(self):  # noqa: D107
        pass

    def fit(self, X, y):
        """Fit the nearest neighbor classifier from the training dataset.

        Parameters :
        X : Training data (ndarray of shape (n_samples, n_features))
        Y : Target values (array-like of shape (n_samples,) or
        (n_samples, n_targets))
        """
        X, y = check_X_y(X, y)
        check_classification_targets(y)
        self.classes_ = np.unique(y)

        # XXX fix
        self.X_train_ = X
        self.y_train_ = y
        self.n_features_in_ = X.shape[1]
        return self

    def predict(self, X):
        """Predict the class labels for the provided data.

        Parameters:
        X : Test samples
        """
        check_is_fitted(self)
        X = check_array(X)
        y_pred = np.full(
            shape=len(X), fill_value=self.classes_[0],
            dtype=self.classes_.dtype
        )

        # XXX fix
        for index, element in enumerate(X):
            distance_list = []
            nearest_neighbour = []
            for x in self.X_train_:
                distance = self.euclid_distance(element, x)
                distance_list.append(distance)
            sorted_list = np.argsort(distance_list)[:1]
            for sort_distance in sorted_list:
                nearest_neighbour.append(self.y_train_[sort_distance])
            pred = self.mode(nearest_neighbour)
            y_pred[index] = pred
        return y_pred

    def score(self, X, y):
        """Return the mean accuracy on the given test data and labels.

        Parameters :
        X : Test samples
        y : True labels for X
        """
        X, y = check_X_y(X, y)
        y_pred = self.predict(X)

        # XXX fix
        accuracy_score = (y_pred == y).sum() / len(y)
        return accuracy_score

    def mode(self, labels):
        """Returns the  most commonly occured value."""
        return Counter(labels).most_common(1)[0][0]

    def euclid_distance(self, point1, point2):
        """Returns the euclidean distance between two points."""
        return np.sqrt(np.sum((point1 - point2) ** 2))
