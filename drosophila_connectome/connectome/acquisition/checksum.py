"""Streaming checksums used for immutable raw and derived artifacts."""
from __future__ import annotations
import hashlib
from pathlib import Path

CHUNK_SIZE = 1024 * 1024

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(CHUNK_SIZE), b""):
            digest.update(block)
    return digest.hexdigest()
