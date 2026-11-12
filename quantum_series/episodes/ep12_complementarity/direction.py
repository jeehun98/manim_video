import json
from pathlib import Path
import numpy as np
from manim import *
from quantum_series.shared.theme import text,p,configure,INK,MUTED,GOLD
from quantum_series.shared.complementarity import *
from quantum_series.episodes.ep12_complementarity.layouts import ComplementarityLayout
D=json.loads(Path(__file__).with_name('script.json').read_text(encoding='utf-8'));L=ComplementarityLayout(configure().portrait)
def wrap(s,n):
 lines=[];line=''
 for word in s.split():
  if line and len(line+' '+word)>n:lines.append(line);line=word
  else:line=(line+' '+word).strip()
 return '\n'.join(lines+[line])
class EpisodeScene(Scene):
 offset=0
 def setup(self):
  self.caption=None;self.heading=None;self.foot=None;self.body=Group()
  self.add(text('양자역학의 발견   /   1927 · 닐스 보어',0 if L.portrait else -3.7,L.brand_y,17,MUTED))
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
 def label(self,s,c,color=INK,size=28,width=6.3):return text(s,*c[:2],size=size,color=color,width=width)
 def drop(self,*objects):
  self.play(*[FadeOut(o) for o in objects],run_time=.4)
  for o in objects:self.body.remove(o)
 def experiment(self,d=0,n=0):
  self.distinguishability=ValueTracker(d);self.device=Apparatus(L.apparatus,d>.9);self.screen=DetectorScreen(L.screen);self.profile=ProbabilityProfile(L.profile,self.distinguishability);self.put(self.device,self.screen,self.profile)
  self.image=None;self.counter=None;self.status=None;self.record_tag=None;self.accumulate(d,n,animate=False);self.status_update()
  self.note('현대적 이중슬릿 개념 시뮬레이션 · 1927년 보어의 실제 실험 재현이 아님')
 def accumulate(self,d,n,animate=True):
  if self.image:self.remove(self.image);self.body.remove(self.image)
  if self.counter:self.remove(self.counter);self.body.remove(self.counter)
  self.image=self.screen.image(d,n);self.counter=text(f'N = {n:,}',*(L.screen+p(0,.8))[:2],size=23,color=GOLD);self.put(self.image,self.counter)
  if animate:self.play(FadeIn(self.image),run_time=.35)
 def status_update(self):
  if self.status:self.remove(self.status);self.body.remove(self.status)
  d=self.distinguishability.get_value();v=marker_overlap(d);self.status=text(f'경로 구별도 D = {d:.2f}     간섭 가시도 V = {v:.2f}',y=L.summary_y,size=22,color=INK,width=L.body_width);self.put(self.status)
 def distinguish(self,value,duration=1.4):
  if self.status:self.remove(self.status);self.body.remove(self.status);self.status=None
  self.play(self.distinguishability.animate.set_value(value),run_time=duration,rate_func=smooth);self.status_update()
 def finish(self):self.profile.freeze()
 def emit(self,d,index):
  c=L.apparatus;electron=Dot(c+p(-2.4,0),radius=.06,color=BLUE);self.put(electron);self.play(electron.animate.move_to(c+p(-1.25,0)),run_time=.35,rate_func=linear);self.remove(electron);self.body.remove(electron)
  self.accumulate(d,index+1,animate=False)
  if d>.99:
   record=int(samples(d)[index,2])
   if self.record_tag:self.remove(self.record_tag);self.body.remove(self.record_tag)
   self.record_tag=self.label('기록 '+('A' if record==0 else 'B'),c+p(1.55,-.65),PURPLE,size=22);self.put(self.record_tag)
   self.play(Circumscribe(self.device.marker.record_boxes[record],color=PURPLE),Flash(self.screen.at(samples(d)[index]),flash_radius=.16,color=GOLD),run_time=.35)
  else:self.play(Flash(self.screen.at(samples(d)[index]),flash_radius=.16,color=GOLD),run_time=.35)
 def change_device(self,active):
  self.play(Transform(self.device,Apparatus(L.apparatus,active)),run_time=.6)
class QuestionDirection(EpisodeScene):
 offset=0
 def construct(self):
  a,b=L.panels
  self.cue(0);wave=ParametricFunction(lambda t:a+p(t,.7*np.exp(-t*t/2)*np.cos(6*t)),t_range=[-2.8,2.8,.03],color=BLUE);self.put(wave,self.label('1927 · Niels Bohr',b,GOLD,size=38));self.play(Create(wave),run_time=.9);self.note('상태의 파동적 표현과 실험에서 얻는 정보를 함께 묻는다');self.to(6)
  self.cue(1);self.drop(self.body[1]);self.put(self.label('Complementarity',b,GOLD,size=39));self.to(9)
  self.cue(2);self.clear();self.experiment(0,500);self.note('간섭은 반복 검출의 분포 · 각각의 검출은 화면의 한 위치');self.to(15)
  self.cue(3);self.put(self.label('입자?   파동?',L.apparatus+p(0,1.8),GOLD,size=32));self.to(18);self.finish()
class AccumulationDirection(EpisodeScene):
 offset=18
 def construct(self):
  self.cue(4);self.experiment(0,0);self.play(Circumscribe(self.device.slits,color=BLUE),run_time=.7);self.to(21)
  self.cue(5);self.note('한 번에 전자 하나 · 슬릿 이후의 고전적 궤도를 지정하지 않는다');self.to(26)
  self.cue(6);self.emit(0,0);self.emit(0,1);self.to(31)
  self.cue(7)
  for n in [20,200]:self.accumulate(0,n)
  self.to(35)
  self.cue(8);self.accumulate(0,2000);hist=self.profile.histogram(0,2000);self.put(hist);self.play(FadeIn(hist),run_time=.5);self.note('N = 2000 · 금색 히스토그램은 실제 표본, 청록색 곡선은 모형 확률');self.to(42)
  self.cue(9);self.play(Flash(self.screen.at(samples(0)[-1]),color=GOLD,flash_radius=.16),run_time=.6);self.note('한 점의 검출과 여러 번 반복한 분포는 서로 다른 수준의 정보');self.to(46)
  self.cue(10);self.to(47);self.finish()
class AmplitudesDirection(EpisodeScene):
 offset=47
 def construct(self):
  self.cue(11);self.experiment(0,2000);self.drop(self.device);c=L.apparatus
  origin=c+p(-1.3,-.2);one=Arrow(origin,origin+p(1.3,0),buff=0,color=BLUE);two=Arrow(origin+p(1.3,0),origin+p(2.6,0),buff=0,color=PURPLE);self.put(one,two,self.label('같은 위치에 기여하는 두 진폭',c+p(0,1.3),size=25),self.label('P(x) = |ψA(x) + ψB(x)|²',c+p(0,-1.25),size=27));self.play(Create(one),Create(two),run_time=.8);self.note('화살표는 확률진폭의 복소 평면 표현 · 입자의 이동 경로가 아님');self.to(55)
  self.cue(12);reversed_arrow=Arrow(origin+p(1.3,0),origin,buff=0,color=PURPLE);self.play(Transform(two,reversed_arrow),run_time=1);self.note('위치별 위상차가 다르므로 보강과 상쇄가 분포의 봉우리와 골을 만든다');self.play(Transform(two,Arrow(origin+p(1.3,0),origin+p(2.6,0),buff=0,color=PURPLE)),run_time=1);self.to(61);self.finish()
class PathsDirection(EpisodeScene):
 offset=61
 def construct(self):
  self.cue(13);self.experiment(0,0);self.to(63)
  self.cue(14);self.play(Circumscribe(self.device.slits,color=PURPLE),run_time=.6);self.to(66)
  self.cue(15);c=L.apparatus;ball=Dot(c+p(-2.3,0),radius=.1,color=MUTED);label=self.label('회색 공 · 고전적 비교 예시',c+p(0,1.9),MUTED,size=23);self.put(ball,label);self.note('이 궤도는 비교용 고전적 공 · 전자의 실제 궤도로 제시하지 않는다');self.play(ball.animate.move_to(c+p(-.75,0)),run_time=.5);self.play(Circumscribe(self.device.slits[1],color=MUTED),FadeOut(ball),run_time=.35);self.remove(ball);self.body.remove(ball);ball=Dot(c+p(1.6,0),radius=.1,color=MUTED);self.put(ball);self.play(FadeIn(ball),run_time=.25);self.drop(ball,label);self.to(70)
  self.cue(16);self.change_device(True);self.note('전자를 흡수하는 화면 검출기와 구별 · 통과 경로를 기록하는 이상적 장치');self.to(75)
  self.cue(17);self.distinguish(1,1.1);self.emit(1,0);self.emit(1,1);self.play(Circumscribe(self.device.marker,color=PURPLE),run_time=.5);self.note('정면 표시 기준 A는 왼쪽 틈, B는 오른쪽 틈 · 경로 기록은 서로 구별 가능');self.to(79);self.finish()
class LossDirection(EpisodeScene):
 offset=79
 def construct(self):
  self.cue(18);self.experiment(1,0);self.note('같은 전자총·두 슬릿·검출 화면 · 경로 기록 조건을 바꾼 새 실험');self.to(83)
  self.cue(19);reference=self.profile.ax.plot(lambda x:float(probability(x,1)),x_range=[-3,3,.025],color=GREEN,stroke_opacity=.35);self.put(reference);self.note('희미한 청록색은 이전 조건의 기준 곡선 · 현재 분포는 주황색');self.play(Circumscribe(self.profile.curve,color=ORANGE),run_time=.7);self.to(87)
  self.cue(20);self.drop(reference);self.emit(1,0);self.emit(1,1);self.note('기록 A/B는 남고, 화면의 개별 검출도 계속된다');self.to(90)
  self.cue(21)
  for n in [20,200,2000]:self.accumulate(1,n)
  hist=self.profile.histogram(1,2000);self.put(hist);self.play(FadeIn(hist),run_time=.5);self.note('N = 2000 · 각 경로의 확률을 더한 매끄러운 분포 · 평평한 직선이 아님');self.to(94);self.finish()
class RecordsDirection(EpisodeScene):
 offset=94
 def construct(self):
  self.cue(22);self.experiment(1,2000);self.note('전자만의 분포에서 사라진 간섭항 · 전체 전자–기록 상태의 소멸을 뜻하지 않음');self.to(98)
  self.cue(23);kick=Arrow(L.apparatus+p(.5,0),L.apparatus+p(1.6,.65),buff=0,color=MUTED);self.put(kick);self.play(Create(kick),run_time=.55);self.note('단순 충격으로만 설명하려는 직관을 먼저 비교한다');self.to(102)
  self.cue(24);self.drop(kick);self.to(104)
  self.cue(25);self.drop(self.device,self.image,self.counter,self.screen);self.image=None;self.counter=None;self.put(self.label('기록 상태 내적 γ = 〈mA|mB〉',L.screen,PURPLE,size=25));c=L.apparatus
  self.distinguish(0,.6);self.note('이제는 기록 상태의 구별 가능성을 변화시키는 별도의 모형 설명')
  self.record_title=self.label('A ↔ |mA〉     B ↔ |mB〉',c+p(0,1.8),PURPLE,size=27);self.put(self.record_title)
  origin=c+p(-1,-.75);axes=VGroup(Line(origin,origin+p(2.6,0),color=MUTED),Line(origin,origin+p(0,2),color=MUTED));self.put(axes)
  self.recordA=Arrow(origin,origin+p(2,0),buff=0,color=BLUE)
  self.recordB=always_redraw(lambda:Arrow(origin,origin+p(2*marker_overlap(self.distinguishability.get_value()),2*self.distinguishability.get_value()),buff=0,color=PURPLE));self.put(self.recordA,self.recordB);self.to(109)
  self.cue(26);self.distinguish(.65,1.7);self.note('추상적 기록 상태 공간 · 화살표의 겹침은 기록 내적 γ를 뜻함');self.to(114)
  self.cue(27);self.distinguish(1,1.5);self.note('〈mA|mB〉 = 0 · 기록을 나누어 읽지 않고 전자만 집계하면 간섭항은 0');self.to(118)
  self.cue(28);eye=VGroup(Ellipse(width=.7,height=.32,color=MUTED),Dot(radius=.06,color=MUTED)).move_to(c+p(1.8,.6));self.put(eye);self.play(FadeIn(eye),run_time=.35);self.drop(eye);self.note('사람이 기록을 읽지 않아도 구별 가능한 기록 상태는 그대로 남는다');self.to(122)
  self.cue(29);env=VGroup(*[Circle(radius=.17,color=PURPLE,fill_opacity=.2).move_to(c+p(x,-1.25)) for x in [-1.5,0,1.5]]);self.put(env,self.label('장치 · 주변 환경과의 상관관계',c+p(0,-1.8),PURPLE,size=22));self.play(LaggedStart(*[FadeIn(e) for e in env],lag_ratio=.15),run_time=.7);self.note('환경 상태 변화의 추상적 표현 · 전자에서 정보 입자가 떨어져 나오는 그림이 아님');self.to(127);self.recordB.clear_updaters();self.finish()
class MeaningDirection(EpisodeScene):
 offset=127
 def construct(self):
  self.cue(30);self.experiment(0,0);self.note('이중슬릿은 상보성의 대표 예시 · 보어의 관점은 실험 조건과 개념 적용의 더 넓은 주제');self.to(131)
  self.cue(31);self.distinguish(.6,1.4);self.note('동등한 두 경로와 이상적인 순수 기록 상태를 가정한 교육용 모형');self.to(136)
  self.cue(32);self.change_device(True);self.distinguish(1,1.2);self.accumulate(1,2000);self.to(141)
  self.cue(33);self.accumulate(0,0);self.distinguish(0,1.4);self.change_device(False);self.accumulate(0,2000);self.note('조건을 바꿀 때마다 새로 준비한 실험의 결과 · 기존 점들이 위치를 옮기는 것이 아님');self.to(147)
  self.cue(34);self.play(Circumscribe(self.device.source,color=BLUE),run_time=.7);self.note('전자 아이콘을 입자와 파동으로 바꾸지 않는다 · 바뀐 것은 실험 조건');self.to(152)
  self.cue(35);self.accumulate(0,0);self.change_device(True);self.distinguish(1,1.2);self.accumulate(1,2000);self.to(157)
  self.cue(36);self.note('경로를 완전히 구별하는 정보와 선명한 간섭은 같은 조건에서 양립하지 않는다');self.to(162)
  self.cue(37);self.note('실험의 구성에 따라 확인할 수 있는 물리적 정보가 달라진다');self.to(165);self.finish()
class EquivalenceDirection(EpisodeScene):
 offset=165
 def construct(self):
  a,b=L.panels
  self.cue(38);self.put(self.label('같은 양자현상',p(0,4.05) if L.portrait else p(0,1.9),GOLD,size=34));self.note('실험에서 얻는 현상은 같지만, 수학적 출발점은 달랐다');self.to(168)
  self.cue(39);matrix=VGroup(*[self.label(s,a+p(x,y),BLUE,size=27,width=2) for s,x,y in [('X₁₁',-1,.5),('X₁₂',1,.5),('X₂₁',-1,-.4),('…',1,-.4)]]);wave=ParametricFunction(lambda x:b+p(x,.6*np.exp(-x*x/2)*np.cos(5*x)),t_range=[-2.6,2.6,.03],color=BLUE)
  self.put(matrix,wave,self.label('행렬역학',a+p(0,-1.3),size=27),self.label('파동역학',b+p(0,-1.3),size=27));self.play(Create(matrix),Create(wave),run_time=.9);self.to(173)
  self.cue(40);self.put(text('서로 다른 표현은 어떻게 같은 결과를 줄까?',y=L.summary_y,size=28,color=GOLD,width=L.body_width));self.to(178)
