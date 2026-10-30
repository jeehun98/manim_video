import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import AttentionBase
class Attention09(AttentionBase):
    INDEX=8
