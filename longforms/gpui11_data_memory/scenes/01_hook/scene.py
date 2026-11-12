import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scene_engine import MemoryScene
class Scene01(MemoryScene):
    index=0
