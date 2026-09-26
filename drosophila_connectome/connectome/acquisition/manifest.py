"""Manifest creation and verification for immutable raw inputs."""
from __future__ import annotations
from datetime import datetime, timezone
import json
from pathlib import Path
from .checksum import sha256_file

def build_manifest(config: dict, raw_root: Path, output: Path) -> dict:
    files = []
    for spec in config["files"]:
        path = raw_root / spec["filename"]
        if not spec.get("source_url"):
            raise ValueError(f"raw artifact {spec['filename']} is missing its exact official source URL")
        if not path.is_file():
            raise FileNotFoundError(f"missing required raw artifact: {path}")
        files.append({"path": str(path), "sha256": sha256_file(path), "size_bytes": path.stat().st_size,
                      "role": spec["role"], "format": spec["format"], "source_url": spec.get("source_url"),
                      "reason": spec["reason"]})
    manifest = {key: config[key] for key in ("dataset_id", "name", "version", "sex", "coverage", "source_id", "source_url", "license")}
    manifest.update({"retrieved_at": datetime.now(timezone.utc).isoformat(), "files": files})
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest

def verify_manifest(path: Path) -> list[str]:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    failures = []
    for artifact in manifest["files"]:
        local = Path(artifact["path"])
        if not local.is_file(): failures.append(f"missing: {local}")
        elif sha256_file(local) != artifact["sha256"]: failures.append(f"hash mismatch: {local}")
    return failures
