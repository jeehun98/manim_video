"""Reading, erasing and tracing information are different experiments."""
import json
import os
import sys
from pathlib import Path
import numpy as np
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.nncalc06_circuit_tracing import scene as circuits
from episodes.nncalc03_patterning import scene as patterning
from visual_library.manim import BG,INK,MUTED,ACCENT,GOOD,PRUNE,ZERO
config.pixel_width=int(os.environ.get('VIDEO_WIDTH','1920'))
config.pixel_height=int(os.environ.get('VIDEO_HEIGHT','1080'))
PORTRAIT=config.pixel_height>config.pixel_width
config.frame_width=9 if PORTRAIT else 16;config.frame_height=16 if PORTRAIT else 9
config.frame_rate=30;config.background_color=BG;config.disable_caching=True
HERE=Path(__file__).resolve().parent
label=circuits.label;card=circuits.card;p=circuits.p;Edge=circuits.ContributionEdge
H='#B39CFF';INTERVENTION='#F7A65E';OUTPUT='#7EB8F3';CHANGED=ACCENT
W=np.array([1.,1.])/np.sqrt(2)
PROJECTION=np.eye(2)-np.outer(W,W)
SAMPLES=np.array([[1.4,.6],[1,.2],[.6,1],[-.6,-1.4],[-1,-.6],[-1.3,-.7]])
OTHER=np.array([1.3,.1])

def center(portrait):return (0,1.4) if portrait else (-3.7,.1)

class ReadoutModelView(VGroup):
    original_weights_frozen=True
    probe_trained_separately=True
    probe_prediction_fed_into_model=False
    def __init__(self,portrait=False,probe=True):
        cx,cy=center(portrait)
        self.sentence=card('The cats are sleeping',cx,cy+2.2,6.6,.65,INK,26)
        self.front=card('원래 모델 앞부분\n가중치 고정',cx-1.7,cy+.7,2.85,1,MUTED,22)
        self.activation=card('대상 위치\nh ∈ ℝᵈ',cx+1.7,cy+.7,2.3,1,H,24)
        self.rear=card('원래 모델 뒷부분\n가중치 고정',cx-1.7,cy-.9,2.85,1,MUTED,22)
        self.model_output=card('원 모델 출력\n토큰 예측',cx-1.7,cy-2.15,2.85,1,OUTPUT,22)
        self.probe=card('별도 Linear Probe\nwᵀh + b',cx+1.7,cy-.9,2.85,1,GOOD,22)
        self.probe_output=card('Probe 판독\n단수 / 복수 ?',cx+1.7,cy-2.15,2.85,1,GOOD,22)
        self.edges=VGroup(Edge(self.front,self.activation,H),Edge(self.activation,self.rear,H),Edge(self.rear,self.model_output,OUTPUT))
        super().__init__(self.edges,self.sentence,self.front,self.activation,self.rear,self.model_output)
        if probe:
            self.edges.add(Edge(self.activation,self.probe,GOOD),Edge(self.probe,self.probe_output,GOOD))
            self.add(self.probe,self.probe_output)

class DualPathView(VGroup):
    same_input=True
    same_downstream_weights=True
    intervention_target='activation'
    def __init__(self,portrait=False):
        cx,cy=center(portrait)
        self.header=card('동일 입력 · 원래 모델 가중치 고정',cx,cy+2.2,6.6,.65,MUTED,23)
        self.h=card('Baseline · h',cx-1.7,cy+1,2.85,.65,H,25)
        self.hp=card('Intervention · h′=Ph',cx+1.7,cy+1,2.85,.65,CHANGED,21)
        self.rears=VGroup(*[card('원 모델 뒷부분\n동일한 파라미터',cx+dx,cy-.25,2.85,1,MUTED,22) for dx in [-1.7,1.7]])
        self.outputs=VGroup(card('원 모델 예측\np(y | h)',cx-1.7,cy-1.8,2.85,1.15,OUTPUT,23),
            card('개입 후 모델 예측\np(y | h′)',cx+1.7,cy-1.8,2.85,1.15,OUTPUT,22))
        edges=VGroup(*[Edge(a,b,H if j==0 else CHANGED) for j,(a,b) in enumerate(zip([self.h,self.hp],self.rears))],
            *[Edge(a,b,OUTPUT) for a,b in zip(self.rears,self.outputs)])
        super().__init__(edges,self.header,self.h,self.hp,self.rears,self.outputs)

class ProjectionPlane(VGroup):
    measured=False
    single_step_is_illustration=True
    def __init__(self,portrait=False,confound=False):
        cx,cy=center(portrait);side=5.4 if portrait else 4.8
        self.axes=Axes(x_range=[-2,2,1],y_range=[-2,2,1],x_length=side,y_length=side,
            tips=False,axis_config=dict(include_ticks=False,color=MUTED,stroke_width=1.5)).move_to(p(cx,cy))
        self.origin=self.axes.c2p(0,0)
        self.point=lambda x:self.axes.c2p(*x)
        self.direction=Arrow(self.origin,self.point(W*1.6),buff=0,color=INTERVENTION,stroke_width=4)
        self.kept=Line(self.point([-1.7,1.7]),self.point([1.7,-1.7]),color=CHANGED,stroke_width=2)
        self.dots=VGroup(*[Dot(self.point(x),radius=.065,color=GOOD if i<3 else OUTPUT) for i,x in enumerate(SAMPLES)])
        self.paths=VGroup(*[DashedLine(self.point(x),self.point(PROJECTION@x),color=MUTED,dash_length=.09,stroke_width=1) for x in SAMPLES])
        self.h=Arrow(self.origin,self.point(SAMPLES[0]),buff=0,color=H,stroke_width=4)
        self.hp=Arrow(self.origin,self.point(PROJECTION@SAMPLES[0]),buff=0,color=CHANGED,stroke_width=4)
        self.confound=confound
        if confound:
            self.other=Arrow(self.origin,self.point(OTHER),buff=0,color=PRUNE,stroke_width=5)
            self.other_after=Arrow(self.origin,self.point(PROJECTION@OTHER),buff=0,color=PRUNE,stroke_width=4)
            self.other_path=DashedLine(self.point(OTHER),self.point(PROJECTION@OTHER),color=PRUNE,dash_length=.08)
            super().__init__(self.axes,self.kept,self.direction,self.other,
                label('제거 방향 w',cx+1.3,cy+1.5,21,INTERVENTION,2.5),label('다른 정보 u',cx-1.05,cy-1.6,21,PRUNE,2.6))
        else:
            super().__init__(self.axes,self.kept,self.direction,self.dots,
                label('POS 판독 방향 w',cx+1.2,cy+1.6,21,INTERVENTION,3),
                label('품사 분포의 2D 가상 예시',cx,cy-2.2,18,MUTED,6.7))
    def project(self,scene):
        if self.confound:
            self.add(self.other_path,self.other_after);scene.play(Create(self.other_path),GrowArrow(self.other_after),run_time=1)
        else:
            self.add(self.paths,self.h,self.hp)
            scene.play(Create(self.paths),GrowArrow(self.h),run_time=.65)
            scene.play(*[dot.animate.move_to(self.point(PROJECTION@x)) for dot,x in zip(self.dots,SAMPLES)],GrowArrow(self.hp),run_time=1.1)

class PredictionComparison(VGroup):
    measured=False
    def __init__(self,portrait=False):
        cx,cy=center(portrait);self.cx=cx;self.cy=cy
        self.groups=VGroup();self.bars=VGroup()
        for j,(x,title) in enumerate([(cx-1.75,'개입 전 · h'),(cx+1.75,'개입 후 · h′')]):
            self.groups.add(VGroup(card(title,x,cy+1.9,2.9,.65,H if j==0 else CHANGED,24),
                card('동일한 원 모델\n뒷부분 가중치',x,cy+.65,2.9,1,MUTED,22)))
            bars=VGroup()
            for k,value in enumerate([.75,.25]):
                bar=Rectangle(width=.65,height=1.6*value,stroke_width=0,fill_color=OUTPUT if j==0 else CHANGED,fill_opacity=.9)
                bar.move_to(p(x+(k-.5)*1.1,cy-1.7+bar.height/2));bars.add(bar)
            self.bars.add(bars)
            self.groups.add(label('Token A   Token B',x,cy-2.05,18,MUTED,3))
        super().__init__(self.groups,self.bars)
    def change(self,scene,values):
        animations=[]
        for old,value in zip(self.bars[1],values):
            new=old.copy().stretch_to_fit_height(1.6*value);new.move_to(p(old.get_x(),self.cy-1.7+new.height/2))
            animations.append(Transform(old,new))
        scene.play(*animations,run_time=1)

class EvidencePanels(VGroup):
    def __init__(self,portrait=False):
        cx,cy=center(portrait);ys=[3.5,1.6,-.3] if portrait else [1.45,.05,-1.35]
        self.panels=VGroup(*[card(s,cx,y,6.6,1.1,col,25) for s,y,col in zip(
            ['01 · Probing\n어떤 정보가 읽히는가?', '02 · Intervention\n바꾸면 행동이 달라지는가?',
             '03 · Mechanistic Explanation\n어떤 경로로 출력에 기여하는가?'],ys,[GOOD,INTERVENTION,H])])
        super().__init__(self.panels)

class LearningValidationView(VGroup):
    requires_retraining=True
    def __init__(self,portrait=False):
        cx,cy=center(portrait)
        self.weights=patterning.DataReweightingView().scale(.7).move_to(p(cx,cy+1.25))
        self.train=card('데이터 재가중 → 새로 학습',cx,cy-.35,6.6,.7,GOOD,25)
        self.nodes=VGroup(*[card(s,cx+dx,cy-1.85,1.9,.75,col,23) for s,dx,col in zip(['F1','F2','출력 ?'],[-2.2,0,2.2],[H,H,OUTPUT])])
        edges=VGroup(*[Edge(a,b,MUTED) for a,b in zip(self.nodes,self.nodes[1:])])
        super().__init__(self.weights,self.train,edges,self.nodes)

class ProbingVideo(circuits.CircuitTracingVideo):
    SECTION=None
    def construct(self):
        self.portrait=PORTRAIT;P=PORTRAIT;data=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
        selected=data['segments'] if self.SECTION is None else [data['segments'][self.SECTION]]
        self.offset=selected[0]['start'];self.view=VGroup();self.info=VGroup();self.aux=VGroup();self.heading=VGroup();self.caption=VGroup()
        self.fixed=VGroup(label('신경망 내부의 계산  07',x=0 if P else -5.2,y=7.4 if P else 4.08,size=20 if P else 18,color=MUTED,width=7.5 if P else 5),
            label('읽을 수 있는 정보와\n실제로 쓰이는 정보' if P else '신경망이 알고 있는 정보와 실제 계산에 사용하는 정보를 구별하는 방법',
                x=0 if P else 2.4,y=6.5 if P else 4.08,size=29 if P else 21,width=7.5 if P else 9.8),
            Line(p(-3.9 if P else -7.4,5.75 if P else 3.65),p(3.9 if P else 7.4,5.75 if P else 3.65),color=ZERO),
            RoundedRectangle(width=7.9 if P else 15,height=1.85 if P else 1.04,corner_radius=.1,stroke_width=0,
                fill_color='#14212D',fill_opacity=.95).move_to(p(0,-6.2 if P else -3.65)),
            label('도식·분포는 가상 예시 · Elazar et al., 2021',y=-7.45 if P else -4.3,size=15,color=MUTED,width=7.5 if P else 14))
        self.add(self.fixed)
        for seg in selected:
            self.to(seg['start'])
            for obj in list(self.mobjects):
                if obj is not self.fixed:self.remove(obj)
            self.view=VGroup();self.info=VGroup();self.aux=VGroup()
            self.heading=label(f'{seg["index"]:02}  {seg["title"]}',y=5.25 if P else 3.12,size=23 if P else 28,color=ACCENT,width=7.7 if P else 14.5)
            self.add(self.heading);self.setup_section(seg['index']-1)
            for q in seg['cues']:
                self.to(q['start']);self.remove(self.caption);self.caption=self.caption_obj(q['text']);self.add(self.caption)
                self.event(q['index']);self.to(q['end'])
        self.to(selected[-1]['end'])
    def setup_section(self,k):
        P=self.portrait
        if k==0:self.set_view(ReadoutModelView(P,probe=False))
        elif k==1:self.set_view(ReadoutModelView(P))
        elif k==2:self.set_view(DualPathView(P))
        elif k==3:self.set_view(PredictionComparison(P))
        elif k==4:self.set_view(EvidencePanels(P))
        else:self.set_view(LearningValidationView(P))
    def event(self,i):
        P=self.portrait;cx,cy=center(P)
        if i==0:self.panel('정보의 존재 = 실제 사용?',['활성화 h에서 읽을 수 있다면','모델이 그 정보를 쓰고 있을까?'])
        elif i==1:self.panel('언어 모델에 영어 문장을 입력',['하나의 입력과 내부 활성화','원래 모델의 계산을 관찰한다'])
        elif i==2:
            nodes=VGroup(*[card(s,cx+dx,cy+1.1,1.55,.75,col,25) for s,dx,col in zip(['The','cats','are','sleeping'],[-2.55,-.85,.85,2.55],[INK,GOOD,GOOD,INK])])
            self.set_view(VGroup(nodes,card('고양이들이 자고 있다.',cx,cy-1.1,6.6,1,MUTED,28)))
            self.panel('The cats are sleeping',['문장 구성 요소를 나눈 예시','실제 네 토큰 분할을 뜻하지 않음'],[INK,MUTED]);self.pulse(nodes[1],nodes[2])
        elif i==3:self.panel('cat + s → Plural',['cats는 복수형']);self.pulse(self.view[0][1])
        elif i==4:
            self.set_view(ReadoutModelView(P,probe=False));self.panel('대상 단어 위치의 활성화 h',['h = (h₁, h₂, …, h_d)','특정 좌표를 복수형 뉴런으로 단정하지 않음'],[H,MUTED]);self.pulse(self.view.activation)
        elif i==5:self.panel('Linear Probing · 선형 탐침',['원래 모델과 별도의 분류기','단수·복수 정보의 판독 가능성'],[GOOD,INK]);self.pulse(self.view.probe)
        elif i==6:
            self.panel('원 모델 고정 · 활성화 수집',['The cat is sleeping → Singular','The cats are sleeping → Plural','대상 단어의 h와 정답 라벨 수집'])
            self.note('분류기 학습 자료를 모으는 단계 · 원래 Transformer를 재학습하지 않음')
        elif i==7:self.clear_aux();self.panel('Probe의 w,b만 학습한다',['p(plural | h) = σ(wᵀh + b)','Probe 분류 오류로 w,b 갱신','원 모델의 가중치는 고정'],[GOOD,INK,MUTED]);self.pulse(self.view.probe)
        elif i==8:
            self.panel('새 문장에서도 높은 정확도라면',['학습 밖 자료 · Held-out Data','Linear Decodability의 근거','실제 측정 정확도를 제시한 장면은 아님'],[INK,GOOD,MUTED]);self.pulse(self.view.probe_output)
        elif i==9:self.panel('하지만 원래 모델도 사용했을까?',['Accurate Probe','Original Model Uses It?'],[GOOD,ACCENT])
        elif i==10:self.panel('판독 가능성 ≠ 실제 사용의 증명',['Decodable','Causally Used?'],[GOOD,ACCENT]);self.pulse(self.view.probe_output,self.view.model_output)
        elif i==11:self.panel('Probe는 별도로 학습한 모델',['청록: Probe의 단수·복수 판독','파랑: 원 모델의 토큰 예측'],[GOOD,OUTPUT]);self.pulse(self.view.probe)
        elif i==12:self.panel('사용하지 않는 정보도 읽힐 수 있다',['Probe 판독과 원 모델 계산은 별개','판독창에서 원 모델로 피드백하지 않는다'],[INK,MUTED]);self.pulse(self.view.activation)
        elif i==13:self.panel('실제 계산의 필요성을 확인하려면?',['같은 입력 · 같은 모델','내부 활성화만 바꿔 비교한다'])
        elif i==14:self.panel('Read → Remove',['정보가 있는가?','제거하면 계산이 달라지는가?'],[GOOD,INTERVENTION])
        elif i==15:self.panel('h와 h′를 같은 뒷부분에 전달',['Baseline: h','Intervention: h′','원래 모델의 가중치는 동일'],[H,CHANGED,MUTED]);self.pulse(self.view.h,self.view.hp)
        elif i==16:self.panel('Amnesic Probing',['정보 제거 개입으로 행동 변화를 분석','Elazar et al., 2021'],[INTERVENTION,MUTED])
        elif i==17:
            self.set_view(ProjectionPlane(P));self.panel('분석 속성 전환: Number → POS',['Noun / Verb / Adjective …','품사를 구분하는 선형 방향 w 찾기'],[INTERVENTION,INK])
            self.note('고차원 활성화의 2D 가상 분포 · 실제 모델의 품사 군집 재현이 아님')
        elif i==18:
            self.clear_aux()
            self.panel('h′ = Ph · 판독 방향에 수직으로 투영',['P = I − wwᵀ · ‖w‖=1 · 한 단계','INLP: Probe 재학습 → 투영을 반복','새 Probe로 선형 판독 약화 여부 평가'],[CHANGED,INK,MUTED]);self.view.project(self)
            self.note('모든 정보의 완전 삭제를 뜻하지 않음 · 비선형 정보는 남을 수 있음')
        elif i==19:self.set_view(DualPathView(P));self.panel('변환된 h′를 원래 모델에 전달',['속성: POS · Number 실험과 구별','입력과 뒷부분 가중치는 동일','활성화 변환 · 뉴런 삭제가 아님'],[INTERVENTION,INK,MUTED]);self.pulse(self.view.hp)
        elif i==20:self.panel('원 모델의 예측을 비교한다',['Baseline: p(y | h)','Intervention: p(y | h′)'],[OUTPUT,CHANGED]);self.pulse(self.view.outputs)
        elif i==21:
            self.panel('가상 예시 A · 행동이 달라진다면',['제거한 표현의 행동상 영향에 관한 근거','품사 정보만의 효과인지는 아직 모른다'],[OUTPUT,MUTED]);self.view.change(self,[.3,.7]);self.note('분포 막대는 설명용 가상 예시 · 논문의 실측 결과나 실제 확률이 아님')
        elif i==22:self.panel('가상 예시 B · 거의 달라지지 않는다면',['해당 예측에서 사용하지 않았을 가능성','다른 표현·비선형 정보로 보완 가능','출력 비교만으로 어느 쪽인지 확정 불가'],[INK,INK,MUTED]);self.view.change(self,[.74,.26])
        elif i==23:self.panel('개입에서도 확인할 문제가 있다',['What else was removed?'],[PRUNE])
        elif i==24:
            self.set_view(ProjectionPlane(P,confound=True));self.panel('같은 제거 방향에 다른 정보도 있다면?',['POS 방향 w와 다른 정보 u가 겹침','Pu ≠ u · 다른 정보도 함께 손상'],[INTERVENTION,PRUNE]);self.view.project(self)
            self.note('방향의 겹침을 설명하는 가상 예시 · 특정 모델의 실제 정보 배치 아님')
        elif i==25:
            nodes=VGroup(card('POS 표현 변경',cx-1.8,cy+1.2,3,.9,INTERVENTION,23),card('다른 정보 손상',cx+1.8,cy+1.2,3,.9,PRUNE,23),card('출력 변화의 원인 ?',cx,cy-1.15,5,1,OUTPUT,26))
            self.set_view(VGroup(Edge(nodes[0],nodes[2],INTERVENTION),Edge(nodes[1],nodes[2],PRUNE),nodes))
            self.panel('변화의 원인을 분리해야 한다',['출력이 달라졌다는 사실','어떤 정보의 효과인지는 별도 검증'])
        elif i==26:self.panel('Intervention Effect ≠ 완전한 설명',['Output Changed ✓','Exact Mechanism Identified ?'],[OUTPUT,ACCENT])
        elif i==27:self.panel('서로 다른 세 가지 질문',['판독 · 행동 영향 · 계산 경로','우열이 아닌 질문과 근거의 구분'])
        elif i in (28,29,30):
            titles=['01 · 어떤 정보를 읽을 수 있는가?','02 · 바꾸면 행동이 달라지는가?','03 · 어떤 경로로 영향을 주는가?']
            self.panel(titles[i-28],['서로 다른 질문에 대한 증거를 모은다']);self.pulse(self.view.panels[i-28])
        elif i==31:self.panel('Probing과 Intervention의 역할',['Probe → 판독 가능성','개입 → 행동상 영향'],[GOOD,INTERVENTION]);self.pulse(self.view.panels[0],self.view.panels[1])
        elif i==32:self.panel('경로 가설 + 개입 결과를 함께 분석',['중간 계산 관계와 예측을 대조','가설을 더 구체적으로 검증한다','한 실험으로 완전한 알고리즘 확정은 아님'],[H,INTERVENTION,MUTED]);self.pulse(self.view.panels[2])
        elif i==33:self.panel('학습 데이터 → 내부 계산 형성',['원하는 회로를 유도했다면','무엇을 근거로 확인할까?'])
        elif i==34:
            self.panel('유도한 회로를 실제로 학습했을까?',['데이터 재가중 → 새로 학습','형성된 내부 구조와 역할을 조사','이미 학습한 회로를 즉시 바꾸는 뜻은 아님'],[GOOD,H,MUTED]);self.view.weights.reweight(self);self.pulse(self.view.train);self.pulse(self.view.nodes)
        elif i==35:self.panel('정답 변화만으로는 충분하지 않다',['Behavior Alone ≠ Complete Mechanism','같은 답과 다른 계산도 가능'],[OUTPUT,MUTED])
        elif i==36:self.panel('무엇이 형성됐고, 어떻게 쓰이는가?',['표현 관찰 · 계산 경로 가설','개입 결과와 대조 실험으로 검증'],[H,INTERVENTION]);self.pulse(self.view.nodes)

class ProbingIntervention(ProbingVideo):pass
class ProbingInterventionShorts(ProbingVideo):pass
class ProbeIntroduction(ProbingVideo):SECTION=0
class LinearProbeTraining(ProbingVideo):SECTION=1
class AmnesicIntervention(ProbingVideo):SECTION=2
class BehaviorComparison(ProbingVideo):SECTION=3
class EvidenceLevels(ProbingVideo):SECTION=4
class PatterningValidationBridge(ProbingVideo):SECTION=5
