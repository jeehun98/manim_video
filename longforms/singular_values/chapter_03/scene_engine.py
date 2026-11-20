from visual_common import *
config.background_color='#10141e'
STARTS=[0,29,57,78,112,158];ENDS=[29,57,78,112,158,180]
A=B

def vec(t):return np.array([np.cos(t),np.sin(t)])
def norm(t):return np.linalg.norm(A@vec(t))
class DerivationScene(Scene):
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
    m.become(self.caps[key]);m.set_z_index(100);self.cap_key=key
  self.cap.add_updater(update);self.bar=Rectangle(width=14.22,height=1.3,stroke_width=0,fill_color='#090d15',fill_opacity=1).move_to([0,-3.35,0]);self.bar.z_index=90;self.cap.z_index=100;self.add(self.bar,self.cap)
 def reset(self,title):
  for m in list(self.mobjects):
   if m not in [self.cap,self.bar]:self.remove(m)
  self.add(label(title,[0,3.2,0],32))
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
 def ellipse(self,c,scale=1):return ParametricFunction(lambda t:np.array(c)+np.r_[A@vec(t),0]*scale,t_range=[0,TAU,.025],color=ORANGE,stroke_width=3)
 def two(self,title=None):
  l=np.array([-3.45,.35,0]);r=np.array([3.45,.35,0]);self.add(grid(l),grid(r),Circle(radius=.95,color=BLUEC).move_to(l),self.ellipse(r,.95),Arrow([-.6,.35,0],[.6,.35,0]),label('A',[0,.9,0],26));return l,r
 def blocks(self,rows,cols,c,color):
  return VGroup(*[Square(side_length=.43,color=color,stroke_width=1,fill_color=color,fill_opacity=.13).move_to(np.array(c)+np.array([(j-(cols-1)/2)*.5,((rows-1)/2-i)*.5,0])) for i in range(rows) for j in range(cols)])
 def weightbar(self,alpha,y=-.45):
  alpha=min(max(alpha,0),1);x=-4.5;w=9;g=VGroup()
  if alpha>1e-8:g.add(Rectangle(width=w*alpha,height=.32,stroke_width=0,fill_color=PURPLE,fill_opacity=1).move_to([x+w*alpha/2,y,0]))
  if alpha<1-1e-8:g.add(Rectangle(width=w*(1-alpha),height=.32,stroke_width=0,fill_color=BLUEC,fill_opacity=1).move_to([x+w*alpha+w*(1-alpha)/2,y,0]))
  return g
 def construct(self):
  self.caption_setup();i=self.index;M=A.T@A;CYAN='#2dd4bf';V1=vec(67.5*DEGREES);V2=vec(157.5*DEGREES);lam=np.array([3+2*np.sqrt(2),3-2*np.sqrt(2)])
  if i==0:
   self.reset('구하고 싶은 것은 변환된 벡터의 길이');l,r=self.two();self.add(arrow(l,V1,BLUEC,.95),arrow(r,A@V1,ORANGE,.95));self.eq(r'\|v\|=1',[ -3.45,-1.6,0],36,BLUEC);self.eq(r'\|Av\|=?',[3.45,-1.6,0],36,ORANGE);self.to(5)
   self.reset('벡터의 길이를 수식으로');c=np.array([-3,-.15,0]);v=np.array([1.6,1.2]);self.add(grid(c),arrow(c,v,BLUEC,1),DashedLine(c,c+RIGHT*1.6,color=BLUEC),DashedLine(c+RIGHT*1.6,c+np.r_[v,0],color=CYAN),label('x',c+RIGHT*.8+DOWN*.3,26,BLUEC),label('y',c+RIGHT*1.9+UP*.6,26,CYAN));self.eq(r'v=\begin{pmatrix}x\\y\end{pmatrix}',[2.5,.8,0],45);self.to(8)
   self.add(Square(side_length=1.6,color=BLUEC,fill_color=BLUEC,fill_opacity=.12).move_to(c+RIGHT*.8+DOWN*.8),Square(side_length=1.2,color=CYAN,fill_color=CYAN,fill_opacity=.12).move_to(c+RIGHT*2.2+UP*.6));f=self.eq(r'\|v\|=\sqrt{x^2+y^2}',[2.5,-1,0],44,BLUEC,width=6);self.to(14);f=self.replace_eq(f,r'\|v\|^2=x^2+y^2',color=BLUEC);self.to(18)
   self.reset('제곱의 합을 벡터의 곱으로');self.add(label('전치: 공간 회전이 아닌 행·열 표현의 변경',[0,2.4,0],25,MUTED));column=self.eq(r'v=\begin{pmatrix}x\\y\end{pmatrix}',[-3,.9,0],46,BLUEC);row=self.eq(r'v^T=\begin{pmatrix}x&y\end{pmatrix}',[2.8,.9,0],46,CYAN);self.to(20)
   f=self.eq(r'v^Tv=\begin{pmatrix}x&y\end{pmatrix}\begin{pmatrix}x\\y\end{pmatrix}',[0,-.6,0],42);self.to(22);f=self.replace_eq(f,r'v^Tv=x\cdot x+y\cdot y=x^2+y^2',color=BLUEC);self.to(24)
   self.reset('차원이 달라도 같은 표현');self.eq(r'\mathbb{R}^2:\quad v^Tv=x_1^2+x_2^2',[0,1.8,0],40,BLUEC);self.eq(r'\mathbb{R}^3:\quad v^Tv=x_1^2+x_2^2+x_3^2',[0,.5,0],40,CYAN);self.eq(r'\mathbb{R}^n:\quad \|v\|^2=v^Tv=\sum_{i=1}^n x_i^2',[0,-1.2,0],44,PURPLE);self.to(29)
  elif i==1:
   self.reset('변환된 벡터의 길이 제곱은?');l,r=self.two();self.add(arrow(l,np.array([1,1])/np.sqrt(2),BLUEC,.95),arrow(r,A@np.array([1,1])/np.sqrt(2),ORANGE,.95));f=self.eq(r'\|v\|^2=v^Tv',[0,-1.9,0],44,BLUEC);self.to(34);f=self.replace_eq(f,r'\|Av\|^2=(Av)^T(Av)',color=ORANGE);self.to(38)
   self.reset('곱의 전치에서는 순서가 반대로 바뀐다');self.eq(r'(PQ)^T=Q^TP^T',[0,2.05,0],38,MUTED);a=self.eq(r'(Av)^T',[0,.9,0],58,ORANGE);self.to(40);a=self.replace_eq(a,r'v^TA^T',size=58,color=CYAN);f=self.eq(r'\|Av\|^2=v^TA^TAv',[0,-1.2,0],47);self.to(43)
   self.reset('두 벡터 사이에 나타난 새로운 행렬');self.eq(r'\|Av\|^2=v^T\underbrace{A^TA}_{M}v',[0,1.35,0],54,CYAN);self.to(45);m=self.eq(r'M=A^TA',[0,-.3,0],62,CYAN);self.to(47);self.eq(r'\|Av\|^2=v^TMv',[0,-1.8,0],43);self.to(48)
   self.reset('길이를 측정하다 보니 새로운 행렬이 나타났다')
   for x,s,t,color in [(-4.6,r'\|Av\|','변환된 벡터의 길이',BLUEC),(0,r'(Av)^T(Av)','길이 제곱을 내적으로',ORANGE),(4.6,r'A^TA','새로운 행렬',CYAN)]:
    self.add(RoundedRectangle(width=3.7,height=2.3,color=color,stroke_width=1).move_to([x,.7,0]));self.eq(s,[x,1,0],42,color,width=3.3);self.add(label(t,[x,.05,0],23,MUTED))
   self.add(Arrow([-2.65,.7,0],[-1.95,.7,0]),Arrow([1.95,.7,0],[2.65,.7,0]));self.eq(r'v^TMv=\|Av\|^2',[0,-1.5,0],49,CYAN);self.to(54);self.add(label('A: 벡터의 변환     M: 길이 제곱을 측정하는 이차형식',[0,-2.3,0],25,MUTED));self.to(57)
  elif i==2:
   self.reset('새로운 행렬의 중요한 성질');self.eq(r'M=A^TA',[0,1.9,0],55,CYAN)
   for x,s in [(-4.5,'정사각행렬'),(0,'대칭행렬'),(4.5,'정규직교 고유기저')]:self.add(label(s,[x,.25,0],29,CYAN))
   self.eq(r'v^TMv=\|Av\|^2\geq0',[0,-1.65,0],37,MUTED);self.to(60)
   self.reset('직사각행렬에서도 정사각행렬이 만들어진다');self.add(label('크기 설명용 일반 예시: A는 3×2 행렬',[0,2.4,0],25,MUTED))
   for c,rows,cols,name,size in [([-4.5,.5,0],2,3,'Aᵀ','2 × 3'),([0,.5,0],3,2,'A','3 × 2'),([4.5,.5,0],2,2,'M','2 × 2')]:
    self.add(self.blocks(rows,cols,c,CYAN),label(name,np.array(c)+UP*1.35,33,CYAN),label(size,np.array(c)+DOWN*1.4,30,CYAN))
   self.add(label('×',[-2.3,.5,0],35),label('=',[2.3,.5,0],35));self.eq(r'(n\times m)(m\times n)\longrightarrow n\times n',[0,-2.15,0],34);self.to(66)
   self.reset('전단행렬로 돌아오면: 대칭행렬 M');m=self.eq(r'M=A^TA=\begin{pmatrix}1&0\\2&1\end{pmatrix}\begin{pmatrix}1&2\\0&1\end{pmatrix}=\begin{pmatrix}1&2\\2&5\end{pmatrix}',[0,1.2,0],45,CYAN);self.eq(r'M^T=(A^TA)^T=A^TA=M',[0,-.7,0],43,CYAN);self.add(label('대각선 양쪽의 두 원소 2는 서로 같다',[0,-2,0],28,MUTED));self.to(71)
   self.reset('실수 대칭행렬은 정규직교 고유기저를 갖는다');c=np.array([-2.7,.1,0]);self.add(grid(c),arrow(c,V1,PURPLE,1.7),arrow(c,V2,BLUEC,1.7),DashedLine(c-np.r_[V1,0]*1.9,c+np.r_[V1,0]*1.9,color=PURPLE),DashedLine(c-np.r_[V2,0]*1.9,c+np.r_[V2,0]*1.9,color=BLUEC));self.eq(r'Mv_i=\lambda_i v_i',[2.5,1,0],44,CYAN);self.eq(r'v_1^Tv_2=0',[2.5,-.3,0],45);self.eq(r'\|v_1\|=\|v_2\|=1',[2.5,-1.6,0],38);self.to(78)
  elif i==3:
   self.reset('고유벡터를 길이 1로 정규화');c=np.array([0,.25,0]);ar=arrow(c,V1,PURPLE,1.9);self.add(Circle(radius=1.15,color=BLUEC).move_to(c),ar);self.play(Transform(ar,arrow(c,V1,PURPLE,1.15)),run_time=2);self.eq(r'\|v_i\|=1',[0,-1.9,0],46,PURPLE);self.to(82)
   self.reset('지금 적용하는 행렬은 A가 아닌 M');l=np.array([-3.5,.1,0]);r=np.array([3.5,.1,0]);scale=.4;self.add(grid(l,scale=scale),grid(r,scale=scale),arrow(l,V1,PURPLE,scale),arrow(r,V1,PURPLE,scale),Arrow([-.65,.1,0],[.65,.1,0],color=CYAN),label('M',[0,.65,0],30,CYAN));out=arrow(r,V1,PURPLE,scale);self.add(out);self.play(Transform(out,arrow(r,M@V1,CYAN,scale)),run_time=2);self.eq(r'Mv_1=\lambda_1v_1,\quad\lambda_1=3+2\sqrt2\approx5.828',[0,-1.9,0],38,CYAN);self.to(88)
   self.reset('길이 제곱 식에 고유벡터 관계 대입');self.eq(r'Mv_i=\lambda_i v_i',[0,2,0],40,CYAN);f=self.eq(r'\|Av_i\|^2=v_i^TMv_i',[0,.35,0],52);self.to(90);f=self.replace_eq(f,r'\|Av_i\|^2=v_i^T(\lambda_i v_i)',size=52);self.to(92)
   f=self.replace_eq(f,r'\|Av_i\|^2=\lambda_i(v_i^Tv_i)',size=52);self.eq(r'\lambda_i\text{ is a scalar}',[0,-1.3,0],31,GREEN);self.to(97)
   self.reset('단위벡터의 내적은 1');c=np.array([-3,.15,0]);self.add(Circle(radius=1.5,color=BLUEC).move_to(c),arrow(c,V1,PURPLE,1.5));self.eq(r'v_i^Tv_i=\|v_i\|^2=1',[2,.7,0],46,PURPLE,width=7);self.eq(r'\|Av_i\|^2=\lambda_i\cdot1',[2,-.9,0],42);self.to(102)
   self.reset('원래 행렬 A의 길이 제곱 = M의 고윳값');self.eq(r'\boxed{\|Av_i\|^2=\lambda_i}',[0,.9,0],64,GREEN);self.eq(r'\lambda_i\geq0\quad\text{since}\quad\|Av_i\|^2\geq0',[0,-1.1,0],38,MUTED);self.to(107)
   self.reset('길이 제곱에서 실제 길이로');self.eq(r'\lambda_1=3+2\sqrt2\approx5.828',[0,1.6,0],44,GREEN);self.eq(r'\Downarrow\quad\sqrt{\phantom{\lambda_1}}',[0,.4,0],43);self.eq(r'\sigma_1=\sqrt{\lambda_1}=1+\sqrt2\approx2.414',[0,-.8,0],46,PURPLE);self.eq(r'\|Av_i\|=\sqrt{\lambda_i}',[0,-2.1,0],38);self.to(112)
  elif i==4:
   self.reset('왜 이 방향에서 최대와 최소가 나타날까?');c=np.array([-2.2,.3,0]);self.add(self.ellipse(c,1.15),Line(c-np.r_[A@V1,0]*1.15,c+np.r_[A@V1,0]*1.15,color=PURPLE),Line(c-np.r_[A@V2,0]*1.15,c+np.r_[A@V2,0]*1.15,color=BLUEC),label('왜 최대일까?',[3.7,1,0],32,PURPLE),label('왜 최소일까?',[3.7,-.4,0],32,BLUEC));self.to(118)
   self.reset('임의의 단위벡터를 고유기저로 표현');c=np.array([-3,.1,0]);v=.8*V1+.6*V2;p1=c+np.r_[.8*V1,0]*1.8;p=c+np.r_[v,0]*1.8;self.add(Circle(radius=1.8,color=MUTED).move_to(c),arrow(c,V1,PURPLE,1.8),arrow(c,V2,BLUEC,1.8),arrow(c,v,WHITE,1.8),DashedLine(p1,p,color=MUTED));self.eq(r'v=c_1v_1+c_2v_2',[2.8,1,0],43,width=6);self.eq(r'c_1=0.8,\quad c_2=0.6',[2.8,-.4,0],36,MUTED,width=6);self.to(123)
   self.reset('직교성 때문에 교차항이 사라진다');self.eq(r'v^TMv=(c_1v_1+c_2v_2)^TM(c_1v_1+c_2v_2)',[0,1.8,0],39);f=self.eq(r'=\lambda_1c_1^2+\lambda_2c_2^2+c_1c_2(\lambda_1+\lambda_2)\underbrace{v_1^Tv_2}_{0}',[0,.25,0],39);self.to(127);f=self.replace_eq(f,r'\|Av\|^2=\lambda_1c_1^2+\lambda_2c_2^2',size=53);self.eq(r'v_1^Tv_2=0\quad\text{and}\quad v_i^Tv_i=1',[0,-1.5,0],36,MUTED);self.to(132)
   self.reset('단위벡터이므로 두 성분의 제곱합은 1');self.eq(r'\|v\|^2=c_1^2+c_2^2=1',[0,1.5,0],52);self.add(self.weightbar(.64,y=-.2));self.eq(r'c_1^2=0.64',[ -2.6,-1.05,0],36,PURPLE);self.eq(r'c_2^2=0.36',[2.7,-1.05,0],36,BLUEC);self.to(136)
   self.reset('길이 제곱은 두 고윳값의 가중평균');self.eq(r'\|Av\|^2=\lambda_1c_1^2+\lambda_2c_2^2',[0,1.7,0],49);self.add(self.weightbar(.64,y=.35));self.eq(r'0.64\lambda_1+0.36\lambda_2',[0,-.7,0],46,GREEN);self.eq(r'c_1^2,c_2^2\geq0,\qquad c_1^2+c_2^2=1',[0,-1.9,0],35,MUTED);self.to(141)
   self.reset('가중평균은 두 고윳값 사이에 머문다');alpha=ValueTracker(.64);bar=always_redraw(lambda:self.weightbar(alpha.get_value(),y=1.7));self.add(bar);line=NumberLine(x_range=[0,6,1],length=10,color=MUTED).move_to([0,-.25,0]);self.add(line);self.add(Dot(line.n2p(lam[0]),color=PURPLE),Dot(line.n2p(lam[1]),color=BLUEC));self.eq(r'\lambda_2\approx0.172',[-3.6,-1.05,0],30,BLUEC);self.eq(r'\lambda_1\approx5.828',[3.5,-1.05,0],30,PURPLE);dot=always_redraw(lambda:Dot(line.n2p(alpha.get_value()*lam[0]+(1-alpha.get_value())*lam[1]),color=ORANGE,radius=.09));self.add(dot);self.eq(r'\lambda_2\leq\|Av\|^2\leq\lambda_1',[0,-2.1,0],42);self.play(alpha.animate.set_value(1),run_time=1);self.play(alpha.animate.set_value(0),run_time=2);self.play(alpha.animate.set_value(.64),run_time=1)
   self.reset('고유방향에서 최대·최소 길이를 찾는다');l=np.array([-3.45,1,0]);r=np.array([3.45,1,0]);scale=.75;self.add(Circle(radius=scale,color=BLUEC).move_to(l),self.ellipse(r,scale),label('입력 단위벡터',[-3.45,2.5,0],25,BLUEC),label('출력 Av',[3.45,2.5,0],25,ORANGE));t=ValueTracker(np.arctan2(.6,.8))
   def inp():return np.cos(t.get_value())*V1+np.sin(t.get_value())*V2
   ar=always_redraw(lambda:VGroup(arrow(l,inp(),WHITE,scale),arrow(r,A@inp(),ORANGE,scale)));bars=always_redraw(lambda:self.weightbar(np.cos(t.get_value())**2,y=-.55));self.add(ar,bars)
   self.eq(r'c_1^2=\cos^2\phi,\quad c_2^2=\sin^2\phi',[0,-1.35,0],35);num=DecimalNumber(0,mob_class=Text,num_decimal_places=3,font_size=32,color=ORANGE).move_to([2,-2.1,0]);num.add_updater(lambda m:m.set_value(np.linalg.norm(A@inp())**2));self.add(label('길이 제곱 ≈',[-.8,-2.1,0],27,ORANGE),num);self.play(t.animate.set_value(0),run_time=4);self.play(t.animate.set_value(PI/2),run_time=4)
   self.reset('M의 고유벡터 → 타원의 반축에 대응하는 입력 방향');l,r=self.two();self.add(arrow(l,V1,PURPLE,.95),arrow(l,V2,BLUEC,.95),arrow(r,A@V1,PURPLE,.95),arrow(r,A@V2,BLUEC,.95));self.eq(r'(Av_1)^T(Av_2)=\lambda_2v_1^Tv_2=0',[0,-1.85,0],39);self.add(label('입력과 출력은 서로 다른 방향 · 두 출력은 서로 직교',[0,-2.4,0],24,MUTED));self.to(158)
  else:
   self.reset('기하학적 관찰에서 특잇값의 정의로');f=self.eq(r'A=\begin{pmatrix}1&2\\0&1\end{pmatrix}',[0,.8,0],57);self.to(160);f=self.replace_eq(f,r'A^TA=\begin{pmatrix}1&2\\2&5\end{pmatrix}',size=57,color=CYAN);self.to(162);f=self.replace_eq(f,r'\lambda_1=3+2\sqrt2,\quad\lambda_2=3-2\sqrt2',size=48,color=GREEN);self.to(164);f=self.replace_eq(f,r'\sigma_1=1+\sqrt2,\quad\sigma_2=\sqrt2-1',size=48,color=PURPLE);self.to(166);f=self.replace_eq(f,r'\boxed{\sigma_i(A)=\sqrt{\lambda_i(A^TA)}}',size=58,color=PURPLE,duration=.6);self.to(167)
   self.reset('같은 도구, 새로운 대상');self.add(label('실수 행렬 A ∈ ℝᵐˣⁿ: 특잇값은 min(m, n)개',[0,2.45,0],24,MUTED))
   for x,name,content,color in [(-4.6,'A',r'\lambda=1,1',WHITE),(0,'AᵀA',r'\lambda\approx5.828,0.172',CYAN),(4.6,'√λ',r'\sigma\approx2.414,0.414',PURPLE)]:
    self.add(RoundedRectangle(width=3.8,height=3.3,color=color,stroke_width=1).move_to([x,.25,0]),label(name,[x,1.3,0],40,color));self.eq(content,[x,-.1,0],31,color,width=3.35)
   self.to(171);self.eq(r'\sigma_i(A)=\sqrt{\lambda_i(A^TA)}',[0,-2.1,0],42,PURPLE);self.to(175)
   self.reset('특잇값에 담긴 정보');c=np.array([-4.4,.45,0]);s=ValueTracker(1)
   collapsing=always_redraw(lambda:ParametricFunction(lambda t: c+np.array([1.6*np.cos(t),.9*s.get_value()*np.sin(t),0]),t_range=[0,TAU,.05],color=PURPLE,stroke_width=3));self.add(collapsing,label('랭크와 정보 소실',[-4.4,-1.4,0],27));self.eq(r'\sigma_2\to0',[-4.4,-2.05,0],35,PURPLE);self.play(s.animate.set_value(.4),run_time=2)
   mid=VGroup(Ellipse(width=3,height=1.5,color=ORANGE).move_to([0,.45,0]),label('공간의 부피 변화',[0,-1.4,0],27));right=VGroup(Ellipse(width=3,height=.35,color=PURPLE).move_to([4.4,.45,0]),Arrow([4.4,.45,0],[4.4,1.8,0],color='#ff627e'),label('계산의 안정성',[4.4,-1.4,0],27));self.add(mid,right);eq1=self.eq(r'\sigma_1\sigma_2',[0,-2.05,0],35,PURPLE);eq2=self.eq(r'\sigma_1/\sigma_2',[4.4,-2.05,0],35,PURPLE);self.to(179);self.remove(mid,right,eq1,eq2);self.play(s.animate.set_value(0),run_time=1)
