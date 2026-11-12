"""Born amplitudes, reproducible detector ensembles and coherent alternatives."""
import json
from pathlib import Path
import numpy as np
from manim import *
from quantum_series.shared.theme import text,p,configure,INK,MUTED,GOLD
from quantum_series.shared.wave_mechanics import AtomicField
from quantum_series.shared.matter_waves import matter_wave,abstract_state
from quantum_series.shared.born_visuals import *
from quantum_series.episodes.ep09_born.layouts import BornLayout
from quantum_series.episodes.ep09_born.simulation import samples,psi,density,histogram,interferometer,angular_probabilities
D=json.loads(Path(__file__).with_name('script.json').read_text(encoding='utf-8'));L=BornLayout(configure().portrait)
def wrap(s,n):
 lines=[];line=''
 for word in s.split():
  if line and len(line+' '+word)>n:lines.append(line);line=word
  else:line=(line+' '+word).strip()
 return '\n'.join(lines+[line])
class BornScene(Scene):
 offset=0
 def setup(self):
  self.caption=None;self.heading=None;self.foot=None;self.body=Group()
  self.add(text('양자역학의 발견   /   1926 · 막스 보른',0 if L.portrait else -3.7,L.brand_y,17,MUTED))
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
 def detector_setup(self,n=0):
  screen=Detector(L);self.put(screen);image=screen.image(n);self.put(image)
  counter=text(f'N = {n:,}',screen.center_point[0],screen.center_point[1]-screen.height_value/2-.45,28,GOLD);self.put(counter)
  return screen,image,counter
 def accumulate(self,screen,image,counter,n,duration=.55):
  new=screen.image(n);self.put(new);self.play(FadeIn(new),Transform(counter,text(f'N = {n:,}',screen.center_point[0],screen.center_point[1]-screen.height_value/2-.45,28,GOLD)),run_time=duration);self.remove(image);self.body.remove(image);return new
class QuestionDirection(BornScene):
 offset=0
 def construct(self):
  self.cue(0);field=AtomicField(L.center,size=4.2);name=self.title('1926 · Max Born',y=-2.1,size=34,color=GOLD);self.put(field,name);self.note('파동함수의 공간 부분 표현 · 입자 물질의 분포를 뜻하지 않음');self.to(6)
  self.cue(1);self.play(FadeOut(name),field.animate.scale(1.05),run_time=.7);self.body.remove(name);self.to(10)
  self.cue(2);self.clear();a,b=L.panels;field=AtomicField(a,size=2.65);screen=RoundedRectangle(width=4.6,height=1.85,corner_radius=.1,color=MUTED).move_to(b);self.put(field,screen);self.to(13)
  self.cue(3);dot=Dot(b+p(.55,.2),radius=.08,color=GOLD);self.put(dot);self.play(Flash(dot.get_center(),color=GOLD,flash_radius=.25),run_time=.6);self.note('파동함수의 표현과 국소적 검출을 대비 · 물질이 한 점으로 빨려들어가는 과정 아님');self.to(21)
  self.cue(4);self.put(self.title('ψ = ?',y=.2 if L.portrait else -.3,size=46,color=GOLD));self.to(24)
class ScatteringDirection(BornScene):
 offset=24
 def construct(self):
  self.cue(5);device=Scattering(L);self.put(device);self.note('1926 · 산란 연구의 문제 · 장치와 방향은 설명용 개념도');self.to(28)
  self.cue(6);electron=Dot(device.center_point+p(-2.8,0),color=BLUE,radius=.075);self.put(electron);self.play(electron.animate.move_to(device.center_point+p(-.2,0)),run_time=1.1,rate_func=linear);self.to(31)
  self.cue(7);self.remove(electron);self.body.remove(electron);rays=device.rays();self.put(rays)
  for ray in rays:self.play(Create(ray),run_time=.35)
  self.put(self.title('여러 방향은 각각 가능한 결과',y=-1.5 if L.portrait else -2.0,size=29,color=BLUE));self.note('전자 하나가 여러 개로 복제되어 이동한다는 뜻이 아님');self.to(37)
  self.cue(8);self.play(Indicate(rays),run_time=.7);self.to(40)
class AngularDirection(BornScene):
 offset=40
 def construct(self):
  self.cue(9);device=Scattering(L);self.put(device)
  waves=VGroup(*[Arc(radius=r,start_angle=-2.5,angle=5,color=BLUE,stroke_opacity=.55).shift(device.center_point) for r in [.65,1.1,1.55]])
  incident=VGroup(*[Line(device.center_point+p(x,-.45),device.center_point+p(x,.45),color=BLUE,stroke_opacity=.25) for x in [-2.5,-2.1,-1.7,-1.3]]);self.put(incident);self.play(Create(waves),run_time=1);self.put(waves);self.note('산란 진폭의 모형 · 실제 원자 산란 단면적이 아님');self.to(44)
  self.cue(10);bars=device.bars();label=self.title('방향별 진폭 |f|',y=-.85 if L.portrait else -1.9,size=31,color=BLUE);self.put(bars,label);self.play(Indicate(bars),run_time=.7);self.to(49)
  self.cue(11);self.play(Indicate(label,color=GOLD),run_time=.5);self.to(51)
  self.cue(12);self.play(Transform(bars,device.bars(True)),Transform(label,self.title('같은 크기의 검출 구간별 발견 가능성',y=-.85 if L.portrait else -1.9,size=28,color=GREEN)),run_time=.9)
  hit=2;point=device.at(hit);self.put(Dot(point,radius=.09,color=GOLD));self.play(Flash(point,color=GOLD,flash_radius=.23),run_time=.5);self.note('분포는 유지 · 한 번의 검출 결과는 한 방향');self.to(59)
  self.cue(13);self.put(self.title('보른의 확률 해석',y=-2.3,size=31,color=GOLD));self.to(61)
class RuleDirection(BornScene):
 offset=61
 def construct(self):
  self.cue(14);a,b=L.panels;wave=WavePlot(a,kind='real',label='복소 파동함수의 실수부 Re ψ');self.put(wave);self.note('실수부의 부호만으로 검출 확률을 정할 수 없다');self.to(64)
  self.cue(15);center=b;axes=Axes(x_range=[-1,1,1],y_range=[-1,1,1],x_length=2.4,y_length=1.9,tips=False,axis_config={'color':MUTED,'stroke_width':1}).move_to(center);arrow=Arrow(center,center+p(.65,.65),buff=0,color=BLUE);complexview=VGroup(axes,arrow,text('실수',center[0]+1.4,center[1],20,MUTED),text('허수',center[0],center[1]+1.3,20,MUTED));self.put(complexview);self.play(Rotate(arrow,PI,about_point=center),run_time=1);self.note('ψ는 음수·복소수도 가능 · 확률은 음수가 될 수 없음');self.to(70)
  self.cue(16);self.remove(complexview);self.body.remove(complexview);density_plot=WavePlot(b,kind='density',label='확률밀도 ρ(x)');self.put(density_plot);self.put(self.title('ρ(x) = |ψ(x)|²',y=-2.7 if L.portrait else -2.15,size=37,color=GREEN));self.note('밀도와 영역 확률은 다름 · 영역의 확률은 밀도를 적분해 구한다');self.to(75)
class IndividualDirection(BornScene):
 offset=75
 def construct(self):
  self.cue(17);screen,image,counter=self.detector_setup();plot=DensityPlot(L.hist_center,width=6.3 if L.portrait else 6.0);self.put(plot);self.note('현대적 개념 실험 · 가우스 준비 상태 · 실측/1926 장치 재현이 아님');self.to(76)
  self.cue(18);prep=text('같은 상태로 준비하고 한 번씩 검출',x=0 if L.portrait else 3.65,y=4.35 if L.portrait else 1.95,size=27,color=BLUE,width=6.5);self.put(prep);self.to(80)
  self.cue(19);self.remove(prep);self.body.remove(prep)
  for n in [1,2]:
   image=self.accumulate(screen,image,counter,n,.5);point=screen.at(samples()[n-1]);self.put(Dot(point,radius=.055,color=GOLD));self.play(Flash(point,color=GOLD,flash_radius=.18),run_time=.3)
  self.to(85);self.cue(20);point=screen.at(samples()[1]);self.play(Flash(point,color=GOLD,flash_radius=.2),run_time=.6);self.to(88)
class EnsembleDirection(BornScene):
 offset=88
 def construct(self):
  self.cue(21);screen,image,counter=self.detector_setup(2);plot=DensityPlot(L.hist_center,width=6.3 if L.portrait else 6.0);self.put(plot);self.note('동일한 준비 상태 · 같은 표본을 순서대로 누적 · 모의 데이터')
  for n in [10,100,1000]:image=self.accumulate(screen,image,counter,n,.65)
  self.to(92);self.cue(22);image=self.accumulate(screen,image,counter,3000,.6);bars=plot.bars(3000);self.put(bars);self.play(Create(bars),run_time=.65);self.to(95)
  self.cue(23);curve=plot.curve();self.put(curve);self.play(Create(curve),run_time=1);self.note('막대: count/(N·구간 폭) · 곡선: 예측 밀도 · 가로 위치의 주변 분포');self.to(99)
  self.cue(24);self.put(self.title('개별 위치 하나보다 반복 결과의 빈도를 예측',y=4.4 if L.portrait else -2.15,size=26,color=GREEN));self.play(Indicate(curve),run_time=.8);self.to(106)
class ClassicalDirection(BornScene):
 offset=106
 def construct(self):
  self.cue(25);self.put(self.title('확률은 무엇을 뜻할까?',y=.8,size=43,color=PURPLE));self.to(110)
  self.cue(26);self.clear();c=L.center;coin=VGroup(Circle(radius=.8,color=MUTED,fill_color=MUTED,fill_opacity=.15).move_to(c),text('?',*c[:2],size=43,color=GOLD));self.put(coin);self.to(114)
  self.cue(27);self.play(Rotate(coin,TAU,axis=UP),run_time=1.0);self.put(self.title('앞면 / 뒷면',y=-1.8,size=32,color=MUTED));self.note('고전적 확률의 예');self.to(118)
  self.cue(28);self.clear();self.put(self.title('초기 위치 · 속도 · 회전 · 주변 환경',y=2.0,size=29),self.title('초기 조건 + 운동 법칙 → 결과',y=.3,size=34,color=GOLD));self.note('고전적 결정론의 이상화 · 실제로 초기 조건을 완벽하게 알기는 어려움');self.to(124)
  self.cue(29);self.clear();c=L.center;paths=VGroup()
  for bend in [-1,0,1]:paths.add(DashedVMobject(ParametricFunction(lambda t,b=bend:c+p((t-.5)*5,b*np.sin(PI*t)),t_range=[0,1],color=MUTED),num_dashes=25))
  self.put(paths,self.title('숨겨진 경로가 존재할까?',y=-2,size=32,color=PURPLE));self.note('가상의 경로 후보 · 옳다/그르다를 확정하는 장면이 아님');self.to(129)
  self.cue(30);self.clear();a,b=L.panels;self.put(WavePlot(a,label='파동함수'),WavePlot(b,kind='density',label='보른 규칙의 확률밀도'));self.note('고전적인 경로를 먼저 지정하지 않고도 측정 확률을 계산');self.to(135)
class InterferenceDirection(BornScene):
 offset=135
 def construct(self):
  self.cue(31);ys=[2.6,1.2,-.2] if L.portrait else [1.6,.45,-.7];centers=[p(0,y) for y in ys]
  one=matter_wave(centers[0],3,5.6,.32,BLUE);two=matter_wave(centers[1],3,5.6,.32,GOLD);summed=matter_wave(centers[2],3,5.6,.64,GREEN);self.put(one,two);self.note('같은 검출 결과에 기여하는 두 진폭의 예');self.to(138)
  self.cue(32);self.put(summed);self.play(Create(summed),run_time=.7);self.play(Transform(two,matter_wave(centers[1],3,5.6,-.32,GOLD)),Transform(summed,Line(centers[2]+LEFT*2.8,centers[2]+RIGHT*2.8,color=ORANGE)),run_time=1.1);self.to(142)
  self.cue(33);self.put(self.title('|a₁ + a₂|²',y=-2.1,size=41,color=GREEN));self.note('구별되지 않는 가능성 · 위상 관계가 유지될 때 진폭을 먼저 더한다');self.to(147)
  self.cue(34);self.clear();xs=L.pair;yy=1.0 if L.portrait else .3
  circle=Circle(radius=.65,color=MUTED).move_to(p(xs[0],yy));up=Arrow(p(xs[0],yy),p(xs[0],yy+.58),buff=0,color=BLUE);down=Arrow(p(xs[0],yy),p(xs[0],yy+.58),buff=0,color=GOLD);sumlabel=text('두 진폭의 합',xs[0],yy-1.25,27,BLUE,width=3.5);self.put(circle,up,down,sumlabel)
  phase=ValueTracker(0);barbase=p(xs[1],yy-.7);frame=Rectangle(width=2.8,height=1.4,color=MUTED).move_to(barbase+p(0,.7));self.put(frame)
  bar=always_redraw(lambda:Rectangle(width=2.7,height=max(.005,1.3*abs(interferometer(phase.get_value())[0])**2),fill_color=GREEN,fill_opacity=.75,stroke_width=0).move_to(barbase+p(0,.05+max(.005,1.3*abs(interferometer(phase.get_value())[0])**2)/2)))
  self.put(bar,text('한 출력의 확률',xs[1],yy+1.25,25,GREEN,width=3.5));self.play(phase.animate.set_value(PI),Rotate(down,PI,about_point=p(xs[0],yy)),run_time=1.7,rate_func=linear);bar.clear_updaters();self.play(Transform(sumlabel,text('a₁ + a₂ = 0',xs[0],yy-1.25,27,ORANGE,width=3.5)),run_time=.3);self.put(text('0',xs[1],yy,38,ORANGE),self.title('다른 출력: 확률 1  ·  전체 확률은 유지',y=-2.4,size=26,color=GOLD));self.note('서로 구별되지 않는 두 경로 · 경로 정보가 기록되면 간섭이 약해지거나 사라질 수 있음');self.to(154)
  self.cue(35);self.clear();self.put(self.title('|a₁|² + |a₂|²',y=1.8,size=39,color=MUTED),self.title('≠',y=.65,size=41,color=ORANGE),self.title('|a₁ + a₂|²',y=-.5,size=43,color=GREEN));self.note('경로 정보가 없는 일관된 두 진폭의 예 · 확률을 각각 더하는 계산과 구분');self.to(158)
class MeaningDirection(BornScene):
 offset=158
 def construct(self):
  self.cue(36);a,b=L.panels;self.put(WavePlot(a,label='파동함수 ψ'),WavePlot(b,kind='density',label='확률밀도 |ψ|²'));self.note('파동함수 → 결과 확률 → 반복 검출의 통계');self.to(165)
  self.cue(37);self.clear();self.put(self.title('?',y=.7,size=62,color=PURPLE));self.to(167)
  self.cue(38);xs=L.pair;self.put(text('근본적인 확률?',xs[0],-1.0,28,GREEN,width=3.5),text('숨겨진 정보?',xs[1],-1.0,28,PURPLE,width=3.5));self.note('보른 규칙의 예측과 그 확률의 근본적 의미는 구별되는 문제');self.to(173)
  self.cue(39);self.clear();self.put(abstract_state(L.center),self.title('측정 · 불확정성',y=-1.6,size=31,color=PURPLE));self.note('개별 검출은 국소적 · 반복 측정의 통계에는 파동함수의 구조가 나타남');self.to(177);self.to(178)
