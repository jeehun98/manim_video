"""Wave-value illustrations, never paths of a wiggling electron."""
import numpy as np
from manim import *
from quantum_series.shared.theme import p,text,INK,MUTED,GOLD
WAVE='#579CFF';MATCH='#42C1AA';MISMATCH='#E58A65';NUCLEUS='#F26C65';ELECTRON='#48A9E6'
def circular_point(u,cycles,center,radius=1.85,amplitude=.18):
 theta=TAU*u;r=radius+amplitude*np.cos(cycles*theta)
 return center+p(r*np.cos(theta),r*np.sin(theta))
def straight_point(u,cycles,center,width=6.7,amplitude=.32):
 return center+p(width*(u-.5),amplitude*np.cos(TAU*cycles*u))
def sampled_curve(function,color=WAVE):
 return VMobject(color=color,stroke_width=3).set_points_as_corners([function(u) for u in np.linspace(0,1,421)])
class BohrAtom(VGroup):
 def __init__(self,center,radii=(.85,1.5,2.2),color=MATCH):
  super().__init__();self.center_point=center
  self.orbits=VGroup(*[Circle(radius=r,color=color,stroke_width=1.7).move_to(center) for r in radii]);self.add(self.orbits,Dot(center,radius=.11,color=NUCLEUS),text('+',center[0],center[1],18,INK))
class WavePair(VGroup):
 def __init__(self,L,cycles,color=WAVE):
  super().__init__();self.L=L;self.cycles=cycles
  self.circle=Circle(radius=L.radius,color=MUTED,stroke_width=1.5).move_to(L.ring)
  self.line=Line(L.straight+p(-L.straight_width/2,0),L.straight+p(L.straight_width/2,0),color=MUTED,stroke_width=1.5)
  self.circular=sampled_curve(lambda u:circular_point(u,cycles,L.ring,L.radius),color)
  self.flat=sampled_curve(lambda u:straight_point(u,cycles,L.straight,L.straight_width,L.flat_amplitude),color)
  self.add(self.circle,self.line,self.circular,self.flat)
  self.add(Dot(L.ring,radius=.08,color=NUCLEUS),text('원형 경로',L.ring[0],(L.ring[1]+L.radius+.52 if L.portrait else -2.25),23,MUTED))
  self.count=text(f'둘레 2πr = {cycles:g}λ',L.straight[0],L.straight[1]+1.0,26,color)
  self.add(self.count)
 def ringpoint(self,u):return circular_point(u,self.cycles,self.L.ring,self.L.radius)
 def flatpoint(self,u):return straight_point(u,self.cycles,self.L.straight,self.L.straight_width,self.L.flat_amplitude)
 def endpoints(self):
  return VGroup(Dot(self.flatpoint(0),color=GOLD,radius=.075),Dot(self.flatpoint(1),color=GOLD,radius=.075),text('A · 출발',*(self.L.straight[:2]+[-self.L.straight_width/2+.45,.75]),size=18,color=GOLD),text('A · 한 바퀴 뒤',*(self.L.straight[:2]+[self.L.straight_width/2-.7,.75]),size=18,color=GOLD))
 def phase_indicator(self):
  m=self.cycles;matched=abs(np.exp(TAU*1j*m)-1)<1e-9;color=MATCH if matched else MISMATCH
  phaseword=f'{2*m:g}π';label=f'Δφ = {phaseword}   ·   '+('같은 위상' if matched else '반대 위상')
  return text(label,self.L.straight[0],self.L.phase_y,size=25,color=color,width=6.8 if self.L.portrait else 6.1)
def matter_wave(center,cycles=3,width=5.8,amplitude=.4,color=WAVE):
 return sampled_curve(lambda u:straight_point(u,cycles,center,width,amplitude),color)
def abstract_state(center,width=5.8):
 group=VGroup()
 for j in range(-3,4):
  def f(u,j=j):
   x=(u-.5)*width;envelope=np.exp(-x*x/5)
   return center+p(x,j*.28+.32*envelope*np.cos(4*x+j*.5))
  group.add(sampled_curve(f,WAVE if j%2 else MATCH).set_stroke(opacity=.75-abs(j)*.1))
 return group
