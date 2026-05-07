from src.api_settings import (
    DEFAULT_MODEL,
    LIVE_MODE,
    MOCK_MODE,
    friendly_openai_error,
    is_mock_mode,
    normalize_model_name,
    resolve_openai_api_key,
)


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


def test_normalize_model_name_converts_display_style():
    assert normalize_model_name("GPT-5.4 mini") == "gpt-5.4-mini"


def test_normalize_model_name_uses_default_for_empty(monkeypatch):
    monkeypatch.delenv("OPENAI_MODEL", raising=False)

    assert normalize_model_name("") == DEFAULT_MODEL


def test_friendly_openai_error_hides_raw_model_payload():
    message = friendly_openai_error(Exception("Error code: 400 - {'code': 'model_not_found'}"))

    assert "selected model name was not found" in message
    assert "Error code: 400" not in message
