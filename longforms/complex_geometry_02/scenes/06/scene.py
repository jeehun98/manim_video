import os,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[4]))
os.environ['QCS_LAYOUT']='longform'
from longforms.complex_geometry_02.direction import AnalysisScene
class Shot06(AnalysisScene):
    shot=5
