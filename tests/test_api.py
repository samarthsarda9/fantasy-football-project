import polars as pl
from fastapi.testclient import TestClient

import src.api as api


class StubModel:
    """Fake model whose prediction is just the sum of the input features."""

    def predict(self, X):
        return X.sum(axis=1)


def make_raw_stats() -> pl.DataFrame:
    """
    A small, fake weekly WR stat table (one player, four weeks) shaped like the
    real output of load_wr_weekly_stats(), so the real scoring/feature pipeline
    can run on it without hitting the network.
    """
    weeks = [1, 2, 3, 4]
    return pl.DataFrame({
        "player_display_name": ["Player A"] * 4,
        "season": [2024] * 4,
        "season_type": ["REG"] * 4,
        "week": weeks,
        "team": ["DAL"] * 4,
        "opponent_team": ["NYG", "PHI", "WAS", "NYG"],
        "receptions": [5, 6, 7, 8],
        "targets": [7, 8, 9, 10],
        "receiving_yards": [60.0, 70.0, 80.0, 90.0],
        "receiving_tds": [1, 0, 1, 0],
        "receiving_fumbles_lost": [0, 0, 0, 0],
        "receiving_2pt_conversions": [0, 0, 0, 0],
        "special_teams_tds": [0, 0, 0, 0],
        "rushing_yards": [0.0, 0.0, 0.0, 0.0],
        "rushing_tds": [0, 0, 0, 0],
        "rushing_fumbles_lost": [0, 0, 0, 0],
        "rushing_2pt_conversions": [0, 0, 0, 0],
        "fantasy_points_ppr": [0.0, 0.0, 0.0, 0.0],
    })


def make_client() -> TestClient:
    """
    Swaps out the two side-effecting calls (network fetch + trained-model load)
    made during api.py's startup, so tests run offline and deterministically.
    """
    api.load_wr_weekly_stats = lambda seasons: make_raw_stats()
    api.load_model = lambda: StubModel()
    return TestClient(api.app)


def test_health_check():
    with make_client() as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_player_stats_found():
    with make_client() as client:
        response = client.get("/players/Player A")

    assert response.status_code == 200
    body = response.json()
    assert body["player_display_name"] == "Player A"
    assert body["season"] == 2024
    assert body["week"] == 4


def test_get_player_stats_not_found():
    with make_client() as client:
        response = client.get("/players/Nobody")

    assert response.status_code == 404


def test_get_player_projection_found():
    with make_client() as client:
        response = client.get("/predictions/Player A")

    assert response.status_code == 200
    body = response.json()
    assert body["player_display_name"] == "Player A"
    assert isinstance(body["projected_ppr"], float)


def test_get_player_projection_not_found():
    with make_client() as client:
        response = client.get("/predictions/Nobody")

    assert response.status_code == 404


if __name__ == "__main__":
    test_health_check()
    test_get_player_stats_found()
    test_get_player_stats_not_found()
    test_get_player_projection_found()
    test_get_player_projection_not_found()
    print("All API tests passed.")
