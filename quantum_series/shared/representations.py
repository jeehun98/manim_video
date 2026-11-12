"""Infinite square-well basis, coefficient maps and exactly linked representations."""
import numpy as np
from manim import *
from quantum_series.shared.theme import p,text,INK,MUTED,GOLD
BLUE='#48A9E6';PURPLE='#B28CFF';GREEN='#42C1AA';ORANGE='#F18A54'
C=np.sqrt([.5,.3,.2]);ENERGIES=np.array([1.,4.,9.]);H=np.diag(ENERGIES)
def basis(x):return np.sqrt(2)*np.sin(np.asarray(x)[...,None]*np.pi*np.arange(1,4))
def wave(x,coefficients=C):return basis(x)@coefficients
def energy_action(x,coefficients=C):return basis(x)@(H@coefficients)
def unitary(theta=np.pi/6):return np.array([[np.cos(theta),-np.sin(theta),0],[np.sin(theta),np.cos(theta),0],[0,0,1.]])
def transformed(theta=np.pi/6):
 u=unitary(theta);return u.conj().T@C,u.conj().T@H@u
class WellGraph(VGroup):
 def __init__(self,c,coefficients=C,title='ψ(x)',color=BLUE,width=5.7,height=2.15,show_walls=True):
  super().__init__();limit=max(2.5,float(np.max(abs(wave(np.linspace(0,1,1001),coefficients))))*1.15);self.ax=Axes(x_range=[0,1,.5],y_range=[-limit,limit,limit],x_length=width,y_length=height,tips=False,axis_config={'color':MUTED,'stroke_width':1}).move_to(c)
  self.curve=self.ax.plot(lambda x:float(np.real(wave(x,coefficients))),x_range=[0,1,.005],color=color,stroke_width=3);self.add(self.ax,self.curve)
  if show_walls:
   for x in [0,1]:self.add(Line(self.ax.c2p(x,-limit),self.ax.c2p(x,limit),color=MUTED,stroke_width=2))
  self.add(text(title,c[0],c[1]+height/2+.4,25,color,width=width),text('0',*(self.ax.c2p(0,0)+p(0,-.25))[:2],size=17,color=MUTED),text('L',*(self.ax.c2p(1,0)+p(0,-.25))[:2],size=17,color=MUTED))
class HydrogenLevels(VGroup):
 def __init__(self,c):
  super().__init__()
  for n in [1,2,3]:
   energy=-13.6/n**2;y=c[1]+(energy+7)/5
   label_x=c[0]+(-2.25 if n==2 else 2.25 if n==3 else 0)
   label_y=y+(.15 if n==2 else .05 if n==3 else .25)
   self.add(Line(p(c[0]-1.8,y),p(c[0]+1.8,y),color=GOLD),text(f'n={n}  {energy:.2f} eV',label_x,label_y,18,GOLD,width=2.7))
class EnergyLevels(VGroup):
 def __init__(self,c):
  super().__init__()
  for n,e in enumerate(ENERGIES,1):
   y=c[1]+(e-5)/4;self.add(Line(p(c[0]-1.7,y),p(c[0]+1.7,y),color=GOLD),text(f'E{n} = {int(e)} E₁',c[0],y+.23,23,GOLD))
def lattice(c):return VGroup(*[Dot(c+p((x-3)*.42,(y-1.5)*.42),color=BLUE,radius=.06) for x in range(7) for y in range(4)])
def packet(c):return ParametricFunction(lambda x:c+p(x,.65*np.exp(-x*x/2)*np.cos(6*x)),t_range=[-2.7,2.7,.03],color=BLUE)
