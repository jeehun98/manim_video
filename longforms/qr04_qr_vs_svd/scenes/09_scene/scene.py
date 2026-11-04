import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import ComparisonBase
class QRShot(ComparisonBase):
    INDEX = 8
