import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scene_engine import ReadingScene
class Scene02(ReadingScene):
    start_time=7
    end_time=13
