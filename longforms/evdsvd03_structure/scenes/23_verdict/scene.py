import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import StructureScene
class StructureVerdict(StructureScene):
    INDEX=22
