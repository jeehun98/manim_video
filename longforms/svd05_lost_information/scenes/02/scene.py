import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scene_engine import LossScene
class Scene02(LossScene):
    start_time=11
    end_time=17
