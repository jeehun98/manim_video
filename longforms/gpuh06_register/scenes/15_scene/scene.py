import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from register_visuals import RegisterBase
class Register15(RegisterBase):
    INDEX=14
