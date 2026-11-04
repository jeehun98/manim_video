"""Actual matrix maps, fixed scales and distinct input/output coordinate planes."""
import sys,json,textwrap
from pathlib import Path
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT.parents[1]))
from manim import *
from longforms.evdsvd01_names.visuals import BattleScene,label,pos,SHORT,BLUE,TEAL,WHITE,MUTED,GOLD
from longforms.evdsvd03_structure.revisions.v2_153s.visuals import arr,grid
from data import A1,A2,A1_INV,A2_PLUS,XA,XB,B,XSTAR,B_OFF,PROJECTED
PURPLE='#B49AFF';ORANGE='#FFB066';LOST='#FF7688'
MANIFEST=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'));CUES=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))
def point(w,v):return w['o']+pos(*(w['s']*np.asarray(v)))
def axes(o,s,bounds):
    return VGroup(grid(o,s,bounds=bounds),Line(o+pos(bounds[0]*s,0),o+pos(bounds[1]*s,0),color=MUTED,stroke_opacity=.45,stroke_width=1.5),Line(o+pos(0,bounds[2]*s),o+pos(0,bounds[3]*s),color=MUTED,stroke_opacity=.45,stroke_width=1.5))
def world():
    o=pos(0,-.35);s=1.3 if SHORT else 1.05
    return dict(o=o,s=s,base=axes(o,s,(-2.6,2.6,-1.4,1.4)))
def mapping(w,M,color=TEAL,vector=True):
    shape=Circle(radius=w['s'],color=color,stroke_width=2.5).move_to(w['o']).apply_matrix(M,about_point=w['o'])
    dots=VGroup(*[Dot(point(w,M@np.array([np.cos(t),np.sin(t)])),radius=.025,color=color) for t in np.linspace(0,TAU,24,endpoint=False)])
    g=VGroup(shape,dots)
    if vector:g.add(arr(w['o'],M@XA,w['s'],GOLD,5))
    return g
def pairs():
    s=.85 if SHORT else .9;ci=pos(-1.85,-.35) if SHORT else pos(-3.3,-.25);co=pos(1.7,-.35) if SHORT else pos(3.3,-.25)
    wi=dict(o=ci,s=s);wo=dict(o=co,s=s)
    base=VGroup(axes(ci,s,(-1.4,1.4,-1.5,1.5)),axes(co,s,(-2.35,2.35,-1.5,1.5)),Circle(radius=s,color=BLUE,stroke_width=2).move_to(ci),Line(co+LEFT*2*s,co+RIGHT*2*s,color=TEAL,stroke_width=4),label('입력 공간',ci[0],2 if SHORT else 1.4,23,BLUE,3),label('출력 공간',co[0],2 if SHORT else 1.4,23,TEAL,3))
    return wi,wo,base
def input_points(w,selected=False):
    g=VGroup(Dot(point(w,XA),radius=.065,color=PURPLE),Dot(point(w,XB),radius=.065,color=ORANGE))
    if selected:g.add(Dot(point(w,XSTAR),radius=.075,color=GOLD))
    return g
def solution_line(w):
    x=point(w,XSTAR);return VGroup(DashedLine(x+DOWN*1.35*w['s'],x+UP*1.35*w['s'],color=TEAL,stroke_width=2),label('⋮',x[0],x[1]+1.5*w['s'],20,TEAL,.4),label('⋮',x[0],x[1]-1.5*w['s'],20,TEAL,.4))

class InverseScene(BattleScene):
    def setup(self):
        self.spec=MANIFEST[self.INDEX];self.length=self.spec['duration_seconds']
        self.add(label('MATRIX DECOMPOSITION WORLD CUP',y=6.55 if SHORT else 3.55,size=15,color=MUTED,width=7 if SHORT else 12))
        y=5.85 if SHORT else 2.98
        self.add(label('EVD',-1.35,y,29,BLUE,2),label('VS',0,y,17,MUTED,1),label('SVD',1.35,y,29,TEAL,2),Line(pos(-3.5 if SHORT else -6.5,y-.45),pos(3.5 if SHORT else 6.5,y-.45),color=MUTED,stroke_opacity=.22))
        self.score=label('EVD  3 : 3  SVD',x=0 if SHORT else 5.1,y=5.13 if SHORT else 2.98,size=15,color=MUTED,width=3);self.add(self.score)
        self.add(label('07 / INVERSE  ·  되돌리기와 해의 선택',y=-6.65 if SHORT else -3.65,size=14,color=MUTED,width=7 if SHORT else 12))
        if 1<=self.INDEX<=24 and self.INDEX!=11:self.add(label('A₁ = diag(2, 0.5)' if self.INDEX<11 else 'A₂ = diag(2, 0)',y=3.35 if SHORT else 1.55,size=18,color=MUTED,width=6))
        self.caption=VGroup();self.caption_key=None;self.caption.add_updater(lambda m,dt:self.update_caption());self.add(self.caption);self.update_caption()
    def update_caption(self):
        t=self.spec['start']+self.time+1e-6;cue=next((c for c in CUES if c['start']<=t<c['end']),None);key=cue['start'] if cue else None
        if key==self.caption_key:return
        self.caption_key=key;self.caption.remove(*list(self.caption))
        if cue:
            txt=label('\n'.join(textwrap.wrap(cue['caption'],27 if SHORT else 52,break_long_words=False)),y=-5.7 if SHORT else -2.98,size=22 if SHORT else 23,width=7.1 if SHORT else 12.5)
            bg=RoundedRectangle(width=7.45 if SHORT else 13,height=max(.65,txt.height+.25),corner_radius=.08,stroke_width=0,fill_color='#080F21',fill_opacity=.97).move_to(txt)
            self.caption.add(bg,txt).set_z_index(100)
    def heading(self,s,color=WHITE):
        m=label(s,y=4.25 if SHORT else 2.08,size=32,color=color,width=7 if SHORT else 12);self.add(m);return m
    def note(self,s,color=MUTED):
        m=label(s,y=-4.15 if SHORT else -2.2,size=21,color=color,width=7 if SHORT else 12);self.reveal(m,d=.2);return m
    def formula(self,parts,y=.6,color=BLUE):
        g=VGroup(*[label(s,size=42,color=color) for s in parts]).arrange(RIGHT,buff=.22).move_to(pos(0,y))
        if g.width>(7 if SHORT else 12):g.scale_to_fit_width(7 if SHORT else 12)
        self.reveal(g);return g
    def pairs(self,points=True,selected=False):
        wi,wo,base=pairs();self.add(base,Dot(point(wo,B),radius=.07,color=TEAL))
        if points:self.add(input_points(wi,selected))
        return wi,wo
    def scene_0(self):
        t=label('행렬 분해\n이상형 월드컵!',y=2.4 if SHORT else 1.2,size=40);self.reveal(t);self.to(1)
        self.reveal(self.pair().move_to(pos(0,-.7)),d=.4);self.to(3);self.play(FadeOut(t),run_time=.2)
        self.reveal(label('ROUND 07 · 역변환',y=2.8 if SHORT else 1.3,size=32,color=GOLD))
    def scene_1(self):
        self.heading('좌표평면 위의 단위원',BLUE);w=world();self.add(w['base'])
        self.play(Create(Circle(radius=w['s'],color=BLUE).move_to(w['o'])),run_time=1.8);self.note('x₁² + x₂² = 1',BLUE)
    def scene_2(self):
        self.heading('A₁을 적용하면 원 → 타원',TEAL);w=world();self.add(w['base']);moving=mapping(w,np.eye(2),BLUE);self.add(moving)
        self.to(1);self.play(UpdateFromAlphaFunc(moving,lambda m,t:m.become(mapping(w,(1-t)*np.eye(2)+t*A1,TEAL))),run_time=2)
        self.note('가로 ×2  ·  세로 ×0.5  ·  축척 고정',TEAL)
    def scene_3(self):
        self.heading('타원을 다시 원으로?',GOLD);w=world();self.add(w['base']);moving=mapping(w,A1);self.add(moving)
        self.to(2);self.reveal(label('A₁⁻¹',x=2.4 if SHORT else 4.2,y=2 if SHORT else .8,size=36,color=BLUE,width=2))
        self.to(3.5);self.play(UpdateFromAlphaFunc(moving,lambda m,t:m.become(mapping(w,((1-t)*np.eye(2)+t*A1_INV)@A1,BLUE))),run_time=1.8)
        self.note('A₁⁻¹ A₁ x = x',BLUE)
    def scene_4(self):
        self.heading('EVD · 대각화 가능한 행렬',BLUE);self.to(2);g=self.formula(['A =','P','D','P⁻¹'])
        for i in [3,2,1]:self.play(Indicate(g[i],color=GOLD),run_time=.6)
        self.note('벡터에 적용: P⁻¹ → D → P  (오른쪽부터)',GOLD)
    def scene_5(self):
        self.heading('모든 고윳값이 0이 아니라면',BLUE)
        a=label('2',x=-1.6,y=.7,size=65,color=BLUE);b=label('0.5',x=1.6,y=.7,size=65,color=PURPLE);self.add(a,b)
        self.add(label('수평 고유방향',-1.6,2 if SHORT else 1.2,22,BLUE,3),label('수직 고유방향',1.6,2 if SHORT else 1.2,22,PURPLE,3))
        self.to(2);self.play(Transform(a,label('0.5',-1.6,.7,65,BLUE,3)),Transform(b,label('2',1.6,.7,65,PURPLE,3)),run_time=1.5)
        self.note('각 배율을 역수로  ·  확대 ↔ 축소',GOLD)
    def scene_6(self):
        self.heading('고윳값의 역수로 역행렬 조립',BLUE);g=self.formula(['A⁻¹ =','P','D⁻¹','P⁻¹'])
        self.to(2)
        for i in [3,2,1]:self.play(Indicate(g[i],color=GOLD),run_time=.6)
        self.note('작용 순서: P⁻¹ → D⁻¹ → P',GOLD)
    def scene_7(self):
        self.heading('고유방향의 확대·축소를 되돌림',BLUE);w=world();self.add(w['base'])
        h=arr(w['o'],[2,0],w['s'],BLUE,6);v=arr(w['o'],[0,.5],w['s'],PURPLE,6);self.add(h,v)
        self.to(1);self.play(Transform(h,arr(w['o'],[1,0],w['s'],BLUE,6)),Transform(v,arr(w['o'],[0,1],w['s'],PURPLE,6)),run_time=1.8)
        self.note('수평 ×0.5   /   수직 ×2',GOLD)
    def scene_8(self):
        self.heading('SVD · 입력과 출력의 직교기저',TEAL);self.to(2);g=self.formula(['A =','U','Σ','Vᵀ'],color=TEAL)
        for i in [3,2,1]:self.play(Indicate(g[i],color=GOLD),run_time=.7)
        self.note('Vᵀ: 입력 성분  →  Σ: 배율  →  U: 출력 조합')
    def scene_9(self):
        self.heading('정사각행렬 · 모든 특이값 > 0',TEAL)
        self.formula(['A =','U','Σ','Vᵀ'],y=1 if SHORT else .7,color=TEAL)
        self.to(3);inv=self.formula(['A⁻¹ =','V','Σ⁻¹','Uᵀ'],y=-.7,color=TEAL)
        self.to(5);self.play(Indicate(inv[1],color=GOLD),Indicate(inv[3],color=GOLD),run_time=.7)
        self.note('U, V의 역할을 교환  ·  2 → 0.5,  0.5 → 2',GOLD)
    def scene_10(self):
        self.heading('이 가역 예시에서는 둘 다 가능',GOLD)
        self.reveal(label('EVD ✓',-1.85 if SHORT else -3.2,.4,43,BLUE,3.5),label('SVD ✓',1.85 if SHORT else 3.2,.4,43,TEAL,3.5))
        self.note('A₁은 대각화 가능하고 역행렬이 존재한다')
    def scene_11(self):
        self.heading('이번에는 다른 행렬로 교체',GOLD);old=label('A₁ = diag(2, 0.5)',y=.7,size=42,color=BLUE);self.add(old)
        self.to(1);self.play(Transform(old,label('A₂ = diag(2, 0)',y=.7,size=42,color=LOST)),run_time=1)
        self.note('수직 배율 0.5 → 0  ·  변환 규칙이 바뀐다',LOST)
    def scene_12(self):
        self.heading('원을 완전히 눌러 버린다면?',LOST);w=world();self.add(w['base']);shape=mapping(w,np.eye(2),BLUE,False);self.add(shape)
        self.play(UpdateFromAlphaFunc(shape,lambda m,t:m.become(mapping(w,(1-t)*np.eye(2)+t*A2,TEAL,False))),run_time=3.7)
        self.note('출력은 수평 선분 [−2, 2]  ·  (x,y) → (2x,0)',TEAL)
    def scene_13(self):
        self.heading('다른 두 입력이 같은 출력으로',LOST);wi,wo,base=pairs();self.add(base)
        p=Dot(point(wi,XA),radius=.07,color=PURPLE);q=Dot(point(wi,XB),radius=.07,color=ORANGE);self.add(p,q)
        self.to(.7);self.play(p.animate.move_to(point(wo,B)),q.animate.move_to(point(wo,B)),run_time=1.4)
        self.play(FadeOut(p),FadeOut(q),FadeIn(Dot(point(wo,B),radius=.08,color=TEAL)),run_time=.3)
        self.note('(0.6, 0.8), (0.6, −0.8) → (1.2, 0)',GOLD)
    def scene_14(self):
        self.heading('출력 하나로 원래 점을 알 수 없다',LOST);wi,wo=self.pairs()
        self.to(1);self.reveal(solution_line(wi));self.note('가능한 입력: (0.6, t),  t ∈ ℝ  ·  무수히 많다',GOLD)
    def scene_15(self):
        self.heading('수직 방향의 정보가 사라졌다',LOST);w=world();self.add(w['base'])
        h=arr(w['o'],[1,0],w['s'],BLUE,6);v=arr(w['o'],[0,1],w['s'],LOST,6);self.add(h,v)
        self.play(Transform(h,arr(w['o'],[2,0],w['s'],TEAL,6)),Transform(v,Dot(w['o'],radius=.06,color=LOST)),run_time=1.7)
        self.note('수평 성분은 남고 · 수직 성분은 0',LOST)
    def scene_16(self):
        self.heading('일대일이 아니므로 역행렬 없음',LOST);wi,wo=self.pairs();self.add(solution_line(wi))
        self.note('det(A₂) = 0  ·  출력만으로 원래 입력을 구별할 수 없다',LOST)
    def scene_17(self):
        self.heading('그렇다면 무엇을 알 수 있을까?',GOLD);wi,wo=self.pairs(points=False)
        self.to(2);self.reveal(solution_line(wi));self.note('가능한 입력의 집합을 찾을 수 있다',GOLD)
    def null_directions(self,animate=True):
        w=world();self.add(w['base']);h=arr(w['o'],[1,0],w['s'],BLUE,6);v=arr(w['o'],[0,1],w['s'],LOST,6);self.add(h,v)
        if animate:
            self.play(Transform(h,arr(w['o'],[2,0],w['s'],TEAL,6)),run_time=1.3)
            self.play(Transform(v,Dot(w['o'],radius=.07,color=LOST)),run_time=1.3)
        self.add(label('σ₁ = 2',x=2.3 if SHORT else 3.5,y=.4,size=28,color=TEAL,width=2.5),label('σ₂ = 0',x=-2.3 if SHORT else -3.5,y=.4,size=28,color=LOST,width=2.5))
    def scene_18(self):
        self.heading('특이값이 정보 소실 방향을 구분',TEAL);self.to(3);self.null_directions();self.note('σ = 0인 입력 방향이 영공간에 속한다',LOST)
    def scene_19(self):
        self.heading('0이 아닌 특이값만 역수로',TEAL)
        first=label('Σ = diag(2, 0)',y=1.2 if SHORT else .8,size=40,color=TEAL);self.add(first)
        self.to(2);self.reveal(label('Σ⁺ = diag(0.5, 0)',y=-.1,size=40,color=GOLD))
        self.to(4);self.reveal(label('A₂⁺ = V Σ⁺ Uᵀ',y=-1.3,size=34,color=TEAL));self.note('의사역행렬  ·  0은 역수를 취하지 않고 0으로 유지',GOLD)
    def scene_20(self):
        self.heading('원래 정보를 되살리는 것은 아니다',GOLD);wi,wo=self.pairs();self.to(.7)
        self.reveal(Dot(point(wi,XSTAR),radius=.085,color=GOLD));self.note('A₂⁺b = (0.6, 0)  ·  처음의 두 입력과 다르다',GOLD)
    def scene_21(self):
        self.heading('가능한 입력 중 최소 노름 선택',GOLD);wi,wo=self.pairs();self.to(2);self.reveal(solution_line(wi))
        vectors=VGroup(arr(wi['o'],XA,wi['s'],PURPLE,4),arr(wi['o'],XB,wi['s'],ORANGE,4));self.to(4);self.reveal(vectors)
        self.to(6);self.reveal(arr(wi['o'],XSTAR,wi['s'],GOLD,6),Dot(point(wi,XSTAR),radius=.085,color=GOLD))
        self.note('정확한 해가 여러 개: ‖(0.6,t)‖² = 0.36 + t²',GOLD)
    def scene_22(self):
        self.heading('연립방정식 Ax = b로 연결',TEAL);wi,wo=self.pairs(points=False);self.add(solution_line(wi),Dot(point(wi,XSTAR),radius=.08,color=GOLD))
        self.to(2);off=Dot(point(wo,B_OFF),radius=.07,color=ORANGE);self.reveal(off)
        self.reveal(DashedLine(point(wo,B_OFF),point(wo,PROJECTED),color=ORANGE,stroke_width=3))
        self.reveal(label('별도 출력 b′',x=2.2 if SHORT else 4.4,y=1.1 if SHORT else .9,size=19,color=ORANGE,width=2.7))
        self.note('b: 정확한 해 여러 개  /  b′: 최소제곱 잔차 0.8',GOLD)
    def scene_23(self):
        self.heading('의사역행렬 계산법은 하나가 아니다',GOLD)
        self.reveal(label('SVD',-1.85 if SHORT else -3.5,.5,42,TEAL,3),label('AᵀA의 고유분해',1.85 if SHORT else 3.5,.5,26,BLUE,3.5 if SHORT else 5))
        self.note('서로 다른 계산 경로  →  같은 Moore–Penrose 의사역행렬')
    def scene_24(self):
        self.heading('남아 있는 방향 · 사라진 방향',TEAL);self.null_directions();self.note('모든 실수 행렬에 SVD 존재  ·  직사각행렬도 가능',GOLD)
    def scene_25(self):
        self.heading('ROUND 07 · 역변환',GOLD);pair=self.pair().move_to(pos(0,1 if SHORT else .1));self.reveal(pair)
        self.to(2);self.reveal(label('SVD 승!',y=-1.3 if SHORT else -1.45,size=53 if SHORT else 46,color=TEAL),d=.2)
        self.play(Circumscribe(pair[2],color=TEAL),run_time=.6);self.to(4);self.note('의사역행렬: 최소제곱 해 중 최소 노름 해',GOLD)
    def scene_26(self):
        self.heading('ROUND 07 WINNER · SVD',TEAL);score=label('EVD   3 : 3   SVD',y=.6 if SHORT else 0,size=45);self.add(score)
        self.to(2);self.play(Transform(score,label('EVD   3 : 4   SVD',y=.6 if SHORT else 0,size=45,color=GOLD)),Transform(self.score,label('EVD  3 : 4  SVD',x=0 if SHORT else 5.1,y=5.13 if SHORT else 2.98,size=15,color=MUTED,width=3)),run_time=.6)
        self.to(4);self.reveal(label('SVD가 앞서갑니다!',y=-1.8 if SHORT else -1.5,size=37,color=TEAL),d=.3)
