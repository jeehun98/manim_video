"""Episode 02: exact matrices, actual eigendirections, and two native layouts."""
import sys,json,textwrap
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parents[1]))
from manim import *
from longforms.evdsvd01_names.visuals import (
    BattleScene,label,pos,card,SHORT,BLUE,TEAL,WHITE,MUTED,GOLD,PANEL,
)
MANIFEST=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
CUES=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))
GOOD='#77E2A2';BAD='#FF8299'
SHEAR=np.array([[1.,1.],[0.,1.]])
ROTATION=np.array([[0.,-1.],[1.,0.]])
GRAM=SHEAR.T@SHEAR
EVALS,EVECS=np.linalg.eigh(GRAM)

def matrix(values,color=WHITE,cell=.65,size=29):
    n=len(values);k=len(values[0]);g=VGroup();entries=[]
    for i,row in enumerate(values):
        entries.append([])
        for j,value in enumerate(row):
            m=label(str(value),(j-(k-1)/2)*cell,((n-1)/2-i)*cell,size,color,cell*.9)
            entries[-1].append(m);g.add(m)
    h=n*cell/2;w=k*cell/2+.12
    for sign in [-1,1]:
        g.add(VMobject(color=color,stroke_width=2).set_points_as_corners([pos(sign*(w-.15),h),pos(sign*w,h),pos(sign*w,-h),pos(sign*(w-.15),-h)]))
    g.entries=entries
    return g

def mat_card(values,name,sub='',color=WHITE,width=3):
    m=matrix(values,color).move_to(pos(0,.25))
    return VGroup(RoundedRectangle(width=width,height=2.85,corner_radius=.16,stroke_color=color,stroke_opacity=.65,fill_color=PANEL,fill_opacity=1),label(name,y=1.05,size=20,color=color,width=width-.2),m,label(sub,y=-1.03,size=18,color=MUTED,width=width-.2))

def plane():
    return NumberPlane(x_range=[-2.4,2.4,1],y_range=[-2,2,1],x_length=4.8,y_length=4,background_line_style={'stroke_color':MUTED,'stroke_opacity':.16},axis_config={'stroke_width':1,'stroke_opacity':.4})

def vector(axes,v,color=BLUE):
    return Arrow(axes.c2p(0,0),axes.c2p(*v),buff=0,color=color,stroke_width=5,max_tip_length_to_length_ratio=.17)

class ConditionsScene(BattleScene):
    def setup(self):
        self.spec=MANIFEST[self.INDEX];self.length=self.spec['duration_seconds']
        self.add(label('MATRIX DECOMPOSITION WORLD CUP',y=6.55 if SHORT else 3.55,size=15,color=MUTED,width=7 if SHORT else 12))
        y=5.85 if SHORT else 2.98
        self.add(label('EVD',-1.35,y,29,BLUE,2),label('VS',0,y,17,MUTED,1),label('SVD',1.35,y,29,TEAL,2))
        self.add(Line(pos(-3.5 if SHORT else -6.5,y-.45),pos(3.5 if SHORT else 6.5,y-.45),color=MUTED,stroke_opacity=.25))
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
        m=label(s,y=-4.35 if SHORT else -2.17,size=22,color=color,width=7 if SHORT else 12)
        self.reveal(m,d=.25);return m
    def cards(self,a,b):
        if SHORT:
            a.move_to(pos(-1.8,.3));b.move_to(pos(1.8,.3))
        else:
            a.move_to(pos(-2.35,-.1));b.move_to(pos(2.35,-.1))
        return a,b
    def scene_0(self):
        self.reveal(label('행렬 분해\n이상형 월드컵!',y=2.3 if SHORT else 1.25,size=40))
        self.to(1);self.reveal(self.pair().move_to(pos(0,-.6)),d=.45)
    def scene_1(self):
        self.reveal(label('ROUND 02',y=2 if SHORT else 1.6,size=23,color=GOLD),label('분해 조건',y=.5,size=55),label('어떤 행렬까지 분해할 수 있을까?',y=-.8,size=27))
        self.reveal(label('2 × 2     /     2 × 3     /     고유벡터 부족',y=-2.1,size=23,color=MUTED))
    def scene_2(self):
        self.title('EVD · 고유값 분해',BLUE)
        formula=label('A = PDP⁻¹',y=1.6 if SHORT else .8,size=57,color=BLUE);self.reveal(formula)
        detail=label('P: 고유벡터 기저     D: 고윳값',y=0 if SHORT else -.35,size=23,color=MUTED);self.reveal(detail)
        self.to(2);self.reveal(label('모든 행렬에 적용 가능?',y=-2 if SHORT else -1.3,size=35,color=GOLD))
        self.note('이 영상의 EVD = 대각화 형태')
    def scene_3(self):
        self.title('조건 1 · 정사각행렬',BLUE)
        a,b=self.cards(mat_card([['a','b'],['c','d']],'2 × 2','형태 조건 통과',GOOD),mat_card([['a','b','c'],['d','e','f']],'2 × 3','일반적 EVD 불가',BAD))
        self.reveal(a,b);self.note('정사각형이라고 대각화가 보장되지는 않는다')
    def scene_4(self):
        self.title('Av와 λv는 같은 공간에 있어야 한다',BLUE)
        explanation=VGroup(label('Av = λv',y=.8,size=48,color=BLUE),label('v ≠ 0',y=-.25,size=24,color=MUTED),label('A: 2 × 2   /   v: 2차원',y=-1.2,size=25))
        axes=plane();v=vector(axes,[.6,.6]);ghost=v.copy().set_opacity(.3)
        line=Line(axes.c2p(-1.5,-1.5),axes.c2p(1.8,1.8),color=BLUE,stroke_opacity=.35)
        graph=VGroup(axes,line,ghost,v);explanation,graph=self.split(explanation,graph)
        self.reveal(explanation,graph);self.to(1.5)
        self.play(Transform(v,vector(axes,[1.8,1.8])),run_time=1.5)
        self.to(5)
        self.play(FadeOut(explanation),FadeOut(graph),run_time=.3)
        mismatch=VGroup(label('A: 2 × 3',y=2 if SHORT else 1,size=33,color=GOLD),label('v ∈ ℝ³   →   Av ∈ ℝ²',y=.5 if SHORT else 0,size=35,color=BLUE),label('Av   ≠   λv',y=-1,size=47,color=BAD),label('2차원             3차원',y=-2.15 if SHORT else -1.65,size=25,color=MUTED))
        self.reveal(mismatch);self.note('표준 고유값 문제에서는 입력·출력 공간이 같아야 한다')
    def scene_5(self):
        self.title('정사각행렬만으로는 부족하다',BLUE)
        self.reveal(label('P = [ v₁  v₂ ]',y=2 if SHORT else 1,size=46,color=BLUE),label('P⁻¹이 존재하려면?',y=.6 if SHORT else -.1,size=28))
        self.to(4)
        self.reveal(label('조건 2 · 선형독립인 고유벡터',y=-.9 if SHORT else -1.15,size=30,color=GOLD),label('n × n 행렬 → 독립적인 고유벡터 n개',y=-2.3 if SHORT else -1.75,size=26,color=BLUE))
        self.note('고유벡터들로 기저를 만들 수 있어야 한다')
    def scene_6(self):
        self.title('고윳값 두 개 ≠ 독립 방향 두 개',BLUE)
        mat=matrix([[1,1],[0,1]],BLUE)
        explanation=VGroup(label('전단행렬 A',y=1.2,size=23,color=MUTED),mat,label('(λ − 1)² = 0',y=-1.2,size=30,color=BLUE))
        axes=plane();line=Line(axes.c2p(-2.1,0),axes.c2p(2.1,0),color=BLUE,stroke_width=4)
        v=vector(axes,[1,0])
        graph=VGroup(axes,line,v);explanation,graph=self.split(explanation,graph)
        self.reveal(explanation,graph);self.to(1)
        self.play(Transform(explanation[0],label('λ₁ = λ₂ = 1',explanation[0].get_x(),explanation[0].get_y(),27,GOLD)),run_time=.35)
        self.to(4);self.reveal(vector(axes,[2,0],GOLD))
        self.reveal(label('고유공간: v = (t, 0),  t ≠ 0',x=0 if SHORT else -3.5,y=-4.35 if SHORT else -2.17,size=22,color=BLUE,width=7 if SHORT else 5.6),d=.25)
        self.to(6)
        result=label('P의 두 열이 종속 → P⁻¹ 없음',x=0 if SHORT else 3.1,y=-3.4 if SHORT else -2.17,size=23,color=BAD,width=7 if SHORT else 5.6)
        self.reveal(result)
        self.to(9);self.play(Indicate(line,color=BAD),run_time=.6)
    def scene_7(self):
        self.title('조건 3 · 어떤 수 체계인가?',BLUE)
        self.reveal(label('ℝ',x=-1.9,y=.7,size=85,color=BLUE),label('ℂ',x=1.9,y=.7,size=85,color=TEAL),label('실수',x=-1.9,y=-.65,size=30),label('복소수',x=1.9,y=-.65,size=30),Arrow(pos(-.6,.7),pos(.6,.7),color=MUTED,buff=.05))
        self.note('허용하는 수에 따라 대각화 가능 여부가 달라진다')
    def scene_8(self):
        self.title('90° 회전 · 자기 직선을 떠난다',BLUE)
        explanation=VGroup(label('R',y=1.2,size=28,color=BLUE),matrix([[0,-1],[1,0]],BLUE),label('길이는 그대로, 방향은 회전',y=-1.2,size=24,color=MUTED))
        axes=plane();v=vector(axes,[1.5,0]);old=v.copy().set_color(MUTED).set_opacity(.4)
        graph=VGroup(axes,old,v);explanation,graph=self.split(explanation,graph)
        self.reveal(explanation,graph);self.to(.9)
        self.play(Rotate(v,angle=PI/2,about_point=axes.c2p(0,0)),run_time=1.5)
        self.note('0이 아닌 어떤 실수 벡터도 같은 직선에 남지 않는다')
    def scene_9(self):
        self.title('실수에서는 불가능, 복소수에서는 가능',BLUE)
        self.reveal(label('det(R − λI) = λ² + 1 = 0',y=2.6 if SHORT else 1.2,size=34,color=BLUE))
        self.to(1.4);self.reveal(label('λ₁ = i       λ₂ = −i',y=1 if SHORT else .1,size=41,color=TEAL))
        self.to(3)
        self.reveal(label('실수 대각화  ×',x=0 if SHORT else -3.4,y=-.7 if SHORT else -1.1,size=31,color=BAD),label('복소수 대각화  ✓',x=0 if SHORT else 3.4,y=-2 if SHORT else -1.1,size=31,color=GOOD))
        self.note('복소 고유벡터는 복소 벡터공간에 존재')
    def scene_10(self):
        self.title('그렇다면 SVD는?',TEAL)
        self.reveal(label('SVD',y=1.6 if SHORT else .7,size=76,color=TEAL),label('A = UΣVᵀ',y=-.1 if SHORT else -.7,size=45),label('같은 행렬로 다시 심사',y=-2 if SHORT else -2,size=28,color=MUTED))
    def scene_11(self):
        self.title('정사각형도, 직사각형도 가능',TEAL)
        left=VGroup(label('B: 2 × 3',y=1.1,size=28,color=TEAL),matrix([[1,0,0],[0,2,0]],TEAL),label('B(x, y, z) = (x, 2y)',y=-1.15,size=27))
        right=VGroup(label('ℝ³  →  ℝ²',y=1.1,size=43,color=TEAL),label('x 방향 → 출력 x 방향',y=.1,size=24),label('y 방향 → 2배 확대',y=-.65,size=24),label('z 방향 → 영벡터',y=-1.4,size=25,color=GOLD))
        left,right=self.split(left,right);self.reveal(left,right)
        self.to(2.3);self.note('U₂×₂  Σ₂×₃  Vᵀ₃×₃  →  B₂×₃',TEAL)
    def scene_12(self):
        self.title('같은 행렬, SVD는 모두 통과',TEAL)
        a,b=self.cards(mat_card([[1,1],[0,1]],'전단행렬','대각화 불가능',BLUE),mat_card([[0,-1],[1,0]],'90° 회전','실수 고유벡터 없음',BLUE))
        self.reveal(a,b);self.to(1.5)
        self.reveal(label('SVD ✓',x=a.get_x(),y=-2 if SHORT else -1.72,size=31,color=GOOD),label('SVD ✓',x=b.get_x(),y=-2 if SHORT else -1.72,size=31,color=GOOD))
        self.note('행렬은 그대로 · 분해 방식이 다르다')
    def scene_13(self):
        self.title('전치행렬을 곱하면 대칭행렬',TEAL)
        original=VGroup(label('A',y=1.15,size=28,color=BLUE),matrix([[1,1],[0,1]],BLUE),label('고유기저가 부족했던 행렬',y=-1.15,size=22,color=MUTED))
        result=matrix([[1,1],[1,2]],TEAL)
        gram=VGroup(label('AᵀA',y=1.15,size=33,color=TEAL),result,label('대칭 · 양의 준정부호',y=-1.15,size=24,color=TEAL))
        original,gram=self.split(original,gram)
        self.reveal(original);self.to(2)
        product=VGroup(matrix([[1,0],[1,1]],BLUE).scale(.72).move_to(pos(-1.08,0)),label('×',size=30,color=GOLD),matrix([[1,1],[0,1]],BLUE).scale(.72).move_to(pos(1.08,0))).move_to(original[1])
        self.play(Transform(original[0],label('Aᵀ × A',original[0].get_x(),original[0].get_y(),28,GOLD)),Transform(original[1],product),Transform(original[2],label('전치행렬 × 원래 행렬',original[2].get_x(),original[2].get_y(),22,MUTED)),run_time=.35);self.to(4)
        self.reveal(gram)
        self.play(*[Circumscribe(result.entries[i][j],color=GOLD,fade_out=True) for i,j in [(0,1),(1,0)]],run_time=.8)
        self.note('(AᵀA)ᵀ = AᵀA',TEAL)
    def scene_14(self):
        self.title('대칭행렬 → 직교 고유기저',TEAL)
        explanation=VGroup(label('AᵀAvᵢ = σᵢ²vᵢ',y=.7,size=34,color=TEAL),label('실수 대칭 · 양의 준정부호',y=-.5,size=23),label('고윳값 ≥ 0',y=-1.4,size=26,color=GOLD))
        axes=plane();vs=[EVECS[:,i]*1.65 for i in [1,0]]
        a=vector(axes,vs[0],TEAL);b=vector(axes,vs[1],GOLD)
        d0=EVECS[:,1];d1=EVECS[:,0];o=axes.c2p(0,0)
        corner=VMobject(color=WHITE,stroke_width=2).set_points_as_corners([axes.c2p(*(.23*d0)),axes.c2p(*(.23*(d0+d1))),axes.c2p(*(.23*d1))])
        graph=VGroup(axes,a,b,corner);explanation,graph=self.split(explanation,graph)
        self.reveal(explanation,graph)
        self.note('실제 AᵀA의 고유벡터 · v₁ᵀv₂ = 0',TEAL)
    def scene_15(self):
        self.title('모든 실수 행렬에 존재',TEAL)
        self.reveal(label('A = UΣVᵀ',y=1.7 if SHORT else .7,size=61,color=TEAL))
        self.reveal(label('직사각행렬  ✓\n전단행렬  ✓\n90° 회전행렬  ✓',y=-1 if SHORT else -1.2,size=30,color=GOOD))
    def scene_16(self):
        self.title('ROUND 02 · 분해 조건',GOLD)
        pair=self.pair().move_to(pos(0,1 if SHORT else .1));self.reveal(pair)
        self.to(2)
        winner=label('SVD 승!',y=-1.4 if SHORT else -1.65,size=58,color=TEAL)
        self.reveal(winner,d=.25);self.play(Circumscribe(pair[2],color=TEAL,fade_out=True),run_time=.5)
        self.to(3)
        self.reveal(label('분해 가능한 행렬의 범위에서 우위',y=-3 if SHORT else -2.25,size=25,color=GOLD))
    def scene_17(self):
        self.title('ROUND 02 WINNER · SVD',TEAL)
        self.reveal(label('현재 스코어',y=2.6 if SHORT else 1.2,size=28,color=MUTED))
        score=label('EVD   1 : 0   SVD',y=.6 if SHORT else 0,size=45)
        self.reveal(score,d=.15);self.to(1.1)
        self.play(Transform(score,label('EVD   1 : 1   SVD',y=.6 if SHORT else 0,size=45,color=GOLD)),Transform(self.score,label('EVD  1 : 1  SVD',x=0 if SHORT else 5.1,y=5.13 if SHORT else 2.98,size=15,color=MUTED,width=3)),run_time=.4)
        self.to(2);self.reveal(label('동점!',y=-1.8 if SHORT else -1.5,size=54,color=TEAL),d=.25)
