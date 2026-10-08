from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import EnergyScene

class Scene10(EnergyScene):
    index=10
