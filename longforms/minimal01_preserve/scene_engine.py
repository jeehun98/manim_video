"""Two deliberately composed layouts, driven by approved absolute narration times."""
import json, os, textwrap
from pathlib import Path
import numpy as np
from manim import *

ROOT=Path(__file__).resolve().parent
VERT=os.getenv('MINIMAL_LAYOUT','shorts')=='shorts'
config.frame_width=9 if VERT else 16
config.frame_height=16 if VERT else 9
config.background_color='#0B1423'
INK='#EDF3FA';MUTED='#8B9DB5';TEAL='#42D7BD';RED='#FF6B78';YELLOW='#F3D277';PANEL='#152338';EDGE='#2B3E57'
MANIFEST=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
TIMING=json.loads((ROOT/'narration_timing.json').read_text(encoding='utf-8'))

def txt(s,size=30,color=INK,width=None):
 m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.12)
 if width and m.width>width:m.scale_to_fit_width(width)
 return m

def box(s,width=6,height=1.1,color=TEAL,size=30):
 return VGroup(RoundedRectangle(width=width,height=height,corner_radius=.16,stroke_color=color,stroke_width=1.6,fill_color=PANEL,fill_opacity=1),txt(s,size,color,width-.4))

def linepath(points,color=TEAL,width=7):
 return VMobject(color=color,stroke_width=width).set_points_as_corners(points)

def coins(word,width=6.8):
 # Each item is a single semantic coin: indexable for highlighting runs.
 out=VGroup()
 for c in word:
  col=TEAL if c=='H' else MUTED
  out.add(VGroup(Circle(radius=.28,color=col,stroke_width=1.5,fill_color=col,fill_opacity=.12),txt('앞' if c=='H' else '뒤',18,col)))
 out.arrange(RIGHT,buff=.12)
 out.scale_to_fit_width(width)
 return out

def road(removed=False,center=None,size=None):
 c=np.array(center if center is not None else [0,.7 if VERT else .15,0],float)
 s=size or (2.6 if VERT else 1.35)
 pos={k:c+np.array(v)*s for k,v in {'A':[-1,1,0],'B':[1,1,0],'C':[1,-1,0],'D':[-1,-1,0]}.items()}
 edges=VGroup(*[Line(pos[a],pos[b],color=INK,stroke_width=5) for a,b in [('A','B'),('B','C'),('C','D'),('D','A')]])
 if removed:edges[0].set_opacity(0)
 dots=VGroup(*[Dot(p,radius=.095,color=INK) for p in pos.values()])
 labels=VGroup(*[txt(k,24).move_to(p+(p-c)/np.linalg.norm(p-c)*.36) for k,p in pos.items()])
 unit=txt('도로 길이 = 1',18,MUTED).move_to(c+DOWN*.95)
 return VGroup(edges,dots,labels,unit),pos,edges

class PreserveScene(Scene):
 index=0
 def at(self,absolute):
  target=absolute-self.start
  if self.time>target+.075:raise RuntimeError(f'scene {self.index+1}: {self.time} exceeds {target}')
  if target-self.time>.001:self.wait(target-self.time)
 def note(self,s,color=TEAL):
  m=txt(s,29 if VERT else 25,color,7.1 if VERT else 13).move_to([0,-3.55 if VERT else -1.95,0])
  if hasattr(self,'notice'):self.remove(self.notice)
  self.notice=m;self.add(m);return m
 def condition(self,s):
  m=box(s,7 if VERT else 10,.75,YELLOW,25).move_to([0,4.45 if VERT else 2.5,0])
  if hasattr(self,'cond'):self.remove(self.cond)
  self.cond=m;self.add(m);return m
 def construct(self):
  m=MANIFEST[self.index];self.start=m['start'];self.end=m['end']
  self.add(txt('모든 것이 필요할까?   /   01',20,MUTED).move_to([0,7.05 if VERT else 4.02,0]))
  self.add(txt(m['title'],38 if VERT else 35,INK,7.1 if VERT else 14).move_to([0,6.05 if VERT else 3.35,0]))
  self.add(Line([-3.55 if VERT else -7,5.35 if VERT else 2.88,0],[3.55 if VERT else 7,5.35 if VERT else 2.88,0],color=EDGE,stroke_width=1))
  # Full narration captions are composited once after concat. Mutating a caption
  # group's children during Cairo animations can retain cached old text.
  track=Line([-3.55 if VERT else -7,-6.95 if VERT else -4.08,0],[3.55 if VERT else 7,-6.95 if VERT else -4.08,0],color=EDGE,stroke_width=2)
  progress=Line(track.get_start(),track.get_start()+RIGHT*.001,color=TEAL,stroke_width=3)
  progress.add_updater(lambda p:p.put_start_and_end_on(track.get_start(),track.get_start()+RIGHT*track.width*max(.0001,min(1,(self.start+self.time)/154))))
  self.add(track,progress)
  getattr(self,f'part_{self.index:02}')()
  self.at(self.end)

 def part_00(self):
  cols=10 if VERT else 20
  nums=VGroup(*[txt(str(i%2+1),22,MUTED) for i in range(200)]).arrange_in_grid(cols=cols,buff=(.28,.14))
  nums.scale_to_fit_width(6.8 if VERT else 12)
  if nums.height>(6.4 if VERT else 3.4):nums.scale_to_fit_height(6.4 if VERT else 3.4)
  nums.move_to([0,.8 if VERT else .3,0])
  self.play(LaggedStart(*[FadeIn(VGroup(*nums[k:k+cols])) for k in range(0,200,cols)],lag_ratio=.06),run_time=1.8)
  self.at(2)
  pair=SurroundingRectangle(VGroup(nums[0],nums[1]),color=YELLOW,buff=.08)
  self.play(Create(pair),run_time=.6)
  self.play(*[x.animate.set_color(TEAL if i%2==0 else YELLOW) for i,x in enumerate(nums)],run_time=1.2)
  self.at(7)
  rule=box('[1, 2] × 100',6.3,1.5,TEAL,42).move_to([0,1.3 if VERT else .4,0])
  self.play(FadeOut(pair),ReplacementTransform(nums,rule),run_time=1.8)
  self.note('패턴 + 반복 횟수',YELLOW)
  self.at(13)
  restored=txt('1  2  1  2  1  2  ···  1  2',29,INK,7).move_to([0,-.6 if VERT else -.8,0])
  self.play(FadeIn(restored,shift=DOWN*.2),run_time=.7)
  self.note('200개 숫자 · 원본 복원 가능')

 def part_01(self):
  rule=box('[1, 2] × 100',6.2,1.3,TEAL,39).move_to([0,2.7 if VERT else 1.15,0]);self.add(rule)
  self.note('200개 숫자 · 원본 복원 가능')
  self.at(21)
  q=txt('왜 더 작게 표현할까?',34,YELLOW,7).move_to([0,.7 if VERT else .05,0]);self.play(FadeIn(q),run_time=.6)
  self.at(25)
  labels=['저장 공간','계산 자원*','숨은 규칙']
  cards=VGroup(*[box(s,2.15,.95,TEAL,23) for s in labels]).arrange(RIGHT,buff=.2).move_to([0,-1 if VERT else -1,0])
  self.play(LaggedStart(*[FadeIn(c,shift=UP*.15) for c in cards],lag_ratio=.5),run_time=1.8)
  self.note('* 계산 비용 절감은 조건에 따라 달라짐',MUTED)
  self.at(32)
  self.play(FadeOut(cards),FadeOut(q),run_time=.4);self.note('무엇을 유지해야 할까?',YELLOW)

 def part_02(self):
  q=txt('무엇을 그대로\n유지해야 할까?',43,YELLOW,7).move_to([0,2 if VERT else .6,0]);self.add(q)
  self.at(36)
  a=box('전체 정보 복원',6 if VERT else 5.6,1.2,TEAL)
  b=box('특정 결과 보존',6 if VERT else 5.6,1.2,YELLOW)
  VGroup(a,b).arrange(DOWN if VERT else RIGHT,buff=.55).move_to([0,-.9 if VERT else -.9,0])
  self.play(FadeOut(q),FadeIn(a),FadeIn(b),run_time=.9)
  self.note('무엇이 같아야 하는가?',YELLOW)

 def part_03(self):
  self.condition('관점 ① 전체 정보 복원')
  rule=box('[1, 2] × 3',5.4,1.2,TEAL,40).move_to([0,2.35 if VERT else 1,0]);self.add(rule)
  seq=txt('1   2   1   2   1   2',40,INK,7).move_to([0,-.1 if VERT else -.65,0])
  arrow=Arrow(rule.get_bottom(),seq.get_top()+UP*.12,color=TEAL,buff=.15)
  self.at(44);self.play(GrowArrow(arrow),FadeIn(seq),run_time=1.2)
  self.note('순서까지 그대로 복원')

 def part_04(self):
  self.condition('관점 ② 특정 결과 보존')
  seq=txt('1   2   1   2   1   2',38,INK,7).move_to([0,2.1 if VERT else 1,0]);self.add(seq)
  self.at(54)
  summary=box('1의 개수 = 3',5.7,1.25,YELLOW,35).move_to([0,-.1 if VERT else -.45,0])
  self.play(TransformFromCopy(seq,summary),run_time=1)
  self.note('개수는 보존 · 순서는 복원 불가',YELLOW)

 def part_05(self):
  g,p,e=road();self.play(FadeIn(g),run_time=1.1)
  self.at(62);self.condition('네 지점 · 각 도로의 길이 1')
  self.note('A · B · C · D',MUTED)

 def part_06(self):
  g,p,e=road();e[0].set_color(INK);self.add(g);self.condition('조건 ① 모든 지점에 도달')
  self.note('도로 4개',MUTED)
  self.at(67)
  self.play(e[0].animate.set_color(RED),run_time=.5);self.play(FadeOut(e[0]),run_time=.6)
  self.note('도로 4 → 3 · 도달 경로 확인',TEAL)
  path=linepath([p[k] for k in 'ADCB']);self.play(Create(path),run_time=1.8)
  self.at(71);self.note('도로 4 → 3 · 모든 지점에 도달 가능')

 def part_07(self):
  g,p,e=road(True);self.add(g,linepath([p[k] for k in 'ADCB']))
  self.condition('조건 ② 모든 최단거리 유지')
  self.note('각 도로의 길이 1',MUTED)
  self.at(77)
  ghost=DashedLine(p['A'],p['B'],color=RED,dash_length=.13,stroke_width=3)
  path=linepath([p[k] for k in 'ADCB'],RED)
  self.play(Create(ghost),Create(path),run_time=1.1)
  label=box('A → B : 1 → 3',5.8,.9,RED,29).move_to([0,.65 if VERT else .35,0]);self.play(FadeIn(label),run_time=.5)
  self.note('도달 가능 · 최단거리 보존 실패',RED)

 def part_08(self):
  g,p,e=road(True);self.add(g,linepath([p[k] for k in 'ADCB'],MUTED))
  self.condition('삭제한 도로는 동일')
  labels=VGroup(box('연결성  유지',3.25,.85,TEAL,24),box('거리  달라짐',3.25,.85,RED,24)).arrange(RIGHT,buff=.25).move_to([0,.65 if VERT else .35,0]);self.add(labels)
  self.note('판단 기준이 바뀌면 결과도 달라진다',YELLOW)

 def part_09(self):
  self.condition('질문: 앞면은 몇 번?')
  row=coins('HHHHHTTTTT').move_to([0,2.25 if VERT else .8,0]);self.play(FadeIn(row),run_time=.7)
  self.at(91)
  rings=VGroup(*[SurroundingRectangle(row[j],color=TEAL,buff=.07,corner_radius=.08) for j in range(5)])
  self.play(LaggedStart(*[Create(r) for r in rings],lag_ratio=.12),run_time=1.2)
  self.at(97)
  summary=box('앞면 5번',5.2,1.3,TEAL,41).move_to([0,-.1 if VERT else -.65,0])
  self.play(TransformFromCopy(row,summary),row.animate.set_opacity(.28),FadeOut(rings),run_time=1)
  self.note('횟수 보존 · 순서 제거')

 def part_10(self):
  summary=box('앞면 5번',5.2,1.05,TEAL,34).move_to([0,3 if VERT else 1.55,0]);self.add(summary)
  self.at(102);self.condition('질문 변경: 앞면의 최대 연속 횟수?')
  a=coins('HHHHHTTTTT',6.7).move_to([0,1.05 if VERT else 0,0])
  b=coins('HTHTHTHTHT',6.7).move_to([0,-1 if VERT else -1.1,0])
  self.play(FadeIn(a),FadeIn(b),run_time=.8)
  self.add(txt('기록 A',21,MUTED).next_to(a,UP,buff=.25),txt('기록 B',21,MUTED).next_to(b,UP,buff=.25))
  self.at(106);self.note('같은 요약만으로는 구분 불가',YELLOW)
  self.at(109)
  ra=SurroundingRectangle(VGroup(*a[:5]),color=YELLOW,buff=.08)
  rb=VGroup(*[SurroundingRectangle(b[j],color=YELLOW,buff=.07) for j in range(0,10,2)])
  self.play(Create(ra),Create(rb),run_time=.7)
  self.note('최대 연속 앞면: A = 5번 · B = 1번',YELLOW)

 def part_11(self):
  self.condition('같은 기록, 서로 다른 질문')
  cards=VGroup(box('앞면 횟수 → 5',6 if VERT else 5.8,1.15,TEAL,32),box('최대 연속 → 5 또는 1',6 if VERT else 5.8,1.15,YELLOW,29))
  cards.arrange(DOWN if VERT else RIGHT,buff=.6).move_to([0,1 if VERT else .3,0]);self.add(cards)
  self.at(119)
  self.note('무엇을 알아내려는가?',YELLOW)
  self.play(Indicate(cards[0],color=TEAL),Indicate(cards[1],color=YELLOW),run_time=1)

 def part_12(self):
  self.condition('삭제한 양보다 보존한 조건')
  steps=VGroup(*[box(s,6 if VERT else 3.8,1.15,c,28) for s,c in [('조건 정의',YELLOW),('구조 축소',INK),('결과 확인',TEAL)]])
  steps.arrange(DOWN if VERT else RIGHT,buff=.65).move_to([0,1 if VERT else .35,0])
  self.add(steps[0]);self.note('많이 지웠다고 좋은 표현은 아니다',MUTED)
  self.at(127)
  self.play(FadeIn(steps[1]),run_time=.6);self.play(FadeIn(steps[2]),run_time=.6)
  self.note('보존할 조건 → 더 작은 표현')

 def part_13(self):
  self.condition('가상 예시 · 실제 연구 수치 아님')
  nums=txt('100 → 30',64,INK).move_to([0,2.45,0] if VERT else [-4,.25,0]);self.add(nums)
  q=box('30이 가능한 최소일까?',6.8 if VERT else 6,1.2,YELLOW,32).move_to([0,.3,0] if VERT else [2,.65,0]);self.play(FadeIn(q),run_time=.7)
  self.note('더 작은 후보의 발견 ≠ 최소성의 증명',YELLOW)
  self.at(138)
  unknown=VGroup(DashedVMobject(RoundedRectangle(width=4.6,height=1,corner_radius=.15,color=MUTED),num_dashes=35),txt('더 작은 미지의 표현?',26,MUTED)).move_to([0,-1.7,0] if VERT else [2,-.85,0])
  self.play(FadeIn(unknown),run_time=.8)

 def part_14(self):
  icons=VGroup(box('[1, 2] × N',2.25,.8,TEAL,23),box('도로의 연결',2.25,.8,TEAL,22),box('앞면의 횟수',2.25,.8,TEAL,22)).arrange(RIGHT,buff=.17).move_to([0,3 if VERT else 1.4,0]);self.add(icons)
  self.note('크기보다 먼저, 보존할 조건',YELLOW)
  self.at(147)
  q=txt('무엇을 같다고\n볼 것인가?' if VERT else '무엇을 같다고 볼 것인가?',43,YELLOW,7 if VERT else 13).move_to([0,.7 if VERT else .05,0]);self.play(FadeIn(q),run_time=.7)
  self.at(150)
  sub=txt('그 같음을 유지하는 데\n정말 필요한 것은?' if VERT else '그 같음을 유지하는 데 정말 필요한 것은?',31,TEAL,7 if VERT else 12).move_to([0,-1.65 if VERT else -1.05,0]);self.play(FadeIn(sub),run_time=.7)

