import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[4]))
from episodes.godel01_proof_limits.direction import GodelScene

class Shot09(GodelScene):
    shot=8
