"""Lottery-ticket workflow from actual fixed-mask tutorial weights and measured toy curves."""
import json,os
from pathlib import Path
import numpy as np
from manim import *
ROOT=Path(__file__).resolve().parent;D=np.load(ROOT/'experiment_data.npz')
VERT=os.getenv('MINIMAL_LAYOUT','shorts')=='shorts';config.frame_width=9 if VERT else 16;config.frame_height=16 if VERT else 9;config.background_color='#0B1423'
INK='#EDF3FA';MUTED='#8B9DB5';TEAL='#42D7BD';PINK='#FF6B98';YELLOW='#F3D277';BLUE='#75A7FF';PURPLE='#B89CFF';PANEL='#152338';EDGE='#2B3E57'
MANIFEST=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'));MASK=D['mask'];SIZES=[2,6,4,2]
SAMPLE=np.flatnonzero(MASK)[np.argsort(abs(D['trained'][MASK==1]-D['initial'][MASK==1]))[-3:]]
def txt(s,size=30,color=INK,width=None):
 m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=1.12)
 if width and m.width>width:m.scale_to_fit_width(width)
 return m

def box(s,width=6,height=1,color=YELLOW,size=30):return VGroup(RoundedRectangle(width=width,height=height,corner_radius=.13,color=color,stroke_width=1.5,fill_color=PANEL,fill_opacity=1),txt(s,size,color,width-.35))

def network(weights=None,mask=None,color=TEAL,width=6.4,height=3,center=ORIGIN,dim=False):
 weights=D['initial'] if weights is None else weights;positions=[]
 for x,n in zip(np.linspace(-width/2,width/2,4),SIZES):positions.append([np.array([x,y,0]) for y in np.linspace(height/2,-height/2,n)])
 edges=VGroup();k=0
 for l in range(3):
  for a in positions[l]:
   for b in positions[l+1]:
    active=mask is None or mask[k]>0;edge=Line(a,b,color=color if active else MUTED,stroke_width=float(np.clip(abs(weights[k])*1.5+.7,.7,3.5)),stroke_opacity=1 if active else .13 if dim else 0);edges.add(edge);k+=1
 nodes=VGroup(*[Dot(p,radius=.085,fill_color='#0B1423',fill_opacity=1,stroke_color=INK,stroke_width=1.4) for layer in positions for p in layer])
 return VGroup(edges,nodes).move_to(center)

def weight_table(values,color=BLUE,center=ORIGIN,title='선택된 연결의 실제 값',width=6.8):
 out=VGroup(txt(title,25,color,width).move_to(UP*1.05))
 for j,k in enumerate(SAMPLE):out.add(box(f'w{k+1} = {values[k]:+.3f}',width,.53,color,27).move_to(UP*(.35-j*.67)))
 return out.move_to(center)

def small_graph(tree=False):
 ps=[np.array([np.cos(i*TAU/8)*2.2,np.sin(i*TAU/8)*2.2,0]) for i in range(8)]
 links=[(i,i+1) for i in range(7)] if tree else [(i,j) for i in range(8) for j in range(i+1,8)]
 return VGroup(VGroup(*[Line(ps[i],ps[j],color=TEAL,stroke_width=2) for i,j in links]),VGroup(*[Dot(p,radius=.09,color=YELLOW) for p in ps]))

def icons():
 names=['그래프','유전체','통계','상태','물리'];out=VGroup(*[box(x,2 if VERT else 2.4,.8,[TEAL,PINK,BLUE,YELLOW,PURPLE][i],27) for i,x in enumerate(names)])
 return out.arrange_in_grid(cols=3 if VERT else 5,buff=.25).move_to([0,1.1 if VERT else .5,0])

def chart_pair(first='dense_accuracy',second='ticket_accuracy',center=None,width=None,height=None):
 center=[0,.5 if VERT else .35,0] if center is None else center;width=(6.3 if VERT else 11.5) if width is None else width;height=(3 if VERT else 1.65) if height is None else height
 ax=Axes(x_range=[0,60,20],y_range=[0,1,1],x_length=width,y_length=height,tips=False,axis_config={'include_ticks':False,'color':EDGE,'stroke_width':1.5}).move_to(center)
 labels=VGroup(*[txt(str(i),18,MUTED).move_to(ax.c2p(i,0)+DOWN*.25) for i in [0,20,40,60]])
 for y in [0,.5,1]:labels.add(txt(f'{y*100:g}%',18,MUTED).move_to(ax.c2p(0,y)+LEFT*.35))
 labels.add(txt('회',20,MUTED).move_to(ax.c2p(60,0)+RIGHT*.3),txt('테스트 정확도',22,MUTED).move_to(ax.c2p(12,1)+UP*.25))
 cols=(TEAL,YELLOW) if first=='dense_accuracy' else (YELLOW,PINK)
 curves=[]
 for key,col in zip([first,second],cols):curves.append(VMobject(color=col,stroke_width=4).set_points_as_corners([ax.c2p(i,float(D[key][i])) for i in range(61)]))
 return VGroup(ax,labels),ax,curves

class LotteryScene(Scene):
 index=0
 def at(self,t):
  target=t-self.start
  if self.time>target+.075:raise RuntimeError((self.index,self.time,target))
  if target-self.time>.001:self.wait(target-self.time)
 def note(self,s,color=YELLOW):self.notice.become(txt(s,27 if VERT else 25,color,7.15 if VERT else 13.5).move_to([0,-3.55 if VERT else -1.95,0]))
 def condition(self,s):self.cond.become(box(s,7 if VERT else 12,.75,YELLOW,24).move_to([0,4.45 if VERT else 2.5,0]))
 def construct(self):
  m=MANIFEST[self.index];self.start=m['start'];self.end=m['end']
  self.add(txt('모든 것이 필요할까?   /   07',20,MUTED).move_to([0,7.05 if VERT else 4.02,0]),txt(m['title'],38 if VERT else 35,INK,7.1 if VERT else 14).move_to([0,6.05 if VERT else 3.35,0]),Line([-3.55 if VERT else -7,5.35 if VERT else 2.88,0],[3.55 if VERT else 7,5.35 if VERT else 2.88,0],color=EDGE,stroke_width=1))
  self.cond=VGroup(VectorizedPoint());self.notice=VGroup(VectorizedPoint());self.add(self.cond,self.notice)
  track=Line([-3.55 if VERT else -7,-6.95 if VERT else -4.08,0],[3.55 if VERT else 7,-6.95 if VERT else -4.08,0],color=EDGE,stroke_width=2);progress=Line(track.get_start(),track.get_start()+RIGHT*.001,color=YELLOW,stroke_width=3)
  progress.add_updater(lambda p:p.put_start_and_end_on(track.get_start(),track.get_start()+RIGHT*track.width*max(.0001,min(1,(self.start+self.time)/170))))
  self.add(track,progress);getattr(self,f'part_{self.index:02}')();self.at(self.end)
 def part_00(self):
  self.add(icons());self.note('서로 다른 분야에서 던진 하나의 질문')
  self.at(4);self.note('모든 것이 정말 필요할까?',YELLOW)
 def part_01(self):
  self.condition('보존 조건: 모든 정점 사이의 연결성')
  g=small_graph().scale(1 if VERT else .7).move_to([0,.7 if VERT else .1,0]);self.add(g);self.play(ReplacementTransform(g,small_graph(True).scale(1 if VERT else .7).move_to(g)),run_time=2);self.note('연결은 줄어도 · 모든 정점에 도달할 수 있다')
 def part_02(self):
  self.condition('필수성은 환경과 다른 유전자에 따라 달라진다')
  genes=VGroup(*[box(chr(65+i),.9,.7,PINK if i==2 else TEAL,27) for i in range(7)]).arrange(RIGHT,buff=.1).move_to([0,1.5 if VERT else .7,0]);self.add(genes)
  a=box('영양분이 공급되는 환경',7 if VERT else 11,1,TEAL,32).move_to([0,-.7 if VERT else -.75,0]);self.add(a);self.play(genes[2].animate.set_opacity(.15),run_time=.7);self.note('유전자 C 없이도 생존할 수 있는 조건',MUTED)
  self.at(14);self.play(genes[2].animate.set_opacity(1),run_time=.7);a.become(box('직접 합성해야 하는 환경',7 if VERT else 11,1,PINK,32).move_to(a));self.note('같은 유전자가 다른 환경에서는 필수적일 수 있다',PINK)
 def part_03(self):
  self.condition('독립·동일 정규분포 · 알려진 분산 · 평균 추론')
  rng=np.random.default_rng(707);pts=VGroup(*[Dot([rng.uniform(-3,3),rng.uniform(-.7,2.8),0],color=BLUE,radius=.04) for _ in range(100)])
  if not VERT:pts.scale(.7)
  self.add(pts);target=box('표본평균 x̄',6 if VERT else 9,1.3,YELLOW,43).move_to([0,.5,0]);self.play(ReplacementTransform(pts,target),run_time=2.5);self.note('전체 기록의 복원과 · 특정 모수 정보의 보존을 구별')
 def part_04(self):
  self.condition('예시: ż = −z + 2u · y = z')
  pair=VGroup(box('x₁',3,1.1,BLUE,41),box('x₂',3,1.1,BLUE,41)).arrange(RIGHT,buff=.4).move_to([0,1.3 if VERT else .8,0]);self.add(pair);self.play(ReplacementTransform(pair,box('z = x₁ + x₂',7 if VERT else 10,1.3,YELLOW,40).move_to(pair)),run_time=1.2)
  self.add(box('상태 차원 감소 · 같은 입출력 동작',7 if VERT else 12,1,YELLOW,31).move_to([0,-1 if VERT else -.85,0]));self.note('대응 초기값과 같은 입력에서 출력 일치')
 def part_05(self):
  self.condition('같은 보편성 부류 · 임계 조건에서')
  cards=VGroup(box('액체 · 기체',3.3 if VERT else 5.5,1.4,TEAL,31),box('자석',3.3 if VERT else 5.5,1.4,PINK,31)).arrange(RIGHT,buff=.3).move_to([0,1.6 if VERT else .8,0]);self.add(cards)
  self.play(FadeIn(box('공통 임계 지수 β',7 if VERT else 11,1.3,PURPLE,40).move_to([0,-.9 if VERT else -.85,0])),run_time=1);self.note('미시적인 구조가 달라도 · 거시적 법칙을 공유할 수 있다')
 def part_06(self):
  cards=icons();self.add(cards);self.note('원하는 결과를 유지하려면 · 실제로 무엇이 필요한가?')
  self.at(43);self.play(FadeOut(cards),run_time=.6);g=network(center=[0,.6 if VERT else .2,0],height=3 if VERT else 2.6);self.play(Create(g),run_time=2)
  self.at(47);self.condition('이제, 인공지능의 신경망에서는?');self.note('수많은 연결 속에 필요한 구조가 숨어 있을까?')
 def part_07(self):
  self.condition('설명용 XOR 실험 · 연결 가중치 44개 · 원논문 재현 아님')
  c=[0,1.5,0] if VERT else [-3.6,.1,0];g=network(D['initial'],width=6.4 if VERT else 6,height=2.6,center=c);table=weight_table(D['initial'],BLUE,[0,-1.65,0] if VERT else [3.65,.2,0],width=6.6 if VERT else 5.9);self.add(g,table);self.note('학습하면서 연결 가중치가 바뀐다',MUTED)
  self.at(54);self.play(Transform(g,network(D['trained'],width=6.4 if VERT else 6,height=2.6,center=c)),run_time=.8);table.become(weight_table(D['trained'],TEAL,table.get_center(),width=6.6 if VERT else 5.9))
  self.at(57);self.note('이 연결들이 모두 필요할까?',YELLOW)
  self.at(59);self.condition('이 설명용 예시: 학습 후 44개 중 33개 연결 유지');self.play(Transform(g,network(D['trained'],MASK,YELLOW,6.4 if VERT else 6,2.6,c,True)),run_time=1);self.note('이 예시의 테스트 정확도: 제거 전후 100% · 보편적 수치 아님')
 def part_08(self):
  self.condition('학습된 값을 유지하는 것과 · 처음부터 다시 학습하는 것은 다르다')
  a=box('Train → Prune\n학습된 값 유지',7 if VERT else 12,1.35,TEAL,33).move_to([0,2.1 if VERT else 1,0]);b=box('Train → Prune → Reset → Retrain\n초기값으로 되돌려 재학습',7 if VERT else 12,1.5,YELLOW,29).move_to([0,-.4 if VERT else -.8,0]);self.add(a);self.note('작은 신경망을 처음부터 학습해도 같은 성능에 도달할까?')
  self.at(68);self.play(FadeIn(b),run_time=.8)
  self.at(75);self.condition('Lottery Ticket Hypothesis · 2018년 최초 공개 / ICLR 2019');self.note('어떤 연결과 어떤 초기값의 조합이 잘 학습되는가?')
 def part_09(self):
  self.condition('1. 무작위 초기화 → W₀ 보관 → 전체 신경망 학습')
  c=[0,1.4,0] if VERT else [-3.6,.1,0];g=network(D['initial'],width=6.4 if VERT else 6,height=2.6,center=c);table=weight_table(D['initial'],BLUE,[0,-1.65,0] if VERT else [3.65,.1,0],width=6.6 if VERT else 5.9);self.add(g,table)
  self.add(box('W₀: 원래 초기값을 별도 보관',7 if VERT else 6,.6,BLUE,26).move_to([0,3.6,0] if VERT else [3.65,1.8,0]));self.note('설명용 실험의 실제 가중치 · 원논문 수치 아님',MUTED)
  self.at(84);self.play(Transform(g,network(D['trained'],width=6.4 if VERT else 6,height=2.6,center=c)),run_time=.9);table.become(weight_table(D['trained'],TEAL,table.get_center(),width=6.6 if VERT else 5.9));self.note('전체망을 학습해 W학습을 얻는다 · W₀는 그대로 보관')
 def part_10(self):
  self.condition('2. 연결 선택 → 마스크 M 고정 → 원래 초기값 복원')
  c=[0,1.5,0] if VERT else [-3.6,.1,0];g=network(D['trained'],MASK,YELLOW,6.4 if VERT else 6,2.6,c,True);table=weight_table(D['trained'],YELLOW,[0,-1.6,0] if VERT else [3.65,.1,0],width=6.6 if VERT else 5.9);self.add(g,table);self.note('같은 인덱스의 33개 연결을 선택 · 제거된 11개는 비활성',MUTED)
  self.at(92);self.note('연결 구조는 그대로 두고 · 가중치 값만 되돌린다')
  self.at(94);self.condition('Reset: W부분망 = M ⊙ W₀')
  self.play(Transform(g,network(D['initial']*MASK,MASK,YELLOW,6.4 if VERT else 6,2.6,c)),run_time=1);table.become(weight_table(D['initial'],BLUE,table.get_center(),title='원래 초기값 W₀에서 같은 값 복원',width=6.6 if VERT else 5.9));self.note('학습 후 값 → 원래 초기값 · 새 난수 추첨이 아님',BLUE)
 def part_11(self):
  self.condition('설명용 XOR 실측 · 같은 데이터·Adam·학습률 · 초기 60회')
  legend=VGroup(txt('전체망 44개',26,TEAL),txt('부분망 33개',26,YELLOW)).arrange(RIGHT,buff=.6).move_to([0,3.3 if VERT else 1.9,0]);self.add(legend)
  base,ax,cs=chart_pair();self.add(base);self.note('제거된 연결은 학습 내내 0으로 고정',MUTED)
  self.at(104);self.play(Create(cs[0]),Create(cs[1]),run_time=4)
  target=DashedLine(ax.c2p(0,.95),ax.c2p(60,.95),color=BLUE,stroke_width=1.5,dash_length=.09);self.add(target)
  result=box('목표 테스트 정확도 95%\n전체망 30회 · 부분망 26회',7 if VERT else 12,1.1,BLUE,28).move_to([0,-2.55 if VERT else -1.15,0]);self.play(FadeIn(result),run_time=.7);self.note('이 작은 실험의 결과 · 원논문의 정량적 재현이 아님',MUTED)
  self.at(114);self.note('Winning Ticket: 비교 성능과 학습 반복 조건을 만족하는 부분망')
 def part_12(self):
  self.condition('같은 마스크 M · 같은 데이터·옵티마이저·학습 설정')
  ca,cb=([-1.85,2,0],[1.85,2,0]) if VERT else ([-3.7,1.05,0],[3.7,1.05,0]);a=network(D['initial'],MASK,YELLOW,3 if VERT else 4.5,1.4 if VERT else 1.2,ca);b=network(D['random_initial'],MASK,YELLOW,3 if VERT else 4.5,1.4 if VERT else 1.2,cb);self.add(a,b)
  labels=VGroup(txt('원래 초기값',23,BLUE).move_to(np.array(ca)+UP*(.95 if VERT else .8)),txt('새 무작위 초기값',23,PINK).move_to(np.array(cb)+UP*(.95 if VERT else .8)));self.add(labels)
  k=int(SAMPLE[0]);readouts=VGroup(box(f'w{k+1} = {D["initial"][k]:+.3f}',3.2,.55,BLUE,25).move_to(np.array(ca)+DOWN*(1.1 if VERT else .9)),box(f'w{k+1} = {D["random_initial"][k]:+.3f}',3.2,.55,PINK,25).move_to(np.array(cb)+DOWN*(1.1 if VERT else .9)));self.add(readouts);self.note('남긴 연결의 인덱스는 정확히 같다',MUTED)
  self.at(121);self.note('같은 구조만으로 학습 경로까지 정해지지는 않는다')
  self.at(123);self.play(FadeOut(a),FadeOut(b),FadeOut(readouts),run_time=.4);labels[0].set_color(YELLOW)
  base,ax,cs=chart_pair('ticket_accuracy','random_accuracy',center=[0,-.35 if VERT else -.35,0],height=2.4 if VERT else 1.7);self.add(base)
  self.play(Create(cs[0]),Create(cs[1]),run_time=3.5);self.note('설명용 XOR 실측 · 원래 초기값이 항상 더 빠르지는 않음',MUTED)
  self.at(129);self.note('초기값이 바뀌면 학습 경로도 달라질 수 있다 · 우열은 설정에 의존')
 def part_13(self):
  self.condition('극단적 압축이 항상 가능하거나 · 발견 비용이 사라지는 것은 아니다')
  a=box('가능한 희소도는 조건에 의존',7 if VERT else 12,1.2,YELLOW,33).move_to([0,1.8 if VERT else .8,0]);self.add(a);self.note('모든 신경망에서 대부분의 연결을 제거할 수 있다는 보장 없음',MUTED)
  self.at(139);b=box('큰 신경망 학습 → 탐색 → 작은 부분망',7 if VERT else 12,1.15,TEAL,29).move_to([0,-.7 if VERT else -.85,0]);self.play(FadeIn(b),run_time=.7);self.note('발견 비용과 최종 모델 크기는 서로 다른 문제')
 def part_14(self):
  self.condition('구조와 초기 조건의 조합')
  pair=VGroup(box('연결 마스크 M',6.6 if VERT else 5.7,1.15,YELLOW,35),box('원래 초기값 W₀',6.6 if VERT else 5.7,1.15,BLUE,35)).arrange(DOWN if VERT else RIGHT,buff=.35).move_to([0,1.8 if VERT else .8,0]);self.add(pair);self.note('크기만 줄이는 문제를 넘어 · 무엇이 학습을 가능하게 하는가?')
  self.at(149);self.play(FadeIn(box('M ⊙ W₀',7 if VERT else 10,1.25,YELLOW,46).move_to([0,-1 if VERT else -.9,0])),run_time=1);self.note('특정한 구조와 초기 조건이 중요한 역할을 할 수 있다')
 def part_15(self):
  self.condition('연결 수와 독립 자유도는 서로 다른 질문')
  self.add(network(D['initial'],MASK,YELLOW,6.4 if VERT else 8,2.5 if VERT else 1.8,[0,1.5 if VERT else .8,0]));self.note('신경망의 크기는 무엇으로 결정해야 할까?')
  self.at(161);q=box('연결의 개수?\n학습에 필요한 독립적인 자유도?',7 if VERT else 12,1.3,BLUE,32).move_to([0,-1.05 if VERT else -.95,0]);self.play(FadeIn(q),run_time=.8);self.note('복권 가설이 최소 독립 자유도의 수를 증명한 것은 아님',MUTED)
  self.at(167);self.note('신경망에서 정말 필요한 것은 무엇일까?',YELLOW)
