"""Nonlinear chiral amplification and asymmetric autocatalysis."""
import json,sys
from pathlib import Path
import numpy as np
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.science02_gravitational_lensing.scene import txt,LIGHT,OBS,MASS,GAS
from episodes.science08_density_growth.scene import DensityGrowthDiscovery
R='#FF7B72';S='#6EDDF2';GOOD='#75E6A4';GOLD='#FFD166';DIM='#40536C';PURPLE='#A18CFF'

def hand(center=ORIGIN,left=True,color=R):
 c=np.array(center,float);p=RoundedRectangle(width=1.25,height=1.65,corner_radius=.3,color=color,fill_color=color,fill_opacity=.16).move_to(c+[0,-.35,0]);f=VGroup()
 xs=(-.48,-.16,.16,.48) if left else (.48,.16,-.16,-.48)
 for i,x in enumerate(xs):f.add(RoundedRectangle(width=.23,height=1.1+.16*i,corner_radius=.12,color=color,fill_color=color,fill_opacity=.16).move_to(c+[x,.85+.08*i,0]))
 thumb=RoundedRectangle(width=.28,height=.95,corner_radius=.12,color=color,fill_color=color,fill_opacity=.16).rotate(-.75 if left else .75).move_to(c+([- .82,.05,0] if left else [.82,.05,0]))
 return VGroup(p,f,thumb)
def molecule(center=ORIGIN,mirror=False,scale=1):
 c=np.array(center,float);sgn=-1 if mirror else 1;g=VGroup(Dot(c,radius=.15,color=GOLD))
 pts=[c+[sgn*1,0,0],c+[0,.95,0],c+[-sgn*.72,-.72,0],c+[sgn*.35,-1.05,0]];cols=[R,S,GOOD,PURPLE]
 for p,col in zip(pts,cols):g.add(Line(c,p,color=col,stroke_width=5),Dot(p,radius=.18,color=col))
 return g.scale(scale)
def bars(r,s,y=.2):
 return VGroup(Rectangle(width=2,height=4*r/100,fill_color=R,fill_opacity=.75,stroke_width=0).align_to([ -1.3,y-2,0],DOWN).move_to([-1.3,y-2+2*r/100,0]),Rectangle(width=2,height=4*s/100,fill_color=S,fill_opacity=.75,stroke_width=0).align_to([1.3,y-2,0],DOWN).move_to([1.3,y-2+2*s/100,0]))
def ratio(r,s,y=-3):return VGroup(txt(f'R  {r:g}',y,30,R).shift(LEFT*1.7),txt(':',y,30,LIGHT),txt(f'{s:g}  S',y,30,S).shift(RIGHT*1.7))
def axes_graph(curved=False):
 a=Axes(x_range=[0,1,.25],y_range=[0,1,.25],x_length=5.7,y_length=4.3,axis_config={'include_ticks':False,'color':GAS}).move_to([0,.35,0]);f=(lambda x:x) if not curved else (lambda x:1-(1-x)**3)
 return a,a.plot(f,x_range=[0,1],color=R if curved else S,stroke_width=5)
def hill():return ParametricFunction(lambda x:np.array([x,.35+1.2*np.exp(-x*x/1.4)-.18*x*x,0]),t_range=[-3.5,3.5],color=PURPLE,stroke_width=5)

class ChiralAmplificationDiscovery(DensityGrowthDiscovery):
 TIMING=json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'));DURATION=TIMING['duration']
 def construct(self):
  self.brand=txt('과학의 한 장면  /  Nobel Chemistry 01',7.1,21,'#9BA9C3');self.add(self.brand)
  self.cue('거울상인데, 겹칠 수 없는 두 손','같아 보이지만 회전만으로는\n완전히 포개지지 않습니다.');l=hand([-1.8,.4,0],True,R);r=hand([1.8,.4,0],False,S);self.beat(.25,FadeIn(l));self.beat(.3,TransformFromCopy(l,r));self.beat(.2,r.animate.move_to([-1.5,.4,0]).rotate(.4));self.add(txt('LEFT',-2.6,27,R),txt('RIGHT',-3.25,27,S));self.finish()
  self.cue('분자에도, 왼손과 오른손이 있다','연결은 같지만 공간 배열이 다른\n겹칠 수 없는 거울상 분자입니다.');a=molecule([-1.9,.6,0]);b=molecule([1.9,.6,0],True);self.beat(.3,FadeIn(a),FadeIn(b));self.add(DashedLine([0,-1.3,0],[0,3,0],color=GAS),txt('R',-2.25,42,R).shift(LEFT*1.9),txt('S',-2.25,42,S).shift(RIGHT*1.9),txt('CHIRAL MOLECULES',-3.4,31,LIGHT));self.finish()
  self.cue('비슷한 성질, 다른 생체 작용','키랄한 수용체에서는 두 거울상이\n서로 다르게 맞을 수 있습니다.');self.add(molecule([-2.4,1.5,0],False,.65),molecule([2.4,1.5,0],True,.65));checks=VGroup(*[txt(x,1.1-i*.65,24,GOOD) for i,x in enumerate(('✓ same mass','✓ same bonds','✓ same atoms'))]);self.add(checks);lock=Arc(radius=1.1,start_angle=.25,angle=PI*1.5,color=GOLD,stroke_width=12).move_to([0,-2.1,0]);self.beat(.25,Create(lock));self.add(txt('BIOLOGY IS CHIRAL',-3.7,28,GOLD));self.finish()
  self.cue('생명은, 거의 한쪽 손만 사용한다','단백질의 아미노산은\n거의 한쪽 손성으로 정렬됩니다.');chain=VGroup(*[molecule([-3+i*1.0,.5,0],False,.32) for i in range(7)]);self.beat(.4,LaggedStart(*[FadeIn(x) for x in chain],lag_ratio=.08));self.add(txt('L   L   L   L   L   L   L',-1.8,30,R),txt('HOMOCHIRALITY',-3.2,36,GOLD));self.finish()
  self.cue('대칭적인 반응은, 보통 50 대 50','키랄한 원인이 없다면\n두 거울상은 같은 확률로 생깁니다.');self.add(txt('A  +  B',1.8,45,LIGHT),Arrow([-1,1.1,0],[1,1.1,0],color=GAS),molecule([-1.8,-1,0],False,.48),molecule([1.8,-1,0],True,.48),ratio(50,50,-3.15));self.finish()
  self.cue('아주 작은 차이는, 그대로 남을까?','R 하나가 조금 많다면 결과도\n조금만 기울 것처럼 보입니다.');self.add(bars(51,49,.8),ratio(51,49,-2.3),txt('51 : 49   →   51 : 49',-3.55,35,LIGHT));self.finish()
  self.cue('선형 예상: 입력만큼 출력도 기울어진다','촉매 비대칭과 생성물 비대칭이\n정비례한다고 예상했습니다.');a,g=axes_graph(False);self.add(a,txt('catalyst asymmetry',-2.25,22,GAS),txt('product\nasymmetry',1.5,20,GAS).shift(LEFT*3.25));self.beat(.45,Create(g));self.add(txt('LINEAR',-3.3,32,S));self.finish()
  self.cue('Kagan이 발견한, 휘어진 관계','작은 촉매 비대칭이 생성물에서\n훨씬 큰 차이가 될 수 있습니다.');a,line=axes_graph(False);_,curve=axes_graph(True);self.add(a,line.set_opacity(.3));self.beat(.5,Create(curve));self.add(txt('small asymmetry  →  LARGE EFFECT',-3.35,29,R),txt('HENRI B. KAGAN · 1986',-4.15,24,GOLD));self.finish()
  self.cue('작은 차이는, 화학반응에서 증폭될 수 있다','51:49가 반드시 그대로\n끝날 필요는 없습니다.');vals=[(51,49),(60,40),(75,25)];b=bars(*vals[0],.8);lab=ratio(*vals[0],-2.4);self.add(b,lab)
  for v in vals[1:]:
   self.beat(.2,Transform(b,bars(*v,.8)),Transform(lab,ratio(*v,-2.4)))
  self.add(txt('ASYMMETRIC AMPLIFICATION',-3.6,29,GOLD));self.finish()
  self.cue('생성물이, 자기 자신을 만드는 촉매가 된다','결과가 다시 반응을 촉진하는\n비대칭 자기촉매작용입니다.');self.add(txt('A + B',1.5,42,LIGHT),Arrow([-1,1.5,0],[1,1.5,0],color=GAS),molecule([2.4,1.5,0],False,.5));loop=CurvedArrow([2.5,.7,0],[.3,1.2,0],angle=-1.5,color=R);self.beat(.35,Create(loop));self.add(txt('R',.55,34,R),txt('A + B   ⟶   R + R',-1.3,38,R),txt('AUTOCATALYSIS',-3,34,GOLD));self.finish()
  self.cue('R은 R을, S는 S를 더 만든다','같은 손성의 생성을 돕는\n결과-원인 피드백입니다.');self.add(molecule([-2.4,1,0],False,.45),txt('R  →  R + R',-1,36,R).shift(LEFT*1.8),molecule([2.4,1,0],True,.45),txt('S  →  S + S',-1,36,S).shift(RIGHT*1.8),txt('RESULT  →  CAUSE',-3.2,32,GOLD));self.finish()
  self.cue('필요한 시작은, 극도로 작은 우연','분자 몇 개의 불균형도\n피드백의 씨앗이 됩니다.');self.add(bars(50.000025,49.999975,.8),txt('50.000025 : 49.999975',-2.4,37,LIGHT),SurroundingRectangle(txt('0.00005% ee',-3.55,35,GOLD),color=GOLD),txt('0.00005% ee',-3.55,35,GOLD));self.finish()
  self.cue('우세가 촉매를 만들고, 촉매가 우세를 키운다','차이가 더 큰 차이를 만드는\n양의 피드백입니다.');items=VGroup(txt('R ↑',1.8,40,R),txt('R production ↑',0,34,LIGHT),txt('R catalyst ↑',-1.8,34,GOLD)).arrange(DOWN,buff=.8);self.add(items)
  arrows=VGroup(Arrow([2.75,1.4,0],[2.75,.45,0],buff=0,color=R,stroke_width=4),Arrow([2.75,-.35,0],[2.75,-1.3,0],buff=0,color=R,stroke_width=4),CurvedArrow([-2.55,-1.5,0],[-2.55,1.5,0],angle=-PI/1.45,color=R,stroke_width=4))
  self.beat(.4,LaggedStart(*[Create(a) for a in arrows],lag_ratio=.12));self.finish()
  self.cue('50 대 50이, 세 주기 뒤 거의 100 대 0','0.00005% ee가 세 번의 증폭으로\n99.5%보다 크게 커졌습니다.');seq=[('START',50.000025),('CYCLE 1',55),('CYCLE 2',80),('CYCLE 3',99.5)];g=VGroup();bar_left=-1.45;bar_width=4.7
  for i,(lab,v) in enumerate(seq):
   y=2.45-i*1.25
   track=Rectangle(width=bar_width,height=.5,color=DIM,stroke_width=2).move_to([.9,y,0])
   fill=Rectangle(width=bar_width*v/100,height=.5,fill_color=R,fill_opacity=.8,stroke_width=0).move_to([bar_left+bar_width*v/200,y,0])
   label=txt(lab,y-.12,20,LIGHT).move_to([-2.55,y,0])
   g.add(VGroup(label,track,fill))
  self.beat(.5,LaggedStart(*[FadeIn(x) for x in g],lag_ratio=.08));self.add(txt('0.00005% ee  →  > 99.5% ee',-3.15,34,R));self.finish()
  self.cue('처음에는, R과 S가 완벽히 대칭이다','중앙의 대칭 상태에는\n어느 쪽도 선택할 이유가 없습니다.');h=hill();ball=Dot([0,1.55,0],radius=.14,color=GOLD);self.add(h,ball,txt('R',-2.4,40,R).shift(LEFT*2.2),txt('S',-2.4,40,S).shift(RIGHT*2.2),txt('UNSTABLE SYMMETRY',-3.5,29,LIGHT));self.finish()
  self.cue('작은 흔들림이, 내려갈 방향을 정한다','미세한 우연을 자기촉매가\n한쪽 선택으로 확대합니다.');h=hill();ball=Dot([0,1.55,0],radius=.14,color=GOLD);self.add(h,ball);path=ParametricFunction(lambda t:np.array([-3*t,.35+1.2*np.exp(-9*t*t/1.4)-.18*9*t*t,0]),t_range=[0,1]);self.beat(.65,MoveAlongPath(ball,path),rate_func=rush_into);self.add(txt('TINY FLUCTUATION  →  CHOICE',-3.5,29,GOLD));self.finish()
  self.cue('대칭적인 법칙에서, 비대칭 결과가 나타난다','조건은 R과 S를 같게 취급하지만\n결과는 한쪽으로 치우칩니다.');self.add(txt('R = S',1.6,48,LIGHT),Arrow([-1,0,0],[1,0,0],color=GOLD),txt('R ≫ S',-1.6,54,R),txt('SYMMETRY BREAKING',-3.45,35,PURPLE));self.finish()
  self.cue('생명의 homochirality를 설명하는 모델','역사적 원인을 확정한 것이 아니라\n가능한 증폭 경로를 실험으로 보였습니다.');self.add(txt('tiny imbalance',2.2,30,S),Arrow([0,1.55,0],[0,.65,0],color=GAS),txt('amplification',0,31,GOLD),Arrow([0,-.65,0],[0,-1.55,0],color=GAS),txt('homochirality ?',-2.2,34,R),txt('MODEL, NOT THE FULL HISTORY',-3.55,25,LIGHT));self.finish()
  self.cue('비선형 효과와 자기촉매가, 하나로 연결된다','Kagan의 증폭과 Soai의 피드백이\n비대칭 선택의 화학을 열었습니다.');left=VGroup(txt('HENRI B. KAGAN',2.2,28,GOLD).shift(LEFT*2),txt('NON-LINEAR EFFECT',1.4,24,R).shift(LEFT*2));right=VGroup(txt('KENSO SOAI',2.2,28,GOLD).shift(RIGHT*2),txt('ASYMMETRIC AUTOCATALYSIS',1.4,21,S).shift(RIGHT*2));self.add(left,right);self.beat(.35,GrowArrow(Arrow([-2,.5,0],[0,-.5,0],color=R)),GrowArrow(Arrow([2,.5,0],[0,-.5,0],color=S)));self.add(txt('ASYMMETRIC AMPLIFICATION',-2,34,LIGHT));self.finish()
  self.cue('화학은, 어떻게 한쪽 손을 선택하는가','작은 차이와 자기촉매가\n거울 대칭을 깨뜨립니다.');l=hand([-1.2,1.5,0],True,R);r=hand([1.2,1.5,0],False,S);self.add(l,r);self.beat(.35,l.animate.scale(1.35),r.animate.scale(.55).set_opacity(.25));self.add(molecule([0,-1.25,0],False,.7),txt('HOW CHEMISTRY CHOOSES A HANDEDNESS',-3,29,GOLD),txt('2026 NOBEL PRIZE IN CHEMISTRY',-3.8,27,LIGHT),txt('HENRI B. KAGAN  ·  KENSO SOAI',-4.45,22,R));self.finish()
