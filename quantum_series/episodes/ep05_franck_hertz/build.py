import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from quantum_series.shared.build import main
if __name__=="__main__":main(Path(__file__).parent)
