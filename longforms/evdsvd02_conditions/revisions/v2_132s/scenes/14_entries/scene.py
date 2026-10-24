import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import RevisedConditions
class RevisionEntries(RevisedConditions):
    INDEX=13
