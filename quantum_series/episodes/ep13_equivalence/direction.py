import json
from pathlib import Path
import numpy as np
from manim import *
from quantum_series.shared.theme import text,p,configure,INK,MUTED,GOLD
from quantum_series.shared.representations import *
from quantum_series.shared.matrix_mechanics import MatrixGrid
from quantum_series.episodes.ep13_equivalence.layouts import FinaleLayout
D=json.loads(Path(__file__).with_name('script.json').read_text(encoding='utf-8'));L=FinaleLayout(configure().portrait)
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
  self.add(text('양자역학의 발견   /   1925–1932 · 두 표현의 연결',0 if L.portrait else -3.7,L.brand_y,17,MUTED))
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
 def pair_titles(self,left,right):
  a,b=L.panels;self.put(self.label(left,a+p(0,1.65),PURPLE,size=27),self.label(right,b+p(0,1.65),BLUE,size=27))
 def symbolic_matrix(self,c,label='A'):
  values=[[f'{label}{i}{j}'.translate(str.maketrans('123','₁₂₃')) for j in range(1,4)] for i in range(1,4)]
  grid=MatrixGrid(c,values,label=label,cell=.7,size=25)
  for entry in grid.entries.values():entry.set_color(PURPLE)
  return grid
 def vector(self,c,values=C,label='c'):
  return MatrixGrid(c,[[f'{v:.3f}'] for v in values],cell=.72,label=label,symbolic=False,indices=False,size=25)
 def summary(self,s,color=GOLD):
  if getattr(self,'summary_obj',None):self.remove(self.summary_obj);self.body.remove(self.summary_obj)
  self.summary_obj=text(s,y=L.summary_y,size=29,color=color,width=L.body_width);self.put(self.summary_obj)
 def expectation(self,changed=False):
  a,b=L.panels;self.put(text('∫ ψ* Hψ dx',a[0],-1.55,28,BLUE),text('c′† H′ c′' if changed else 'c† H c',b[0],-1.55,28,PURPLE));self.summary('두 계산의 평균 에너지 〈H〉 = 3.50 E₁')
class ContrastsDirection(EpisodeScene):
 offset=0
 def construct(self):
  a,b=L.panels
  self.cue(0);orbit=Circle(radius=.9,color=MUTED).move_to(a);core=Dot(a,color=GOLD,radius=.1);self.put(orbit,core);self.note('1925 · 전자의 궤도보다 스펙트럼과 물리량 사이의 관계에서 출발');self.play(Create(orbit),run_time=.6);self.drop(orbit,core);matrix=self.symbolic_matrix(a,'X');self.put(matrix);self.to(8)
  self.cue(1);self.to(9)
  self.cue(2);waveplot=WellGraph(b,title='1926 · 파동함수 ψ(x)');self.put(waveplot);self.play(Create(waveplot.curve),run_time=.8);self.note('파동 그림은 표현 방식의 비교를 위한 모형 · 전자의 궤적이 아님');self.to(14)
  self.cue(3);self.summary('iℏ ∂ψ/∂t = Hψ',BLUE);self.to(19)
  self.cue(4);self.play(Circumscribe(matrix,color=PURPLE),Circumscribe(waveplot,color=BLUE),run_time=.7);self.to(23)
  self.cue(5);self.note('서로 다른 수학적 출발점이 같은 자연을 설명할 수 있을까?');self.to(26)
class EvidenceDirection(EpisodeScene):
 offset=26
 def construct(self):
  a,b=L.panels
  self.cue(6);left=HydrogenLevels(a);right=HydrogenLevels(b);self.put(left,right);self.pair_titles('행렬역학의 예측','파동역학의 예측');self.note('수소 원자의 비상대론적 에너지 · 미세구조 등은 생략');self.to(31)
  self.cue(7);self.summary('일부 예측의 일치 ≠ 이론 구조의 연결');self.to(36)
  self.cue(8);self.play(Circumscribe(left,color=GOLD),Circumscribe(right,color=GOLD),run_time=.7);self.to(40)
  self.cue(9);self.clear();self.put(self.symbolic_matrix(a),WellGraph(b,title='ψ(x)'));self.to(43)
  self.cue(10);self.summary('행렬 원소와 파동함수 사이의 수학적 관계는?');self.to(47)
class ExpansionDirection(EpisodeScene):
 offset=47
 def construct(self):
  a,b=L.panels
  self.cue(11);plot=WellGraph(a,title='같은 양자상태 ψ(x)');self.put(plot,self.label('1926 · Schrödinger',b,GOLD,size=34));self.note('기저 전개를 설명하는 1차원 무한정사각우물 예시 · 수소 원자 파동함수가 아님');self.to(51)
  self.cue(12);self.drop(self.body[1]);self.to(54)
  self.cue(13);components=VGroup()
  for i,y in enumerate([1.25,.05,-1.15]):
   c=b+p(0,y-.25);component=WellGraph(c,coefficients=np.eye(3)[i]*C[i],title='',width=4.5,height=.72)
   label=text(f'c{i+1} φ{i+1}(x)   ·   E{i+1}={int(ENERGIES[i])}E₁',c[0],c[1]+.52,21,BLUE);components.add(component,label)
  self.put(components);self.play(LaggedStart(*[FadeIn(o) for o in components],lag_ratio=.08),run_time=1);self.summary('ψ(x) = c₁φ₁(x) + c₂φ₂(x) + c₃φ₃(x)',GREEN);self.to(60)
  self.cue(14);self.drop(components);vector=self.vector(b);self.put(vector);self.play(Create(vector),run_time=.7);self.note('설명용 실수 계수 · 일반적으로 계수는 복소수 · |c₁|²+|c₂|²+|c₃|² = 1');self.to(65)
class OperatorsDirection(EpisodeScene):
 offset=65
 def construct(self):
  a,b=L.panels
  self.cue(15);plot=WellGraph(a,title='상태 ψ(x)');operator=self.symbolic_matrix(b);self.put(plot,operator);self.summary('상태의 표현 c     /     물리량의 표현 A',GREEN);self.note('상태를 나타내는 벡터와 상태에 작용하는 연산자 행렬은 서로 다르다');self.to(71)
  self.cue(16);self.clear();nodes=VGroup(*[VGroup(Circle(radius=.3,color=BLUE).move_to(a+p(x,0)),text(f'φ{i+1}',a[0]+x,a[1],23,BLUE)) for i,x in enumerate([-1.8,0,1.8])]);grid=self.symbolic_matrix(b);self.put(nodes,grid)
  self.put(Line(a+p(-1.8,.3),a+p(0,.7),color=GREEN),Line(a+p(0,.7),a+p(1.8,.3),color=GREEN));self.summary('Aₘₙ = 〈φₘ | A | φₙ〉',GREEN);self.note('정규직교 기저 · 입력 n → 출력 m의 계수 · 반드시 실제 전이 사건을 뜻하지 않음');self.to(76)
  self.cue(17);highlight=grid.highlight(0,1);self.put(highlight);self.play(Create(highlight),run_time=.65);self.to(79)
  self.cue(18);self.clear();left=WellGraph(a,coefficients=H@C,title='Hψ(x) / E₁',height=1.7);right=self.vector(b,H@C,label='Hc / E₁');self.put(left,right);self.expectation();self.note('수치 예: H/E₁ = diag(1,4,9) · 연산 결과는 정규화된 새 상태와 구별');self.to(84)
class AlgebraDirection(EpisodeScene):
 offset=84
 def construct(self):
  a,b=L.panels
  self.cue(19);self.put(self.label('연산자의 합성과 곱',a,PURPLE,size=31),self.label('기저에서의 행렬곱',b,BLUE,size=31));self.to(86)
  self.cue(20);self.summary('A(Bψ)  ↔  A(Bc)',GREEN);self.note('완비 기저와 적절한 정의역에서 연산의 대응을 이해한다 · 원소별 곱이 아님');self.to(91)
  self.cue(21);self.clear();self.put(self.label('xψ(x)',a+p(0,.65),BLUE,size=34),self.label('pψ(x) = −iℏ ∂ψ/∂x',a+p(0,-.55),BLUE,size=30),self.label('XP − PX = iℏ I',b,PURPLE,size=35));self.summary('[x, p]ψ = iℏψ',GREEN);self.note('정준교환관계는 전체 연산자의 관계 · 유한 3×3 행렬이 이를 정확히 만족한다는 뜻 아님');self.to(98)
  self.cue(22);self.clear();self.put(WellGraph(a),self.vector(b));self.summary('ψ(x)  ↔  기저 계수 c',GREEN);self.note('1926 · 슈뢰딩거의 연결 · 이후 더 일반적이고 엄밀한 정식화로 발전');self.to(104)
  self.cue(23);ellipse=Ellipse(width=13,height=4.2,color=GREEN,stroke_opacity=.45).move_to(p(0,.2));self.put(ellipse);self.to(109)
class FoundationsDirection(EpisodeScene):
 offset=109
 def construct(self):
  self.cue(24);labels=VGroup(text('일반적인 변환',-4,.5,30,PURPLE),text('연산자와 상태',0,.5,30,BLUE),text('수학적 토대',4,.5,30,GOLD));self.put(labels);self.note('초기의 구조적 연결 발견과 후속 수학적 정식화를 구분한다');self.to(112)
  self.cue(25);self.put(DashedLine(p(-3,-.1),p(3,-.1),color=GREEN));self.to(117)
  self.cue(26);self.clear();left=self.vector(p(-4.7,.1));cp,hp=transformed();right=self.vector(p(4.7,.1),cp,label='c′');self.put(left,right,text('c′ = U†c',0,.35,34,GREEN),text('A′ = U†AU',0,-.65,31,GREEN));self.summary('Dirac · Jordan   /   변환 이론',GREEN);self.note('직교정규 기저 사이의 유니터리 변환 예시 · 역사적 변환 이론의 전체 범위는 아님');self.to(122)
  self.cue(27);self.clear();origin=p(-4,-.65);axes=VGroup(Arrow(origin,origin+p(2.3,0),buff=0,color=MUTED),Arrow(origin,origin+p(0,2),buff=0,color=MUTED),Arrow(origin,origin+p(1.6,1.35),buff=0,color=GOLD));self.put(axes,text('Hilbert Space',3.4,.5,37,GOLD),text('폰 노이만 · 수학적 토대의 정리',3.4,-.4,28,INK,width=7));self.note('추상 상태공간의 개념적 투영 · 실제 공간의 2차원이나 3차원으로 한정하지 않음');self.to(128)
  self.cue(28);self.clear();self.put(Circle(radius=1.0,color=GREEN),text('|ψ〉',0,0,42,INK),text('ψ(x)',-4,0,40,BLUE),text('c',4,0,40,PURPLE),DoubleArrow(p(-2.8,0),p(-1.2,0),buff=0,color=GREEN),DoubleArrow(p(1.2,0),p(2.8,0),buff=0,color=GREEN));self.summary('하나의 상태 · 서로 다른 표현');self.to(136)
class BasisDirection(EpisodeScene):
 offset=136
 def construct(self):
  a,b=L.panels
  self.cue(29);plot=WellGraph(a,title='같은 ψ(x)');vector=self.vector(p(1.9,.25));hm=MatrixGrid(p(5.35,.25),[[f'{v:.2f}' for v in row] for row in H],cell=.72,label='H / E₁',indices=False,size=20,symbolic=False);self.put(plot,vector,hm);self.summary('기저가 바뀌면 계수와 행렬을 함께 바꾼다',GREEN);self.note('1차원 우물의 세 에너지 상태로 만든 예시 · 파동함수는 그대로 유지');self.to(141)
  self.cue(30);cp,hp=transformed();self.play(Transform(vector,self.vector(p(1.9,.25),cp,label='c′')),Transform(hm,MatrixGrid(p(5.35,.25),[[f'{v:.2f}' for v in row] for row in hp],cell=.72,label='H′ / E₁',indices=False,size=20,symbolic=False)),run_time=1.2);self.note('U†U = I · H′ = U†HU · 〈H〉 = c†Hc = c′†H′c′');self.expectation(True);self.play(Circumscribe(plot,color=GREEN),run_time=.6);self.to(149)
class OriginsDirection(EpisodeScene):
 offset=149
 def construct(self):
  from quantum_series.shared.components import distribution
  from quantum_series.shared.franck_hertz import Levels as MercuryLevels
  a,b=L.panels
  self.cue(31);self.put(text('1900',-4,.3,48,GOLD),text('여러 현상에서 시작된 발견',2,.3,33,INK));self.note('최종화 회고 · 초기 발견은 1900–1927년, 후속 정식화는 이후의 발전');self.to(151)
  self.cue(32);self.clear();ax=Axes(x_range=[0,12,3],y_range=[0,1.1,.5],x_length=5.4,y_length=2.1,tips=False).move_to(a);curve=ax.plot(lambda x:distribution(x),x_range=[.3,12,.04],color=GOLD);blocks=VGroup(*[RoundedRectangle(width=.6,height=.45,corner_radius=.05,color=GOLD,fill_opacity=.25).move_to(b+p(x,0)) for x in [-1.3,-.45,.45,1.3]]);self.put(ax,curve,blocks,self.label('흑체복사 스펙트럼',a+p(0,1.6),size=26),self.label('ε = hν',b+p(0,1.3),GOLD,size=37));self.play(Create(curve),run_time=.75);self.note('T = 1500 K의 이론적 흑체복사 분포 · 에너지 단위는 개념도');self.to(156)
  self.cue(33);self.clear();metal=Rectangle(width=4.3,height=.4,color=MUTED,fill_opacity=.3).move_to(a);light=Arrow(a+p(-1.4,1.5),a+p(0,.3),buff=0,color=GOLD);electron=Dot(a+p(.4,.7),color=BLUE,radius=.08);self.put(metal,light,electron,self.label('광전효과',a+p(0,-1.1),size=29),self.label('빛의 양자 · E = hν',b,GOLD,size=36));self.play(electron.animate.shift(p(.9,.6)),run_time=.7);self.note('광전효과의 개념도 · 물체와 빛 사이의 에너지 전달');self.to(161)
  self.cue(34);self.clear();nucleus=Dot(a,color=ORANGE,radius=.13);self.put(nucleus,Circle(radius=1.4,color=MUTED).move_to(a),Arrow(a+p(-2.4,.25),a+p(-.3,.25),color=GOLD,buff=0),Arrow(a+p(-.3,.25),a+p(-1.7,1.2),color=GOLD,buff=0),HydrogenLevels(b));self.put(self.label('원자핵',a+p(0,-1.8),ORANGE),self.label('불연속 에너지 준위',b+p(0,-1.8),GOLD));self.note('원자핵 산란과 수소 에너지 준위의 개념도 · 축척과 미세구조는 생략');self.to(169)
  self.cue(35);self.clear();levels=MercuryLevels(a,width=4);atom=Circle(radius=.65,color=ORANGE).move_to(b);incident=Dot(b+p(-2.2,0),color=BLUE,radius=.08);self.put(levels,atom,incident,self.label('수은의 특정한 들뜸 에너지',b+p(0,1.3),ORANGE,size=27));self.play(incident.animate.move_to(b+p(-.7,0)),run_time=.6);self.play(levels.marker.animate.move_to(levels.high),run_time=.6);self.note('수은의 바닥상태와 들뜬 상태 · 충돌로 흡수하는 에너지 약 4.9 eV');self.to(175)
class WavesDirection(EpisodeScene):
 offset=175
 def construct(self):
  from quantum_series.shared.diffraction import electron_wavelength_nm
  from quantum_series.shared.uncertainty import density
  from quantum_series.shared.complementarity import probability
  a,b=L.panels
  self.cue(36);self.put(packet(a),lattice(b),self.label('드브로이 · λ = h / p',a+p(0,1.6),BLUE,size=30),self.label('전자 회절',b+p(0,1.6),GOLD,size=30));self.summary(f'54 V 전자의 파장 ≈ {electron_wavelength_nm(54):.3f} nm');self.note('54 V에서 계산한 드브로이 파장 · 격자와 파동은 개념적 요약');self.to(181)
  self.cue(37);self.clear();self.put(self.symbolic_matrix(a),WellGraph(b));self.summary('행렬과 파동으로 구축된 새로운 역학',GREEN);self.to(186)
  self.cue(38);self.clear()
  for c,title,kind in [(p(-4.8,.4),'보른 · 확률',0),(p(0,.4),'불확정성',1),(p(4.8,.4),'상보성',2)]:
   ax=Axes(x_range=[-3,3,1],y_range=[0,1,.5],x_length=3.5,y_length=1.5,tips=False,axis_config={'color':MUTED,'stroke_width':1}).move_to(c)
   curve=ax.plot((lambda x:float(density(x,.7))) if kind<2 else (lambda x:float(probability(x,1))),x_range=[-3,3,.03],color=GREEN if kind<2 else PURPLE)
   self.put(ax,curve,self.label(title,c+p(0,1.35),size=25,width=4))
   if kind==1:self.put(ax.plot(lambda x:float(density(x,1.2)),x_range=[-3,3,.03],color=GOLD))
  self.note('확률밀도 · 위치와 운동량의 폭 · 두 경로 간섭을 요약한 모형');self.to(194)
class QuestionsDirection(EpisodeScene):
 offset=194
 def construct(self):
  self.cue(39);self.note('열복사 · 원자의 구조와 안정성 · 전자의 파동성, 서로 다른 출발점');self.put(text('하나의 질문에서 시작된 것은 아니었다',0,.2,37,INK));self.to(197)
  self.cue(40);self.clear();self.nodes=[p(-4.8,1.1),p(-4.8,-1.0),p(4.8,.1)]
  for c,s in zip(self.nodes,['빛의 색','원자의 안정성','전자의 움직임']):self.put(RoundedRectangle(width=3.2,height=.9,corner_radius=.14,color=MUTED).move_to(c),self.label(s,c,size=27,width=3))
  self.to(203)
  self.cue(41);center=p(0,.1);self.put(Circle(radius=1.05,color=GREEN).move_to(center),text('양자역학',0,.1,31,GREEN))
  for c in self.nodes:
   delta=center-c;start=c+delta/np.linalg.norm(delta)*1.7;end=center-delta/np.linalg.norm(delta)*1.15;arrow=Arrow(start,end,buff=0,color=GREEN);self.put(arrow);self.play(Create(arrow),run_time=.35)
  self.to(207)
class ConclusionDirection(EpisodeScene):
 offset=207
 def construct(self):
  self.cue(42);self.put(text('고전역학의 설명이 닿지 못한 현상들',0,1.1,35,INK),text('빛  ·  원자  ·  전자',0,-.2,40,GOLD));self.note('서로 다른 문제의 해결이 새로운 이론의 구조로 연결되었다');self.to(213)
  self.cue(43);self.clear();self.put(text('현대 양자역학',0,.3,51,GREEN),text('자연의 한계를 이해하려는 시도에서',0,-1,29,INK));self.to(217)
  self.cue(44);self.clear()
  if self.foot:self.remove(self.foot)
  self.put(text('1900 — 1927',0,1.55,29,GOLD),text('양자역학의 발견',0,.35,58,INK),text('PART I · THE BIRTH OF QUANTUM MECHANICS',0,-.7,24,MUTED,width=13),text('END OF PART I',0,-1.65,24,GOLD));self.to(221)
