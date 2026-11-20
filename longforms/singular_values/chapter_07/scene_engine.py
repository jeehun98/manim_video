from visual_common import *
config.background_color='#10141e'
STARTS=[0,12,25,60,72];ENDS=[12,25,60,72,90]
A=B

def vec(t):return np.array([np.cos(t),np.sin(t)])
def norm(t):return np.linalg.norm(A@vec(t))
class ConnectionsScene(Scene):
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
 def disk(self,c,d=[1,1],scale=1,color=BLUEC,fill=.15):
  d=np.array(d);c=np.array(c)
  return ParametricFunction(lambda t:c+np.r_[d*vec(t),0]*scale,t_range=[0,TAU,.03],color=color,stroke_width=3,fill_color=color,fill_opacity=fill)
 def arr(self,c,v,color,scale=1):
  if np.linalg.norm(v)==0:return Dot(c,color=color,radius=.055)
  return arrow(c,v,color,scale)
 def planes(self,left='입력',right='출력',middle='B'):
  l=np.array([-3.45,.25,0]);r=np.array([3.45,.25,0]);self.add(grid(l),grid(r),label(left,[-3.45,2.35,0],26,BLUEC),label(right,[3.45,2.35,0],26,ORANGE),Arrow([-.6,.25,0],[.6,.25,0]),label(middle,[0,.8,0],28));return l,r
 def error_pair(self,c,exact,noisy,scale=1.2):
  c=np.array(c);p=c+np.r_[exact,0]*scale;q=c+np.r_[noisy,0]*scale
  return VGroup(self.arr(c,exact,'#2dd4bf',scale),self.arr(c,noisy,'#fb7185',scale),Dot(p,color='#2dd4bf',radius=.035),Dot(q,color='#fb7185',radius=.035),Line(p,q,color='#fb7185',stroke_width=4))
 def ellipse(self,c,M=A,scale=.9,color=ORANGE):
  c=np.array(c);return ParametricFunction(lambda t:c+np.r_[M@vec(t),0]*scale,t_range=[0,TAU,.025],color=color,fill_color=color,fill_opacity=.13,stroke_width=3)
 def axes_svd(self,c,M=A,scale=.9):
  u,s,v=np.linalg.svd(M);c=np.array(c);g=VGroup()
  for k in range(2):
   w=u[:,k]*s[k]*scale
   if w[0]<0:w=-w
   p=c+np.r_[w,0];g.add(Line(c,p,color=PURPLE,stroke_width=5),label('σ'+str(k+1),p+UP*.24,24,PURPLE))
  return g
 def card(self,k,done=False):
  colors=[PURPLE,GREEN,'#facc15','#fb7185'];titles=['크기','개수','곱','비율'];values=['길이 변화','랭크와 차원','부피 변화','오차 민감도'];forms=[r'\sigma_i',r'\#\{i:\sigma_i>0\}',r'\prod_i\sigma_i',r'\sigma_{\max}/\sigma_{\min}']
  c=np.array([-4.8+3.2*k,-1.98,0]);box=RoundedRectangle(width=2.9,height=1.05,corner_radius=.1,color=colors[k],stroke_width=1.5,fill_color=colors[k],fill_opacity=.06).move_to(c)
  return VGroup(box,label(titles[k]+' · '+(values[k] if done else '?'),c+UP*.27,21,colors[k]),MathTex(forms[k],font_size=27,color=colors[k]).move_to(c+DOWN*.22))
 def construct(self):
  self.caption_setup();i=self.index;CYAN='#2dd4bf';RED='#fb7185';YEL='#facc15';U,S,VT=np.linalg.svd(A)
  if i==0:
   self.reset('하나의 행렬은 방향마다 길이를 다르게 바꾼다');l,r=self.pair(scale=.9);v=vec(PI/4);a=self.arr(l,v,BLUEC,.9);b=self.arr(r,v,ORANGE,.9);self.add(a,b);self.play(Transform(b,self.arr(r,A@v,ORANGE,.9)),run_time=1.6)
   rays=VGroup(*[self.arr(l,vec(t),BLUEC,.9) for t in np.linspace(0,TAU,12,endpoint=False)]);outs=VGroup(*[self.arr(r,A@vec(t),ORANGE,.9) for t in np.linspace(0,TAU,12,endpoint=False)]);self.play(FadeIn(rays),FadeIn(outs),run_time=1.4);self.eq(r's(v)=\frac{\|Av\|_2}{\|v\|_2}',[0,-2,0],39,PURPLE);self.to(5)
   circle=self.ellipse(l,np.eye(2),.9,BLUEC);ell=self.ellipse(r,A,.9);self.play(Create(circle),Create(ell),run_time=2);self.play(FadeOut(rays),FadeOut(outs),FadeOut(a),FadeOut(b),run_time=.7);self.play(Create(self.axes_svd(r)),run_time=1.3);self.eq(r'\sigma_1=1+\sqrt2,\qquad\sigma_2=\sqrt2-1',[0,-1.1,0],34,PURPLE);self.to(12)
  elif i==1:
   self.reset('長이의 제곱을 표현하면 AᵀA가 나타난다'.replace('長','길'));f=self.eq(r'\|Av\|_2^2',[0,.65,0],66,BLUEC);self.to(14);f=self.replace_eq(f,r'(Av)^T(Av)',size=66);self.to(16);f=self.replace_eq(f,r'v^T\underbrace{A^TA}_{M}v',size=66);self.to(18);self.eq(r'M=A^TA=\begin{pmatrix}1&2\\2&5\end{pmatrix}',[0,-1.6,0],45,CYAN);self.to(19)
   self.reset('새로운 행렬의 고윳값에서 길이 변화 배율로');self.eq(r'A^TA\ \longrightarrow\ \lambda_i\ \longrightarrow\ \sigma_i=\sqrt{\lambda_i}',[0,1.6,0],51,PURPLE);self.add(label('A 자체의 고윳값과 구별한다',[0,2.45,0],24,MUTED));self.to(21);self.eq(r'\lambda_{1,2}=3\pm2\sqrt2',[ -3,.1,0],37,GREEN);self.eq(r'\sigma_1=1+\sqrt2\approx2.414',[ -3,-.75,0],33,PURPLE);self.eq(r'\sigma_2=\sqrt2-1\approx0.414',[ -3,-1.5,0],33,PURPLE);self.play(Create(self.ellipse([3.2,-.1,0])),Create(self.axes_svd([3.2,-.1,0])),run_time=1.5);self.to(25)
  elif i==2:
   self.reset('같은 숫자에 네 가지 관찰을 적용한다');self.eq(r'\sigma_1=1+\sqrt2,\quad\sigma_2=\sqrt2-1',[0,2.1,0],40,PURPLE);cards=[self.card(k) for k in range(4)];self.play(LaggedStart(*[FadeIn(c) for c in cards],lag_ratio=.25),run_time=2);self.eq(r'\sigma_1,\sigma_2,\ldots,\sigma_n',[0,.5,0],54,PURPLE);self.add(label('크기를 보고 · 개수를 세고 · 곱하고 · 나눈다',[0,-.5,0],30));self.to(33)
   # Keep the four observation cards throughout this entire independent group.
   for m in list(self.mobjects):
    if m not in [self.cap,self.bar,*cards]:self.remove(m)
   self.add(label('개별 특잇값 · 주축 방향의 길이 변화',[0,3.2,0],32));geometry=VGroup(self.ellipse([-3,.6,0]),self.axes_svd([-3,.6,0]));self.add(geometry);self.eq(r'\|Av_i\|_2=\sigma_i\quad(\|v_i\|_2=1)',[2.8,1.1,0],36,PURPLE,width=6);self.eq(r'2.414\qquad0.414',[2.8,.1,0],44,PURPLE);self.to(38);self.play(Transform(cards[0],self.card(0,True)),run_time=.7);self.to(39)
   for m in list(self.mobjects):
    if m not in [self.cap,self.bar,*cards]:self.remove(m)
   self.add(label('양의 특잇값 개수 · 남아 있는 차원',[0,3.2,0],32),label('별도 가변 예시: diag(2, t)',[0,2.35,0],25,MUTED));t=ValueTracker(.7);geo=always_redraw(lambda:self.ellipse([-3,.6,0],np.diag([2,t.get_value()]),.8));self.add(geo);self.eq(r'\operatorname{rank}(A)=\#\{i:\sigma_i>0\}',[2.7,1,0],36,GREEN,width=6);status=label('t > 0 : rank = 2',[2.7,.1,0],31,GREEN);self.add(status);self.to(41);self.play(t.animate.set_value(0),run_time=2,rate_func=linear);self.remove(geo);self.add(Line([-4.6,.6,0],[-1.4,.6,0],color=ORANGE,stroke_width=4),Dot([-3,.6,0],color=RED));self.play(Transform(status,label('t = 0 : rank = 1',[2.7,.1,0],31,GREEN)),run_time=.5);self.to(45);self.play(Transform(cards[1],self.card(1,True)),run_time=.7);self.to(46)
   for m in list(self.mobjects):
    if m not in [self.cap,self.bar,*cards]:self.remove(m)
   self.add(label('すべて'.replace('すべて','모든')+' 특잇값의 곱 · 넓이와 부피',[0,3.2,0],32),label('정사각행렬 · A = [[1, 2], [0, 1]]',[0,2.4,0],24,MUTED));self.add(self.ellipse([-3,.6,0],np.eye(2),.85,BLUEC),self.ellipse([3,.6,0],A,.85));self.eq(r'|\det A|=\prod_i\sigma_i=1',[0,-.75,0],41,YEL);self.play(FadeIn(shape([-3,.6,0],scale=.85)),FadeIn(shape([3,.6,0],A,ORANGE,.85)),run_time=1);self.to(50);self.play(Transform(cards[2],self.card(2,True)),run_time=.7);self.to(51)
   for m in list(self.mobjects):
    if m not in [self.cap,self.bar,*cards]:self.remove(m)
   self.add(label('최대·최소 특잇값의 비율 · 상대 오차 민감도',[0,3.2,0],32));self.eq(r'\kappa_2(A)=\frac{\sigma_{\max}}{\sigma_{\min}}=3+2\sqrt2\approx5.828',[0,2.15,0],43,RED);p=ValueTracker(0);y=np.array([1.,.2]);dy=np.array([0,.04]);c=np.array([0,.2,0]);exact=always_redraw(lambda:self.error_pair(c,(np.eye(2)+p.get_value()*(np.linalg.inv(A)-np.eye(2)))@y,(np.eye(2)+p.get_value()*(np.linalg.inv(A)-np.eye(2)))@(y+dy),1.4));self.add(exact,label('正確'.replace('正確','정확한 출력')+'과 오차 출력이 같은 역변환을 받는다',[0,-.8,0],25,MUTED));self.to(54);self.play(p.animate.set_value(1),run_time=2,rate_func=linear);self.add(label('고정된 가역행렬 · 2-노름 · 상대 오차의 최악 상한',[0,1.3,0],25,MUTED));self.to(58);self.play(Transform(cards[3],self.card(3,True)),run_time=.7);self.to(60)
  elif i==3:
   self.reset('하나의 행렬에서 관찰하는 서로 다른 성질');positions=[[-3.6,1.5,0],[3.6,1.5,0],[-3.6,-.8,0],[3.6,-.8,0]];titles=['고윳값','특잇값','랭크','행렬식'];descs=['고유벡터 방향의 변화','직교하는 주축의 길이 변화','출력 공간의 차원','부피 변화와 방향성'];forms=[r'Av=\lambda v\quad(\lambda=1,1)',r'\sigma=(1+\sqrt2,\sqrt2-1)',r'\operatorname{rank}(A)=2',r'\det A=1'];colors=[GREEN,PURPLE,CYAN,YEL];cards=[]
   for c,title,desc,f,col in zip(positions,titles,descs,forms,colors):
    c=np.array(c);card=VGroup(RoundedRectangle(width=5.7,height=1.85,color=col,stroke_width=1.5,fill_color=col,fill_opacity=.05).move_to(c),label(title,c+UP*.55,30,col),MathTex(f,font_size=30,color=col).move_to(c),label(desc,c+DOWN*.58,22));cards.append(card)
   self.play(LaggedStart(*[FadeIn(c) for c in cards],lag_ratio=.3),run_time=3);self.to(66)
   targets=[[-4.4,1.8,0],[4.4,1.8,0],[-4.4,-1.3,0],[4.4,-1.3,0]];self.play(*[c.animate.scale(.72).move_to(t) for c,t in zip(cards,targets)],run_time=1.3);center=np.array([0,.3,0]);self.play(Create(self.ellipse(center,scale=.6)),run_time=1);self.add(label('하나의 선형변환 A',[0,-.9,0],28));links=VGroup(*[Line(center,np.array(t),color=col,stroke_opacity=.45).set_z_index(-1) for t,col in zip(targets,colors)]);self.play(Create(links),run_time=1.2);self.add(label('조건수: 특잇값의 비율 → 상대 오차 민감도',[0,-2.3,0],25,RED));self.to(72)
  else:
   self.reset('숫자들의 배열에서 공간을 바꾸는 연산으로');matrix=self.eq(r'A=\begin{pmatrix}1&2\\0&1\end{pmatrix}',[-3.8,.7,0],62);c=np.array([2.8,.5,0]);self.to(74);self.eq(r'Ae_1=\binom10,\quad Ae_2=\binom21',[-3.8,-1.2,0],33,BLUEC,width=5.8);basis1=self.arr(c,A[:,0],BLUEC,.8);basis2=self.arr(c,A[:,1],GREEN,.8);self.play(TransformFromCopy(matrix,basis1),TransformFromCopy(matrix,basis2),run_time=1.4);self.to(77);self.remove(basis1,basis2)
   t=ValueTracker(0);field=always_redraw(lambda:VGroup(grid(c,np.array([[1,2*t.get_value()],[0,1]]),.8),self.ellipse(c,np.array([[1,2*t.get_value()],[0,1]]),.8),self.arr(c,np.array([1,0]),BLUEC,.8),self.arr(c,np.array([2*t.get_value(),1]),GREEN,.8)));self.add(field);self.play(t.animate.set_value(1),run_time=2,rate_func=linear);self.add(label('길이 · 차원 · 부피 · 민감도',[0,-2.2,0],30,PURPLE));self.to(82)
   self.reset('공간의 변화에 담긴 정보를 읽어내는 숫자');c=np.array([0,1.3,0]);final_geometry=VGroup(self.ellipse(c,scale=.8),self.axes_svd(c,scale=.8));self.add(final_geometry);f=self.eq(r'\sigma_i=\sqrt{\lambda_i(A^TA)}',[0,-.15,0],42,PURPLE);cards=[self.card(k,True) for k in range(4)];self.play(LaggedStart(*[FadeIn(card) for card in cards],lag_ratio=.3),run_time=2);self.play(Create(VGroup(*[Line([0,-.5,0],[-4.8+3.2*k,-1.4,0],stroke_width=1,color=PURPLE).set_z_index(-1) for k in range(4)])),run_time=1.2);self.to(89)
   self.play(*[FadeOut(m) for m in list(self.mobjects) if m not in [self.cap,self.bar,final_geometry]],run_time=.5);self.add(label('특잇값 · Singular Values',[0,-.15,0],37,PURPLE));self.to(90)
  self.to(ENDS[i])
