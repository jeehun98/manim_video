"""Exact discrete dynamics, independent replaceable scenes, native aspect ratios."""
import sys,json,textwrap
from pathlib import Path
ROOT=Path(__file__).resolve().parent;WORK=ROOT.parents[1];sys.path.insert(0,str(WORK))
from manim import *
from longforms.evdsvd01_names.visuals import BattleScene,label,pos,SHORT,BLUE,TEAL,WHITE,MUTED,GOLD
from longforms.evdsvd03_structure.revisions.v2_153s.visuals import arr,grid
PURPLE='#B49AFF';ORANGE='#FFB066'
MANIFEST=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
CUES=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))
AE=np.diag([2.,.5]);AS=np.array([[0.,-1.],[2.,0.]])
X0=np.array([.25,1.]);TRANSIENT=np.array([[.8,2.],[0.,.7]])

def world():
    o=pos(-1.3,-.65) if SHORT else pos(-1.35,-.35);s=1.6 if SHORT else 1.35
    top=1.55 if SHORT else 1.2
    g=grid(o,s,bounds=(-.8,2.8,-.8,top))
    axes=VGroup(Line(o+pos(-.5*s,0),o+pos(2.8*s,0),color=BLUE,stroke_opacity=.55),Line(o+pos(0,-.5*s),o+pos(0,top*s),color=PURPLE,stroke_opacity=.55))
    return dict(o=o,s=s,base=VGroup(g,axes))

def state(w,x,parts=False):
    o,s=w['o'],w['s'];g=VGroup()
    if parts:g.add(arr(o,[x[0],0],s,BLUE),arr(o+pos(x[0]*s,0),[0,x[1]],s,PURPLE))
    g.add(arr(o,x,s,GOLD,6));return g

class FutureScene(BattleScene):
    def setup(self):
        self.spec=MANIFEST[self.INDEX];self.length=self.spec['duration_seconds']
        self.add(label('MATRIX DECOMPOSITION WORLD CUP',y=6.55 if SHORT else 3.55,size=15,color=MUTED,width=7 if SHORT else 12))
        y=5.85 if SHORT else 2.98
        self.add(label('EVD',-1.35,y,29,BLUE,2),label('VS',0,y,17,MUTED,1),label('SVD',1.35,y,29,TEAL,2),Line(pos(-3.5 if SHORT else -6.5,y-.45),pos(3.5 if SHORT else 6.5,y-.45),color=MUTED,stroke_opacity=.22))
        self.score=label('EVD  2 : 2  SVD',x=0 if SHORT else 5.1,y=5.13 if SHORT else 2.98,size=15,color=MUTED,width=3);self.add(self.score)
        self.add(label('05 / FUTURE  ·  반복 변환의 미래',y=-6.65 if SHORT else -3.65,size=14,color=MUTED,width=7 if SHORT else 12))
        if 1<=self.INDEX<=15:
            is_svd=12<=self.INDEX<=14
            self.add(label('예시 B · Aₛ(x,y) = (−y, 2x)' if is_svd else '예시 A · Aₑ = diag(2, 0.5)',y=3.35 if SHORT else 1.52,size=18,color=TEAL if is_svd else MUTED,width=7 if SHORT else 10))
        self.caption=VGroup();self.caption_key=None
        self.caption.add_updater(lambda m,dt:self.update_caption());self.add(self.caption);self.update_caption()
    def update_caption(self):
        t=self.spec['start']+self.time+1e-6;cue=next((c for c in CUES if c['start']<=t<c['end']),None);key=cue['start'] if cue else None
        if key==self.caption_key:return
        self.caption_key=key;self.caption.remove(*list(self.caption))
        if cue:
            words='\n'.join(textwrap.wrap(cue['caption'],27 if SHORT else 52,break_long_words=False))
            txt=label(words,y=-5.7 if SHORT else -2.98,size=22 if SHORT else 23,width=7.1 if SHORT else 12.5)
            bg=RoundedRectangle(width=7.45 if SHORT else 13,height=max(.65,txt.height+.25),corner_radius=.08,stroke_width=0,fill_color='#080F21',fill_opacity=.97).move_to(txt)
            self.caption.add(bg,txt).set_z_index(100)
    def heading(self,s,color=WHITE):
        m=label(s,y=4.25 if SHORT else 2.04,size=32,color=color,width=7 if SHORT else 12);self.add(m);return m
    def note(self,s,color=MUTED):
        m=label(s,y=-4.1 if SHORT else -2.15,size=22,color=color,width=7 if SHORT else 12);self.reveal(m,d=.2);return m
    def clock(self,n):return label(f't = {n}',x=-2.3 if SHORT else -4.3,y=2.3 if SHORT else 1.05,size=27,color=GOLD,width=2)
    def evolution(self,parts=False):
        w=world();moving=state(w,X0,parts);clock=self.clock(0);self.add(w['base'],moving,clock)
        for n in range(1,4):
            self.add(Dot(w['o']+pos(*(w['s']*(np.linalg.matrix_power(AE,n-1)@X0))),radius=.035,color=MUTED))
            x=np.linalg.matrix_power(AE,n)@X0
            self.play(Transform(moving,state(w,x,parts)),Transform(clock,self.clock(n)),run_time=.9)
        return w
    def scene_0(self):
        t=label('행렬 분해\n이상형 월드컵!',y=2.4 if SHORT else 1.2,size=40);self.reveal(t)
        self.to(1);self.reveal(self.pair().move_to(pos(0,-.7)),d=.4)
        self.to(3);self.play(FadeOut(t),run_time=.2);self.reveal(label('ROUND 05 · 미래 예측',y=2.8 if SHORT else 1.3,size=32,color=GOLD))
    def scene_1(self):
        self.heading('현재 상태를 벡터로',GOLD);w=world();self.add(w['base'],self.clock(0));self.reveal(state(w,X0),d=1)
        self.to(3);self.reveal(label('xₜ₊₁ = A xₜ',x=0 if SHORT else 3.7,y=2 if SHORT else .6,size=34,color=BLUE,width=4));self.note('같은 변화 규칙 A를 매 단계 적용')
    def scene_2(self):
        self.heading('한 번, 두 번, 계속 적용하면?',GOLD);w=world();moving=state(w,X0);clock=self.clock(0);self.add(w['base'],moving,clock)
        for n,target in [(1,0),(2,2),(3,5)]:
            self.to(target);prev=np.linalg.matrix_power(AE,n-1)@X0;self.add(Dot(w['o']+pos(*(w['s']*prev)),radius=.04,color=MUTED))
            self.play(Transform(moving,state(w,np.linalg.matrix_power(AE,n)@X0)),Transform(clock,self.clock(n)),run_time=1.3)
        self.to(8);self.note('t = 10 ?       t = 100 ?',GOLD)
    def scene_3(self):
        self.heading('두 방향 · 두 가지 변화',BLUE);w=world();clock=self.clock(0);self.add(w['base'],clock)
        h=arr(w['o'],[.25,0],w['s'],BLUE,6);v=arr(w['o'],[0,1],w['s'],PURPLE,6);self.reveal(h,v)
        self.to(3)
        for n in range(1,4):self.play(Transform(h,arr(w['o'],[.25*2**n,0],w['s'],BLUE,6)),Transform(v,arr(w['o'],[0,.5**n],w['s'],PURPLE,6)),Transform(clock,self.clock(n)),run_time=1)
        self.note('수평: 매 단계 ×2     수직: 매 단계 ×0.5')
    def scene_4(self):
        self.heading('변해도 같은 직선 위에',BLUE);w=world();self.add(w['base'])
        self.add(DashedLine(w['o']-RIGHT*.6,w['o']+RIGHT*4,color=BLUE),DashedLine(w['o']-UP*.6,w['o']+UP*2.4,color=PURPLE))
        h=arr(w['o'],[.6,0],w['s'],BLUE,6);v=arr(w['o'],[0,1],w['s'],PURPLE,6);self.reveal(h,v)
        self.play(Transform(h,arr(w['o'],[1.2,0],w['s'],BLUE,6)),Transform(v,arr(w['o'],[0,.5],w['s'],PURPLE,6)),run_time=2)
        self.to(4);self.reveal(label('고유벡터',x=0 if SHORT else 3,y=2.2 if SHORT else .7,size=35,color=BLUE))
        self.to(5);self.note('Avᵢ = λᵢvᵢ     λ₁ = 2,  λ₂ = 0.5',BLUE)
    def scene_5(self):
        self.heading('고윳값 2 → 2ⁿ',BLUE)
        o=pos(-2.9,-.25) if SHORT else pos(-4.1,-.2);s=.7 if SHORT else 1.
        self.add(Line(o-LEFT*.1,o+RIGHT*8.2*s,color=MUTED,stroke_opacity=.35))
        for k in [1,2,4,8]:self.add(label(str(k),x=o[0]+k*s,y=-.85,size=18,color=MUTED,width=1))
        moving=arr(o,[1,0],s,BLUE,6);self.add(moving)
        for target,length in [(1,2),(2,4),(3,8)]:self.to(target);self.play(Transform(moving,arr(o,[length,0],s,BLUE,6)),run_time=.65)
        self.note('1 → 2 → 4 → 8   ·   축척 고정',BLUE)
    def scene_6(self):
        self.heading('고윳값 0.5 → 0.5ⁿ',PURPLE);w=world();self.add(w['base']);v=arr(w['o'],[0,1],w['s'],PURPLE,6);self.add(v)
        for n in range(1,4):self.to(n);self.play(Transform(v,arr(w['o'],[0,.5**n],w['s'],PURPLE,6)),run_time=.6)
        self.note('1 → 0.5 → 0.25 → 0.125 → …',PURPLE)
    def scene_7(self):
        self.heading('한 벡터를 두 고유성분으로',GOLD);w=world();self.add(w['base'],state(w,X0));self.to(2)
        self.reveal(arr(w['o'],[X0[0],0],w['s'],BLUE));self.to(3)
        self.reveal(arr(w['o']+pos(X0[0]*w['s'],0),[0,X0[1]],w['s'],PURPLE));self.note('x₀ = c₁v₁ + c₂v₂',GOLD)
    def scene_8(self):
        self.heading('서로 다른 배율 · 달라지는 방향',GOLD);self.evolution(parts=True);self.note('성장하는 성분의 방향으로 가까워진다')
    def scene_9(self):
        self.heading('EVD · 성분별 변화를 표현',BLUE);w=world();self.add(w['base'],state(w,X0,True))
        self.to(3);panel=RoundedRectangle(width=6.8 if SHORT else 9,height=2.4,corner_radius=.15,stroke_color=BLUE,fill_color='#080F21',fill_opacity=.95).move_to(pos(0,.45))
        self.reveal(panel,label('A = P D P⁻¹',y=.8,size=48,color=BLUE),label('P⁻¹: 고유좌표   D: 성분별 배율   P: 조합',y=-.15,size=21,width=6.4 if SHORT else 9))
        self.note('이 예시는 P = I,  D = diag(2, 0.5)',MUTED)
    def scene_10(self):
        self.heading('반복하면 가운데가 상쇄된다',BLUE)
        tokens=VGroup(*[label(s,size=34,color=GOLD if i in [3,4] else BLUE) for i,s in enumerate(['A² =','P','D','P⁻¹','P','D','P⁻¹'])]).arrange(RIGHT,buff=.2).move_to(pos(0,.5))
        if tokens.width>7 if SHORT else tokens.width>12:tokens.scale_to_fit_width(7 if SHORT else 12)
        self.reveal(tokens);self.to(2);self.play(Circumscribe(VGroup(tokens[3],tokens[4]),color=GOLD),run_time=.7)
        self.reveal(label('P⁻¹ P = I',y=-1,size=35,color=GOLD));self.to(4)
        self.play(Transform(tokens,label('A² = P D² P⁻¹',y=.5,size=44,color=BLUE)),run_time=.5)
    def scene_11(self):
        self.heading('고윳값만 n제곱하면 된다',BLUE)
        self.reveal(label('Aⁿ = P Dⁿ P⁻¹',y=1.55 if SHORT else .8,size=46,color=BLUE))
        self.to(4);self.reveal(label('Dⁿ = diag(λ₁ⁿ, λ₂ⁿ)',y=-.1 if SHORT else -.2,size=36,color=GOLD))
        self.to(6);self.reveal(label('2ⁿ ↑        0.5ⁿ ↓',y=-1.5 if SHORT else -1.2,size=36,color=BLUE))
        self.note('조건: A가 대각화 가능할 때',GOLD)
    def scene_12(self):
        self.heading('SVD · 한 번의 길이 변화',TEAL)
        s=.82 if SHORT else .72;ci=pos(-1.9,-.25) if SHORT else pos(-3.2,-.2);co=pos(1.8,-.25) if SHORT else pos(3.2,-.2)
        circle=Circle(radius=s,color=BLUE).move_to(ci);ellipse=Ellipse(width=2*s,height=4*s,color=TEAL).move_to(co)
        self.add(circle,label('입력',ci[0],1.6 if SHORT else 1.35,22,BLUE),label('출력',co[0],1.6 if SHORT else 1.35,22,TEAL));self.to(2)
        shape=circle.copy();self.add(shape);self.play(Transform(shape,ellipse),run_time=2.5)
        self.to(5);self.reveal(arr(ci,[1,0],s,GOLD,6),arr(co,[0,2],s,TEAL,6));self.note('수평 입력 → 수직 출력   ·   최대 배율 ×2',TEAL)
    def scene_13(self):
        self.heading('같은 Aₛ를 두 번 적용',TEAL);o=pos(0,-.2);s=1.15 if SHORT else .8
        self.add(grid(o,s,bounds=(-2.8,2.8,-1.8,2.5)));v=arr(o,[1,0],s,GOLD,6);self.add(v)
        self.play(Transform(v,arr(o,[0,2],s,TEAL,6)),run_time=1.6)
        one=label('첫 번째 ×2',y=-3 if SHORT else -1.7,size=30,color=TEAL);self.reveal(one)
        self.to(3);self.play(Transform(v,arr(o,[-2,0],s,ORANGE,6)),run_time=1.5)
        self.play(Transform(one,label('두 번째 ×1  ·  길이는 2 그대로',y=-3 if SHORT else -1.7,size=28,color=ORANGE)),run_time=.4)
    def scene_14(self):
        self.heading('특이값을 제곱하면?',TEAL)
        self.reveal(label('한 번의 최대 배율: 2',y=1.8 if SHORT else 1,size=30,color=TEAL))
        guess=label('2² = 4 ?',y=.25,size=53,color=MUTED);self.reveal(guess)
        self.to(3);self.play(Transform(guess,label('실제 두 번의 최대 배율: 2',y=.25,size=36,color=GOLD)),run_time=.7)
        self.reveal(label('Aₛ² = −2I',y=-1.15,size=35,color=TEAL));self.note('σₘₐₓ(Aₛ²) = 2  ≠  σₘₐₓ(Aₛ)² = 4',GOLD)
    def scene_15(self):
        self.heading('EVD · 반복 변환의 구조',BLUE);self.evolution(parts=True);self.note('Aⁿ = P Dⁿ P⁻¹   ·   고유성분별 분석',BLUE)
    def scene_16(self):
        self.heading('EVD에도 조건과 한계가 있다',GOLD)
        left=pos(-1.85,-.2) if SHORT else pos(-3.3,-.3);right=pos(1.55,-.2) if SHORT else pos(2.8,-.3)
        self.add(label('대각화 불가능',left[0],2 if SHORT else 1.1,25,BLUE,3.4),label('과도한 성장 뒤 감소',right[0],2 if SHORT else 1.1,23,ORANGE,3.5))
        self.add(Line(left-LEFT*.1,left+RIGHT*1.25,color=BLUE),arr(left,[1,0],.8,BLUE),label('전단 · 독립 고유방향 하나',left[0],-1.4,17,MUTED,3.5))
        # A separate stable nonnormal matrix: actual norms, no decorative curve.
        vals=[np.linalg.norm(np.linalg.matrix_power(TRANSIENT,n)@np.array([0.,1.])) for n in range(25)]
        base=right+pos(-1.25,-.75);width=2.8;height=1.6
        self.add(Line(base,base+RIGHT*width,color=MUTED),Line(base,base+UP*height,color=MUTED),label('n →',right[0]+1.15,-1.4,16,MUTED,1))
        points=[base+pos(width*n/24,height*v/max(vals)) for n,v in enumerate(vals)]
        curve=VMobject(color=ORANGE,stroke_width=3).set_points_as_corners(points);self.play(Create(curve),run_time=2)
        self.note('별도 예시 B = [0.8, 2; 0, 0.7]  ·  ‖Bⁿe₂‖',MUTED)
    def scene_17(self):
        self.heading('ROUND 05 · 미래 예측',GOLD);pair=self.pair().move_to(pos(0,1 if SHORT else .1));self.reveal(pair)
        self.to(2);self.reveal(label('EVD 승!',y=-1.3 if SHORT else -1.35,size=53,color=BLUE),d=.2)
        self.play(Circumscribe(pair[0],color=BLUE),run_time=.6);self.to(3)
        self.note('대각화 가능한 행렬 · 반복 변환을 고윳값의 거듭제곱으로',GOLD)
    def scene_18(self):
        self.heading('ROUND 05 WINNER · EVD',BLUE);score=label('EVD   2 : 2   SVD',y=.6 if SHORT else 0,size=45);self.add(score)
        self.play(Transform(score,label('EVD   3 : 2   SVD',y=.6 if SHORT else 0,size=45,color=GOLD)),Transform(self.score,label('EVD  3 : 2  SVD',x=0 if SHORT else 5.1,y=5.13 if SHORT else 2.98,size=15,color=MUTED,width=3)),run_time=.6)
        self.to(2);self.reveal(label('EVD가 다시 앞서갑니다!',y=-1.8 if SHORT else -1.5,size=35,color=BLUE),d=.3)
