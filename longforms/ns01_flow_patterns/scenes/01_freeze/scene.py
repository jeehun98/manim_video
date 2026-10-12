from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import FlowScene

class Scene01(FlowScene):
    index = 1
