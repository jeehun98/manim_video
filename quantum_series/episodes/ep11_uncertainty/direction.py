import json
from pathlib import Path
import numpy as np
from manim import *
from quantum_series.shared.theme import text,p,configure,INK,MUTED,GOLD
from quantum_series.episodes.ep11_uncertainty.layouts import UncertaintyLayout
from quantum_series.shared.uncertainty import *
D=json.loads(Path(__file__).with_name('script.json').read_text(encoding='utf-8'));L=UncertaintyLayout(configure().portrait)
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
  self.add(text('양자역학의 발견   /   1927 · 하이젠베르크',0 if L.portrait else -3.7,L.brand_y,17,MUTED))
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
 def pair(self,sigma=.9):
  self.sigma=ValueTracker(sigma);a,b=L.panels
  self.pos=PositionDistribution(a,self.sigma);self.mom=MomentumDistribution(b,self.sigma);self.put(self.pos,self.mom)
  self.status=None;self.update_status();self.note('정규화된 최소 불확정성 가우스 상태 · ℏ = 1 · 점선은 평균 ± 표준편차')
 def update_status(self,relation=False):
  if self.status:self.remove(self.status);self.body.remove(self.status)
  sx=self.sigma.get_value();sp=momentum_std(sx)
  s='Δx Δpₓ ≥ ℏ / 2' if relation else f'Δx = {sx:.2f}    Δpₓ = {sp:.2f}    Δx Δpₓ = 0.50'
  self.status=text(s,y=L.summary_y,size=30 if relation else 23,color=INK,width=L.body_width);self.put(self.status)
 def width_to(self,sigma,duration=1.6):
  if self.status:self.remove(self.status);self.body.remove(self.status);self.status=None
  self.play(self.sigma.animate.set_value(sigma),run_time=duration,rate_func=smooth);self.update_status()
 def finish_pair(self):self.pos.freeze();self.mom.freeze()
class QuestionDirection(EpisodeScene):
 offset=0
 def construct(self):
  a,b=L.panels
  self.cue(0);wave=WavePacket(a);dot=Dot(b,color=GOLD,radius=.1);self.put(wave,dot,self.label('위치 x',a+p(0,1.25),GREEN),self.label('운동량 pₓ',b+p(0,1.25),GOLD));self.note('한 상태의 위치와 운동량을 함께 묻는다');self.play(Create(wave),run_time=1);self.to(7)
  self.cue(1);self.play(Flash(dot.get_center(),color=GOLD,flash_radius=.3),run_time=.5);self.to(9)
  self.cue(2);self.clear();ax=Axes(x_range=[0,90,30],y_range=[0,1.1,.5],x_length=5.6,y_length=1.6,tips=False).move_to(a);curve=ax.plot(lambda t:.1+.85*np.exp(-((t-50)/8)**2),color=GOLD);self.put(ax,curve,self.label('니켈 산란 · 각도별 전류',a+p(0,1.25),GOLD,size=25));screen=Rectangle(width=5.6,height=1.5,color=MUTED).move_to(b);self.put(screen,Dot(b+p(.5,0),color=GOLD,radius=.08),self.label('국소 검출의 개념 표현',b+p(0,-1.15),size=24));self.note('산란 전류의 실험과 한 점의 검출 개념도는 구분한 표현');self.to(15)
  self.cue(3);self.clear();self.put(self.label('위치 x = ?',a,GREEN,size=40),self.label('운동량 pₓ = ?',b,GOLD,size=40));self.to(19)
class PlaneDirection(EpisodeScene):
 offset=19
 def construct(self):
  a,b=L.panels;phase=ValueTracker(0)
  self.cue(4);wave=always_redraw(lambda:PlaneWave(a,k=6,phase=phase.get_value()));self.put(wave,self.label('Re ψ(x) · 오른쪽 진행파',a+p(0,1.15),BLUE,size=26),self.label('…',a+p(-3.2,0),MUTED),self.label('…',a+p(3.2,0),MUTED));self.note('이상적인 평면파 · 유한한 화면 창이며 물리적 경계가 아님');self.play(phase.animate.set_value(2*PI),run_time=1.2,rate_func=linear);self.to(22)
  self.cue(5);self.play(phase.animate.increment_value(4*PI),run_time=2,rate_func=linear);self.to(26)
  self.cue(6);spectrum=VGroup(Line(b+p(-2.7,-.55),b+p(2.7,-.55),color=MUTED),Arrow(b+p(0,-.55),b+p(0,.85),buff=0,color=GOLD),self.label('하나의 성분 p₀ = ℏk₀ > 0',b+p(0,1.3),GOLD,size=25),self.label('pₓ = h / λ',b+p(0,-1.2),GOLD,size=32));self.put(spectrum);self.play(Create(spectrum[1]),run_time=.65);self.to(31)
  self.cue(7);self.drop(spectrum);flat=VGroup(Line(b+p(-2.7,0),b+p(2.7,0),color=GREEN),self.label('|ψ|²는 위치에 무관',b+p(0,.85),GREEN),self.label('특정 위치에 집중되지 않는다',b+p(0,-.85),size=25));self.put(flat);self.to(35)
  self.cue(8);region=Rectangle(width=.7,height=1.5,color=PURPLE,fill_opacity=.08).move_to(a);self.put(region);self.note('화면의 일부를 강조해도 평면파 자체가 국소화되는 것은 아니다');self.to(38);wave.clear_updaters()
class SuperpositionDirection(EpisodeScene):
 offset=38
 def construct(self):
  a,b=L.panels
  self.cue(9);components=VGroup(*[PlaneWave(a+p(0,y),k=k,amp=.23,color=c) for y,k,c in [(.7,4.8,BLUE),(0,6,GREEN),(-.7,7.2,PURPLE)]]);self.put(components,self.label('서로 다른 파수 k',a+p(0,1.5),size=26));self.note('파수 k = 2π / λ · 표시한 세 성분은 중첩 원리를 설명하는 예');self.play(LaggedStart(*[Create(w) for w in components],lag_ratio=.2),run_time=1.1);self.to(42)
  self.cue(10);self.play(*[w.animate.move_to(a).set_opacity(.3) for w in components],run_time=.7)
  summed=ParametricFunction(lambda x:b+p(x,float(np.real(component_sum(x)[0]))),t_range=[-2.9,2.9,.03],color=BLUE);sum_label=self.label('81개 파수 성분의 중첩',b+p(0,1.2),BLUE,size=25);self.put(summed,sum_label);self.play(Create(summed),run_time=1);self.note('가우스 가중치로 81개 성분을 합산 · 단순히 사인파를 자른 것이 아님');self.to(46)
  self.cue(11);self.drop(components);packet=WavePacket(a,sigma=.7);self.put(packet,self.label('파동함수의 실수부 · 회색은 |ψ|',a+p(0,-1.25),BLUE,size=23));self.play(Create(packet),run_time=.7);self.to(50)
  self.cue(12);self.drop(summed,sum_label);curve=ParametricFunction(lambda x:b+p(x,1.2*float(density(x,.7))-.4),t_range=[-2.9,2.9,.04],color=GREEN);self.put(curve,self.label('위치 확률밀도 |ψ|²',b+p(0,1.2),GREEN,size=26));self.note('파란 진동선은 Re ψ · 청록색 곡선은 확률밀도 · 진폭 포락선과 구분');self.to(52)
class TradeoffDirection(EpisodeScene):
 offset=52
 def construct(self):
  self.cue(13);self.pair(1.15);self.width_to(.7,2);self.to(57)
  self.cue(14);self.update_status();self.note('pₓ = ℏk · 파수 성분의 분포가 운동량 분포로 이어진다');self.play(Indicate(self.mom.ax,color=GOLD),run_time=.7);self.to(60)
  self.cue(15);self.width_to(.43,2.4);self.to(65)
  self.cue(16);self.width_to(1.2,2.1);self.to(69)
  self.cue(17);self.width_to(.7,1.1);self.note('한 번의 측정값이 아니라 같은 상태에서 얻을 결과들의 표준편차');self.to(73)
  self.cue(18);self.update_status(True);self.note('Δx와 Δpₓ는 표준편차 · 일반적인 상태는 ≥ · 이 가우스 예는 등호');self.play(Indicate(self.status),run_time=.7);self.to(78)
  self.cue(19);self.width_to(.48,1.4);self.update_status(True);self.to(82);self.finish_pair()
class MicroscopeDirection(EpisodeScene):
 offset=82
 def construct(self):
  c=p(0,.1) if L.portrait else p(-3.65,-1.05);b=p(0,-1.65) if L.portrait else p(3.65,.1)
  self.cue(20);scope=GammaMicroscope(c);self.put(scope);self.note('1927년의 역사적 사고실험 · 실제 감마선 현미경의 설계도가 아님');self.to(86)
  self.cue(21);self.put(self.label('감마선 현미경',p(0,4.15) if L.portrait else b+p(0,1.55),ORANGE,size=31));self.to(89)
  self.cue(22);wave=PlaneWave(b,k=5,amp=.2,color=ORANGE);self.put(wave,self.label('파장 ↓  →  분해능 영역 ↓',b+p(0,-.8),ORANGE,size=25));self.play(Transform(wave,PlaneWave(b,k=11,amp=.2,color=ORANGE)),run_time=1.1);self.note('주어진 광학 조건에서 짧은 파장이 더 작은 구조를 구별한다');self.to(94)
  self.cue(23);self.drop(wave);formula=self.label('pγ = h / λ',b,ORANGE,size=35);self.put(formula);self.to(97)
  self.cue(24);photon=Dot(c+p(-2.8,0),color=ORANGE,radius=.07);self.put(photon);self.play(photon.animate.move_to(c),run_time=.7,rate_func=linear)
  self.play(photon.animate.move_to(c+p(.65,1.8)),run_time=.6,rate_func=linear);kick=Arrow(c,c+p(1.2,-.8),buff=.1,color=BLUE);self.put(kick);self.play(Create(kick),run_time=.5);self.note('광자의 산란에 따른 운동량 전달 · 화살표는 정량 충돌 궤적이 아님');self.to(101)
  self.cue(25);options=VGroup(*[DashedLine(c,c+p(1.5,y),color=BLUE,dash_length=.08) for y in [-.3,-.7,-1.1]]);self.put(options);self.play(Create(options),run_time=.7);self.note('수집 각도 범위 때문에 운동량 전달을 완전히 특정하지 못하는 사고실험');self.to(106)
class IntrinsicDirection(EpisodeScene):
 offset=106
 def construct(self):
  a,b=L.panels
  self.cue(26);scope=GammaMicroscope(a+p(0,-1.5)).scale(.65,about_point=a);packet=WavePacket(b);self.put(scope,packet,self.label('장비의 영향만으로 설명될까?',b+p(0,1.3),size=25));self.note('측정 교란과 준비된 상태의 불확정성은 서로 구별한다');self.to(110)
  self.cue(27);self.clear();self.pair(.75);self.note('측정 장치와 광자 없이, 준비된 파동함수의 두 분포만 분석');self.to(116)
  self.cue(28);self.width_to(.55,1.5);self.note('동일한 상태의 두 표현 · 위치 파동함수와 운동량 파동함수는 푸리에 변환으로 연결');self.to(120)
  self.cue(29);self.width_to(1.15,1.7);self.width_to(.5,1.7);self.note('장치가 없어도 유지되는 제약 · Δx Δpₓ ≥ ℏ / 2');self.to(126);self.finish_pair()
class EquivalenceDirection(EpisodeScene):
 offset=126
 def construct(self):
  a,b=L.panels
  self.cue(30);operators=VGroup(RoundedRectangle(width=2,height=1.2,corner_radius=.1,color=BLUE).move_to(a+p(-1.3,0)),RoundedRectangle(width=2,height=1.2,corner_radius=.1,color=GOLD).move_to(a+p(1.3,0)),self.label('X',a+p(-1.3,0),BLUE,size=39),self.label('P',a+p(1.3,0),GOLD,size=39));self.put(operators,self.label('위치 · 운동량 연산자',a+p(0,1.4),size=25));packet=WavePacket(b);self.put(packet,self.label('파동함수의 중첩',b+p(0,1.4),BLUE,size=25));self.note('연산자는 상징적으로 표시 · 유한 행렬이 정준교환관계를 정확히 만족한다는 뜻 아님');self.to(131)
  self.cue(31);self.drop(operators);formula=self.label('XP − PX = iℏ I',a,GOLD,size=35);self.put(formula);self.play(Indicate(formula),run_time=.7);self.to(136)
  self.cue(32);self.play(Transform(packet,WavePacket(b,sigma=.45)),run_time=1);self.note('위치·운동량 표현을 잇는 푸리에 구조와 정준교환관계는 같은 제약을 준다');self.to(141)
  self.cue(33);self.put(text('Δx Δpₓ ≥ ℏ / 2',y=L.summary_y,size=33,color=INK));self.to(145)
class PredictionDirection(EpisodeScene):
 offset=145
 def construct(self):
  a,b=L.panels
  self.cue(34);self.put(self.label('현재 ψ(x, 0)',a+p(0,1.25),BLUE),self.label('미래 ψ(x, t)',b+p(0,1.25),BLUE));initial=WavePacket(a,sigma=.65,k0=1.2);self.put(initial);self.note('예시: 외력이 없는 자유입자 · 모든 상태가 반드시 퍼지는 것은 아님');self.to(149)
  self.cue(35);future=WavePacket(b,sigma=.65,k0=1.2);self.put(future);self.to(151)
  self.cue(36);self.drop(future);clock=ValueTracker(0);evolved=always_redraw(lambda:ParametricFunction(lambda x:b+p(x,float(np.real(free_psi(x,clock.get_value())))),t_range=[-2.9,2.9,.025],color=BLUE));self.put(evolved);self.play(clock.animate.set_value(.9),run_time=2.2,rate_func=linear);evolved.clear_updaters();self.to(155)
  self.cue(37);self.clear();ax=Axes(x_range=[-4,4,2],y_range=[0,1,.5],x_length=5.7,y_length=1.7,tips=False).move_to(a);rho=ax.plot(lambda x:float(density(x,.95)),color=GREEN);screen=Rectangle(width=5.7,height=1.5,color=MUTED).move_to(b);self.put(ax,rho,screen,self.label('보른 규칙 · |ψ|²',a+p(0,1.35),GREEN,size=26))
  rng=np.random.default_rng(1927);positions=rng.normal(0,.95,80);dots=VGroup(*[Dot(b+p(x*.62,rng.uniform(-.55,.55)),radius=.035,color=GOLD) for x in positions]);self.put(dots);self.play(LaggedStart(*[FadeIn(d) for d in dots],lag_ratio=.006),run_time=1.2);self.note('같은 상태를 반복 준비 · 평균 중심 좌표로 표시 · 각 검출은 한 위치');self.to(159)
  self.cue(38);self.put(self.label('상태의 변화는 방정식으로',a+p(0,-1.35),BLUE,size=24),self.label('개별 결과는 확률로',b+p(0,-1.35),GOLD,size=24));self.to(166)
class ComplementarityDirection(EpisodeScene):
 offset=166
 def construct(self):
  a,b=L.panels
  self.cue(39);pattern=VGroup(*[Line(a+p(x,-.8),a+p(x,.8),color=BLUE,stroke_width=8,stroke_opacity=.015+.985*np.cos(3*x)**2) for x in np.linspace(-2.5,2.5,61)]);screen=Rectangle(width=5.6,height=1.6,color=MUTED).move_to(b);dot=Dot(b+p(.35,.15),color=GOLD,radius=.09);self.put(pattern,screen,dot,self.label('간섭무늬의 분포',a+p(0,1.25),BLUE,size=26),self.label('하나의 검출 결과',b+p(0,-1.25),GOLD,size=26));self.note('간섭 분포와 국소 검출을 대비 · 경로 정보의 확정과는 구별');self.to(170)
  self.cue(40);self.clear();slits=VGroup(*[Line(a+p(-1.2,y0),a+p(-1.2,y1),color=MUTED,stroke_width=6) for y0,y1 in [(-1.3,-.45),(-.25,.25),(.45,1.3)]]);self.put(slits,self.label('?',a+p(-2,.0),PURPLE,size=37))
  for y in [-.35,.35]:self.put(Arc(radius=1.25,start_angle=-.65,angle=1.3,color=BLUE).shift(a+p(-1.2,y)))
  self.put(self.label('두 슬릿',a+p(0,1.65),size=26),pattern.copy().move_to(b),self.label('경로 정보도 얻는다면?',b+p(0,-1.3),PURPLE,size=26));self.note('경로 검출기는 아직 작동시키지 않은 질문 · 선명한 경로 정보와 간섭의 공존을 주장하지 않음');self.to(174)
  self.cue(41);self.put(text('1927 · Niels Bohr',y=L.summary_y,size=30,color=PURPLE));self.to(177)
