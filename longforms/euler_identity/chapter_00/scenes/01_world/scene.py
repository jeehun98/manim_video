import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import IntroScene
class Shot01(IntroScene):
    index=1
