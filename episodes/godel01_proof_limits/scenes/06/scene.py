import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[4]))
from episodes.godel01_proof_limits.direction import GodelScene

class Shot06(GodelScene):
    shot=5
