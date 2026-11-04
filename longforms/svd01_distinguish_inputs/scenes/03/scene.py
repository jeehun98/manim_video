import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scene_engine import ExperimentScene
class Scene03(ExperimentScene):
    start_time=11
    end_time=19
