import src.agent as agent


class StubResponse:
    def __init__(self, status_code: int, payload: dict | None = None):
        self.status_code = status_code
        self._payload = payload

    def json(self) -> dict:
        return self._payload

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


def test_fetch_projection_found(monkeypatch):
    def fake_get(url):
        assert url == f"{agent.API_BASE_URL}/predictions/CeeDee Lamb"
        return StubResponse(200, {"player_display_name": "CeeDee Lamb", "projected_ppr": 15.08})

    monkeypatch.setattr(agent.requests, "get", fake_get)

    message = agent._fetch_projection("CeeDee Lamb")

    assert "CeeDee Lamb" in message
    assert "15.08" in message


def test_fetch_projection_not_found(monkeypatch):
    def fake_get(url):
        return StubResponse(404)

    monkeypatch.setattr(agent.requests, "get", fake_get)

    message = agent._fetch_projection("Nobody")

    assert "No projection found" in message
    assert "Nobody" in message


def make_recent_stats_payload() -> dict:
    return {
        "player_display_name": "CeeDee Lamb",
        "season": 2025,
        "week": 18,
        "opponent_team": "NYG",
        "receptions": 1,
        "targets": 1,
        "receiving_yards": 4,
        "receiving_tds": 0,
        "calculated_ppr": 1.4,
        "prev_rolling_3_ppr": 12.6,
        "prev_season_avg_ppr": 16.62,
    }


def test_fetch_recent_stats_found(monkeypatch):
    def fake_get(url):
        assert url == f"{agent.API_BASE_URL}/players/CeeDee Lamb"
        return StubResponse(200, make_recent_stats_payload())

    monkeypatch.setattr(agent.requests, "get", fake_get)

    message = agent._fetch_recent_stats("CeeDee Lamb")

    assert "CeeDee Lamb" in message
    assert "season 2025, week 18" in message
    assert "12.6" in message
    assert "16.62" in message


def test_fetch_recent_stats_not_found(monkeypatch):
    def fake_get(url):
        return StubResponse(404)

    monkeypatch.setattr(agent.requests, "get", fake_get)

    message = agent._fetch_recent_stats("Nobody")

    assert "No stats found" in message
    assert "Nobody" in message


def test_compare_players_a_higher(monkeypatch):
    responses = {
        f"{agent.API_BASE_URL}/predictions/Player A": StubResponse(
            200, {"player_display_name": "Player A", "projected_ppr": 20.0}
        ),
        f"{agent.API_BASE_URL}/predictions/Player B": StubResponse(
            200, {"player_display_name": "Player B", "projected_ppr": 10.0}
        ),
    }
    monkeypatch.setattr(agent.requests, "get", lambda url: responses[url])

    message = agent._compare_players("Player A", "Player B")

    assert "Player A is projected higher" in message
    assert "20.0" in message
    assert "10.0" in message


def test_compare_players_tie(monkeypatch):
    responses = {
        f"{agent.API_BASE_URL}/predictions/Player A": StubResponse(
            200, {"player_display_name": "Player A", "projected_ppr": 15.0}
        ),
        f"{agent.API_BASE_URL}/predictions/Player B": StubResponse(
            200, {"player_display_name": "Player B", "projected_ppr": 15.0}
        ),
    }
    monkeypatch.setattr(agent.requests, "get", lambda url: responses[url])

    message = agent._compare_players("Player A", "Player B")

    assert "same projection" in message


def test_compare_players_first_not_found(monkeypatch):
    def fake_get(url):
        return StubResponse(404)

    monkeypatch.setattr(agent.requests, "get", fake_get)

    message = agent._compare_players("Nobody", "Player B")

    assert "No projection found" in message
    assert "Nobody" in message


class _FakeMonkeypatch:
    """Minimal stand-in for pytest's monkeypatch fixture so these tests can run
    as a plain script, matching this project's existing test-script convention."""

    def setattr(self, obj, name, value):
        setattr(obj, name, value)


if __name__ == "__main__":
    mp = _FakeMonkeypatch()
    test_fetch_projection_found(mp)
    test_fetch_projection_not_found(mp)
    test_fetch_recent_stats_found(mp)
    test_fetch_recent_stats_not_found(mp)
    test_compare_players_a_higher(mp)
    test_compare_players_tie(mp)
    test_compare_players_first_not_found(mp)
    print("All agent tests passed.")
