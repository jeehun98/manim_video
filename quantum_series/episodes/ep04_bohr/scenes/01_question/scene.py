import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from quantum_series.episodes.ep04_bohr.direction import ChargeQuestionDirection

class ChargeQuestion(ChargeQuestionDirection):
    pass
