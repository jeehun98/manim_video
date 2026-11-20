from visual_common import *
config.background_color='#10141e'
STARTS=[0,25,49,59,76,112,125];ENDS=[25,49,59,76,112,125,151]
A=B

def vec(t):return np.array([np.cos(t),np.sin(t)])
def norm(t):return np.linalg.norm(A@vec(t))
class VolumeScene(ThreeDScene):
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
 def replace_eq(self,m,s,p=None,size=43,color=WHITE,duration=.8):
  n=MathTex(s,font_size=size,color=color)
  if n.width>12:n.scale_to_fit_width(12)
  n.move_to(m.get_center() if p is None else p);self.play(TransformMatchingTex(m,n),run_time=duration);return n
 def hud(self,s,p,size=28,color=WHITE):
  m=label(s,p,size,color);self.add_fixed_in_frame_mobjects(m);return m
 def wire(self,d=np.ones(3),color=BLUEC,center=ORIGIN,scale=1.3):
  d=np.array(d);c=np.array(center);g=VGroup()
  for phi in np.linspace(.22,PI-.22,9):
   g.add(ParametricFunction(lambda t:c+scale*d*np.array([np.sin(phi)*np.cos(t),np.sin(phi)*np.sin(t),np.cos(phi)]),t_range=[0,TAU,.12],color=color,stroke_width=1,stroke_opacity=.55))
  for theta in np.linspace(0,TAU,12,endpoint=False):
   g.add(ParametricFunction(lambda t:c+scale*d*np.array([np.sin(t)*np.cos(theta),np.sin(t)*np.sin(theta),np.cos(t)]),t_range=[0,PI,.10],color=color,stroke_width=1,stroke_opacity=.55))
  return g
 def disk(self,c,d=[1,1],scale=1,color=BLUEC,fill=.15):
  d=np.array(d);c=np.array(c)
  return ParametricFunction(lambda t:c+np.r_[d*vec(t),0]*scale,t_range=[0,TAU,.03],color=color,stroke_width=3,fill_color=color,fill_opacity=fill)
 def diskgrid(self,c,d=[1,1],scale=1,color=BLUEC):
  c=np.array(c);d=np.array(d);g=VGroup()
  for r in [.25,.5,.75]:g.add(self.disk(c,d*r,scale,color,0).set_stroke(width=1,opacity=.25))
  for t in np.arange(0,TAU,PI/8):g.add(Line(c,c+np.r_[d*vec(t),0]*scale,color=color,stroke_width=1,stroke_opacity=.25))
  return g
 def square(self,c,w=1,h=1,scale=.8,color=BLUEC,tiles=False):
  c=np.array(c);pts=[c,c+RIGHT*w*scale,c+(RIGHT*w+UP*h)*scale,c+UP*h*scale];g=VGroup(Polygon(*pts,color=color,fill_color=color,fill_opacity=.18,stroke_width=3))
  if tiles:
   for x in range(1,int(round(w))):g.add(Line(c+RIGHT*x*scale,c+RIGHT*x*scale+UP*h*scale,color=color,stroke_width=1))
   for y in range(1,int(round(h))):g.add(Line(c+UP*y*scale,c+UP*y*scale+RIGHT*w*scale,color=color,stroke_width=1))
  return g
 def pair_disk(self):
  l=np.array([-3.45,.3,0]);r=np.array([3.45,.3,0]);self.add(grid(l),grid(r),Arrow([-.65,.3,0],[.65,.3,0]),label('A',[0,.85,0],26));return l,r
 def solid(self,c,d=[1,1,1],scale=1,color=BLUEC):
  c=np.array(c);d=np.array(d)
  return Surface(lambda u,v:c+scale*d*np.array([np.sin(u)*np.cos(v),np.sin(u)*np.sin(v),np.cos(u)]),u_range=[0,PI],v_range=[0,TAU],resolution=(10,20),checkerboard_colors=[color,color],fill_opacity=.1,stroke_opacity=0)
 def sample_shape(self,c,factor):
  c=np.array(c);M=np.diag([factor,1.]);corners=np.array([[-.8,-.7],[.8,-.7],[.8,.7],[-.8,.7]]);g=VGroup(Polygon(*[c+np.r_[M@p,0] for p in corners],color=ORANGE,fill_color=ORANGE,fill_opacity=.12))
  points=[np.array([.5,.35]),np.array([-.45,.2]),np.array([-.35,-.4])];colors=[BLUEC,'#2dd4bf',YELLOW]
  for p,name,color in zip(points,['P','Q','R'],colors):
   pos=c+np.r_[M@p,0];g.add(Dot(pos,color=color,radius=.065),label(name,pos+UP*.22,21,color))
  for a,b in zip(points,points[1:]+points[:1]):g.add(Arrow(c+np.r_[M@a,0],c+np.r_[M@b,0],buff=.09,color=MUTED,stroke_width=1.5,max_tip_length_to_length_ratio=.18))
  return g
 def construct(self):
  self.caption_setup();i=self.index;YEL='#facc15';CYAN='#2dd4bf';RED='#fb7185';LIGHT='#e9d5ff'
  if i==0:
   self.reset('직교하는 주축 방향의 길이 변화');l,r=self.pair_disk();self.add(self.disk(l,scale=.95),self.disk(r,[2,.8],.95,ORANGE),arrow(r,np.array([2,0]),PURPLE,.95),arrow(r,np.array([0,.8]),LIGHT,.95));self.eq(r'\sigma_1\times\sigma_2=?',[0,-2.2,0],43,PURPLE);self.to(4);self.play(Indicate(self.mobjects[-1],scale_factor=1.08),run_time=1);self.to(9)
   self.reset('단위 정사각형의 넓이는 1');c=np.array([-2,-.7,0]);self.add(grid(c),self.square(c,scale=1.1));self.eq(r'1\times1=1',[2.3,.6,0],55,BLUEC);self.eq(r'S_{\rm before}=1',[2.3,-.9,0],39);self.to(13)
   self.reset('가로 두 배, 세로 세 배');l=np.array([-3.9,-1.15,0]);r=np.array([2.7,-1.15,0]);self.add(self.square(l),label('원래 정사각형',[-3.45,2.25,0],27,BLUEC),label('변환된 영역',[3.45,2.25,0],27,ORANGE),Arrow([-.6,.1,0],[.6,.1,0]));x=ValueTracker(1);y=ValueTracker(1);moving=always_redraw(lambda:self.square(r,x.get_value(),y.get_value(),color=ORANGE));self.add(moving);self.play(x.animate.set_value(2),run_time=2);self.play(y.animate.set_value(3),run_time=3);self.remove(moving);self.add(self.square(r,2,3,color=ORANGE,tiles=True));self.eq(r'2\times3=6',[0,-2.25,0],45,YEL);self.to(20)
   self.reset('직교하는 주축의 배율을 곱하면 넓이 배율');self.add(self.square([-3,-.8,0],2,3,color=ORANGE,tiles=True));self.eq(r'2\times3=6',[2.6,.9,0],59,YEL);self.eq(r'\sigma_1=3,\quad\sigma_2=2',[2.6,-.55,0],36,PURPLE);self.eq(r'\text{Area scaling}=\sigma_1\sigma_2',[0,-2.1,0],42);self.to(25)
  elif i==1:
   self.reset('단위 원으로 둘러싸인 영역');c=np.array([-2.7,.2,0]);self.add(grid(c),self.disk(c,scale=1.35),arrow(c,np.array([1,0]),BLUEC,1.35));self.to(28);self.eq(r'S_{\rm before}=\pi\cdot1^2=\pi',[2.5,.5,0],43,BLUEC,width=6);self.to(31)
   self.reset('새 예시: A = diag(2, 0.75)');l,r=self.pair_disk();self.add(self.disk(l,scale=.95),self.diskgrid(l,scale=.95));self.add(label('단위 원판',[-3.45,2.35,0],27,BLUEC),label('변환된 타원 영역',[3.45,2.35,0],27,ORANGE));p=ValueTracker(0)
   def dims():return [1+p.get_value(),1-.25*p.get_value()]
   moving=always_redraw(lambda:VGroup(self.disk(r,dims(),.95,ORANGE),self.diskgrid(r,dims(),.95,ORANGE)));self.add(moving);self.to(33);self.play(p.animate.set_value(1),run_time=3);self.add(arrow(r,np.array([2,0]),PURPLE,.95),arrow(r,np.array([0,.75]),LIGHT,.95));self.eq(r'\sigma_1=2,\quad\sigma_2=0.75',[0,-2.15,0],39,PURPLE);self.to(38)
   self.reset('타원의 넓이는 반축 두 길이의 곱 × π');c=np.array([-3,.3,0]);self.add(self.disk(c,[2,.75],1,ORANGE),arrow(c,np.array([2,0]),PURPLE,1),arrow(c,np.array([0,.75]),LIGHT,1));self.eq(r'S=\pi ab',[2.8,1.1,0],53);self.eq(r'S_{\rm after}=\pi\sigma_1\sigma_2',[2.8,-.6,0],43,YEL,width=6);self.add(label('a, b는 전체 축이 아닌 반축의 길이',[0,-2.1,0],26,MUTED));self.to(43)
   self.reset('변환 후 넓이를 원래 넓이로 나누면');l,r=self.pair_disk();self.add(self.disk(l,scale=.95),self.disk(r,[2,.75],.95,ORANGE));self.eq(r'\pi',[-3.45,.3,0],44,BLUEC);self.eq(r'\pi\sigma_1\sigma_2',[3.45,.3,0],39,ORANGE);f=self.eq(r'\frac{S_{\rm after}}{S_{\rm before}}=\frac{\pi\sigma_1\sigma_2}{\pi}',[0,-1.75,0],45);self.to(47);f=self.replace_eq(f,r'\frac{S_{\rm after}}{S_{\rm before}}=\sigma_1\sigma_2',size=48,color=YEL);self.to(49)
  elif i==2:
   self.reset('넓이에서 부피로');self.add_fixed_in_frame_mobjects(self.bar,self.cap);self.set_camera_orientation(phi=65*DEGREES,theta=-55*DEGREES);ring=Ellipse(width=4,height=1.5,color=ORANGE);self.add(ring);self.play(Create(self.wire(d=[2,1,.75],scale=1.1,color=ORANGE)),FadeOut(ring),run_time=2);self.to(52)
   self.reset('단위구와 타원체의 부피');basis=np.array([np.cos(35*DEGREES),np.sin(35*DEGREES),0]);l=-3.3*basis;r=3.3*basis;scale=.95;self.add(self.wire(center=l,scale=scale),self.solid(l,scale=scale));out=VGroup(self.wire(center=r,scale=scale),self.solid(r,scale=scale));self.add(out);self.hud('단위구',[-3.3,2.35,0],28,BLUEC);self.hud('B = diag(2, 1, 0.75)',[3.3,2.35,0],28,ORANGE);self.to(54)
   target=VGroup(self.wire(d=[2,1,.75],center=r,scale=scale,color=ORANGE),self.solid(r,[2,1,.75],scale,ORANGE));self.play(Transform(out,target),run_time=3)
   self.hud('V = 4π/3',[-3.3,-1.55,0],28,BLUEC);self.hud('V = (4π/3) σ₁σ₂σ₃',[3.3,-1.55,0],28,ORANGE);self.hud('부피 변화 배율 = σ₁σ₂σ₃ = 1.5',[0,-2.3,0],30,YEL);self.to(59)
  elif i==3:
   self.reset('공간 전체의 크기 변화를 나타내는 숫자');l=np.array([-3.7,.1,0]);corners=[np.array(p) for p in [[-.8,-.8],[.8,-.8],[.8,.8],[-.8,.8]]];M=np.array([[1,.7],[0,1]])
   self.add(Polygon(*[l+np.r_[p,0] for p in corners],color=BLUEC),Polygon(*[l+np.r_[M@p,0] for p in corners],color=ORANGE,fill_color=ORANGE,fill_opacity=.12),label('넓이의 변화',[-3.7,-1.5,0],27))
   # True cube vertices projected only for this explanatory inset.
   c=np.array([3.3,.1,0]);proj=np.array([[1,.45,0],[0,.3,1.]])
   for shear,color in [(0,BLUEC),(.5,ORANGE)]:
    P=np.array([[1,shear,0],[0,1,0],[0,0,1]])
    for a in range(8):
     v=np.array([(a>>k)&1 for k in range(3)])-.5
     for k in range(3):
      if not ((a>>k)&1):w=v.copy();w[k]+=1;self.add(Line(c+np.r_[proj@(P@v),0]*1.7,c+np.r_[proj@(P@w),0]*1.7,color=color,stroke_width=2))
   self.add(label('부피의 변화',[3.3,-1.5,0],27),label('?',[0,-2.15,0],58,YEL));self.to(65)
   self.reset('행렬식');self.eq(r'\det(A)',[0,.45,0],90,YEL);self.to(66)
   self.reset('행렬식의 절댓값 = 공간의 부피 배율');self.eq(r'V_{\rm after}=|\det(A)|V_{\rm before}',[0,.6,0],57,YEL);self.add(label('실수 정사각행렬 A에 대해',[0,-1.4,0],29,MUTED));self.to(71)
   self.reset('동일한 공간의 부피 변화 배율');self.eq(r'\prod_{i=1}^{n}\sigma_i',[-3.3,1,0],63,PURPLE);self.eq(r'|\det(A)|',[3.3,1,0],63,YEL);self.add(Arrow([-2,.3,0],[-.3,-.75,0]),Arrow([2,.3,0],[.3,-.75,0]));self.eq(r'\boxed{|\det(A)|=\prod_{i=1}^{n}\sigma_i}',[0,-1.6,0],55,YEL);self.to(76)
  elif i==4:
   self.reset('같은 행렬식을 두 가지 방법으로 계산');self.eq(r'|\det(A)|=\prod_i\sigma_i',[0,1.1,0],60,YEL);self.add(label('실수 n×n 행렬',[0,-.7,0],29,MUTED));self.to(79)
   self.reset('특잇값의 제곱은 AᵀA의 고윳값');self.eq(r'M=A^TA',[0,1.9,0],52,CYAN);f=self.eq(r'\sigma_i=\sqrt{\lambda_i(M)}',[0,.2,0],58,PURPLE);self.to(83);f=self.replace_eq(f,r'\sigma_i^2=\lambda_i(A^TA)',size=58,color=GREEN);self.to(85)
   self.reset('행렬식은 고윳값의 곱');f=self.eq(r'\det(M)=\lambda_1\lambda_2\cdots\lambda_n',[0,.6,0],57,GREEN);self.to(88)
   self.reset('방법 1: 고윳값으로 계산');f=self.eq(r'\det(A^TA)=\lambda_1\lambda_2\cdots\lambda_n',[0,1,0],52,GREEN);self.to(90);f=self.replace_eq(f,r'\det(A^TA)=\sigma_1^2\sigma_2^2\cdots\sigma_n^2',size=52,color=PURPLE);self.to(92);f=self.replace_eq(f,r'\det(A^TA)=\left(\prod_i\sigma_i\right)^2',size=56,color=PURPLE);self.to(94)
   self.reset('방법 2: 행렬식의 성질로 계산');left=self.eq(r'\det(A^TA)=\left(\prod_i\sigma_i\right)^2',[-3.45,1.7,0],35,PURPLE,width=6.4);self.add(label('방법 1',[-3.45,2.4,0],24,PURPLE),label('방법 2',[3.45,2.4,0],24,CYAN));f=self.eq(r'\det(A^TA)=\det(A^T)\det(A)',[3.45,1,0],35,CYAN,width=6.4);self.eq(r'\det(PQ)=\det(P)\det(Q)',[0,-.5,0],38,MUTED);self.to(97);self.eq(r'\det(A^T)=\det(A)',[0,-1.7,0],41,CYAN);self.to(99);f=self.replace_eq(f,r'\det(A^TA)=\det(A)\det(A)',p=[3.45,1,0],size=34,color=CYAN);self.to(101)
   self.reset('동일한 행렬식에서 만나는 두 결과');self.eq(r'\det(A^TA)=\left(\prod_i\sigma_i\right)^2',[-3.4,1.35,0],36,PURPLE,width=6.2);self.eq(r'\det(A^TA)=\det(A)^2',[3.4,1.35,0],38,CYAN,width=6.2);self.to(104);self.eq(r'\det(A)^2=\left(\prod_i\sigma_i\right)^2',[0,-1,0],56,YEL);self.to(106)
   self.reset('양변에 제곱근을 취하면');f=self.eq(r'\sqrt{\det(A)^2}=\sqrt{\left(\prod_i\sigma_i\right)^2}',[0,.65,0],53);self.to(108);f=self.replace_eq(f,r'|\det(A)|=\prod_i\sigma_i',size=66,color=YEL);self.eq(r'\sigma_i\geq0',[0,-1.2,0],37,PURPLE);self.to(110);self.play(Indicate(f,color=YEL,scale_factor=1.06),run_time=1);self.to(112)
  elif i==5:
   self.reset('왜 절댓값이 필요할까?');self.eq(r'\det(A)\in\mathbb R',[-3.4,1.05,0],51,YEL);self.eq(r'\prod_i\sigma_i\geq0',[3.4,1.05,0],51,PURPLE);self.eq(r'|\det(A)|=\prod_i\sigma_i',[0,-1.15,0],55);self.to(116)
   self.reset('길이는 같아도 공간의 방향성은 다르다');l=np.array([-3.45,.45,0]);r=np.array([3.45,.45,0]);left=self.sample_shape(l,1);right=self.sample_shape(r,1);self.add(left,right);self.add(label('A = diag(2, 1)',[-3.45,2.35,0],27),label('B = diag(−2, 1)',[3.45,2.35,0],27));self.to(118)
   self.play(Transform(left,self.sample_shape(l,2)),Transform(right,self.sample_shape(r,-2)),run_time=3);self.eq(r'\sigma_1=2,\ \sigma_2=1',[-3.45,-1.2,0],32,PURPLE);self.eq(r'\sigma_1=2,\ \sigma_2=1',[3.45,-1.2,0],32,PURPLE);self.eq(r'\det(A)=+2',[-3.45,-2.05,0],39,YEL);self.eq(r'\det(B)=-2',[3.45,-2.05,0],39,RED);self.to(125)
  else:
   self.reset('전체 넓이는 같지만 방향별 변화는 다르다');scale=.38
   for x,d in [(-4.5,[1,1]),(0,[2,.5]),(4.5,[4,.25])]:
    self.add(Circle(radius=scale,color=BLUEC,stroke_opacity=.25).move_to([x,.75,0]),self.disk([x,.75,0],d,scale,ORANGE));self.eq(r'\sigma=('+str(d[0])+','+str(d[1])+')',[x,-.55,0],32,PURPLE,width=4);self.eq(r'|\det|=1',[x,-1.5,0],40,YEL,width=4)
   self.add(label('세 도형 모두 동일한 좌표 척도',[0,-2.3,0],27,MUTED));self.to(133)
   self.reset('넓이를 유지하면서 극단적으로 변하는 형태');p=ValueTracker(0);c=np.array([0,.3,0]);scale=.1
   def stretch():return 100**p.get_value()
   def rect():
    s=stretch();return Polygon(c+np.array([-s/2,-.5/s,0])*scale,c+np.array([s/2,-.5/s,0])*scale,c+np.array([s/2,.5/s,0])*scale,c+np.array([-s/2,.5/s,0])*scale,stroke_width=0,fill_color=ORANGE,fill_opacity=1)
   centerline=always_redraw(lambda:Line(c+LEFT*stretch()*scale/2,c+RIGHT*stretch()*scale/2,color=ORANGE,stroke_width=2));self.add(always_redraw(rect),centerline,DashedLine([-5,.3,0],[5,.3,0],color=MUTED,stroke_width=1,stroke_opacity=.35));self.add(label('주황색: 중심 위치 표시 · 점선 폭 = 100 (고정 척도)',[0,-.55,0],22,MUTED),Square(side_length=1.2,color=BLUEC,fill_color=BLUEC,fill_opacity=.15).move_to([-4.6,1.9,0]),label('입력 확대 ×12',[-4.6,2.8,0],21,MUTED))
   xnum=DecimalNumber(1,mob_class=Text,num_decimal_places=2,font_size=36,color=PURPLE).move_to([-2.4,-1.35,0]);ynum=DecimalNumber(1,mob_class=Text,num_decimal_places=4,font_size=36,color=LIGHT).move_to([2.4,-1.35,0]);xnum.add_updater(lambda m:m.set_value(stretch()));ynum.add_updater(lambda m:m.set_value(1/stretch()));self.add(xnum,ynum,label('×',[0,-1.35,0],35),label('= 1',[0,-2.15,0],39,YEL));self.play(p.animate.set_value(1),run_time=5,rate_func=linear)
   self.add(Line([3.7,1.35,0],[5.2,1.35,0],color=ORANGE),Line([3.7,2.35,0],[5.2,2.35,0],color=ORANGE),label('두께 ×1000 · 중앙 단면',[4.45,2.8,0],21,MUTED),label('실제 두께 0.01',[4.45,.95,0],21,MUTED));self.to(140)
   self.reset('같은 행렬식, 서로 다른 길이 변화')
   for x,name,sig in [(-3.45,'A = I',(1,1)),(3.45,'B = diag(100, 0.01)',(100,.01))]:
    self.add(label(name,[x,2.15,0],29));self.eq(r'\sigma_1='+str(sig[0])+r',\quad\sigma_2='+str(sig[1]),[x,.7,0],38,PURPLE,width=6);self.eq(r'|\det|=1',[x,-.9,0],52,YEL)
   self.to(145)
   self.reset('방향별 길이 배율의 차이는 계산에 어떤 영향을 줄까?');self.eq(r'\sigma_1/\sigma_2=?',[0,1.9,0],55,PURPLE);self.add(Line([-5,.2,0],[5,.2,0],color=ORANGE,stroke_width=3),label('출력의 중심선 · 실제 두께는 1픽셀보다 작음',[0,-.4,0],24,MUTED));self.to(147)
   self.add(Dot([1,.2,0],color=BLUEC),Dot([1,.85,0],color=RED),Arrow([1,.2,0],[1,.85,0],buff=0,color=RED),label('작은 출력 오차 · 가시성을 위한 개념도',[1.6,1.25,0],23,RED));self.to(149);self.add(Arrow([-.5,-1.1,0],[-2.7,-1.1,0],color=MUTED),label('원래 공간으로 복원하면?',[.9,-1.65,0],30));self.to(151)
