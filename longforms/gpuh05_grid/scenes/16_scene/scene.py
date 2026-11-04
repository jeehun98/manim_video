import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from grid_visuals import GridBase
class Grid16(GridBase):
    INDEX=15
