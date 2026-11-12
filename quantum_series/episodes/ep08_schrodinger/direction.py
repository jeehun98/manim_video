"""Boundary conditions, hydrogen eigenstates and the question of wavefunction meaning."""
import json
from pathlib import Path
import numpy as np
from manim import *
from quantum_series.shared.theme import text,p,configure,INK,MUTED,GOLD
from quantum_series.shared.matter_waves import BohrAtom,abstract_state,matter_wave,ELECTRON
from quantum_series.shared.wave_mechanics import *
from quantum_series.episodes.ep08_schrodinger.layouts import WaveLayout
from quantum_series.episodes.ep08_schrodinger.physics_model import solve_radial,AtomicState,standing
D=json.loads(Path(__file__).with_name('script.json').read_text(encoding='utf-8'));L=WaveLayout(configure().portrait)
def wrap(s,n):
 lines=[];line=''
 for word in s.split():
  if line and len(line+' '+word)>n:lines.append(line);line=word
  else:line=(line+' '+word).strip()
 return '\n'.join(lines+[line])
class WaveScene(Scene):
 offset=0
 def setup(self):
  self.caption=None;self.heading=None;self.foot=None;self.body=Group()
  self.add(text('양자역학의 발견   /   1926 · 슈뢰딩거',0 if L.portrait else -3.7,L.brand_y,17,MUTED))
 def to(self,t):
  remain=t-self.offset-self.time
  if remain<-.018:raise RuntimeError(f'Timing overrun {self.offset+self.time} > {t}')
  frames=round(remain*30)
  if frames:self.wait((frames+1e-5)/30)
 def cue(self,i):
  s=D['sentences'][i];self.to(s['start'])
  if self.caption:self.remove(self.caption)
  self.caption=text(wrap(s['text'],26 if L.portrait else 62),y=L.caption_y,size=24 if L.portrait else 25,width=7.6 if L.portrait else 14.1);self.add(self.caption)
  h=text(s['heading'],y=L.heading_y,size=32,width=L.body_width)
  if self.heading:self.play(Transform(self.heading,h),run_time=.25)
  else:self.heading=h;self.play(FadeIn(h),run_time=.3)
 def put(self,*objects):self.body.add(*objects);self.add(*objects)
 def clear(self):
  if len(self.body):self.play(FadeOut(self.body),run_time=.35)
  self.body=Group()
 def note(self,s,color=MUTED):
  if self.foot:self.remove(self.foot)
  self.foot=text(s,y=-3.95 if L.portrait else -2.85,size=18,color=color,width=L.body_width);self.add(self.foot)
 def title(self,s,y=0,size=32,color=INK):return text(s,y=y,size=size,color=color,width=L.body_width)
 def field_note(self):self.note('색: ψ의 부호 · 밝기: 상대 |ψ| · 확률밀도 그림이 아님')
 def oscillate(self,curves,centers,modes,duration=1.8,mixed=False,width=6.4,amplitude=.55):
  self.play(*[UpdateFromAlphaFunc(curve,lambda obj,a,c=center,n=mode:obj.become(string_curve(c,n,a*TAU,width,amplitude,mixed))) for curve,center,mode in zip(curves,centers,modes)],run_time=duration,rate_func=linear)
class QuestionDirection(WaveScene):
 offset=0
 def construct(self):
  self.cue(0);wave=abstract_state(L.center);self.put(wave,self.title('Erwin Schrödinger',y=-1.8,size=31,color=GOLD));self.play(Create(wave),run_time=1);self.to(5)
  self.cue(1);self.clear();wave=matter_wave(L.center,3,6.3);electron=Dot(L.center+p(-2.4,0),color=ELECTRON,radius=.1);self.put(electron);self.play(electron.animate.shift(RIGHT*2),run_time=.8);self.play(FadeOut(electron),Create(wave),run_time=.8);self.body.remove(electron);self.put(wave);self.note('물질파는 전자의 구불구불한 이동 궤적이 아님');self.to(10)
  self.cue(2);formula=self.title('λ = h/p',y=-1.4,size=42,color=GOLD);self.put(formula,Dot(L.center,color=NUCLEUS,radius=.09));self.play(Indicate(formula),run_time=.8);self.to(16)
  self.cue(3);self.clear();c=L.center;self.put(Dot(c,color=NUCLEUS,radius=.11),text('+',*c[:2],size=20));arrows=VGroup()
  for angle,r in [(0,1.3),(PI*.7,2.2),(PI*1.4,2.8)]:
   unit=p(np.cos(angle),np.sin(angle));start=c+r*unit;length=.95*(1.3/r)**2
   arrows.add(Arrow(start,start-length*unit,buff=0,color=ORANGE),Dot(start,radius=.05,color=ELECTRON))
  self.put(arrows,self.title('거리와 함께 달라지는 전기적 인력',y=-2.2,size=28,color=ORANGE));self.note('전기적 인력의 방향과 상대 크기 · 파동을 유체처럼 당기는 그림이 아님');self.to(23)
  self.cue(4);self.play(FadeOut(arrows),run_time=.4);self.body.remove(arrows);self.put(abstract_state(c).set_opacity(.5));self.to(26)
class StringDirection(WaveScene):
 offset=26
 def construct(self):
  self.cue(5);c=L.center;fixed=fixed_string(c);self.put(fixed);self.note('줄의 양끝 변위 = 0');self.to(29)
  self.cue(6);curve=string_curve(c,mixed=True);self.put(curve);self.oscillate([curve],[c],[1],1.6,mixed=True);self.note('일반적인 진동은 여러 정상모드의 합일 수도 있음');self.to(32)
  self.cue(7);self.play(Transform(curve,string_curve(c,1.5)),run_time=.8);bad=Dot(c+p(3.2,-.55),radius=.09,color=ORANGE);badlabel=self.title('시험 파형 · 오른쪽 끝이 고정 조건과 불일치',y=-1.7,size=27,color=ORANGE);self.put(bad,badlabel);self.play(Indicate(bad),run_time=.7);self.play(Transform(curve,string_curve(c,2)),FadeOut(bad),run_time=.8);self.body.remove(bad);self.play(Transform(badlabel,self.title('정수 모드 · 양끝 고정 조건 만족',y=-1.7,size=27,color=GREEN)),run_time=.5);self.note('제한되는 것은 개별 정상모드 · 임의의 순간 모양 전체가 아님');self.to(41)
  self.cue(8);self.clear();centers=[p(0,y) for y in L.row_y];curves=[]
  for mode,center in enumerate(centers,1):
   curve=string_curve(center,mode,width=6.1,amplitude=.38);curves.append(curve);self.put(fixed_string(center,6.1),curve,text(f'n={mode}',-3.5,center[1]+.65,23,GREEN))
  self.to(45);self.cue(9);self.oscillate(curves,centers,[1,2,3],2.0,width=6.1,amplitude=.38);self.note('정상파: 마디 위치와 공간적 모양을 유지하며 실제로 진동한다');self.to(49)
  self.cue(10);self.play(Indicate(fixed_string(centers[0],6.1)),run_time=.7);self.put(self.title('고정된 양끝 → 허용된 정상모드',y=-2.5 if L.portrait else -2.2,size=29,color=GOLD));self.to(55)
class EquationDirection(WaveScene):
 offset=55
 def construct(self):
  self.cue(11);a,b=L.panels;line=string_curve(a,1,width=5.5);field=AtomicField(b,size=2.5);self.put(line,field);self.note('줄의 경계조건과 원자의 쿨롱 퍼텐셜은 서로 다른 조건');self.to(59)
  self.cue(12);self.clear();field=AtomicField(L.panels[0],size=2.5,label=False);plot=PotentialPlot(L.panels[1],width=5.8 if L.portrait else 5.3,height=2.1);self.put(field,plot)
  dot=Dot(plot.axes.c2p(.4,-2.5),radius=.07,color=GOLD);self.put(dot);self.play(UpdateFromAlphaFunc(dot,lambda obj,a:obj.move_to(plot.axes.c2p(.4+4.6*a,-1/(.4+4.6*a)))),run_time=1.4,rate_func=linear);self.note('퍼텐셜 에너지 · 확률밀도와는 다른 물리량');self.to(64)
  self.cue(13);self.clear();self.put(self.title('전자의 운동에너지',y=2.3 if L.portrait else 1.5,size=33,color=BLUE),self.title('+',y=1.25 if L.portrait else .5,size=38),self.title('원자핵과의 전기적 상호작용',y=.2 if L.portrait else -.5,size=31,color=ORANGE));self.note('조건을 함께 고려해 원자 안의 파동 상태를 구한다');self.to(69)
  self.cue(14);self.clear();eq=self.title('Ĥψ = Eψ',y=1.6 if L.portrait else .7,size=55);definition=self.title('Ĥ = 운동에너지 + 퍼텐셜 에너지',y=-.1 if L.portrait else -.7,size=29,color=GOLD);subtitle=self.title('시간에 무관한 슈뢰딩거 방정식',y=-1.5 if L.portrait else -1.8,size=26,color=MUTED);self.put(eq,definition,subtitle);self.to(75)
  self.cue(15);self.remove(definition,subtitle);self.body.remove(definition,subtitle);self.play(eq.animate.shift(UP*.65),run_time=.5);self.put(self.title('방정식 + 정규화 가능한 결합 상태',y=.2 if L.portrait else -.2,size=29,color=GREEN));self.note('임의 파형의 단순 선별이 아니라 주어진 조건의 해를 구하는 문제');self.to(80)
class BoundDirection(WaveScene):
 offset=80
 def construct(self):
  self.cue(16);self.put(self.title('Ĥψ = Eψ',y=3.9 if L.portrait else 2.0,size=36,color=GOLD));centers=[p(x,1.3 if L.portrait else .4) for x in [-2.45,0,2.45]]
  fields=[AtomicField(c,n=n,l=l,size=2.1,label=False) for c,(n,l) in zip(centers,[(1,0),(2,0),(2,1)])];self.put(*fields);self.note('수소 결합 상태의 공간 부분 단면 · 각 그림의 축척·밝기는 개별 정규화');self.to(83)
  self.cue(17);labels=VGroup(*[text(name,c[0],c[1]-1.35,25,BLUE) for c,name in zip(centers,['1s','2s','2p_z'])]);self.put(labels);self.play(*[Indicate(f.image) for f in fields],run_time=.7);self.to(87)
  self.cue(18);energies=VGroup(*[text(value,c[0],c[1]-2.25,27,GOLD if i==0 else LEVEL,width=2.35) for i,(c,value) in enumerate(zip(centers,['−13.60 eV','−3.40 eV','−3.40 eV']))]);self.put(energies);self.note('2s와 2p는 같은 에너지 · 한 에너지에 여러 상태가 대응할 수 있음');self.to(94)
  self.cue(19);self.clear();spectrum=EnergySpectrum(L.center,width=4.3,height=3.4,label='');self.put(spectrum);self.put(text('E ≥ 0: 연속 영역',x=0 if L.portrait else 4.7,y=4.3 if L.portrait else 1.7,size=24,color=MUTED,width=6 if L.portrait else 4.5),self.title('원자에 묶인 상태 · E < 0',y=-2.0 if L.portrait else -2.2,size=25,color=LEVEL));self.note('불연속 에너지는 여기서 결합 상태에 한정한다');self.to(100)
class HydrogenDirection(WaveScene):
 offset=100
 def construct(self):
  self.cue(20);self.put(AtomicField(L.center,size=3.4),self.title('Hydrogen · 수소',y=-1.9,size=32,color=GOLD));self.field_note();self.to(103)
  self.cue(21);self.clear();xs=L.pair;yy=1.0 if L.portrait else .15
  _,energies,_=solve_radial();left=EnergySpectrum(p(xs[0],yy),width=2.25,height=2.8,label='보어 · 가정');right=EnergySpectrum(p(xs[1],yy),width=2.25,height=2.8,label='슈뢰딩거 · 계산',values=energies);self.put(left,right)
  for n in [1,2,3]:self.play(Indicate(left.levels[n]),Indicate(right.levels[n]),run_time=.65)
  self.note('비상대론적 수소의 대표 근삿값 · −13.60 / n² eV');self.to(109)
  self.cue(22);left.remove(left.label_mobject);right.remove(right.label_mobject);self.put(self.title('같은 결합 에너지 · 다른 접근',y=-2.1,size=29,color=GOLD));self.to(114)
  self.cue(23);self.clear();bohr=BohrAtom(p(xs[0],1.2 if L.portrait else .4),(.5,.9,1.35));field=AtomicField(p(xs[1],1.2 if L.portrait else .4),size=2.7);self.put(bohr,field,text('허용 궤도를 가정',xs[0],-1.0,24,MUTED,width=3.5));self.play(Indicate(bohr.orbits),run_time=.6);self.to(117)
  self.cue(24);self.put(text('파동을 풀어 에너지를 도출',xs[1],-1.0,23,GREEN,width=3.55),self.title('원자핵의 인력 + 운동에너지 → Ĥψ = Eψ',y=-2.3,size=27,color=GOLD));self.play(Indicate(field.image),run_time=.8);self.field_note();self.to(126)
class SpaceDirection(WaveScene):
 offset=126
 def construct(self):
  self.cue(25);c=L.center;atom=BohrAtom(c,(.8,1.4,2));self.put(atom);e=Dot(c+p(1.4,0),radius=.08,color=ELECTRON);self.put(e);self.play(MoveAlongPath(e,Circle(radius=1.4).move_to(c)),run_time=.7,rate_func=linear);self.play(FadeOut(atom.orbits),FadeOut(e),run_time=.65);atom.remove(atom.orbits);self.body.remove(e);self.note('같은 핵 중심을 유지 · 원형 경로를 미리 정하지 않는다');self.to(130)
  self.cue(26);field=AtomicField(c,size=4.4,nucleus=True);self.put(field);self.play(FadeIn(field),run_time=.8);self.field_note();self.to(135)
class StationaryDirection(WaveScene):
 offset=135
 def construct(self):
  self.cue(27);c=L.center;field=AtomicField(c,size=3.8);orbit=Circle(radius=1.5,color=MUTED).move_to(c);self.put(field,orbit);self.play(FadeOut(orbit),run_time=.65);self.body.remove(orbit);self.field_note();self.to(139)
  self.cue(28);self.clear();xs=L.pair;yy=1.1 if L.portrait else .4;leftc=p(xs[0],yy);rightc=p(xs[1],yy);orbit=Circle(radius=1.35,color=MUTED).move_to(leftc);field=AtomicField(rightc,size=2.7,label=False);self.put(orbit,Dot(leftc,color=NUCLEUS),field,text('고전적 원운동',xs[0],yy+(1.9 if L.portrait else 1.65),23,MUTED,width=3.5),text('양자 정상상태',xs[1],yy+(1.9 if L.portrait else 1.65),23,GREEN,width=3.5))
  e=Dot(leftc+p(1.35,0),radius=.08,color=ELECTRON);self.put(e)
  acceleration=always_redraw(lambda:Arrow(e.get_center(),e.get_center()+(leftc-e.get_center())*.55,buff=0,color=ORANGE,stroke_width=2));self.put(acceleration);self.play(MoveAlongPath(e,orbit),run_time=1.6,rate_func=linear);acceleration.clear_updaters()
  phasecenter=rightc+p(0,-1.65);phasecircle=Circle(radius=.23,color=MUTED).move_to(phasecenter);phasearrow=Arrow(phasecenter,phasecenter+RIGHT*.23,buff=0,color=GOLD,stroke_width=3);self.put(phasecircle,phasearrow,text('전체 위상',phasecenter[0],phasecenter[1]-.5,19,GOLD));self.play(Rotate(phasearrow,TAU,about_point=phasecenter),run_time=1.2,rate_func=linear);self.put(self.title('Ψ(r,t) = ψ(r) exp(−iEt/ℏ)',y=-1.6 if L.portrait else -2.15,size=32,color=GOLD));self.note('정상상태의 공간적 모양은 일정 · 전체 위상은 시간에 따라 변할 수 있음');self.to(147)
  self.cue(29);self.clear();levels=EnergySpectrum(L.center,width=4,height=2.9,label='');self.put(levels,SurroundingRectangle(levels.levels[1],color=GOLD,buff=.15));self.put(self.title('더 낮은 원자 내부 상태로의 방출 전이 없음',y=-2.3,size=26,color=GOLD));self.note('바닥상태의 존재에는 양자 운동에너지와 원자핵 인력이 함께 관여');self.to(152)
class MeaningDirection(WaveScene):
 offset=152
 def construct(self):
  self.cue(30);field=AtomicField(L.center,size=4.4);eq=self.title('Ĥψ = Eψ',y=3.8 if L.portrait else 2.2,size=38,color=GOLD);questionline=self.title('상태·에너지 계산 뒤에도 남은 질문',y=-2.1,size=28);self.put(field,eq,questionline);self.field_note();self.to(160)
  self.cue(31);self.remove(eq,questionline);self.body.remove(eq,questionline);self.play(field.animate.scale(1.08),run_time=.6);self.to(163)
  self.cue(32);detector=text('측정 사례 · 한 위치의 검출',y=-1.75,size=27,color=GOLD);point=L.center+p(.65,.35);dot=Dot(point,radius=.085,color=GOLD);self.put(detector,dot);self.play(Flash(point,color=GOLD,flash_radius=.25),run_time=.6);self.note('한 번의 위치 측정 결과만 표시 · 파동의 물리적 붕괴 과정을 묘사하지 않음');self.to(168)
  self.cue(33);self.play(FadeOut(dot),FadeOut(detector),run_time=.4);self.body.remove(dot,detector);self.put(text('?',0,L.center[1],48,GOLD));self.field_note();self.to(172)
  self.cue(34);self.put(self.title('1926 · Max Born',y=-2.5,size=27,color=GOLD));self.to(175);self.to(176)
