import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[4]))
from episodes.basis01_fourier_heat.direction import FourierScene

class Shot10(FourierScene):
    shot=9
