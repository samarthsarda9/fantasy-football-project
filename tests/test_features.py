from src.features import create_features, create_defensive_features
import polars as pl


def test_create_player_features():
    feature_test_data = pl.DataFrame({
        "player_display_name": [
            "Player A", "Player A", "Player A", "Player A", "Player A",
            "Player B", "Player B", "Player B",
        ],
        "season": [2024, 2024, 2024, 2024, 2025, 2024, 2024, 2025],
        "week": [15, 16, 17, 18, 1, 1, 2, 1],
        "calculated_ppr": [10.0, 20.0, 30.0, 40.0, 50.0, 5.0, 15.0, 25.0],
        "targets": [1, 2, 3, 4, 5, 1, 2, 3],
        "receptions": [1, 2, 3, 4, 5, 1, 2, 3],
        "receiving_yards": [10, 20, 30, 40, 50, 10, 20, 30],
    })

    result = create_features(feature_test_data)
    player_a = result.filter(pl.col("player_display_name") == "Player A")

    assert player_a.item(0, "prev_rolling_3_ppr") is None
    assert player_a.item(1, "prev_rolling_3_ppr") is None
    assert player_a.item(2, "prev_rolling_3_ppr") is None

    assert player_a.item(3, "prev_rolling_3_ppr") == 20.0
    assert player_a.item(4, "prev_rolling_3_ppr") == 30.0

    assert player_a.item(0, "prev_season_avg_ppr") is None
    assert player_a.item(1, "prev_season_avg_ppr") == 10.0
    assert player_a.item(2, "prev_season_avg_ppr") == 15.0
    assert player_a.item(3, "prev_season_avg_ppr") == 20.0
    assert player_a.item(4, "prev_season_avg_ppr") is None


def test_create_defensive_features():
    defensive_test_data = pl.DataFrame({
        "player_display_name": [
            "Player A", "Player B",
            "Player C", "Player D",
            "Player E",
            "Player F", "Player G",
            "Player H",
        ],
        "season": [2024, 2024, 2024, 2024, 2024, 2024, 2024, 2025],
        "week": [1, 1, 2, 2, 3, 1, 2, 1],
        "opponent_team": ["DAL", "DAL", "DAL", "DAL", "DAL", "NYG", "NYG", "DAL"],
        "calculated_ppr": [10.0, 20.0, 30.0, 5.0, 40.0, 8.0, 12.0, 100.0],
    })

    result = create_defensive_features(defensive_test_data)

    dal_week_1 = result.filter(
        (pl.col("season") == 2024)
        & (pl.col("week") == 1)
        & (pl.col("opponent_team") == "DAL")
    )

    dal_week_2 = result.filter(
        (pl.col("season") == 2024)
        & (pl.col("week") == 2)
        & (pl.col("opponent_team") == "DAL")
    )

    dal_week_3 = result.filter(
        (pl.col("season") == 2024)
        & (pl.col("week") == 3)
        & (pl.col("opponent_team") == "DAL")
    )

    nyg_week_2 = result.filter(
        (pl.col("season") == 2024)
        & (pl.col("week") == 2)
        & (pl.col("opponent_team") == "NYG")
    )

    dal_2025_week_1 = result.filter(
        (pl.col("season") == 2025)
        & (pl.col("week") == 1)
        & (pl.col("opponent_team") == "DAL")
    )

    assert dal_week_1.item(0, "prev_defense_wr_ppr_allowed_avg") is None

    assert dal_week_2.item(0, "prev_defense_wr_ppr_allowed_avg") == 30.0
    assert dal_week_2.item(1, "prev_defense_wr_ppr_allowed_avg") == 30.0

    assert dal_week_3.item(0, "prev_defense_wr_ppr_allowed_avg") == 32.5

    assert nyg_week_2.item(0, "prev_defense_wr_ppr_allowed_avg") == 8.0

    assert dal_2025_week_1.item(0, "prev_defense_wr_ppr_allowed_avg") is None


if __name__ == "__main__":
    test_create_player_features()
    test_create_defensive_features()
    print("All feature tests passed.")