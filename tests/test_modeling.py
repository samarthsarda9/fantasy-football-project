from src.modeling import make_train_test_data, evaluate_predictions
import polars as pl
import numpy as np


def test_make_train_test_data_splits_by_season():
    data = pl.DataFrame({
        "season": [2023, 2023, 2024, 2024, 2025, 2025],
        "feature_a": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
        "feature_b": [10.0, 20.0, 30.0, 40.0, 50.0, 60.0],
        "target": [100.0, 200.0, 300.0, 400.0, 500.0, 600.0],
    })

    X_train, X_test, y_train, y_test = make_train_test_data(
        data,
        feature_columns=["feature_a", "feature_b"],
        target_column="target",
        test_season=2025,
    )

    assert X_train.shape == (4, 2)
    assert X_test.shape == (2, 2)

    assert list(y_train) == [100.0, 200.0, 300.0, 400.0]
    assert list(y_test) == [500.0, 600.0]

    assert list(X_test[0]) == [5.0, 50.0]
    assert list(X_test[1]) == [6.0, 60.0]


def test_evaluate_predictions():
    y_true = np.array([10.0, 20.0, 30.0])
    y_pred = np.array([12.0, 18.0, 30.0])

    mae, rmse = evaluate_predictions(y_true, y_pred)

    # Errors are 2, 2, 0 -> mean absolute error = 4/3
    assert mae == round(4 / 3, 2)
    # Squared errors are 4, 4, 0 -> mean = 8/3, rmse = sqrt(8/3)
    assert rmse == round((8 / 3) ** 0.5, 2)


if __name__ == "__main__":
    test_make_train_test_data_splits_by_season()
    test_evaluate_predictions()
    print("All modeling tests passed.")
