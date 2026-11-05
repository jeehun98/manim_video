"""Calculated string modes, amplitude slices, Coulomb potential and energy levels."""
import numpy as np
from functools import lru_cache
from manim import *
from quantum_series.shared.theme import p,text,INK,MUTED,GOLD,BG
from quantum_series.episodes.ep08_schrodinger.physics_model import psi_slice,standing
BLUE='#579CFF';GREEN='#42C1AA';ORANGE='#E58A65';NUCLEUS='#F26C65';LEVEL='#739CE8'
def string_curve(center,mode=1,time=0,width=6.4,amplitude=.55,mixed=False):
 def point(u):
  value=standing(u,time,mode)
  if mixed:value=.65*standing(u,time,1)+.28*standing(u,time+.4,2)+.18*standing(u,time+.7,3)
  return center+p(width*(u-.5),amplitude*value)
 return VMobject(color=GREEN if float(mode).is_integer() else ORANGE,stroke_width=3).set_points_as_corners([point(u) for u in np.linspace(0,1,301)])
def fixed_string(center,width=6.4):
 return VGroup(Line(center+p(-width/2,0),center+p(width/2,0),color=MUTED,stroke_width=1),Dot(center+p(-width/2,0),color=GOLD,radius=.07),Dot(center+p(width/2,0),color=GOLD,radius=.07))
@lru_cache(maxsize=16)
def field_pixels(n,l,resolution=360):
 extent=5 if n==1 else (14 if n==2 else 26)
 axis=np.linspace(-extent,extent,resolution);x,z=np.meshgrid(axis,axis[::-1]);v=psi_slice(x,z,n,l);strength=np.abs(v)/np.max(np.abs(v))
 base=np.array([11,16,32]);positive=np.array([87,156,255]);negative=np.array([229,138,101]);color=np.where((v>=0)[...,None],positive,negative)
 rgb=base+(color-base)*strength[...,None]**.7
 return np.clip(rgb,0,255).astype(np.uint8)
class AtomicField(Group):
 def __init__(self,center,n=1,l=0,size=3.5,label=True,nucleus=True):
  super().__init__();self.image=ImageMobject(field_pixels(n,l)).set_resampling_algorithm(RESAMPLING_ALGORITHMS['bilinear']).set_width(size).move_to(center)
  self.add(self.image)
  if nucleus:self.add(Dot(center,radius=.055,color=NUCLEUS))
  if label:
   name=f'{n}'+('s' if l==0 else 'p_z')
   self.add(text(f'ψ · {name} 공간 부분 단면',center[0],(center[1]+size*.36 if size>=3.8 else center[1]+size/2+.25),20,BLUE,width=size+.6))
class EnergySpectrum(VGroup):
 def __init__(self,center,width=2.4,height=2.8,label='',values=None):
  super().__init__();self.levels={};self.center_point=center
  self.y=lambda e:center[1]+(e+14)/14*height-height/2
  energies=[-13.6,-3.4,-13.6/9,-.85] if values is None else values
  for n,e in enumerate(energies,1):
   yy=self.y(e);line=Line(p(center[0]-width/2,yy),p(center[0]+width/2,yy),color=GOLD if n==1 else LEVEL,stroke_width=2);self.levels[n]=line;self.add(line)
   # n=3/4 are too close for separate adjacent text: show only representative n=1/2 values.
   if n<=2:self.add(text(f'{e:.2f} eV',center[0],yy-.23,18,GOLD if n==1 else LEVEL,width=width))
  zero=self.y(0);self.add(DashedLine(p(center[0]-width/2,zero),p(center[0]+width/2,zero),color=MUTED),text('0 · 이온화 경계',center[0],zero+.28,17,MUTED,width=width+.5))
  if label:
   self.label_mobject=text(label,center[0],center[1]-height/2-.85,24,INK,width=width+1);self.add(self.label_mobject)
class PotentialPlot(VGroup):
 def __init__(self,center,width=5.5,height=2.5):
  super().__init__();self.axes=Axes(x_range=[0,6,1],y_range=[-4,0,1],x_length=width,y_length=height,tips=False,axis_config={'color':MUTED,'stroke_width':1}).move_to(center)
  self.curve=self.axes.plot(lambda r:-1/r,x_range=[.25,6],color=ORANGE);self.add(self.axes,self.curve,text('거리 r →',center[0],center[1]-height/2-.42,21,MUTED),text('퍼텐셜 에너지 V(r) ∝ −1/r',center[0],center[1]+height/2+.4,24,ORANGE,width=width+1))
