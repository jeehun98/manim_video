import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scene_engine import InverseScene
class Scene08(InverseScene):
    start_time=60
    end_time=70
