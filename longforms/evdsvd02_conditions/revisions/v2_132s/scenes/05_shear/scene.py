import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import RevisedConditions
class RevisionShear(RevisedConditions):
    INDEX=4
