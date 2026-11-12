import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[4]))
from episodes.legendre01_tangent_duality.direction import LegendreScene

class Shot07(LegendreScene):
    shot=6
