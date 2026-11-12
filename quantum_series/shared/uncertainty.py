"""Normalized Gaussian states and reusable fixed-axis uncertainty visuals.
Units: hbar=m=1. Momentum panels use q=p-p0, with p0=k0.
"""
import numpy as np
from manim import *
from quantum_series.shared.theme import text,p,INK,MUTED,GOLD
BLUE='#48A9E6';GREEN='#42C1AA';ORANGE='#F18A54';PURPLE='#B28CFF'
def psi(x,sigma=1,k0=6):
 return (2*np.pi*sigma*sigma)**(-.25)*np.exp(-np.asarray(x)**2/(4*sigma*sigma))*np.exp(1j*k0*np.asarray(x))
def density(x,sigma):return np.exp(-np.asarray(x)**2/(2*sigma*sigma))/(np.sqrt(2*np.pi)*sigma)
def momentum_std(sigma):return 1/(2*sigma)
def free_psi(x,t,sigma=.65,k0=1.2):
 z=1+1j*t/(2*sigma*sigma)
 return (2*np.pi*sigma*sigma)**(-.25)/np.sqrt(z)*np.exp(-(np.asarray(x)-k0*t)**2/(4*sigma*sigma*z))*np.exp(1j*(k0*np.asarray(x)-k0*k0*t/2))
def component_sum(x,sigma=.7,k0=6,count=81):
 k=np.linspace(k0-7,k0+7,count);dk=k[1]-k[0]
 # Fourier amplitude, normalized for the chosen convention; tails outside +-7 negligible.
 phi=(2*sigma*sigma/np.pi)**.25*np.exp(-sigma*sigma*(k-k0)**2)
 return np.sum(phi[:,None]*np.exp(1j*k[:,None]*np.atleast_1d(x)),axis=0)*dk/np.sqrt(2*np.pi)
class PlaneWave(VGroup):
 def __init__(self,c,k=6,phase=0,amp=.5,color=BLUE):
  super().__init__();self.add(ParametricFunction(lambda x:c+p(x,amp*np.cos(k*x-phase)),t_range=[-2.9,2.9,.025],color=color))
class WavePacket(VGroup):
 def __init__(self,c,sigma=.7,phase=0,k0=6):
  super().__init__();self.add(ParametricFunction(lambda x:c+p(x,float(np.real(psi(x,sigma,k0)*np.exp(-1j*phase)))),t_range=[-2.9,2.9,.025],color=BLUE))
  self.add(ParametricFunction(lambda x:c+p(x,float(abs(psi(x,sigma,k0)))),t_range=[-2.9,2.9,.04],color=MUTED,stroke_opacity=.6,stroke_width=1))
class Distribution(VGroup):
 def __init__(self,c,tracker,momentum=False):
  super().__init__();self.tracker=tracker;self.momentum=momentum;self.color=GOLD if momentum else GREEN
  self.ax=Axes(x_range=[-4,4,2],y_range=[0,1.2,.4],x_length=5.7,y_length=1.75,tips=False,axis_config={'color':MUTED,'stroke_width':1}).move_to(c)
  self.add(self.ax,text('운동량 확률밀도 |φ(pₓ)|²' if momentum else '위치 확률밀도 |ψ(x)|²',*(c+p(0,1.3))[:2],size=26,color=self.color,width=6.3))
  self.add(text('pₓ − 〈pₓ〉' if momentum else 'x − 〈x〉',*(c+p(0,-1.25))[:2],size=21,color=MUTED))
  for val in [-4,0,4]:self.add(text(str(val),*(self.ax.c2p(val,0)+p(0,-.25))[:2],size=17,color=MUTED))
  self.curve=always_redraw(self.make_curve);self.marks=always_redraw(self.make_marks);self.add(self.curve,self.marks)
 def sd(self):return momentum_std(self.tracker.get_value()) if self.momentum else self.tracker.get_value()
 def make_curve(self):
  sd=self.sd();return self.ax.plot(lambda x:float(density(x,sd)),x_range=[-4,4,.04],color=self.color,stroke_width=3)
 def make_marks(self):
  sd=self.sd();return VGroup(*[DashedLine(self.ax.c2p(s*sd,0),self.ax.c2p(s*sd,float(density(sd,sd))),color=self.color,stroke_width=1.2,dash_length=.06) for s in [-1,1]],Line(self.ax.c2p(-sd,.055),self.ax.c2p(sd,.055),color=self.color,stroke_width=3))
 def freeze(self):
  self.curve.clear_updaters();self.marks.clear_updaters()
class PositionDistribution(Distribution):
 def __init__(self,c,tracker):super().__init__(c,tracker,False)
class MomentumDistribution(Distribution):
 def __init__(self,c,tracker):super().__init__(c,tracker,True)
class GammaMicroscope(VGroup):
 def __init__(self,c):
  super().__init__();self.center_point=c
  electron=Dot(c,radius=.1,color=BLUE);lens=Ellipse(width=2.0,height=.27,color=MUTED).move_to(c+p(0,1.8));tube=Rectangle(width=1.9,height=.8,color=MUTED).move_to(c+p(0,2.25))
  self.add(electron,lens,tube,DashedLine(c,c+p(-.85,1.8),color=ORANGE),DashedLine(c,c+p(.85,1.8),color=ORANGE),text('수집 가능한 산란광 방향',*(c+p(0,3))[:2],size=21,color=MUTED,width=5.8),text('전자',*(c+p(0,-.4))[:2],size=23,color=BLUE))
