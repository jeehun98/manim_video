"""Optogenetics: observing activity to testing its causal role."""
import json,sys
from pathlib import Path
import numpy as np
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.science02_gravitational_lensing.scene import txt,LIGHT,GAS
from episodes.science08_density_growth.scene import DensityGrowthDiscovery
BLUE='#62CFFF';GREEN='#78E6A6';GOLD='#FFD166';RED='#FF7B72';DIM='#40536C'

def label(s,x,y,size=28,color=LIGHT,width=7):
 return txt(s,y,size,color,width=width).move_to([x,y,0])

def neuron(x=0,y=0,color=GAS,scale=1):
 soma=Circle(radius=.4,color=color,fill_color=color,fill_opacity=.18)
 branches=VGroup(*[Line([-.3,.15,0],[-1.05,a,0],color=color,stroke_width=3) for a in (-.7,0,.7)],Line([.4,0,0],[1.5,0,0],color=color,stroke_width=4),*[Line([1.5,0,0],[1.9,a,0],color=color,stroke_width=3) for a in (-.4,.4)])
 return VGroup(soma,branches).scale(scale).move_to([x,y,0])

def circuit():
 pts=[[-2.7+(i%4)*1.8,2-(i//4)*1.5,0] for i in range(12)]
 edges=VGroup(*[Line(pts[i],pts[j],color=DIM,stroke_width=1.5) for i in range(12) for j in (i+1,i+4) if j<12])
 nodes=VGroup(*[neuron(p[0],p[1],GREEN if i%3==0 else GAS,.32) for i,p in enumerate(pts)])
 return VGroup(edges,nodes)

def channel(opened=False):
 membrane=VGroup(Line([-3,1,0],[-.5,1,0],color=GAS,stroke_width=8),Line([.5,1,0],[3,1,0],color=GAS,stroke_width=8),Line([-3,.6,0],[-.5,.6,0],color=GAS,stroke_width=8),Line([.5,.6,0],[3,.6,0],color=GAS,stroke_width=8))
 protein=VGroup(RoundedRectangle(width=.28,height=1.45,corner_radius=.1,color=GREEN).move_to([-.5,.8,0]),RoundedRectangle(width=.28,height=1.45,corner_radius=.1,color=GREEN).move_to([.5,.8,0]))
 gate=Line([-.4,.8,0],[.4,.8,0],color=RED,stroke_width=8).set_opacity(0 if opened else 1)
 return VGroup(membrane,protein,gate)

def algae():
 body=Ellipse(width=2.4,height=3.1,color=GREEN,fill_color=GREEN,fill_opacity=.12).move_to([0,.4,0])
 tails=VGroup(*[CubicBezier([x,1.8,0],[x-.8,2.5,0],[x+1,3.2,0],[x-.3,3.65,0],color=GREEN) for x in (-.4,.4)])
 return VGroup(body,tails,Dot([.65,.85,0],radius=.16,color=RED))

def bulb(x=0,y=0,color=GAS):
 return VGroup(Circle(radius=.18,color=color,fill_color=color,fill_opacity=.2).move_to([x,y,0]),Line([x-.1,y-.22,0],[x+.1,y-.22,0],color=color,stroke_width=3))

def bulbs():
 dots=VGroup(*[bulb(-2.8+(j%8)*.8,2.1-(j//8)*.75,GAS) for j in range(48)])
 wires=VGroup(*[Line(dots[j].get_center(),dots[j+1].get_center(),color=DIM,stroke_width=1) for j in range(47) if j%8<7])
 return VGroup(wires,dots)

def remote(x=-2.5,y=-1.5):
 box=RoundedRectangle(width=.9,height=1.4,corner_radius=.16,color=BLUE).move_to([x,y,0])
 return VGroup(box,Dot([x,y+.3,0],radius=.14,color=BLUE),label('ON',x,y-.3,18,BLUE))

def mouse(x=0,y=-2,color=LIGHT):
 return VGroup(Ellipse(width=1.25,height=.55,color=color).move_to([x,y,0]),Circle(radius=.16,color=color).move_to([x+.45,y+.27,0]),Dot([x+.55,y+.07,0],radius=.035,color=color),Arc(radius=.48,start_angle=0,angle=PI,color=color).move_to([x-.9,y,0]))

class OptogeneticsDiscovery(DensityGrowthDiscovery):
 TIMING=json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'));DURATION=TIMING['duration']
 def construct(self):
  self.brand=txt('과학의 한 장면  /  Nobel Medicine 01',7.1,21,'#9BA9C3');self.add(self.brand)
  titles=[
   ('뇌 속 수많은 전구가, 행동과 함께 켜진다','뉴런의 활동을 전구로 표현한 개념도입니다.'),
   ('켜져서 움직였을까, 움직여서 켜졌을까?','함께 나타나는 것만으로는\n원인의 방향을 알 수 없습니다.'),
   ('그렇다면, 원하는 전구를 직접 켜보면?','원하는 뉴런에 스위치를 달고\n행동이 바뀌는지 시험합니다.'),
   ('작은 뉴런에, 어떤 스위치를 달 수 있을까?','원하는 세포를 원하는 순간에\n자극할 방법이 필요했습니다.'),
   ('답은 뇌 밖의, 작은 녹조류에 있었다','빛의 방향을 감지하는 생물에서\n빛 스위치의 단서를 찾았습니다.'),
   ('빛을 받으면, 작은 문이 열린다','문은 세포막의 이온 통로를\n표현한 비유입니다.'),
   ('빛 → 문 → 전기적 변화','이 빛의 문이 채널로돕신입니다.'),
   ('이 문을, 뉴런에도 만들 수 있다면?','유전자를 발현시켜 뉴런 막에\n같은 단백질을 만듭니다.'),
   ('이제 뉴런에, 빛 리모컨이 생긴다','충분한 전기적 변화가 생기면\n뉴런이 신호를 발생시킵니다.'),
   ('빛은 퍼져도, 반응할 세포는 선택한다','빛 조사 영역과 단백질 발현이\n겹치는 세포가 광자극에 반응합니다.'),
   ('빛은 언제, 유전학은 누구를 고른다','시간과 대상을 함께 선택하는 기술.\n광유전학입니다.'),
   ('이 뉴런을 켜면, 행동이 바뀔까?','신경 활동에 개입하고\n실험 결과를 측정합니다.'),
   ('같이 움직임에서, 직접 개입으로','대조 실험과 함께 뉴런의\n인과적 역할을 시험합니다.'),
   ('회로의 일부를, 하나씩 눌러본다','각 집단의 역할과 연결을\n실험으로 조사합니다.'),
   ('다른 단백질로, 활동을 억제할 수도 있다','자극과 억제에는 서로 다른\n광감응 단백질을 사용합니다.'),
   ('조류의 작은 문에서, 뇌의 리모컨까지','기초 연구의 발견이\n새로운 실험 도구가 되었습니다.'),
   ('뇌를 본다 → 뇌에 개입한다','관찰에 스위치를 더해\n신경 활동의 역할을 시험했습니다.')]
  for i,(title,caption) in enumerate(titles):
   self.cue(title,caption);self.visual(i);self.finish()

 def visual(self,i):
  if i==0:
   board=bulbs();self.add(Ellipse(width=7.2,height=5.5,color=GAS).move_to([0,.2,0]),board)
   for idx,name in [(5,'움직임'),(21,'감정'),(37,'기억')]:
    self.beat(.18,board[1][idx].animate.set_color(GOLD))
    self.add(label(name,0,-3.5,32,GOLD))
    if idx!=37:self.remove(self.mobjects[-1])
  elif i==1:
   n=neuron(0,1.7,RED,.65);m=mouse(-1.4,-.1);self.add(n,m)
   self.beat(.22,m.animate.shift(RIGHT*2.8))
   self.add(label('뉴런 활성 → 움직임 ?',0,-1.4,34),label('움직임 → 뉴런 활성 ?',0,-2.45,34),label('함께 나타났다 ≠ 원인이다',0,-3.6,28,GOLD))
  elif i==2:
   board=bulbs().scale(.85).shift(UP*.5);r=remote();target=board[1][28]
   self.add(board,r,label('DIRECTLY PRESS IT',0,-3.4,30,GOLD))
   self.beat(.25,Create(DashedLine(r.get_top(),target.get_center(),color=BLUE)))
   self.beat(.25,target.animate.set_color(BLUE),Flash(target.get_center(),color=BLUE))
   self.add(label('행동이 바뀌는지 측정',1,-2.3,25))
  elif i==3:
   n=neuron(0,1,GAS);switch=RoundedRectangle(width=2.3,height=1.3,corner_radius=.2,color=RED).move_to([-2,-1.4,0])
   switch=VGroup(switch,label('기계식 스위치',-2,-1.4,22,RED));self.add(n,switch)
   self.beat(.25,switch.animate.shift(UP*1.1))
   self.beat(.2,switch.animate.shift(DOWN*1.1).set_opacity(.3))
   self.add(label('원하는 세포 × 원하는 순간',0,-3.25,34,GOLD))
  elif i==4:
   a=algae().scale(.8);others=VGroup(algae().scale(.28).move_to([-2.6,-1.5,0]),algae().scale(.28).move_to([2.3,-.8,0]))
   self.add(a,others,label('빛을 감지하는 작은 생물',0,-3.3,30,GREEN))
   self.beat(.25,Create(Arrow([3.3,2,0],[1.1,1.3,0],color=BLUE)))
   self.beat(.25,a.animate.shift(RIGHT*.5).rotate(-.2),others.animate.shift(RIGHT*.4))
  elif i==5:
   c=channel(False);ions=VGroup(*[label('+',x,2.4,36,GOLD) for x in (-.55,0,.55)])
   state=label('닫힌 문',0,-2.7,33,RED);self.add(c,ions,label('세포 밖',-2,2.3,24),label('세포 안',-2,-.9,24),state)
   self.beat(.18,Create(Arrow([2,3,0],[.3,1.4,0],color=BLUE)),c[2].animate.set_opacity(0))
   self.beat(.32,ions.animate.shift(DOWN*3.1))
   self.remove(state);self.add(label('빛으로 열린 문',0,-3.5,33,BLUE))
  elif i==6:
   nodes=VGroup(label('빛',-2.5,1.6,36,BLUE),label('문 열림',0,1.6,32,GREEN),label('전기 변화',2.5,1.6,30,GOLD))
   self.add(nodes,Arrow([-1.8,1.6,0],[-.9,1.6,0],color=GAS),Arrow([.9,1.6,0],[1.6,1.6,0],color=GAS))
   for node in nodes:self.beat(.15,Indicate(node,color=node.get_color()))
   self.beat(.2,FadeIn(label('Channelrhodopsin',0,-1,38,GREEN)))
   self.add(label('채널로돕신 = 빛으로 여는 이온 통로',0,-3.35,28))
  elif i==7:
   left=algae().scale(.4).move_to([-2.5,1.4,0]);n=neuron(2,1.4,GAS,.65)
   self.add(left,n,label('유전자',-2,-.8,28,GREEN),label('단백질',0,-.8,28,GREEN),label('뉴런의 막',2,-.8,28,BLUE),Arrow([-1.25,-.8,0],[-.6,-.8,0],color=GAS),Arrow([.6,-.8,0],[1.25,-.8,0],color=GAS))
   doors=VGroup(*[RoundedRectangle(width=.16,height=.45,corner_radius=.05,color=GREEN).move_to([1.7+j*.3,1.4,0]) for j in range(3)])
   self.beat(.32,FadeIn(doors),n.animate.set_color(GREEN))
   self.add(label('유전자 발현으로 같은 문을 만든다',0,-3.3,29,GOLD))
  elif i==8:
   n=neuron(0,1, GAS,1.1);r=remote(-2.7,-1.65);pulse=Dot(n.get_left(),radius=.13,color=BLUE)
   state=label('광자극 없음',1.3,-1.6,27);self.add(n,r,state)
   self.beat(.2,Create(Arrow([-1,3.1,0],[0,1.8,0],color=BLUE)),n.animate.set_color(BLUE),Transform(state,label('광자극 ON',1.3,-1.6,27,BLUE)))
   self.add(pulse);self.beat(.35,pulse.animate.move_to(n.get_right()))
   self.add(label('빛 → 문 → 전기 → 신호',0,-3.4,32,BLUE))
  elif i==9:
   board=bulbs();selected=[10,18,26,34];self.add(board)
   for idx in selected:board[1][idx].set_color(GREEN)
   illumination=Rectangle(width=3.2,height=4.3,stroke_width=0,fill_color=BLUE,fill_opacity=.08).move_to([-1.1,.25,0])
   self.beat(.2,FadeIn(illumination))
   self.beat(.35,*[board[1][idx].animate.set_color(BLUE) for idx in selected])
   self.add(label('빛이 닿고 + 빛의 문을 가진 세포',0,-3.4,29,GOLD))
  elif i==10:
   for row in range(3):
    for col in range(6):
     self.add(Square(side_length=.65,color=DIM,fill_color=GREEN if row==1 else DIM,fill_opacity=.08).move_to([-1.5+col*.8,1.8-row*.9,0]))
   time_col=Rectangle(width=.7,height=2.5,color=BLUE,fill_color=BLUE,fill_opacity=.08).move_to([.9,.9,0])
   self.add(label('빛: WHEN',.6,3,30,BLUE),label('유전학\nWHO',-2.65,.9,26,GREEN))
   self.beat(.25,Create(time_col),FadeIn(Dot([.9,.9,0],radius=.22,color=GOLD)))
   self.add(label('Opto + Genetics',0,-1.8,37,BLUE),label('광유전학',0,-3,37,GOLD))
  elif i==11:
   n=neuron(0,1.4,GREEN,.8);m=mouse(0,-1.2);self.add(n,m,label('뉴런에 개입한다',0,2.8,30,BLUE))
   self.beat(.2,Create(Arrow([-2.2,2.4,0],[-1,1.9,0],color=BLUE)),n.animate.set_color(BLUE))
   self.beat(.3,m.animate.shift(RIGHT*1))
   self.add(label('행동 변화를 측정한다',0,-2.5,30,GOLD),label('개념 실험 · 결과는 회로마다 다름',0,-3.5,23))
  elif i==12:
   for x,c in [(-1.85,GAS),(1.85,BLUE)]:self.add(RoundedRectangle(width=3.25,height=4.4,corner_radius=.2,color=c).move_to([x,.4,0]))
   self.add(label('관찰',-1.85,3,31),label('개입',1.85,3,31,BLUE),label('A ↔ B',-1.85,1.5,40),label('A → B ?',1.85,1.5,36,GOLD),label('같이 변한다',-1.85,-.6,27),label('직접 바꿔본다',1.85,-.6,27,BLUE))
   self.add(label('+ 대조 실험',0,-2.5,28,GREEN),label('인과적 역할을 시험한다',0,-3.5,32,GOLD))
  elif i==13:
   net=circuit();self.add(net)
   for idx,name in [(0,'움직임'),(3,'감정'),(6,'보상'),(9,'기억')]:
    self.beat(.13,net[1][idx].animate.set_color(BLUE))
    item=label(name,0,-3.3,34,GOLD);self.add(item)
    if idx!=9:self.remove(item)
   self.add(label('기능은 분산되고 집단은 상호작용합니다',0,-2.5,23))
  elif i==14:
   left=neuron(-2,1,BLUE,.7);right=neuron(2,1,GOLD,.7)
   self.add(left,right,label('자극용 단백질',-2,-.5,25,BLUE),label('억제용 단백질',2,-.5,25,GOLD))
   self.beat(.25,Create(Arrow([-2,3,0],[-2,1.8,0],color=BLUE)),Create(Arrow([2,3,0],[2,1.8,0],color=GOLD)),right.animate.set_opacity(.3))
   self.add(label('활동 증가',-2,-1.6,28,BLUE),label('활동 억제',2,-1.6,28,GOLD),label('단백질에 따라 작동 방식이 다릅니다',0,-3.4,27))
  elif i==15:
   for j,(name,col) in enumerate([('조류의 작은 문',GREEN),('뉴런의 빛 스위치',BLUE),('선택한 신경 회로',BLUE),('행동의 역할 시험',GOLD)]):
    y=2.6-j*1.6;self.add(label(name,0,y,33,col))
    if j<3:self.beat(.14,GrowArrow(Arrow([0,y-.45,0],[0,y-1,0],color=GAS)))
  else:
   board=bulbs().scale(.62).shift(UP*1.6);self.add(board)
   self.beat(.22,board[1][18].animate.set_color(BLUE))
   self.add(label('뇌를 본다',0,-.7,34),label('↓',0,-1.5,35,BLUE),label('뇌에 개입한다',0,-2.3,35,GOLD),label('Hegemann · Nagel · Deisseroth',0,-3.2,25),label('2026 NOBEL · PHYSIOLOGY OR MEDICINE',0,-4.05,23,BLUE))
