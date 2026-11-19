import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import RuleScene,tx
class Shot10(RuleScene):
    index=10
    def show(self,*objects,d=.5):
        for obj in objects:
            if '기준순서'==getattr(obj,'text','').replace(' ',''):
                # A neutral label stays true after the animated swaps as well.
                obj.become(tx('순서와 부호',-4.9,.8,25,w=2.4))
        return super().show(*objects,d=d)
