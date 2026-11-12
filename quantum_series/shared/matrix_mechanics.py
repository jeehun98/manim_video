"""Legible symbolic/numeric grids and spectrum diagrams without a TeX dependency."""
import numpy as np
from manim import *
from quantum_series.shared.theme import p,text,INK,MUTED,GOLD
ENTRY='#65B8E8';PRODUCT='#42C1AA';ORDER='#F18A54';LEVEL='#739CE8';WAVE='#B28CFF'
SUB=str.maketrans('0123456789','₀₁₂₃₄₅₆₇₈₉')
def symbol(i,j):return ('x'+str(i+1)+str(j+1)).translate(SUB)
class MatrixGrid(VGroup):
 def __init__(self,center,values=None,cell=.78,label='X',symbolic=True,size=25,indices=True):
  super().__init__();self.entries={};self.cells={};self.center_point=center
  if values is None:values=[[symbol(i,j) for j in range(3)] for i in range(3)]
  self.rows=len(values);self.cols=len(values[0]);w=self.cols*cell;h=self.rows*cell
  for i,row in enumerate(values):
   for j,value in enumerate(row):
    c=center+p((j-(self.cols-1)/2)*cell,((self.rows-1)/2-i)*cell)
    box=Rectangle(width=cell,height=cell,color=MUTED,stroke_width=.7,stroke_opacity=.28).move_to(c);entry=text(str(value),*c[:2],size=size,color=ENTRY if symbolic else INK,width=cell*.91)
    self.cells[i,j]=box;self.entries[i,j]=entry;self.add(box,entry)
  for sign in [-1,1]:
   x=center[0]+sign*(w/2+.13);self.add(Line(p(x,center[1]-h/2),p(x,center[1]+h/2),color=MUTED),Line(p(x,center[1]+h/2),p(x-sign*.13,center[1]+h/2),color=MUTED),Line(p(x,center[1]-h/2),p(x-sign*.13,center[1]-h/2),color=MUTED))
  if label:self.add(text(label,center[0],center[1]+h/2+.55,28,color=INK))
  if indices:
   for j in range(self.cols):self.add(text(str(j+1),center[0]+(j-(self.cols-1)/2)*cell,center[1]+h/2+.2,16,MUTED))
   for i in range(self.rows):self.add(text(str(i+1),center[0]-w/2-.4,center[1]+((self.rows-1)/2-i)*cell,16,MUTED))
 def highlight(self,i,j,color=GOLD):return SurroundingRectangle(self.cells[i,j],buff=.015,color=color,stroke_width=2.5)
 def row_highlight(self,i):return SurroundingRectangle(VGroup(*[self.cells[i,j] for j in range(self.cols)]),buff=.025,color=GOLD,stroke_width=2)
 def column_highlight(self,j):return SurroundingRectangle(VGroup(*[self.cells[i,j] for i in range(self.rows)]),buff=.025,color=GOLD,stroke_width=2)
class ThreeLevels(VGroup):
 def __init__(self,center,width=3.7,height=2.15):
  super().__init__();self.level_points=[]
  for i,energy in enumerate([0,1,3]):
   c=center+p(0,(energy/3-.5)*height);self.level_points.append(c)
   self.add(Line(c+p(-width/2,0),c+p(width/2,0),color=LEVEL),text(str(i+1),c[0]-width/2-.3,c[1],21,LEVEL))
  self.add(text('에너지 ↑',center[0],center[1]+height/2+.55,21,MUTED))
 def relation(self,i,j,x=0,color=GOLD):return DoubleArrow(self.level_points[i]+p(x,0),self.level_points[j]+p(x,0),buff=.04,color=color,stroke_width=2)
class SpectralLines(VGroup):
 def __init__(self,center,width=4.8,height=1.7):
  super().__init__();self.lines=[];self.bars=[]
  self.add(Line(center+p(-width/2,-height/2-.2),center+p(width/2,-height/2-.2),color=MUTED))
  for n,(col,opacity) in enumerate([(ENTRY,.9),(GOLD,.3),(WAVE,.55)]):
   x=center[0]+(n-1)*width/3
   line=Line(p(x,center[1]-height/2),p(x,center[1]+height/2),color=col,stroke_width=6);self.lines.append(line);self.add(line,text(f'ν{str(n+1).translate(SUB)}',x,center[1]-height/2-.5,21,col))
  self.add(text('진동수 ν →',center[0],center[1]-height/2-.95,21,MUTED))
 def strengths(self):
  for line,opacity in zip(self.lines,[.9,.3,.55]):line.set_opacity(opacity)
def index_chain(center,k=2,width=4.8):
 group=VGroup();xs=[center[0]-width/2,center[0],center[0]+width/2]
 for x,label in zip(xs,['1',str(k),'3']):group.add(Circle(radius=.26,color=GOLD).move_to(p(x,center[1])),text(label,x,center[1],23,GOLD))
 for i in range(2):group.add(Arrow(p(xs[i]+.3,center[1]),p(xs[i+1]-.3,center[1]),buff=0,color=PRODUCT,stroke_width=2))
 return group
