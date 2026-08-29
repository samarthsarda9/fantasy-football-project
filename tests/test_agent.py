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


class _FakeMonkeypatch:
    """Minimal stand-in for pytest's monkeypatch fixture so these tests can run
    as a plain script, matching this project's existing test-script convention."""

    def setattr(self, obj, name, value):
        setattr(obj, name, value)


if __name__ == "__main__":
    mp = _FakeMonkeypatch()
    test_fetch_projection_found(mp)
    test_fetch_projection_not_found(mp)
    print("All agent tests passed.")
