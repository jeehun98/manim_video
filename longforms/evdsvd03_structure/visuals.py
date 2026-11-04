"""EVD coordinate changes and SVD paired input/output geometry, with exact clocks."""
import sys,json,textwrap
from pathlib import Path
ROOT=Path(__file__).resolve().parent
WORK=ROOT.parents[1];sys.path.insert(0,str(WORK))
from manim import *
from longforms.evdsvd01_names.visuals import BattleScene,label,pos,card,SHORT,BLUE,TEAL,WHITE,MUTED,GOLD,PANEL
from longforms.evdsvd02_conditions.visuals import matrix,GOOD,BAD
MANIFEST=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
CUES=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))
AE=np.array([[2.,1.],[0.,1.]])
P=np.array([[1.,1.],[0.,-1.]])
D=np.diag([2.,1.])
AS=np.array([[0.,-1.],[3.,0.]])
U=np.array([[0.,-1.],[1.,0.]])
SIGMA=np.diag([3.,1.])

def rows(*strings,color=WHITE,size=28):
    return VGroup(*[label(s,y=((len(strings)-1)/2-i)*.85,size=size,color=color,width=6.1) for i,s in enumerate(strings)])

def arrow_at(origin,v,unit=1,color=BLUE,width=5):
    return Arrow(origin,origin+pos(*(np.asarray(v)*unit)),buff=0,color=color,stroke_width=width,max_tip_length_to_length_ratio=.17)

def coordinate_picture():
    unit=.95 if SHORT else .72
    origin=pos(-1.2,-.65) if SHORT else pos(2.0,.45)
    def point(v):return origin+pos(*(np.asarray(v)*unit))
    standard=VGroup(*[Line(point([-1.1,t]),point([3.6,t]),color=MUTED,stroke_opacity=.15,stroke_width=1) for t in [-2,-1,0,1]],*[Line(point([t,-2]),point([t,1.2]),color=MUTED,stroke_opacity=.15,stroke_width=1) for t in [-1,0,1,2,3]])
    oblique=VGroup(*[Line(point(P@np.array([a,-.9])),point(P@np.array([a,1.8])),color=BLUE,stroke_opacity=.2,stroke_width=1) for a in [-1,0,1,2,3]],*[Line(point(P@np.array([-1,b])),point(P@np.array([3.1,b])),color=TEAL,stroke_opacity=.2,stroke_width=1) for b in [-1,0,1,2]])
    # Clip the visual extent by using only the two oblique basis axes and a few local parallels.
    oblique=VGroup(Line(point([-1,0]),point([3.5,0]),color=BLUE,stroke_opacity=.5),Line(point([-.7,.7]),point([2,-2]),color=TEAL,stroke_opacity=.5),Line(point([0,-1]),point([3.3,-1]),color=BLUE,stroke_opacity=.15),Line(point([.3,.7]),point([3,-2]),color=TEAL,stroke_opacity=.15))
    bases=VGroup(arrow_at(origin,[1,0],unit,BLUE,4),arrow_at(origin,[1,-1],unit,TEAL,4))
    x=arrow_at(origin,[2,-1],unit,GOLD,5)
    return dict(origin=origin,unit=unit,point=point,standard=standard,oblique=oblique,bases=bases,x=x)

def pair_picture():
    unit=.73 if SHORT else .46
    ci=pos(-1.9,-.4) if SHORT else pos(-3.15,-.1)
    co=pos(1.9,-.4) if SHORT else pos(3.15,-.1)
    def at(origin,v):return origin+pos(*(np.asarray(v)*unit))
    axes=VGroup(Line(at(ci,[-1.4,0]),at(ci,[1.4,0]),color=MUTED,stroke_opacity=.4),Line(at(ci,[0,-1.4]),at(ci,[0,1.4]),color=MUTED,stroke_opacity=.4),Line(at(co,[-1.4,0]),at(co,[1.4,0]),color=MUTED,stroke_opacity=.4),Line(at(co,[0,-3.3]),at(co,[0,3.3]),color=MUTED,stroke_opacity=.4))
    circle=Circle(radius=unit,color=BLUE,stroke_width=2).move_to(ci)
    ellipse=Ellipse(width=2*unit,height=6*unit,color=TEAL,stroke_width=2).move_to(co)
    labels=VGroup(label('입력 · 단위원',ci[0],2.2 if SHORT else 1.6,21,BLUE,3.3),label('출력 · 타원',co[0],2.2 if SHORT else 1.6,21,TEAL,3.3))
    formula=label('A(x, y) = (−y, 3x)',y=3.3 if SHORT else .85,size=24,color=MUTED,width=7 if SHORT else 3.8)
    return dict(unit=unit,ci=ci,co=co,at=at,axes=axes,circle=circle,ellipse=ellipse,labels=labels,formula=formula,group=VGroup(axes,circle,ellipse,labels,formula))

class StructureScene(BattleScene):
    def setup(self):
        self.spec=MANIFEST[self.INDEX];self.length=self.spec['duration_seconds']
        self.add(label('MATRIX DECOMPOSITION WORLD CUP',y=6.55 if SHORT else 3.55,size=15,color=MUTED,width=7 if SHORT else 12))
        y=5.85 if SHORT else 2.98
        self.add(label('EVD',-1.35,y,29,BLUE,2),label('VS',0,y,17,MUTED,1),label('SVD',1.35,y,29,TEAL,2),Line(pos(-3.5 if SHORT else -6.5,y-.45),pos(3.5 if SHORT else 6.5,y-.45),color=MUTED,stroke_opacity=.25))
        self.score=label('EVD  1 : 1  SVD',x=0 if SHORT else 5.1,y=5.13 if SHORT else 2.98,size=15,color=MUTED,width=3)
        self.add(self.score,label('03 / STRUCTURE  ·  같은 기저와 두 직교기저',y=-6.65 if SHORT else -3.65,size=14,color=MUTED,width=7 if SHORT else 12))
        self.caption=VGroup();self.caption_key=None
        self.caption.add_updater(lambda m,dt:self.update_caption());self.add(self.caption);self.update_caption()
    def update_caption(self):
        t=self.spec['start']+self.time+1e-6
        cue=next((c for c in CUES if c['start']<=t<c['end']),None)
        key=cue['start'] if cue else None
        if key==self.caption_key:return
        self.caption_key=key;self.caption.remove(*list(self.caption))
        if cue:
            text='\n'.join(textwrap.wrap(cue['caption'],27 if SHORT else 52,break_long_words=False))
            txt=label(text,y=-5.7 if SHORT else -2.98,size=22 if SHORT else 23,width=7.1 if SHORT else 12.5)
            bg=RoundedRectangle(width=7.45 if SHORT else 13,height=max(.65,txt.height+.25),corner_radius=.08,stroke_width=0,fill_color='#080F21',fill_opacity=.97).move_to(txt)
            self.caption.add(bg,txt).set_z_index(100)
    def note(self,s,color=MUTED):
        m=label(s,y=-4.35 if SHORT else -2.2,size=22,color=color,width=7 if SHORT else 12)
        self.reveal(m,d=.2);return m
    def pair_start(self,title):
        self.title(title,TEAL);g=pair_picture();self.reveal(g['group']);return g
    def arrows(self,g,x,color=GOLD):
        return VGroup(arrow_at(g['ci'],x,g['unit'],BLUE),arrow_at(g['co'],AS@x,g['unit'],color))
    def move_pair(self,g,arrows,theta0,theta1,duration):
        def update(m,alpha):
            theta=interpolate(theta0,theta1,alpha);x=np.array([np.cos(theta),np.sin(theta)])
            m.become(self.arrows(g,x))
        self.play(UpdateFromAlphaFunc(arrows,update),run_time=duration,rate_func=smooth)
    def scene_0(self):
        opening=label('행렬 분해\n이상형 월드컵!',y=2.3 if SHORT else 1.3,size=40)
        self.reveal(opening);self.to(1);self.reveal(self.pair().move_to(pos(0,-.6)),d=.4)
        self.to(3);self.play(FadeOut(opening),run_time=.2)
        self.reveal(label('ROUND 03 · 분해 구조',y=2.7 if SHORT else 1.3,size=32,color=GOLD))
    def scene_1(self):
        self.title('EVD · 왜 P와 P⁻¹일까?',BLUE)
        formula=VGroup(label('A =',x=-2.8,size=44),label('P',x=-1.5,size=56,color=BLUE),label('D',x=0,size=56,color=GOLD),label('P⁻¹',x=1.8,size=56,color=BLUE)).move_to(pos(0,1.1))
        self.to(2);self.reveal(formula);self.to(5)
        self.reveal(CurvedArrow(formula[1].get_bottom()+DOWN*.15,formula[3].get_bottom()+DOWN*.15,angle=PI/3,color=BLUE),label('하나의 기저와 그 역변환',y=-1.5,size=31,color=BLUE))
        self.note('양 끝의 P와 P⁻¹는 무엇을 할까?')
    def scene_2(self):
        self.title('고유벡터는 원래 직선 위에 남는다',BLUE)
        c=coordinate_picture();origin=c['origin'];unit=c['unit']
        graph=VGroup(c['standard'],Line(c['point']([-1,0]),c['point']([3.5,0]),color=BLUE,stroke_opacity=.5),arrow_at(origin,[1,0],unit,BLUE))
        exp=rows('A = [ 2  1 ; 0  1 ]','p₁ = (1, 0)ᵀ',color=BLUE).move_to(pos(0,2.7) if SHORT else pos(-3.4,.2))
        self.reveal(exp,graph);self.to(3)
        self.play(Transform(graph[2],arrow_at(origin,[2,0],unit,BLUE)),run_time=2)
        self.to(6);self.note('Ap₁ = 2p₁   ·   일반식 Apᵢ = λᵢpᵢ',BLUE)
        self.reveal(label('별도 예: λ=−1이면 p → −p · 같은 직선',x=0 if SHORT else -3.5,y=-3.3 if SHORT else -1.5,size=21,color=MUTED,width=6))
    def scene_3(self):
        self.title('P⁻¹ → D → P',BLUE)
        c=coordinate_picture();basis=c['bases'];x=c['x'];grid=c['standard'];standard_back=grid.copy()
        calc=rows('x = (2, −1)ᵀ','P⁻¹x = (1, 1)ᵀ',color=BLUE).move_to(pos(0,2.8) if SHORT else pos(-3.5,.45))
        self.reveal(grid,basis,x,calc)
        self.to(1)
        self.play(ReplacementTransform(grid,c['oblique']),run_time=.6)
        p1_segment=arrow_at(c['origin'],[1,0],c['unit'],BLUE,3)
        p2_segment=arrow_at(c['point']([1,0]),[1,-1],c['unit'],TEAL,3)
        self.reveal(p1_segment,p2_segment,d=.2)
        change=self.note('벡터는 고정 · 좌표 표현만 (2,−1) → (1,1)')
        self.to(4)
        self.play(Transform(x,arrow_at(c['origin'],[3,-1],c['unit'],GOLD)),Transform(p1_segment,arrow_at(c['origin'],[2,0],c['unit'],BLUE,3)),Transform(p2_segment,arrow_at(c['point']([2,0]),[1,-1],c['unit'],TEAL,3)),Transform(calc,rows('D(1,1)ᵀ = (2,1)ᵀ','고유기저의 성분별 배율',color=GOLD).move_to(calc)),run_time=1.5)
        self.to(7)
        self.play(ReplacementTransform(c['oblique'],standard_back),Transform(calc,rows('P(2,1)ᵀ = (3,−1)ᵀ','Ax = (3,−1)ᵀ',color=GOLD).move_to(calc)),Transform(change,label('변환 결과를 원래 좌표로 표현',y=-4.35 if SHORT else -2.2,size=22,color=MUTED,width=7 if SHORT else 12)),run_time=.6)
        self.to(9);self.play(Circumscribe(calc,color=GOLD),run_time=.6)
    def scene_4(self):
        self.title('행렬곱은 각 행과 입력의 내적')
        mat=matrix([['a','b'],['c','d']]).scale(1.1)
        exp=VGroup(label('M',y=1.2,size=30),mat,label('x = (x₁, x₂)ᵀ',y=-1.2,size=28))
        outputs=rows('(a,b) · x = ax₁ + bx₂','(c,d) · x = cx₁ + dx₂',color=GOLD)
        exp,outputs=self.split(exp,outputs);self.reveal(exp);self.to(3)
        self.reveal(outputs[0]);self.play(*[Indicate(m,color=BLUE) for m in mat.entries[0]],run_time=.4)
        self.to(5);self.reveal(outputs[1]);self.play(*[Indicate(m,color=TEAL) for m in mat.entries[1]],run_time=.4)
        self.to(7);self.note('스칼라 내적값 두 개를 모아 출력 벡터 구성')
    def scene_5(self):
        self.title('직접 내적 ≠ 비직교 기저의 좌표',BLUE)
        correct=rows('P⁻¹ = [ 1  1 ; 0  −1 ]','P⁻¹(2,−1)ᵀ = (1,1)ᵀ','실제 고유기저 좌표  ✓',color=GOOD)
        wrong=rows('p₁ᵀx = 2','p₂ᵀx = 3','직접 내적값 (2,3) ≠ 좌표',color=BAD)
        correct,wrong=self.split(correct,wrong);self.reveal(correct)
        self.to(4);self.reveal(wrong)
        self.to(8);self.note('Pᵀ ≠ P⁻¹  ·  고유기저는 일반적으로 정규직교가 아님')
    def scene_6(self):
        self.title('입력과 출력에 같은 고유기저',BLUE)
        self.reveal(label('x = c₁p₁ + c₂p₂',y=2 if SHORT else 1,size=36,color=BLUE),label('Ax = λ₁c₁p₁ + λ₂c₂p₂',y=.3 if SHORT else -.15,size=36,color=BLUE))
        self.to(3);self.reveal(label('ONE EIGENBASIS',y=-2 if SHORT else -1.5,size=40,color=GOLD))
        self.note('같은 p₁, p₂ · 달라지는 것은 좌표 성분')
    def scene_7(self):
        self.title('SVD · 단위원에 A를 적용하면?',TEAL)
        g=pair_picture();self.to(3)
        temporary=Circle(radius=g['unit'],color=TEAL).move_to(g['co'])
        angles=np.linspace(0,TAU,32,endpoint=False)
        inputs=VGroup(*[Dot(g['at'](g['ci'],[np.cos(t),np.sin(t)]),radius=.025,color=BLUE) for t in angles])
        outputs=VGroup(*[Dot(g['at'](g['co'],[np.cos(t),np.sin(t)]),radius=.025,color=GOLD) for t in angles])
        self.reveal(g['axes'],g['circle'],g['labels'],g['formula'],temporary,inputs,outputs)
        self.to(5)
        target=VGroup(*[Dot(g['at'](g['co'],AS@np.array([np.cos(t),np.sin(t)])),radius=.025,color=GOLD) for t in angles])
        self.play(Transform(temporary,g['ellipse']),Transform(outputs,target),run_time=2.2)
        self.note('가역 2차원 예시 · 세로 반축 3, 가로 반축 1',TEAL)
    def scene_8(self):
        g=self.pair_start('방향에 따라 출력 길이가 달라진다')
        arrows=self.arrows(g,np.array([1.,0.]));self.reveal(arrows,d=.2)
        norm=label('출력 길이 = 3.00',y=-3.5 if SHORT else -1.8,size=25,color=GOLD);self.add(norm)
        last=[None]
        def scan(m,alpha):
            theta=PI*alpha;x=np.array([np.cos(theta),np.sin(theta)])
            m.become(self.arrows(g,x))
            value=round(float(np.linalg.norm(AS@x)),1)
            if last[0]!=value:
                norm.become(label(f'출력 길이 = {value:.1f}',y=-3.5 if SHORT else -1.8,size=25,color=GOLD));last[0]=value
        self.play(UpdateFromAlphaFunc(arrows,scan),run_time=2.5,rate_func=linear)
        self.note('입력 길이는 항상 1 · 출력 길이는 1~3')
    def scene_9(self):
        g=self.pair_start('가장 긴 출력에 대응하는 입력 방향')
        arrows=self.arrows(g,np.array([np.cos(.9),np.sin(.9)]));self.reveal(arrows,d=.2)
        self.move_pair(g,arrows,.9,0,2)
        self.to(3)
        self.reveal(DashedLine(g['at'](g['co'],[0,-3]),g['at'](g['co'],[0,3]),color=GOLD),d=.2)
        self.to(5);self.note('v₁ = (1,0)ᵀ  ·  오른쪽 특이벡터는 입력 방향',BLUE)
    def scene_10(self):
        g=self.pair_start('출력의 단위방향과 길이 배율')
        arrows=self.arrows(g,np.array([1.,0.]));self.reveal(arrows)
        self.to(2)
        unit=arrow_at(g['co'],[0,1],g['unit'],TEAL,8);self.reveal(unit,d=.3)
        self.reveal(label('u₁',x=g['co'][0]+.45,y=g['co'][1]+g['unit']*.6,size=25,color=TEAL,width=1),d=.2)
        self.to(5)
        ruler_x=g['co'][0]-.55
        ruler=VGroup(Line(pos(ruler_x,g['co'][1]),pos(ruler_x,g['co'][1]+3*g['unit']),color=GOLD),*[Line(pos(ruler_x-.08,g['co'][1]+i*g['unit']),pos(ruler_x+.08,g['co'][1]+i*g['unit']),color=GOLD) for i in range(4)])
        self.reveal(ruler);self.note('u₁ = (0,1)ᵀ, ‖u₁‖=1  ·  σ₁ = 3',TEAL)
    def scene_11(self):
        g=self.pair_start('Av₁ = σ₁u₁')
        self.reveal(self.arrows(g,np.array([1.,0.])),d=.2)
        self.note('입력 방향 v₁ → 출력 단위방향 u₁ × 배율 3',GOLD)
    def scene_12(self):
        g=self.pair_start('임의의 단위벡터도 크기 × 방향?')
        x=np.array([np.cos(35*DEGREES),np.sin(35*DEGREES)])
        self.reveal(self.arrows(g,x),d=.3)
        self.to(1.5);self.note('Ax = ‖Ax‖ · (Ax / ‖Ax‖)',GOLD)
        self.reveal(label('이 예시는 가역 → Ax ≠ 0',y=-3.4 if SHORT else -1.75,size=22,color=MUTED))
    def scene_13(self):
        g=self.pair_start('입력도 직교 · 출력도 직교')
        a=arrow_at(g['ci'],[1,0],g['unit'],BLUE);b=arrow_at(g['ci'],[0,1],g['unit'],TEAL)
        ci=g['ci'];co=g['co'];s=g['unit']*.22
        corner1=VMobject(color=WHITE).set_points_as_corners([ci+pos(s,0),ci+pos(s,s),ci+pos(0,s)])
        self.reveal(a,b,corner1)
        self.to(3)
        av1=arrow_at(co,[0,3],g['unit'],BLUE);av2=arrow_at(co,[-1,0],g['unit'],TEAL)
        corner2=VMobject(color=WHITE).set_points_as_corners([co+pos(0,s),co+pos(-s,s),co+pos(-s,0)])
        self.reveal(av1,av2,corner2)
        self.to(6);self.note('Av₁ = 3u₁   ·   Av₂ = u₂   ·   직교 → 직교',GOLD)
    def scene_14(self):
        self.title('두 기저의 방향은 달라도 된다',TEAL)
        left=VGroup(arrow_at(pos(-2,0),[1,0],.9,BLUE),arrow_at(pos(-2,0),[0,1],.9,TEAL),label('V = I',x=-2,y=-1.1,size=29,color=BLUE))
        rightaxes=VGroup(arrow_at(pos(2,0),[1,0],.9,BLUE),arrow_at(pos(2,0),[0,1],.9,TEAL))
        self.reveal(left,rightaxes);self.play(Rotate(rightaxes,angle=PI/2,about_point=pos(2,0)),run_time=.8)
        self.reveal(label('U · 90° 회전',x=2,y=-1.1,size=27,color=TEAL))
        self.note('입력 기저 V ≠ 출력 기저 U',GOLD)
    def scene_15(self):
        # This scene is exactly one second; use a single concise transition.
        self.add(label('방향들을 행렬로 모으면',y=1.5,size=35,color=TEAL),label('[v₁ v₂]   →   Vᵀ   →   Σ   →   [u₁ u₂]',y=-.3,size=30,width=7 if SHORT else 12))
        self.play(FadeIn(label('기하학에서 분해식으로',y=-1.6,size=24,color=MUTED)),run_time=.3)
    def scene_16(self):
        self.title('V의 열을 Vᵀ의 행으로',TEAL)
        columns=VGroup(matrix([['v₁','v₂']]).scale(1.3),label('V = [v₁ v₂]',y=-1.2,size=30,color=BLUE))
        transposed=VGroup(matrix([['v₁ᵀ'],['v₂ᵀ']],TEAL),label('Vᵀ의 각 행',y=-1.2,size=29,color=TEAL))
        columns,transposed=self.split(columns,transposed);self.reveal(columns)
        self.to(2);self.reveal(transposed);self.note('이 예시는 V=I · 숫자보다 열→행의 구조에 주목')
    def scene_17(self):
        self.title('Vᵀx · 각 행과 입력의 내적',TEAL)
        exp=rows('x = (2,1)ᵀ','Vᵀ = [ v₁ᵀ ; v₂ᵀ ]',color=TEAL)
        values=rows('v₁ᵀx = (1,0)·(2,1) = 2','v₂ᵀx = (0,1)·(2,1) = 1',color=GOLD)
        exp,values=self.split(exp,values);self.reveal(exp,values[0]);self.to(2);self.reveal(values[1])
        self.to(4);self.note('Vᵀx = (2,1)ᵀ · 입력 기저 좌표 (아직 Ax 아님)',TEAL)
    def scene_18(self):
        self.title('정규직교하므로 내적값이 좌표',TEAL)
        self.reveal(label('v₁ᵀv₁ = v₂ᵀv₂ = 1',y=2 if SHORT else 1,size=32,color=BLUE),label('v₁ᵀv₂ = v₂ᵀv₁ = 0',y=.6 if SHORT else -.1,size=32,color=TEAL))
        self.to(2);self.reveal(label('VᵀV = I',y=-1 if SHORT else -1.2,size=42,color=GOLD))
        self.note('EVD: P⁻¹x   /   SVD: Vᵀx')
    def scene_19(self):
        self.title('Σ가 배율을 적용 · U가 출력 조합',TEAL)
        calculations=rows('Vᵀx = (2,1)ᵀ','Σ(2,1)ᵀ = (6,1)ᵀ',color=GOLD)
        unit=.47 if SHORT else .38
        origin=pos(.55,-2.6) if SHORT else pos(3.2,-1.35)
        p1=arrow_at(origin,[0,6],unit,BLUE);p2=arrow_at(origin+pos(0,6*unit),[-1,0],unit,TEAL)
        resultant=arrow_at(origin,[-1,6],unit,GOLD)
        calculations.move_to(pos(0,2.8) if SHORT else pos(-3.4,.4));self.reveal(calculations)
        self.to(3);self.reveal(p1,d=.3);self.to(4)
        self.reveal(p2,resultant,d=.3);self.note('6u₁ + u₂ = (−1,6)ᵀ = Ax',GOLD)
    def scene_20(self):
        self.title('전체 분해식 완성',TEAL)
        self.reveal(label('Ax = UΣVᵀx',y=2 if SHORT else 1,size=47,color=TEAL),label('Vᵀ → Σ → U',y=.4 if SHORT else -.2,size=39,color=GOLD))
        self.to(2);self.reveal(label('A = UΣVᵀ',y=-1.7 if SHORT else -1.3,size=47,color=TEAL))
        self.note('좌표 추출 → 배율 적용 → 출력 조합')
    def scene_21(self):
        self.title('하나의 고유기저 vs 두 직교기저')
        pair=self.pair().move_to(pos(0,1 if SHORT else .3));self.reveal(pair)
        self.reveal(label('같은 고유기저',x=-1.8,y=-1 if SHORT else -1.2,size=24,color=BLUE,width=3.2))
        self.to(4);self.reveal(label('입력·출력 직교기저',x=1.8,y=-1 if SHORT else -1.2,size=23,color=TEAL,width=3.2))
        self.note('EVD: pᵢ → λᵢpᵢ    /    SVD: vᵢ → σᵢuᵢ',GOLD)
    def scene_22(self):
        self.title('ROUND 03 · 분해 구조',GOLD)
        pair=self.pair().move_to(pos(0,1 if SHORT else .3));self.reveal(pair)
        self.to(3)
        crown=Polygon(pos(-2.75,-1.05),pos(-2.65,-1.6),pos(-1.95,-1.6),pos(-1.85,-1.05),pos(-2.1,-1.25),pos(-2.3,-.9),pos(-2.5,-1.25),color=GOLD,fill_color=GOLD,fill_opacity=.85)
        self.reveal(label('EVD 승!',y=-1.3,size=56,color=BLUE),crown,d=.2)
        self.play(Circumscribe(pair[0],color=BLUE),run_time=.5)
        self.to(4);self.note('취향 판정: 하나의 고유기저라는 구조적 간결성',GOLD)
    def scene_23(self):
        self.title('ROUND 03 WINNER · EVD',BLUE)
        self.reveal(label('현재 스코어',y=2.6 if SHORT else 1.25,size=28,color=MUTED))
        score=label('EVD   1 : 1   SVD',y=.6 if SHORT else 0,size=45);self.reveal(score)
        self.to(1.2)
        self.play(Transform(score,label('EVD   2 : 1   SVD',y=.6 if SHORT else 0,size=45,color=GOLD)),Transform(self.score,label('EVD  2 : 1  SVD',x=0 if SHORT else 5.1,y=5.13 if SHORT else 2.98,size=15,color=MUTED,width=3)),run_time=.5)
        self.to(3);self.reveal(label('EVD 리드!',y=-1.8 if SHORT else -1.5,size=45,color=BLUE),d=.2)
