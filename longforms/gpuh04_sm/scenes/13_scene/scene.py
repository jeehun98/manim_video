import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from sm_visuals import SMBase
class SM13(SMBase):
    INDEX=12
