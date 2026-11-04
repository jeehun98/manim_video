import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scene_engine import DirectionScene
class Scene02(DirectionScene):
    start_time=9
    end_time=12
