"""One animation logic with native portrait and landscape compositions."""
import json
from pathlib import Path
import numpy as np
from manim import *
from longforms.qcs01_speed.direction import QCSScene,PORTRAIT,L
from quantum_series.shared.theme import text

HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
BG,BLUE,GREEN,AMBER,INK,MUTED='#0B1020','#60A5FA','#34D399','#FBBF24','#E5E7EB','#8D9BB6'
config.background_color=BG

def pt(x,y):return np.array([x,y,0.])
def at(short,long):return pt(*(short if PORTRAIT else long))
def say(s,short=(0,0),long=(0,0),size=30,color=INK,width=None):
 x,y=(short if PORTRAIT else long)
 return text(s,x=x,y=y,size=size,color=color,width=width or (7.5 if PORTRAIT else 13.8))

def card(s,short=(0,0),long=(0,0),w=5,h=1,color=BLUE,size=27):
 center=at(short,long)
 return VGroup(RoundedRectangle(width=w,height=h,corner_radius=.15,color=color,fill_color=color,fill_opacity=.07).move_to(center),text(s,*center[:2],size,color,w-.3))

def utterance():
 words=VGroup(*[text(s,size=37 if PORTRAIT else 32,color=BLUE) for s in ['그거','거기','놓아줘.']]).arrange(RIGHT,buff=.3)
 words.move_to(at((0,3.5),(-4.1,1.1)))
 rect=RoundedRectangle(width=7.3 if PORTRAIT else 6.2,height=1.25 if PORTRAIT else 1.1,corner_radius=.2,color=BLUE,fill_color=BLUE,fill_opacity=.06).move_to(words)
 return VGroup(rect,words)

def place_sentence():
 return card('우리 지난번에 갔던 곳으로 가자.',(0,3.5),(0,1.85),w=7.5 if PORTRAIT else 10,h=1.1,color=BLUE,size=30)

def book(center,color=GREEN):
 x,y=center[:2]
 return VGroup(RoundedRectangle(width=1.1,height=.78,corner_radius=.06,color=color,fill_color=color,fill_opacity=.2).move_to(center),Line(pt(x-.35,y-.35),pt(x-.35,y+.35),color=color),text('책',x=x+.1,y=y,size=22,color=color))

def desk(x,y):
 return VGroup(Rectangle(width=2.8,height=.18,color=GREEN,fill_color=GREEN,fill_opacity=.25).move_to(pt(x,y)),Line(pt(x-1.1,y-.1),pt(x-1.1,y-1.12),color=GREEN),Line(pt(x+1.1,y-.1),pt(x+1.1,y-1.12),color=GREEN),text('책상',x=x,y=y-1.45,size=23,color=GREEN))

def person(center,color=GREEN):
 x,y=center[:2]
 return VGroup(Circle(radius=.23,color=color).move_to(pt(x,y+.38)),Arc(radius=.48,start_angle=0,angle=PI,color=color).move_to(pt(x,y-.2)),Line(pt(x-.47,y-.2),pt(x+.47,y-.2),color=color))

def location(name,center,color=GREEN,scale=1):
 x,y=center[:2]
 roof=Polygon(pt(-.65,.3),pt(0,.85),pt(.65,.3),color=color)
 base=Rectangle(width=1.05,height=.8,color=color).move_to(pt(0,-.1))
 door=Rectangle(width=.25,height=.45,color=color).move_to(pt(0,-.27))
 icon=VGroup(roof,base,door).scale(scale).move_to(center)
 lab=text(name,x=x,y=y-.85*scale-.18,size=24,color=color)
 return VGroup(icon,lab)

def network(center,seed=1,scale=1,color=GREEN):
 rng=np.random.default_rng(seed)
 xy=rng.uniform([-2,-1.3],[2,1.3],size=(12,2))*scale
 dots=VGroup(*[Dot(center+pt(x,y),radius=.055,color=color) for x,y in xy])
 edges=VGroup(*[Line(dots[i].get_center(),dots[(i+1)%12].get_center(),color=color,stroke_width=1.1,stroke_opacity=.45) for i in range(12)],*[Line(dots[i].get_center(),dots[(i+4)%12].get_center(),color=color,stroke_width=1,stroke_opacity=.25) for i in range(0,12,2)])
 return VGroup(edges,dots)

def connect(a,b,color=GREEN,buff=.18):
 return Arrow(a.get_center(),b.get_center(),buff=buff,color=color,stroke_width=2,max_tip_length_to_length_ratio=.13).set_z_index(-1)

class BaseExpressionScene(QCSScene):
 data=DATA

 def replace(self,old,new):return Scene.replace(self,old,new)

 def setup(self):
  super().setup()
  old=self.mobjects[0];self.remove(old)
  self.brand=text('과학 한조각  /  표현은 무엇을 전달하는가?',y=L.brand_y,size=17,color=MUTED,width=7.6 if PORTRAIT else 14)
  self.add(self.brand)
  self.body_checks=[]

 def clear_body(self):
  keep=[self.title,self.caption,self.caption_panel,self.brand]
  objects=[o for o in self.mobjects if all(o is not k for k in keep) and o.get_center()[1]<(6.5 if PORTRAIT else 3.6)]
  if objects:self.play(*[FadeOut(o) for o in objects],run_time=.4)

 def check_body(self):
  for o in self.mobjects:
   if o is self.caption or o is self.caption_panel:continue
   if not o.width or not o.height:continue
   assert o.get_left()[0]>=-config.frame_width/2+.12 and o.get_right()[0]<=config.frame_width/2-.12,(self.info['id'],'horizontal',o)
   assert o.get_bottom()[1]>=(-4.9 if PORTRAIT else -2.6),(self.info['id'],'subtitle overlap',o)

 def play(self,*args,**kwargs):
  result=super().play(*args,**kwargs)
  self.check_body()
  return result
