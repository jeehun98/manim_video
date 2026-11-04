"""Computed block spins, schematic effective-theory flow, and conditional universality."""
import json,os
from pathlib import Path
import numpy as np
from manim import *
ROOT=Path(__file__).resolve().parent
D=np.load(ROOT/'simulation_data.npz')
VERT=os.getenv('MINIMAL_LAYOUT','shorts')=='shorts'
config.frame_width=9 if VERT else 16;config.frame_height=16 if VERT else 9;config.background_color='#0B1423'
INK='#EDF3FA';MUTED='#8B9DB5';TEAL='#42D7BD';RED='#FF6B98';YELLOW='#F3D277';PURPLE='#B89CFF';PANEL='#152338';EDGE='#2B3E57'
MANIFEST=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
def txt(s,size=30,color=INK,width=None):
 m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.12)
 if width and m.width>width:m.scale_to_fit_width(width)
 return m

def box(s,width=6,height=1,color=YELLOW,size=30):return VGroup(RoundedRectangle(width=width,height=height,corner_radius=.13,color=color,stroke_width=1.5,fill_color=PANEL,fill_opacity=1),txt(s,size,color,width-.35))

def lattice(s,width=5.8,center=ORIGIN,block=False):
 n=len(s);cell=width/n;fills=[VMobject(stroke_width=0,fill_color=c,fill_opacity=.2) for c in [TEAL,RED]];arrows=[VMobject(color=YELLOW if block else c,stroke_width=2 if n<=8 else 1.5) for c in [TEAL,RED]]
 for i in range(n):
  for j in range(n):
   c=np.array([(j-(n-1)/2)*cell,((n-1)/2-i)*cell,0]);v=int(s[i,j]);k=0 if v>0 else 1
   fills[k].append_vectorized_mobject(Square(side_length=cell*.94,stroke_width=0).move_to(c))
   tail=c+DOWN*v*cell*.28;tip=c+UP*v*cell*.28;h1=tip+DOWN*v*cell*.16+LEFT*cell*.14;h2=tip+DOWN*v*cell*.16+RIGHT*cell*.14
   arrows[k].start_new_path(tail);arrows[k].add_points_as_corners([tip,h1,tip,h2])
 return VGroup(*fills,*arrows).move_to(center)

def boundaries(width=5.8,center=ORIGIN):
 v=VMobject(color=YELLOW,stroke_width=1.5)
 for i in range(9):
  x=-width/2+width*i/8;v.start_new_path(np.array([x,-width/2,0]));v.add_line_to(np.array([x,width/2,0]));v.start_new_path(np.array([-width/2,x,0]));v.add_line_to(np.array([width/2,x,0]))
 return v.move_to(center)

def coupling_edges(n,width,center,extra=False):
 c=np.array(center);cell=width/n;out=VMobject(color=PURPLE,stroke_width=1.5,stroke_opacity=.55).set_z_index(-1)
 def pt(i,j):return c+np.array([(j-(n-1)/2)*cell,((n-1)/2-i)*cell,0])
 for i in range(n):
  for j in range(n):
   for di,dj in ([(1,0),(0,1),(1,1)] if extra else [(1,0),(0,1)]):
    if i+di<n and j+dj<n:
     a=pt(i,j);b=pt(i+di,j+dj);delta=b-a;out.start_new_path(a+delta*.25);out.add_line_to(b-delta*.25)
 return out

def fluid(width=3.6,height=3.3,mixed=False):
 rng=np.random.default_rng(19);out=VGroup(RoundedRectangle(width=width,height=height,corner_radius=.12,color=TEAL,fill_color=PANEL,fill_opacity=.5,stroke_width=1.5))
 for k in range(52):
  x=rng.uniform(-width*.43,width*.43);y=rng.uniform(-height*.43,height*.43) if mixed else rng.uniform(-height*.43,-.05) if k<42 else rng.uniform(.25,height*.43)
  out.add(Dot([x,y,0],radius=.045,color=TEAL))
 if not mixed:out.add(DashedLine([-width/2,0,0],[width/2,0,0],color=MUTED,dash_length=.1,stroke_width=1))
 return out

def material_pair():
 ca,cb=([0,2.2,0],[0,-1.15,0]) if VERT else ([-3.7,.2,0],[3.7,.2,0])
 a=fluid(3.5,2.25 if VERT else 2.7).move_to(ca);b=lattice(D['critical'][0][:8,:8],2.25 if VERT else 2.7,cb)
 labels=VGroup(txt('액체 · 기체',27,TEAL).move_to(np.array(ca)+UP*(1.45 if VERT else 1.7)),txt('자석',27,RED).move_to(np.array(cb)+UP*(1.45 if VERT else 1.7)))
 return VGroup(a,b,labels)

def scaling(center,width=3.9,height=2.4,color=TEAL,amplitude=1):
 ax=Axes(x_range=[0,1,1],y_range=[0,1.2,1],x_length=width,y_length=height,tips=False,axis_config={'include_ticks':False,'color':EDGE,'stroke_width':1.4}).move_to(center)
 xs=np.linspace(0,1,151);c=VMobject(color=color,stroke_width=4).set_points_as_corners([ax.c2p(x,amplitude*x**.33) for x in xs])
 labels=VGroup(txt('0',18,MUTED).move_to(ax.c2p(0,0)+DOWN*.22),txt('ε',23,MUTED).move_to(ax.c2p(1,0)+RIGHT*.2))
 return VGroup(ax,c,labels)

def scaling_pair():
 ca,cb=([0,2,0],[0,-.9,0]) if VERT else ([-3.6,.3,0],[3.6,.3,0]);w,h=(5.5,1.8) if VERT else (5.3,2.3)
 a=scaling(ca,w,h,TEAL,1);b=scaling(cb,w,h,RED,.72)
 labs=VGroup(txt('밀도 차이 Δρ',25,TEAL).move_to(np.array(ca)+UP*(1.25 if VERT else 1.55)),txt('자화 크기 M',25,RED).move_to(np.array(cb)+UP*(1.25 if VERT else 1.55)))
 return VGroup(a,b,labs)

def flow_axes():
 center=[0,.6,0] if VERT else [-3.4,.1,0];w,h=(6,4.5) if VERT else (5.7,3)
 ax=Axes(x_range=[-1.2,1.2,1],y_range=[-1,1,1],x_length=w,y_length=h,tips=False,axis_config={'include_ticks':False,'color':EDGE,'stroke_width':1.5}).move_to(center)
 labels=VGroup(txt('r · 관련 방향',21,RED).move_to(ax.c2p(1,0)+DOWN*.3),txt('g · 무관 방향',21,TEAL).move_to(ax.c2p(0,1)+UP*.2))
 critical=DashedLine(ax.c2p(0,-.95),ax.c2p(0,.95),color=PURPLE,dash_length=.1,stroke_width=2)
 fixed=Dot(ax.c2p(0,0),color=PURPLE,radius=.11)
 return VGroup(ax,labels,critical,fixed),ax

class UniversalityScene(Scene):
 index=0
 def at(self,t):
  target=t-self.start
  if self.time>target+.075:raise RuntimeError((self.index,self.time,target))
  if target-self.time>.001:self.wait(target-self.time)
 def note(self,s,color=YELLOW):self.notice.become(txt(s,27 if VERT else 25,color,7.15 if VERT else 13.5).move_to([0,-3.55 if VERT else -1.95,0]))
 def condition(self,s):self.cond.become(box(s,7 if VERT else 12,.75,YELLOW,24).move_to([0,4.45 if VERT else 2.5,0]))
 def construct(self):
  m=MANIFEST[self.index];self.start=m['start'];self.end=m['end']
  self.add(txt('모든 것이 필요할까?   /   06',20,MUTED).move_to([0,7.05 if VERT else 4.02,0]),txt(m['title'],38 if VERT else 35,INK,7.1 if VERT else 14).move_to([0,6.05 if VERT else 3.35,0]),Line([-3.55 if VERT else -7,5.35 if VERT else 2.88,0],[3.55 if VERT else 7,5.35 if VERT else 2.88,0],color=EDGE,stroke_width=1))
  self.cond=VGroup(VectorizedPoint());self.notice=VGroup(VectorizedPoint());self.add(self.cond,self.notice)
  track=Line([-3.55 if VERT else -7,-6.95 if VERT else -4.08,0],[3.55 if VERT else 7,-6.95 if VERT else -4.08,0],color=EDGE,stroke_width=2);progress=Line(track.get_start(),track.get_start()+RIGHT*.001,color=YELLOW,stroke_width=3)
  progress.add_updater(lambda p:p.put_start_and_end_on(track.get_start(),track.get_start()+RIGHT*track.width*max(.0001,min(1,(self.start+self.time)/160))))
  self.add(track,progress);getattr(self,f'part_{self.index:02}')();self.at(self.end)
 def part_00(self):
  self.condition('서로 다른 미시 구조 · 같은 거시 법칙?')
  pair=material_pair();self.play(FadeIn(pair),run_time=.7);self.note('입자와 상호작용은 서로 다르다',MUTED)
  self.at(8);self.note('어떻게 같은 법칙이 나타날까?',YELLOW)
 def part_01(self):
  self.condition('유체: 온도와 압력을 함께 조절해 임계점에 접근')
  ca,cb=([0,2.15,0],[0,-1.15,0]) if VERT else ([-3.7,.2,0],[3.7,.2,0])
  f=fluid(3.6,2.4).move_to(ca);g=lattice(D['low'][0][:8,:8],2.4,cb);self.add(f,g)
  self.add(txt('액체 · 기체',25,TEAL).move_to(np.array(ca)+UP*1.5),txt('자석',25,RED).move_to(np.array(cb)+UP*1.5));self.note('상전이의 개념도 · 온도만으로 모든 조건이 정해지지 않음',MUTED)
  self.play(Transform(f,fluid(3.6,2.4,True).move_to(ca)),run_time=3)
  self.at(15);self.play(Transform(g,lattice(D['high'][0][:8,:8],2.4,cb)),run_time=2);self.note('액체·기체의 구분 소멸 / 자화 소멸',YELLOW)
  self.at(19);self.condition('서로 다른 현상에 나타나는 임계점 · Critical Point')
 def part_02(self):
  self.condition('같은 보편성 부류에 속하는 조건에서')
  pair=scaling_pair();self.add(pair);self.note('ε = (Tc − T) / Tc → 0 · 임계점 접근',MUTED)
  self.at(28)
  eq=box('Δρ ∝ εᵝ      M ∝ εᵝ',7 if VERT else 12,.8,YELLOW,33).move_to([0,-2.7 if VERT else -1.25,0]);self.play(FadeIn(eq),run_time=.7);self.note('공통인 것은 임계 지수 β · 그래프는 설명용')
  self.at(34);self.note('구조가 다른데 왜 같은 임계 지수가 나타날까?')
 def part_03(self):
  self.condition('2D Ising 모형 · ↑ 또는 ↓ · 가까운 이웃 상호작용')
  g=lattice(D['level0'],5.7,[0,.65 if VERT else .1,0]);
  if not VERT:g.scale(.58).shift(LEFT*3.3)
  self.play(FadeIn(g),run_time=.8);self.note('청록 ↑ · 분홍 ↓',MUTED)
  self.at(42);eq=box('sᵢ = +1 또는 −1\nH = −J Σ sᵢsⱼ',7 if VERT else 6,.9 if VERT else 1.1,TEAL,26 if VERT else 29).move_to([0,-2.75,0] if VERT else [3.5,.5,0]);self.play(FadeIn(eq),run_time=.8);self.note('이웃이 같은 방향이면 에너지가 낮아진다',TEAL)
 def part_04(self):
  self.condition('낮은 온도 · 2D Ising Monte Carlo 표본')
  center=[0,.65 if VERT else .1,0];w=5.8 if VERT else 3.4;g=lattice(D['low'][0],w,center);self.add(g);self.note('낮은 온도: 대부분 같은 방향으로 정렬',TEAL)
  self.at(51);self.condition('높은 온도 · 열적 요동')
  self.play(Transform(g,lattice(D['high'][0],w,center)),run_time=1)
  self.play(Transform(g,lattice(D['high'][1],w,center)),run_time=1);self.note('고온: 불규칙한 배열',RED)
  self.at(56);self.condition('임계점 부근 · 실제 상관된 표본 · 유한 격자')
  self.play(Transform(g,lattice(D['level0'],w,center)),run_time=1.2);self.note('작은 집단과 큰 집단이 함께 나타난다',YELLOW)
 def part_05(self):
  self.condition('2 × 2 블록 다수결 · 동률은 공정 추첨')
  w=5.8 if VERT else 3.5;center=[0,.65 if VERT else .1,0];g=lattice(D['level0'],w,center);self.add(g);self.note('16 × 16개의 개별 스핀',MUTED)
  self.at(64);b=boundaries(w,center);self.play(Create(b),run_time=1.3);self.note('네 스핀을 하나의 블록으로 묶는다')
  self.at(71);new=lattice(D['level1'],w,center,True);self.play(FadeOut(b),ReplacementTransform(g,new),run_time=1.7);self.note('16 × 16 → 8 × 8 · 각 블록의 대표 방향',YELLOW)
 def part_06(self):
  self.condition('블록화 + 길이 재척도화 + 유효 상호작용 변화')
  c=np.array([0,1.7,0] if VERT else [-3.6,.3,0]);w=3.5 if VERT else 3.3;g=lattice(D['level1'],w,c,True);links=coupling_edges(8,w,c);self.add(links,g)
  loc=[0,-1.3,0] if VERT else [3.6,.4,0]
  coeff=box('유효 상호작용\n(K₁, K₂, …)',6.8 if VERT else 6,1.5,PURPLE,31).move_to(loc);self.add(coeff);self.note('격자: 계산된 블록 스핀 · 상호작용: 개념도',MUTED)
  self.at(77)
  for lev,n,label in [(2,4,'다음 척도의 상호작용\n(K₁′, K₂′, …)'),(3,2,'더 큰 척도의 상호작용\n(K₁″, K₂″, …)')]:
   coeff.become(box(label,6.8 if VERT else 6,1.5,PURPLE,31).move_to(loc))
   self.play(g.animate.scale(.5).set_opacity(0),links.animate.scale(.5).set_opacity(0),run_time=.45)
   self.remove(g,links);g=lattice(D[f'level{lev}'],w,c,True);links=coupling_edges(n,w,c,True)
   self.play(FadeIn(g),FadeIn(links),run_time=.65)
  self.at(81);self.note('8 × 8 → 4 × 4 → 2 × 2 · 상호작용 변화는 개념도',MUTED)
  self.add(txt('Renormalization',29,YELLOW,7).move_to([0,3.75 if VERT else 1.85,0]))
  self.at(87);self.note('새 변수와 새 상호작용으로 거시적인 거동을 기술한다')
 def part_07(self):
  self.condition('고정점 부근의 개념 모형 · r → 2r, g → g/2')
  base,ax=flow_axes();self.add(base);self.note('계수가 작다는 이유가 아니라 · 반복 변환에 대한 반응으로 구분',MUTED)
  p=Dot(ax.c2p(0,.8),color=TEAL,radius=.09);q=Dot(ax.c2p(.08,-.4),color=RED,radius=.09);self.add(p,q)
  self.at(93);self.add(txt('고정점에서의 차이를 추적',24,TEAL,6).move_to([0,3.5,0] if VERT else [3.7,.9,0]))
  self.at(98)
  self.add(box('r: 임계 조건에서 벗어나는 정도',7 if VERT else 6,.7,RED,26).move_to([0,-2.6,0] if VERT else [3.7,-.45,0]))
  for i in range(1,4):self.play(p.animate.move_to(ax.c2p(0,.8*.5**i)),q.animate.move_to(ax.c2p(.08*2**i,-.4*.5**i)),run_time=1)
  self.note('g는 감소 · r는 증가 · 어떤 방향이 남는가?',YELLOW)
 def part_08(self):
  self.condition('임계 조건에 맞춘 흐름 · 임계면 r = 0 위')
  base,ax=flow_axes();self.add(base)
  p=Dot(ax.c2p(0,.82),color=TEAL,radius=.1);q=Dot(ax.c2p(0,-.8),color=RED,radius=.1);off=Dot(ax.c2p(.08,.45),color=MUTED,radius=.07);self.add(p,q,off)
  labels=VGroup(txt('A',24,TEAL).move_to(ax.c2p(0,.82)+LEFT*.3),txt('B',24,RED).move_to(ax.c2p(0,-.8)+LEFT*.3));self.add(labels)
  self.note('임계면을 벗어난 회색 점은 고정점에서 멀어진다',MUTED)
  for i in range(1,4):self.play(p.animate.move_to(ax.c2p(0,.82*.5**i)),q.animate.move_to(ax.c2p(0,-.8*.5**i)),off.animate.move_to(ax.c2p(.08*2**i,.45*.5**i)),run_time=1.4)
  self.at(111);label=box('Fixed Point\n다시 척도를 바꾸어도 핵심 구조 유지',7 if VERT else 6.2,1.25,PURPLE,27).move_to([0,-2.6,0] if VERT else [3.6,.4,0]);self.play(FadeIn(label),run_time=.7)
  self.play(p.animate.move_to(ax.c2p(0,.02)),q.animate.move_to(ax.c2p(0,-.02)),run_time=1.5);self.note('모든 근처 상태가 아니라 · 임계 조건의 흐름이 접근',YELLOW)
 def part_09(self):
  self.condition('같은 고정점의 지배 → 공통 임계 법칙')
  self.add(Dot([0,2.7 if VERT else 1.4,0],color=PURPLE,radius=.16),txt('Fixed Point',28,PURPLE).move_to([0,3.3 if VERT else 1.85,0]))
  pair=scaling_pair().scale(.72 if VERT else .85).move_to([0,-.1 if VERT else -.35,0]);self.add(pair);self.note('같은 임계 지수 β · 같은 스케일링 법칙',YELLOW)
  self.at(123);self.note('보편성 · Universality',PURPLE)
 def part_10(self):
  self.condition('보편성의 조건 · 차원, 대칭성, 상호작용 등')
  centers=([-2.2,2.1,0],[0,2.1,0],[2.2,2.1,0]) if VERT else ([-4.5,.2,0],[0,.2,0],[4.5,.2,0])
  for i,c in enumerate(centers):self.add(Dot(c,color=[TEAL,PURPLE,RED][i],radius=.16),txt(f'부류 {i+1}',27,[TEAL,PURPLE,RED][i]).move_to(np.array(c)+DOWN*.65))
  self.note('모든 물질이 하나의 보편성 부류에 속하는 것은 아니다',MUTED)
  self.at(129);labels=VGroup(*[box(s,6.6 if VERT else 4,.7,YELLOW,27) for s in ['공간의 차원','질서변수의 대칭성','상호작용의 성질']]).arrange(DOWN if VERT else RIGHT,buff=.15).move_to([0,-.9 if VERT else -1.15,0]);self.play(FadeIn(labels),run_time=.8)
 def part_11(self):
  self.condition('공통인 임계 지수 · 물질마다 다른 세부 특성')
  cards=VGroup(box('Δρ ∼ Aρ εᵝ',7 if VERT else 6,1.15,TEAL,39),box('M ∼ Aₘ εᵝ',7 if VERT else 6,1.15,RED,39)).arrange(DOWN if VERT else RIGHT,buff=.4).move_to([0,1.5 if VERT else .65,0]);self.add(cards)
  self.add(box('β는 공통 · 진폭 A는 물질별',7 if VERT else 12,1,YELLOW,33).move_to([0,-1.1 if VERT else -.95,0]));self.note('미시적인 특성과 비보편적인 수치가 모두 사라지지는 않는다',MUTED)
 def part_12(self):
  self.condition('거시 임계 법칙을 이해하는 데 필요한 정보')
  pair=material_pair();self.add(pair);self.note('모든 미시적 차이를 전부 알아야 하는 것은 아니다')
  self.play(pair.animate.set_opacity(.35),run_time=1.5)
  self.add(box('남는 핵심: 대칭성 · 차원 · 임계 구조',7 if VERT else 12,1.1,YELLOW,31).move_to([0,.4 if VERT else 0,0]))
 def part_13(self):
  self.condition('같은 보편성 부류 · 임계 조건에서의 거시 법칙')
  pair=material_pair();self.add(pair);self.note('미시적인 내부 구조는 서로 다르다',MUTED)
  self.at(154);self.play(pair.animate.set_opacity(.18),run_time=1)
  core=box('서로 다른 구조에서\n같은 핵심 성질이 남는다',7 if VERT else 12,1.5,YELLOW,38).move_to([0,.6 if VERT else .3,0]);self.play(FadeIn(core),run_time=.8);self.note('모든 미시적 차이가 거시적 법칙을 결정하는 것은 아니다')
