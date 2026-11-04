import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import ReconstructionScene
class Reconstruction19(ReconstructionScene):
    INDEX=18
