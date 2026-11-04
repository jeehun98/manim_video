"""Fixed node positions, computed energies, and explicit all-vector certificates."""
import json,os
from pathlib import Path
import numpy as np
from manim import *
from data_model import *
ROOT=Path(__file__).resolve().parent
VERT=os.getenv('MINIMAL_LAYOUT','shorts')=='shorts'
config.frame_width=9 if VERT else 16;config.frame_height=16 if VERT else 9;config.background_color='#0B1423'
INK='#EDF3FA';MUTED='#8B9DB5';TEAL='#42D7BD';RED='#FF6B78';YELLOW='#F3D277';BLUE='#6FAAFF';PANEL='#152338';EDGE='#2B3E57'
MANIFEST=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
def txt(s,size=30,color=INK,width=None):
 m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.1)
 if width and m.width>width:m.scale_to_fit_width(width)
 return m
def box(s,width=6,height=1,color=TEAL,size=30):
 return VGroup(RoundedRectangle(width=width,height=height,corner_radius=.13,color=color,stroke_width=1.5,fill_color=PANEL,fill_opacity=1),txt(s,size,color,width-.3))
def ring(n,radius=2.6,center=(0,.5,0)):
 return [np.array(center,float)+radius*np.array([np.cos(PI/2-TAU*i/n),np.sin(PI/2-TAU*i/n),0]) for i in range(n)]
def graph(pos,edges,values=None,color=TEAL,node_radius=.12):
 lines=VGroup(*[Line(pos[i],pos[j],color=color if w>=1 else MUTED,stroke_width=1+min(w,5)*.75,stroke_opacity=.85 if w>=1 else .32) for i,j,w in edges])
 nodes=VGroup(*[Dot(p,radius=node_radius,color=INK) if values is None else VGroup(Circle(radius=node_radius,color=color,stroke_width=1.5,fill_color=PANEL,fill_opacity=1).move_to(p),txt(f'{values[i]:g}',19 if node_radius<.25 else 31,INK,node_radius*1.65).move_to(p)) for i,p in enumerate(pos)])
 return VGroup(lines,nodes)
def path(points,color=TEAL):return VMobject(color=color,stroke_width=6).set_points_as_corners(points)
def cluster_positions():
 if VERT:return [np.array(p,float) for p in [(-1,3,0),(1,3,0),(-1,1.4,0),(1,1.4,0),(-1,-.4,0),(1,-.4,0),(-1,-2,0),(1,-2,0)]]
 return [np.array(p,float) for p in [(-4,1.2,0),(-2,1.2,0),(-4,-.6,0),(-2,-.6,0),(2,1.2,0),(4,1.2,0),(2,-.6,0),(4,-.6,0)]]
def energy_pair(values=(1,3)):
 p=[np.array([-2,.8 if VERT else .5,0]),np.array([2,.8 if VERT else .5,0])]
 g=graph(p,[(0,1,2.)],values=values,node_radius=.45)
 g.add(txt('w = 2',27,YELLOW).move_to([0,1.6 if VERT else 1.35,0]));return g
def triangle_panel(edges,values,center,label):
 c=np.array(center,float);scale=1.15 if VERT else 1.0
 p=[c+scale*np.array([0,1,0]),c+scale*np.array([-1,-.7,0]),c+scale*np.array([1,-.7,0])]
 g=graph(p,edges,values=values,node_radius=.23 if VERT else .2)
 if len(edges)==2 and not VERT:label='축소 · 2개 · w = 1.5'
 g.add(txt(label,24,MUTED).move_to(c+[0,1.6,0]))
 e=energy(edges,values)
 b=box(f'E = {e:g}',2.3,.8 if VERT else .65,YELLOW,32).move_to([2.05,c[1],0] if VERT else c+[0,-1.4,0]);g.add(b)
 if len(edges)==2 and VERT:g.add(txt('각 w = 1.5',20,YELLOW).move_to(c+[0,-1.35,0]))
 return g
def comparison(values,original_sparse=False):
 # Same positions in each panel, same assigned values; only edges/weights differ.
 centers=([-1.1,2.1,0],[-1.1,-1.3,0]) if VERT else ([-3.65,.3,0],[3.65,.3,0])
 out=VGroup()
 for idx,(edges,c,label) in enumerate(zip([SPARSE_G,SPARSE_H if original_sparse else SPARSE_G],centers,['원본 G · 28개',('축소 H · 8개' if original_sparse else '선택 전 · 28개')])):
  pos=ring(8,1.25 if VERT else .98,c);g=graph(pos,edges,values=values,node_radius=.18)
  g.add(txt(label,22,TEAL if idx else MUTED).move_to(np.array(c)+[0,1.64 if VERT else 1.5,0]))
  b=box(f'E = {energy(edges,values):.1f}',2.35,.73 if VERT else .65,YELLOW,29).move_to([2.1,c[1],0] if VERT else [c[0],-1.28,0]);g.add(b);out.add(g)
 return out
class SparsificationScene(Scene):
 index=0
 def at(self,t):
  target=t-self.start
  if self.time>target+.075:raise RuntimeError((self.index,self.time,target))
  if target-self.time>.001:self.wait(target-self.time)
 def note(self,s,color=TEAL):
  self.notice.become(txt(s,27 if VERT else 25,color,7.15 if VERT else 13.5).move_to([0,-3.55 if VERT else -1.95,0]))
 def condition(self,s):
  self.cond.become(box(s,7 if VERT else 11,.75,YELLOW,24).move_to([0,4.45 if VERT else 2.5,0]))
 def construct(self):
  m=MANIFEST[self.index];self.start=m['start'];self.end=m['end']
  self.add(txt('모든 것이 필요할까?   /   03',20,MUTED).move_to([0,7.05 if VERT else 4.02,0]),txt(m['title'],38 if VERT else 35,INK,7.1 if VERT else 14).move_to([0,6.05 if VERT else 3.35,0]),Line([-3.55 if VERT else -7,5.35 if VERT else 2.88,0],[3.55 if VERT else 7,5.35 if VERT else 2.88,0],color=EDGE,stroke_width=1))
  self.cond=VGroup(VectorizedPoint());self.notice=VGroup(VectorizedPoint());self.add(self.cond,self.notice)
  track=Line([-3.55 if VERT else -7,-6.95 if VERT else -4.08,0],[3.55 if VERT else 7,-6.95 if VERT else -4.08,0],color=EDGE,stroke_width=2)
  progress=Line(track.get_start(),track.get_start()+RIGHT*.001,color=TEAL,stroke_width=3)
  progress.add_updater(lambda p:p.put_start_and_end_on(track.get_start(),track.get_start()+RIGHT*track.width*max(.0001,min(1,(self.start+self.time)/163))))
  self.add(track,progress);getattr(self,f'part_{self.index:02}')();self.at(self.end)
 def part_00(self):
  pos=ring(32,2.6 if VERT else 1.8,(0,.7 if VERT else .2,0));edges=sorted({tuple(sorted((i,(i+k)%32))) for i in range(32) for k in [1,4,9]})
  g=graph(pos,[(i,j,1) for i,j in edges],node_radius=.055)
  self.play(FadeIn(g[1]),LaggedStart(*[Create(e) for e in g[0]],lag_ratio=.008),run_time=2.5)
  self.condition('연결된 무방향 네트워크');self.note('점 32개 · 연결 96개',MUTED)
  self.at(4);self.play(Indicate(g[0],color=TEAL,scale_factor=1),run_time=.8)
  self.at(8);self.play(VGroup(*g[0][::5]).animate.set_color(RED).set_opacity(.3),run_time=.8);self.note('어떤 성질을 유지할까?',YELLOW)
 def part_01(self):
  self.condition('조건: 연결성 · 연결된 무방향 그래프')
  pos=ring(8,2.55 if VERT else 1.65,(0,.65 if VERT else .25,0));all_edges=complete(8);g=graph(pos,all_edges);self.add(g);self.note('노드 8개 · 원본 간선 28개',MUTED)
  self.at(15);keep={(i,j) for i,j,w in TREE}
  self.play(*[e.animate.set_opacity(0 if (i,j) not in keep else 1).set_color(TEAL) for e,(i,j,w) in zip(g[0],all_edges)],run_time=1.4)
  self.note('연결을 유지하도록 고른 7개 간선')
  self.at(20);tracer=Dot(pos[0],radius=.15,color=YELLOW);self.add(tracer)
  for i in range(7):self.play(tracer.animate.move_to(pos[i+1]),run_time=.25,rate_func=linear)
  self.note('신장 트리 · Spanning Tree · 8 − 1 = 7')
 def part_02(self):
  self.condition('각 간선의 길이 1 · 거리 비교 예시')
  s=2.3 if VERT else 1.3;c=np.array([0,.65 if VERT else .3,0]);p={k:c+s*np.array(v) for k,v in {'A':[-1,1,0],'B':[1,1,0],'C':[1,-1,0],'D':[-1,-1,0]}.items()}
  lines=VGroup(*[Line(p[a],p[b],color=MUTED,stroke_width=4) for a,b in [('A','B'),('B','C'),('C','D'),('D','A')]])
  nodes=VGroup(*[VGroup(Dot(v,radius=.1,color=INK),txt(k,22).move_to(v+(v-c)/np.linalg.norm(v-c)*.3)) for k,v in p.items()]);self.add(lines,nodes);self.note('모든 지점이 연결되어 있어도…',YELLOW)
  self.at(32);self.play(lines[0].animate.set_color(RED),run_time=.4);self.play(lines[0].animate.set_opacity(0),Create(path([p[k] for k in 'ADCB'])),run_time=1)
  b=box('A → B : 1 → 3',5.6 if VERT else 5,.9,RED,32).move_to(c);self.play(FadeIn(b),run_time=.5)
  self.at(38);self.note('연결성 유지 ≠ 최단거리 유지',YELLOW)
 def part_03(self):
  self.condition('같은 노드 · 간선 선택 + 가중치 조정')
  pos=ring(8,2.2 if VERT else 1.5,(0,.5,0) if VERT else (-3,.2,0));g=graph(pos,SPARSE_G);self.add(g)
  name=txt('Graph Sparsification',29,TEAL,7 if VERT else 6).move_to([0,3.25,0] if VERT else [3.3,.7,0]);self.add(name);self.note('굵기: 간선 가중치 표현',MUTED)
  self.at(47);self.play(*[e.animate.set_opacity(1 if (i,j) in CYCLE else 0).set_stroke(width=4.45 if (i,j) in CYCLE else 1) for e,(i,j,w) in zip(g[0],SPARSE_G)],run_time=1.3)
  self.play(Transform(name,txt('Spectral Sparsification',29,YELLOW,7).move_to(name)),run_time=.6);self.note('에너지 구조를 근사적으로 보존한다',YELLOW)
 def part_04(self):
  self.condition('노드의 값 x와 간선 가중치 w를 구별')
  self.add(energy_pair());self.note('점마다 하나의 숫자를 배치',MUTED)
  self.at(57);b=box('1 − 3 = −2',5.7,1,YELLOW,39).move_to([0,-1.1 if VERT else -.9,0]);self.play(FadeIn(b),run_time=.7)
  self.note('두 점의 값이 얼마나 다른가?',YELLOW)
 def part_05(self):
  g=energy_pair();self.add(g);self.condition('무방향 간선 한 번씩 · w ≥ 0')
  calc=box('2 × (1 − 3)² = 8',6.4,1,YELLOW,37).move_to([0,-1.1 if VERT else -.9,0]);self.play(FadeIn(calc),run_time=.8);self.note('가중치 × 차이의 제곱')
  self.at(66);self.play(FadeOut(g),FadeOut(calc),run_time=.3)
  self.condition('예시 가중치 2, 1, 1 · 간선 한 번씩 합산')
  formula=txt('E(x) = Σ wᵢⱼ (xᵢ − xⱼ)²',37,YELLOW,7 if VERT else 13).move_to([0,2 if VERT else 1.2,0])
  p=[[-1.8,.4,0],[1.8,.4,0],[0,-1.3,0]] if VERT else [[-1.8,.2,0],[1.8,.2,0],[0,-1.1,0]]
  tri=graph([np.array(x) for x in p],[(0,1,2),(0,2,1),(1,2,1)],[1,3,2],node_radius=.28);self.add(formula,tri);self.note('8 + 1 + 1 = 10 · 모든 간선의 기여 합')
 def part_06(self):
  self.condition('같은 가중치 w = 2 · 값만 변화')
  t=ValueTracker(3)
  g=always_redraw(lambda:energy_pair((1,round(t.get_value(),1))))
  b=always_redraw(lambda:box(f'E = 2 × (1 − {round(t.get_value(),1):.1f})² = {2*(1-round(t.get_value(),1))**2:.2f}',7.1,1,YELLOW,31).move_to([0,-1.1 if VERT else -.9,0]));self.add(g,b)
  self.note('연결된 두 값이 같아지면 기여는 0')
  self.play(t.animate.set_value(1),run_time=4.5,rate_func=smooth)
 def part_07(self):
  self.condition('삼각형 원리 예시 · 좋은 오차 보장과 구별')
  centers=([-1.15,2.1,0],[-1.15,-.95,0]) if VERT else ([-3.6,.15,0],[3.5,.15,0])
  g=triangle_panel(TRI_G,TRI_VALUES[0],centers[0],'원본 · w = 1')
  h=triangle_panel(TRI_G,TRI_VALUES[0],centers[1],'간선 삭제 전');self.add(g,h);self.note('원본 에너지 1 + 1 + 4 = 6',MUTED)
  self.at(76);new=triangle_panel(TRI_H,TRI_VALUES[0],centers[1],'축소 · 3개 → 2개');self.play(Transform(h,new),run_time=1)
  self.note('재가중 후 7.5 · 정확히 같지는 않다',YELLOW)
  self.at(80)
  for when,values in [(80,TRI_VALUES[1]),(83,TRI_VALUES[2])]:
   self.at(when);self.play(Transform(g,triangle_panel(TRI_G,values,centers[0],'원본 · w = 1')),Transform(h,triangle_panel(TRI_H,values,centers[1],'축소 · 각 w = 1.5')),run_time=.7)
   self.note(f'같은 값 배치: E_G = {energy(TRI_G,values):g} · E_H = {energy(TRI_H,values):g}',YELLOW)
  self.at(85);self.note('이 예시의 최악 상대 오차는 50%',YELLOW)
 def part_08(self):
  self.condition('단 하나의 배치가 아닌, 모든 x에 대해')
  formula='(1 − ε) E_G(x)\n≤ E_H(x)\n≤ (1 + ε) E_G(x)' if VERT else '(1 − ε) E_G(x) ≤ E_H(x) ≤ (1 + ε) E_G(x)'
  self.add(box(formula,7 if VERT else 13,3 if VERT else 1.4,YELLOW,35).move_to([0,1 if VERT else .35,0]));self.note('표본 몇 개의 일치 ≠ 모든 배치의 보장',MUTED)
  self.at(91);self.note('간선 수보다, 에너지 구조를 얼마나 대표하는가?',YELLOW)
 def part_09(self):
  self.condition('각 집단 K4 · 모든 간선 가중치 1')
  p=cluster_positions();g=graph(p,CLUSTERS,node_radius=.12);self.add(g[1]);self.note('두 집단 · 내부 연결 6 + 6',MUTED)
  self.at(100);self.play(Create(g[0]),run_time=1.4)
  self.at(104);self.play(g[0][-1].animate.set_color(YELLOW).set_stroke(width=5),run_time=.5);self.note('두 집단을 잇는 유일한 다리',YELLOW)
 def part_10(self):
  self.condition('같은 노드 · 내부 삭제와 다리 삭제 비교')
  p=cluster_positions();g=graph(p,CLUSTERS,node_radius=.12);self.add(g);internal=g[0][0];bridge=g[0][-1]
  self.play(internal.animate.set_color(RED),run_time=.3);self.play(internal.animate.set_opacity(0),Create(path([p[k] for k in [0,2,1]])),run_time=.8);self.note('내부 간선: 다른 경로로 이동 가능')
  self.at(111);self.play(bridge.animate.set_color(RED),run_time=.3);self.play(bridge.animate.set_opacity(0),run_time=.5)
  divider=DashedLine([-3,.5,0],[3,.5,0],color=RED,dash_length=.15) if VERT else DashedLine([0,-1.4,0],[0,1.7,0],color=RED,dash_length=.15)
  self.play(Create(divider),run_time=.5);self.note('유일한 다리 삭제 → 연결 성분 2개',RED)
  self.at(116);self.note('모든 연결이 똑같이 중요하지 않다',YELLOW)
 def part_11(self):
  self.condition('원본 회로 · w = 1 → 저항 r = 1')
  p=cluster_positions();g=graph(p,CLUSTERS,node_radius=.11);self.add(g)
  for idx in [0,len(CLUSTERS)-1]:
   line=g[0][idx];res=Rectangle(width=.34,height=.15,color=YELLOW,fill_color=PANEL,fill_opacity=1,stroke_width=2).rotate(line.get_angle()).move_to(line.get_center());self.add(res)
  r1=box('내부 R\n0.50' if VERT else '집단 내부 R = 0.50',2.2 if VERT else 5,.95 if VERT else .65,TEAL,25).move_to([2.35,2.2,0] if VERT else [-3.3,-1.25,0])
  r2=box('다리 R\n1.00' if VERT else '유일한 다리 R = 1.00',2.2 if VERT else 5,.95 if VERT else .65,YELLOW,25).move_to([2.35,.35,0] if VERT else [3.3,-1.25,0]);self.play(FadeIn(r1),FadeIn(r2),run_time=.7)
  self.note('유효 저항 · Effective Resistance',YELLOW)
  self.at(126);self.note('중요도 예시 wR · 표본 선택 + 가중치 조정')
 def part_12(self):
  self.condition('별도 검증 예시 · G: 4 / 0.1 → H: 4.6')
  original=comparison(VALUES[0],False);self.add(original);self.note('같은 노드와 같은 값 · 원본 28개 간선',MUTED)
  self.at(134);self.play(Transform(original,comparison(VALUES[0],True)),run_time=1.2);self.note('28 → 8개 간선 · 남은 가중치 4.6')
  self.at(136);self.remove(original)
  tracker=ValueTracker(0)
  def values():
   t=tracker.get_value();k=min(1,int(t));f=t-k
   return np.round((1-f)*np.array(VALUES[k])+f*np.array(VALUES[k+1]),1)
  live=always_redraw(lambda:comparison(values(),True));self.add(live)
  self.play(tracker.animate.set_value(1),run_time=1.5,rate_func=linear)
  self.play(tracker.animate.set_value(2),run_time=1.5,rate_func=linear)
  self.note('모든 x에서 ε = 0.15 이내 · 별도 검증 완료',YELLOW)
 def part_13(self):
  self.condition('보존 대상: 에너지 · 모든 최단거리 아님')
  self.add(comparison(VALUES[2],True));self.note('선택한 수학적 조건의 근사 보존',YELLOW)
  self.at(146);self.note('모든 x: 0.85 E_G(x) ≤ E_H(x) ≤ 1.15 E_G(x)',YELLOW)
 def part_14(self):
  self.condition('선택 · 재가중 · 보존 조건 검증')
  pos=ring(8,2.25 if VERT else 1.55,(0,.8,0) if VERT else (-3.5,.25,0));g=graph(pos,SPARSE_H,node_radius=.12);self.add(g)
  self.note('적은 간선만으로는 충분하지 않다',MUTED)
  self.at(155)
  steps=VGroup(*[box(s,2.15 if VERT else 4.2,.8,c,25) for s,c in [('관계 선택',TEAL),('가중치 조정',YELLOW),('조건 검증',BLUE)]]).arrange(RIGHT if VERT else DOWN,buff=.18).move_to([0,-2.3,0] if VERT else [3.1,.25,0]);self.play(FadeIn(steps),run_time=.8)
  self.note('더 작은 네트워크 · 핵심 성질의 근사 보존')
