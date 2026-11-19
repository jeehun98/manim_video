import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visuals import RuleScene,combo,VGroup,Indicate,Transform,MUTED,GREEN
class Shot06(RuleScene):
    index=6
    def shot_06(self):
        panels=VGroup(*[combo(p,x,y) for p,x,y in [((0,0),-3.4,1),((0,1),3.4,1),((1,0),-3.4,-1.3),((1,1),3.4,-1.3)]])
        panels.scale(.85).move_to([0,.25,0]);self.add(panels)
        self.act(.6,Indicate(panels[0],color=MUTED),Indicate(panels[3],color=MUTED))
        note=self.note('det(e₁,e₁) = det(e₂,e₂) = 0',MUTED);self.show(note,d=.4);self.to(72)
        self.act(.6,panels[0].animate.set_opacity(.12),panels[3].animate.set_opacity(.12))
        self.act(.5,Transform(note,self.note('같은 방향은 0 · 서로 다른 두 방향만 남는다',GREEN)));self.to(76)
