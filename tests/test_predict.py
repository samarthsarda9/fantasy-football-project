from src.predict import get_latest_player_row, predict_player_projection, predict_next_week_ppr
import polars as pl


class StubModel:
    """Fake model whose prediction is just the sum of the input features."""

    def predict(self, X):
        return X.sum(axis=1)


def make_features_df():
    return pl.DataFrame({
        "player_display_name": [
            "Player A", "Player A", "Player A",
            "Player B", "Player B",
        ],
        "season": [2024, 2024, 2025, 2024, 2024],
        "week": [16, 17, 1, 1, 2],
        "prev_rolling_3_ppr": [10.0, 12.0, 14.0, 5.0, 6.0],
        "prev_season_avg_ppr": [8.0, 9.0, 11.0, 4.0, 4.5],
    })


def test_get_latest_player_row():
    features_df = make_features_df()

    latest = get_latest_player_row(features_df, "Player A")

    assert latest.height == 1
    assert latest.item(0, "season") == 2025
    assert latest.item(0, "week") == 1


def test_get_latest_player_row_missing_player():
    features_df = make_features_df()

    try:
        get_latest_player_row(features_df, "Player Z")
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_predict_player_projection():
    features_df = make_features_df()
    feature_columns = ["prev_rolling_3_ppr", "prev_season_avg_ppr"]
    player_row = get_latest_player_row(features_df, "Player A")

    projection = predict_player_projection(StubModel(), player_row, feature_columns)

    assert projection == 25.0  # 14.0 + 11.0


def test_predict_next_week_ppr():
    features_df = make_features_df()
    feature_columns = ["prev_rolling_3_ppr", "prev_season_avg_ppr"]

    projection = predict_next_week_ppr(StubModel(), features_df, "Player B", feature_columns)

    assert projection == 10.5  # latest Player B row: 6.0 + 4.5


if __name__ == "__main__":
    test_get_latest_player_row()
    test_get_latest_player_row_missing_player()
    test_predict_player_projection()
    test_predict_next_week_ppr()
    print("All predict tests passed.")
