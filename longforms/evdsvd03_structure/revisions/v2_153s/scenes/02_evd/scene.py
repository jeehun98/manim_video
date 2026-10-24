import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import GraphStructure
class GraphEVD(GraphStructure):
    INDEX=1
