"""Series finale: distinguish behavior, explain computation, test and influence."""
import json
import os
import sys
from pathlib import Path
import numpy as np
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.nncalc01_same_answers import scene as brackets
from episodes.nncalc03_patterning import scene as patterning
from episodes.nncalc04_feature_superposition import scene as superposition
from episodes.nncalc05_sparse_autoencoders import scene as sae
from episodes.nncalc06_circuit_tracing import scene as circuits
from episodes.nncalc07_probing_intervention import scene as probing
from visual_library.manim import BG,INK,MUTED,ACCENT,GOOD,PRUNE,ZERO
config.pixel_width=int(os.environ.get('VIDEO_WIDTH','1920'))
config.pixel_height=int(os.environ.get('VIDEO_HEIGHT','1080'))
PORTRAIT=config.pixel_height>config.pixel_width
config.frame_width=9 if PORTRAIT else 16;config.frame_height=16 if PORTRAIT else 9
config.frame_rate=30;config.background_color=BG;config.disable_caching=True
HERE=Path(__file__).resolve().parent
label=circuits.label;card=circuits.card;p=circuits.p;Edge=circuits.ContributionEdge
COUNT='#F7A65E';PREFIX=GOOD;PATH='#B39CFF';DATA='#7EB8F3'
center=probing.center

def depths(s):return np.r_[0,np.cumsum([1 if c=='(' else -1 for c in s])]
def count_rule(s):return s.count('(')==s.count(')')
def nested_rule(s):
    d=depths(s);return bool(d[-1]==0 and np.min(d)>=0)

class BracketAlgorithms(VGroup):
    extracted_neural_circuit=False
    def __init__(self,s='(()())',portrait=False):
        cx,cy=center(portrait);self.string=s
        self.seq=brackets.BracketSequence(s,cx,cy+1.65,INK)
        valid=nested_rule(s);n=s.count('(');m=s.count(')')
        self.a=card(f'A · 총개수 비교\n{n} = {m} → '+('수락' if valid else '수락 (오판)'),cx-1.7,cy-.15,3.1,1.35,COUNT,23)
        self.b=card('B · 접두 균형\n'+('음수 없음 → 수락' if valid else '중간 −1 → 거부'),cx+1.7,cy-.15,3.1,1.35,PREFIX,23)
        super().__init__(self.seq,self.a,self.b,label('일부 입력의 같은 답 · 서로 다른 규칙' if valid else '같은 개수 · 서로 다른 판단',cx,cy-1.75,25,INK,6.8))

class BracketPrefixGraph(VGroup):
    def __init__(self,s='())(',portrait=False):
        cx,cy=center(portrait);self.values=depths(s);self.string=s
        self.seq=brackets.BracketSequence(s,cx,cy+1.65,PREFIX)
        self.point=lambda i,v:p(cx-2.35+4.7*i/len(s),cy-.7+.62*v)
        axes=VGroup(Line(self.point(0,0),self.point(len(s),0),color=MUTED),Line(self.point(0,-1),self.point(0,2),color=ZERO))
        self.path=VGroup();self.dot=Dot(self.point(0,0),radius=.06,color=PREFIX)
        self.readout=label('접두 깊이 0',cx,cy-1.9,25,PREFIX,6.6)
        super().__init__(self.seq,axes,self.path,self.dot,self.readout)
    def run(self,scene):
        for i,value in enumerate(self.values[1:],1):
            color=PRUNE if value<0 else PREFIX
            edge=Line(self.point(i-1,self.values[i-1]),self.point(i,value),color=color,stroke_width=4)
            self.path.add(edge)
            scene.play(Create(edge),self.dot.animate.move_to(self.point(i,value)).set_color(color),
                Transform(self.readout,label(f'접두 깊이 {value}',self.readout.get_x(),self.readout.get_y(),25,color,6.6)),
                Indicate(self.seq[i-1],color=color),run_time=.4)
            if value<0:scene.wait(.35)
        valid=np.min(self.values)>=0 and self.values[-1]==0
        scene.play(Transform(self.readout,label('최종 0 · 음수 없음' if valid else '최종 0 · 중간 −1 위반',
            self.readout.get_x(),self.readout.get_y(),25,PREFIX if valid else PRUNE,6.6)),run_time=.3)

class DirectionQuestionView(VGroup):
    def __init__(self,portrait=False):
        cx,cy=center(portrait);self.cx=cx;self.cy=cy
        self.nodes=VGroup(*[card(s,cx+dx,cy,1.95,1.2,col,24) for s,dx,col in
            [('Data\n데이터',-2.25,DATA),('Learning\n학습',0,MUTED),('Circuit\n내부 계산',2.25,PATH)]])
        self.edges=VGroup(*[Edge(a,b,PATH) for a,b in zip(self.nodes,self.nodes[1:])])
        self.description=label('데이터와 학습에서 나타난 내부 구조를 조사',cx,cy-1.65,23,INK,6.8)
        super().__init__(self.edges,self.nodes,self.description)
    def reverse_question(self,scene):
        new=VGroup(*[card(s,self.cx+dx,self.cy,1.95,1.2,col,23) for s,dx,col in
            [('Data\n조절 방향',-2.25,DATA),('Inverse\n추정',0,ACCENT),('Target\n목표 계산',2.25,PATH)]])
        edges=VGroup(Edge(new[2],new[1],ACCENT),Edge(new[1],new[0],ACCENT))
        scene.play(Transform(self.nodes,new),Transform(self.edges,edges),
            Transform(self.description,label('목표 내부 구조에서 데이터 조절 방향을 묻는다',self.cx,self.cy-1.65,23,ACCENT,6.8)),run_time=1)

class LocalResponseView(VGroup):
    requires_retraining=True
    local_approximation=True
    def __init__(self,portrait=False):
        cx,cy=center(portrait)
        self.weights=patterning.DataReweightingView().scale(.75).move_to(p(cx,cy+1.35))
        self.train=card('데이터 비중 변경 → 새 학습',cx,cy-.3,6.5,.75,DATA,25)
        self.observable=card('내부 관측량 μ의 변화',cx,cy-1.75,6.5,.75,PATH,25)
        super().__init__(self.weights,self.train,self.observable,Edge(self.train,self.observable,PATH))
    def measure(self,scene):self.weights.reweight(scene);scene.pulse(self.train);scene.pulse(self.observable)
    def set_goal(self,scene):
        scene.play(Transform(self.observable,card('목표 Δμ 지정 → 데이터 방향 추정',self.observable.get_x(),self.observable.get_y(),6.5,.75,ACCENT,24)),run_time=.7)
        scene.pulse(self.weights)

class FinalCircuitView(VGroup):
    complete_circuit=False
    unverified_edges_dashed=True
    def __init__(self,portrait=False):
        cx,cy=center(portrait)
        self.input=card('입력',cx,cy+1.7,3.2,.7,MUTED,25)
        self.paths=VGroup(card('후보 경로 A\n계산 ?',cx-1.75,cy+.05,2.8,1.15,COUNT,24),
            card('후보 경로 B\n계산 ?',cx+1.75,cy+.05,2.8,1.15,PREFIX,24))
        self.output=card('출력',cx,cy-1.6,3.2,.7,INK,25)
        self.edges=VGroup()
        for a,b in [(self.input,n) for n in self.paths]+[(n,self.output) for n in self.paths]:
            edge=Edge(a,b,MUTED)
            self.edges.add(DashedLine(edge.get_start(),edge.get_end(),color=MUTED,dash_length=.12,stroke_width=1.5).add_tip(tip_length=.12))
        self.tag=label('Discover → Explain → Test',cx,cy-2.3,24,ACCENT,6.8)
        super().__init__(self.edges,self.input,self.paths,self.output,self.tag)

class FinaleVideo(probing.ProbingVideo):
    SECTION=None
    def construct(self):
        self.portrait=PORTRAIT;P=PORTRAIT;data=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
        selected=data['segments'] if self.SECTION is None else [data['segments'][self.SECTION]]
        self.offset=selected[0]['start'];self.view=VGroup();self.info=VGroup();self.aux=VGroup();self.heading=VGroup();self.caption=VGroup()
        self.fixed=VGroup(label('신경망 내부의 계산  08 · 마지막 편',x=0 if P else -4.9,y=7.4 if P else 4.08,size=19 if P else 18,color=MUTED,width=7.5 if P else 5.5),
            label('알고리즘의 발견에서\n형성을 유도하는 것까지' if P else '신경망의 알고리즘을 발견하는 것에서 형성을 유도하는 것까지',
                x=0 if P else 2.65,y=6.5 if P else 4.08,size=29 if P else 21,width=7.5 if P else 9.3),
            Line(p(-3.9 if P else -7.4,5.75 if P else 3.65),p(3.9 if P else 7.4,5.75 if P else 3.65),color=ZERO),
            RoundedRectangle(width=7.9 if P else 15,height=1.85 if P else 1.04,corner_radius=.1,stroke_width=0,
                fill_color='#14212D',fill_opacity=.95).move_to(p(0,-6.2 if P else -3.65)),
            label('연구 원리의 개념도 · Patterning: Wang & Murfet, 2026',y=-7.45 if P else -4.3,size=15,color=MUTED,width=7.5 if P else 14))
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
        if k==0:self.set_view(FinalCircuitView(P))
        elif k==1:self.set_view(BracketPrefixGraph('())(',P))
        elif k==2:self.set_view(patterning.InductionCircuitView(*center(P),w=5.7))
        elif k==3:self.set_view(DirectionQuestionView(P))
        elif k==4:self.set_view(LocalResponseView(P))
        else:self.set_view(FinalCircuitView(P))
    def event(self,i):
        P=self.portrait;cx,cy=center(P)
        if i==0:self.panel('Correct Answer = Correct Algorithm?',['정답만으로는 내부 규칙을 모른다']);self.pulse(self.view.output)
        elif i==1:self.set_view(BracketAlgorithms('(()())',P));self.panel('괄호 문자열 판별',['(()()) · 올바른 문자열','두 수학적 규칙을 비교한다'])
        elif i==2:
            self.set_view(VGroup(brackets.BracketSequence('(((',cx,cy+1,COUNT),brackets.BracketSequence(')))',cx,cy-.5,COUNT),label('3 = 3',cx,cy-1.8,36,COUNT,6.8)))
            self.panel('A · 전체 개수만 비교',['여는 괄호 3개 · 닫는 괄호 3개','순서는 보지 않는 규칙'],[COUNT,MUTED])
        elif i==3:self.set_view(BracketPrefixGraph('(()())',P));self.panel('B · 모든 접두 구간의 균형',['최종 깊이 0','한 번도 0 아래로 내려가지 않기'],[PREFIX,PREFIX]);self.view.run(self)
        elif i==4:self.set_view(BracketAlgorithms('(()())',P));self.panel('같은 답 · 서로 다른 규칙',['(()())와 ()()에서는 모두 통과','모든 입력에서 같은 규칙은 아니다'],[INK,MUTED]);self.pulse(self.view.a,self.view.b)
        elif i==5:self.panel('어느 규칙을 배웠는지 구별하려면?',['정답이 같았던 입력만 보지 말고','규칙이 갈리는 입력을 찾아야 한다'])
        elif i==6:self.panel('Distinguishing Input',['두 알고리즘의 답이 갈리는 입력','규칙을 구별하기 위한 행동 시험'])
        elif i==7:self.panel('새 입력: ())( ',['여는 괄호 2개 · 닫는 괄호 2개','왼쪽부터 읽으면 1 → 0 → −1 → 0']);self.view.run(self)
        elif i==8:self.panel('개수는 같지만 중간 균형이 깨진다',['세 번째 위치에서 깊이 −1','최종 0만으로는 올바르지 않다'],[PRUNE,MUTED]);self.pulse(self.view.seq[2])
        elif i==9:self.set_view(BracketAlgorithms('())(',P));self.panel('행동으로 두 규칙 후보를 구별',['A: 수락 · 개수만 같아서 오판','B: 거부 · 중간 위반을 감지'],[COUNT,PREFIX])
        elif i==10:self.panel('Correct Behavior ≠ Unique Mechanism',['시험 통과는 행동에 대한 근거','정확한 내부 구현을 확정하지는 못한다'],[INK,MUTED])
        elif i==11:self.set_view(circuits.DenseNeuralView(P));self.panel('모델의 내부 계산으로',['어떤 계산이 형성되었을까?'])
        elif i==12:
            self.set_view(patterning.InductionCircuitView(cx,cy-.35,w=5.7))
            head=self.view.heads[1]
            head.become(card('Head 2 · Induction\n앞 A 이력이 있는\nB 위치를 참조',head.get_x(),head.get_y(),head.width,head.height,PATH,24))
            self.extra(card('A B C D A → B',cx,cy+2,6.5,.65,PATH,29))
            self.panel('두 헤드가 연결된 패턴 이어받기',['이전 토큰 정보를 옮기는 헤드','그 정보를 이용해 다음 토큰을 찾는 헤드'])
            self.pulse(self.view.heads[0]);self.pulse(self.view.heads[1])
        elif i==13:self.set_view(superposition.FeaturePlane(P));self.view.set_features(self,superposition.REGULAR);self.panel('뉴런 하나 = 특징 하나는 아니다',['뉴런: 좌표축 · 특징: 방향','2차원 공간을 공유하는 다섯 방향'],[MUTED,GOOD])
        elif i==14:self.set_view(sae.SparseAutoencoderView(P));self.view.activate(self,sae.EXAMPLES[0]);self.panel('Sparse Autoencoder',['혼합 활성화 → 희소 잠재값 → 복원','해석 가능한 특징 후보','완전한 정답 특징 복원을 보장하지 않음'],[GOOD,GOOD,MUTED])
        elif i==15:self.set_view(circuits.AttributionGraphView(P,named=False));self.panel('특징 사이의 기여 관계를 추적',['특정 출력에 이르는 경로 가설','SAE와 CLT가 같은 사전이라는 뜻은 아님'],[PATH,MUTED]);self.view.trace(self)
        elif i==16:self.set_view(probing.ReadoutModelView(P));self.panel('Readable ≠ Proven Causal Use',['Probe로 읽을 수 있는 정보','원 모델이 실제 쓰는지는 다른 질문'],[GOOD,ACCENT]);self.pulse(self.view.probe_output,self.view.model_output)
        elif i==17:self.set_view(probing.DualPathView(P));self.panel('판독과 개입으로 서로 다른 근거 수집',['h → h′ · 같은 원 모델의 뒷부분','p(y | h)와 p(y | h′)를 비교','변화 하나로 완전한 인과 설명은 아님'],[PATH,ACCENT,MUTED]);self.pulse(self.view.hp)
        elif i==18:self.panel('모든 분석이 향하는 질문',['어떤 알고리즘이 학습되었는가?','무엇을 근거로 설명할 수 있는가?'])
        elif i==19:self.panel('What algorithm did the model learn?',['내부 구조에 관한 가설','가설을 지지하거나 반박하는 증거'],[PATH,ACCENT]);self.pulse(self.view.nodes[2])
        elif i==20:self.panel('질문의 방향을 바꿔보면?',['Data → Learning → Circuit']);self.view.reverse_question(self)
        elif i==21:self.panel('목표 계산 → 데이터 조절 방향',['학습된 계산을 발견하는 질문에서','원하는 계산의 형성을 유도하는 질문으로'],[PATH,DATA]);self.note('역방향은 설계 질문 · 실제 학습은 데이터에서 모델로 진행')
        elif i==22:self.panel('Patterning · ICML 2026',['The Dual of Interpretability','Wang & Murfet'],[DATA,MUTED])
        elif i==23:
            self.panel('작은 데이터 변화와 내부 관측량',['Δμ ≈ χ Δh · 국소 반응 관계','정방향 측정 → 목표 변화의 역추정'],[PATH,DATA]);self.view.measure(self)
            self.to(122);self.view.set_goal(self)
            self.note('μ: 사후 기대 관측량 · 작은 변화의 근사 · 임의 목표 도달을 보장하지 않음')
        elif i==24:
            plot=patterning.CircuitFormationPlot(False);plot.scale_to_fit_width(6.5).move_to(p(cx,cy))
            self.set_view(plot);self.panel('작은 언어 모델의 회로 형성 시점',['데이터 재가중으로 앞당기거나 늦추기','곡선은 결과 방향의 개념도'],[DATA,MUTED]);plot.form(self)
        elif i==25:self.set_view(BracketAlgorithms('())(',P));self.panel('별도 실험: 합성 괄호 문제',['같은 훈련 정확도 · 다른 일반화','재가중으로 알고리즘 선택에 영향','그림은 새 입력에서의 규칙 비교'],[INK,DATA,MUTED])
        elif i==26:self.set_view(FinalCircuitView(P));self.panel('임의의 알고리즘을 자유롭게 설계?',['작은 모델·제한된 과제에서의 결과','모든 신경망의 완전한 제어를 뜻하지 않음'],[PRUNE,MUTED])
        elif i==27:self.set_view(probing.EvidencePanels(P));self.panel('관측한 구조의 실제 역할도 검증',['어떤 계산을 수행하는가?','데이터 개입 뒤에도 같은 역할인가?','관측량 변화만으로 결론 내리지 않는다'],[PATH,ACCENT,MUTED]);self.pulse(self.view.panels[1],self.view.panels[2])
        elif i==28:self.panel('출발점: 모델이 맞힌 정답',['무엇을 출력하는지 관찰했다']);self.pulse(self.view.output)
        elif i==29:self.panel('특징 발견 → 경로 추적 → 역할 검증',['표현과 계산의 후보를 찾고','실제로 작동하는지 시험한다'],[GOOD,ACCENT]);self.pulse(self.view.paths)
        elif i==30:self.panel('이해를 바탕으로 학습 형성에 영향',['발견한 구조 → 목표 관측량','데이터 조절 → 새 학습과 검증'],[PATH,DATA])
        elif i==31:self.panel('정답을 아는 것만으로는 충분하지 않다',['무엇을 맞혔나?','어떤 계산으로 도달했나?'],[MUTED,PATH])
        elif i==32:self.panel('설명하고, 그 설명을 시험하는 일',['Discover → Explain → Test','남은 불확실성까지 검증할 수 있는 설명'],[ACCENT,MUTED]);self.pulse(self.view.paths);self.pulse(self.view.tag)

class InterpretabilityPatterningFinale(FinaleVideo):pass
class InterpretabilityPatterningFinaleShorts(FinaleVideo):pass
class SameAnswerDifferentAlgorithm(FinaleVideo):SECTION=0
class DistinguishingTest(FinaleVideo):SECTION=1
class MechanisticMethodsRecap(FinaleVideo):SECTION=2
class InterpretabilityToPatterning(FinaleVideo):SECTION=3
class PatterningLearningControl(FinaleVideo):SECTION=4
class SeriesFinale(FinaleVideo):SECTION=5
