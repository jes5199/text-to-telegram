"""Configuration loading."""

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    token: str
    chat_id: int


def load_config(path: Path) -> Config:
    """Load config from JSON file."""
    try:
        data = json.loads(path.read_text())
    except FileNotFoundError:
        raise SystemExit(f"Config file not found: {path}")
    except json.JSONDecodeError as e:
        raise SystemExit(f"Invalid JSON in config file: {e}")

    if "token" not in data:
        raise SystemExit("Config missing required field: token")
    if "chat_id" not in data:
        raise SystemExit("Config missing required field: chat_id")

    return Config(token=data["token"], chat_id=int(data["chat_id"]))
