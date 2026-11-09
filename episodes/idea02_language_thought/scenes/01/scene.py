import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[4]))
from episodes.idea02_language_thought.direction import IdeaTwoScene

class Shot01(IdeaTwoScene):
    shot=0
