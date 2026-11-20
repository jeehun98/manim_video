from visual_common import *
config.background_color='#10141e'
STARTS=[0,17,36,61,95,121];ENDS=[17,36,61,95,121,137]
A=B

def vec(t):return np.array([np.cos(t),np.sin(t)])
def norm(t):return np.linalg.norm(A@vec(t))
class InformationScene(ThreeDScene):
 index=0
 def to(self,t):
  d=(round((t-STARTS[self.index])*config.frame_rate)-round(self.time*config.frame_rate))/config.frame_rate
  if d>.001:self.wait(d)
  elif d<-.04:raise ValueError((t,self.time))
 def caption_setup(self):
  self.caps={}
  for j,row in enumerate(DATA):
   group=VGroup(*[txt(s,25) for s in textwrap.wrap(row['text'],width=48,break_long_words=False)]).arrange(DOWN,buff=.12)
   if group.width>12.8:group.scale_to_fit_width(12.8)
   group.move_to([0,-3.25,0]);assert group.get_bottom()[1]>-3.98
   self.caps[j]=group
  self.cap=VGroup();self.cap_key=-1
  def update(m,dt):
   t=STARTS[self.index]+self.time
   key=next((j for j,r in enumerate(DATA) if r['start']<=t<r['end']),len(DATA)-1)
   if key!=self.cap_key:
    m.become(self.caps[key]);m.set_z_index(100);self.camera.add_fixed_in_frame_mobjects(m);self.cap_key=key
  self.cap.add_updater(update);self.bar=Rectangle(width=14.22,height=1.3,stroke_width=0,fill_color='#090d15',fill_opacity=1).move_to([0,-3.35,0]);self.bar.z_index=90;self.cap.z_index=100;self.add(self.bar,self.cap)
 def reset(self,title):
  for m in list(self.mobjects):
   if m not in [self.cap,self.bar]:self.remove(m)
  self.add_fixed_in_frame_mobjects(label(title,[0,3.2,0],32))
 def formula(self,s,y=-2,size=33,color=PURPLE):
  m=label(s,[0,y,0],size,color)
  if m.width>12:m.scale_to_fit_width(12)
  self.add(m);return m
 def pair(self,v=np.array([1.,1.]),scale=.8,y=.4):
  l=np.array([-3.45,y,0]);r=np.array([3.45,y,0]);self.add(grid(l,scale=scale),grid(r,scale=scale),label('입력 벡터 v',l+UP*1.9,25,BLUEC),label('출력 벡터 Av',r+UP*1.9,25,ORANGE),Arrow([-.6,y,0],[.6,y,0]),label('A',[0,y+.5,0],24))
  return l,r
 def bars(self,x,y,length,color):return Line([x,y,0],[x+length,y,0],stroke_width=12,color=color)
 def graph(self,center=[0,-.55,0],width=11.5,height=2.4):
  ax=Axes(x_range=[0,360,90],y_range=[0,3,1],x_length=width,y_length=height,tips=False,axis_config={'stroke_color':MUTED,'stroke_width':1.3}).move_to(center)
  self.add(ax)
  for n in [0,90,180,270,360]:self.add(label(f'{n}°',ax.c2p(n,0)+DOWN*.25,18,MUTED))
  for n in [1,2,3]:self.add(label(str(n),ax.c2p(0,n)+LEFT*.25,18,MUTED))
  self.add(DashedLine(ax.c2p(0,1),ax.c2p(360,1),color=BLUEC,stroke_width=2))
  return ax
 def curve(self,ax,end=360):return ax.plot(lambda x:norm(x*DEGREES),x_range=[0,max(.01,end),1],color=ORANGE,stroke_width=3,use_smoothing=False)
 def eq(self,s,p=[0,.3,0],size=43,color=WHITE,width=12):
  m=MathTex(s,font_size=size,color=color)
  if m.width>width:m.scale_to_fit_width(width)
  m.move_to(p);self.add(m);return m
 def hud(self,s,p,size=28,color=WHITE):
  m=label(s,p,size,color);self.add_fixed_in_frame_mobjects(m);return m
 def wire(self,d=np.ones(3),color=BLUEC,center=ORIGIN,scale=1.3):
  d=np.array(d);c=np.array(center);g=VGroup()
  for phi in np.linspace(.22,PI-.22,9):
   g.add(ParametricFunction(lambda t:c+scale*d*np.array([np.sin(phi)*np.cos(t),np.sin(phi)*np.sin(t),np.cos(phi)]),t_range=[0,TAU,.12],color=color,stroke_width=1,stroke_opacity=.55))
  for theta in np.linspace(0,TAU,12,endpoint=False):
   g.add(ParametricFunction(lambda t:c+scale*d*np.array([np.sin(t)*np.cos(theta),np.sin(t)*np.sin(theta),np.cos(t)]),t_range=[0,PI,.10],color=color,stroke_width=1,stroke_opacity=.55))
  return g
 def safe_arrow(self,c,v,color,scale=1):
  if np.linalg.norm(v)==0:return Dot(c,radius=.065,color=color)
  return arrow(c,v,color,scale)
 def outline(self,c,t,scale=.95,color=ORANGE):
  if t==0:return Line(np.array(c)+LEFT*2*scale,np.array(c)+RIGHT*2*scale,color=color,stroke_width=4)
  return ParametricFunction(lambda a:np.array(c)+np.array([2*np.cos(a),t*np.sin(a),0])*scale,t_range=[0,TAU,.035],color=color,stroke_width=3)
 def plane(self,c,t=1,scale=.95):
  g=VGroup()
  for x in np.arange(-2,2.01,.5):g.add(Line(np.array(c)+np.array([x,-2*t,0])*scale,np.array(c)+np.array([x,2*t,0])*scale,color=MUTED,stroke_opacity=.13,stroke_width=1)) if t>0 else None
  for y in np.arange(-2,2.01,.5):g.add(Line(np.array(c)+np.array([-2,y*t,0])*scale,np.array(c)+np.array([2,y*t,0])*scale,color=MUTED,stroke_opacity=.13,stroke_width=1))
  return g
 def pair_at(self,t,heading=True):
  l=np.array([-3.45,.3,0]);r=np.array([3.45,.3,0]);self.add(self.plane(l),Circle(radius=.95,color=BLUEC).move_to(l),Arrow([-.6,.3,0],[.6,.3,0]),label('Aₜ',[0,.85,0],27))
  if heading:self.add(label('입력 단위 원',[-3.45,2.35,0],26,BLUEC),label('변환된 공간',[3.45,2.35,0],26,ORANGE))
  display=always_redraw(lambda:VGroup(self.plane(r,t.get_value()),self.outline(r,t.get_value()),self.safe_arrow(r,np.array([2,0]),PURPLE,.95),self.safe_arrow(r,np.array([0,t.get_value()]),'#e9d5ff',.95)));self.add(display)
  self.add(label('σ₁ = 2',[-3.45,-1.85,0],29,PURPLE),label('σ₂ =',[2.5,-1.85,0],29,'#e9d5ff'))
  num=always_redraw(lambda:label(('> 0' if 0<t.get_value()<.001 else f'{t.get_value():.3f}'),[3.9,-1.85,0],30,'#e9d5ff'));self.add(num);return l,r,display
 def rank_label(self,t,p=[0,-2.35,0]):
  return always_redraw(lambda:label('Rank = '+('2' if t.get_value()>0 else '1'),p,31,GREEN if t.get_value()>0 else '#fb7185'))
 def spectrum(self,vals,c=[0,.1,0],width=10,height=2.4):
  g=VGroup();n=len(vals);mx=max(max(vals),1);step=width/n
  for i,v in enumerate(vals):
   x=c[0]-width/2+step*(i+.5);y=c[1]-height/2
   if v>0:g.add(Rectangle(width=step*.65,height=height*v/mx,color=PURPLE,fill_color=PURPLE,fill_opacity=.85).move_to([x,y+height*v/mx/2,0]))
   else:g.add(Line([x-step*.25,y,0],[x+step*.25,y,0],color='#fb7185'))
   g.add(label(f'σ{i+1}',[x,y-.3,0],21,MUTED))
  return g
 def construct(self):
  self.caption_setup();i=self.index;RED='#fb7185';LIGHT='#e9d5ff'
  if i==0:
   self.reset('특잇값과 공간의 변화');t=ValueTracker(1);l,r,display=self.pair_at(t);self.to(4)
   self.add(Arrow(r+UP*1.6,r+UP*.8,color=RED),Arrow(r+DOWN*1.6,r+DOWN*.8,color=RED));self.to(9)
   self.reset('새로운 예시: 두 특잇값을 따로 조절');self.eq(r'A_t=\begin{pmatrix}2&0\\0&t\end{pmatrix},\qquad0\leq t\leq1',[0,1.2,0],53);self.eq(r'\sigma_1=2\quad\text{(fixed)},\qquad\sigma_2=t',[0,-.7,0],43,PURPLE);self.to(12)
   self.reset('특잇값과 공간의 변화');t=ValueTracker(1);self.pair_at(t);self.play(t.animate.set_value(.6),run_time=5,rate_func=linear)
  elif i==1:
   self.reset('특잇값과 공간의 변화');t=ValueTracker(.6);l,r,display=self.pair_at(t);self.add(DashedVMobject(self.outline(r,1),num_dashes=40).set_stroke(opacity=.2));rank=self.rank_label(t);self.add(rank);self.play(t.animate.set_value(.1),run_time=4,rate_func=linear)
   self.play(t.animate.set_value(.01),run_time=3,rate_func=linear)
   inset=VGroup(label('세로 단면 ×60',[3.45,2.35,0],24,MUTED),Line([2.2,1.35,0],[4.7,1.35,0],color=PURPLE),Line([3.45,.75,0],[3.45,1.95,0],color=LIGHT));
   for m in list(self.mobjects):
    if isinstance(m,Text) and np.allclose(m.get_center(),[3.45,2.35,0]):self.remove(m)
   self.add(inset);self.to(27);self.remove(inset)
   self.play(t.animate.set_value(0),run_time=3,rate_func=linear);t.set_value(0);self.to(32)
   self.reset('입력 공간은 2차원, 이미지 공간은 1차원');l=np.array([-3.45,.25,0]);r=np.array([3.45,.25,0]);self.add(self.plane(l),self.safe_arrow(l,np.array([1,0]),GREEN,.9),self.safe_arrow(l,np.array([0,1]),RED,.9),Arrow([-.6,.25,0],[.6,.25,0]),label('A₀',[0,.8,0],26));moving=self.plane(r);basis=VGroup(self.safe_arrow(r,np.array([1,0]),GREEN,.9),self.safe_arrow(r,np.array([0,1]),RED,.9));self.add(moving,basis);self.play(Transform(moving,self.plane(r,0)),Transform(basis,VGroup(self.safe_arrow(r,np.array([2,0]),GREEN,.9),Dot(r,color=RED))),run_time=2);self.eq(r'(x,y)\mapsto(2x,0)',[0,-1.7,0],42);self.add(label('입력 차원 2',[-3.45,-2.3,0],27,BLUEC),label('이미지 차원 1',[3.45,-2.3,0],27,GREEN));self.to(36)
  elif i==2:
   self.reset('차원 붕괴는 입력의 차이를 지운다');l=np.array([-3.45,.2,0]);r=np.array([3.45,.2,0]);self.add(grid(l),grid(r),Arrow([-.6,.2,0],[.6,.2,0]),label('A₀',[0,.7,0],26));p=Dot(l+np.array([.8,1,0]),color=PURPLE);q=Dot(l+np.array([.8,-1,0]),color='#2dd4bf');self.add(p,q);self.play(TransformFromCopy(p,Dot(r+np.array([1.6,0,0]),color=PURPLE)),TransformFromCopy(q,Dot(r+np.array([1.6,0,0]),color='#2dd4bf')),run_time=2);self.to(40)
   self.reset('사라지는 입력 방향은 영벡터가 된다');l=np.array([-3.45,.25,0]);r=np.array([3.45,.25,0]);self.add(grid(l),grid(r),Line(l+UP*1.8,l+DOWN*1.8,color=RED,stroke_width=5),Arrow([-.6,.25,0],[.6,.25,0]),label('A₀',[0,.85,0],26));v=VGroup(*[self.safe_arrow(l,np.array([0,c]),RED,.7) for c in [-2,-1,1,2]]);out=v.copy().shift(r-l);self.add(v,out);self.play(Transform(out,VGroup(*[Dot(r,color=RED) for _ in range(4)])),run_time=3);self.eq(r'A_0\begin{pmatrix}0\\c\end{pmatrix}=\begin{pmatrix}0\\0\end{pmatrix}\quad(c\in\mathbb R)',[0,-2,0],40);self.to(45)
   self.reset('다른 입력, 같은 출력');l=np.array([-3.45,.3,0]);r=np.array([3.45,.3,0]);self.add(grid(l),grid(r),Arrow([-.6,.3,0],[.6,.3,0]),label('A₀',[0,.85,0],26));colors=[BLUEC,'#2dd4bf',PURPLE,YELLOW,RED]
   for y,color in zip([-2,-1,0,1,2],colors):self.add(self.safe_arrow(l,np.array([1,y]),color,.7))
   self.to(47);s=ValueTracker(1);out=always_redraw(lambda:VGroup(*[self.safe_arrow(r,np.array([2,s.get_value()*y]),color,.7) for y,color in zip([-2,-1,0,1,2],colors)]));self.add(out);self.play(s.animate.set_value(0),run_time=2);self.add(Dot(r+RIGHT*1.4,color=RED));self.eq(r'A_0(1,y)^T=(2,0)^T',[0,-2.1,0],41);self.to(51)
   self.reset('출력만으로 입력을 구별할 수 없다')
   for y in [-2,-1,0,1,2]:
    self.add(label(f'(1, {y})',[-4.6,y*.65,0],27,colors[y+2]),Line([-3.7,y*.65,0],[-.6,0,0],color=MUTED,stroke_width=1))
   self.add(label('(2, 0)',[.5,0,0],40,ORANGE),label('원래 입력은?',[4,.5,0],32),label('?',[4,-.4,0],65,RED));self.to(55)
   self.reset('영공간: 영벡터로 보내지는 모든 입력');c=np.array([-3,.1,0]);self.add(grid(c),Line(c+UP*1.9,c+DOWN*1.9,color=RED,stroke_width=5));self.eq(r'\ker(A)=\{v:Av=0\}',[2.5,1.1,0],40,RED,width=7);self.eq(r'\ker(A_0)=\{(0,c)^T:c\in\mathbb R\}',[2.2,-.4,0],34,width=7.5);self.add(label('영공간의 차원 = 1',[2.2,-1.7,0],30,RED));self.to(61)
  elif i==3:
   self.reset('랭크: 출력에 남아 있는 독립적인 방향');l=np.array([-3.45,.3,0]);r=np.array([3.45,.3,0]);self.add(grid(l),grid(r),self.safe_arrow(l,np.array([1,0]),GREEN,1),self.safe_arrow(l,np.array([0,1]),RED,1),self.safe_arrow(r,np.array([2,0]),GREEN,1),Dot(r,color=RED),Arrow([-.6,.3,0],[.6,.3,0]));self.add(label('소실된 입력 방향: 1개',[-3.45,-1.85,0],27,RED),label('Rank = 1',[3.45,-1.85,0],35,GREEN));self.to(66)
   self.reset('양의 특잇값이 두 개면 Rank = 2');t=ValueTracker(.62);c=np.array([-3,.35,0]);self.add(self.outline(c,t.get_value(),1.1),self.safe_arrow(c,np.array([2,0]),GREEN,1.1),self.safe_arrow(c,np.array([0,.62]),GREEN,1.1),self.spectrum([2,.62],c=[3,.5,0],width=4,height=2.3),label('Rank = 2',[0,-2,0],37,GREEN));self.to(71)
   self.reset('랭크는 정확히 0이 되는 순간에만 감소한다');t=ValueTracker(.5);c=np.array([-3,.3,0]);self.add(always_redraw(lambda:self.outline(c,t.get_value(),1.1)),always_redraw(lambda:self.spectrum([2,t.get_value()],c=[3,.5,0],width=4,height=2.2)),self.rank_label(t,p=[0,-2.15,0]));self.play(t.animate.set_value(.01),run_time=3,rate_func=linear);self.to(76);self.play(t.animate.set_value(0),run_time=1,rate_func=linear);t.set_value(0);self.to(78)
   self.reset('삼차원에서도 양의 특잇값 개수가 남은 차원이다');self.add_fixed_in_frame_mobjects(self.bar,self.cap);self.set_camera_orientation(phi=65*DEGREES,theta=-55*DEGREES);s=ValueTracker(1);t=ValueTracker(.65)
   def body():
    a,b=s.get_value(),t.get_value()
    if a==0:return Line(LEFT*2.8,RIGHT*2.8,color=ORANGE,stroke_width=5)
    if b==0:
     area=Ellipse(width=5.6,height=2.8*a,color=ORANGE,fill_color=ORANGE,fill_opacity=.2)
     return VGroup(area,*[Line(np.array([-2.8*np.sqrt(max(0,1-y*y)),1.4*a*y,0]),np.array([2.8*np.sqrt(max(0,1-y*y)),1.4*a*y,0]),color=ORANGE,stroke_width=1,stroke_opacity=.4) for y in np.linspace(-.9,.9,9)])
    return self.wire(d=[2,a,b],scale=1.4,color=ORANGE)
   obj=always_redraw(body);self.add(obj);self.hud('새 행렬 B = diag(2, s, t)',[0,2.45,0],28,ORANGE)
   hud=VGroup();self.add_fixed_in_frame_mobjects(hud)
   def status(m,dt):
    vals=[2,s.get_value(),t.get_value()];rank=sum(x>0 for x in vals)
    m.become(VGroup(label('Rank = '+str(rank),[0,-1.95,0],35,GREEN),label(f'σ = (2, {vals[1]:.2f}, {vals[2]:.2f})',[0,-2.5,0],25,PURPLE)));self.camera.add_fixed_in_frame_mobjects(m)
   hud.add_updater(status);self.to(82);self.to(84);self.play(t.animate.set_value(0),run_time=3,rate_func=linear);t.set_value(0);self.move_camera(theta=-40*DEGREES,run_time=1);self.play(s.animate.set_value(0),run_time=2,rate_func=linear);s.set_value(0);self.to(91)
   self.reset('랭크는 양의 특잇값 개수');self.set_camera_orientation(phi=0,theta=-90*DEGREES);self.add(self.spectrum([2,1.55,1.2,.65,0,0,0],c=[0,.9,0],width=11,height=2));self.eq(r'\operatorname{rank}(A)=\dim\operatorname{Im}(A)=\#\{i:\sigma_i>0\}',[0,-1.4,0],39);self.add(label('설명용 예시 · Rank = 4',[0,-2.3,0],29,GREEN));self.to(95)
  elif i==4:
   self.reset('매우 작은 양수도 정확한 0과 다르다');vals=[2,1.55,1.2,.65,.08,.04,.02];self.add(self.spectrum(vals,c=[0,.7,0],width=11,height=2.4),label('설명용 분포 · 모두 양수이므로 Rank = 7',[0,-1.3,0],29,GREEN),label('작은 세 값: 0.08, 0.04, 0.02',[0,-2.1,0],28,LIGHT));self.to(101)
   self.reset('작게 남은 성분은 사라진 성분이 아니다');l=np.array([-3.45,.25,0]);r=np.array([3.45,.25,0]);self.add(grid(l),grid(r),self.safe_arrow(l,np.array([1,1]),BLUEC,1),self.safe_arrow(l,np.array([1,0]),PURPLE,1),Line(l+RIGHT,l+RIGHT+UP,color=LIGHT,stroke_width=4),Arrow([-.6,.25,0],[.6,.25,0]));out=self.safe_arrow(r,np.array([1,1]),ORANGE,1);self.add(out);self.play(Transform(out,self.safe_arrow(r,np.array([2,.1]),ORANGE,1)),run_time=2);self.add(Line(r+RIGHT*2,r+RIGHT*2+UP*.1,color=RED,stroke_width=6),label('세로 성분 0.1 ≠ 0',[3.45,1.5,0],27,RED));self.eq(r'A=\operatorname{diag}(2,0.1),\quad A(1,1)^T=(2,0.1)^T',[0,-2.1,0],37);self.to(107)
   self.reset('작은 특잇값을 의도적으로 제거');self.eq(r'A=\begin{pmatrix}2&0\\0&0.1\end{pmatrix}',[-3.5,1.6,0],42,ORANGE);self.eq(r'A_1=\begin{pmatrix}2&0\\0&0\end{pmatrix}',[3.5,1.6,0],42,GREEN);self.add(self.outline([-3.5,-.1,0],.1,1),self.outline([3.5,-.1,0],0,1),label('Rank = 2',[-3.5,-1.1,0],28,ORANGE),label('Rank = 1',[3.5,-1.1,0],28,GREEN));self.to(110);self.eq(r'A(1,1)^T=(2,0.1)^T,\quad A_1(1,1)^T=(2,0)^T',[0,-2,0],35);self.to(113)
   self.reset('차원을 줄이되 변환 오차를 제한한다');self.eq(r'A-A_1=\begin{pmatrix}0&0\\0&0.1\end{pmatrix}',[0,1.2,0],48,RED);self.eq(r'\max_{\|v\|=1}\|(A-A_1)v\|=0.1',[0,-.5,0],49,PURPLE);self.add(label('단위입력에 대한 최대 절대 오차',[0,-1.9,0],28,MUTED));self.to(116)
   self.reset('저랭크 근사와 데이터 압축');left=np.array([-3.45,.55,0]);right=np.array([3.45,.55,0]);vals=[2,1.55,1.2,.65,.08,.04,.02];self.add(self.spectrum(vals,left,width=5.8,height=2.3),self.spectrum(vals[:4]+[0,0,0],right,width=5.8,height=2.3),label('Rank = 7',[-3.45,-1.45,0],29,ORANGE),label('Rank = 4',[3.45,-1.45,0],29,GREEN));self.eq(r'\|A-A_k\|_2=\sigma_{k+1}',[0,-2.25,0],35,PURPLE);self.to(121)
  else:
   self.reset('특잇값이 알려주는 정보');self.eq(r'\sigma_i: \text{scaling of each principal direction}',[0,.5,0],40,PURPLE);self.to(124);self.reset('특잇값이 알려주는 정보')
   for x,t,title,desc,color in [(-4.4,1,'유지 또는 팽창','출력에 반영되는 성분',GREEN),(0,.07,'강한 수축','작지만 남아 있는 성분',PURPLE),(4.4,0,'완전한 소실','구별할 수 없는 입력 차이',RED)]:
    self.add(RoundedRectangle(width=4,height=4.1,color='#344256',fill_color='#151e2b',fill_opacity=1).move_to([x,.3,0]),label(title,[x,1.75,0],27,color),Circle(radius=.8,color=BLUEC,stroke_opacity=.2).move_to([x,.4,0]),self.outline([x,.4,0],t,.78),label(desc,[x,-1,0],21,color))
   self.to(128);self.eq(r'\operatorname{rank}(A)=\#\{i:\sigma_i>0\},\qquad\ker(A)=\{v:Av=0\}',[0,-2.25,0],34);self.to(132)
   self.reset('길이 변화 배율을 모두 곱하면?');t=ValueTracker(.8);l,r,_=self.pair_at(t);self.to(134);self.eq(r'\sigma_1\times\sigma_2=?',[0,-2.4,0],45,PURPLE);self.to(136);self.add(Circle(radius=.95,color=BLUEC,fill_color=BLUEC,fill_opacity=.14).move_to(l),Ellipse(width=3.8,height=1.52,color=ORANGE,fill_color=ORANGE,fill_opacity=.14).move_to(r));self.to(137)
