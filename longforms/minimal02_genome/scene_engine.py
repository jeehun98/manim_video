"""Minimal genome: experiments and conditions, not a universal gene-count bound."""
import json,os
from pathlib import Path
import numpy as np
from manim import *
ROOT=Path(__file__).resolve().parent
VERT=os.getenv('MINIMAL_LAYOUT','shorts')=='shorts'
config.frame_width=9 if VERT else 16;config.frame_height=16 if VERT else 9
config.background_color='#0B1423'
INK='#EDF3FA';MUTED='#8B9DB5';TEAL='#42D7BD';RED='#FF6B78';YELLOW='#F3D277';BLUE='#6FAAFF';PANEL='#152338';EDGE='#2B3E57'
MANIFEST=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
def txt(s,size=30,color=INK,width=None):
 m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.12)
 if width and m.width>width:m.scale_to_fit_width(width)
 return m
def box(s,width=6,height=1.1,color=TEAL,size=30):
 return VGroup(RoundedRectangle(width=width,height=height,corner_radius=.15,color=color,stroke_width=1.6,fill_color=PANEL,fill_opacity=1),txt(s,size,color,width-.4))
def cell(width=5.5,height=4.3,count=30,irregular=False,color=TEAL):
 if irregular:
  th=np.linspace(0,TAU,129);r=1+.15*np.sin(3*th)+.08*np.cos(5*th)
  outline=VMobject(color=color,stroke_width=3,fill_color=color,fill_opacity=.055).set_points_smoothly([np.array([width/2*rr*np.cos(t),height/2*rr*np.sin(t),0]) for t,rr in zip(th,r)])
 else:outline=Ellipse(width=width,height=height,color=color,stroke_width=3,fill_color=color,fill_opacity=.055)
 genes=VGroup(*[RoundedRectangle(width=.36,height=.15,corner_radius=.03,stroke_width=0,fill_color=TEAL if j%3 else BLUE,fill_opacity=.85) for j in range(count)])
 if count:
  genes.arrange_in_grid(cols=6,buff=(.1,.16));genes.scale_to_fit_width(width*.64)
  if genes.height>height*.58:genes.scale_to_fit_height(height*.58)
 return VGroup(outline,genes)
def assay(label,removed=(),alive=True):
 w,h=(6.6,2.5) if VERT else (5.8,3.1)
 frame=RoundedRectangle(width=w,height=h,corner_radius=.17,color=EDGE,stroke_width=1.5,fill_color=PANEL,fill_opacity=.65)
 title=txt(label,25,INK,w-.5).move_to([0,h/2-.34,0])
 center=np.array([-1.55,-.1,0]) if VERT else np.array([-1.15,-.15,0])
 shell=Ellipse(width=2.35,height=1.4,color=TEAL if alive else RED,stroke_width=2.5,fill_opacity=.04).move_to(center)
 genes=VGroup(*[box(s,.65,.5,RED if s in removed else (BLUE if s=='A' else TEAL),23).move_to(center+[x,0,0]) for s,x in [('A',-.45),('B',.45)]])
 strikes=VGroup(*[Cross(genes[j],stroke_color=RED,stroke_width=3) for j,s in enumerate(['A','B']) if s in removed])
 status=txt('생존' if alive else '생존 불가',30,TEAL if alive else RED,2.4).move_to([1.75 if VERT else 1.4,-.15,0])
 desc=txt('원본에서 독립 비교',17,MUTED,w-.5).move_to([0,-h/2+.25,0])
 return VGroup(frame,title,shell,genes,strikes,status,desc)
def flow_model():
 a=box('유전자 A',2.5,.9,BLUE,28).move_to([-1.75,2.1 if VERT else 1.4,0])
 b=box('유전자 B',2.5,.9,TEAL,28).move_to([1.75,2.1 if VERT else 1.4,0])
 f=box('생존에 필요한 기능',5.4,1.15,TEAL,31).move_to([0,-.5 if VERT else -.6,0])
 aa=Arrow(a.get_bottom(),f.get_top()+LEFT*1,color=BLUE,buff=.13,stroke_width=5)
 ab=Arrow(b.get_bottom(),f.get_top()+RIGHT*1,color=TEAL,buff=.13,stroke_width=5)
 return VGroup(a,b,f,aa,ab),a,b,f,aa,ab
def gene_grid():
 grid=VGroup(*[Square(side_length=.13,stroke_width=0,fill_color=MUTED,fill_opacity=.75) for _ in range(473)])
 grid.arrange_in_grid(cols=22,buff=.055)
 grid.scale_to_fit_height(6.15 if VERT else 3.4)
 grid.move_to([0,.6,0] if VERT else [-3.5,.25,0])
 return grid
class GenomeScene(Scene):
 index=0
 def at(self,t):
  target=t-self.start
  if self.time>target+.075:raise RuntimeError((self.index,self.time,target))
  if target-self.time>.001:self.wait(target-self.time)
 def note(self,s,color=TEAL):
  self.notice.become(txt(s,28 if VERT else 25,color,7.15 if VERT else 13.5).move_to([0,-3.55 if VERT else -1.95,0]))
 def condition(self,s):
  self.cond.become(box(s,7 if VERT else 11,.75,YELLOW,24).move_to([0,4.45 if VERT else 2.5,0]))
 def construct(self):
  m=MANIFEST[self.index];self.start=m['start'];self.end=m['end']
  self.add(txt('모든 것이 필요할까?   /   02',20,MUTED).move_to([0,7.05 if VERT else 4.02,0]),txt(m['title'],38 if VERT else 35,INK,7.1 if VERT else 14).move_to([0,6.05 if VERT else 3.35,0]),Line([-3.55 if VERT else -7,5.35 if VERT else 2.88,0],[3.55 if VERT else 7,5.35 if VERT else 2.88,0],color=EDGE,stroke_width=1))
  self.cond=VGroup(VectorizedPoint());self.notice=VGroup(VectorizedPoint());self.add(self.cond,self.notice)
  track=Line([-3.55 if VERT else -7,-6.95 if VERT else -4.08,0],[3.55 if VERT else 7,-6.95 if VERT else -4.08,0],color=EDGE,stroke_width=2)
  progress=Line(track.get_start(),track.get_start()+RIGHT*.001,color=TEAL,stroke_width=3)
  progress.add_updater(lambda p:p.put_start_and_end_on(track.get_start(),track.get_start()+RIGHT*track.width*max(.0001,min(1,(self.start+self.time)/164))))
  self.add(track,progress)
  getattr(self,f'part_{self.index:02}')();self.at(self.end)
 def part_00(self):
  c=cell(5.5,4.3) if VERT else cell(5,3.1)
  c.move_to([0,.75 if VERT else .2,0]);self.play(FadeIn(c),run_time=1)
  self.condition('유전자 구성 개념도 · 실제 위치 아님');self.note('세포는 유지하고, 유전자를 줄인다면?',YELLOW)
  self.at(4);selected=VGroup(*c[1][::4]);self.play(selected.animate.set_color(RED),run_time=.6)
  self.at(8);self.play(LaggedStart(*[g.animate.set_opacity(.08) for g in selected],lag_ratio=.15),run_time=1.5)
  self.note('어디까지 줄일 수 있을까?',YELLOW)
 def part_01(self):
  self.condition('실제 연구 · 2016년')
  institute=txt('J. Craig Venter Institute',27,MUTED,7).move_to([0,3 if VERT else 1.65,0]);self.add(institute)
  name=txt('JCVI-syn3.0',40,TEAL).move_to([0,1.6 if VERT else .7,0]);self.at(16);self.play(FadeIn(name),run_time=.6)
  count=txt('473',94,INK).move_to([0,-.2 if VERT else -.3,0]);self.at(18);self.play(FadeIn(count,shift=UP*.2),run_time=.6)
  self.add(txt('genes',28,MUTED).next_to(count,DOWN,buff=.25));self.note('확인된 축소 유전체 · 절대 최소값 아님',YELLOW)
 def part_02(self):
  self.condition('유전체 합성 ≠ 세포 전체의 합성')
  steps=VGroup(*[box(s,6 if VERT else 3.6,.9,c,26) for s,c in [('기존 세균 유전체',MUTED),('제거 · 재설계',YELLOW),('합성 유전체',TEAL)]])
  steps.arrange(DOWN if VERT else RIGHT,buff=.35).move_to([0,2.15 if VERT else 1.15,0]);self.play(LaggedStart(*[FadeIn(x) for x in steps],lag_ratio=.25),run_time=1.5)
  c=cell(3.5,2.15 if VERT else 1.75,0).move_to([0,-1.3 if VERT else -.45,0]);self.add(c)
  genome=VGroup(*[Line([-.65+j*.18,-.2,0],[-.65+j*.18,.2,0],color=TEAL,stroke_width=4) for j in range(8)]).move_to(steps[-1])
  self.at(25);self.add(genome);self.play(genome.animate.move_to(c.get_center()),run_time=1.2)
  self.note('합성한 유전정보 → 수용 세포')
 def part_03(self):
  self.condition('영양분이 충분한 특정 배양 환경')
  c=cell(3.6,2.9,24).move_to([0,.8 if VERT else .2,0]);self.add(c)
  particles=VGroup(*[Dot([3*np.cos(t),(.8 if VERT else .2)+2.2*np.sin(t),0],radius=.06,color=YELLOW) for t in np.linspace(0,TAU,12,endpoint=False)])
  self.add(particles);self.note('세균 세포 · 성장과 분열 가능')
  self.play(*[p.animate.move_to(c.get_center()+.5*(p.get_center()-c.get_center())) for p in particles],run_time=1)
  self.play(c.animate.scale(1.12),run_time=.7)
  daughters=VGroup(cell(2.7,2.2,18),cell(2.2,2.5,18)).arrange(RIGHT,buff=.25).move_to(c)
  self.play(ReplacementTransform(c,daughters),FadeOut(particles),run_time=1.2)
  self.note('분열 형태의 균일성과는 별도 조건',MUTED)
 def part_04(self):
  self.condition('성공한 구성 = 가능한 최소 구성?')
  q=txt('473개 = 최소?',57,YELLOW,7).move_to([0,1.5 if VERT else .5,0]);self.add(q);self.note('어떤 유전자가 필요한가?',YELLOW)
  self.at(39);self.play(q.animate.set_color(MUTED),run_time=.5)
  b=box('제거 → 생존 여부 확인',6.4,1.2,TEAL,32).move_to([0,-.6 if VERT else -.8,0]);self.play(FadeIn(b),run_time=.7)
 def part_05(self):
  self.condition('개념 실험 · 같은 원본에서 출발')
  c=cell(5,3.5,24).move_to([0,.7 if VERT else .25,0]);self.add(c)
  a=box('A',1,.65,BLUE,30).move_to(c.get_center());self.add(a);self.note('유전자 하나를 제거하고 관찰',YELLOW)
  self.play(a.animate.set_color(RED),run_time=.5);self.play(FadeOut(a),run_time=.6);self.play(Indicate(c[0],color=TEAL,scale_factor=1.02),run_time=.8)
 def part_06(self):
  self.condition('독립 복제본 비교 · 개념 실험')
  ac=assay('A만 제거',('A',));bc=assay('B만 제거',('B',))
  ac.move_to([0,2.35,0] if VERT else [-3.05,.25,0]);bc.move_to([0,-.6,0] if VERT else [3.05,.25,0])
  self.play(FadeIn(ac),run_time=.7);self.note('A 제거 → 생존')
  self.at(51);self.play(FadeIn(bc),run_time=.7);self.at(54);self.note('A만 제거해도, B만 제거해도 생존')
 def part_07(self):
  self.condition('기능 보완의 한 가지 개념 모델')
  model,a,b,f,aa,ab=flow_model();self.add(model);self.note('A와 B를 모두 제거하면?',YELLOW)
  self.at(61);self.play(a.animate.set_opacity(.2),aa.animate.set_opacity(.15),ab.animate.set_color(YELLOW),run_time=.7)
  self.note('A가 없어도 B 경로가 기능을 보완')
  self.at(64);self.play(a.animate.set_opacity(1),aa.animate.set_opacity(1),b.animate.set_opacity(.2),ab.animate.set_opacity(.15),run_time=.6)
  self.note('별도 원본: B가 없어도 A가 보완')
 def part_08(self):
  self.condition('개념 모델 · 두 변화가 결합할 때')
  model,a,b,f,aa,ab=flow_model();self.add(model)
  self.play(a.animate.set_opacity(.2),b.animate.set_opacity(.2),aa.animate.set_opacity(.1),ab.animate.set_opacity(.1),f[0].animate.set_stroke(RED),f[1].animate.set_color(RED),run_time=1)
  self.note('A + B 동시 제거 → 기능 상실 · 생존 불가',RED)
  self.at(71)
  self.play(FadeOut(model),run_time=.4)
  table=VGroup()
  labels=[('원본','생존',TEAL),('A만 제거','생존',TEAL),('B만 제거','생존',TEAL),('A + B 제거','생존 불가',RED)]
  for left,right,color in labels:
   row=VGroup(box(left,3.7 if VERT else 4.8,.8,MUTED,26),box(right,2.5 if VERT else 3.5,.8,color,27)).arrange(RIGHT,buff=.2);table.add(row)
  table.arrange(DOWN,buff=.15).move_to([0,.7 if VERT else .1,0]);
  if not VERT:table.scale(.8)
  self.play(FadeIn(table),run_time=.6);self.note('합성 치사 · Synthetic Lethality',YELLOW)
 def part_09(self):
  self.condition('유전자 간 의존 관계 · 개념도')
  positions=[[-2.1,1.9,0],[0,2.7,0],[2.1,1.9,0],[-2.1,-.4,0],[0,.5,0],[2.1,-.4,0]] if VERT else [[-4,1,0],[0,1.5,0],[4,1,0],[-4,-.8,0],[0,-.2,0],[4,-.8,0]]
  nodes=VGroup(*[box(s,1.25,.7,BLUE if j<3 else TEAL,26).move_to(p) for j,(s,p) in enumerate(zip(['A','B','C','기능 1','기능 2','기능 3'],positions))])
  edges=VGroup(*[Line(nodes[a].get_center(),nodes[b].get_center(),color=EDGE,stroke_width=3) for a,b in [(0,3),(0,4),(1,3),(1,4),(2,4),(2,5)]])
  self.add(edges,nodes);self.note('개별 필수성 ≠ 조합의 필수성',YELLOW)
  self.at(84);self.play(edges[2].animate.set_color(TEAL),edges[3].animate.set_color(TEAL),nodes[0].animate.set_opacity(.25),run_time=.8)
 def environment_panel(self,label,supply):
  w,h=(6.6,2.65) if VERT else (5.9,3.4)
  frame=RoundedRectangle(width=w,height=h,corner_radius=.18,color=EDGE,fill_color=PANEL,fill_opacity=.5,stroke_width=1.5)
  title=txt(label,25,YELLOW,w-.4).move_to([0,h/2-.35,0])
  shell=Ellipse(width=2.5,height=1.4,color=TEAL if supply else RED,stroke_width=2).move_to([-1.25,-.12,0])
  block=box('합성',1,.5,RED,21).move_to(shell)
  cross=Cross(block,stroke_color=RED,stroke_width=3)
  status=txt('필요 물질 확보' if supply else '필요 물질 부족',23,TEAL if supply else RED,2.6).move_to([1.6,-.1,0])
  dots=VGroup(*[Dot([x,-h/2+.5,0],radius=.06,color=YELLOW) for x in [-2.5,-2,-1.5,-1,-.5]]) if supply else VGroup()
  return VGroup(frame,title,shell,block,cross,status,dots)
 def part_10(self):
  self.condition('같은 합성 경로 결손 · 환경만 변경')
  left=self.environment_panel('외부 영양분 공급',True);right=self.environment_panel('외부 공급 제한',False)
  left.move_to([0,2.3,0] if VERT else [-3.15,.2,0]);right.move_to([0,-.75,0] if VERT else [3.15,.2,0])
  self.note('필수성은 환경에도 의존한다',YELLOW)
  self.at(91);self.play(FadeIn(left),run_time=.6)
  particles=left[-1];self.play(*[d.animate.move_to(left[2].get_center()+RIGHT*.25*(j-2)) for j,d in enumerate(particles)],run_time=1.3)
  self.at(97);self.play(FadeIn(right),run_time=.6);self.note('대체 공급·경로가 없는 조건의 개념 예시',MUTED)
 def part_11(self):
  self.condition('실제 연구 · 분열 형태의 개선')
  conditions=VGroup(box('생존',2.6,.8,TEAL,29),box('안정적 성장·분열',4.1,.8,YELLOW,28)).arrange(RIGHT,buff=.25).move_to([0,3.1 if VERT else 1.45,0]);self.add(conditions)
  self.note('같은 조건이 아니다',YELLOW)
  self.at(107)
  original=cell(2.35,1.95,12,True).move_to([-1.65,.5,0] if VERT else [-3.1,-.1,0]);self.play(FadeIn(original),run_time=.6)
  label=txt('JCVI-syn3.0',23,MUTED).next_to(original,DOWN,buff=.3);self.add(label)
  self.play(original.animate.stretch(1.15,0),run_time=.8)
  self.at(112)
  improved=VGroup(cell(1.2,1.2,6),cell(1.2,1.2,6)).arrange(RIGHT,buff=.12).move_to([1.65,.5,0] if VERT else [3.1,-.1,0])
  self.play(FadeIn(improved),run_time=.7);self.add(txt('JCVI-syn3A',23,TEAL).next_to(improved,DOWN,buff=.35))
  arrow=Arrow(original.get_right(),improved.get_left(),color=YELLOW,buff=.12,stroke_width=3)
  if arrow.get_length()>.2:self.play(GrowArrow(arrow),run_time=.5)
  self.note('일부 유전자 보강 → 분열 특성 개선')
 def part_12(self):
  self.condition('2016년 최초 발표 당시의 지식 상태')
  grid=gene_grid();self.add(grid);self.note('실제 473칸 · 한 칸은 유전자 한 개',MUTED)
  self.at(119);self.play(VGroup(*grid[:149]).animate.set_fill(YELLOW,opacity=1),run_time=1.4)
  if not VERT:
   self.add(txt('149 / 473',57,YELLOW).move_to([3.1,.8,0]),txt('약 31.5%',35,YELLOW).move_to([3.1,-.15,0]),txt('구체적 기능 미해명',26,MUTED).move_to([3.1,-.9,0]))
  self.note('149 / 473 · 약 31.5% · 기능 미해명',YELLOW)
 def part_13(self):
  self.condition('필요성의 확인과 작동 원리의 이해')
  cards=VGroup(box('필요함을 확인',6 if VERT else 5.6,1.2,TEAL,33),box('정확한 역할은 미지',6 if VERT else 5.6,1.2,YELLOW,31)).arrange(DOWN if VERT else RIGHT,buff=.8).move_to([0,.85 if VERT else .25,0]);self.add(cards)
  self.note('필요하다는 사실 ≠ 기능을 안다는 뜻',YELLOW)
 def part_14(self):
  self.condition('구성의 발견 ≠ 최소성의 증명')
  known=box('473개로 생존 가능',6.5 if VERT else 6.2,1.25,TEAL,34).move_to([0,2.4,0] if VERT else [-3.6,.55,0]);self.add(known)
  self.note('확인된 축소 유전체',TEAL)
  self.at(138)
  q=box('더 적으면 불가능?',6.5 if VERT else 6.2,1.25,YELLOW,34).move_to([0,-.2,0] if VERT else [3.3,.55,0]);self.play(FadeIn(q),run_time=.6)
  self.note('모든 가능한 조합에 대한 하한 증명은 아님',YELLOW)
 def part_15(self):
  self.condition('작은 조합의 가능성과 탐색 조건')
  unknown=VGroup(DashedVMobject(RoundedRectangle(width=6.4,height=1.25,corner_radius=.15,color=MUTED),num_dashes=45),txt('더 작은 미지의 조합?',33,MUTED,6)).move_to([0,2 if VERT else .95,0]);self.add(unknown)
  labels=VGroup(*[box(s,2.1 if VERT else 3.7,.9,c,25) for s,c in [('환경',YELLOW),('유전자 조합',BLUE),('요구 기능',TEAL)]]).arrange(RIGHT,buff=.18).move_to([0,-.3 if VERT else -.65,0]);self.play(FadeIn(labels),run_time=.8)
  self.note('조건이 달라지면 필요한 유전자도 달라진다',YELLOW)
 def part_16(self):
  self.condition('개별 삭제를 넘어, 조건과 조합으로')
  cards=VGroup(*[box(s,2.15 if VERT else 3.6,.9,c,25) for s,c in [('관계',BLUE),('환경',YELLOW),('유지할 기능',TEAL)]]).arrange(RIGHT,buff=.18).move_to([0,2.65 if VERT else 1.35,0]);self.add(cards)
  self.note('단순히 유전자 수를 줄이는 일이 아니다',MUTED)
  self.at(157)
  target=box('생명 유지에 필요한\n유전자 조합' if VERT else '생명 유지에 필요한 유전자 조합',6.8 if VERT else 11.5,1.8 if VERT else 1.25,TEAL,38).move_to([0,-.3 if VERT else -.65,0])
  arrows=VGroup(*[Arrow(x.get_bottom(),target.get_top()+RIGHT*d,color=c,buff=.1,stroke_width=2) for x,d,c in zip(cards,[-1.9,0,1.9],[BLUE,YELLOW,TEAL])]);self.play(FadeIn(target),*[GrowArrow(a) for a in arrows],run_time=1)
  self.note('관계와 생존 조건을 함께 고려한다')
