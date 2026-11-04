"""PCA animation from deterministic observations; no hand-picked PC angles."""
import os
import numpy as np
from manim import *
from data_model import *
VERT=os.environ.get('EIGEN_LAYOUT','longform')=='shorts'
config.frame_width=8 if VERT else 128/9;config.frame_height=128/9 if VERT else 8;config.background_color='#09121F'
BLUE='#458EFA';TEAL='#20BCA5';ORANGE='#F0A34E';PURPLE='#B68AFA';YELLOW='#F4CF63';INK='#EDF3F7';MUTED='#91A4BA';GRID='#26384D'
BOUNDS=[0,6,13,23,29,38,43,53,61,67,74,81,88,97,105,113,120,131,142,146]
TITLES=['점은 조금, 주요 방향은 크게?','데이터의 주요 방향을 찾는 PCA','어느 방향으로 가장 넓게 퍼질까?','평균을 기준으로 퍼짐을 요약','공분산의 고유벡터가 주성분 방향','타원이 원형에 가까워진다면','서로 가까워지는 두 고윳값','점 80개 중 4개만 바꿔보면','PCA를 다시 계산한 결과','같은 변화, 서로 다른 반응','왜 방향의 변화량이 다를까?','고윳값 사이의 간격, Eigengap','간격이 크면 첫 방향이 뚜렷하다','간격이 작으면 민감해질 수 있다','모든 방향의 분산이 같다면','작은 변화가 선택하는 방향','방향 변화와 데이터 변화는 다르다','고윳값의 크기와 간격을 함께 읽기','고윳값 하나만으로는 부족하다']
def txt(s,size=26,color=INK,width=None):
 m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.15)
 if width and m.width>width:m.scale_to_fit_width(width)
 return m

def num(x,d=3):
 x=float(x)
 if abs(x)<.5*10**(-d):x=0
 return f'{x:.{d}f}'.rstrip('0').rstrip('.')

def axis_line(point,points,color=TEAL,length=3.2,dashed=False):
 info=pca(points);theta=info['angle'];assert theta is not None;d=np.array([np.cos(theta),np.sin(theta)]);a=point(info['mean']-length*d);b=point(info['mean']+length*d)
 return DashedLine(a,b,color=color,stroke_width=2,dash_length=.10) if dashed else Line(a,b,color=color,stroke_width=4)
class Cloud(Group):
 def __init__(self,fn,origin=(0,.2,0),unit=.78,pc1=True,pc2=False,ghost=False,highlight=None,contour=False,radius=.037,grid=True,pc_length=3.2):
  super().__init__();self.fn=fn;self.origin=np.array(origin,dtype=float);self.unit=unit;self.show_pc1=pc1;self.show_pc2=pc2;self.pc_length=pc_length;self.callbacks=[];self.highlight=set([] if highlight is None else highlight)
  self.clock=ValueTracker(0);points=fn(0);self.info=pca(points);self.points_data=points
  if grid:
   for k in [-3,-2,-1,0,1,2,3]:
    self.add(Line(self.point([-3,k]),self.point([3,k]),color=GRID,stroke_width=.8,stroke_opacity=.35),Line(self.point([k,-3]),self.point([k,3]),color=GRID,stroke_width=.8,stroke_opacity=.35))
  if ghost and self.info['angle'] is not None:self.add(axis_line(self.point,points,MUTED,dashed=True).set_opacity(.8))
  self.outline=VMobject(color=MUTED,stroke_width=1.3,stroke_opacity=.35);self.has_contour=contour
  if contour:self.add(self.outline)
  self.dots=VGroup(*[Dot(self.point(q),radius=radius,color=PURPLE if j in self.highlight else BLUE,fill_opacity=.9) for j,q in enumerate(points)])
  self.second=DashedLine(self.point([-1,0]),self.point([1,0]),color=ORANGE,stroke_width=2,dash_length=.11);self.first=Line(self.point([-1,0]),self.point([1,0]),color=TEAL,stroke_width=4)
  self.add(self.dots,self.second,self.first,self.clock)
  self.clock.add_updater(lambda _:self.refresh());self.refresh()
 def point(self,v):return self.origin+self.unit*np.r_[np.array(v,dtype=float),0]
 def refresh(self):
  points=self.fn(self.clock.get_value());info=pca(points);self.points_data=points;self.info=info
  for dot,q in zip(self.dots,points):dot.move_to(self.point(q))
  if info['angle'] is None:self.first.set_opacity(0);self.second.set_opacity(0)
  else:
   d=np.array([np.cos(info['angle']),np.sin(info['angle'])]);d2=np.array([-d[1],d[0]]);mu=info['mean']
   self.first.put_start_and_end_on(self.point(mu-self.pc_length*d),self.point(mu+self.pc_length*d)).set_opacity(1 if self.show_pc1 else 0)
   self.second.put_start_and_end_on(self.point(mu-2.7*d2),self.point(mu+2.7*d2)).set_opacity(.8 if self.show_pc2 else 0)
  if self.has_contour:
   vals=info['values'];v=info['vectors'];theta=np.linspace(0,2*np.pi,97);ellipse=info['mean']+np.c_[2*np.sqrt(vals[0])*np.cos(theta),2*np.sqrt(vals[1])*np.sin(theta)]@v.T;self.outline.set_points_as_corners([self.point(q) for q in ellipse])
  for callback in self.callbacks:callback(info)
 def connect(self,callback):self.callbacks.append(callback);callback(self.info)
class EigengapScene(Scene):
 index=0
 def construct(self):
  self.i=self.index;duration=BOUNDS[self.i+1]-BOUNDS[self.i];self.footer=None;self.cache={};top=6.1 if VERT else 3.35
  self.add(txt('고윳값과 고유벡터  /  05',16,MUTED).move_to([0,top+.48,0]),txt(TITLES[self.i],30,width=7.2 if VERT else 13).move_to([0,top,0]),Line([-3.6 if VERT else -6.6,top-.45,0],[3.6 if VERT else 6.6,top-.45,0],color=GRID,stroke_width=1))
  i=self.i
  if i==0:
   plot=self.main(lambda t:perturb(SMALL,t),ghost=True,highlight=INDICES);self.note('점 4개만 이동 · 같은 데이터에서 PCA 재계산');self.wait(.6);self.play(plot.clock.animate.set_value(1),run_time=3.2);self.angle_arc(plot,SMALL,perturb(SMALL));self.note('최대 점 이동 0.099   ·   PC1 직선 회전 31.72°')
  elif i==1:
   plot=self.main(lambda t:data_for_cov((1-t)*C_SMALL+t*C_ELLIPSE),pc1=False);self.add(txt('PCA',41,YELLOW).move_to([0,4.0,0] if VERT else [3.5,1.5,0]),txt('Principal Component Analysis',18,MUTED,width=7 if VERT else 5.9).move_to([0,3.35,0] if VERT else [3.5,.75,0]));self.until(4);self.play(plot.clock.animate.set_value(1),run_time=2.5);self.note('주성분 분석 · 계산된 합성 데이터 80개')
  elif i==2:
   plot=self.main(lambda t:ELLIPSE,pc1=False,contour=True);theta=self.projection(plot,0);self.note('후보 방향에 투영한 데이터의 분산 비교')
   self.play(theta.animate.set_value(np.deg2rad(70)),run_time=2);self.play(theta.animate.set_value(np.pi/2),run_time=1.5);self.play(theta.animate.set_value(pca(ELLIPSE)['angle']),run_time=2.5);self.until(7);plot.show_pc1=True;plot.refresh();self.note('최대 투영 분산 = 3   ·   첫 번째 주성분 PC1')
  elif i==3:
   mu=np.array([.4,.2]);plot=self.main(lambda t:ELLIPSE+mu,pc1=False);mark=Dot(plot.point(mu),radius=.065,color=YELLOW);connectors=VGroup(*[Line(plot.point(q),plot.point(mu),color=MUTED,stroke_width=.7,stroke_opacity=.25) for q in (ELLIPSE+mu)[::6]]);self.add(connectors,mark);self.info_panel(plot,bars=False);self.note('평균을 기준으로 위치를 읽고 퍼짐을 계산')
   old_axes=VGroup(Line(plot.point([-3,0]),plot.point([3,0]),color=MUTED,stroke_width=1),Line(plot.point([0,-2]),plot.point([0,2]),color=MUTED,stroke_width=1));self.add(old_axes);self.play(old_axes.animate.shift(plot.unit*np.r_[mu,0]),run_time=2);self.add(txt('평균',19,YELLOW).move_to(plot.point(mu)+[.3,-.25,0]))
  elif i==4:
   plot=self.main(lambda t:ELLIPSE,pc1=False,pc2=True);self.info_panel(plot);self.note('Cv₁ = λ₁v₁   ·   λ₁ ≥ λ₂');self.until(5);plot.show_pc1=True;plot.refresh();self.play(Indicate(plot.first,color=TEAL,scale_factor=1.02),run_time=.8);self.note('PC1 = 가장 큰 고윳값에 대응하는 방향')
  elif i==5:
   plot=self.main(lambda t:data_for_cov((1-t)*C_ELLIPSE+t*C_ROUND),pc2=True,contour=True);self.info_panel(plot);self.play(plot.clock.animate.set_value(1),run_time=4);self.note('실제 점 좌표와 공분산을 함께 갱신')
  elif i==6:
   plot=self.main(lambda t:data_for_cov((1-t)*C_ROUND+t*C_SMALL),pc2=True);self.info_panel(plot);self.play(plot.clock.animate.set_value(1),run_time=5.5);self.until(6);self.note('분산 차이 0.12 → 0.01   ·   방향의 구별이 약해짐')
  elif i==7:
   plot=self.main(lambda t:perturb(SMALL,t),pc1=False,ghost=True,highlight=INDICES);self.info_panel(plot);self.note('전체 80개 중 보라색 4개만 수정');self.wait(1);self.play(plot.clock.animate.set_value(1),run_time=3.8);self.until(5);self.note('나머지 76개는 고정 · 최대 점 이동 0.099')
  elif i==8:
   plot=self.main(lambda t:perturb(SMALL,t),pc1=False,ghost=True,highlight=INDICES);plot.clock.set_value(1);plot.refresh();self.info_panel(plot);self.note('같은 점들에서 공분산과 PCA를 다시 계산');self.wait(.5);plot.show_pc1=True;plot.refresh();self.play(Create(plot.first),run_time=1);self.angle_arc(plot,SMALL,perturb(SMALL));self.note('PC1 직선의 회전량 31.72°')
  elif i==9:
   a,b=self.comparison();self.note('같은 4개 점에 같은 이동 · 공분산 변화도 동일');self.play(a.clock.animate.set_value(1),b.clock.animate.set_value(1),run_time=3.5);self.note('공분산 변화의 크기 ‖ΔC‖₂ = 0.01 (양쪽 동일)')
  elif i==10:
   self.comparison_bars();self.note('같은 교란에서 비교: 작은 간격이 더 민감할 수 있다')
  elif i==11:
   plot=self.main(lambda t:SMALL,pc2=True);self.info_panel(plot,cov=False);self.add(txt('Eigengap',37,YELLOW).move_to([0,4.4,0] if VERT else [3.5,1.7,0]),txt('λ₁ − λ₂',40,YELLOW).move_to([0,3.45,0] if VERT else [3.5,.75,0]));self.note('λ₁ ≥ λ₂   ·   고윳값은 단위 방향의 분산')
  elif i==12:
   plot=self.main(lambda t:ELLIPSE,pc2=True,contour=True);angle=pca(ELLIPSE)['angle'];theta=self.projection(plot,angle);self.note('PC1 분산 3   ·   PC2 분산 0.5');self.until(3);self.play(theta.animate.set_value(angle+np.pi/2),run_time=2);self.play(theta.animate.set_value(angle),run_time=2);self.note('첫 주성분의 퍼짐이 다른 방향보다 뚜렷하다')
  elif i==13:
   plot=self.main(lambda t:perturb(SMALL,t),ghost=True,highlight=INDICES);self.info_panel(plot);self.play(plot.clock.animate.set_value(1),run_time=3.5);self.angle_arc(plot,SMALL,perturb(SMALL));self.note('작은 Eigengap + 작은 변화 → 큰 회전 가능')
  elif i==14:
   plot=self.main(lambda t:ISO,pc1=False);self.info_panel(plot);self.note('C = I   ·   λ₁ = λ₂ = 1   ·   고유축은 유일하지 않음')
   for angle in np.linspace(0,np.pi,6,endpoint=False):
    d=np.array([np.cos(angle),np.sin(angle)]);self.add(Line(plot.point(-2.7*d),plot.point(2.7*d),color=MUTED,stroke_width=1,stroke_opacity=.45))
   theta=self.candidate(plot,0);self.play(theta.animate.set_value(5*np.pi/6),run_time=4.5);self.until(5);self.note('모든 단위 방향의 투영 분산 = 1\\n특별한 첫 번째 주성분을 정할 수 없다')
  elif i==15:
   centers=self.centers();plots=[]
   for j,c in enumerate(centers):
    self.card(c,'수평 점 2개 수정' if j==0 else '수직 점 2개 수정',TEAL if j==0 else PURPLE);plot=Cloud(lambda t,j=j:isotropic_choice(j,t),origin=c,unit=.49,radius=.028,pc_length=2.3,highlight=[76,77] if j==0 else [78,79]);plot.first.set_color(TEAL if j==0 else PURPLE);self.add(plot);plots.append(plot)
    label=txt('C = I 에서 출발',20,MUTED).move_to(c+[0,-1.42,0]);self.add(label)
   self.play(*[plot.clock.animate.set_value(1) for plot in plots],run_time=3);self.note('각각 λ = 1.01, 1   ·   선택되는 PC1은 90° 차이')
  elif i==16:
   plot=self.main(lambda t:PLUS,pc1=False);other=VGroup(*[Dot(plot.point(q),radius=.026,color=PURPLE,fill_opacity=.55) for q in MINUS]);axes=VGroup(axis_line(plot.point,PLUS,TEAL),axis_line(plot.point,MINUS,PURPLE));self.add(other,axes)
   self.add(txt('수평 점 수정 후 PC1',22,TEAL).move_to([0,4.45,0] if VERT else [3.5,1.6,0]),txt('수직 점 수정 후 PC1',22,PURPLE).move_to([0,3.7,0] if VERT else [3.5,.85,0]));self.note('큰 주성분 변화 ≠ 큰 데이터 구조 변화');self.until(5);self.play(FadeOut(axes),run_time=.6);self.note('PC1 직선을 숨기면 두 점 구름은 거의 같다')
  elif i==17:
   centers=[np.array([0,2.35,0]),np.array([0,-.85,0])] if VERT else [np.array([-3.45,.15,0]),np.array([3.45,.15,0])]
   for c,x,formula,title,col in zip(centers,[LARGE,SMALL],['λ₁ = 2','λ₁ − λ₂ = 0.01'],['첫 주성분 방향의 분산','두 주성분의 분산 차이'],[TEAL,YELLOW]):
    self.add(RoundedRectangle(width=6.6 if VERT else 6.2,height=2.75 if VERT else 4.1,corner_radius=.15,color=GRID,stroke_width=1).move_to(c));mini=Cloud(lambda t,x=x:x,origin=c+[-1.55,0,0],unit=.27,radius=.02,pc1=True);self.add(mini)
    self.add(txt(formula,30,col,width=3.4).move_to(c+[1.25,.45,0]),txt(title,21,MUTED,width=3.5).move_to(c+[1.25,-.5,0]))
   self.note('방향의 안정성은 간격과 교란의 크기를 함께 고려')
  else:
   plot=self.main(lambda t:perturb(SMALL,t),ghost=True);plot.clock.set_value(1);plot.refresh();self.info_panel(plot,cov=False);self.add(txt('크기와 간격을 함께',31,YELLOW,width=7 if VERT else 6).move_to([0,4.4,0] if VERT else [3.5,1.8,0]),txt('Eigengap = λ₁ − λ₂',29,INK,width=7 if VERT else 6).move_to([0,3.5,0] if VERT else [3.5,.8,0]));self.note('같은 수준의 작은 변화에 대한 방향의 민감성')
  self.until(duration)
 def until(self,t):
  if self.time<t:self.wait(t-self.time)
  elif self.time>t+.04:raise RuntimeError(f'scene {self.i+1} timing overrun {self.time}>{t}')
 def note(self,s):
  if self.footer:self.remove(self.footer)
  self.footer=txt(s,19 if VERT else 22,MUTED,width=7 if VERT else 12.6).move_to([0,-4.35 if VERT else -2.8,0]);self.add(self.footer)
 def main(self,fn,**kwargs):
  plot=Cloud(fn,origin=(0,.15,0) if VERT else (-2.85,0,0),unit=.78 if VERT else .65,**kwargs);self.add(plot);return plot
 def dynamic_label(self,getter,pos,size=23,color=INK,width=None):
  holder=VGroup(txt(' ',size,color));prev=[None]
  def update(_):
   s=getter()
   if s!=prev[0]:
    key=(s,size,color,width)
    if key not in self.cache:self.cache[key]=txt(s,size,color,width)
    holder.become(self.cache[key].copy().move_to(pos));prev[0]=s
  holder.add_updater(update);update(holder);self.add(holder);return holder
 def info_panel(self,plot,cov=True,bars=True):
  if cov:
   c=np.array([0,4.05,0]) if VERT else np.array([3.5,1.35,0]);self.add(txt('공분산행렬 C',20,PURPLE).move_to(c+[0,.95,0]))
   entries=VGroup(*[txt('0',27,PURPLE).move_to(c+[x,y,0]) for y in [.27,-.27] for x in [-.65,.65]])
   brackets=VGroup()
   for x in [-1.35,1.35]:
    brackets.add(Line(c+[x,-.55,0],c+[x,.55,0],color=PURPLE))
    for y in [-.55,.55]:brackets.add(Line(c+[x,y,0],c+[x-np.sign(x)*.12,y,0],color=PURPLE))
   self.add(entries,brackets)
   for n in range(4):
    holder=entries[n];position=holder.get_center();previous=[None]
    def update_entry(info,n=n,holder=holder,pos=position,previous=previous):
     s=num(info['cov'].flat[n]);key=(s,27,PURPLE,None)
     if s!=previous[0]:
      if key not in self.cache:self.cache[key]=txt(s,27,PURPLE)
      holder.become(self.cache[key].copy().move_to(pos));previous[0]=s
    plot.connect(update_entry)
  if bars:
   left=-2.1 if VERT else 2.0;ys=[-2.65,-3.15] if VERT else [-.45,-1.0];scale=.9 if VERT else .72
   for j,y in enumerate(ys):
    col=TEAL if j==0 else ORANGE;bar=Rectangle(width=.01,height=.16,fill_color=col,fill_opacity=1,stroke_width=0);self.add(txt('λ₁' if j==0 else 'λ₂',22,col).move_to([left-.5,y,0]),bar)
    def update_bar(info,j=j,y=y,bar=bar):
     w=max(.005,float(info['values'][j])*scale);bar.stretch_to_fit_width(w).move_to([left+w/2,y,0])
    plot.connect(update_bar);self.dynamic_label(lambda j=j:num(plot.info['values'][j]),[2.6 if VERT else 5.7,y,0],22,col)
   pos=[0,-3.65,0] if VERT else [3.55,-1.85,0];self.add(RoundedRectangle(width=5.5,height=.52,corner_radius=.1,color=YELLOW,stroke_width=1).move_to(pos));self.dynamic_label(lambda:'gap = '+num(plot.info['gap']),pos,23,YELLOW)
 def angle_arc(self,plot,before,after):
  a=pca(before)['angle'];b=pca(after)['angle'];delta=(b-a+np.pi/2)%np.pi-np.pi/2;self.add(Arc(radius=.65,start_angle=a,angle=delta,color=YELLOW,stroke_width=2).move_arc_center_to(plot.point(pca(before)['mean'])));self.dynamic_label(lambda:f'PC1 회전 {np.rad2deg(abs(delta)):.2f}°',[0,3.05,0] if VERT else [3.5,.3,0],23,YELLOW,width=6)
 def centers(self):return [np.array([0,2.1,0]),np.array([0,-1.65,0])] if VERT else [np.array([-3.45,.05,0]),np.array([3.45,.05,0])]
 def card(self,c,title,color):self.add(RoundedRectangle(width=6.7 if VERT else 6.1,height=3.5,corner_radius=.15,color=GRID,stroke_width=1).move_to(c),txt(title,23,color,width=6 if VERT else 5.6).move_to(c+[0,1.45,0]))
 def comparison(self):
  result=[]
  for c,x,title in zip(self.centers(),[LARGE,SMALL],['길쭉한 분포','원형에 가까운 분포']):
   self.card(c,title,INK);plot=Cloud(lambda t,x=x:perturb(x,t),origin=c,unit=.48,ghost=True,highlight=INDICES,radius=.026);self.add(plot);result.append(plot);self.dynamic_label(lambda plot=plot,x=x:f'PC1 회전 {rotation(x,plot.clock.get_value()):.2f}°',c+[0,-1.42,0],21,YELLOW)
  return result
 def comparison_bars(self):
  for c,x,title in zip(self.centers(),[LARGE,SMALL],['길쭉한 분포','원형에 가까운 분포']):
   self.card(c,title,INK);plot=Cloud(lambda t,x=x:perturb(x,t),origin=c+[-1.35,0,0],unit=.32,ghost=True,radius=.022);plot.clock.set_value(1);plot.refresh();self.add(plot);vals=pca(x)['values'];base=c+[.65,-.65,0];height_scale=.62
   for j,(v,col) in enumerate(zip(vals,[TEAL,ORANGE])):
    xloc=base[0]+j*.85;h=v*height_scale;self.add(Rectangle(width=.46,height=h,fill_color=col,fill_opacity=.85,stroke_width=0).move_to([xloc,base[1]+h/2,0]),txt('λ₁' if j==0 else 'λ₂',17,col).move_to([xloc,base[1]-.25,0]),txt(num(v),17,col).move_to([xloc,base[1]+h+.2,0]))
   xloc=base[0]+1.55;y1=base[1]+vals[1]*height_scale;y2=base[1]+vals[0]*height_scale;self.add(Line([xloc,y1,0],[xloc,y2,0],color=YELLOW,stroke_width=3),Line([xloc-.12,y1,0],[xloc+.12,y1,0],color=YELLOW),Line([xloc-.12,y2,0],[xloc+.12,y2,0],color=YELLOW),txt('변경 전 간격 '+num(pca(x)['gap']),20,YELLOW).move_to(c+[.5,1.05,0]),txt(f'회전 {rotation(x):.2f}°',21,YELLOW).move_to(c+[-1.3,-1.38,0]))
 def projection(self,plot,initial):
  theta=ValueTracker(initial);self.add(theta);candidate=Line(plot.point([-1,0]),plot.point([1,0]),color=INK,stroke_width=2);self.add(candidate)
  center=np.array([0,-2.5,0]) if VERT else np.array([3.4,-.55,0]);scale=.62;self.add(Line(center+[-2.2,0,0],center+[2.2,0,0],color=MUTED,stroke_width=1));dots=VGroup(*[Dot(radius=.023,color=YELLOW) for _ in range(N)]);self.add(dots)
  var=[0.]
  def update(_):
   angle=theta.get_value();d=np.array([np.cos(angle),np.sin(angle)]);mu=plot.info['mean'];candidate.put_start_and_end_on(plot.point(mu-3.25*d),plot.point(mu+3.25*d));scores=(plot.points_data-mu)@d;var[0]=float(np.var(scores,ddof=1))
   for j,(dot,z) in enumerate(zip(dots,scores)):dot.move_to(center+[scale*z,((j%3)-1)*.055,0])
  theta.add_updater(update);update(theta)
  self.add(txt('해당 방향으로 투영한 점들',20,MUTED).move_to(center+[0,-.4,0]));self.dynamic_label(lambda:'투영 분산 = '+num(var[0]),[0,4.3,0] if VERT else [3.4,1.4,0],29,YELLOW,width=6)
  return theta
 def candidate(self,plot,initial):
  theta=ValueTracker(initial);self.add(theta);line=Line(plot.point([-3,0]),plot.point([3,0]),color=INK,stroke_width=2);self.add(line)
  def update(_):
   d=np.array([np.cos(theta.get_value()),np.sin(theta.get_value())]);line.put_start_and_end_on(plot.point(-3*d),plot.point(3*d))
  theta.add_updater(update);update(theta);self.add(txt('모든 방향의 투영 분산 = 1',23,YELLOW).move_to([0,3.0,0] if VERT else [3.5,.3,0]));return theta
