from src.api_settings import LIVE_MODE, MOCK_MODE, is_mock_mode, resolve_openai_api_key


def test_resolve_openai_api_key_prefers_session_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "env-key")

    assert resolve_openai_api_key("session-key") == "session-key"


def test_resolve_openai_api_key_falls_back_to_env(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "env-key")

    assert resolve_openai_api_key("") == "env-key"


def test_resolve_openai_api_key_empty_without_sources(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    assert resolve_openai_api_key("") == ""


def test_is_mock_mode():
    assert is_mock_mode(MOCK_MODE) is True
    assert is_mock_mode(LIVE_MODE) is False
