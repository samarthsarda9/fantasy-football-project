from src.data import filter_wr_regular_season, WR_STAT_COLUMNS
import polars as pl


def test_filter_wr_regular_season():
    raw_stats = pl.DataFrame({
        "player_display_name": ["WR Player", "RB Player", "WR Playoff Player"],
        "position": ["WR", "RB", "WR"],
        "season": [2024, 2024, 2024],
        "season_type": ["REG", "REG", "POST"],
        "week": [1, 1, 19],
        "team": ["DAL", "DAL", "DAL"],
        "opponent_team": ["NYG", "NYG", "NYG"],
        "receptions": [5, 3, 6],
        "targets": [7, 5, 8],
        "receiving_yards": [60, 40, 70],
        "receiving_tds": [1, 0, 1],
        "receiving_fumbles_lost": [0, 0, 0],
        "receiving_2pt_conversions": [0, 0, 0],
        "special_teams_tds": [0, 0, 0],
        "rushing_yards": [0, 20, 0],
        "rushing_tds": [0, 0, 0],
        "rushing_fumbles_lost": [0, 0, 0],
        "rushing_2pt_conversions": [0, 0, 0],
        "fantasy_points_ppr": [11.0, 7.0, 13.0],
    })

    result = filter_wr_regular_season(raw_stats)

    assert result.shape[0] == 1
    assert result.item(0, "player_display_name") == "WR Player"
    assert result.columns == WR_STAT_COLUMNS


if __name__ == "__main__":
    test_filter_wr_regular_season()
    print("All data tests passed.")
