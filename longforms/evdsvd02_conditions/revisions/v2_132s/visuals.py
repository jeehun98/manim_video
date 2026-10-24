"""132-second revision: columns, Gram entries, symmetry, and actual eigendirections."""
import sys,json,textwrap
from pathlib import Path
ROOT=Path(__file__).resolve().parent
WORK=next(p for p in ROOT.parents if (p/'scripts/render.py').exists())
sys.path.insert(0,str(WORK))
from manim import *
from longforms.evdsvd01_names.visuals import BattleScene,label,pos,card,SHORT,BLUE,TEAL,WHITE,MUTED,GOLD,PANEL
from longforms.evdsvd02_conditions.visuals import matrix,mat_card,plane,vector,GOOD,BAD
MANIFEST=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
CUES=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))
A=np.array([[1.,2.],[2.,0.],[0.,1.]])
G=A.T@A
S=np.array([[1.,1.],[0.,1.]])

def gram(values):
    mat=matrix(values,cell=1.2,size=31)
    for i in range(2):
        for j in range(2):mat.entries[i][j].set_color(BLUE if i==j else TEAL)
    group=VGroup(label('AᵀA',y=1.6,size=31,color=TEAL),mat,label('2 × 2',y=-1.6,size=20,color=MUTED))
    group.mat=mat
    return group

def lines(*rows,color=WHITE):
    return VGroup(*[label(s,y=(len(rows)-1)/2*.85-i*.85,size=28,color=color,width=6.2) for i,s in enumerate(rows)])

class RevisedConditions(BattleScene):
    def setup(self):
        self.spec=MANIFEST[self.INDEX];self.length=self.spec['duration_seconds']
        self.add(label('MATRIX DECOMPOSITION WORLD CUP',y=6.55 if SHORT else 3.55,size=15,color=MUTED,width=7 if SHORT else 12))
        y=5.85 if SHORT else 2.98
        self.add(label('EVD',-1.35,y,29,BLUE,2),label('VS',0,y,17,MUTED,1),label('SVD',1.35,y,29,TEAL,2),Line(pos(-3.5 if SHORT else -6.5,y-.45),pos(3.5 if SHORT else 6.5,y-.45),color=MUTED,stroke_opacity=.25))
        self.score=label('EVD  1 : 0  SVD',x=0 if SHORT else 5.1,y=5.13 if SHORT else 2.98,size=15,color=MUTED,width=3)
        self.add(self.score,label('02 / CONDITIONS  ·  분해 가능한 행렬의 범위',y=-6.65 if SHORT else -3.65,size=14,color=MUTED,width=7 if SHORT else 12))
        self.caption=VGroup();self.caption_key=None
        self.caption.add_updater(lambda m,dt:self.update_caption());self.add(self.caption);self.update_caption()
    def update_caption(self):
        t=self.spec['start']+self.time+1e-6
        cue=next((c for c in CUES if c['start']<=t<c['end']),None)
        key=cue['start'] if cue else None
        if key==self.caption_key:return
        self.caption_key=key;self.caption.remove(*list(self.caption))
        if cue:
            words='\n'.join(textwrap.wrap(cue['caption'],27 if SHORT else 52,break_long_words=False))
            txt=label(words,y=-5.7 if SHORT else -2.98,size=22 if SHORT else 23,width=7.1 if SHORT else 12.5)
            bg=RoundedRectangle(width=7.45 if SHORT else 13,height=max(.65,txt.height+.25),corner_radius=.08,stroke_width=0,fill_color='#080F21',fill_opacity=.97).move_to(txt)
            self.caption.add(bg,txt).set_z_index(100)
    def note(self,s,color=MUTED):
        m=label(s,y=-4.35 if SHORT else -2.2,size=22,color=color,width=7 if SHORT else 12)
        self.reveal(m,d=.2);return m
    def cards(self,a,b):
        a.move_to(pos(-1.8 if SHORT else -2.35,.3 if SHORT else -.1))
        b.move_to(pos(1.8 if SHORT else 2.35,.3 if SHORT else -.1))
        return a,b
    def study(self,title,explanation,values):
        self.title(title,TEAL)
        panel=gram(values);explanation,panel=self.split(explanation,panel)
        self.reveal(explanation,panel)
        return panel.mat
    def fill(self,mat,i,j,value,color):
        old=mat.entries[i][j]
        new=label(str(value),old.get_x(),old.get_y(),31,color,width=.9)
        self.play(Transform(old,new),run_time=.3)
    def scene_0(self):
        title=label('행렬 분해\n이상형 월드컵!',y=2.3 if SHORT else 1.25,size=40)
        self.reveal(title);self.to(1);pair=self.pair().move_to(pos(0,-.6));self.reveal(pair,d=.4)
        self.to(3);self.play(FadeOut(title),run_time=.2)
        self.reveal(label('ROUND 02 · 분해 조건',y=2.7 if SHORT else 1.3,size=32,color=GOLD))
    def scene_1(self):
        self.title('EVD · 고유값 분해',BLUE)
        self.reveal(label('A = PDP⁻¹',y=2 if SHORT else 1,size=55,color=BLUE),label('P: 고유벡터 기저   D: 고윳값',y=.6 if SHORT else -.1,size=24,color=MUTED))
        self.to(2);self.reveal(label('2×2 ?     2×3 ?     3×3 ?',y=-1 if SHORT else -1.1,size=32,color=GOLD))
        self.note('이 영상의 EVD = 대각화 형태')
    def scene_2(self):
        self.title('조건 1 · 정사각행렬',BLUE)
        self.to(2)
        a,b=self.cards(mat_card([['a','b'],['c','d']],'2 × 2','ℝ² → ℝ²',GOOD),mat_card([['a','b','c'],['d','e','f']],'2 × 3','ℝ³ → ℝ²',BAD))
        self.reveal(a,b)
        self.to(5);self.note('Av = λv  ·  양변은 같은 공간에 속해야 한다',BLUE)
        self.reveal(label('첫 번째 조건 충족',x=a.get_x(),y=-2 if SHORT else -1.85,size=20,color=GOOD,width=3),label('표준 EVD 정의 불가',x=b.get_x(),y=-2 if SHORT else -1.85,size=20,color=BAD,width=3))
    def scene_3(self):
        self.title('정사각행렬 ≠ 항상 대각화 가능',BLUE)
        self.reveal(label('P = [ v₁  v₂ ]',y=2.8 if SHORT else 1.2,size=40,color=BLUE))
        self.to(4)
        axes=plane();x=vector(axes,[1.6,.2],BLUE);y=vector(axes,[-.4,1.5],GOLD)
        picture=VGroup(axes,x,y).scale(.65).move_to(pos(0,-.5) if SHORT else pos(3.1,-.4))
        self.reveal(picture,label('서로 독립인 두 방향',x=0 if SHORT else -3.3,y=1 if SHORT else -.5,size=29,color=GOLD,width=6))
        self.note('기저 구성의 개념도 · 아직 실제 고유벡터 사례는 아님')
    def scene_4(self):
        self.title('전단행렬 · 수평 방향만 고유벡터',BLUE)
        exp=VGroup(label('A',y=1.15,size=28,color=BLUE),matrix([[1,1],[0,1]],BLUE),label('Av = v → v = (t, 0), t ≠ 0',y=-1.15,size=23,color=BLUE))
        axes=plane();v=vector(axes,[1.6,0],BLUE);line=Line(axes.c2p(-2,0),axes.c2p(2,0),color=BLUE,stroke_opacity=.4)
        graph=VGroup(axes,line,v);exp,graph=self.split(exp,graph)
        self.reveal(exp,graph);self.to(1)
        self.play(Indicate(v,color=BLUE),run_time=.7)
        self.to(3)
        other=vector(axes,[0,1.3],GOLD);self.reveal(other,d=.2)
        self.play(Transform(other,vector(axes,[1.3,1.3],GOLD)),run_time=.8)
        self.note('(x, y) → (x+y, y)')
    def scene_5(self):
        self.title('두 벡터를 골라도 같은 직선',BLUE)
        axes=plane();line=Line(axes.c2p(-2,0),axes.c2p(2,0),color=BLUE,stroke_opacity=.5)
        graph=VGroup(axes,line,vector(axes,[1,0],BLUE),vector(axes,[2,0],GOLD))
        exp=lines('독립적인 방향이 두 개 필요','고유방향은 수평 하나뿐',color=BLUE);exp,graph=self.split(exp,graph)
        self.reveal(exp,graph);self.to(3)
        self.note('모든 고유벡터가 같은 직선 → 기저 구성 불가',BAD)
        self.to(5);self.play(FadeOut(exp),run_time=.2)
        det=VGroup(label('P',y=1.1,size=27,color=BLUE),matrix([[1,2],[0,0]],BLUE),label('det P = 0',y=-1.1,size=29,color=BAD)).move_to(exp)
        self.reveal(det);self.reveal(label('P⁻¹ 없음 · 대각화 불가능',x=0 if SHORT else 3.15,y=-3.5 if SHORT else -1.8,size=24,color=BAD,width=6))
    def scene_6(self):
        self.title('어떤 수를 허용할까?',BLUE)
        self.reveal(label('ℝ',x=-1.9,y=.9,size=85,color=BLUE),label('ℂ',x=1.9,y=.9,size=85,color=TEAL),label('실수',x=-1.9,y=-.6,size=30),label('복소수',x=1.9,y=-.6,size=30))
        self.to(2);self.note('같은 행렬 · 허용하는 수 체계를 바꿔 본다')
    def scene_7(self):
        self.title('90° 회전 · 실수 고유벡터가 있을까?',BLUE)
        exp=VGroup(label('R',y=1.1,size=28,color=BLUE),matrix([[0,-1],[1,0]],BLUE),label('0이 아닌 벡터만 고려',y=-1.1,size=23,color=MUTED))
        axes=plane();vs=VGroup(*[vector(axes,v,c) for v,c in [([1.5,0],BLUE),([.9,1.1],TEAL),([-1,.4],GOLD)]])
        ghosts=vs.copy().set_opacity(.2);graph=VGroup(axes,ghosts,vs);exp,graph=self.split(exp,graph)
        self.reveal(exp,graph);self.to(2)
        self.play(*[Rotate(v,angle=PI/2,about_point=axes.c2p(0,0)) for v in vs],run_time=3)
        self.to(6);self.note('실수 고유벡터 없음',BAD)
    def scene_8(self):
        self.title('복소수에서는 대각화 가능',TEAL)
        eq=label('det(R − λI) = λ² + 1 = 0',y=3.3 if SHORT else 1.15,size=31,color=BLUE)
        self.reveal(eq);self.to(1.5)
        self.reveal(label('λ₁ = i       λ₂ = −i',y=2 if SHORT else .2,size=37,color=TEAL))
        self.to(3)
        vecs=VGroup(label('v₁ = (1, −i)ᵀ',y=.55,size=31,color=BLUE),label('v₂ = (1, i)ᵀ',y=-.55,size=31,color=TEAL)).move_to(pos(0,-.1) if SHORT else pos(-3.2,-1.15))
        self.reveal(vecs);self.to(6)
        self.reveal(label('P = [v₁ v₂]',x=0 if SHORT else 3.2,y=-1.9 if SHORT else -.9,size=31,color=TEAL),label('det P = 2i ≠ 0  ✓',x=0 if SHORT else 3.2,y=-3 if SHORT else -1.7,size=28,color=GOOD))
        self.note('복소 벡터공간의 두 독립적인 고유벡터')
    def scene_9(self):
        self.title('같은 행렬 · 다른 수 체계')
        a,b=self.cards(mat_card([[0,-1],[1,0]],'실수 EVD','대각화 불가능',BAD),mat_card([[0,-1],[1,0]],'복소수 EVD','대각화 가능',GOOD))
        self.reveal(a,b);self.note('행렬은 그대로 · 허용하는 수만 다르다')
    def scene_10(self):
        self.title('그렇다면 SVD는?',TEAL)
        formula=label('A = UΣVᵀ',y=2.7 if SHORT else 1.15,size=51,color=TEAL);self.reveal(formula)
        self.to(2)
        mat=matrix([[1,2],[2,0]],TEAL).move_to(pos(0,-.2));self.reveal(mat)
        self.to(5);self.play(Transform(mat,matrix([[1,2],[2,0],[0,1]],TEAL).move_to(mat)),run_time=.6)
        self.note('정사각행렬 ✓   직사각행렬 ✓',GOOD)
    def scene_11(self):
        self.title('행렬의 열 = 입력 좌표축의 도착점',TEAL)
        mat=matrix([[1,2],[2,0],[0,1]],WHITE)
        exp=VGroup(label('A · 3 × 2',y=1.6,size=28,color=TEAL),mat,label('A = [a₁ a₂]',y=-1.6,size=28))
        mappings=VGroup(label('Ae₁ = a₁ = (1, 2, 0)ᵀ',y=.7,size=27,color=BLUE),label('Ae₂ = a₂ = (2, 0, 1)ᵀ',y=-.7,size=27,color=TEAL))
        exp,mappings=self.split(exp,mappings);self.reveal(exp);self.to(1)
        self.reveal(mappings[0]);self.play(*[m.animate.set_color(BLUE) for row in mat.entries for m in [row[0]]],run_time=.3)
        self.to(3);self.reveal(mappings[1]);self.play(*[m.animate.set_color(TEAL) for row in mat.entries for m in [row[1]]],run_time=.3)
        self.to(5);self.note('입력 ℝ² → 출력 ℝ³ · 열벡터는 3차원')
    def scene_12(self):
        self.title('전치행렬 × 원래 행렬',TEAL)
        product=VGroup(matrix([[1,2,0],[2,0,1]],WHITE).scale(.8).move_to(pos(-1.7,0)),label('×',size=30,color=GOLD),matrix([[1,2],[2,0],[0,1]],WHITE).scale(.8).move_to(pos(1.65,0)))
        product,g=self.split(product,gram([['□','□'],['□','□']]))
        self.reveal(product);self.to(1.2);self.reveal(g)
        self.note('2×3  ×  3×2  →  2×2',TEAL)
    def scene_13(self):
        mat=self.study('각 원소는 열벡터의 내적',lines('대각: 자기 자신과의 내적','비대각: 두 열벡터의 내적'),[['a₁ᵀa₁','a₁ᵀa₂'],['a₂ᵀa₁','a₂ᵀa₂']])
        # Longer symbolic entries need wider cells than the numeric matrix.
        for i in range(2):
            for j in range(2):mat.entries[i][j].scale(.7)
        self.to(2);self.play(*[Indicate(mat.entries[i][i],color=BLUE) for i in range(2)],run_time=.5)
        self.note('아직 계산값 대신, 각 칸의 구조를 본다')
    def scene_14(self):
        mat=self.study('대각 원소 = 열벡터의 길이 제곱',lines('a₁ᵀa₁ = 1²+2²+0² = 5','a₂ᵀa₂ = 2²+0²+1² = 5',color=BLUE),[['□','□'],['□','□']])
        self.to(.9);self.fill(mat,0,0,5,BLUE)
        self.to(1.9);self.fill(mat,1,1,5,BLUE)
        self.note('각 입력 좌표축의 출력 길이²',BLUE)
    def scene_15(self):
        mat=self.study('비대각 원소 = 두 열벡터의 내적',lines('a₁ᵀa₂ = 1·2+2·0+0·1','             = 2',color=TEAL),[[5,'□'],['□',5]])
        self.to(1);self.fill(mat,0,1,2,TEAL)
        self.to(2);self.fill(mat,1,0,2,TEAL)
        self.note('a₁ᵀa₂ = a₂ᵀa₁',TEAL)
    def scene_16(self):
        exp=lines('대각: ‖Aeᵢ‖²','변환된 좌표축의 길이 제곱','비대각: (Aeᵢ)ᵀ(Aeⱼ)','변환된 축들의 내적')
        mat=self.study('변환의 길이·내적 정보',exp,[[5,2],[2,5]])
        self.to(1);self.play(*[Circumscribe(mat.entries[i][i],color=BLUE) for i in range(2)],run_time=.6)
        self.to(3);self.play(*[Circumscribe(mat.entries[i][1-i],color=TEAL) for i in range(2)],run_time=.6)
        self.to(5);self.note('임의의 입력 x: ‖Ax‖² = xᵀAᵀAx',GOLD)
    def scene_17(self):
        mat=self.study('내적의 대칭성 → 대칭행렬',lines('a₁ᵀa₂ = a₂ᵀa₁','(AᵀA)ᵀ = AᵀA',color=TEAL),[[5,2],[2,5]])
        diagonal=DashedLine(mat.entries[0][0].get_center()+pos(-.4,.4),mat.entries[1][1].get_center()+pos(.4,-.4),color=MUTED)
        self.reveal(diagonal,d=.2);self.to(1.5)
        self.play(*[Circumscribe(mat.entries[i][1-i],color=GOLD) for i in range(2)],run_time=.6)
        self.note('SYMMETRIC MATRIX',TEAL)
    def ortho_graph(self,axes,directions):
        a,b=directions
        vs=VGroup(vector(axes,a*1.6,TEAL),vector(axes,b*1.6,GOLD))
        corner=VMobject(color=WHITE,stroke_width=2).set_points_as_corners([axes.c2p(*(.22*a)),axes.c2p(*(.22*(a+b))),axes.c2p(*(.22*b))])
        return VGroup(axes,vs,corner)
    def scene_18(self):
        self.title('대칭행렬 → 직교 고유기저',TEAL)
        exp=lines('AᵀA = [ 5  2 ; 2  5 ]','v₁ = (1, 1)ᵀ / √2','v₂ = (1, −1)ᵀ / √2',color=TEAL)
        axes=plane();directions=[np.array([1.,1.])/np.sqrt(2),np.array([1.,-1.])/np.sqrt(2)]
        graph=self.ortho_graph(axes,directions);exp,graph=self.split(exp,graph)
        self.reveal(exp,graph);self.to(2)
        self.play(Indicate(graph[2],color=WHITE),run_time=.4)
        self.note('고유벡터 2개 → 직교기저 · v₁ᵀv₂ = 0',TEAL)
    def scene_19(self):
        self.title('전단행렬로 돌아가도 SVD는 가능',TEAL)
        left=VGroup(label('원본 A',y=1.15,size=26,color=BLUE),matrix([[1,1],[0,1]],BLUE),label('EVD: 고유기저 부족',y=-1.15,size=24,color=BAD))
        right=VGroup(label('이 행렬의 AᵀA',y=1.15,size=26,color=TEAL),matrix([[1,1],[1,2]],TEAL),label('SVD: 직교기저 구성 ✓',y=-1.15,size=24,color=GOOD))
        left,right=self.split(left,right);self.reveal(left,right)
        self.to(2)
        self.note('예시 전환: 직사각행렬 → 전단행렬',GOLD)
        self.to(3)
        self.play(FadeOut(right[1]),FadeOut(right[2]),run_time=.2)
        axes=plane();_,v=np.linalg.eigh(S.T@S)
        graph=self.ortho_graph(axes,[v[:,1],v[:,0]]).scale(.55).move_to(right[1])
        self.reveal(graph);self.reveal(label('SVD ✓',x=0 if SHORT else 3.15,y=-3.5 if SHORT else -1.8,size=28,color=GOOD))
    def scene_20(self):
        self.title('모든 실수 행렬에 SVD 존재',TEAL)
        self.reveal(label('A = UΣVᵀ',y=2 if SHORT else 1,size=58,color=TEAL),label('2×2 ✓   3×2 ✓\n전단행렬 ✓   회전행렬 ✓',y=-.4 if SHORT else -.7,size=28,color=GOOD))
        self.note('랭크가 부족한 행렬도 포함')
    def scene_21(self):
        self.title('ROUND 02 · 분해 조건',GOLD)
        pair=self.pair().move_to(pos(0,1 if SHORT else .2));self.reveal(pair)
        self.to(3)
        crown=Polygon(pos(-2.75,-1.05),pos(-2.65,-1.6),pos(-1.95,-1.6),pos(-1.85,-1.05),pos(-2.1,-1.25),pos(-2.3,-.9),pos(-2.5,-1.25),color=GOLD,fill_color=GOLD,fill_opacity=.85,stroke_width=1.5)
        self.reveal(label('SVD 승!',y=-1.3,size=57,color=TEAL),crown,d=.2)
        self.play(Circumscribe(pair[2],color=TEAL),run_time=.5)
        self.to(4);self.note('직사각행렬 ✓  대각화 불가능 행렬 ✓  회전행렬 ✓',GOOD)
    def scene_22(self):
        self.title('ROUND 02 WINNER · SVD',TEAL)
        self.reveal(label('현재 스코어',y=2.6 if SHORT else 1.25,size=28,color=MUTED))
        score=label('EVD   1 : 0   SVD',y=.6 if SHORT else 0,size=45);self.reveal(score)
        self.to(2)
        self.play(Transform(score,label('EVD   1 : 1   SVD',y=.6 if SHORT else 0,size=45,color=GOLD)),Transform(self.score,label('EVD  1 : 1  SVD',x=0 if SHORT else 5.1,y=5.13 if SHORT else 2.98,size=15,color=MUTED,width=3)),run_time=.5)
        self.to(4);self.reveal(label('동점!',y=-1.8 if SHORT else -1.5,size=54,color=TEAL),d=.2)
