"""Streaming, resumable downloads that never replace a verified raw file."""
from __future__ import annotations
from pathlib import Path
from urllib.request import Request, urlopen
from .checksum import sha256_file
from .source import require_official_url

CHUNK_SIZE = 1024 * 1024

def download(url: str, destination: Path, expected_sha256: str | None = None) -> Path:
    require_official_url(url)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        actual = sha256_file(destination)
        if expected_sha256 and actual.lower() == expected_sha256.lower():
            return destination
        raise FileExistsError(f"refusing to overwrite existing unverified file: {destination}")
    partial = destination.with_name(destination.name + ".part")
    offset = partial.stat().st_size if partial.exists() else 0
    request = Request(url, headers={"Range": f"bytes={offset}-"} if offset else {})
    with urlopen(request) as response:  # nosec B310: source host is allow-listed above
        status = getattr(response, "status", response.getcode())
        if offset and status != 206:
            partial.unlink(missing_ok=True)
            return download(url, destination, expected_sha256)
        mode = "ab" if offset else "wb"
        with partial.open(mode) as output:
            for block in iter(lambda: response.read(CHUNK_SIZE), b""):
                output.write(block)
    actual = sha256_file(partial)
    if expected_sha256 and actual.lower() != expected_sha256.lower():
        raise ValueError(f"checksum mismatch for {url}: expected {expected_sha256}, got {actual}")
    partial.replace(destination)
    return destination
