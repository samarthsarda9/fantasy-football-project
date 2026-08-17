import polars as pl

def calculate_ppr(df: pl.DataFrame) -> pl.DataFrame:
    """
    Calculate the PPR (Points Per Reception) for each player in the DataFrame.

    Parameters:
    df (pl.DataFrame): Input DataFrame containing player statistics.

    Returns:
    pl.DataFrame: Original DataFrame with new column as calculated_ppr.
    """
    return df.with_columns(
        (
            pl.col('receptions')
            + (pl.col('receiving_yards') * 0.1)
            + (pl.col('receiving_tds') * 6)
            + (pl.col('rushing_yards') * 0.1)
            + (pl.col('rushing_tds') * 6)
            - (pl.col('receiving_fumbles_lost') * 2)
            - (pl.col('rushing_fumbles_lost') * 2)
        ).round(2).alias("calculated_ppr")
    )

