from src.features import create_features
import polars as pl

def test_create_features():
    feature_test_data = pl.DataFrame({
        "player_display_name": [
            "Player A",
            "Player A",
            "Player A",
            "Player A",
            "Player A",
            "Player B",
            "Player B",
            "Player B",
        ],
        "season": [
            2024,
            2024,
            2024,
            2024,
            2025,
            2024,
            2024,
            2025,
        ],
        "week": [
            15,
            16,
            17,
            18,
            1,
            1,
            2,
            1,
        ],
        "calculated_ppr": [
            10.0,
            20.0,
            30.0,
            40.0,
            50.0,
            5.0,
            15.0,
            25.0,
        ],
        "targets": [
            1,
            2,
            3,
            4,
            5,
            1,
            2,
            3,
        ],
        "receptions": [
            1,
            2,
            3,
            4,
            5,
            1,
            2,
            3,
        ],
        "receiving_yards": [
            10,
            20,
            30,
            40,
            50,
            10,
            20,
            30,
        ],
    })
    result = create_features(feature_test_data)
    player_a = result.filter(pl.col("player_display_name") == "Player A")
    assert player_a.item(3, "prev_rolling_3_ppr") == 20.0
    assert player_a.item(4, "prev_rolling_3_ppr") == 30.0
    assert player_a.item(4, "prev_season_avg_ppr") is None

    print("All feature tests passed.")

if __name__ == "__main__":
    test_create_features()