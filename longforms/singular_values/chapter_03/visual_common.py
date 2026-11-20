from manim import *
import numpy as np
import json,textwrap
from pathlib import Path
config.background_color='#0d121d'
config.frame_width=14.222222
config.frame_height=8
BLUEC='#58a6ff'; ORANGE='#ff963e'; GREEN='#47e78b'; PURPLE='#bd87ff'; MUTED='#94a3b8'
ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))
B=np.array([[1.,2.],[0.,1.]])
def txt(s,size=28,color=WHITE):return Text(s,font='Malgun Gothic',font_size=size,color=color)
def label(s,p,size=28,color=WHITE):return txt(s,size,color).move_to(p)
def arrow(c,v,color,scale=1):return Arrow(np.array(c),np.array(c)+np.r_[v,0]*scale,buff=0,stroke_width=4,max_tip_length_to_length_ratio=.16,color=color)
def clipped(p,q):
 d=q-p;lo=0.;hi=1.
 for k,limit in [(0,2.75),(1,1.7)]:
  if abs(d[k])<1e-9:
   if abs(p[k])>limit:return None
  else:
   a,b=sorted(((-limit-p[k])/d[k],(limit-p[k])/d[k]));lo=max(lo,a);hi=min(hi,b)
 if hi<=lo:return None
 return p+lo*d,p+hi*d

def grid(c,M=np.eye(2),scale=.9):
 g=VGroup();c=np.array(c)
 for axis in [0,1]:
  for x in np.arange(-5,5.01,.5):
   p=np.array([x,-5.]) if axis==0 else np.array([-5.,x]);q=np.array([x,5.]) if axis==0 else np.array([5.,x])
   pair=clipped(M@p*scale,M@q*scale)
   if pair:
    a,b=pair;g.add(Line(c+np.r_[a,0],c+np.r_[b,0],color=MUTED,stroke_width=1,stroke_opacity=.38 if abs(x)<.01 else .13))
 return g

def shape(c,M=np.eye(2),color=BLUEC,scale=.9):
 c=np.array(c);pts=[c+np.r_[M@np.array(p)*scale,0] for p in [(0,0),(1,0),(1,1),(0,1)]]
 return VGroup(Polygon(*pts,color=color,fill_opacity=.14,stroke_width=3),arrow(c,M@np.array([1,0]),color,scale),arrow(c,M@np.array([0,1]),color,scale))
