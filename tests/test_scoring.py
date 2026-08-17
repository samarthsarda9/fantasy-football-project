from src.scoring import calculate_ppr
import polars as pl

def test_calculate_ppr():
    data = {
        "player_display_name": ["Player A", "Player B"],
        "receptions": [5, 3],
        "receiving_yards": [100, 50],
        "receiving_tds": [1, 0],
        "rushing_yards": [20, 30],
        "rushing_tds": [0, 1],
        "receiving_fumbles_lost": [0, 1],
        "rushing_fumbles_lost": [0, 0],
    }

    df = pl.DataFrame(data)
    df_with_ppr = calculate_ppr(df)

    assert df_with_ppr.item(0, "calculated_ppr") == 23.0
    assert df_with_ppr.item(1, "calculated_ppr") == 15.0

    print("All scoring tests passed.")


if __name__ == "__main__":
    test_calculate_ppr()