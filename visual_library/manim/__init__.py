"""Public Manim object library.

Importing this module has no resolution or global Manim configuration side
effects. Call ``configure_vertical()`` explicitly in new standalone scenes.
"""

from .primitives import Pill, WeightMatrix, pill, weight_connection
from .theme import (
    ACCENT,
    BG,
    FONT,
    GOOD,
    INK,
    MUTED,
    PRUNE,
    SPARSE,
    WEIGHT,
    ZERO,
    configure_vertical,
)
from .typography import text, txt

__all__ = [
    "ACCENT",
    "BG",
    "FONT",
    "GOOD",
    "INK",
    "MUTED",
    "PRUNE",
    "SPARSE",
    "WEIGHT",
    "ZERO",
    "Pill",
    "WeightMatrix",
    "configure_vertical",
    "pill",
    "text",
    "txt",
    "weight_connection",
]

