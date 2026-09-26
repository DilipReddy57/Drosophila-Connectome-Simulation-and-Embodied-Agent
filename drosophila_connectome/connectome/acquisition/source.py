"""Official-source guardrails for downloads."""
from __future__ import annotations
from urllib.parse import urlparse

OFFICIAL_HOSTS = {"flywire.ai", "www.flywire.ai", "codex.flywire.ai", "github.com", "raw.githubusercontent.com"}

def is_official_url(url: str) -> bool:
    host = urlparse(url).hostname
    return bool(host and (host in OFFICIAL_HOSTS or host.endswith(".flywire.ai")))

def require_official_url(url: str) -> None:
    if not is_official_url(url):
        raise ValueError(f"refusing non-official source URL: {url}")
