"""Seven replaceable scenes; shared qcs subtitle timing and safe regions."""
import json
from pathlib import Path
from manim import *
import numpy as np
from longforms.qcs01_speed.direction import QCSScene, label, text, p, L, PORTRAIT

HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
config.background_color='#0B1020'
INK,BLUE,GREEN,ORANGE,MUTED='#E5E7EB','#60A5FA','#2DD4BF','#F59E0B','#8D9BB6'
FORMS=[r'x^2-6x+8',r'(x-2)(x-4)',r'(x-3)^2-1']

def eq(s,x=0,y=0,size=44,color=INK,width=7):
 o=MathTex(s,font_size=size*1.35,color=color)
 if o.width>width:o.scale_to_fit_width(width)
 return o.move_to(p(x,y))

def node(s,x,y,color=GREEN,r=.57):
 return VGroup(Circle(radius=r,color=color,fill_color=color,fill_opacity=.09).move_to(p(x,y)),label(s,x,y,27,color,width=r*1.7))

def link(a,b,color=GREEN):
 return Line(a.get_center(),b.get_center(),buff=.62,color=color,stroke_width=2).set_z_index(-1)

def relation_graph(y=.5,scale=1):
 points=[(-2,1.5),(0,2.5),(2,1.5),(-2,-.7),(0,-1.8),(2,-.7),(0,.4)]
 dots=VGroup(*[Dot(p(x*scale,y+v*scale),radius=.10,color=BLUE if i==6 else GREEN) for i,(x,v) in enumerate(points)])
 edges=VGroup(*[Line(dots[a].get_center(),dots[b].get_center(),color=GREEN,stroke_opacity=.65,stroke_width=2) for a,b in [(0,1),(1,2),(0,3),(2,5),(3,4),(4,5),(0,6),(2,6),(4,6)]])
 return VGroup(edges,dots)

class IdeaScene(QCSScene):
 data=DATA
 def replace(self,old,new):
  return Scene.replace(self,old,new)
 def setup(self):
  super().setup()
  self.remove(self.mobjects[0])
  self.add(text('과학 한조각  /  아이디어 노트',y=L.brand_y,size=18,color=MUTED))

 def clear_body(self):
  keep=[self.title,self.caption,self.caption_panel]
  objects=[o for o in self.mobjects if all(o is not k for k in keep) and o.get_center()[1]<6.5]
  if objects:self.play(*[FadeOut(o) for o in objects],run_time=.45)

 def s01(self):
  forms=[r'a^2+b^2',r'\int f(x)\,dx',r'\nabla f',r'Ax=b',r'\frac{df}{dt}',r'\sum_{k=1}^{n}a_k']
  g=VGroup(*[eq(s,size=39) for s in forms]).arrange_in_grid(rows=3,cols=2,buff=(1.0,1.0)).move_to(p(0,.8))
  self.play(LaggedStart(*[Write(o) for o in g],lag_ratio=.15),run_time=2)
  self.to(4)
  a=eq('a+b',-2,1.8);b=eq('b+a',2,1.8)
  c=eq('u+v',-2,-.2);d=eq('v+u',2,-.2)
  self.play(ReplacementTransform(g,VGroup(a,b,c,d)),run_time=.8)
  arrows=VGroup(DoubleArrow(p(-.8,1.8),p(.8,1.8),color=GREEN,buff=0),DoubleArrow(p(-.8,-.2),p(.8,-.2),color=GREEN,buff=0))
  self.show(arrows,label('실수의 덧셈',y=-2,size=25,color=MUTED))
  self.to(8);self.clear_body()
  graph=relation_graph(y=.9,scale=.72);self.show(graph)
  self.play(graph.animate.scale(.72),run_time=1)
  self.show(label('최소한의 표현이 가능할까?',y=-2,size=35,color=ORANGE),eq('?',x=2.4,y=1.2,color=ORANGE,size=70))

 def s02(self):
  axes=Axes(x_range=[0,6,1],y_range=[-2,9,2],x_length=6.5,y_length=4.4,tips=False,axis_config={'color':MUTED,'stroke_width':1.5}).move_to(p(0,-.55))
  curve=axes.plot(lambda x:(x-3)**2-1,x_range=[0,6],color=BLUE,stroke_width=4)
  self.add(axes);self.play(Create(curve),run_time=1)
  f=eq(r'f(x)='+FORMS[0],y=3.7,size=43);self.show(f)
  self.to(18)
  new=eq(r'f(x)='+FORMS[1],y=3.7,size=43)
  self.play(TransformMatchingTex(f,new),run_time=1);f=new
  roots=VGroup(*[Dot(axes.c2p(x,0),color=ORANGE,radius=.095) for x in [2,4]])
  values=VGroup(*[eq(str(x),size=30,color=ORANGE).next_to(roots[i],DOWN,buff=.22) for i,x in enumerate([2,4])])
  self.to(23)
  for i in range(2):self.show(roots[i],values[i],run_time=.45)
  self.to(26)
  new=eq(r'f(x)='+FORMS[2],y=3.7,size=43)
  self.play(TransformMatchingTex(f,new),roots.animate.set_opacity(.2),values.animate.set_opacity(.2),run_time=.8);f=new
  self.to(29)
  axis=DashedLine(axes.c2p(3,-2),axes.c2p(3,9),color=GREEN)
  vertex=Dot(axes.c2p(3,-1),color=ORANGE,radius=.11)
  vl=eq('(3,-1)',size=29,color=ORANGE).next_to(vertex,DOWN,buff=.38)
  al=eq('x=3',size=29,color=GREEN).next_to(axis,UP,buff=.1)
  self.play(Create(axis),FadeIn(vertex),FadeIn(vl),FadeIn(al),run_time=1)
  self.to(33)
  rows=VGroup(*[eq(s,size=31) for s in FORMS]).arrange(DOWN,buff=.24).move_to(p(0,3.4))
  self.play(ReplacementTransform(f,rows),run_time=.8)
  self.to(36)
  self.play(Indicate(rows,color=GREEN),Indicate(curve,color=BLUE),roots.animate.set_opacity(1),values.animate.set_opacity(1),run_time=1.1)
  self.note('표현은 다르지만, 함수는 같다.',GREEN)

 def s03(self):
  center=node('f',0,.6,BLUE,r=.75)
  fs=VGroup(eq(FORMS[0],y=3.4,size=38),eq(FORMS[1],x=-1.9,y=-1.5,size=30,width=3.7),eq(FORMS[2],x=1.9,y=-1.5,size=30,width=3.7))
  self.show(fs,center)
  lines=VGroup(*[link(center,o) for o in fs]);self.play(Create(lines),run_time=1)
  self.note('동일한 함수에 연결된 여러 표현 · 개념도')
  self.to(48)
  q1=label('근 찾기',-1.9,-2.5,29,ORANGE,width=3.5);q2=label('최솟값',1.9,-2.5,29,ORANGE,width=3.5)
  self.show(q1,q2)
  self.play(Indicate(fs[1],color=ORANGE),ShowPassingFlash(lines[1].copy().set_color(ORANGE)),run_time=.8)
  self.play(Indicate(fs[2],color=ORANGE),ShowPassingFlash(lines[2].copy().set_color(ORANGE)),run_time=.8)

 def s04(self):
  time_axes=Axes(x_range=[0,2,1],y_range=[-1.6,1.6,1],x_length=6.6,y_length=2.5,tips=False,axis_config={'color':MUTED,'stroke_width':1.2}).move_to(p(0,2.1))
  base=time_axes.plot(lambda t:np.sin(TAU*t),color=BLUE)
  high=time_axes.plot(lambda t:.5*np.sin(3*TAU*t),color=ORANGE)
  combined=time_axes.plot(lambda t:np.sin(TAU*t)+.5*np.sin(3*TAU*t),color=BLUE,stroke_width=3)
  self.show(label('시간 영역',y=4.0,size=28,color=BLUE));self.play(Create(time_axes),Create(base),run_time=1)
  self.to(56);self.play(Create(high),run_time=.8)
  self.play(Transform(base,combined),FadeOut(high),run_time=1)
  dot=Dot(time_axes.c2p(0,0),color=ORANGE,radius=.08)
  self.add(dot);self.play(MoveAlongPath(dot,combined),run_time=1.5,rate_func=linear);self.remove(dot)
  self.to(61)
  freq=Axes(x_range=[0,4,1],y_range=[0,1.3,1],x_length=6.6,y_length=1.8,tips=False,axis_config={'color':MUTED,'stroke_width':1.2}).move_to(p(0,-.7))
  bars=VGroup(*[Line(freq.c2p(f,0),freq.c2p(f,a),color=GREEN,stroke_width=8) for f,a in [(1,1),(3,.5)]])
  tags=VGroup(*[label(f'{f} Hz',size=24,color=GREEN).next_to(freq.c2p(f,0),DOWN,buff=.18) for f in [1,3]])
  self.play(Create(freq),Create(bars),FadeIn(tags),run_time=.9)
  self.show(label('주파수 영역 · 양의 주파수 진폭',y=.65,size=24,color=GREEN))
  formula=eq(r'\widehat{f\,\prime}(\omega)=i\omega\hat f(\omega)',y=-2.65,size=38,color=INK)
  self.show(formula,run_time=.7)
  self.to(65);self.play(Indicate(formula,color=GREEN),run_time=1)
  self.note('적절한 조건에서 성립 · 주기 신호는 급수/분포로 해석')
  self.to(71);self.clear_body()
  center=node('신호',0,.7,BLUE,r=.8)
  a=eq(r'f(t)',-2,2.8,color=BLUE,size=46);b=eq(r'\hat f(\omega)',2,2.8,color=GREEN,size=46)
  self.show(center,a,b);self.play(Create(link(center,a)),Create(link(center,b)),run_time=.8)
  self.show(label('시간의 관점',-2,-1.1,28,BLUE,width=3.5),label('주파수의 관점',2,-1.1,28,GREEN,width=3.5))
  self.show(label('하나의 대상, 서로 다른 표현',y=-2.7,size=32))

 def s05(self):
  self.show(label('무엇이 유지될까?',y=2.8,size=40,color=ORANGE))
  g=relation_graph(y=.2,scale=.67);self.show(g)
  self.to(82)
  self.clear_body()
  fs=VGroup(*[eq(s,size=36) for s in FORMS]).arrange(DOWN,buff=.65).move_to(p(0,1.0))
  self.show(fs);self.to(84)
  g=relation_graph(y=.6,scale=.72)
  self.play(ReplacementTransform(fs,g),run_time=1)
  self.note('표현보다 관계를 남긴다면? · 개념도',GREEN)
  self.to(88);self.clear_body()
  cases=[r'2(3+4)=2\cdot3+2\cdot4',r'x(y+z)=xy+xz',r'A(B+C)=AB+AC']
  rows=VGroup(*[eq(s,size=37,color=c) for s,c in zip(cases,[BLUE,GREEN,ORANGE])]).arrange(DOWN,buff=1.0).move_to(p(0,.8))
  self.show(rows)
  self.note('수 · 스칼라 · 크기가 맞는 행렬의 왼쪽 분배법칙')
  self.to(93)
  rule=eq(r'a(b+c)\longrightarrow ab+ac',y=2,size=43,color=GREEN)
  self.play(ReplacementTransform(rows,rule),run_time=1)
  fresh=eq(r'P(Q+R)',y=-.1,size=44,color=BLUE);self.show(fresh)
  self.to(96)
  result=eq(r'PQ+PR',y=-.1,size=44,color=GREEN)
  self.play(TransformMatchingTex(fresh,result),run_time=1)
  self.to(98);self.show(label('분배법칙',y=-2.1,size=34,color=ORANGE),label('먼저 패턴을, 그다음 이름을',y=-2.9,size=24,color=MUTED))

 def s06(self):
  g=relation_graph(y=.8,scale=.7);self.show(g)
  self.show(label('수학적 관계 → 구조적 학습',y=-2,size=33,color=GREEN))
  self.note('가능한 모델을 상상한 개념도 · 실제 내부 구조 설명 아님')
  self.to(105)
  tokens=eq(r'x\quad{}^2\quad-\quad6\quad x\quad+\quad8',y=3.1,size=36)
  self.show(tokens)
  self.play(*[ShowPassingFlash(edge.copy().set_color(ORANGE),time_width=.6) for edge in g[0]],run_time=1.5)
  self.to(112)
  self.play(g.animate.scale(.08),run_time=1)
  loss=label('보존해야 할 관계는?',y=.0,size=33,color=ORANGE);self.show(loss)
  self.to(115)
  self.play(g.animate.scale(12.5),FadeOut(loss),run_time=.8)
  self.to(117);self.clear_body()
  self.show(label('무엇을 보존할 것인가?',y=3.2,size=35,color=ORANGE))
  a=eq(FORMS[1],y=1.3,size=43,color=GREEN);b=eq(FORMS[2],y=-.8,size=43,color=BLUE)
  self.show(a,b,label('근',x=-2.9,y=1.3,size=25,color=GREEN,width=1),label('최솟값',x=-2.9,y=-.8,size=24,color=BLUE,width=1.5))
  self.show(label('목적에 따라 필요한 표현도 달라진다',y=-2.7,size=29))

 def s07(self):
  fs=VGroup(*[eq(s,size=40) for s in FORMS]).arrange(DOWN,buff=.9).move_to(p(0,1.0))
  self.show(fs)
  lines=VGroup(*[Line(fs[i].get_bottom(),fs[i+1].get_top(),color=GREEN,stroke_width=2,buff=.18) for i in range(2)])
  self.play(Create(lines),run_time=.8)
  self.to(124);question=label('수많은 수식 자체일까?',y=-2.6,size=33);self.show(question)
  self.to(128)
  self.play(fs.animate.set_opacity(.22),lines.animate.set_stroke(width=5),Transform(question,label('아니면, 그 사이의 관계일까?',y=-2.6,size=33,color=GREEN)),run_time=.8)
  self.to(131);self.clear_body()
  g=relation_graph(y=.5,scale=.72);self.show(g)
  outer=VGroup(*[Dot(p(3.1*np.cos(t),.5+3.1*np.sin(t)),radius=.07,color=BLUE) for t in np.linspace(0,TAU,12,endpoint=False)])
  edges=VGroup(*[Line(g[1][i%6].get_center(),d.get_center(),color=GREEN,stroke_width=1.2,stroke_opacity=.45) for i,d in enumerate(outer)])
  self.play(LaggedStart(*[Create(o) for o in edges],lag_ratio=.05),FadeIn(outer),run_time=1.6)
  self.show(label('수식 너머의 공통 구조',y=-3.25,size=35,color=GREEN))
