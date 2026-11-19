"""162-second determinant elimination short; exact row operations."""
import json,sys,itertools,math
from pathlib import Path
from manim import *
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
import longforms.qcs01_speed.direction as shared
from longforms.qcs01_speed.direction import QCSScene
from episodes.detperm01_permutation_sign.scene import txt,eq,cards,selected,BLUE,GREEN,GOLD,PURPLE,RED,INK,MUTED
shared.FPS=30
config.frame_rate=30
config.background_color='#0B1020'
DATA=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
A=[[2,1,1],[4,3,3],[2,2,3]]
U=[[2,1,1],[0,1,1],[0,0,1]]
L=[[1,0,0],[2,1,0],[1,1,1]]
PERMS=list(itertools.permutations((1,2,3)))
def mtex(values,y=0,x=0,scale=1,color=INK):
 m=Matrix([[str(v) for v in r] for r in values],h_buff=1.15,v_buff=.85,element_to_mobject=lambda s:MathTex(s,font_size=44,color=color))
 return m.scale(scale).move_to([x,y,0])
def parity(p):return (-1)**sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))
class ElimScene(QCSScene):
 data=DATA
 replace=Scene.replace
 def setup(self):
  super().setup();keep=[self.title,self.caption,self.caption_panel]
  self.remove(*[m for m in list(self.mobjects) if m not in keep]);self.title.move_to(UP*6.1)
  self.header=VGroup(txt('LINEAR ALGEBRA  /  GAUSSIAN ELIMINATION',7.2,16,MUTED),Line([-3.8,6.65,0],[3.8,6.65,0],color=MUTED,stroke_opacity=.25),txt('모든 항의 합 → 0을 만드는 연산 → 대각선 곱',5.05,25,BLUE))
  self.add(self.header)
 def clear_body(self):
  keep=[self.title,self.caption,self.caption_panel,self.header]
  obs=[m for m in self.mobjects if m not in keep]
  if obs:self.play(*[FadeOut(m) for m in obs],run_time=.4)
 def row_update(self,m,row,values,duration=.8):
  n=len(values);entries=m.get_entries()
  targets=[MathTex(str(v),font_size=44,color=RED if v==0 else INK).match_height(entries[row*n+j]).move_to(entries[row*n+j]) for j,v in enumerate(values)]
  self.play(*[Transform(entries[row*n+j],t) for j,t in enumerate(targets)],run_time=duration)
 def triangular(self,m):
  n=3
  for i,e in enumerate(m.get_entries()):e.set_color(GREEN if i//n==i%n else RED if i//n>i%n else INK)
 def ref(self,y=-3.5):
  self.add(txt('원래 A',y,23,BLUE,x=-2.8,width=1.5),mtex(A,y,-.55,.48,BLUE),eq(r'\det A=2',y,31,GREEN,x=2.4,width=2.5))

class Shot01(ElimScene):
 shot=0
 def s01(self):
  m=mtex([['a','b','c'],['d','e','f'],['g','h','i']],2.1);self.show(m,run_time=.4)
  for k,(p,t) in enumerate(zip(PERMS,['+aei','-afh','-bdi','+bfg','+cdh','-ceg'])):
   color=GREEN if parity(p)>0 else GOLD;box=selected(m,p,color)
   self.play(FadeIn(box),run_time=.2);self.show(eq(t,-.35-(k//3)*1.1,32,color,x=-2.4+(k%3)*2.4,width=2),run_time=.3);self.play(FadeOut(box),run_time=.2)
  self.show(txt('각 행·각 열에서 하나씩 · 부호는 홀짝성',-3.5,28));self.to(8)
  self.clear_body()
  grid=VGroup(*[Square(side_length=.28,stroke_width=1,stroke_color=BLUE,fill_color=BLUE,fill_opacity=.1).move_to([(j-4.5)*.34,2.4-(i-4.5)*.34,0]) for i in range(10) for j in range(10)])
  self.show(grid,txt('10×10 행렬',4.35,31,BLUE),run_time=.4)
  number=eq('3!=6',-.55,44,GREEN);self.show(number,run_time=.3)
  for target in ['5!=120',r'8!=40\,320',r'10!=3\,628\,800']:
   self.play(Transform(number,eq(target,-.55,44,GREEN)),run_time=.6)
   self.play(*[Indicate(grid[i*10+(i*3)%10],color=GOLD,scale_factor=1.1) for i in range(10)],run_time=.4)
  self.show(eq(r'n!\ \mathrm{terms}',-2.2,43,GOLD),txt('차수가 커질수록 폭발하는 항의 수',-3.7,30));self.to(18)
  self.clear_body();self.show(eq(r'3\,628\,800',2.4,72,GOLD),txt('이 모든 항을 계산해야 할까?',-.1,38),eq(r'A\longrightarrow U',-2.4,57,BLUE),txt('계산하기 쉬운 구조로 바꾸기',-4,29));self.to(23)

class Shot02(ElimScene):
 shot=1
 def s02(self):
  m=mtex([[2,1],[4,3]],1.9);status=eq(r'\det A=?',3.8,42,BLUE);self.show(m,status,txt('값을 보존하는 변형을 찾는다',-2.8,33));self.to(30)
  rowbox=SurroundingRectangle(m.get_rows()[0],color=BLUE,buff=.18);self.show(rowbox,run_time=.3);self.to(32)
  self.play(Transform(rowbox,SurroundingRectangle(m.get_rows()[1],color=GOLD,buff=.18)),run_time=.3);self.to(34)
  self.play(FadeOut(rowbox),run_time=.3);calc=eq(r'\det A=2\times3-1\times4=2',-.1,40,GREEN);self.show(calc);self.play(Transform(status,eq(r'\det A=2',3.8,42,GREEN)),run_time=.4);self.to(39)
  self.clear_body();m=mtex([[2,1],[4,3]],1.6);self.show(m,eq(r'R_2\leftarrow R_2-2R_1',3.8,39,GOLD),eq(r'(4,3)-2(2,1)=(0,1)',-.65,36,GOLD),eq(r'\det A=2',-3,42,GREEN),run_time=.3)
  self.row_update(m,1,[0,1],1.1);self.to(43)
  self.show(txt('첫 행은 그대로 · 둘째 행만 갱신',-1.7,29),run_time=.4);self.to(45)
  self.clear_body();self.show(mtex([[2,1],[4,3]],1.5,-2,.85),mtex([[2,1],[0,1]],1.5,2,.85),txt('A',3,30,BLUE,x=-2,width=1),txt('U',3,30,BLUE,x=2,width=1),txt('→',1.5,35,GOLD),eq(r'\det A=2=\det U',-.8,46,GREEN),txt('행렬식은 변하지 않았다',-3.3,36,GREEN),run_time=.4);self.to(48)

class Shot03(ElimScene):
 shot=2
 def s03(self):
  self.show(eq(r'R_i\leftarrow R_i+kR_j\quad(i\ne j)',2.8,38,GOLD),eq(r'\det A\,{}^{\prime}=\det A',.7,50,GREEN),txt('다른 행의 배수를 더하거나 뺀다',-1.2,32));self.to(50)
  self.show(eq(r'A^{\prime}=EA,\qquad\det E=1',-2.6,36,PURPLE),eq(r'\det(EA)=\det E\,\det A=\det A',-4,31,GREEN));self.to(56)
  self.clear_body();self.show(txt('별도 예시: 넓이 1의 정사각형에 전단 E 적용',4.15,24,MUTED),eq(r'E(k)=\begin{pmatrix}1&k\\0&1\end{pmatrix}',2.8,38,PURPLE),eq(r'\det E(k)=1',-3.3,43,GREEN),run_time=.4)
  o=np.array([-2,-1.5,0]);s=2
  def shear(k):return Polygon(o,o+[s,0,0],o+[s*(1+k),s,0],o+[s*k,s,0],color=PURPLE,fill_color=PURPLE,fill_opacity=.2)
  p=shear(0);base=Line(o,o+[s,0,0],color=GREEN,stroke_width=5);height=DashedLine(o+[-.35,0,0],o+[-.35,s,0],color=GREEN);self.show(p,base,height,run_time=.4);self.to(60)
  self.play(UpdateFromAlphaFunc(p,lambda m,a:m.become(shear(.8*a))),run_time=3,rate_func=linear)
  self.show(txt('밑변 × 높이 = 1 · 모양 변화 ≠ 넓이 변화',-2.3,27,PURPLE),run_time=.4);self.to(67)
  self.clear_body();self.show(mtex([[2,1],[4,3]],1.1,-2,.9),mtex([[2,1],[0,1]],1.1,2,.9),eq(r'R_2\leftarrow R_2-2R_1',3.5,36,GOLD),eq(r'4\longrightarrow0',-1.1,52,RED),eq(r'\det A=\det U=2',-2.7,43,GREEN),txt('값은 유지하고, 0을 만든다',-4.1,31),run_time=.4);self.to(73)

class Shot04(ElimScene):
 shot=3
 def s04(self):
  m=mtex(A,1.5);self.show(m,eq(r'\det A=2',3.9,40,GREEN),run_time=.4);self.ref();self.to(76)
  op=eq(r'R_2\leftarrow R_2-2R_1',-.8,37,GOLD);self.show(op,run_time=.3);self.row_update(m,1,[0,1,1],.8);self.to(78)
  self.play(Transform(op,eq(r'R_3\leftarrow R_3-R_1',-.8,37,GOLD)),run_time=.3);self.row_update(m,2,[0,1,2],.8);self.to(80)
  self.play(Transform(op,eq(r'R_3\leftarrow R_3-R_2',-.8,37,GOLD)),run_time=.3);self.row_update(m,2,[0,0,1],.8);self.to(83)
  self.triangular(m);self.play(Transform(op,txt('상삼각행렬  Upper triangular',-.8,31,BLUE)),run_time=.4)
  self.show(txt('대각선 아래는 모두 0',-2.15,32,RED),run_time=.4);self.to(88)

class Shot05(ElimScene):
 shot=4
 def s05(self):
  m=mtex(U,2.25);self.triangular(m);self.show(m,eq(r'\det U=2\times1\times1=2',-.2,43,GREEN),run_time=.4);self.to(94)
  self.show(txt('왜 대각선만 남을까?',-2.6,35,PURPLE),run_time=.3);self.to(95)
  self.clear_body();m=mtex(U,2.35);self.triangular(m);self.show(m,txt('각 행·각 열에서 하나씩 고르기',.45,27,BLUE),run_time=.4);self.to(98)
  rows=[]
  for k,p in enumerate(PERMS):
   values=[U[i][j-1] for i,j in enumerate(p)];nonzero=all(values);color=GREEN if nonzero else RED;boxes=selected(m,p,color)
   self.play(FadeIn(boxes),run_time=.2)
   x=-1.95 if k%2==0 else 1.95;y=-.7-(k//2)*1.15
   row=VGroup(cards(p,y+.2,x,.42),eq(('+' if parity(p)>0 else '-')+r'\,'+r'\times'.join(map(str,values))+'='+str(parity(p)*math.prod(values)),y-.35,25,color,x=x,width=3.4))
   self.show(row,run_time=.3);self.play(FadeOut(boxes),run_time=.3);rows.append(row)
  self.to(105);self.show(txt('0이 포함된 다섯 곱은 모두 0',-4.3,29,RED),run_time=.4)
  self.play(*[r.animate.set_color(MUTED) for r in rows[1:]],run_time=.3)
  self.play(*[FadeOut(r) for r in rows[1:]],run_time=.4);self.to(110)
  self.clear_body();m=mtex(U,1.8);self.triangular(m);self.show(m,txt('0을 피하려면 첫 열은 첫 행에서',-.7,30),run_time=.4)
  lock=selected(m,(1,2,3),GREEN);self.show(lock[0],run_time=.3);self.to(112)
  self.show(lock[1],txt('그다음 둘째 열은 둘째 행에서',-1.7,30),run_time=.3);self.to(114)
  self.show(lock[2],txt('마지막 선택도 대각선으로 고정',-2.7,30),run_time=.3);self.to(116)
  self.clear_body();self.show(mtex(U,2),eq(r'\det U=u_{11}u_{22}u_{33}',-.2,44,GREEN),eq(r'=2\times1\times1=2',-1.5,47,GREEN),txt('복잡한 합이 하나의 곱으로 바뀐다',-3.5,33),run_time=.4);self.to(120)

class Shot06(ElimScene):
 shot=5
 def s06(self):
  self.show(mtex(A,1.9,-1.95,.75),mtex(U,1.9,1.95,.75),txt('→',1.9,35,GOLD),eq(r'\det A=\det U=2',-.5,44,GREEN),txt('Gaussian elimination',-2,31,BLUE),txt('행 덧셈으로 만든 상삼각행렬',-3.5,30));self.to(125)
  self.clear_body();self.show(txt('행 연산마다 변화 규칙이 다르다',3.9,32,PURPLE),eq(r'R_i\leftrightarrow R_j\ :\ D\to-D',2.5,36,GOLD),eq(r'R_i\leftarrow kR_i\ :\ D\to kD\quad(k\ne0)',1,34,BLUE),eq(r'R_i\leftarrow R_i+kR_j\ :\ D\to D\quad(i\ne j)',-.5,31,GREEN),txt('D는 연산 직전의 행렬식',-2,26,MUTED),run_time=.4);self.to(129)
  m=mtex([[2,1],[4,3]],-3.4,-2,.65);value=eq('D=2',-3.4,34,GREEN,x=1.5,width=2.5);self.show(m,value,run_time=.3)
  self.play(Swap(m.get_rows()[0],m.get_rows()[1],path_arc=PI/2),Transform(value,eq('D=-2',-3.4,34,GOLD,x=1.5,width=2.5)),run_time=.8);self.to(132)
  self.play(Swap(m.get_rows()[0],m.get_rows()[1],path_arc=PI/2),Transform(value,eq('D=2',-3.4,34,GREEN,x=1.5,width=2.5)),run_time=.6)
  self.row_update(m,0,[6,3],.6);self.play(Transform(value,eq('D=6',-3.4,34,BLUE,x=1.5,width=2.5)),run_time=.3);self.to(136)
  self.clear_body();self.show(txt('이번 소거: 행 교환 0회 · 행 배수 없음',3.5,31,BLUE),eq(r'(-1)^0=+1',1.7,48,GREEN),eq(r'\det A=\det U=2',-.4,50,GREEN),txt('교환·배수 변화까지 추적하면 원래 값 복원',-2.8,30),run_time=.4);self.to(140)

class Shot07(ElimScene):
 shot=6
 def s07(self):
  lm=mtex(L,1.8,-2,.8);um=mtex(U,1.8,2,.8)
  self.show(eq('A=LU',3.8,53,BLUE),lm,um,txt('L · 하삼각',.1,28,BLUE,x=-2,width=3.3),txt('U · 상삼각',.1,28,GREEN,x=2,width=3.3),run_time=.4)
  self.show(txt('소거 계수를 L에 기록',-.75,26,GOLD),run_time=.3)
  coeff=MathTex('2',',','1',',','1',font_size=34,color=GOLD).move_to([0,-1.45,0]);self.show(coeff,run_time=.3)
  targets=VGroup(*[lm.get_entries()[i].copy().set_color(GOLD) for i in [3,6,7]])
  self.play(*[TransformFromCopy(coeff[j],targets[k]) for k,j in enumerate([0,2,4])],run_time=.8);self.to(144)
  self.show(eq(r'\det A=\det L\det U',-2.4,40,GREEN),eq(r'=1\times2=2',-3.5,43,GREEN),txt('현재 예시는 행 교환 없음 · 일반적으로 PA = LU',-4.45,22,MUTED),run_time=.4);self.to(150)

class Shot08(ElimScene):
 shot=7
 def s08(self):
  self.show(txt('순열 직접 전개',3.8,30,GOLD,x=-1.95,width=3.6),txt('가우스 소거',3.8,30,BLUE,x=1.95,width=3.6),eq(r'n!',2.2,65,GOLD,x=-1.95,width=3.3),eq(r'O(n^3)',2.2,54,BLUE,x=1.95,width=3.3),txt('항의 개수',.9,25,MUTED,x=-1.95,width=3),txt('산술 연산량',.9,25,MUTED,x=1.95,width=3),mtex(U,-1.2,0,.9),txt('실행시간 수치가 아닌 증가 속도 비교',-3.3,26,MUTED),run_time=.4);self.to(155)
  self.clear_body();m=mtex(U,.4);self.triangular(m);self.show(m,eq(r'A\longrightarrow U',3.4,56,BLUE),eq(r'\det A=2\times1\times1=2',-1.8,42,GREEN),txt('결과의 변화를 아는 연산으로',-3.2,31),txt('복잡한 문제를 단순한 구조로',-4.25,33,BLUE),run_time=.4);self.to(162)
