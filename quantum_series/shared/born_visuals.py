"""Detector events and density diagrams all share one underlying sample sequence."""
import numpy as np
from PIL import Image,ImageDraw
from manim import *
from quantum_series.shared.theme import p,text,INK,MUTED,GOLD
from quantum_series.episodes.ep09_born.simulation import samples,density,psi,histogram,angular_amplitudes,angular_probabilities
BLUE='#48A9E6';GREEN='#42C1AA';ORANGE='#F18A54';PURPLE='#B28CFF';RED='#F26C65'
class Detector(VGroup):
 def __init__(self,L):
  super().__init__();self.L=L;self.center_point=L.detector_center;self.width_value=L.detector_width;self.height_value=L.detector_height
  self.add(RoundedRectangle(width=self.width_value,height=self.height_value,corner_radius=.1,color=MUTED,stroke_width=1.5).move_to(self.center_point))
  self.add(text('검출 화면 · 동일한 준비 상태',self.center_point[0],self.center_point[1]+self.height_value/2+(.4 if L.portrait else .28),23,MUTED,width=self.width_value))
 def at(self,xy):return self.center_point+p(xy[0]/8*(self.width_value-.04),xy[1]/4*(self.height_value-.04))
 def image(self,n):
  w,h=900,400;im=Image.new('RGB',(w,h),(11,16,32));draw=ImageDraw.Draw(im)
  for x,y in samples()[:n]:
   px=(x+4)/8*w;py=(2-y)/4*h;draw.ellipse((px-1.4,py-1.4,px+1.4,py+1.4),fill=(255,209,102))
  return ImageMobject(np.asarray(im)).set_width(self.width_value-.04).stretch_to_fit_height(self.height_value-.04).move_to(self.center_point)
class DensityPlot(VGroup):
 def __init__(self,center,width=6.3,height=2.05):
  super().__init__();self.center_point=center
  self.axes=Axes(x_range=[-4,4,2],y_range=[0,.6,.2],x_length=width,y_length=height,tips=False,axis_config={'color':MUTED,'stroke_width':1.3}).move_to(center);self.add(self.axes)
  self.add(text('검출 위치 x',center[0],center[1]-height/2-.45,21,MUTED),text('확률밀도 · 정규화한 빈도',center[0],center[1]+height/2+.35,21,GREEN,width=width))
  for x in [-4,0,4]:self.add(text(str(x),*self.axes.c2p(x,0)[:2]+[0,-.18],size=15,color=MUTED))
 def curve(self):return self.axes.plot(lambda x:float(density(x)),x_range=[-4,4,.04],color=GREEN,stroke_width=3)
 def bars(self,n):
  edges,counts,heights=histogram(n);bars=VGroup()
  for i,height in enumerate(heights):
   if height<=0:continue
   a=self.axes.c2p(edges[i],0);b=self.axes.c2p(edges[i+1],height)
   bars.add(Rectangle(width=b[0]-a[0],height=b[1]-a[1],fill_color=GOLD,fill_opacity=.32,stroke_color=GOLD,stroke_width=.6).move_to((a+b)/2))
  return bars
class WavePlot(VGroup):
 def __init__(self,center,width=5.6,height=1.7,kind='real',label=''):
  super().__init__();low=-.8 if kind=='real' else 0;high=.8 if kind=='real' else .6
  self.axes=Axes(x_range=[-4,4,2],y_range=[low,high,high-low],x_length=width,y_length=height,tips=False,axis_config={'color':MUTED,'stroke_width':1}).move_to(center);self.add(self.axes)
  f=(lambda x:float(np.real(psi(x)))) if kind=='real' else (lambda x:float(density(x)))
  self.curve=self.axes.plot(f,x_range=[-4,4,.04],color=BLUE if kind=='real' else GREEN,stroke_width=3);self.add(self.curve)
  if label:self.add(text(label,center[0],center[1]+height/2+.4,23,BLUE if kind=='real' else GREEN,width=width))
class Scattering(VGroup):
 def __init__(self,L):
  super().__init__();self.center_point=L.scatter_center;self.angles=np.linspace(-2.5,2.5,7);self.radius=1.75
  self.add(Dot(self.center_point,radius=.1,color=RED),DashedVMobject(Circle(radius=.32,color=MUTED).move_to(self.center_point),num_dashes=12))
  self.add(RoundedRectangle(width=.5,height=.45,corner_radius=.07,color=MUTED).move_to(self.center_point+p(-3.1,0)),text('전자원',*(self.center_point[:2]+[-3.1,-.55]),size=18,color=MUTED))
 def at(self,i):return self.center_point+self.radius*p(np.cos(self.angles[i]),np.sin(self.angles[i]))
 def rays(self):return VGroup(*[DashedVMobject(Line(self.center_point,self.at(i),color=BLUE),num_dashes=15) for i in range(7)])
 def bars(self,probability=False):
  values=angular_probabilities() if probability else abs(angular_amplitudes());values=values/max(values);group=VGroup()
  for i,value in enumerate(values):
   point=self.at(i);unit=p(np.cos(self.angles[i]),np.sin(self.angles[i]));group.add(Line(point,point+unit*.65*value,color=GREEN if probability else BLUE,stroke_width=5))
  return group
