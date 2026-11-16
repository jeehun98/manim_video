"""Persistent original-problem reference strips; no solution values."""
import json,sys
from pathlib import Path
from manim import *
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from quantum_series.shared.theme import text
HERE=Path(__file__).parent
DATA=json.loads((HERE/'problems.json').read_text(encoding='utf-8'))
config.pixel_width=1920;config.pixel_height=180
config.frame_width=16;config.frame_height=1.5
config.background_color='#0B1020'
INK='#F8FAFC';MUTED='#94A3B8';CYAN='#38BDF8';GREEN='#4ADE80';PURPLE='#C084FC'
def tx(s,x,y,size=19,color=INK,width=8):return text(s,x,y,size,color,width)
def math(s,x,y,size=28,color=INK,width=9,height=.46):
 m=MathTex(s,font_size=size,color=color)
 if m.width>width:m.scale_to_fit_width(width)
 if m.height>height:m.scale_to_fit_height(height)
 return m.move_to([x,y,0])
class ProblemCard(Scene):
 episode=1
 def construct(self):
  d=DATA[f'csat{self.episode:02d}']
  self.add(RoundedRectangle(width=15.7,height=1.36,corner_radius=.09,stroke_color='#334155',stroke_width=1.2,fill_color='#111B2E',fill_opacity=1),Line([-5.9,-.54,0],[-5.9,.54,0],color='#334155',stroke_width=1),Line([3.15,-.54,0],[3.15,.54,0],color='#334155',stroke_width=1))
  self.add(tx(f'수능 수학 {self.episode:02d}번',-6.87,.27,19,CYAN,1.75),tx(d['topic']+'\n다항함수 f, g' if self.episode==13 else d['topic'],-6.87,-.23,13 if self.episode==13 else 16,MUTED,1.75))
  lines=d['conditions'];ys={1:[0],2:[.28,-.28],3:[.43,0,-.43]}[len(lines)] if lines else []
  for item,y in zip(lines,ys):
   if isinstance(item,list):m=tx(item[1],-1.4,y,18,MUTED,8.65)
   else:m=math(item,-1.4,y,23 if len(lines)==3 else 28,width=8.65,height=.34 if len(lines)==3 else .46)
   self.add(m)
  if self.episode==4:self.graph()
  if self.episode==13:
   self.add(tx('옳은 보기',5.45,.54,15,GREEN,4.1))
   for label,formula,y in [('ㄱ','a=1',.24),('ㄴ','S(3)=6',-.12),('ㄷ',r'\int_{-2}^2(f-g)\,dx=\int_0^4(f-g)\,dx',-.48)]:
    self.add(tx(label,3.55,y,16,INK,.5),math(formula,5.65,y,18,GREEN,3.7,height=.28))
  else:
   self.add(tx('구하는 값',5.45,.49,15,MUTED,4.2))
   target=d['target'];ys=[-.12] if len(target)==1 else [.04,-.39]
   for item,y in zip(target,ys):
    self.add(tx(item[1],5.45,y,23,GREEN,4.25) if isinstance(item,list) else math(item,5.45,y,31 if len(target)==1 else 24,GREEN,4.25))
  for m in self.mobjects:
   assert m.get_left()[0]>-8 and m.get_right()[0]<8
   assert m.get_bottom()[1]>-.75 and m.get_top()[1]<.75,(self.episode,m.get_bottom(),m.get_top())
 def graph(self):
  d=json.loads((ROOT/'episodes/csat04_one_sided_limits/graph_data.json').read_text())
  def p(x,y):return [-1.5+x*1.12,-.11+y*.25,0]
  self.add(Line(p(-2.8,0),p(2.8,0),color=MUTED,stroke_width=.7),Line(p(0,-1.3),p(0,2.35),color=MUTED,stroke_width=.7))
  for pts in [d['left'],d['middle'],d['right']]:self.add(VMobject(color=CYAN,stroke_width=1.5).set_points_as_corners([p(x,y) for x,y in pts]).set_fill(opacity=0))
  for x,y in d['open_points']:self.add(Circle(radius=.032,color=INK,stroke_width=1,fill_color='#111B2E',fill_opacity=1).move_to(p(x,y)))
  for x,y in d['closed_points']:self.add(Dot(p(x,y),radius=.032,color=PURPLE))
  for x in [-1,1]:self.add(math(str(x),p(x,0)[0],-.27,11,MUTED,.3))
  for y in [-1,1,2]:self.add(math(str(y),-1.7,p(0,y)[1],11,MUTED,.3))
for i in range(1,23):globals()[f'Card{i:02d}']=type(f'Card{i:02d}',(ProblemCard,),{'episode':i})
