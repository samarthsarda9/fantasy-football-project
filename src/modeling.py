import polars as pl
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
import numpy as np
import joblib
from pathlib import Path

FEATURE_COLUMNS = [
    "prev_rolling_3_ppr",
    "prev_rolling_3_targets",
    "prev_rolling_3_receptions",
    "prev_rolling_3_receiving_yards",
    "prev_season_avg_ppr",
    "prev_defense_wr_ppr_allowed_avg"
]

TARGET_COLUMN = "calculated_ppr"
TEST_SEASON = 2025
DEFAULT_MODEL_PATH = Path("models/linear_regression.joblib")

def make_train_test_data(
    dataset: pl.DataFrame,
    feature_columns: list[str],
    target_column: str,
    test_season: int = TEST_SEASON,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Splits the input DataFrame into training and testing sets based on the season.

    Parameters:
    dataset (pl.DataFrame): Input DataFrame containing player statistics.
    feature_columns (list[str]): List of feature column names to be used for training.
    target_column (str): Name of the target column.
    test_season (int): Season to use as the test set. Earlier seasons are used for training.

    Returns:
    tuple: A tuple containing four numpy arrays: X_train, X_test, y_train, y_test.
    """
    X_train = dataset.filter(pl.col("season") < test_season).select(feature_columns).to_numpy()

    X_test = dataset.filter(pl.col("season") == test_season).select(feature_columns).to_numpy()

    y_train = dataset.filter(pl.col("season") < test_season).select(target_column).to_numpy().ravel()
    y_test = dataset.filter(pl.col("season") == test_season).select(target_column).to_numpy().ravel()   
    return X_train, X_test, y_train, y_test

def evaluate_predictions(y_true: np.ndarray, y_pred: np.ndarray) -> tuple[float, float]:
    """
    Calculates MAE and RMSE for a set of predictions.

    Parameters:
    y_true (np.ndarray): Actual target values.
    y_pred (np.ndarray): Predicted target values.

    Returns:
    tuple: (mae, rmse), each rounded to 2 decimal places.
    """
    mae = round(mean_absolute_error(y_true, y_pred), 2)
    rmse = round(root_mean_squared_error(y_true, y_pred), 2)
    return mae, rmse

def train_linear_regression(df: pl.DataFrame):
    """
    Trains a linear regression model using the provided DataFrame.

    Parameters:
    df (pl.DataFrame): Input DataFrame containing player statistics.

    Returns:
    tuple: A tuple containing the trained model, mean absolute error, and root mean squared error.
    """
    from sklearn.linear_model import LinearRegression

    X_train, X_test, y_train, y_test = make_train_test_data(
        df,
        FEATURE_COLUMNS,
        TARGET_COLUMN,
        TEST_SEASON,
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mae, rmse = evaluate_predictions(y_test, y_pred)

    return model, mae, rmse

def save_model(model, path: Path = DEFAULT_MODEL_PATH) -> None:
    """
    Saves a trained model to disk so it can be reused without retraining.

    Parameters:
    model: A trained scikit-learn model (e.g. from train_linear_regression()).
    path (Path): File path to save the model to. Parent directories are created if needed.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)

def load_model(path: Path = DEFAULT_MODEL_PATH):
    """
    Loads a previously saved model from disk.

    Parameters:
    path (Path): File path to load the model from.

    Returns:
    A trained scikit-learn model.
    """
    return joblib.load(Path(path))
