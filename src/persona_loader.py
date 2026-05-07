from pathlib import Path

import yaml


def load_persona(path: str) -> dict:
    """Load a persona YAML file."""
    persona_path = Path(path)
    if not persona_path.exists():
        raise FileNotFoundError(f"Persona file not found: {persona_path}")

    try:
        with persona_path.open("r", encoding="utf-8") as file:
            persona = yaml.safe_load(file) or {}
    except yaml.YAMLError as exc:
        raise ValueError(f"Could not parse persona YAML at {persona_path}: {exc}") from exc

    if not isinstance(persona, dict):
        raise ValueError(f"Persona file must contain a mapping: {persona_path}")
    if "name" not in persona:
        raise ValueError(f"Persona file is missing required field 'name': {persona_path}")

    return persona


def load_all_personas(persona_dir: str) -> dict:
    """Load all YAML personas in a directory keyed by persona name."""
    directory = Path(persona_dir)
    if not directory.exists():
        raise FileNotFoundError(f"Persona directory not found: {directory}")
    if not directory.is_dir():
        raise NotADirectoryError(f"Persona path is not a directory: {directory}")

    personas = {}
    for path in sorted(directory.glob("*.yaml")):
        persona = load_persona(str(path))
        personas[persona["name"]] = persona

    if not personas:
        raise FileNotFoundError(f"No persona YAML files found in: {directory}")

    return personas
