import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import RuleScene,Matrix,PURPLE
class Shot11(RuleScene):
    index=11
    def add(self,*objects):
        for obj in objects:
            if isinstance(obj,Matrix) and len(obj.get_columns())==3:
                obj.get_columns()[2].set_color(PURPLE)
        return super().add(*objects)
