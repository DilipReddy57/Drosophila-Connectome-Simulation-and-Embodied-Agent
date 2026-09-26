"""Dataset configuration loading. JSON is used so it can be schema-validated without dependencies."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG = ROOT / "configs" / "fafb_v783.json"

def load_config(path: Path | None = None) -> dict:
    with (path or DEFAULT_CONFIG).open(encoding="utf-8") as handle:
        return json.load(handle)
