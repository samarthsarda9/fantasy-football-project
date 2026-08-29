import nflreadpy as nfl
import polars as pl

WR_STAT_COLUMNS = [
    "player_display_name",
    "season",
    "season_type",
    "week",
    "team",
    "opponent_team",
    "receptions",
    "targets",
    "receiving_yards",
    "receiving_tds",
    "receiving_fumbles_lost",
    "receiving_2pt_conversions",
    "special_teams_tds",
    "rushing_yards",
    "rushing_tds",
    "rushing_fumbles_lost",
    "rushing_2pt_conversions",
    "fantasy_points_ppr",
]


def load_weekly_stats(seasons: list[int]) -> pl.DataFrame:
    """
    Loads raw weekly player stats for the given seasons from nflreadpy.

    Parameters:
    seasons (list[int]): NFL seasons to load, e.g. [2021, 2022, 2023].

    Returns:
    pl.DataFrame: Raw weekly player stats, all positions and season types.
    """
    return nfl.load_player_stats(seasons)


def filter_wr_regular_season(df: pl.DataFrame) -> pl.DataFrame:
    """
    Filters weekly player stats down to regular-season wide receiver rows
    and selects the fantasy-relevant columns used by feature engineering.

    Parameters:
    df (pl.DataFrame): Raw weekly player stats (any position/season type).

    Returns:
    pl.DataFrame: Regular-season WR rows with only WR_STAT_COLUMNS selected.
    """
    return (
        df
        .filter((pl.col("position") == "WR") & (pl.col("season_type") == "REG"))
        .select(WR_STAT_COLUMNS)
    )


def load_wr_weekly_stats(seasons: list[int]) -> pl.DataFrame:
    """
    Loads and filters regular-season WR weekly stats for the given seasons.

    Parameters:
    seasons (list[int]): NFL seasons to load, e.g. [2021, 2022, 2023].

    Returns:
    pl.DataFrame: Regular-season WR rows with only WR_STAT_COLUMNS selected.
    """
    return filter_wr_regular_season(load_weekly_stats(seasons))
