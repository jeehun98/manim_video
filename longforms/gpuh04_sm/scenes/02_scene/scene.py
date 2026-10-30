import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from sm_visuals import SMBase
class SM02(SMBase):
    INDEX=1
