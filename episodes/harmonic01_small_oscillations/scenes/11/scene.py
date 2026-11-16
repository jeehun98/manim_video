import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[4]))
from episodes.harmonic01_small_oscillations.direction import HarmonicGeometry
class Shot11(HarmonicGeometry):
 shot=10
