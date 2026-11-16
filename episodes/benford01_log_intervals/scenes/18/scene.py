import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[4]))
from episodes.benford01_log_intervals.direction import BenfordGeometry
class Shot18(BenfordGeometry):
 shot=17
