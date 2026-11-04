"""Patterning: forward local response and inverse data design, in two layouts."""
import json
import os
import sys
import textwrap
from pathlib import Path
import numpy as np
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.nncalc02_induction_heads import scene as induction
from visual_library.manim import BG,INK,MUTED,ACCENT,GOOD,PRUNE,ZERO

config.pixel_width=int(os.environ.get('VIDEO_WIDTH','1920'))
config.pixel_height=int(os.environ.get('VIDEO_HEIGHT','1080'))
PORTRAIT=config.pixel_height>config.pixel_width
config.frame_width=9 if PORTRAIT else 16;config.frame_height=16 if PORTRAIT else 9
config.frame_rate=30;config.background_color=BG;config.disable_caching=True
HERE=Path(__file__).resolve().parent
DATA='#4CD9CB';CIRCUIT='#B39CFF';RESPONSE='#F7A65E';TARGET='#F3CF75'
label=induction.label;card=induction.card;arrow=induction.arrow;p=induction.p

class InductionCircuitView(VGroup):
    """Reuse episode 02's two-head blocks, grouped as the observed circuit."""
    def __init__(self,x=0,y=0,w=4.5):
        reference=induction.CircuitComposition(False)
        heads=VGroup(reference.blocks[0].copy(),reference.blocks[2].copy()).arrange(DOWN,buff=.28)
        heads.scale_to_fit_width(w-.3).move_to(p(x,y))
        path=arrow(heads[0].get_bottom(),heads[1].get_top(),CIRCUIT)
        self.heads=heads;self.path=path
        super().__init__(heads,path,SurroundingRectangle(heads,color=CIRCUIT,buff=.12,corner_radius=.12))

class DataReweightingView(VGroup):
    changes_model_weights_directly=False
    requires_retraining=True
    def __init__(self,x=0,y=0):
        self.x=x;self.y=y;self.bars=VGroup();self.cards=VGroup()
        for i,s in enumerate(['A B … A B','K M … K M','P Q R S']):
            yy=y+.8-i*.8
            self.cards.add(card(s,x-1.1,yy,2.65,.58,DATA,21))
            self.bars.add(Rectangle(width=.65,height=.22,stroke_width=0,fill_color=DATA,fill_opacity=.9).move_to(p(x+1.25,yy)))
        super().__init__(self.cards,self.bars)
    def reweight(self,scene):
        anim=[]
        for bar,width,color in zip(self.bars,[1.4,1.05,.3],[DATA,DATA,MUTED]):
            left=bar.get_left().copy()
            target=bar.copy().stretch_to_fit_width(width).move_to(left+RIGHT*width/2).set_fill(color)
            anim.append(Transform(bar,target))
        scene.play(*anim,run_time=1)

class TrainingPopulation(VGroup):
    def __init__(self,portrait=False):
        self.positions=[(0,3.15),(0,.45),(0,-2.25)] if portrait else [(-4.8,.55),(0,.55),(4.8,.55)]
        self.panels=VGroup();self.bars=VGroup()
        for (x,y),title in zip(self.positions,['조건 A','조건 B','조건 C']):
            panel=VGroup(card(title,x,y+.6,6.8 if portrait else 4,.75,CIRCUIT,26),
                label('같은 구조 · 다음 토큰 예측',x,y-.3,23,INK,6.9 if portrait else 4.4))
            self.panels.add(panel)
            self.bars.add(Rectangle(width=1.3,height=.22,stroke_width=0,fill_color=DATA,fill_opacity=.9).move_to(p(x,y-.9)))
        super().__init__(self.panels,self.bars)
    def conditions(self,scene):
        anim=[]
        for panel,bar,title,width,color in zip(self.panels,self.bars,['억제','기본','강조'],[.4,1.3,2.5],[MUTED,INK,DATA]):
            old=panel[0];x,y=old.get_center()[:2]
            anim.extend([Transform(old,card(title,x,y,old.width,.75,color,26)),
                bar.animate.stretch_to_fit_width(width).set_fill(color)])
        scene.play(*anim,run_time=1)

class CircuitFormationPlot(VGroup):
    measured=False
    def __init__(self,portrait=False):
        width=6.5 if portrait else 10.2;height=3.3 if portrait else 2.65
        origin=p(-width/2,-.7 if portrait else -.85)
        def point(x,y):return origin+RIGHT*(width*x)+UP*(height*y)
        axis=VGroup(Line(point(0,0),point(1,0),color=MUTED),Line(point(0,0),point(0,1),color=MUTED))
        self.curves=VGroup()
        for vals,color in [([.03,.035,.04,.045,.08],MUTED),([.03,.04,.15,.67,.82],INK),([.03,.44,.8,.89,.9],DATA)]:
            curve=VMobject(stroke_color=color,stroke_width=3).set_points_as_corners([point(i/4,v) for i,v in enumerate(vals)])
            curve.set_opacity(0);self.curves.add(curve)
        legends=VGroup(*[label(s,(-2.2+i*2.2) if portrait else (-3.4+i*3.4),
            -2.2 if portrait else -1.75,24,col,2 if portrait else 3.2) for i,(s,col) in enumerate([('억제',MUTED),('기본',INK),('강조',DATA)])])
        super().__init__(axis,self.curves,legends,
            label('Prefix Matching Score · 개념도',y=3.4 if portrait else 2.18,size=24,color=CIRCUIT,width=7.2 if portrait else 13),
            label('학습 진행 →',y=-1.3 if portrait else -1.28,size=20,color=MUTED),
            label('논문 조건: 0× · 1× · 2× · 4×',y=-3.65 if portrait else -2.35,size=22,color=DATA,width=7.4 if portrait else 14))
    def form(self,scene):
        for curve in reversed(self.curves.submobjects):scene.play(Create(curve.set_stroke(opacity=1).set_fill(opacity=0)),run_time=.65)

class SusceptibilityMatrixView(VGroup):
    dimensions=(2,3)
    uses_ordinary_inverse=False
    def __init__(self,x=0,y=0,portrait=False):
        self.entries=VGroup()
        for i in range(2):
            for j in range(3):
                self.entries.add(card(f'χ{str(i+1).translate(str.maketrans("12","₁₂"))}{str(j+1).translate(str.maketrans("123","₁₂₃"))}',
                    x+(j-1)*.73,y+.12-i*.56,.65,.48,RESPONSE,20))
        frame=RoundedRectangle(width=7 if portrait else 3.15,height=1.85,corner_radius=.12,
            color=RESPONSE,stroke_width=1.5,fill_color=RESPONSE,fill_opacity=.04).move_to(p(x,y))
        super().__init__(frame,self.entries,label('χ · 감수율 행렬',x,y+.67,24,RESPONSE,6.5 if portrait else 2.9))

class InverseDesignView(VGroup):
    relation='Δμ ≈ χ Δh'
    inverse_relation='χ Δh ≈ Δμ_target'
    def __init__(self,portrait=False):
        self.portrait=portrait
        self.locations=[(0,3.3),(0,.6),(0,-2.1)] if portrait else [(-4.75,.55),(0,.55),(4.75,.55)]
        a,b,c=self.locations
        self.data=card('Δh\n데이터 가중치 변화',*a,7 if portrait else 3.6,1.2,DATA,26)
        self.matrix=SusceptibilityMatrixView(*b,portrait)
        self.mu=card('Δμ\n구조 관측량 변화',*c,7 if portrait else 3.6,1.2,CIRCUIT,26)
        self.edges=VGroup()
        for left,right in [(self.data,self.matrix),(self.matrix,self.mu)]:
            self.edges.add(arrow(left.get_bottom() if portrait else left.get_right(),right.get_top() if portrait else right.get_left(),RESPONSE))
        self.formula=label(self.relation,y=-3.82 if portrait else -1.55,size=38,color=RESPONSE,width=7.4 if portrait else 14)
        self.annotation=label('μ: 구조 관측량의 사후기댓값 · 국소 반응',y=-4.85 if portrait else -2.75,
            size=17,color=MUTED,width=7.6 if portrait else 14)
        super().__init__(self.data,self.matrix,self.mu,self.edges,self.formula,self.annotation)
        self.targets=[self.data[1].copy(),self.mu[1].copy(),self.matrix.entries.copy(),self.formula.copy()]
    def prepare_intro(self):
        self.data[1].set_opacity(0);self.mu[1].set_opacity(0);self.matrix.entries.set_opacity(0);self.formula.set_opacity(0)
    def reveal_vectors(self,scene):scene.play(Transform(self.data[1],self.targets[0]),Transform(self.mu[1],self.targets[1]),run_time=.7)
    def reveal_relation(self,scene):scene.play(Transform(self.matrix.entries,self.targets[2]),Transform(self.formula,self.targets[3]),run_time=.7)
    def reverse(self,scene):
        anim=[]
        for edge,left,right in zip(self.edges,[self.data,self.matrix],[self.matrix,self.mu]):
            start=right.get_top() if self.portrait else right.get_left()
            end=left.get_bottom() if self.portrait else left.get_right()
            anim.append(Transform(edge,arrow(start,end,TARGET)))
        scene.play(*anim,run_time=.8)
    def set_goal(self,scene):
        x,y=self.locations[2]
        target=card('Δμ_target\n원하는 구조 변화',x,y,7 if self.portrait else 3.6,1.2,TARGET,25)
        scene.play(Transform(self.mu,target),run_time=.6)
        border=DashedVMobject(SurroundingRectangle(self.mu,buff=.08,color=TARGET),num_dashes=25)
        self.add(border);scene.play(Create(border),run_time=.4)
    def candidate(self,scene):
        x,y=self.locations[0]
        target=card('Δh_candidate\n데이터 조합 추정',x,y,7 if self.portrait else 3.6,1.2,DATA,25)
        scene.play(Transform(self.data,target),Transform(self.formula,label(self.inverse_relation,
            y=-3.82 if self.portrait else -1.55,size=31 if self.portrait else 38,color=RESPONSE,width=7.4 if self.portrait else 14)),run_time=.8)
    def limits(self,scene):
        text='국소 근사 · 도달 불가 방향 · 큰 변화의 오차'
        scene.play(Transform(self.annotation,label(text,y=-4.85 if self.portrait else -2.75,size=17,
            color=ACCENT,width=7.6 if self.portrait else 14)),
            Transform(self.formula,label('가능한 방향의 근사해\n큰 변화는 별도 검증' if self.portrait else '가능한 방향의 근사해 · 큰 변화는 별도 검증',
                y=-3.82 if self.portrait else -1.55,size=25 if self.portrait else 29,color=TARGET,width=7.4 if self.portrait else 14)),run_time=.6)

class AlgorithmSelectionView(VGroup):
    is_separate_experiment=True
    def __init__(self,portrait=False):
        if portrait:
            seqy=3.45;positions=[(0,1.5),(0,-.6)]
        else:seqy=1.85;positions=[(-3.9,.2),(3.9,.2)]
        seq=card('())(',y=seqy,w=4,color=ACCENT,size=41)
        a=card('개수 비교\n2 = 2 → 수락',*positions[0],7 if portrait else 6.4,1.4,DATA,28)
        b=card('중첩 확인\n1 → 0 → −1 → 0  ·  거부',*positions[1],7 if portrait else 6.4,1.4,CIRCUIT,25)
        super().__init__(seq,a,b,label('별도의 괄호 분류 실험 · LLC 기반 분석',y=-2.65 if portrait else -1.6,size=24,
            color=RESPONSE,width=7.5 if portrait else 14),label('데이터 분포 → 새 학습 → 알고리즘 경향',y=-4.05 if portrait else -2.35,
            size=25,color=ACCENT,width=7.5 if portrait else 14))

class PatterningVideo(Scene):
    def construct(self):
        self.portrait=PORTRAIT
        data=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
        assert data['script_approved'] and data['duration']==171
        if self.portrait:
            self.fixed=VGroup(label('신경망 내부의 계산  /  03',y=7.4,size=20,color=MUTED,width=7.6),
                label('학습 데이터로\n내부 회로의 형성을 조절한다',y=6.5,size=29,width=7.5),
                Line(p(-3.9,5.75),p(3.9,5.75),color=ZERO),
                RoundedRectangle(width=7.9,height=1.85,corner_radius=.1,stroke_width=0,fill_color='#14212D',fill_opacity=.95).move_to(p(0,-6.2)),
                label('도식·곡선은 개념도 · Wang & Murfet, 2026',y=-7.45,size=15,color=MUTED,width=7.5))
        else:
            self.fixed=VGroup(label('신경망 내부의 계산  03',-5.15,4.08,18,MUTED,5),
                label('학습 데이터로 신경망 내부 회로의 형성을 조절하는 방법',2.6,4.08,20,INK,9.7),
                Line(p(-7.4,3.65),p(7.4,3.65),color=ZERO),
                RoundedRectangle(width=15,height=1.04,corner_radius=.1,stroke_width=0,fill_color='#14212D',fill_opacity=.95).move_to(p(0,-3.65)),
                label('곡선·반응값은 개념도 · 실측 그래프 아님',-4.8,-4.3,15,MUTED,6.4),
                label('Wang & Murfet · Patterning (2026)',4.75,-4.3,15,MUTED,6))
        self.add(self.fixed);self.stage=VGroup();self.heading=VGroup();self.caption=VGroup()
        for k,seg in enumerate(data['segments']):
            self.to(seg['start'])
            preserve=k in (8,9,10)
            if preserve:self.remove(self.heading,self.caption)
            else:
                for obj in list(self.mobjects):
                    if obj is not self.fixed:self.remove(obj)
                self.stage=VGroup()
            self.heading=label(f'{k+1:02}  {seg["title"]}',y=5.25 if self.portrait else 3.12,
                size=24 if self.portrait else 29,color=ACCENT,width=7.7 if self.portrait else 14.5)
            self.add(self.heading);callbacks=self.build(k)
            self.caption=self.caption_obj(seg['cues'][0]['text']);self.add(self.caption)
            self.check_layout(k)
            if not preserve:self.play(FadeIn(self.stage,shift=UP*.06),run_time=.2)
            for j,cue in enumerate(seg['cues']):
                self.to(cue['start']);self.remove(self.caption);self.caption=self.caption_obj(cue['text']);self.add(self.caption)
                if j in callbacks:callbacks[j]()
                self.to(cue['end'])
        self.to(171)
    def caption_obj(self,s):
        obj=label(textwrap.fill(s,width=29 if self.portrait else 60,break_long_words=False,break_on_hyphens=False),
            y=-6.2 if self.portrait else -3.65,size=25 if self.portrait else 27,width=7.2 if self.portrait else 14.4)
        maxheight=1.5 if self.portrait else .88
        if obj.height>maxheight:obj.scale_to_fit_height(maxheight)
        return obj
    def to(self,target):
        frames=round(target*30)-round(self.time*30)
        if frames>0:self.wait(frames/30)
        elif frames < -10:raise RuntimeError(f'Timing overflow: {self.time} > {target}')
    def show(self,*objs):self.stage.add(*objs)
    def note(self,s):self.show(label(s,y=-4.85 if self.portrait else -2.75,size=17,color=MUTED,width=7.6 if self.portrait else 14.5))
    def pulse(self,*objs,color=ACCENT,duration=.6):self.play(*[Indicate(o,color=color,scale_factor=1.07) for o in objs],run_time=duration)
    def check_layout(self,k):
        for obj in self.stage:
            xmax,ymin,ymax=(4,-5.1,4.85) if self.portrait else (7.6,-3,2.75)
            if obj.get_left()[0]<-xmax or obj.get_right()[0]>xmax or obj.get_bottom()[1]<ymin or obj.get_top()[1]>ymax:
                raise ValueError(f'Scene {k+1} outside safe area: {obj}')
    def build(self,k):
        P=self.portrait;cb={}
        if k==0:
            circuit=InductionCircuitView(y=1.1 if P else -.25,w=5 if P else 3.75)
            self.show(card('A B C D A → B',y=4.05 if P else 2.05,w=7,color=DATA,size=30),circuit,
                label('Induction Circuit',y=-1.25 if P else -1.95,size=30,color=CIRCUIT,width=7.4 if P else 14),
                label('형성되는 시점도 바꿀 수 있을까?',y=-3.4 if P else -2.55,size=25,color=TARGET,width=7.4 if P else 14))
            cb={0:lambda:self.pulse(circuit,color=CIRCUIT),1:lambda:self.pulse(self.stage[-1])}
        elif k in (1,2):
            pop=TrainingPopulation(P);self.show(pop)
            self.note('조건별로 새로 학습 · 모델 구조와 학습 목표는 동일')
            cb={0:lambda:self.pulse(pop.panels),1:lambda:pop.conditions(self)} if k==1 else {0:lambda:pop.conditions(self)}
        elif k==3:
            plot=CircuitFormationPlot(P);self.show(plot)
            self.show(label('약 300만 파라미터 · attention-only',y=4.25 if P else 2.56,size=21,color=INK,width=7.4 if P else 14))
            self.note('결과 경향을 설명하는 개념도 · 형성 시점과 곡선값은 실측 재현 아님')
            cb={0:lambda:self.pulse(self.stage[1]),1:lambda:plot.form(self)}
        elif k==4:
            model=card('모델 구조 · Head 직접 편집 X',y=3.6 if P else 1.65,w=7.3 if P else 10,color=MUTED,size=27)
            weights=DataReweightingView(-.2 if P else -4.1,1.3 if P else -.25)
            training=card('데이터 가중치 변경\n→ 새로 학습',y=-1.4 if P else -.15,x=0 if P else 1,w=7 if P else 4.4,h=1.1,color=DATA,size=26)
            outcome=card('회로 형성 비교',y=-3.4 if P else -.15,x=0 if P else 5,w=7 if P else 3.2,color=CIRCUIT,size=25)
            self.show(model,weights,training,outcome)
            self.note('모델 파라미터는 학습 과정에서 갱신됨 · 직접 편집과 구별')
            cb={0:lambda:self.pulse(model,color=MUTED),1:lambda:weights.reweight(self)}
        elif k==5:
            weights=DataReweightingView(0,2.6 if P else .65)
            self.show(weights,card('어떤 데이터 방향이\n원하는 관측량에 영향을 줄까?',y=-.25 if P else -1.55,w=7.3 if P else 10,h=1.25,color=RESPONSE,size=28),
                label('영향의 크기와 방향은 같지 않다',y=-3 if P else 2.3,size=26,color=TARGET,width=7.4 if P else 14))
            self.note('데이터 유형별 영향은 예시 · 실제 샘플별 수치를 제시하지 않음')
            cb={0:lambda:self.pulse(self.stage[1]),1:lambda:self.pulse(weights.cards[0],weights.cards[2])}
        elif k==6:
            ys=[2.8,-.6] if P else [.9,-1.05]
            groups=VGroup()
            for i,y in enumerate(ys):
                inputcard=card(f'데이터 {"A" if i==0 else "B"}\n동일한 +Δh',-1.9 if P else -4.5,y,3.2 if P else 4.2,1.1,DATA,24)
                output=card('작은 +Δμ' if i==0 else '큰 −Δμ',1.9 if P else 4.5,y,3.2 if P else 4.2,1.1,CIRCUIT,26)
                groups.add(VGroup(inputcard,output,arrow(inputcard.get_right(),output.get_left(),RESPONSE)))
            self.show(groups,label('크기뿐 아니라 부호도 다를 수 있다',y=-3.3 if P else -2.3,size=25,color=RESPONSE,width=7.4 if P else 14))
            self.note('반응의 부호·크기는 설명용 예시 · 실측값 아님')
            cb={0:lambda:self.pulse(groups[0][1],groups[1][1],color=CIRCUIT)}
        elif k==7:
            self.flow=InverseDesignView(P);self.flow.prepare_intro();self.show(self.flow)
            cb={0:lambda:self.pulse(self.flow.matrix,color=RESPONSE),1:lambda:self.flow.reveal_vectors(self),2:lambda:self.flow.reveal_relation(self)}
        elif k==8:
            def reverse_question():
                self.flow.reverse(self)
                self.play(Transform(self.heading,label('09  같은 관계를 역으로 활용',y=5.25 if P else 3.12,
                    size=24 if P else 29,color=ACCENT,width=7.7 if P else 14.5)),run_time=.4)
            cb={0:lambda:self.pulse(self.flow.matrix.entries,color=RESPONSE),1:reverse_question,
                2:lambda:self.pulse(self.flow.data,self.flow.mu)}
        elif k==9:
            cb={0:lambda:self.flow.set_goal(self),1:lambda:self.pulse(self.flow.mu,color=TARGET)}
        elif k==10:
            cb={0:lambda:self.flow.candidate(self),1:lambda:self.flow.limits(self)}
        elif k==11:
            weights=DataReweightingView(-.2 if P else -4.65,2.65 if P else .5)
            train=card('감수율로 추정한 가중치\n→ 새 학습 실험',y=.2 if P else .45,x=0 if P else -.15,w=7.3 if P else 4.4,h=1.15,color=DATA,size=24)
            outcome=card('Induction Circuit\n형성 양상 비교',y=-2.2 if P else .45,x=0 if P else 4.7,w=7.3 if P else 4.3,h=1.15,color=CIRCUIT,size=25)
            self.show(weights,train,outcome)
            self.note('선택한 데이터 개입으로 재학습한 결과의 정성적 설명')
            def retrain():weights.reweight(self);self.pulse(train);self.pulse(outcome,color=CIRCUIT)
            cb={0:retrain}
        elif k==12:
            example=AlgorithmSelectionView(P);self.show(example)
            self.note('Induction 실험과 별개 · 모델 수·비율을 임의로 제시하지 않음')
            cb={0:lambda:self.pulse(example[1],example[2])}
        elif k==13:
            if P:ys=[2.65,-.65];xs=[0,0]
            else:ys=[.65,.65];xs=[-4,4]
            observe=card('Interpretability\n학습된 계산을 발견',xs[0],ys[0],7 if P else 6,1.5,CIRCUIT,28)
            design=card('Patterning\n원하는 계산 → 데이터 설계',xs[1],ys[1],7 if P else 6,1.5,DATA,27)
            direction=arrow(p(0,1.55),p(0,.45),RESPONSE) if P else arrow(p(-.8,.65),p(.8,.65),RESPONSE)
            self.show(observe,design,direction,label('무엇을 배웠나?  ↔  무엇을 배우게 할까?',y=-3.5 if P else -1.55,size=25,color=TARGET,width=7.4 if P else 14))
            cb={0:lambda:self.pulse(observe),1:lambda:self.play(Rotate(direction,PI),run_time=.6),2:lambda:self.pulse(design)}
        elif k==14:
            if P:coords=[(0,3.2),(0,.7),(0,-1.85)]
            else:coords=[(-4.65,.5),(0,.5),(4.65,.5)]
            blocks=VGroup(*[card(s,*xy,7 if P else 4.1,1.1,color,26) for s,xy,color in zip(
                ['학습 데이터 설계','새로운 학습','내부 계산의 형성 유도'],coords,[DATA,RESPONSE,CIRCUIT])])
            self.show(blocks)
            for a,b in zip(blocks,blocks[1:]):self.show(arrow(a.get_bottom() if P else a.get_right(),b.get_top() if P else b.get_left(),TARGET))
            self.show(label('발견하는 대상에서\n형성을 유도할 수 있는 대상으로' if P else '발견하는 대상에서, 형성을 유도할 수 있는 대상으로',
                y=-3.6 if P else -1.7,size=28,color=TARGET,width=7.4 if P else 14))
            self.note('작은 모델·제한된 문제에서 확인 · 완전한 제어를 보장하지 않음')
            cb={0:lambda:self.pulse(blocks[1],color=MUTED),1:lambda:self.pulse(blocks[0],blocks[2],color=TARGET)}
        return cb

class Patterning(PatterningVideo):pass
class PatterningShorts(PatterningVideo):pass
