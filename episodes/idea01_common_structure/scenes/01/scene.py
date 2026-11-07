import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[4]))
from episodes.idea01_common_structure.direction import IdeaScene

class Shot01(IdeaScene):
    shot=0
