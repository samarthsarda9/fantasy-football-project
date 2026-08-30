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
    # Player A has four 2024 (latest-season) weeks; Player C only has an
    # earlier 2023 week, to exercise /players' latest-season filtering.
    return pl.DataFrame({
        "player_display_name": ["Player A"] * 4 + ["Player C"],
        "season": [2024] * 4 + [2023],
        "season_type": ["REG"] * 5,
        "week": [1, 2, 3, 4, 1],
        "team": ["DAL"] * 4 + ["NYG"],
        "opponent_team": ["NYG", "PHI", "WAS", "NYG", "DAL"],
        "receptions": [5, 6, 7, 8, 3],
        "targets": [7, 8, 9, 10, 5],
        "receiving_yards": [60.0, 70.0, 80.0, 90.0, 40.0],
        "receiving_tds": [1, 0, 1, 0, 0],
        "receiving_fumbles_lost": [0, 0, 0, 0, 0],
        "receiving_2pt_conversions": [0, 0, 0, 0, 0],
        "special_teams_tds": [0, 0, 0, 0, 0],
        "rushing_yards": [0.0, 0.0, 0.0, 0.0, 0.0],
        "rushing_tds": [0, 0, 0, 0, 0],
        "rushing_fumbles_lost": [0, 0, 0, 0, 0],
        "rushing_2pt_conversions": [0, 0, 0, 0, 0],
        "fantasy_points_ppr": [0.0, 0.0, 0.0, 0.0, 0.0],
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


def test_list_players_returns_latest_season_only():
    with make_client() as client:
        response = client.get("/players")

    assert response.status_code == 200
    assert response.json() == ["Player A"]


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


class StubRunResult:
    def __init__(self, final_output, new_items):
        self.final_output = final_output
        self.new_items = new_items


class FakeRunner:
    """Stands in for agents.Runner so tests never make a real LLM call."""

    @staticmethod
    async def run(agent, question):
        return StubRunResult(final_output=f"Echo: {question}", new_items=[])


class FailingRunner:
    @staticmethod
    async def run(agent, question):
        raise RuntimeError("boom")


def test_ask_agent_success():
    original_runner = api.Runner
    api.Runner = FakeRunner
    try:
        with make_client() as client:
            response = client.post("/agent/ask", json={"question": "How good is Player A?"})
    finally:
        api.Runner = original_runner

    assert response.status_code == 200
    body = response.json()
    assert body["answer"] == "Echo: How good is Player A?"
    assert body["trace"] == []


def test_ask_agent_failure():
    original_runner = api.Runner
    api.Runner = FailingRunner
    try:
        with make_client() as client:
            response = client.post("/agent/ask", json={"question": "How good is Player A?"})
    finally:
        api.Runner = original_runner

    assert response.status_code == 502


if __name__ == "__main__":
    test_health_check()
    test_list_players_returns_latest_season_only()
    test_get_player_stats_found()
    test_get_player_stats_not_found()
    test_get_player_projection_found()
    test_get_player_projection_not_found()
    test_ask_agent_success()
    test_ask_agent_failure()
    print("All API tests passed.")
