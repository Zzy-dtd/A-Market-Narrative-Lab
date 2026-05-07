import os


MOCK_MODE = "Mock mode"
LIVE_MODE = "Live OpenAI API mode"
DEFAULT_MODEL = "gpt-5.2"


def resolve_openai_api_key(session_key: str | None = None) -> str:
    """Resolve API key from session input first, then environment fallback."""
    if session_key and session_key.strip():
        return session_key.strip()
    return os.getenv("OPENAI_API_KEY", "").strip()


def is_mock_mode(api_mode: str) -> bool:
    return api_mode == MOCK_MODE


def normalize_model_name(model_name: str | None) -> str:
    """Normalize display-style model names into API-id style strings."""
    if not model_name or not model_name.strip():
        return os.getenv("OPENAI_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL
    return "-".join(model_name.strip().lower().split())


def friendly_openai_error(exc: Exception) -> str:
    """Return a readable error without exposing credentials or noisy internals."""
    message = str(exc)
    if "model_not_found" in message or "does not exist" in message:
        return (
            "OpenAI API call failed because the selected model name was not found or your account does not have access to it. "
            "Use an API model ID such as `gpt-5.2`, or check the model name in Settings."
        )
    if "invalid_api_key" in message or "Incorrect API key" in message:
        return "OpenAI API call failed because the API key is invalid. Please re-enter the key in Settings."
    return "OpenAI API call failed. Please check your API key, model name, and network connection."
