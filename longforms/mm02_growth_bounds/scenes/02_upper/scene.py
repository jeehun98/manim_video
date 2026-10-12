import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import BoundsScene
class Scene02(BoundsScene):
    index=2
