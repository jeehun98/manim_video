import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import GradientBase
class Gradient11(GradientBase):
    INDEX=10
