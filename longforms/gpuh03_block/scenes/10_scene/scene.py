import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from block_visuals import BlockBase
class Block10(BlockBase):
    INDEX=9
