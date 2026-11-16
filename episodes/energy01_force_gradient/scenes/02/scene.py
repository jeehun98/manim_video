import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[4]))
from episodes.energy01_force_gradient.direction import EnergyForceGeometry
class Shot02(EnergyForceGeometry):
 shot=1
