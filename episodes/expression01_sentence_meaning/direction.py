"""Revised 168-second episode: context, Bayesian models and uncertainty."""
from .visuals import *
from .probability_model import LABELS,PRIOR,POSTERIOR,UNIFORM,entropy,interpolate,validate

def mathline(s,short,long,size=38,color=INK,width=7.2):
 o=MathTex(s,font_size=size*1.35,color=color)
 if o.width>width:o.scale_to_fit_width(width)
 return o.move_to(at(short,long))

def opinion_sentence():
 return card('이번에는 괜찮네.',(0,3.5),(0,1.85),w=6.8 if PORTRAIT else 8.5,h=1.1,color=BLUE,size=34)

class ProbabilityBars(VGroup):
 """Interpolate one probability vector; percentages and H use the same vector."""
 def __init__(self,labels,values,center,width=6.4,height=2.7):
  super().__init__();self.initial=validate(values);self.target=self.initial.copy();self.mix=ValueTracker(0)
  self.base=center[1]-height/2;self.unit=height;self.xs=np.linspace(center[0]-width*.375,center[0]+width*.375,len(labels));self.bar_width=width/len(labels)*.48
  self.rects=[];self.numbers=[]
  self.add(Line(pt(center[0]-width/2,self.base),pt(center[0]+width/2,self.base),color=MUTED,stroke_width=1.5))
  for i,(name,x) in enumerate(zip(labels,self.xs)):
   color=GREEN if i==0 else AMBER
   r=Rectangle(width=self.bar_width,height=.1,stroke_width=0,fill_color=color,fill_opacity=.85)
   n=DecimalNumber(100*self.initial[i],num_decimal_places=0,unit=r"\%",font_size=23,color=color)
   caption=text(name,x=x,y=self.base-.4,size=23,color=INK,width=width/len(labels)*.94)
   self.rects.append(r);self.numbers.append(n);self.add(r,n,caption)
  self.refresh();self.add_updater(lambda mob,dt:mob.refresh())
 def probs(self):return interpolate(self.initial,self.target,float(np.clip(self.mix.get_value(),0,1)))
 def refresh(self):
  for x,r,n,v in zip(self.xs,self.rects,self.numbers,self.probs()):
   h=max(.008,self.unit*v);r.stretch_to_fit_height(h).move_to(pt(x,self.base+h/2));n.set_value(v*100).move_to(pt(x,self.base+h+.25))
  return self
 def prepare(self,target):
  self.initial=self.probs().copy();self.target=validate(target);self.mix.set_value(0);return self.mix

class ExpressionScene(BaseExpressionScene):
 data=DATA

 def s01(self):
  bubble=utterance()
  self.play(Create(bubble[0]),run_time=.7)
  self.to(3);self.play(Write(bubble[1]),run_time=.8)
  self.to(4)
  lines=VGroup(*[Underline(w,color=AMBER,buff=.12) for w in bubble[1][:2]])
  self.play(Create(lines),run_time=.6)
  a=card('그거 → 무엇?',(0,1.1),(3.7,1.0),w=4.7,color=AMBER)
  b=card('거기 → 어디?',(0,-.5),(3.7,-.7),w=4.7,color=AMBER)
  self.show(a,b)

 def s02(self):
  bubble=utterance();self.add(bubble)
  bx,by=(-2.1,-.3) if PORTRAIT else (1.5,.35)
  dx,dy=(1.4,-.8) if PORTRAIT else (4.65,-.2)
  obj=book(pt(bx,by));table=desk(dx,dy)
  self.show(obj,table)
  hand=Arrow(pt(bx-.7,by+1.4),pt(bx,by+.45),color=GREEN,buff=.1)
  gaze=Arrow(pt(dx+1.0,dy+1.8),pt(dx,dy+.2),color=GREEN,buff=.1)
  self.play(GrowArrow(hand),GrowArrow(gaze),run_time=.7)
  self.show(say('손짓과 주변 상황',(-.1,1.6),(3.2,1.85),size=26,color=GREEN))
  self.to(13)
  destination=pt(dx,dy+.5)
  self.play(MoveAlongPath(obj,ArcBetweenPoints(obj.get_center(),destination,angle=-.7)),FadeOut(hand),FadeOut(gaze),run_time=1.1)
  self.show(say('그거 → 책     거기 → 책상',(0,-3.25),(-4.1,-.6),size=29,color=GREEN,width=6.4))

 def s03(self):
  u=utterance();self.add(u)
  term=card('직시 · Deixis',(0,1.2),(3.8,1),w=4.7,color=GREEN,size=34);self.show(term)
  self.play(*[Indicate(w,color=AMBER) for w in u[1][:2]],run_time=.9)
  self.show(say('상황에 따라 가리키는 대상이 달라진다',(0,-.4),(3.6,-.35),size=28,color=GREEN,width=7 if PORTRAIT else 6.5))
  self.to(22);self.clear_body();self.add(utterance())
  self.show(card('책 · 책상',(0,.5),(3.7,.6),w=4.8,color=GREEN,size=32))
  self.show(say('이 단어들은 문장에 없다',(0,-1.2),(3.7,-.7),size=29,color=AMBER,width=6.5))
  self.to(27);self.show(say('어디에서 가져온 정보일까?',(0,-2.8),(0,-1.9),size=33,color=AMBER))

 def s04(self):
  self.add(utterance())
  clues=VGroup(*[card(s,w=1.6 if PORTRAIT else 2.6,h=.7,color=GREEN,size=23) for s in ['손짓','시선','상황','경험']])
  clues.arrange_in_grid(rows=1 if PORTRAIT else 2,cols=4 if PORTRAIT else 2,buff=.2).move_to(at((0,.5),(3.4,.6)))
  self.show(clues);self.play(LaggedStart(*[Indicate(c,color=GREEN) for c in clues],lag_ratio=.15),run_time=1.6)
  self.to(37);self.clear_body();self.add(utterance())
  chart=ProbabilityBars(LABELS,PRIOR,at((0,.2),(3.5,.0)),width=6.5,height=2.6)
  self.show(chart)
  self.show(say('가능한 지시 대상 · 상대적 확률(%)',(0,2.0),(3.5,1.95),size=25,color=AMBER,width=7))
  self.note('설명용 가상분포 · 실제 인간의 측정 데이터가 아님')

 def s05(self):
  self.add(utterance())
  chart=ProbabilityBars(LABELS,PRIOR,at((0,.2),(3.5,0)),width=6.5,height=2.6);self.add(chart)
  cue=card('책을 가리키는 손짓',(0,2.1),(-4.1,-.4),w=5.3,h=.8,color=GREEN,size=26);self.show(cue)
  self.note('설명용 가상분포 · 확률 막대와 표시는 같은 분포에 연동')
  tracker=chart.prepare(POSTERIOR)
  self.play(tracker.animate.set_value(1),run_time=3.0,rate_func=smooth)
  self.to(47)
  self.show(mathline(r'P(M\mid S,C)',(0,-2.5),(-4.1,-1.4),size=40,color=GREEN))
  self.show(say('베이즈 추론',(0,-3.25),(3.5,1.95),size=29,color=GREEN))
  self.note('M: 대상 후보 · S: 문장 · C: 문맥 / 수치는 개념 예시')

 def s06(self):
  self.show(say('같은 말도 다르게 들릴 수 있다',(0,3.0),(0,1.85),size=34,color=AMBER))
  self.to(54)
  a=person(at((-2.4,.3),(-4,.0)));b=person(at((2.4,.3),(4,.0)))
  plate=VGroup(Ellipse(width=2.6,height=1.0,color=GREEN),Ellipse(width=1.9,height=.6,color=GREEN),Circle(radius=.18,color=GREEN).shift(LEFT*.45),Circle(radius=.22,color=GREEN).shift(RIGHT*.3)).move_to(at((0,-.5),(0,-.2)))
  self.show(a,b);self.to(58);self.play(Create(plate),run_time=.8)
  self.to(62);self.show(say('음식을 맛본 친구의 한마디',(0,-2.2),(0,-1.6),size=29,color=BLUE))
  self.to(65);self.clear_body();self.show(opinion_sentence(),run_time=.6)

 def s07(self):
  phrase=opinion_sentence();self.add(phrase)
  left=card('전보다 맛있어졌어!',(-1.95,.8),(-3.8,.2),w=3.55 if PORTRAIT else 5.8,h=1.2,color=GREEN,size=25)
  right=card('전에는 별로였다는 건가?',(1.95,.8),(3.8,.2),w=3.55 if PORTRAIT else 5.8,h=1.2,color=AMBER,size=23)
  self.show(left)
  self.play(GrowArrow(Arrow(phrase.get_bottom(),left.get_top(),buff=.18,color=GREEN)),run_time=.6)
  self.to(70);self.show(right)
  self.play(GrowArrow(Arrow(phrase.get_bottom(),right.get_top(),buff=.18,color=AMBER)),run_time=.6)
  self.to(76)
  influences=VGroup(*[card(s,w=1.5 if PORTRAIT else 2.2,h=.75,color=GREEN,size=22) for s in ['관계','경험','기대','감정']]).arrange(RIGHT,buff=.2).move_to(at((0,-2.1),(0,-1.65)))
  self.show(influences)
  self.note('같은 발언에 대한 두 해석의 가능성 · 실제 의도는 별도 확인')

 def s08(self):
  self.add(opinion_sentence())
  centers=[at((-1.95,.5),(-3.8,0)),at((1.95,.5),(3.8,0))]
  a=ProbabilityBars(['칭찬','비꼼','중립'],[.7,.1,.2],centers[0],width=3.3 if PORTRAIT else 5.8,height=2.1)
  b=ProbabilityBars(['칭찬','비꼼','중립'],[.2,.6,.2],centers[1],width=3.3 if PORTRAIT else 5.8,height=2.1)
  self.show(a,b)
  self.show(say('사전 정보 A',(-1.95,2.1),(-3.8,1.08),size=25,color=GREEN,width=3.5),say('사전 정보 B',(1.95,2.1),(3.8,1.08),size=25,color=GREEN,width=3.5))
  self.note('가상의 상대적 가능성 · 개인의 기억과 사전확률은 일대일 대응 아님')
  self.to(90);self.show(say('공유된 의미와 규칙도 존재한다',(0,-2.5),(0,-1.8),size=30,color=BLUE))

 def s09(self):
  self.add(opinion_sentence())
  candidates=VGroup(*[card(s,w=3.2 if PORTRAIT else 4.5,h=.9,color=c,size=25) for s,c in [('칭찬',GREEN),('마지못한 인정',GREEN),('비꼼',GREEN),('내일 비가 온다',AMBER)]])
  candidates.arrange_in_grid(rows=2,cols=2,buff=(.4,.6)).move_to(at((0,.3),(0,-.2)))
  self.show(candidates);self.play(FadeOut(candidates[3]),run_time=.7)
  self.note('이 대화 상황에서 언어 규칙과 관습이 해석을 제한한다')
  self.to(100);self.clear_body()
  self.show(card('문맥은 무엇을 변화시킬까?',(0,1),(0,.4),w=7.2,h=1.4,color=AMBER,size=33))

 def s10(self):
  self.show(mathline(r'H(M)=-\sum_i p_i\log_2p_i',(0,3.7),(-4.0,1.0),size=34,color=BLUE,width=7.5))
  chart=ProbabilityBars(LABELS,UNIFORM,at((0,.7),(3.5,.0)),width=6.4,height=2.7);self.show(chart)
  entropy_label=say('불확실성 H',(0,-1.65),(-4.0,-.2),size=28,color=INK)
  number=DecimalNumber(entropy(UNIFORM),num_decimal_places=2,font_size=42,color=GREEN).move_to(at((-.35,-2.55),(-4.4,-1.25)))
  number.add_updater(lambda m:m.set_value(entropy(chart.probs())))
  unit=say('bit',(1.2,-2.55),(-2.9,-1.25),size=25,color=GREEN)
  self.show(entropy_label,number,unit)
  self.note('같은 4개 후보 · 설명용 가상분포 / 균등할 때 H = 2 bit')
  self.to(109)
  tracker=chart.prepare(POSTERIOR);self.play(tracker.animate.set_value(1),run_time=4,rate_func=smooth)
  self.to(115)
  self.note('선택한 사례 · 문맥이 항상 불확실성을 줄이는 것은 아님')

 def s11(self):
  self.show(say('표현의 길이와 정보의 유용성',(0,3.5),(0,1.95),size=32,color=BLUE))
  long_text=card('방 안에는 여러 물건이 있고,\n책상 위에는 공간이 있어.\n물건을 옮기고 싶어.',(-1.9,.7),(-3.8,.3),w=3.6 if PORTRAIT else 6.0,h=2.3,color=BLUE,size=23)
  pointer=card('책을 가리키는 손짓',(1.9,.7),(3.8,.3),w=3.6 if PORTRAIT else 6.0,h=2.3,color=GREEN,size=23)
  self.show(long_text,pointer)
  self.to(125)
  self.play(Indicate(pointer,color=GREEN),run_time=.8)
  self.show(say('여러 후보가 남음',(-1.9,-1.4),(-3.8,-1.3),size=24,color=AMBER,width=3.7 if PORTRAIT else 6),say('대상을 특정하는 단서',(1.9,-1.4),(3.8,-1.3),size=24,color=GREEN,width=3.7 if PORTRAIT else 6))
  self.to(131)
  self.show(say('어떤 질문의 불확실성을 줄이는가?',(0,-2.75),(0,-1.9),size=30,color=AMBER))
  self.note('길이·문자 수와 정보이론의 정보량은 같은 개념이 아니다')

 def s12(self):
  sentence=card('짧은 표현',(0,3.0),(-4.2,.8),w=5,color=BLUE,size=31)
  context=card('문맥 · 공유된 정보',(0,.8),(4.2,.8),w=5,color=GREEN,size=29)
  self.show(sentence,context)
  self.to(141)
  self.show(say('+',(0,1.9),(0,.8),size=38))
  meaning=card('구체적인 의미',(0,-1.5),(0,-1.0),w=4.5,color=INK,size=30);self.show(meaning)
  if PORTRAIT:self.play(GrowArrow(Arrow(context.get_bottom(),meaning.get_top(),buff=.15,color=GREEN)),run_time=.6)
  else:self.play(GrowArrow(Arrow(sentence.get_bottom(),meaning.get_left(),buff=.15,color=BLUE)),GrowArrow(Arrow(context.get_bottom(),meaning.get_right(),buff=.15,color=GREEN)),run_time=.6)
  self.to(146)
  self.show(say('공유된 정보가 다르면, 해석도 달라질 수 있다',(0,-3),(0,-2.05),size=29,color=AMBER))

 def s13(self):
  natural=card('조금 더 빠르게 움직인다.',(0,3.2),(-4.1,1),w=7 if PORTRAIT else 6.6,color=BLUE,size=30);self.show(natural)
  formula=mathline(r'v_2=v_1+\Delta v',(0,1.0),(3.5,1.0),size=47,color=AMBER);self.show(formula)
  self.show(say('변수는 무엇을 뜻할까?',(0,-.5),(3.5,-.2),size=29,color=AMBER,width=7))
  self.to(155)
  self.show(say('v₁: 변화 전 속력   v₂: 변화 후 속력\nΔv: 속력 증가량 · 단위 m/s · Δv > 0',(0,-1.9),(0,-1.55),size=25,color=GREEN,width=7.3 if PORTRAIT else 13))
  self.note('기호와 정의로 조건을 명시한다 · ‘조금’의 크기는 여전히 미정')

 def s14(self):
  self.show(mathline('x+y',(0,3.4),(0,1.75),size=58,color=BLUE))
  a=card('실수의 덧셈',(-1.95,1.6),(-3.8,.7),w=3.5 if PORTRAIT else 5.8,h=.8,color=GREEN,size=25)
  b=card('벡터의 덧셈',(1.95,1.6),(3.8,.7),w=3.5 if PORTRAIT else 5.8,h=.8,color=GREEN,size=25)
  self.show(a,b)
  self.show(mathline('2+3=5',(-1.95,-.1),(-3.8,-.5),size=34,width=3.5 if PORTRAIT else 5.8),mathline('(1,0)+(0,1)=(1,1)',(1.95,-.1),(3.8,-.5),size=28,width=3.5 if PORTRAIT else 5.8))
  self.to(165)
  self.show(say('같은 기호가 언제나 같은 의미일까?',(0,-2.7),(0,-1.9),size=33,color=AMBER))
