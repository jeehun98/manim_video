"""Responsive Franck–Hertz documentary; each class is one replaceable claim."""
import json
from pathlib import Path
import numpy as np
from manim import *
from quantum_series.shared.theme import text,p,configure,INK,MUTED,GOLD,BG
from quantum_series.shared.franck_hertz import Tube,Levels
from quantum_series.episodes.ep05_franck_hertz.layouts import FranckHertzLayout
from quantum_series.episodes.ep05_franck_hertz.experiment_model import current_curve,MODEL,ElectronState
D=json.loads(Path(__file__).with_name('script.json').read_text(encoding='utf-8'))
L=FranckHertzLayout(configure().portrait)
CYAN='#43C5F4';HG='#D6A25B';RED='#F18A54';UV='#B28CFF';GREEN='#4DB6AC'
def wrap(s,n):
 lines=[];line=''
 for w in s.split():
  if len(line+' '+w)>n and line:lines.append(line);line=w
  else:line=(line+' '+w).strip()
 return '\n'.join(lines+[line])
class Plot(VGroup):
 def __init__(self,L):
  super().__init__();self.ax=Axes(x_range=[0,20,5],y_range=[0,1,.25],x_length=L.plot_width,y_length=L.plot_height,tips=False,axis_config={'color':MUTED,'stroke_width':1.5}).move_to(L.plot_center)
  self.add(self.ax)
  for u in [0,5,10,15,20]:self.add(text(str(u),*self.ax.c2p(u,0)[:2]+[0,-.23],size=16,color=MUTED))
  self.add(text('가속 전압 U (V)',*self.ax.c2p(10,0)[:2]+[0,-.63],size=20))
  self.add(text('검출 전류 · 상대값',*self.ax.c2p(10,1)[:2]+[0,.35],size=20))
  self.add(text('설명용 수송 모형 · 실측 자료 아님',*self.ax.c2p(10,0)[:2]+[0,-1.0],size=15,color=MUTED))
  self.data=current_curve()
 def curve(self,end=20):
  xs=np.linspace(0,max(end,.001),max(2,int(end*16)));ys=np.interp(xs,self.data['voltage'],self.data['current'])
  return VMobject(color=CYAN,stroke_width=3).set_points_as_corners([self.ax.c2p(x,y) for x,y in zip(xs,ys)])
class FH(Scene):
 offset=0
 def setup(self):
  self.L=L;self.caption=None;self.heading=None
  self.add(text('양자역학의 발견   /   1914 · 프랑크–헤르츠',0 if L.portrait else -3.7,L.brand_y,17,MUTED))
 def to(self,t):
  rem=t-self.offset-self.time
  if rem<-.018:raise RuntimeError(f'Overrun {self.offset+self.time} > {t}')
  frames=round(rem*30)
  if frames:self.wait((frames+1e-5)/30)
 def cue(self,i):
  s=D['sentences'][i];self.to(s['start'])
  if self.caption:self.remove(self.caption)
  self.caption=text(wrap(s['text'],26 if L.portrait else 62),y=L.caption_y,size=24 if L.portrait else 25,width=7.6 if L.portrait else 14.1);self.add(self.caption)
  h=text(s['heading'],y=L.heading_y,size=32,width=L.body_width)
  if self.heading:self.play(Transform(self.heading,h),run_time=.25)
  else:self.heading=h;self.play(FadeIn(h),run_time=.3)
 def note(self,s,color=MUTED):return text(s,y=-3.65 if L.portrait else -2.85,size=18,color=color,width=L.body_width)
 def tube(self):
  t=Tube(L);self.add(t);return t
 def travel(self,t,start=0,end=1.22,y=0,duration=1.3,color=CYAN):
  a=t.at(start,y);b=t.at(end,y) if end<=1 else t.collector(y)
  e=Dot(a,radius=.075,color=color);self.add(e);self.play(e.animate.move_to(b),run_time=duration,rate_func=linear);return e
 def graph(self,full=True):
  g=Plot(L);self.add(g)
  if full:self.add(g.curve())
  return g
 def energy(self,value,center=None):
  c=L.energy_center if center is None else center
  group=VGroup(Rectangle(width=2.7,height=.22,color=MUTED,stroke_width=1).move_to(c))
  bar=Rectangle(width=max(.01,2.7*value/6),height=.18,stroke_width=0,fill_color=CYAN,fill_opacity=1).move_to(c+p(-1.35+max(.01,2.7*value/6)/2,0))
  group.add(bar)
  group.add(text(f'K = {value:.1f} eV',c[0],c[1]-.38,23,CYAN))
  return group
class ApparatusDirection(FH):
 offset=0
 def construct(self):
  self.cue(0);t=self.tube();label=self.note('가속 전압 U → 운동에너지 증가 ΔK = eU',CYAN);self.add(label)
  e=self.travel(t,duration=1.4);self.to(3)
  self.cue(1);g=self.graph(False);expect=DashedVMobject(Line(g.ax.c2p(0,0),g.ax.c2p(19,.88),color=MUTED),num_dashes=20);self.play(Create(expect),run_time=1);self.add(text('예상',*g.ax.c2p(15,.8)[:2],size=20,color=MUTED));self.to(6)
  self.cue(2);self.remove(e);self.play(Indicate(t),run_time=1);self.to(12)
  self.cue(3)
  for y in [-.15,.15]:
   e=self.travel(t,y=y,duration=1.5);self.remove(e)
  self.to(17);self.cue(4);self.remove(label);signal=self.note('측정 대상: 검출부에 도달한 전자',CYAN);self.add(signal)
  for y in [-.15,0,.15]:
   e=self.travel(t,y=y,duration=1.1);self.play(Flash(t.collector(y),color=CYAN,flash_radius=.18),run_time=.25);self.remove(e)
  self.to(24)
class CurrentDirection(FH):
 offset=24
 def construct(self):
  self.cue(5);self.tube();g=self.graph(False);curve=g.curve(.01);self.add(curve)
  def grow(end,duration):self.play(Transform(curve,g.curve(end)),run_time=duration,rate_func=linear)
  grow(5.3,1.8);self.to(27);self.cue(6);grow(6.6,2.2);self.to(31);self.cue(7);grow(12.2,3.1);self.to(36);self.cue(8);grow(19.5,1.2)
  mins=g.data['voltage'][g.data['minima_indices']]
  for a,b in zip(mins[:-1],mins[1:]):
   y=.88;self.add(DoubleArrow(g.ax.c2p(a,y),g.ax.c2p(b,y),buff=0,color=GOLD,stroke_width=2),text('≈4.9 V',*g.ax.c2p((a+b)/2,y)[:2]+[0,.23],size=18,color=GOLD))
  self.add(self.note('첫 감소의 절대 전압은 접촉 전위 등에 따라 달라짐'))
  self.to(40);self.cue(9);self.play(Indicate(curve,color=GOLD),run_time=.8);self.to(42)
class CollisionDirection(FH):
 offset=42
 def construct(self):
  self.cue(10);self.tube();c=L.atom_center;atom=Circle(radius=.48,color=HG,fill_color=HG,fill_opacity=.18).move_to(c);label=text('Hg',c[0],c[1],26,HG);lv=Levels(L.level_center);self.add(atom,label,lv,self.note('실험 원리의 현대적 해석 · 원자 위치와 내부 상태는 구분'))
  self.to(45);self.cue(11);bar=self.energy(3);self.add(bar);e=Dot(c+p(-1.35,0),radius=.08,color=CYAN);self.add(e);self.play(e.animate.move_to(c+p(-.5,0)),run_time=1);self.play(e.animate.move_to(c+p(-1.1,.3)),run_time=1.2);ground_note=text('내부 들뜸 없음',c[0],c[1]+.95,21,MUTED);self.add(ground_note);self.to(52)
  self.cue(12);self.play(Transform(bar,self.energy(4.9)),run_time=1.3);self.play(Indicate(lv,color=GOLD),run_time=.8);self.to(57)
  self.cue(13);self.remove(e,ground_note);e=Dot(c+p(-1.4,0),radius=.08,color=CYAN);self.add(e);self.play(Transform(bar,self.energy(5.2)),run_time=.5);self.play(e.animate.move_to(c+p(-.48,0)),run_time=.7)
  self.play(lv.marker.animate.move_to(lv.high),atom.animate.set_stroke(GOLD,width=4),Transform(bar,self.energy(.3)),run_time=1.3)
  self.play(e.animate.move_to(c+p(.65,0)),run_time=1.5,rate_func=linear);self.to(64)
  self.cue(14);self.play(e.animate.shift(RIGHT*.45),run_time=1.4,rate_func=linear);self.add(text('5.2 − 4.9 = 0.3 eV',c[0],c[1]-2.45,22,CYAN,width=3.3));self.to(67)
class CollectionDirection(FH):
 offset=67
 def construct(self):
  self.cue(15);t=self.tube();g=self.graph();self.add(self.note('감속 전위차 · 실제 벽이 아님',RED));arrow=Arrow(t.collector()+p(-.1,-.3),t.at(1)+p(.05,-.3),buff=0,color=RED);self.add(arrow);self.to(73)
  self.cue(16);collision_atom=Circle(radius=.14,color=HG).move_to(t.at(.96));self.add(collision_atom);e=Dot(t.at(.96),radius=.085,color=CYAN);self.add(e)
  self.play(Flash(t.at(.96),color=GOLD,flash_radius=.2),run_time=.4);self.play(e.animate.move_to(t.at(1)),run_time=.6)
  state=ElectronState().accelerate(.96,6.6125);state,_=state.collide();state=state.accelerate(1,6.6125);turn_state,_=state.enter_retarding_region(1.22);turn=t.at(turn_state.x);self.play(e.animate.move_to(turn),run_time=1.1,rate_func=rate_functions.ease_out_sine);self.play(e.animate.move_to(t.at(.94)),run_time=1.1,rate_func=rate_functions.ease_in_sine);self.remove(e)
  e=self.travel(t,y=.3,duration=1.2);self.play(Flash(t.collector(.3),color=CYAN,flash_radius=.16),run_time=.3);self.remove(e);self.to(80)
  self.cue(17);e=Dot(t.at(0,-.15),radius=.08,color=CYAN);self.add(e)
  for x in [.49,.97]:
   self.add(Circle(radius=.14,color=HG).move_to(t.at(x,-.15)))
   self.play(e.animate.move_to(t.at(x,-.15)),run_time=.9,rate_func=linear);self.play(Flash(t.at(x,-.15),color=GOLD,flash_radius=.2),run_time=.3)
  self.play(e.animate.move_to(t.at(1,-.15)),run_time=.5);self.play(e.animate.move_to(t.at(1,-.15)+p(.65,0)),run_time=.8);self.play(e.animate.shift(LEFT*.3),run_time=.5);self.remove(e)
  self.add(text('격자 이전: 재가속과 여러 번의 들뜸 충돌',*(L.tube_center[:2]+[0,-1.85]),size=20,color=GOLD,width=6.4));self.to(87)
  self.cue(18);self.play(Indicate(g,color=GOLD),run_time=1.1);self.to(91)
class LevelsDirection(FH):
 offset=91
 def construct(self):
  self.cue(19);xs=L.pair_columns;y=.65 if L.portrait else .35
  lv=Levels(p(xs[1],y),2.65);self.add(lv,text('수은 원자의 내부 에너지',xs[1],y+1.8,23,HG,width=3.3))
  values=VGroup(text('전압의 간격',xs[0],y+1.5,24),text('ΔU ≈ 4.9 V',xs[0],y+.85,28,CYAN),text('ΔK = eΔU',xs[0],y,26,MUTED),text('ΔE ≈ 4.9 eV',xs[0],y-.85,27,GOLD))
  self.add(values,self.note('특정한 내부 상태 전이의 에너지 · 모든 충돌 에너지 교환이 같은 것은 아님'))
  self.play(lv.marker.animate.move_to(lv.high),run_time=1.5);self.to(101)
  self.cue(20);self.play(FadeOut(values),run_time=.4)
  h=VGroup(text('수소 · 보어 모형',xs[0],y+1.8,24,CYAN,width=3.3))
  for yy,label in [(-.8,'n=1'),(.3,'n=2'),(.75,'n=3')]:h.add(Line(p(xs[0]-1.2,y+yy),p(xs[0]+1.2,y+yy),color=CYAN),text(label,xs[0]-1.5,y+yy,17,CYAN))
  self.add(h);self.to(105)
class EmissionDirection(FH):
 offset=105
 def construct(self):
  self.cue(21);xs=L.pair_columns;y=.5 if L.portrait else .3
  left=Levels(p(xs[0],y),2.5);right=Levels(p(xs[1],y),2.5);right.marker.move_to(right.high)
  self.add(left,right,text('에너지 흡수',xs[0],y+1.75,26,CYAN),text('빛 방출',xs[1],y+1.75,26,UV))
  self.play(right.marker.animate.move_to(right.low),run_time=1.2)
  wave=ParametricFunction(lambda t:p(xs[1]+t,y-1.45+.15*np.sin(12*t)),t_range=[-1.25,1.25],color=UV)
  self.play(Create(wave),run_time=1.1);self.add(text('자외선 UV · 253.7 nm',xs[1],y-2.0,21,UV,width=3.5),self.note('빛의 색은 식별용 · 253.7 nm는 가시광선이 아님',UV));self.to(113)
  self.cue(22);self.play(left.marker.animate.move_to(left.high),run_time=1.2);self.add(text('같은 내부 에너지 차이  ΔE ≈ 4.9 eV',y=3.25 if L.portrait else -2.1,size=26,color=GOLD,width=L.body_width));self.to(119)
  self.cue(23);self.play(Indicate(VGroup(left,right),color=GOLD),run_time=.8);self.to(121);self.to(122)
