"""A historical introduction, using the established determinant graphics."""
import importlib.util,json
from pathlib import Path
from manim import *
R=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('det_intro_shared',R.parent/'chapter_04/visuals.py')
shared=importlib.util.module_from_spec(spec);spec.loader.exec_module(shared)
basis=shared.shared;geometry=basis.shared;foundation=geometry.shared
tx,eq,fit=shared.tx,shared.eq,shared.fit
BLUE,GOLD,GREEN,PURPLE,RED,INK,MUTED=shared.BLUE,shared.GOLD,shared.GREEN,shared.PURPLE,shared.RED,shared.INK,shared.MUTED

def scholar(x,year,name,roman,topic,formula):
 panel=RoundedRectangle(width=5.65,height=3.8,corner_radius=.15,color=GOLD,stroke_opacity=.35,fill_color=GOLD,fill_opacity=.025).move_to([x,.35,0])
 return VGroup(panel,tx(str(year),x,1.8,35,GOLD,w=5),tx(name,x,1.05,35,INK,w=5),tx(roman,x,.5,19,MUTED,w=5),Line([x-2.5,.1,0],[x+2.5,.1,0],color=MUTED,stroke_opacity=.25),tx(topic,x,-.4,26,BLUE,w=5),eq(formula,x,-1.05,34,PURPLE,w=5))

def timeline():
 g=VGroup(Arrow([-5.8,0,0],[5.9,0,0],buff=0,color=MUTED))
 for x,y,year,c,label in [(-5,1,'1683',GOLD,'세키'),(-3.7,-1,'1693',GOLD,'라이프니츠'),(-.4,1,'1750',GOLD,'크라메르'),(4.6,1,'1850',PURPLE,'행렬 이론')]:
  g.add(Dot([x,0,0],color=c,radius=.07),Line([x,0,0],[x,y*.55,0],color=c),tx(year,x,y*.9,30,c,w=2),tx(label,x,y*1.4,23,c,w=2.6))
 g.add(tx('초기 행렬식 연구',-2.7,2.1,30,GOLD,w=6),tx('현대 행렬 이론',4.4,2.1,30,PURPLE,w=4))
 return g

class IntroScene(shared.EliminationScene):
 def construct(self):
  self.rec=json.loads((R/'manifest.json').read_text(encoding='utf-8'))[self.index-1]
  self.start=self.rec['start'];self.end=self.start+self.rec['duration_seconds'];self.audit=[]
  self.masthead=VGroup(tx('CHAPTER 00',-5.7,3.65,17,MUTED,w=2),Line([-6.35,3.35,0],[6.35,3.35,0],color=MUTED,stroke_opacity=.25));self.add(self.masthead)
  self.header=tx('행렬식은 왜 등장했을까?',0,2.94,31);self.add(self.header)
  self.panel=RoundedRectangle(width=13,height=.96,corner_radius=.12,stroke_width=0,fill_color='#172437',fill_opacity=1).move_to([0,-3.3,0]).set_z_index(50)
  self.cap=VGroup().set_z_index(51);self.add(self.panel,self.cap)
  self.lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines'];self.current=None
  self.schedule=[l for l in self.lines if self.start<=l['start']<self.end];self.set_caption(self.start)
  getattr(self,f'shot_{self.index:02}')();self.to(self.end)
  (R/self.rec['directory']/'layout_audit.json').write_text(json.dumps(self.audit,ensure_ascii=False,indent=2),encoding='utf-8')
 def shot_01(self):
  m=foundation.matrix(-3.4,.5);self.add(m,tx('행렬',-3.4,-1.15,28,MUTED,w=4))
  entries=m.get_entries()
  ad=Line(entries[0].get_center(),entries[3].get_center(),color=BLUE,stroke_width=4).set_z_index(-1)
  bc=Line(entries[1].get_center(),entries[2].get_center(),color=GOLD,stroke_width=4).set_z_index(-1)
  self.act(.8,Create(ad));self.act(.8,Create(bc))
  self.show(Arrow([-1.4,.5,0],[.5,.5,0],buff=0,color=MUTED),eq('ad-bc',3.3,.5,75,PURPLE,w=5),tx('행렬식',3.3,-1.15,28,PURPLE,w=4),d=.7)
  self.to(6)
 def shot_02(self):
  self.show(timeline(),d=.7);self.show(self.note('역사적 발전 순서는 학습 순서와 달랐다',GOLD),d=.6);self.to(13)
 def shot_03(self):
  a=scholar(-3.1,1683,'세키 다카카즈','Seki Takakazu · 일본','다항식 방정식의 미지수 소거',r'f(x,y)=0,\quad g(x,y)=0')
  b=scholar(3.1,1693,'라이프니츠','Gottfried Wilhelm Leibniz · 유럽','연립방정식의 해가 존재할 조건',r'a_{ij}')
  self.show(a,d=.7);self.to(17);self.show(b,d=.7)
  self.show(self.note('서로 독립적으로 발견한 행렬식에 해당하는 구조',PURPLE),d=.6);self.to(23)
 def shot_04(self):
  e=foundation.equations(True,-3.5,.8);self.add(e,tx('현대 표기로 재구성',-3.5,2.0,20,MUTED,w=5))
  self.show(eq(r'\begin{aligned}ad\,x+bd\,y&=de\\bc\,x+bd\,y&=bf\end{aligned}',3.15,.8,41,BLUE,w=5.8),d=.7)
  self.act(.7,Indicate(e,color=BLUE))
  self.show(eq(r'(ad-bc)x=de-bf',0,-1.1,51,PURPLE,w=11),self.note('미지수를 제거하고, 계수 사이의 관계를 찾는다',BLUE),d=.8);self.to(31)
 def shot_05(self):
  self.add(tx('1750 · 크라메르',0,2.05,35,GOLD,w=10),tx('Gabriel Cramer',0,1.4,21,MUTED,w=10))
  self.show(eq(r'\Delta=\begin{vmatrix}a&b\\c&d\end{vmatrix}=ad-bc',-3.2,.35,42,PURPLE,w=6),eq(r'\Delta_x=\begin{vmatrix}e&b\\f&d\end{vmatrix}=ed-bf',3.2,.35,42,BLUE,w=6),d=.7)
  self.show(eq(r'x=\frac{\Delta_x}{\Delta},\qquad\Delta\ne0',0,-1.2,53,GREEN,w=10),d=.7)
  self.show(self.note('일반적인 n개 미지수의 연립일차방정식에 적용',GOLD),d=.6);self.to(40)
 def shot_06(self):
  self.add(tx('1850 · 실베스터',-3.1,1.7,35,GOLD,w=5.5),tx('Matrix라는 용어 도입',-3.1,.8,27,MUTED,w=5.5),tx('1858 · 케일리',3.1,1.7,35,GOLD,w=5.5),tx('행렬 이론의 체계적 발전',3.1,.8,27,MUTED,w=5.5),self.note('대표적인 이정표 · 기하학적 해석은 18세기에도 등장',MUTED))
  self.to(44);self.clear(d=.3)
  b=geometry.Board(np.eye(2),origin=(1,-1.45,0),unit=.75,bounds=(.3,6.25,-1.9,2.2))
  self.add(foundation.matrix(-3.4,.65),b,eq(r'\det(A)=ad-bc',-3.4,-1.3,40,PURPLE,w=5))
  target=np.array([[3,1],[1,2]])
  self.act(2.5,UpdateFromAlphaFunc(b,lambda m,t:m.update_matrix((1-t)*np.eye(2)+t*target)));self.to(48)
 def shot_07(self):
  g=foundation.graph_state();g.scale(.58).move_to([-3.4,.8,0]);self.add(g)
  b=geometry.Board(np.array([[3,1],[1,2]]),origin=(1,-.45,0),unit=.63,bounds=(.3,6.1,-.65,2.1));self.add(b)
  self.add(tx('방정식과 해',-3.4,-1.65,28,BLUE,w=5),tx('공간의 부피와 방향',3.2,-1.65,28,GREEN,w=5),eq('ad-bc',-3.4,-1.02,37,PURPLE,w=4),eq('ad-bc',3.2,-1.02,37,PURPLE,w=4))
  self.to(54);self.show(self.note('같은 수식 안에는 어떤 구조가 숨어 있을까?',PURPLE),d=.6);self.to(57)
 def shot_08(self):
  panels=VGroup();icons=VGroup()
  labels=['01 · 등장 배경','02 · 기하학적 의미','03 · 계산 공식','04 · 효율적인 계산']
  for j,(x,y) in enumerate([(-3.15,1.25),(3.15,1.25),(-3.15,-1.15),(3.15,-1.15)]):
   panel=RoundedRectangle(width=5.9,height=2.15,corner_radius=.12,color=MUTED,stroke_opacity=.3,fill_color='#172437',fill_opacity=.35).move_to([x,y,0]);panels.add(panel);self.add(panel,tx(labels[j],x,y+.74,23,[BLUE,GOLD,GREEN,PURPLE][j],w=5.5))
  graph=foundation.graph_state().scale(.30).move_to([-3.15,1.1,0]);icons.add(graph)
  para,_=basis.para(origin=(2.5,.65,0),scale=.4,c=GOLD);icons.add(para)
  cards=VGroup(*[basis.cards(p,-4.35+k*1.2,-1.15,.22) for k,p in enumerate([(0,1,2),(1,2,0),(2,0,1)])]);icons.add(cards,eq('ad-bc',-3.15,-1.75,23,GREEN,w=4))
  u=shared.matrix(shared.U,3.15,-1.15,32).scale(.52);icons.add(u,eq(r'2\times1\times1',3.15,-1.9,23,PURPLE,w=4));self.add(icons)
  for j in range(4):self.act(2.3,Indicate(panels[j],color=[BLUE,GOLD,GREEN,PURPLE][j],scale_factor=1.02))
  self.to(67)
 def shot_09(self):
  self.act(.3,Transform(self.header,tx('방정식에서 발견한 특별한 숫자',0,2.94,31)))
  e=foundation.equations(False,0,.45);self.show(e,d=.6)
  self.show(self.note('방정식의 해는 언제 유일하게 결정될까?',BLUE),d=.5);self.to(71)
