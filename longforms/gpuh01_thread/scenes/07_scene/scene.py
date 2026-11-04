import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import ThreadBase
class Thread07(ThreadBase):
    INDEX=6
