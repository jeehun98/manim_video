"""Multilinearity → alternating components → permutations; column-first convention."""
import importlib.util,json,itertools,math
from pathlib import Path
from manim import *
R=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('det_ch02_shared',R.parent/'chapter_02/visuals.py')
shared=importlib.util.module_from_spec(spec);spec.loader.exec_module(shared)
tx,eq,fit=shared.tx,shared.eq,shared.fit
BLUE,GOLD,GREEN,PURPLE,RED,INK,MUTED=shared.BLUE,shared.GOLD,shared.GREEN,shared.PURPLE,shared.RED,shared.INK,shared.MUTED
COLORS=[BLUE,GOLD,PURPLE]
COMBINATIONS=list(itertools.product(range(3),repeat=3))
PERMS=[p for p in COMBINATIONS if len(set(p))==3]
def parity(p):return (-1)**sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))
def term(p):return ''.join(f'a_{{{r+1}{j+1}}}' for j,r in enumerate(p))
def cards(p,x=0,y=0,size=.65):
 # Color encodes the source column; number encodes the selected row/direction.
 g=VGroup(*[VGroup(RoundedRectangle(width=size,height=size,corner_radius=.08,stroke_color=COLORS[j],stroke_width=2,fill_color=COLORS[j],fill_opacity=.18),eq(str(n+1),size=32*size/.65,c=COLORS[j],w=size*.7)) for j,n in enumerate(p)])
 return g.arrange(RIGHT,buff=size*.18).move_to([x,y,0])
def arrows(pts,reverse=False,c=GREEN):
 order=[pts[0],pts[3],pts[2],pts[1]] if reverse else pts
 return VGroup(*[Arrow(p,q,buff=.15,color=c,stroke_width=2.5,max_tip_length_to_length_ratio=.17) for p,q in zip(order,order[1:]+order[:1])])
def para(u=(2,0),v=(.8,1.7),origin=(-1,-.8,0),scale=1,c=PURPLE):
 o=np.array(origin,dtype=float);u=np.r_[u,0]*scale;v=np.r_[v,0]*scale;pts=[o,o+u,o+u+v,o+v]
 return VGroup(shared.outline(pts,c),Arrow(o,o+u,buff=0,color=BLUE,stroke_width=4),Arrow(o,o+v,buff=0,color=GOLD,stroke_width=4)),pts
def combo(p,x,y,zero=False):
 # Schematic lengths; the literal coefficient remains explicit in each label.
 o=np.array([x-.85,y-.45,0]);u=np.array([1.55,0,0]) if p[0]==0 else np.array([0,1.05,0]);v=np.array([1.15,0,0]) if p[1]==0 else np.array([0,1.05,0])
 pts=[o,o+u,o+u+v,o+v];g=VGroup()
 if p[0]!=p[1]:g.add(shared.outline(pts,GREEN if p==(0,1) else RED))
 g.add(Arrow(o,o+u,buff=0,color=BLUE,stroke_width=5),Arrow(o,o+v,buff=0,color=GOLD,stroke_width=2.5))
 pair=['ab','ad','bc','cd'][p[0]*2+p[1]]
 g.add(eq(pair,x,y-1.0,31,MUTED if zero else INK,w=2.5),eq(r'(e_'+str(p[0]+1)+r',e_'+str(p[1]+1)+')',x,y+1.0,25,MUTED,w=3))
 return g
def cube(M,center,scale=1.15):
 verts=np.array(list(itertools.product([0,1],repeat=3)),dtype=float);proj=np.array([[1,.5,0],[-.25,.4,1]])
 points=(verts@np.asarray(M).T)@proj.T-(verts@proj.T).mean(axis=0)
 pp=[np.r_[p,0]*scale+np.array(center) for p in points]
 faces=[[0,4,6,2],[0,2,3,1],[0,1,5,4],[4,5,7,6],[2,6,7,3],[1,3,7,5]]
 g=VGroup(*[Polygon(*[pp[i] for i in f],stroke_color=PURPLE,stroke_width=1.5,fill_color=PURPLE,fill_opacity=.035 if abs(np.linalg.det(M))<1e-8 else .07) for f in faces])
 for k,i in enumerate([4,2,1]):g.add(Arrow(pp[0],pp[i],buff=0,color=COLORS[k],stroke_width=4,max_tip_length_to_length_ratio=.16))
 return g
FORMULA=r'\det(A)=\sum_{\sigma\in S_n}\operatorname{sgn}(\sigma)\prod_{j=1}^{n}a_{\sigma(j),j}'

class RuleScene(shared.GeometryScene):
 def construct(self):
  self.rec=json.loads((R/'manifest.json').read_text(encoding='utf-8'))[self.index-1]
  self.start=self.rec['start'];self.end=self.start+self.rec['duration_seconds'];self.audit=[]
  self.add(tx('CHAPTER 03',-5.7,3.65,17,MUTED,w=2),Line([-6.35,3.35,0],[6.35,3.35,0],color=MUTED,stroke_opacity=.25))
  self.header=tx('행렬식의 계산 규칙 · 순열과 방향',0,2.94,31);self.add(self.header)
  self.panel=RoundedRectangle(width=13,height=.96,corner_radius=.12,stroke_width=0,fill_color='#172437',fill_opacity=1).move_to([0,-3.3,0]).set_z_index(50)
  self.cap=VGroup().set_z_index(51);self.add(self.panel,self.cap)
  self.lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines'];self.current=None
  self.schedule=[l for l in self.lines if self.start<=l['start']<self.end];self.set_caption(self.start)
  getattr(self,f'shot_{self.index:02}')();self.to(self.end)
  (R/self.rec['directory']/'layout_audit.json').write_text(json.dumps(self.audit,ensure_ascii=False,indent=2),encoding='utf-8')
 def shot_01(self):
  g,pts=para(origin=(-4.9,-.8,0),scale=1.2);path=arrows(pts);self.add(g,path)
  area=eq(r'|\det A|',3.4,1.25,58,GREEN,w=5);sgn=eq(r'\operatorname{sgn}(\det A)',3.4,-.1,46,RED,w=5)
  self.add(area,sgn,tx('넓이·부피 배율',3.4,.6,26,GREEN,w=5),tx('공간의 방향',3.4,-.85,26,RED,w=5))
  self.act(.8,Indicate(g[0],color=GREEN));self.to(4);self.act(.7,Indicate(path,color=RED));self.to(9)
  self.clear();self.show(eq(r'\det\begin{pmatrix}a&b\\c&d\end{pmatrix}=ad-bc',0,.65,65,PURPLE),self.note('부피와 방향은 왜 이런 계산 규칙을 만들까?',PURPLE),d=.7);self.to(14)
 def shot_02(self):
  g,p=para(origin=(-3.6,-.7,0),scale=1.2);self.add(g,eq(r'S=\det(u,v)',0,2.1,45,PURPLE,w=8))
  self.to(18)
  target,q=para(u=(4,0),v=(.8,1.7),origin=(-3.6,-.7,0),scale=1.2)
  self.act(1.3,Transform(g,target))
  self.show(DashedLine(p[1],p[2],color=MUTED),eq('S',-1.9,.3,35,GREEN,w=1),eq('S',.5,.3,35,GREEN,w=1),d=.4)
  self.show(self.note('det(2u, v) = 2 det(u, v)',GREEN),d=.4);self.to(22)
 def shot_03(self):
  o=np.array([-4.9,-1.35,0]);s=1.02
  def p(x,y):return o+s*np.array([x,y,0])
  first=shared.outline([p(0,0),p(1,0),p(1,2),p(0,2)],BLUE)
  second=shared.outline([p(1,0),p(2,1),p(2,3),p(1,2)],GREEN)
  self.show(first,d=.4);self.show(second,d=.4)
  self.add(eq('u_1=(1,0)',2.4,1.6,34,BLUE,w=6),eq('u_2=(1,1)',2.4,.85,34,GREEN,w=6),eq('v=(0,2)',2.4,.1,34,GOLD,w=6))
  total=Polygon(p(0,0),p(2,1),p(2,3),p(0,2),stroke_color=PURPLE,stroke_width=3,fill_opacity=0)
  self.show(total,eq(r'u=u_1+u_2=(2,1)',2.4,-.8,35,PURPLE,w=6),d=.5)
  self.to(25)
  # Remove the excess bottom triangle, translate it by v into the equal top gap.
  rem1=shared.outline([p(0,0),p(1,.5),p(1,2),p(0,2)],BLUE)
  rem2=shared.outline([p(1,.5),p(2,1),p(2,3),p(1,2)],GREEN)
  tri=Polygon(p(0,0),p(1,0),p(2,1),color=GOLD,fill_color=GOLD,fill_opacity=.35,stroke_width=2)
  self.act(.5,Transform(first,rem1),Transform(second,rem2),FadeIn(tri))
  self.act(1.5,tri.animate.shift(s*2*UP))
  self.show(eq('4=2+2',2.4,-1.55,41,GREEN,w=5),d=.4);self.to(31)
  self.clear();self.show(eq(r'\det(ku,v)=k\det(u,v)',0,1.55,44),eq(r'\det(u_1+u_2,v)=\det(u_1,v)+\det(u_2,v)',0,.2,40),tx('각각의 열벡터에 대한 선형성',0,-1.1,32,PURPLE),self.note('다중선형성 · Multilinearity',PURPLE),d=.6);self.to(35)
 def shot_04(self):
  g,p=para(origin=(-1.7,-.8,0),scale=1.25);path=arrows(p);self.add(g,path)
  order=eq('(v_1,v_2)',-4.5,1,43,GREEN,w=3.8);self.add(order)
  self.act(1.2,Transform(order,eq('(v_2,v_1)',-4.5,1,43,RED,w=3.8)));self.to(38)
  self.act(.8,Transform(path,arrows(p,True,RED)))
  self.show(tx('도형과 넓이는 그대로',3.8,1.5,26,MUTED,w=4),tx('순환 방향만 반전',3.8,.7,26,RED,w=4),d=.4);self.to(44)
  self.show(eq(r'\det(v_2,v_1)=-\det(v_1,v_2)',0,-1.65,45,RED),d=.5);self.to(47)
  self.clear();self.show(tx('다중선형성',-3.3,1.25,35,BLUE,w=5),tx('교대성',3.3,1.25,35,RED,w=5),eq(r'u=u_1+u_2',-3.3,.15,43,BLUE,w=5),eq(r'\det(v,u)=-\det(u,v)',3.3,.15,35,RED,w=5.8),self.note('성분을 분해하고, 순서에 따른 부호를 추적한다',PURPLE),d=.6);self.to(51)
 def shot_05(self):
  m=shared.mat([['a','b'],['c','d']],-4.3,.7);self.add(m)
  origin=np.array([.4,-1.25,0]);u=np.array([2.8,1.3,0]);v=np.array([1.2,3,0])
  def split(vec,c,label,y):
   corner=origin+vec*RIGHT
   return VGroup(Arrow(origin,origin+vec,buff=0,color=c,stroke_width=4),DashedLine(origin,corner,color=c),DashedLine(corner,origin+vec,color=c),eq(label,3.3,y,35,c,w=6))
  one=split(u,BLUE,r'v_1=ae_1+ce_2',2.1);self.show(one,d=.8);self.to(56)
  two=split(v,GOLD,r'v_2=be_1+de_2',-1.95);self.show(two,d=.8);self.to(60)
  self.clear(d=.3)
  top=VGroup(eq('ae_1',-4.5,1.8,36,BLUE,w=2),eq('ce_2',-1.5,1.8,36,BLUE,w=2),eq('be_1',1.5,1.8,36,GOLD,w=2),eq('de_2',4.5,1.8,36,GOLD,w=2));self.add(top)
  for k,(i,j,s) in enumerate([(0,2,r'ab\det(e_1,e_1)'),(0,3,r'ad\det(e_1,e_2)'),(1,2,r'bc\det(e_2,e_1)'),(1,3,r'cd\det(e_2,e_2)')]):
   x=-4.5+3*k;dest=eq(s,x,-.5,30,w=2.85)
   lines=VGroup(Line(top[i].get_bottom(),[x,.1,0],color=BLUE,stroke_opacity=.4),Line(top[j].get_bottom(),[x,.1,0],color=GOLD,stroke_opacity=.4))
   self.act(.8,Create(lines),TransformFromCopy(VGroup(top[i],top[j]),dest))
  self.show(self.note('각 열에서 하나의 성분씩 선택 → 네 가지 조합',PURPLE),d=.5);self.to(66)
 def shot_06(self):
  combos=VGroup(*[combo(p,x,y) for p,x,y in [((0,0),-3.4,1),((0,1),3.4,1),((1,0),-3.4,-1.3),((1,1),3.4,-1.3)]])
  # Compact the four panels vertically to reserve the subtitle lane.
  combos.scale(.85).move_to([0,.25,0]);self.add(combos)
  self.show(SurroundingRectangle(combos[0],color=MUTED),SurroundingRectangle(combos[3],color=MUTED),d=.5);self.to(72)
  self.act(.6,combos[0].animate.set_opacity(.12),combos[3].animate.set_opacity(.12))
  self.show(self.note('같은 방향은 0 · 서로 다른 두 방향만 남는다',GREEN),d=.5);self.to(76)
 def shot_07(self):
  m=shared.mat([['a','b'],['c','d']],-3.7,.8);self.add(m)
  boxes=VGroup(*[SurroundingRectangle(m.get_entries()[i],color=GREEN,buff=.15) for i in [0,3]])
  self.show(boxes,combo((0,1),2.8,.6),d=.5)
  first=eq(r'ad\det(e_1,e_2)=ad',0,-1.6,44,GREEN);self.show(first,d=.5)
  self.show(tx('기준: det(e₁,e₂)=det(I)=1',0,2.1,26,MUTED),d=.4);self.to(82)
  self.clear(d=.3);m=shared.mat([['a','b'],['c','d']],-3.7,.8);self.add(m)
  self.show(VGroup(*[SurroundingRectangle(m.get_entries()[i],color=RED,buff=.15) for i in [2,1]]),combo((1,0),2.8,.6),eq(r'bc\det(e_2,e_1)',0,-1.6,45,GOLD),d=.6);self.to(88)
  self.clear(d=.3);self.show(eq(r'\det(e_1,e_2)=+1',-3.2,.8,43,GREEN,w=6),eq(r'\det(e_2,e_1)=-1',3.2,.8,43,RED,w=6),eq(r'bc\det(e_2,e_1)=-bc',0,-.75,50,RED),d=.6);self.to(93)
  self.clear(d=.3);value=eq(r'\det A=0+ad-bc+0',0,.55,61,PURPLE);self.show(value,d=.4)
  self.act(.7,TransformMatchingTex(value,eq(r'\det A=ad-bc',0,.55,68,PURPLE)));self.to(96)
 def shot_08(self):
  m=shared.mat([[r'a_{11}',r'a_{12}',r'a_{13}'],[r'a_{21}',r'a_{22}',r'a_{23}'],[r'a_{31}',r'a_{32}',r'a_{33}']],0,.5,35);self.add(m)
  self.to(100)
  for j in range(3):
   self.show(SurroundingRectangle(m.get_columns()[j],color=COLORS[j],buff=.13),tx(f'{j+1}열: e₁, e₂, e₃',-4.2+j*4.2,-1.65,24,COLORS[j],w=4),d=.5)
  self.to(104);self.clear(d=.3)
  allcards=VGroup(*[cards(p,-4.2+(k//9)*4.2,1.9-(k%9)*.42,.29) for k,p in enumerate(COMBINATIONS)])
  self.act(.9,LaggedStart(*[FadeIn(c) for c in allcards],lag_ratio=.02))
  self.show(self.note('3 × 3 × 3 = 27가지 성분 조합',PURPLE),d=.5);self.to(109)
 def shot_09(self):
  # (e1,e2,e3) → (e1,e1,e2) removes the third independent direction.
  M=np.array([[1,1,0],[0,0,1],[0,0,0]],dtype=float)
  left=cube(np.eye(3),[-3.3,.3,0],1.45);right=cube(np.eye(3),[3.3,.3,0],1.45);self.add(left,right)
  self.add(eq(r'(e_1,e_2,e_3)',-3.3,1.9,34,GREEN,w=5),eq(r'(e_1,e_1,e_2)',3.3,1.9,34,RED,w=5))
  self.act(2,UpdateFromAlphaFunc(right,lambda m,t:m.become(cube((1-t)*np.eye(3)+t*M,[3.3,.3,0],1.45))))
  self.show(eq('V=1',-3.3,-1.25,42,GREEN,w=4),eq('V=0',3.3,-1.25,42,RED,w=4),d=.4);self.to(114)
  self.clear(d=.3)
  groups=[cards(p,-4.2+(k//9)*4.2,1.9-(k%9)*.42,.29) for k,p in enumerate(COMBINATIONS)];self.add(*groups)
  invalid=[g for p,g in zip(COMBINATIONS,groups) if len(set(p))<3];valid=[g for p,g in zip(COMBINATIONS,groups) if len(set(p))==3]
  self.act(.6,*[g.animate.set_opacity(.15) for g in invalid]);self.act(.4,*[FadeOut(g) for g in invalid])
  self.act(.8,*[g.animate.scale(1.8).move_to([-3.5+(k%3)*3.5,1.3-(k//3)*1.25,0]) for k,g in enumerate(valid)])
  self.show(self.note('27 − 21 = 6 · 중복 방향이 없는 조합',GREEN),d=.4);self.to(118)
 def shot_10(self):
  groups=VGroup(*[cards(p,-3.8+(k%3)*3.8,1.5-(k//3)*1.3,.55) for k,p in enumerate(PERMS)]);self.add(groups)
  self.show(self.note('각 숫자 = 해당 열에서 선택한 기본 방향',MUTED),d=.5);self.to(123)
  self.show(tx('순열 · Permutation',0,-1.15,38,PURPLE),d=.4);self.to(125)
  self.clear(d=.3);g=cards((0,1,2),-1.3,.8,.8);sign=eq('+1',2.4,.8,66,GREEN,w=2);self.add(g,sign)
  self.show(tx('기준 순서',-4.9,.8,25,MUTED,w=2.4),d=.3)
  self.act(1,Swap(g[0],g[1],path_arc=PI/2),Transform(sign,eq('-1',2.4,.8,66,RED,w=2)))
  # After physical swap, reorder references to track actual current positions.
  g.submobjects[0],g.submobjects[1]=g.submobjects[1],g.submobjects[0]
  self.to(129)
  self.act(1,Swap(g[1],g[2],path_arc=PI/2),Transform(sign,eq('+1',2.4,.8,66,GREEN,w=2)))
  self.show(tx('짝순열: 123, 231, 312',-3.3,-.75,25,GREEN,w=6),tx('홀순열: 132, 213, 321',3.3,-.75,25,RED,w=6),self.note('교환 방법이 달라도 교환 횟수의 홀짝성은 같다',MUTED),d=.5);self.to(133)
 def shot_11(self):
  self.add(eq(r'A\in\mathbb R^{n\times n}',0,1.25,65,PURPLE),eq(r'n^n\longrightarrow n!',0,-.3,59,GREEN))
  self.to(137);self.clear(d=.3)
  m=shared.mat([[fr'a_{{{i+1}{j+1}}}' for j in range(3)] for i in range(3)],-3.5,.5,36);self.add(m)
  self.add(tx('열 1       열 2       열 3',-3.5,2.2,23,MUTED,w=5.3),tx('선택한 행 번호 → 곱셈 항',3.2,2.2,24,MUTED,w=5.8))
  for k,p in enumerate(PERMS):
   c=GREEN if parity(p)>0 else RED;chosen=[m.get_entries()[r*3+j] for j,r in enumerate(p)]
   boxes=VGroup(*[SurroundingRectangle(v,color=COLORS[j],buff=.1) for j,v in enumerate(chosen)])
   dest=eq(('+' if parity(p)>0 else '-')+term(p),3.2,1.45-k*.52,29,c,w=5.5)
   tag=tx(''.join(str(r+1) for r in p),-.5,1.45-k*.52,20,c,w=.8)
   self.act(.3,FadeIn(boxes));self.act(.4,TransformFromCopy(VGroup(*chosen),dest),FadeIn(tag));self.act(.3,FadeOut(boxes))
  self.to(145);self.clear(d=.25)
  self.show(eq(FORMULA,0,.5,50,PURPLE,w=12),tx('라이프니츠 공식 · Leibniz Formula',0,-1.35,34,PURPLE),d=.5);self.to(147)
 def shot_12(self):
  self.add(eq(FORMULA,0,1.7,43,PURPLE,w=12))
  for x,title,sub,c in [(-4.2,'성분 분해','모든 성분 조합 생성',BLUE),(0,'방향 중복 제거','서로 다른 행 선택',MUTED),(4.2,'순서 교환','홀짝성으로 부호 결정',RED)]:
   self.add(tx(title,x,.2,31,c,w=3.8),tx(sub,x,-.6,23,c,w=3.9),Arrow([x,.6,0],[x,1.15,0],color=c,buff=.04,stroke_width=2))
  self.to(153)
  self.show(self.note('공간의 부피와 방향 → 대수적인 계산 규칙',PURPLE),d=.6);self.to(158)
 def shot_13(self):
  counts=[2,3,4,5,6,8,10]
  bars=VGroup()
  for k,n in enumerate(counts):
   y=2.05-k*.53;length=.25+7*math.log10(math.factorial(n))/math.log10(math.factorial(10))
   bar=Rectangle(width=length,height=.23,stroke_width=0,fill_color=PURPLE,fill_opacity=.7).move_to([-3+length/2,y,0])
   bars.add(VGroup(tx(f'{n}×{n}',-4.5,y,23,MUTED,w=1.8),bar,tx(f'{math.factorial(n):,}',-2.7+length,y,22,PURPLE,w=2.2)))
  self.act(1.8,LaggedStart(*[FadeIn(g) for g in bars],lag_ratio=.1))
  self.show(tx('막대 길이: 로그 척도 · 항의 개수',0,-2.05,21,MUTED,w=10),d=.4);self.to(163)
  self.clear(d=.3)
  self.show(eq(r'10!=3,628,800',0,1.85,51,PURPLE),eq(r'\begin{pmatrix}a&b&c\\d&e&f\\g&h&i\end{pmatrix}\quad\longrightarrow\quad\begin{pmatrix}*&*&*\\0&*&*\\0&0&*\end{pmatrix}',0,.1,42,w=11),self.note('모든 순열을 직접 계산해야 할까?',PURPLE),d=.7);self.to(168)
