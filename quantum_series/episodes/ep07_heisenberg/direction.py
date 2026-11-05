"""From observed spectra to state-pair arrays and noncommuting operations."""
import json
from pathlib import Path
import numpy as np
from manim import *
from quantum_series.shared.theme import text,p,configure,INK,MUTED,GOLD
from quantum_series.shared.matter_waves import BohrAtom,abstract_state,circular_point,sampled_curve,NUCLEUS,ELECTRON
from quantum_series.shared.matrix_mechanics import *
from quantum_series.episodes.ep07_heisenberg.layouts import MatrixLayout
from quantum_series.episodes.ep07_heisenberg.example_matrices import A,B,AB,BA,frequency,TRANSITIONS
D=json.loads(Path(__file__).with_name('script.json').read_text(encoding='utf-8'));L=MatrixLayout(configure().portrait)
def wrap(s,n):
 lines=[];line=''
 for w in s.split():
  if line and len(line+' '+w)>n:lines.append(line);line=w
  else:line=(line+' '+w).strip()
 return '\n'.join(lines+[line])
class MatrixScene(Scene):
 offset=0
 def setup(self):
  self.caption=None;self.heading=None;self.foot=None;self.body=VGroup()
  self.add(text('양자역학의 발견   /   1925 · 하이젠베르크',0 if L.portrait else -3.7,L.brand_y,17,MUTED))
 def to(self,t):
  rem=t-self.offset-self.time
  if rem<-.018:raise RuntimeError(f'Timing overrun {self.offset+self.time} > {t}')
  frames=round(rem*30)
  if frames:self.wait((frames+1e-5)/30)
 def cue(self,i):
  s=D['sentences'][i];self.to(s['start'])
  if self.caption:self.remove(self.caption)
  self.caption=text(wrap(s['text'],26 if L.portrait else 62),y=L.caption_y,size=24 if L.portrait else 25,width=7.6 if L.portrait else 14.1);self.add(self.caption)
  h=text(s['heading'],y=L.heading_y,size=32,width=L.body_width)
  if self.heading:self.play(Transform(self.heading,h),run_time=.25)
  else:self.heading=h;self.play(FadeIn(h),run_time=.3)
 def put(self,*objects):self.body.add(*objects);self.add(*objects)
 def clear(self):
  if len(self.body):self.play(FadeOut(self.body),run_time=.35)
  self.body=VGroup()
 def note(self,s,color=MUTED):
  if self.foot:self.remove(self.foot)
  self.foot=text(s,y=-3.95 if L.portrait else -2.85,size=18,color=color,width=L.body_width);self.add(self.foot)
 def title(self,s,y=None,size=32,color=INK):return text(s,y=(L.center[1] if y is None else y),size=size,color=color,width=L.body_width)
 def diagram(self):
  a,b=L.observation_centers;levels=ThreeLevels(a);spectrum=SpectralLines(b);self.put(levels,spectrum);return levels,spectrum
 def grids(self):
  a,b=L.matrix_centers;left=MatrixGrid(a,label='첫 번째 X');right=MatrixGrid(b,label='두 번째 X');self.put(left,right);return left,right
class ObservablesDirection(MatrixScene):
 offset=0
 def construct(self):
  self.cue(0);c=L.center;atom=BohrAtom(c);wave=sampled_curve(lambda u:circular_point(u,3,c,2.2),WAVE);self.put(atom,wave);self.play(FadeOut(wave),run_time=.8);self.put(text('?',c[0]+2.5,c[1],42,GOLD));self.note('1925 · Werner Heisenberg');self.to(5)
  self.cue(1);self.play(FadeOut(atom.orbits),run_time=.9);atom.remove(atom.orbits);self.put(self.title('궤도 없이 원자를 계산할 수 있을까?',y=-2.05 if L.portrait else -2.0,size=30,color=GOLD));self.to(9)
  self.cue(2);self.clear();atom=BohrAtom(c);self.put(atom)
  for i,r in enumerate([.85,1.5,2.2]):self.put(text(f'n={i+1}',c[0]+r/np.sqrt(2)+.18,c[1]+r/np.sqrt(2)+.18,19,MUTED))
  e=Dot(c+p(.85,0),radius=.08,color=ELECTRON);self.put(e);self.play(MoveAlongPath(e,Circle(radius=.85).move_to(c)),run_time=1.6,rate_func=linear);self.note('허용 상태를 나타내는 보어 모형 · 축척은 개념도');self.to(15)
  self.cue(3);self.play(atom.orbits.animate.set_opacity(.2),e.animate.set_opacity(.25),run_time=.8);self.put(text('직접 관측되지 않은 경로',y=-2.0,size=28,color=MUTED));self.to(19)
  self.cue(4);self.clear();levels,spectrum=self.diagram();self.note('빛의 분석 → 스펙트럼 · 설명용 세 상태 모형')
  packet=sampled_curve(lambda u:L.observation_centers[0]+p((u-.5)*2,.15*np.sin(TAU*3*u)),GOLD);self.put(packet);self.play(packet.animate.move_to(L.observation_centers[1]),run_time=1.1);self.play(FadeOut(packet),run_time=.25);self.to(23)
class SpectrumDirection(MatrixScene):
 offset=23
 def construct(self):
  self.cue(5);levels,spectrum=self.diagram();arrows=[]
  for n,(hi,lo,_) in enumerate(TRANSITIONS):
   arrow=levels.relation(hi,lo,x=(n-1)*.85,color=spectrum.lines[n].get_color());arrows.append(arrow);self.put(arrow);self.play(Indicate(spectrum.lines[n]),run_time=.55)
  energy_formula=self.title('hν = ΔE',y=.5 if L.portrait else -2.1,size=31,color=GOLD);self.put(energy_formula);self.note('설명용 모형 · 실측 수소 스펙트럼이 아님');self.to(31)
  self.cue(6);self.play(Indicate(spectrum),run_time=.65);self.to(33)
  self.cue(7);self.remove(energy_formula);self.body.remove(energy_formula);self.play(*[line.animate.set_opacity(opacity) for line,opacity in zip(spectrum.lines,[.9,.3,.55])],run_time=.9)
  c=L.observation_centers[1];bars=VGroup()
  for n,strength in enumerate([.9,.3,.55]):
   x=c[0]+(n-1)*1.6;bars.add(Rectangle(width=.35,height=.4*strength,color=ENTRY,fill_color=ENTRY,fill_opacity=.7,stroke_width=0).move_to(p(x,-3.25 if L.portrait else -2.05)))
  self.put(bars);self.note('진동수와 세기는 다른 정보 · 선의 높이·굵기는 고정');self.to(37)
  self.cue(8)
  for n in [0,1]:self.play(Indicate(arrows[n]),Indicate(spectrum.lines[n]),run_time=.8)
  self.note('선 세기에는 전이 진폭·상태 점유·관측 조건 등이 관여');self.to(41)
  self.cue(9);self.put(self.title('궤도 대신 상태 사이의 관계',y=4.25 if L.portrait else 1.95,size=28,color=GOLD));self.play(Indicate(levels),run_time=.9);self.to(47)
class ArraysDirection(MatrixScene):
 offset=47
 def construct(self):
  self.cue(10);xs=L.comparison_x;yy=L.pair_y if hasattr(L,'pair_y') else .8
  old=text('x(t)',xs[0],1.2,44,MUTED);new=text('x₁₂   x₁₃   x₂₃',xs[1],1.2,34,ENTRY,width=3.6);self.put(old,new,Arrow(p(xs[0]+.9,.2),p(xs[1]-.9,.2),buff=0,color=GOLD));self.note('xₙₘ: 위치라는 물리량을 두 상태 사이에서 표현한 성분');self.to(52)
  self.cue(11);self.clear();levels=ThreeLevels(L.observation_centers[0]);self.put(levels);self.to(57)
  self.cue(12);relations=VGroup()
  for n,(i,j) in enumerate([(0,1),(0,2),(1,2)]):
   arrow=levels.relation(i,j,x=(n-1)*.9);label=text(symbol(i,j),levels.level_points[j][0]+(n-1)*.9+.3,(levels.level_points[i][1]+levels.level_points[j][1])/2,24,GOLD);relations.add(arrow,label);self.put(arrow,label);self.play(Create(arrow),run_time=.65)
  self.note('상태 쌍의 관계선 · 전자의 공간 이동 경로가 아님');self.to(65)
  self.cue(13);self.clear();grid=MatrixGrid(L.center,cell=1.0,label='X · 하나의 물리량',size=32);self.put(grid);self.play(Create(grid),run_time=1.1);self.note('행: 첫 상태 번호 · 열: 둘째 상태 번호 · 대각 성분 포함');self.to(70)
  self.cue(14);signs=self.title('+     ×     =     ?',y=-2.25 if L.portrait else -2.1,size=38,color=GOLD);self.put(signs);self.to(74)
  self.cue(15);self.play(Indicate(grid),run_time=.65);self.to(76)
class SquareDirection(MatrixScene):
 offset=76
 def construct(self):
  self.cue(16);line=NumberLine(x_range=[0,4,1],length=5.5,include_numbers=False).move_to(L.center+p(0,.7));self.put(line,Dot(line.n2p(3),color=ELECTRON,radius=.09),self.title('예시: x = 3',y=-.2,size=31,color=MUTED),self.title('x² = x × x',y=-1.25,size=39),self.title('3 × 3 = 9',y=-2.3,size=36,color=GOLD));self.note('고전적인 값의 제곱 · 단위는 생략한 수학 예');self.to(82)
  self.cue(17);self.clear();grid=MatrixGrid(L.center,cell=.95,label='X² · 결과 배열',values=[['□','□','□'],['□','□','□'],['□','□','□']],size=28);self.put(grid,grid.highlight(0,2));self.note('결과의 한 성분부터 계산한다');self.to(87)
  self.cue(18);target=self.title('(X²)₁₃',y=-1.7 if L.portrait else -1.8,size=44,color=GOLD);self.put(target);self.play(Indicate(grid.cells[0,2],color=GOLD),run_time=.8);self.note('지금 계산할 결과: 1행 3열');self.to(91)
class ProductDirection(MatrixScene):
 offset=91
 def construct(self):
  self.cue(19);left,right=self.grids();r=left.row_highlight(0);c=right.column_highlight(2);self.put(r,c)
  chain=index_chain(p(0,L.links_y),k=2,width=4.8);self.put(chain);term=self.title('x₁₂ × x₂₃',y=L.calculation_y,size=35,color=GOLD);self.put(term)
  highlights=VGroup(left.highlight(0,1,PRODUCT),right.highlight(1,2,PRODUCT));self.put(highlights);self.play(Indicate(highlights),run_time=1.0);self.note('1 → k → 3은 중간 인덱스 연결 · 실제 연속 전이가 아님');self.to(99)
  self.cue(20);self.remove(term,chain,highlights);self.body.remove(term,chain,highlights)
  terms=['x₁₁x₁₃','x₁₂x₂₃','x₁₃x₃₃'];parts=VGroup()
  for k,txt in enumerate(terms):
   high=VGroup(left.highlight(0,k,PRODUCT),right.highlight(k,2,PRODUCT));label=text(('' if k==0 else '+ ')+txt,0 if L.portrait else (k-1)*3.8,(-1.35-k*.72) if L.portrait else L.sum_y,33,PRODUCT,width=6.4 if L.portrait else 3.6);parts.add(label);self.put(high,label);self.play(Indicate(high),run_time=.55);self.remove(high);self.body.remove(high)
  self.put(self.title('(X²)₁₃ =',y=L.calculation_y,size=32,color=GOLD));self.to(103)
  self.cue(21);self.clear();general=self.title('(X²)ₙₘ = Σₖ xₙₖ xₖₘ',y=1.1 if L.portrait else .6,size=43,color=PRODUCT);self.put(general,self.title('중간 상태 번호 k에 대해 합산',y=-.3 if L.portrait else -.6,size=28));self.note('화면의 세 상태는 설명용 · 일반 이론은 전체 상태에 대해 합산');self.to(107)
  self.cue(22);self.clear();left,right=self.grids();self.put(left.row_highlight(0),right.column_highlight(2));result=self.title('(X²)₁₃ = x₁₁x₁₃\n+ x₁₂x₂₃ + x₁₃x₃₃' if L.portrait else '(X²)₁₃ = x₁₁x₁₃ + x₁₂x₂₃ + x₁₃x₃₃',y=-2.25 if L.portrait else L.sum_y,size=33,color=PRODUCT);self.put(result)
  for k in range(3):self.play(Indicate(left.entries[0,k],color=PRODUCT),Indicate(right.entries[k,2],color=PRODUCT),run_time=.55)
  self.to(112);self.cue(23);self.body.remove(result);self.clear();self.put(result);out=MatrixGrid(p(0,2.0 if L.portrait else .35),values=[['□','□','Σ'],['□','□','□'],['□','□','□']],label='X² · 결과',size=27);self.put(out,out.highlight(0,2,PRODUCT));self.play(TransformFromCopy(result,out.entries[0,2]),run_time=.55);self.put(self.title('행렬곱 · Matrix multiplication',y=L.calculation_y,size=30,color=GOLD));self.note('행·열의 곱을 합산한 결과 → 1행 3열 성분',PRODUCT);self.to(114)
class OrderDirection(MatrixScene):
 offset=114
 def construct(self):
  self.cue(24);self.put(MatrixGrid(L.center,label='행렬역학 · 1925'));xs=L.comparison_x;self.put(text('Max Born',xs[0],-1.4,30,GOLD),text('Pascual Jordan',xs[1],-2.3 if L.portrait else -1.4,30,GOLD,width=3.8));self.note('하이젠베르크의 규칙 → 보른의 인식 → 보른·요르단의 정식화');self.to(121)
  self.cue(25);self.clear();self.put(self.title('A     ×     B',y=1.2,size=49,color=ENTRY),self.title('곱셈 순서',y=-.6,size=30,color=GOLD));self.to(124)
  self.cue(26);self.clear();first=self.title('2 × 3 = 6',y=1,size=48);self.put(first);self.play(Transform(first,self.title('3 × 2 = 6',y=1,size=48)),run_time=.85);self.note('일반적인 숫자의 곱셈');self.to(128)
  self.cue(27);self.clear();xs=L.comparison_x;self.put(MatrixGrid(p(xs[0],2 if L.portrait else .8),A.tolist(),cell=.8,label='A',symbolic=False,indices=False),MatrixGrid(p(xs[1],2 if L.portrait else .8),B.tolist(),cell=.8,label='B',symbolic=False,indices=False));self.note('순수 수학 예 · 원자의 위치·운동량 행렬이 아님');self.to(130)
  self.cue(28);cy=-1.0 if L.portrait else -1.65;ab=MatrixGrid(p(xs[0],cy),AB.tolist(),cell=.8,label='AB',symbolic=False,indices=False);ba=MatrixGrid(p(xs[1],cy),BA.tolist(),cell=.8,label='BA',symbolic=False,indices=False);self.put(ab,ba,ab.highlight(0,0,ORDER),ba.highlight(0,0,ORDER),ab.highlight(1,1,ORDER),ba.highlight(1,1,ORDER));self.play(FadeIn(ab),FadeIn(ba),run_time=.7);self.put(self.title('AB ≠ BA',y=-2.9 if L.portrait else -.1,size=35,color=ORDER));self.to(134)
class OperatorsDirection(MatrixScene):
 offset=134
 def construct(self):
  self.cue(29);self.put(self.title('AB ≠ BA',y=1.4,size=55,color=ORDER));self.note('수학 예를 넘어 · 실제 양자 물리량의 연산 구조');self.to(138)
  self.cue(30);self.clear();self.put(self.title('위치 연산       운동량 연산',y=1.6,size=32),self.title('x̂p̂   와   p̂x̂',y=.4,size=47,color=GOLD),self.title('x̂p̂ − p̂x̂ = iℏI',y=-1.0,size=43,color=ORDER));self.note('정준 위치·운동량 연산자의 관계 · 앞의 2×2 숫자 예와는 별개');self.to(145)
  self.cue(31);self.put(self.title('1927 · 불확정성 관계의 토대',y=-2.15,size=28,color=WAVE));self.note('1925 행렬역학과 이후 불확정성 관계의 발전을 구분');self.to(149)
class MeaningDirection(MatrixScene):
 offset=149
 def construct(self):
  self.cue(32);c=L.center if L.portrait else p(-3.4,.2);atom=BohrAtom(c,(.7,1.2,1.8),MUTED);grid=MatrixGrid(p(0,-1.8) if L.portrait else p(3.4,.2),cell=.43 if L.portrait else .65,label='',size=16 if L.portrait else 23,indices=False);self.put(atom,grid);self.note('행렬이라는 도구에 앞선 계산 관점의 변화');self.to(155)
  self.cue(33);self.play(FadeOut(atom.orbits),run_time=.8);atom.remove(atom.orbits);spectrum=SpectralLines(c,width=4,height=1.5);spectrum.strengths();self.put(spectrum);self.note('궤도를 계산의 출발점에서 제외 · 원자 자체는 유지');self.to(160)
  self.cue(34);self.clear();a,b=L.observation_centers;spectrum=SpectralLines(a,width=3.8,height=1.2);matrix=MatrixGrid(b,cell=.78,label='상태 쌍의 성분');self.put(spectrum,matrix);self.play(Indicate(spectrum),Indicate(matrix),run_time=1.0);self.note('관측 현상과 연결된 물리량들 사이의 관계를 계산');self.to(165)
  self.cue(35);self.clear();self.put(self.title('관측 → 상태 사이의 관계',y=2.0,size=32,color=ENTRY),self.title('새로운 연산 · AB ≠ BA',y=.3,size=39,color=ORDER));self.note('무엇을 계산할 것인가를 바꾸자 다른 수학 구조가 나타났다');self.to(170)
  self.cue(36);self.clear();xs=L.comparison_x;yy=.75;matrix=MatrixGrid(p(xs[0],yy),cell=.68,label='행렬',size=22);wave=abstract_state(p(xs[1],yy),width=3.3);question=text('?',0,-1.5 if L.portrait else yy,44,GOLD);self.put(matrix,wave,question);self.note('궤도 없는 계산을 파동적 상태의 관점에서 설명한다면?');self.to(176)
  self.cue(37);self.play(FadeOut(matrix),FadeOut(question),wave.animate.scale(1.5).move_to(L.center),run_time=.7);self.put(self.title('1926 · Schrödinger',y=-1.9,size=27,color=WAVE));self.note('행렬과 파동 · 원자를 설명하는 새로운 역학');self.to(178);self.to(179)
