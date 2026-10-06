"""Reusable text constructors."""

from manim import NORMAL, Text

from .theme import FONT, INK


def text(value, size=28, color=INK, max_width=7.7, weight=NORMAL):
    """Create Korean-capable text and shrink it to ``max_width`` if needed."""

    obj = Text(
        str(value),
        font=FONT,
        font_size=size,
        color=color,
        weight=weight,
        line_spacing=1.18,
    )
    if obj.width > max_width:
        obj.scale_to_fit_width(max_width)
    return obj


# Compatibility with the established scene vocabulary.
txt = text

