import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[4]))
from episodes.lagrange01_constraint_value.direction import LagrangeScene

class Shot01(LagrangeScene):
    shot=0
