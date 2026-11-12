import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[4]))
from longforms.qcs01_speed.direction import QCSScene

class Shot03(QCSScene):
    shot=2
