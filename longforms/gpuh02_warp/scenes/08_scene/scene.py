import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from warp_visuals import WarpBase
class Warp08(WarpBase):
    INDEX=7
