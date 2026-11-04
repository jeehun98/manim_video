"""163s synthesis; independent scene clocks, single global subtitle pass."""
import json,os,importlib.util
from pathlib import Path
import numpy as np
from manim import *
ROOT=Path(__file__).resolve().parent
os.environ['MINIMAL_LAYOUT']='longform'
spec=importlib.util.spec_from_file_location('lottery_visual_reuse',ROOT.parent/'minimal07_lottery/scene_engine.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
config.frame_width=16;config.frame_height=9;config.background_color='#0B1423'
INK=old.INK;MUTED=old.MUTED;TEAL=old.TEAL;YELLOW=old.YELLOW;BLUE=old.BLUE;PINK=old.PINK;PURPLE=old.PURPLE;EDGE=old.EDGE
txt=old.txt;box=old.box;network=old.network
MANIFEST=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
NAMES=['그래프','최소 유전체','충분통계량','최소 실현','보편성','복권 가설']
GOALS=['연결성 · 구조적 성질','특정 환경에서의 생존','모수 추론 정보','외부 입출력 관계','임계 스케일링 법칙','조건부 학습 성능']
EP=[3,2,4,5,6,7]
def graph(edges=None,center=ORIGIN,radius=1.65):
 ps=[np.array([np.cos(i*TAU/8)*radius,np.sin(i*TAU/8)*radius,0]) for i in range(8)]
 if edges is None:edges=[(i,j) for i in range(8) for j in range(i+1,8)]
 return VGroup(VGroup(*[Line(ps[a],ps[b],color=TEAL,stroke_width=2.2) for a,b in edges]),VGroup(*[Dot(p,radius=.075,color=YELLOW) for p in ps])).move_to(center)
def curve(ax,fun,color):return ax.plot(fun,x_range=[0,6],color=color,stroke_width=4)
def axes(center,width=5,height=1.7):return Axes(x_range=[0,6,2],y_range=[0,2,1],x_length=width,y_length=height,tips=False,axis_config={'include_ticks':False,'color':EDGE}).move_to(center)
class FinaleScene(Scene):
 index=0
 def at(self,t):
  remain=t-self.start-self.time
  if remain<-.08:raise RuntimeError((self.index,self.time,t))
  if remain>.001:self.wait(remain)
 def note(self,s,color=YELLOW):self.notice.become(txt(s,25,color,14).move_to([0,-2.2,0]))
 def cond(self,s):self.condition.become(box(s,13.3,.6,YELLOW,24).move_to([0,2.5,0]))
 def construct(self):
  m=MANIFEST[self.index];self.start=m['start'];self.add(txt('모든 것이 필요할까?  /  01–07 통합 마무리',19,MUTED).move_to([0,4.05,0]),txt(m['title'],35,INK,14).move_to([0,3.4,0]),Line([-7,2.96,0],[7,2.96,0],color=EDGE))
  self.notice=VGroup(VectorizedPoint());self.condition=VGroup(VectorizedPoint());self.add(self.notice,self.condition)
  track=Line([-7,-4.1,0],[7,-4.1,0],color=EDGE);progress=Line([-7,-4.1,0],[-6.999,-4.1,0],color=YELLOW,stroke_width=3)
  progress.add_updater(lambda p:p.put_start_and_end_on(track.get_start(),track.get_start()+RIGHT*14*max(.0001,min(1,(self.start+self.time)/163))))
  self.add(track,progress);getattr(self,f'part{self.index:02}')();self.at(m['end'])
 def part00(self):
  cards=Group(*[Group(ImageMobject(str(ROOT/f'assets/ep{ep:02}.png')).set_width(3.6),txt(n,23,TEAL).shift(DOWN*.9)) for ep,n in zip(EP,NAMES)]).arrange_in_grid(rows=2,cols=3,buff=(.4,.6)).move_to([0,.2,0]);self.play(FadeIn(cards),run_time=.8)
  self.at(4);self.play(cards.animate.scale(.65).set_opacity(.25),FadeIn(box('모든 것이 정말 필요할까?',12,1.2,YELLOW,40).move_to([0,.2,0])),run_time=1)
 def part01(self):
  self.cond('보존 조건을 먼저 선택한다');g=graph(center=[-3.6,.15,0]);self.add(g)
  tree=[(i,i+1) for i in range(7)];h=graph(tree,center=[3.6,.15,0]);self.add(txt('원래 그래프',25,MUTED).move_to([-3.6,2,0]),txt('연결성만 유지',25,TEAL).move_to([3.6,2,0]));self.play(TransformFromCopy(g,h),run_time=3)
  self.note('8개 정점 · 트리의 7개 간선으로 모두 연결')
  self.at(16);self.note('최단거리: 직접 1개 간선 → 우회 7개 간선',YELLOW)
  direct=Line(g[1][0].get_center(),g[1][7].get_center(),color=YELLOW,stroke_width=7);path=VGroup(*[Line(h[1][i].get_center(),h[1][i+1].get_center(),color=YELLOW,stroke_width=6) for i in range(7)])
  self.play(Create(direct),Create(path),run_time=1.4)
  self.at(19);self.cond('연결성 보존 ≠ 최단거리 보존')
 def part02(self):
  self.cond('같은 유전자 제거 · 다른 생존 조건')
  genes=VGroup(*[box(chr(65+i),.8,.65,TEAL,25) for i in range(9)]).arrange(RIGHT,buff=.12).move_to([0,1.5,0]);self.add(genes)
  self.at(26);self.play(genes[3].animate.set_opacity(.15),run_time=.6)
  self.add(box('환경 A · 영양분 공급\n생존 가능',6,1.45,TEAL,30).move_to([-3.4,-.4,0]),box('환경 B · 직접 합성 필요\n생존 불가',6,1.45,MUTED,30).move_to([3.4,-.4,0]));self.note('필수성은 다른 유전자와 환경에 의존한다')
 def part03(self):
  self.cond('독립·동일 정규분포 / 알려진 동일 분산 / 고정 n / 평균 μ 추론')
  a=box('1, 2, 3, 4, 5',6,.8,BLUE,31).move_to([-3.5,1.1,0]);b=box('0, 0, 3, 6, 6',6,.8,BLUE,31).move_to([3.5,1.1,0]);self.add(a,b)
  out=box('표본평균 x̄ = 3',7,1.2,TEAL,40).move_to([0,-.4,0]);self.play(TransformFromCopy(VGroup(a,b),out),run_time=2);self.note('원본 복원은 불가 · μ에 대한 상대 우도 정보는 동일')
 def part04(self):
  self.cond('ż = −z + 2u · y = z / 대응 초기값과 같은 입력')
  pair=VGroup(box('x₁',2,.8,BLUE),box('x₂',2,.8,BLUE)).arrange(RIGHT).move_to([-3.7,1.3,0]);self.add(pair)
  self.play(TransformFromCopy(pair,box('z = x₁ + x₂',5,.8,TEAL,30).move_to([3.5,1.3,0])),run_time=1)
  ax=axes([0,-.5,0],10,1.8);self.add(ax);self.play(Create(curve(ax,lambda t:1.7*(1-np.exp(-t)),INK)),run_time=1);self.play(Create(curve(ax,lambda t:1.7*(1-np.exp(-t)),TEAL)),run_time=1);self.note('같은 입력 → 같은 출력 · 내부 상태 전체의 복원은 아님')
 def part05(self):
  self.cond('같은 보편성 부류 · 임계점 근방의 점근적 법칙')
  ims=Group(*[ImageMobject(str(ROOT/'assets/ep06.png')).set_width(5).move_to([x,.3,0]) for x in [-3.6,3.6]])
  # Distinct schematic microstructures, not identical microscopic models.
  rng=np.random.default_rng(6);liquid=VGroup(*[Dot([rng.uniform(-2.1,2.1),rng.uniform(-1,1),0],radius=.04,color=BLUE) for _ in range(110)]).move_to([-3.6,.5,0]);spins=VGroup(*[Arrow([j*.35,i*.35,0],[j*.35,i*.35+.22*(1 if rng.random()>.5 else -1),0],buff=0,color=TEAL,stroke_width=2,max_tip_length_to_length_ratio=.3) for i in range(6) for j in range(10)]).move_to([3.6,.5,0]);self.add(liquid,spins,txt('액체 · 기체',26,BLUE).move_to([-3.6,1.95,0]),txt('자석',26,TEAL).move_to([3.6,1.95,0]))
  self.play(liquid.animate.set_opacity(.3),spins.animate.set_opacity(.3),FadeIn(box('공통 임계 지수 β',8,.85,YELLOW,34).move_to([0,-1.1,0])),run_time=1.5);self.note('미시적 세부 정보 전체를 보존하는 것은 아니다')
 def part06(self):
  self.cond('07편 설명용 XOR 실험 재사용 · 원논문 정량 재현 아님')
  g=network(width=5.5,height=2.4,center=[-3.7,.4,0]);self.add(g)
  self.play(Transform(g,network(old.D['trained'],old.MASK,TEAL,5.5,2.4,[-3.7,.4,0],True)),run_time=1.3)
  self.at(59);self.add(txt('선택 → 원래 초기값 복원 → 재학습',25,YELLOW,6.5).move_to([3.4,1.9,0]));self.play(Transform(g,network(old.D['initial'],old.MASK,TEAL,5.5,2.4,[-3.7,.4,0])),run_time=.6)
  base,ax,curves=old.chart_pair(center=[3.3,.3,0],width=5.1,height=1.6);self.add(base);self.play(Create(curves[0]),Create(curves[1]),run_time=1);self.note('Winning Ticket · 성능과 학습 조건을 비교 · 함수 전체 동일성은 아님')
 def part07(self):
  self.cond('모두 같은 것을 보존하는 것은 아니다')
  cards=VGroup();goals=VGroup()
  for i,(name,goal) in enumerate(zip(NAMES,GOALS)):
   row,col=divmod(i,3);p=np.array([(col-1)*4.55,1.05-row*2.05,0]);a=box(name,4.2,.65,MUTED,27).move_to(p+UP*.42);b=box(goal,4.2,.85,TEAL,27).move_to(p+DOWN*.45);cards.add(a);goals.add(b)
  self.play(FadeIn(cards),run_time=.7);self.note('표현 · 구조 · 기술 방식을 줄여도, 비교 기준은 다르다')
  self.at(67);self.play(FadeIn(goals),run_time=1)
  self.at(71);self.note('그래프 · 생명 · 통계의 보존 조건',TEAL)
  self.play(Indicate(VGroup(*goals[:3]),color=YELLOW),run_time=1)
  self.at(80);self.note('제어 · 물리 · 신경망의 보존 조건',TEAL);self.play(Indicate(VGroup(*goals[3:]),color=YELLOW),run_time=1)
  self.at(84);self.play(cards.animate.set_opacity(.2),run_time=.6);self.note('무엇을 보존하는가?',YELLOW)
 def part08(self):
  self.cond('공통된 탐구 방식 / 모든 분야에 같은 축소 정리를 적용하는 것은 아님')
  g=graph(center=[-3.5,.3,0]);self.add(g,box('유지하려는 결과',6,1.1,TEAL,34).move_to([3.4,.4,0]));self.note('어떤 부분이 필요한지는 보존 조건과 함께 판단한다')
  self.at(90);self.play(Transform(g,graph([(i,i+1) for i in range(7)],center=[-3.5,.3,0])),run_time=2)
  self.at(96);self.cond('같은 요소도 · 다른 조건에서는 필요할 수 있다')
  self.at(100);self.note('무엇을 유지할 것인가?',YELLOW)
 def part09(self):
  self.cond('예시 조건: 8개 정점의 연결성 보존')
  tree=[(i,i+1) for i in range(7)];extra=[(0,3),(2,6)]
  g=graph(tree+extra,center=[-3.3,.2,0]);self.add(g);status=box('9개 간선 · 축소된 구조',6,1.2,TEAL,32).move_to([3.4,.3,0]);self.add(status)
  self.note('이미 줄였다는 사실만으로 최소임을 알 수 없다')
  self.at(107);self.play(Transform(g,graph(tree+[extra[0]],center=[-3.3,.2,0])),run_time=1);status.become(box('8개 간선 · 더 줄일 수 있다',6,1.2,YELLOW,30).move_to(status))
  self.at(109);self.cond('줄일 수 있다 ≠ 더 줄일 수 없다')
  self.at(115);self.play(Transform(g,graph(tree,center=[-3.3,.2,0])),run_time=1);status.become(box('7개 간선 · 연결성 유지',6,1.2,TEAL,32).move_to(status));self.note('이 조건에서는 n−1개가 하한 · 다른 보존 조건은 별도 문제')
 def part10(self):
  self.cond('보존 기준에 따라 정확한 동등성 또는 허용 오차를 정의')
  for x,label,c,offset in [(-3.6,'Exact',TEAL,0),(3.6,'Approximate',YELLOW,.12)]:
   ax=axes([x,.2,0],5.8,2.3);self.add(ax,txt(label,30,c).move_to([x,1.95,0]));f=lambda t:1+np.sin(t)*.5;self.add(curve(ax,f,INK));self.play(Create(curve(ax,lambda t:f(t)+offset*np.cos(t*2),c)),run_time=.8)
  self.note('설명용 곡선 · 근사 보존에는 오차 기준이 필요하다')
 def part11(self):
  qs=['무엇을 같은 것으로 볼 것인가?','어디까지 줄일 수 있는가?','더 이상 줄일 수 없음을 증명할 수 있는가?']
  for i,q in enumerate(qs):
   self.play(FadeIn(box(q,12,1,YELLOW if i==0 else TEAL,32).move_to([0,1.5-i*1.3,0])),run_time=.7)
   if i<2:self.at(131 if i==0 else 134)
  self.note('보존 기준 → 후보 탐색 → 최소성의 증명')
 def part12(self):
  self.cond('조건부 성능 보존과 완전한 함수 동등성은 서로 다른 질문')
  g=network(width=9,height=3,center=[0,.3,0]);self.play(Create(g),run_time=1.3)
  self.at(139);self.play(Transform(g,network(old.D['trained'],old.MASK,TEAL,9,3,[0,.3,0],True)),run_time=1);self.note('연결 수를 줄일 수 있는 경우가 있다')
  self.at(143);self.note('연결의 개수보다 먼저, 표현의 동등성을 물을 수 있을까?',YELLOW)
 def part13(self):
  self.cond('파라미터가 다르다는 것은 · 함수도 다르다는 뜻일까?')
  # Two colored neuron bundles use different vertical positions; no pruning implied.
  def net(swap=False):
   left=np.array([-2,0,0]);right=np.array([2,0,0]);out=VGroup()
   for j,(label,color) in enumerate([('A',BLUE),('B',PURPLE)]):
    y=(.8 if j==0 else -.8)*(-1 if swap else 1);p=np.array([0,y,0]);out.add(Line(left,p,color=color),Line(p,right,color=color),Dot(p,radius=.16,color=color),txt(label,24,color).move_to(p+UP*.32))
   out.add(Dot(left,color=INK),Dot(right,color=INK));return out
  a=net().move_to([-3.7,.4,0]);b=net(True).move_to([3.7,.4,0]);self.add(a,b,txt('파라미터 θ',26,BLUE).move_to([-3.7,2,0]),txt('파라미터 θ′',26,PURPLE).move_to([3.7,2,0]));self.add(txt('θ = [(2, 1, 3), (−1, 2, −2)]',19,BLUE).move_to([-3.7,-.72,0]),txt('θ′ = [(−1, 2, −2), (2, 1, 3)]',19,PURPLE).move_to([3.7,-.72,0]));self.note('같은 아키텍처 · 다른 파라미터 배열',MUTED)
  self.at(150)
  for value in ['−1','0','1']:
   inp=txt('x = '+value,28,YELLOW).move_to([0,1.3,0]);self.play(FadeIn(inp),run_time=.2);self.play(Indicate(a),Indicate(b),run_time=.4);self.remove(inp)
  self.at(152);self.add(box('모든 x에 대해 fθ(x) = fθ′(x) ?',12,.7,YELLOW,32).move_to([0,-1.45,0]));self.note('몇 개 입력의 일치만으로는 · 모든 입력의 동일성을 증명할 수 없다',MUTED)
  self.at(156);self.cond('다른 파라미터, 같은 함수?');self.note('서로 다른 배열과 · 서로 다른 함수를 구별할 수 있을까?',YELLOW)
