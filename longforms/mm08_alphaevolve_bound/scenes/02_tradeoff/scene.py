import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import BoundScene
class Scene02(BoundScene):
    index=2
