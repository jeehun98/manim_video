import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scene_engine import InverseScene
class Scene03(InverseScene):
    start_time=16
    end_time=26
