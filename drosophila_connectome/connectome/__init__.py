"""Connectome data tooling; no neural runtime is included here."""
"""Connectome data models and data-loading utilities."""

from .synthetic import SyntheticConnectome, load_synthetic_connectome

__all__ = ["SyntheticConnectome", "load_synthetic_connectome"]
