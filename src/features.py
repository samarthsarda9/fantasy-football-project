import polars as pl

def create_features(df: pl.DataFrame) -> pl.DataFrame:
    """
    Performs feature engineering to create rolling averages of features such as PPR points,
    targets, receptions, and receiving yards. There will also be a season-to-date value that averages PPR
    points of all the weeks before the current one. For rolling averages, the last value from the previous season
    will carry over to the beginning of the next season (i.e. week 18 value is baseline for week 1 the following season).
    However, the season-to-date average will remain within a season and will reset once a season ends. 

    Parameters: 
    df (pl.DataFrame): Input DataFrame containing player statistics.

    Returns:
    pl.DataFrame: Original Dataframe with new columns containing rolling averages and season-to-date average.
    """
    return (
        df
        .sort(["player_display_name", "season", "week"])
        .with_columns(
            pl.col("calculated_ppr")
            .shift(1)
            .rolling_mean(window_size=3, min_samples=3)
            .round(2)
            .over(["player_display_name"])
            .alias("prev_rolling_3_ppr"),

            pl.col("targets")
            .shift(1)
            .rolling_mean(window_size=3, min_samples=3)
            .round(2)
            .over(["player_display_name"])
            .alias("prev_rolling_3_targets"),

            pl.col("receptions")
            .shift(1)
            .rolling_mean(window_size=3, min_samples=3)
            .round(2)
            .over(["player_display_name"])
            .alias("prev_rolling_3_receptions"),

            pl.col("receiving_yards")
            .shift(1)
            .rolling_mean(window_size=3, min_samples=3)
            .round(2)
            .over(["player_display_name"])
            .alias("prev_rolling_3_receiving_yards"),

            (
                pl.col("calculated_ppr").shift(1).cum_sum().over(["player_display_name", "season"])
                /
                pl.col("calculated_ppr").shift(1).cum_count().over(["player_display_name", "season"])
            )
            .round(2)
            .alias("prev_season_avg_ppr")
        )
    )