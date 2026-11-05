"""Mercury tube and internal energy-state symbols; positions supplied by layout."""
from manim import *
from quantum_series.shared.theme import text,p,INK,MUTED,GOLD
CYAN='#43C5F4';HG='#D6A25B';RED='#F18A54';UV='#B28CFF';GREEN='#4DB6AC'
class Tube(VGroup):
 def __init__(self,L):
  super().__init__();self.origin=L.tube_center;self.factor=L.tube_scale
  self.add(RoundedRectangle(width=6.7,height=1.75,corner_radius=.2,color=MUTED,stroke_width=2))
  self.add(Rectangle(width=4.25,height=1.65,stroke_width=0,fill_color=GREEN,fill_opacity=.07).move_to(p(-.475,0)))
  self.add(Rectangle(width=1.1,height=1.65,stroke_width=0,fill_color=RED,fill_opacity=.12).move_to(p(2.2,0)))
  for x,label in [(-2.9,'음극'),(1.65,'격자'),(2.75,'검출부')]:
   self.add(Line(p(x,-.68),p(x,.68),color=GOLD if x<0 else INK,stroke_width=3),text(label,x,-1.12,19))
  self.add(text('가속 구간',-.55,.58,18,GREEN),text('감속',2.2,.58,16,RED))
  for x,y in [(-1.8,.12),(-.8,-.35),(.15,.24),(.95,-.32)]:
   self.add(Circle(radius=.13,color=HG,fill_color=HG,fill_opacity=.25).move_to(p(x,y)))
  self.add(text('Hg · 수은 증기',-.6,1.13,20,HG))
  self.scale(self.factor).shift(self.origin)
 def at(self,x,y=0):
  local=-2.6+4.25*x if x<=1 else 1.65+(x-1)*5
  return self.origin+p(local*self.factor,y*self.factor)
 def collector(self,y=0):return self.origin+p(2.75*self.factor,y*self.factor)
class Levels(VGroup):
 def __init__(self,center,width=2.3):
  super().__init__();self.low=center+p(0,-.65);self.high=center+p(0,.65)
  self.add(Line(self.low+p(-width/2,0),self.low+p(width/2,0),color=CYAN),Line(self.high+p(-width/2,0),self.high+p(width/2,0),color=GOLD))
  self.add(text('바닥 상태',*(self.low[:2]+[0,-.3]),size=18,color=CYAN),text('들뜬 상태',*(self.high[:2]+[0,.3]),size=18,color=GOLD))
  self.marker=Dot(self.low,radius=.09,color=GOLD);self.add(self.marker)
  self.add(text('ΔE ≈ 4.9 eV',*(center[:2]+[0,0]),size=22,color=GOLD,width=width))
