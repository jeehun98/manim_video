import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import AttentionBase
class Attention10(AttentionBase):
    INDEX=9
