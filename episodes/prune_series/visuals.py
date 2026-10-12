"""Compatibility imports for scenes created before ``visual_library``."""

from visual_library.manim import (  # noqa: F401
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
    WeightMatrix,
    configure_vertical,
    pill,
    txt,
    weight_connection,
)

# Preserve the historical behavior of this episode-specific module.
configure_vertical()
