import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[4]))
from episodes.qtier01_experiments.direction import TierScene

class Shot01(TierScene):
    shot=0
