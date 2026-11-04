"""Manim entry points; each scene can be replaced and rerendered independently."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from quantum_series.episodes.ep01_planck.direction import (
    ThermalDirection, SpectrumDirection, EnergyDirection, InterpretationDirection)

class ThermalChapter(ThermalDirection):
    pass

class SpectrumChapter(SpectrumDirection):
    pass

class EnergyChapter(EnergyDirection):
    pass

class InterpretationChapter(InterpretationDirection):
    pass
