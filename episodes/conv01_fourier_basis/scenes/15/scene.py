import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[4]))
from episodes.conv01_fourier_basis.direction import FourierConvolution
class Shot15(FourierConvolution):
 shot=14
