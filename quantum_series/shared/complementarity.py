"""Two-path amplitudes and marker overlap; finite-screen educational model.
The common raised-cosine envelope makes the path amplitudes orthogonal on [-3,3].
This allows exact normalization for every complex marker overlap, without rescaling flux.
"""
from functools import lru_cache
import numpy as np
from PIL import Image,ImageDraw
from manim import *
from quantum_series.shared.theme import text,p,INK,MUTED,GOLD,BG
BLUE='#48A9E6';GREEN='#42C1AA';PURPLE='#B28CFF';ORANGE='#F1A56A'
Q=5*np.pi/3

def envelope(x):
 x=np.asarray(x);return np.where(abs(x)<=3,np.cos(np.pi*x/6)**2/3,0.)
def amplitudes(x):
 x=np.asarray(x);a=np.sqrt(envelope(x)/2)*np.exp(-.5j*Q*x);b=np.sqrt(envelope(x)/2)*np.exp(.5j*Q*x);return a,b
def probability(x,overlap=1.):
 a,b=amplitudes(x)
 return abs(a)**2+abs(b)**2+2*np.real(np.conj(a)*b*overlap)
def marker_overlap(distinguishability):return np.sqrt(max(0.,1-distinguishability**2))
@lru_cache(maxsize=16)
def samples(distinguishability,count=2000):
 grid=np.linspace(-3,3,24001);pdf=probability(grid,marker_overlap(distinguishability));cdf=np.concatenate(([0.],np.cumsum((pdf[:-1]+pdf[1:])*.5*np.diff(grid))));cdf/=cdf[-1]
 rng=np.random.default_rng(202712);u=rng.random(count);x=np.interp(u,cdf,grid);y=rng.uniform(-.47,.47,count);records=np.random.default_rng(1).integers(0,2,count)
 return np.column_stack((x,y,records))
def detection_image(distinguishability,n,width=930,height=160):
 im=Image.new('RGB',(width,height),BG);draw=ImageDraw.Draw(im)
 for x,y,record in samples(float(distinguishability))[:n]:
  ix=(x+3)/6*(width-1);iy=(.5-y)*(height-1);draw.ellipse((ix-1.3,iy-1.3,ix+1.3,iy+1.3),fill=GOLD)
 return np.asarray(im)
class ElectronSource(VGroup):
 def __init__(self,c):
  super().__init__(RoundedRectangle(width=.65,height=.6,corner_radius=.08,color=MUTED).move_to(c+p(-2.7,0)),text('전자총',*(c+p(-2.7,-.75))[:2],size=21,color=MUTED))
class DoubleSlit(VGroup):
 def __init__(self,c):
  super().__init__();self.slit_positions=[c+p(-.75,0),c+p(-.05,0)]
  self.add(Rectangle(width=1.4,height=1.8,color=MUTED,fill_opacity=.08).move_to(c+p(-.4,0)))
  for name,point in zip(['A','B'],self.slit_positions):self.add(Rectangle(width=.13,height=.85,color=BLUE,fill_color=BG,fill_opacity=1).move_to(point),text(name,*(point+p(0,.7))[:2],size=23,color=BLUE))
  self.add(text('두 슬릿 · 정면 표시',*(c+p(-.4,1.3))[:2],size=20,color=MUTED))
class WhichPathMarker(VGroup):
 def __init__(self,c,active=False):
  super().__init__();self.record_boxes=[]
  for name,x in [('A',-.75),('B',-.05)]:
   box=RoundedRectangle(width=.5,height=.37,corner_radius=.04,color=PURPLE,fill_opacity=.3 if active else .02).move_to(c+p(x,-1.05));self.record_boxes.append(box);self.add(box,text(name,*(c+p(x,-1.05))[:2],size=18,color=PURPLE))
class Apparatus(VGroup):
 def __init__(self,c,active=False):
  super().__init__();self.center_point=c;self.source=ElectronSource(c);self.slits=DoubleSlit(c);self.marker=WhichPathMarker(c,active)
  self.add(self.source,self.slits,Arrow(c+p(-2.3,0),c+p(-1.3,0),buff=0,color=BLUE),Rectangle(width=.1,height=2,color=MUTED).move_to(c+p(2.65,0)),text('검출 화면',*(c+p(2.65,1.3))[:2],size=20,color=MUTED),self.marker)
  self.add(text('경로 기록 ON' if active else '경로 기록 OFF',*(c+p(1.75,-1.25))[:2],size=18,color=PURPLE if active else MUTED))
class DetectorScreen(VGroup):
 def __init__(self,c):super().__init__(Rectangle(width=6.2,height=1.05,color=MUTED).move_to(c));self.center_point=c
 def image(self,d,n):return ImageMobject(detection_image(d,n)).set_width(6.16).move_to(self.center_point)
 def at(self,sample):return self.center_point+p(sample[0]*6.16/6,sample[1]*1.02)
class ProbabilityProfile(VGroup):
 def __init__(self,c,tracker):
  super().__init__();self.tracker=tracker
  self.ax=Axes(x_range=[-3,3,1],y_range=[0,.7,.2],x_length=6.0,y_length=1.15,tips=False,axis_config={'color':MUTED,'stroke_width':1}).move_to(c)
  self.add(self.ax,text('전자만 집계한 검출 확률밀도',*(c+p(0,.85))[:2],size=22,color=INK,width=6.3),text('화면의 위치 x',*(c+p(0,-.85))[:2],size=18,color=MUTED))
  self.curve=always_redraw(self.draw_curve);self.add(self.curve)
 def draw_curve(self):
  d=self.tracker.get_value();return self.ax.plot(lambda x:float(probability(x,marker_overlap(d))),x_range=[-3,3,.025],color=GREEN if d<.95 else ORANGE,stroke_width=3)
 def freeze(self):self.curve.clear_updaters()
 def histogram(self,d,n):
  counts,edges=np.histogram(samples(d)[:n,0],bins=36,range=(-3,3),density=True)
  return VGroup(*[Rectangle(width=self.ax.x_axis.unit_size*(edges[1]-edges[0])*.8,height=max(.002,self.ax.y_axis.unit_size*h),stroke_width=0,fill_color=GOLD,fill_opacity=.25).move_to(self.ax.c2p((edges[i]+edges[i+1])/2,h/2)) for i,h in enumerate(counts)])
