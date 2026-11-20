import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scene_engine import VolumeScene
class Scene06(VolumeScene):
    index=5
