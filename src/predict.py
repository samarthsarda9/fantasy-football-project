import polars as pl

from src.modeling import FEATURE_COLUMNS


def get_latest_player_row(features_df: pl.DataFrame, player_display_name: str) -> pl.DataFrame:
    """
    Finds a player's most recent row of computed features.

    Parameters:
    features_df (pl.DataFrame): Output of create_features()/create_defensive_features(),
        containing rolling/season-to-date/defensive features for every player-week.
    player_display_name (str): Player to look up.

    Returns:
    pl.DataFrame: A single-row DataFrame with that player's latest season/week.
    """
    player_rows = (
        features_df
        .filter(pl.col("player_display_name") == player_display_name)
        .sort(["season", "week"])
    )

    if player_rows.height == 0:
        raise ValueError(f"No rows found for player: {player_display_name}")

    return player_rows.tail(1)


def predict_player_projection(
    model,
    player_row: pl.DataFrame,
    feature_columns: list[str] = FEATURE_COLUMNS,
) -> float:
    """
    Predicts next-week full-PPR points for a single player from a trained model.

    Parameters:
    model: A trained scikit-learn regressor (e.g. from train_linear_regression()).
    player_row (pl.DataFrame): A single row containing feature_columns, such as
        the output of get_latest_player_row().
    feature_columns (list[str]): Feature columns the model expects, in order.

    Returns:
    float: Projected full-PPR points, rounded to 2 decimals.
    """
    if player_row.height != 1:
        raise ValueError("player_row must contain exactly one row")

    X = player_row.select(feature_columns).to_numpy()
    prediction = model.predict(X)[0]
    return round(float(prediction), 2)


def predict_next_week_ppr(
    model,
    features_df: pl.DataFrame,
    player_display_name: str,
    feature_columns: list[str] = FEATURE_COLUMNS,
) -> float:
    """
    Looks up a player's latest feature row and predicts next-week full-PPR points.

    Parameters:
    model: A trained scikit-learn regressor (e.g. from train_linear_regression()).
    features_df (pl.DataFrame): Output of create_features()/create_defensive_features().
    player_display_name (str): Player to project.
    feature_columns (list[str]): Feature columns the model expects, in order.

    Returns:
    float: Projected full-PPR points, rounded to 2 decimals.
    """
    player_row = get_latest_player_row(features_df, player_display_name)
    return predict_player_projection(model, player_row, feature_columns)
