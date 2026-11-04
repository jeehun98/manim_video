import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scene_engine import InverseScene
class Scene01(InverseScene):
    start_time=0
    end_time=9
