import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scene_engine import ReadingScene
class Scene04(ReadingScene):
    start_time=22
    end_time=26
