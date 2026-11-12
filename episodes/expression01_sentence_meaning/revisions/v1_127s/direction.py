"""One animation logic with native portrait and landscape compositions."""
import json
from pathlib import Path
import numpy as np
from manim import *
from longforms.qcs01_speed.direction import QCSScene,PORTRAIT,L
from quantum_series.shared.theme import text

HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
BG,BLUE,GREEN,AMBER,INK,MUTED='#0B1020','#60A5FA','#34D399','#FBBF24','#E5E7EB','#8D9BB6'
config.background_color=BG

def pt(x,y):return np.array([x,y,0.])
def at(short,long):return pt(*(short if PORTRAIT else long))
def say(s,short=(0,0),long=(0,0),size=30,color=INK,width=None):
 x,y=(short if PORTRAIT else long)
 return text(s,x=x,y=y,size=size,color=color,width=width or (7.5 if PORTRAIT else 13.8))

def card(s,short=(0,0),long=(0,0),w=5,h=1,color=BLUE,size=27):
 center=at(short,long)
 return VGroup(RoundedRectangle(width=w,height=h,corner_radius=.15,color=color,fill_color=color,fill_opacity=.07).move_to(center),text(s,*center[:2],size,color,w-.3))

def utterance():
 words=VGroup(*[text(s,size=37 if PORTRAIT else 32,color=BLUE) for s in ['그거','거기','놓아줘.']]).arrange(RIGHT,buff=.3)
 words.move_to(at((0,3.5),(-4.1,1.1)))
 rect=RoundedRectangle(width=7.3 if PORTRAIT else 6.2,height=1.25 if PORTRAIT else 1.1,corner_radius=.2,color=BLUE,fill_color=BLUE,fill_opacity=.06).move_to(words)
 return VGroup(rect,words)

def place_sentence():
 return card('우리 지난번에 갔던 곳으로 가자.',(0,3.5),(0,1.85),w=7.5 if PORTRAIT else 10,h=1.1,color=BLUE,size=30)

def book(center,color=GREEN):
 x,y=center[:2]
 return VGroup(RoundedRectangle(width=1.1,height=.78,corner_radius=.06,color=color,fill_color=color,fill_opacity=.2).move_to(center),Line(pt(x-.35,y-.35),pt(x-.35,y+.35),color=color),text('책',x=x+.1,y=y,size=22,color=color))

def desk(x,y):
 return VGroup(Rectangle(width=2.8,height=.18,color=GREEN,fill_color=GREEN,fill_opacity=.25).move_to(pt(x,y)),Line(pt(x-1.1,y-.1),pt(x-1.1,y-1.12),color=GREEN),Line(pt(x+1.1,y-.1),pt(x+1.1,y-1.12),color=GREEN),text('책상',x=x,y=y-1.45,size=23,color=GREEN))

def person(center,color=GREEN):
 x,y=center[:2]
 return VGroup(Circle(radius=.23,color=color).move_to(pt(x,y+.38)),Arc(radius=.48,start_angle=0,angle=PI,color=color).move_to(pt(x,y-.2)),Line(pt(x-.47,y-.2),pt(x+.47,y-.2),color=color))

def location(name,center,color=GREEN,scale=1):
 x,y=center[:2]
 roof=Polygon(pt(-.65,.3),pt(0,.85),pt(.65,.3),color=color)
 base=Rectangle(width=1.05,height=.8,color=color).move_to(pt(0,-.1))
 door=Rectangle(width=.25,height=.45,color=color).move_to(pt(0,-.27))
 icon=VGroup(roof,base,door).scale(scale).move_to(center)
 lab=text(name,x=x,y=y-.85*scale-.18,size=24,color=color)
 return VGroup(icon,lab)

def network(center,seed=1,scale=1,color=GREEN):
 rng=np.random.default_rng(seed)
 xy=rng.uniform([-2,-1.3],[2,1.3],size=(12,2))*scale
 dots=VGroup(*[Dot(center+pt(x,y),radius=.055,color=color) for x,y in xy])
 edges=VGroup(*[Line(dots[i].get_center(),dots[(i+1)%12].get_center(),color=color,stroke_width=1.1,stroke_opacity=.45) for i in range(12)],*[Line(dots[i].get_center(),dots[(i+4)%12].get_center(),color=color,stroke_width=1,stroke_opacity=.25) for i in range(0,12,2)])
 return VGroup(edges,dots)

def connect(a,b,color=GREEN,buff=.18):
 return Arrow(a.get_center(),b.get_center(),buff=buff,color=color,stroke_width=2,max_tip_length_to_length_ratio=.13).set_z_index(-1)

class ExpressionScene(QCSScene):
 data=DATA
 def replace(self,old,new):return Scene.replace(self,old,new)
 def setup(self):
  super().setup()
  old=self.mobjects[0];self.remove(old)
  self.brand=text('과학 한조각  /  표현은 무엇을 전달하는가?',y=L.brand_y,size=17,color=MUTED,width=7.6 if PORTRAIT else 14)
  self.add(self.brand)
  self.body_checks=[]

 def clear_body(self):
  keep=[self.title,self.caption,self.caption_panel,self.brand]
  objects=[o for o in self.mobjects if all(o is not k for k in keep) and o.get_center()[1]<(6.5 if PORTRAIT else 3.6)]
  if objects:self.play(*[FadeOut(o) for o in objects],run_time=.4)

 def check_body(self):
  for o in self.mobjects:
   if o is self.caption or o is self.caption_panel:continue
   if not o.width or not o.height:continue
   assert o.get_left()[0]>=-config.frame_width/2+.12 and o.get_right()[0]<=config.frame_width/2-.12,(self.info['id'],'horizontal',o)
   assert o.get_bottom()[1]>=(-4.9 if PORTRAIT else -2.6),(self.info['id'],'subtitle overlap',o)

 def play(self,*args,**kwargs):
  result=super().play(*args,**kwargs)
  self.check_body()
  return result

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
  bubble=utterance();self.add(bubble)
  self.show(say('문장 안',(-2.8,4.5),(-4.1,2.1),size=23,color=BLUE))
  self.to(19)
  ext=card('책 · 책상',(0,.7),(3.6,.8),w=5,color=GREEN,size=34)
  self.show(ext)
  notice=say('이 단어들은 문장에 없다',(0,-.5),(3.6,-.4),size=28,color=AMBER,width=6.5)
  self.show(notice)
  self.to(24)
  self.play(FadeOut(notice),run_time=.3)
  interpretation=card('구체적인 해석',(0,-2.1),(0,-1.6),w=4.6,h=.85,color=GREEN)
  self.show(interpretation)
  source=bubble.get_left()+DOWN*.6 if PORTRAIT else bubble.get_bottom()
  self.play(GrowArrow(Arrow(source,interpretation.get_left(),buff=.15,color=BLUE).set_z_index(-2)),GrowArrow(Arrow(ext.get_bottom(),interpretation.get_top(),buff=.15,color=GREEN).set_z_index(-2)),run_time=.6)

 def s04(self):
  center=card('해석',(0,.5),(0,.1),w=1.9,h=1,color=INK,size=32)
  self.show(center)
  sentence=card('문장',(0,3.3),(0,1.8),w=2.5,color=BLUE)
  self.show(sentence)
  self.play(GrowArrow(Arrow(sentence.get_bottom(),center.get_top(),buff=.14,color=BLUE)),run_time=.5)
  self.to(31)
  short=[(-2.65,1.6),(2.65,1.6),(-2.65,-1.6),(2.65,-1.6)]
  wide=[(-4.8,1.0),(4.8,1.0),(-4.8,-1.2),(4.8,-1.2)]
  nodes=VGroup(*[card(s,a,b,w=2.6,h=.9,color=GREEN,size=24) for s,a,b in zip(['손짓','시선','주변 상황','공유 경험'],short,wide)])
  for o in nodes:
   self.show(o,run_time=.35);self.play(GrowArrow(connect(o,center,buff=.75)),run_time=.35)
  self.play(Indicate(center,color=GREEN),run_time=.8)

 def s05(self):
  people=VGroup(person(at((-1,1.7),(-1.2,.6))),person(at((1,1.7),(1.2,.6))))
  self.show(people)
  self.to(40);self.play(Indicate(people[0],color=BLUE),run_time=.6)
  self.to(42);self.show(place_sentence(),run_time=.7)
  self.to(44)
  spots=VGroup(*[location(s,at((x,-.8),(x*1.6,-.7)),color=AMBER,scale=.8 if PORTRAIT else .65) for s,x in [('카페',-2.5),('식당',0),('공원',2.5)]])
  self.show(spots)
  self.note('장소 이름도 주소도, 문장에는 없다',AMBER)

 def s06(self):
  self.add(place_sentence())
  left,right=((-1.95,1.0),(1.95,1.0)) if PORTRAIT else ((-3.8,.4),(3.8,.4))
  a=card('공유한 장소 1개',left,left,w=3.4 if PORTRAIT else 5.4,h=.8,color=GREEN,size=24)
  b=card('공유한 장소 여러 개',right,right,w=3.4 if PORTRAIT else 5.4,h=.8,color=GREEN,size=23)
  self.show(a,b)
  single=location('카페',pt(left[0],-.9 if PORTRAIT else -.6),scale=.8 if PORTRAIT else .65)
  self.show(single);self.play(Circumscribe(single,color=GREEN),run_time=.8)
  self.to(53)
  names=['카페','식당','공원']
  if PORTRAIT:
   many=VGroup(*[card(s,(right[0],y),(0,0),w=2.7,h=.62,color=AMBER,size=22) for s,y in zip(names,[-.2,-1.12,-2.04])])
  else:
   many=VGroup(*[location(s,pt(x,-.6),color=AMBER,scale=.52) for s,x in zip(names,[2.0,3.8,5.6])])
  self.show(many)
  self.to(58)
  self.show(say('쉽게 특정',(-1.95,-3),(-3.8,-2.05),size=27,color=GREEN,width=3.5),say('추가 단서가 필요할 수도',(1.95,-3),(3.8,-2.05),size=24,color=AMBER,width=3.5 if PORTRAIT else 6))

 def s07(self):
  sentence=card('짧은 문장',(0,3.0),(-4.7,1.0),w=4.6,color=BLUE)
  context=card('상황 · 공유된 지식',(0,1.0),(-4.7,-.6),w=4.6,color=GREEN)
  result=card('구체적인 해석',(0,-1.5),(3.9,.2),w=4.6,color=GREEN)
  self.show(sentence,context)
  if PORTRAIT:self.show(say('+',(0,2),(0,0),size=36,color=INK),run_time=.3)
  self.to(69);self.show(result)
  if PORTRAIT:
   self.play(GrowArrow(Arrow(context.get_bottom(),result.get_top(),buff=.2,color=GREEN)),run_time=.6)
  else:
   self.play(GrowArrow(Arrow(sentence.get_right(),result.get_left(),buff=.2,color=BLUE)),GrowArrow(Arrow(context.get_right(),result.get_left(),buff=.2,color=GREEN)),run_time=.6)
  self.to(74);self.clear_body()
  blocks=VGroup(*[card(s,w=6.5 if PORTRAIT else 5.4,h=.58,color=GREEN,size=23) for s in ['지난주 토요일','우리가 함께 방문했던','공원 옆 카페에','다시 가고 싶어.']]).arrange(DOWN,buff=.15).move_to(at((0,1.5),(-4.2,.35)))
  self.show(blocks)
  self.note('정보 압축에 빗댄 설명 · 공유 정보를 활용한다')
  self.to(77)
  short=card('우리 지난번에 갔던 곳으로 가자.',(0,2.1),(-3.8,.7),w=7.4 if PORTRAIT else 6.6,h=1.0,color=BLUE,size=27)
  self.play(ReplacementTransform(blocks,short),run_time=.9)
  memory=card('공유된 경험',(0,-.1),(4.0,.7),w=4.6,color=GREEN)
  self.show(memory)
  self.show(say('짧은 표현 + 함께 알고 있는 정보',(0,-2.1),(0,-1.4),size=30,color=GREEN))

 def s08(self):
  u=utterance()
  if not PORTRAIT:u.move_to(pt(0,1.9))
  self.add(u)
  self.to(87)
  parts=VGroup(*[card(s,w=2.2 if PORTRAIT else 3.4,h=1.15,color=BLUE,size=30) for s in ['그거','거기','놓아줘']]).arrange(RIGHT,buff=.35 if PORTRAIT else .8).move_to(at((0,1),(0,.5)))
  self.play(TransformFromCopy(u[1],parts),run_time=.7)
  labels=VGroup(*[text(s,x=o.get_center()[0],y=o.get_bottom()[1]-.65,size=24,color=BLUE) for s,o in zip(['대상 지시','장소 지시','행동 요청'],parts)])
  self.show(labels)
  self.to(94)
  self.play(Indicate(parts[1],color=AMBER),run_time=.7)
  self.show(say('구체적으로 어디인지는 상황에 따라',(0,-2.4),(0,-1.5),size=29,color=AMBER))

 def s09(self):
  sentence=card('그거 거기 놓아줘.',(0,2.9),(-4.7,.8),w=5.4,color=BLUE,size=31)
  context=card('상황과 지식',(0,.8),(-4.7,-.7),w=4.5,color=GREEN)
  meaning=card('해석',(0,-1.5),(3.6,.2),w=3.2,color=GREEN)
  self.show(sentence,context,meaning)
  if PORTRAIT:self.show(say('+',(0,1.85),(0,0),size=36,color=INK),run_time=.3)
  if PORTRAIT:
   self.play(GrowArrow(Arrow(context.get_bottom(),meaning.get_top(),buff=.2,color=GREEN)),run_time=.6)
  else:
   self.play(GrowArrow(Arrow(sentence.get_right(),meaning.get_left(),buff=.2,color=BLUE)),GrowArrow(Arrow(context.get_right(),meaning.get_left(),buff=.2,color=GREEN)),run_time=.6)
  self.to(106);self.clear_body()
  u=card('그거 거기 놓아줘.',(0,1.2),(0,.2),w=5.8,h=1.0,color=BLUE,size=30).set_z_index(2)
  u[0].set_fill(BG,opacity=1)
  net=network(at((0,1.2),(0,.2)),scale=1.5 if PORTRAIT else 2.4)
  if not PORTRAIT:net.scale([1,.55,1])
  self.show(net,u)
  self.show(say('상황 · 지식 · 함께한 경험',(0,-2.4),(0,-2.0),size=30,color=GREEN))
  self.to(112);self.play(u.animate.scale(.78),net.animate.scale(1.12),run_time=1.8)

 def s10(self):
  phrase=card('같은 문장',(0,3.4),(0,1.9),w=4.8,color=BLUE,size=31)
  self.show(phrase)
  self.to(119)
  c1=at((-1.95,.0),(-3.9,.0));c2=at((1.95,.0),(3.9,.0))
  n1=network(c1,seed=2,scale=.7 if PORTRAIT else 1.15)
  n2=network(c2,seed=6,scale=.7 if PORTRAIT else 1.15)
  if not PORTRAIT:n1.scale([1,.62,1]);n2.scale([1,.62,1])
  self.show(n1,n2)
  self.play(GrowArrow(Arrow(phrase.get_bottom(),n1.get_top(),buff=.2,color=BLUE)),GrowArrow(Arrow(phrase.get_bottom(),n2.get_top(),buff=.2,color=BLUE)),run_time=.7)
  self.show(say('경험과 지식 A',(-1.95,-1.8),(-3.9,-1.3),size=24,color=GREEN,width=3.5),say('경험과 지식 B',(1.95,-1.8),(3.9,-1.3),size=24,color=GREEN,width=3.5))
  self.to(124)
  self.show(say('우리는 정말 같은 의미를 이해할까?',(0,-3.25),(0,-2.0),size=34 if PORTRAIT else 32,color=AMBER))
