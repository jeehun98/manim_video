import sys,os
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[4]))
os.environ['QCS_LAYOUT']='longform'
from longforms.complex_geometry_01.direction import GeometryScene
class Shot02(GeometryScene):
    shot=1
