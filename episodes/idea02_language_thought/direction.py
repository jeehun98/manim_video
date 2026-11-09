"""Narration-led portrait shots; research and imagined models remain distinct."""
import json
from pathlib import Path
import numpy as np
from manim import *
from episodes.idea01_common_structure.direction import IdeaScene,eq,label,text,p,relation_graph,BLUE,GREEN,ORANGE,INK,MUTED

HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
PURPLE='#A78BFA'

def card(s,x=0,y=0,w=5.8,h=1.0,color=BLUE,size=28):
 return VGroup(RoundedRectangle(width=w,height=h,corner_radius=.15,color=color,fill_color=color,fill_opacity=.07).move_to(p(x,y)),label(s,x,y,size,color,width=w-.35))

def arrow(a,b,color=GREEN):
 return Arrow(a.get_bottom(),b.get_top(),buff=.12,color=color,stroke_width=2,max_tip_length_to_length_ratio=.16)

def vectors(y=.5,seed=2):
 rng=np.random.default_rng(seed)
 cells=VGroup(*[VGroup(RoundedRectangle(width=.64,height=.49,corner_radius=.06,stroke_width=1,color=PURPLE,fill_color=PURPLE,fill_opacity=.1+.5*abs(v)),text(f'{v:+.1f}',size=16,color=INK)) for v in rng.uniform(-1,1,24)])
 cells.arrange_in_grid(rows=4,cols=6,buff=.08).move_to(p(0,y))
 return cells

class IdeaTwoScene(IdeaScene):
 data=DATA

 def s01(self):
  formula=eq('2x+3=11',y=2.9,size=53);self.show(formula)
  step=card('양변에서 3을 뺍니다.',y=.8);self.show(step)
  self.to(5)
  new=eq('2x=8',y=2.9,size=53)
  self.play(TransformMatchingTex(formula,new),run_time=.8);formula=new
  self.play(Transform(step,card('양변을 2로 나눕니다.',y=.8)),run_time=.7)
  self.to(7)
  new=eq('x=4',y=2.9,size=53)
  self.play(TransformMatchingTex(formula,new),Transform(step,card('따라서 x = 4입니다.',y=.8)),run_time=.8)
  self.show(label('식 정리 → 규칙 적용 → 결과',y=-1.3,size=31,color=GREEN))
  self.to(10);self.clear_body()
  a=card('언어적 설명',y=2.4,color=BLUE);b=card('수학적 계산',y=-.3,color=GREEN)
  self.show(a,b);self.show(eq('?',y=1.0,size=64,color=ORANGE))
  self.to(13);self.show(label('언어가 반드시 필요할까?',y=-2.4,size=37,color=ORANGE))

 def s02(self):
  title=label('미분',y=3.8,size=43,color=BLUE);self.show(title)
  axes=Axes(x_range=[-2,2,1],y_range=[0,4,1],x_length=6.2,y_length=3,tips=False,axis_config={'color':MUTED,'stroke_width':1.2}).move_to(p(0,.4))
  curve=axes.plot(lambda x:x*x,color=BLUE)
  a=ValueTracker(-1.3)
  point=always_redraw(lambda:Dot(axes.c2p(a.get_value(),a.get_value()**2),color=ORANGE,radius=.09))
  tangent=always_redraw(lambda:Line(axes.c2p(a.get_value()-.5,a.get_value()**2-a.get_value()),axes.c2p(a.get_value()+.5,a.get_value()**2+a.get_value()),color=GREEN,stroke_width=3))
  self.to(20);self.play(Create(axes),Create(curve),run_time=.7);self.add(point,tangent)
  self.play(a.animate.set_value(1.2),run_time=2,rate_func=linear)
  self.show(label('순간변화율',y=-2.0,size=31,color=GREEN))
  self.to(24);point.clear_updaters();tangent.clear_updaters();self.clear_body()
  rules=VGroup(eq(r'D(af+bg)=aDf+bDg',y=3,size=36,color=GREEN),eq(r'D(fg)=fDg+gDf',y=.9,size=36,color=BLUE),eq(r'D(f\circ g)=(Df\circ g)\,Dg',y=-1.2,size=33,color=PURPLE))
  labels=VGroup(*[label(s,y=y,size=23,color=MUTED) for s,y in [('선형성 · 상수 a, b',2.25),('곱의 미분법',.15),('연쇄 법칙',-1.95)]])
  self.show(rules,labels)
  for r in rules:self.play(Indicate(r,color=ORANGE),run_time=.6)
  self.note('충분히 미분 가능한 함수 · 상수 a, b')
  self.to(30);self.clear_body()
  top=card('정의를 말로 설명하기',y=2.4,color=BLUE)
  bottom=card('새로운 문제에 성질 활용하기',y=-.5,color=GREEN)
  self.show(top,bottom);self.play(GrowArrow(arrow(top,bottom)),run_time=.6)
  self.show(eq('?',x=1,y=1,size=54,color=ORANGE),label('활용 능력도 확인해야 한다',y=-2.6,size=33,color=ORANGE))

 def s03(self):
  cards=VGroup(*[card(s,y=y,w=4.4,color=c) for s,y,c in [('정의',3,BLUE),('공식',1.6,GREEN),('예제',.2,PURPLE)]])
  self.play(LaggedStart(*[FadeIn(c) for c in cards],lag_ratio=.15),run_time=1)
  self.to(41)
  target=card('새로운 문제',y=-2,w=4.4,color=ORANGE)
  self.show(target)
  self.play(GrowArrow(arrow(cards[-1],target,ORANGE)),run_time=.7)
  self.show(label('일반화할 수 있을까?',x=2.0,y=-.7,size=26,color=ORANGE,width=3.4))
  self.note('설명의 정확성과 관계의 활용을 함께 평가')

 def s04(self):
  self.show(label('GSM-Symbolic · 2024',y=4.0,size=31,color=BLUE))
  a=card('사과 12개 + 8개',y=2.3,w=6.2,color=BLUE)
  b=card('사과 14개 + 6개',y=.5,w=6.2,color=ORANGE)
  self.show(a);self.play(TransformFromCopy(a,b),run_time=.8)
  self.show(label('숫자 변경 · 같은 덧셈 풀이 구조',y=-.6,size=28,color=GREEN))
  self.to(55)
  extra=card('풀이에 필요 없는 정보 추가',y=-1.7,h=.9,color=ORANGE,size=25)
  self.show(extra)
  self.to(58);self.show(label('정답률 변화 관찰',y=-2.8,size=32,color=ORANGE))
  self.note('arXiv:2410.05229 · 문제는 개념 예시, 실제 측정값 아님')

 def s05(self):
  problem=eq('247+386',y=3.9,size=44);self.show(problem)
  v=vectors(y=2.15);self.show(v)
  self.show(label('모델 내부 표현',y=.7,size=25,color=PURPLE))
  out=card('모델 출력: 오답',x=-1.95,y=-1.0,w=3.45,h=1.1,color=ORANGE,size=24)
  probe=card('별도 학습 분석기',x=1.95,y=-1.0,w=3.45,h=1.1,color=GREEN,size=23)
  self.show(out);self.play(GrowArrow(arrow(v,out,ORANGE)),run_time=.6)
  self.to(65);self.show(probe)
  self.play(GrowArrow(arrow(v,probe,GREEN)),run_time=.6)
  result=label('정답 관련 정보',x=1.95,y=-2.5,size=25,color=GREEN,width=3.5)
  self.show(result)
  self.note('Sun et al. · EMNLP 2025 · 247 + 386은 개념 예시')
  self.to(70)
  self.play(Indicate(out,color=ORANGE),Indicate(result,color=GREEN),run_time=.9)
  self.show(label('출력된 답',x=-1.95,y=-2.5,size=25,color=ORANGE,width=3.4),eq(r'\neq',y=-2.5,size=32,color=ORANGE))
  self.to(73)
  self.note('정답 정보의 검출 ≠ 완성된 정답 저장 또는 항상 복원')

 def s06(self):
  a=card('우리가 읽는 설명',y=3.2,color=BLUE)
  b=vectors(y=.4);self.show(a,b,label('내부의 벡터 계산',y=-1.3,size=28,color=PURPLE))
  self.to(80);self.show(label('얼마나 일치할까?',y=-2.8,size=35,color=ORANGE))
  self.to(85);self.clear_body()
  tokens=VGroup(*[card(s,w=w,h=.75,size=23) for s,w in [('미분',1.0),('은',.7),('변화율',1.4),('을',.7),('구한다',1.4)]]).arrange(RIGHT,buff=.12).move_to(p(0,3.5))
  v=vectors(y=1.3,seed=3);self.show(tokens,v)
  self.play(Transform(v,vectors(y=1.3,seed=7)),run_time=1)
  candidates=VGroup(*[card(s,x=x,y=-1.2,w=1.9,h=h,color=BLUE,size=22) for s,x,h in [('후보 A',-2.2,.6),('후보 B',0,1.2),('후보 C',2.2,.8)]])
  self.show(candidates)
  self.note('단어 분리·벡터 값·출력 후보는 개념도')
  self.to(91);self.play(Indicate(candidates[1],color=BLUE),run_time=.8)
  self.show(label('문장 ≠ 내부 모든 연산의 기록',y=-2.8,size=30,color=ORANGE))
  self.to(96);self.clear_body()
  context=card('중간 설명 토큰',y=2.7,color=BLUE)
  next_context=card('다음 단계의 입력 문맥',y=.5,color=PURPLE)
  output=card('후속 계산과 출력',y=-1.7,color=GREEN)
  self.show(context,next_context,output)
  self.play(GrowArrow(arrow(context,next_context)),GrowArrow(arrow(next_context,output)),run_time=.8)
  self.to(101);self.clear_body()
  self.show(card('언어가 도움이 되는가?',y=2,color=BLUE),card('언어가 반드시 필요한가?',y=-.4,color=GREEN))
  self.show(label('서로 다른 질문',y=-2.7,size=34,color=ORANGE))

 def s07(self):
  self.note('IDEA / CONCEPT · 가능한 학습 방식에 대한 사고 실험',GREEN)
  start=eq(r'f,\ g',y=3.8,size=46);self.show(start)
  left=eq('f+g',x=-1.95,y=2,size=34,width=3.4)
  right=eq(r'Df,\ Dg',x=1.95,y=2,size=34,width=3.4)
  self.show(left,right)
  self.play(GrowArrow(arrow(start,left)),GrowArrow(arrow(start,right)),run_time=.6)
  self.show(label('먼저 더하기',x=-1.95,y=1.15,size=24,color=BLUE,width=3.4),label('먼저 미분',x=1.95,y=1.15,size=24,color=GREEN,width=3.4))
  self.to(112)
  l=eq('D(f+g)',x=-1.95,y=-.3,size=35,width=3.4,color=BLUE)
  r=eq('Df+Dg',x=1.95,y=-.3,size=35,width=3.4,color=GREEN)
  self.show(l,r);self.play(GrowArrow(Arrow(p(-1.95,.65),l.get_top(),buff=.1,color=GREEN)),GrowArrow(Arrow(p(1.95,.65),r.get_top(),buff=.1,color=GREEN)),run_time=.6)
  self.to(115)
  rule=eq('D(f+g)=Df+Dg',y=-2.3,size=39,color=GREEN)
  self.show(rule)
  self.to(117);self.clear_body()
  self.note('IDEA / CONCEPT · 사례에서의 패턴과 일반적 증명은 다르다',GREEN)
  examples=VGroup(eq('D(x^2+x)=2x+1',y=3.4,size=31,color=BLUE),eq('D(x^3+x^2)=3x^2+2x',y=2.0,size=31,color=PURPLE),eq(r'D(\sin x+x)=\cos x+1',y=.6,size=31,color=GREEN))
  self.show(examples,run_time=.7)
  self.to(119)
  self.play(ReplacementTransform(examples,eq('D(f+g)=Df+Dg',y=2.5,size=40,color=GREEN)),run_time=.6)
  fresh=eq(r'D(e^x+\cos x)',y=.1,size=38,color=BLUE);self.show(fresh,run_time=.4)
  self.to(121)
  new=eq(r'D(e^x)+D(\cos x)',y=.1,size=38,color=GREEN)
  self.play(TransformMatchingTex(fresh,new),run_time=.6)
  self.to(122)
  self.show(eq(r'e^x-\sin x',y=-1.8,size=41,color=GREEN),run_time=.5)
  self.to(123)
  self.show(label('미분의 선형성 · 덧셈 보존',y=-2.9,size=26,color=ORANGE),run_time=.4)

 def s08(self):
  a=card('언어를 통한 표현',y=2.7,color=BLUE)
  b=card('관계를 통한 표현',y=.3,color=GREEN)
  self.show(a,b,eq('?',y=-1.6,size=62,color=ORANGE))
  self.note('어느 쪽이 더 유리한지는 별도로 검증해야 한다')
  self.to(129);self.play(Indicate(a,color=BLUE),run_time=.8)
  self.to(134);self.clear_body()
  f=eq('D(f+g)=Df+Dg',y=2.8,size=42,color=GREEN)
  sentence=card('합을 미분한 결과는\n각각 미분한 결과의 합과 같다',y=-.5,h=1.8,color=BLUE,size=27)
  self.show(f,sentence)
  self.play(GrowArrow(DoubleArrow(f.get_bottom(),sentence.get_top(),buff=.3,color=GREEN)),run_time=.8)
  self.show(label('수학적 관계 처리 ↔ 사람에게 전달',y=-2.8,size=29))

 def s09(self):
  g=relation_graph(y=.7,scale=.8)
  self.show(g)
  window=RoundedRectangle(width=3.0,height=2.8,corner_radius=.12,color=BLUE,stroke_width=3,fill_color=BLUE,fill_opacity=.06).move_to(p(0,.7))
  self.play(Create(window),run_time=.7)
  self.show(label('언어적 설명이라는 하나의 창',y=3.5,size=32,color=BLUE))
  self.note('관찰 가능한 출력과 내부 계산을 구별하는 비유')
  self.to(147);self.clear_body()
  self.show(card('설명의 정확성',y=2.9,color=BLUE),card('관계의 일반화',y=.9,color=GREEN))
  self.show(eq('+',y=1.9,size=40,color=INK))
  self.to(151)
  formula=eq('D(f+g)=Df+Dg',y=-1.0,size=36,color=GREEN);self.show(formula)
  self.to(155)
  alternate=eq(r'\frac{d}{dx}[u(x)+v(x)]=u^{\prime}(x)+v^{\prime}(x)',y=-1.0,size=30,color=GREEN)
  self.play(TransformMatchingTex(formula,alternate),run_time=.8)
  self.show(label('표현이 달라도, 같은 관계를 활용할까?',y=-2.8,size=30,color=ORANGE))
