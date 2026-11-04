import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from shared_visuals import SharedBase
class Shared16(SharedBase):
    INDEX=15
