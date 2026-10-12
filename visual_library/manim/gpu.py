"""Stable public imports for the existing GPU component collection.

The implementations remain in ``gpu_series`` for compatibility. New scenes
should import them from this module so they can move later without churn.
"""

from gpu_series.components import (
    DataArrow,
    DataCell,
    GPUBlock,
    GPUGrid,
    MemoryBox,
    ThreadGroup,
    ThreadMarker,
    data_row,
)

__all__ = [
    "DataArrow",
    "DataCell",
    "GPUBlock",
    "GPUGrid",
    "MemoryBox",
    "ThreadGroup",
    "ThreadMarker",
    "data_row",
]

