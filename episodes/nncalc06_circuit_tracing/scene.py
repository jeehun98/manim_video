"""Circuit tracing: approximation, attribution and original-model validation."""
import json
import os
import sys
from pathlib import Path
import numpy as np
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.nncalc05_sparse_autoencoders import scene as sae
from visual_library.manim import BG,INK,MUTED,ACCENT,GOOD,PRUNE,ZERO
config.pixel_width=int(os.environ.get('VIDEO_WIDTH','1920'))
config.pixel_height=int(os.environ.get('VIDEO_HEIGHT','1080'))
PORTRAIT=config.pixel_height>config.pixel_width
config.frame_width=9 if PORTRAIT else 16;config.frame_height=16 if PORTRAIT else 9
config.frame_rate=30;config.background_color=BG;config.disable_caching=True
HERE=Path(__file__).resolve().parent
label=sae.label;card=sae.card;p=sae.p;arrow=sae.arrow
FEATURE=GOOD;ATTR='#B39CFF';INTERVENTION='#F7A65E';ERROR=PRUNE
PROMPT='댈러스가 속한 주의 주도는 어디인가?'

def feature_node(name,x,y,w=1.85,color=FEATURE):return card(name,x,y,w,.85,color,22)

class ContributionEdge(Arrow):
    measured=False
    def __init__(self,a,b,color=ATTR,width=2.5):
        delta=b.get_center()-a.get_center()
        def boundary(obj,direction):
            dx,dy=np.abs(direction[:2])
            scale=min(obj.width/(2*dx) if dx>1e-8 else np.inf,obj.height/(2*dy) if dy>1e-8 else np.inf)
            return obj.get_center()+direction*scale
        super().__init__(boundary(a,delta),boundary(b,-delta),buff=.04,
            color=color,stroke_width=width,max_tip_length_to_length_ratio=.18)

class AttributionGraphView(VGroup):
    complete_circuit=False
    original_model_causality_established=False
    input_specific=True
    has_capital_branch=True
    has_shortcut=True
    def __init__(self,portrait=False,named=True):
        self.portrait=portrait
        coords=[(-2,3.7),(2,3.7),(-2,2),(2,2),(0,.6),(0,-.7)] if portrait else [(-6,1.55),(-6,-.65),(-3.85,1.55),(-3.85,-.65),(-1.55,.8),(-1.55,-1.45)]
        names=['Dallas\n입력','capital\n입력','Texas\n특징군','say capital','say Austin','Austin\n출력 logit'] if named else ['Dallas\n입력','capital\n입력','F_A','F_B','F_C','Austin\n출력 logit']
        self.nodes=VGroup(*[feature_node(s,*xy,w=2.15 if portrait else 1.85,color=MUTED if i<2 else INK if i==5 else FEATURE) for i,(s,xy) in enumerate(zip(names,coords))])
        self.topology=[(0,2),(1,3),(2,4),(3,4),(4,5),(0,4)]
        self.edges=VGroup(*[ContributionEdge(self.nodes[a],self.nodes[b],width=1.3 if j==5 else 2.5) for j,(a,b) in enumerate(self.topology)])
        self.edges[5].become(CurvedArrow(self.nodes[0].get_left() if portrait else self.nodes[0].get_top(),
            self.nodes[4].get_left() if portrait else self.nodes[4].get_top(),angle=PI/2 if portrait else -PI/2,
            color=ATTR,stroke_width=1.3,tip_length=.12))
        ex,ey=(-2.85,.1) if portrait else (-6,-2.15)
        self.error=feature_node('오차 항',ex,ey,w=1.65,color=ERROR)
        self.error_edge=ContributionEdge(self.error,self.nodes[5],ERROR,1)
        self.node_style=self.nodes.copy();self.edge_style=self.edges.copy()
        self.error_style=self.error.copy();self.error_edge_style=self.error_edge.copy()
        super().__init__(self.edges,self.error_edge,self.nodes,self.error)
    def trace(self,scene):
        for j in [4,2,0]:
            scene.play(Indicate(self.edges[j],color=ACCENT,scale_factor=1.05),run_time=.45)
        scene.play(Indicate(self.edges[3],color=ACCENT),Indicate(self.edges[5],color=ACCENT),run_time=.5)
    def reveal(self,scene):
        scene.play(Transform(self.nodes,self.node_style.copy()),Transform(self.error,self.error_style.copy()),run_time=.9)
        scene.play(Transform(self.edges,self.edge_style.copy()),Transform(self.error_edge,self.error_edge_style.copy()),run_time=.9)

class TransformerComparison(VGroup):
    replaces_mlp=True
    exact_copy=False
    def __init__(self,portrait=False,outputs=False):
        cx,cy=(0,1.4) if portrait else (-3.7,-.1)
        self.original=VGroup();self.replacement=VGroup()
        for group,x,title,col,labels in [(self.original,cx-1.8,'Original Model',MUTED,['Attention','MLP','Residual']),
            (self.replacement,cx+1.8,'Replacement',ATTR,['Attention*','CLT Features','Residual'])]:
            group.add(label(title,x,cy+2.1,23,col,3.2))
            for j,s in enumerate(labels):group.add(card(s,x,cy+.9-j*.9,2.85,.65,FEATURE if 'CLT' in s else col,22))
            for a,b in zip(group.submobjects[1:],group.submobjects[2:]):group.add(ContributionEdge(a,b,col,1.5))
            if group is self.replacement:group.add(label('근사 오차 항 포함',x,cy-1.5,16,ERROR,2.85))
            if outputs:group.add(label('→ Austin',x,cy-1.9,24,INK,3))
        super().__init__(self.original,self.replacement,label('≈',cx,cy+.05,35,ACCENT,1))

class CrossLayerTranscoderView(VGroup):
    write_pairs=[(i,j) for i in range(4) for j in range(i,4)]
    def __init__(self,portrait=False):
        cx=0 if portrait else -3.7;ys=[3.6,2.5,1.4,.3] if portrait else [1.8,.7,-.4,-1.5]
        self.inputs=VGroup();self.features=VGroup();self.outputs=VGroup();self.edges=VGroup()
        for i,y in enumerate(ys):
            self.inputs.add(card(f'r{i+1}',cx-2.45,y,1.2,.55,MUTED,23))
            self.features.add(card(f'F{i+1}',cx-.45,y,1.2,.55,FEATURE,23))
            self.outputs.add(card(f'MLP{i+1} 출력',cx+2.05,y,1.9,.55,ATTR,20))
            self.edges.add(ContributionEdge(self.inputs[-1],self.features[-1],FEATURE,1.5))
        self.writes=VGroup(*[ContributionEdge(self.features[i],self.outputs[j],ATTR,1.2) for i,j in self.write_pairs])
        super().__init__(self.edges,self.writes,self.inputs,self.features,self.outputs)

class DenseNeuralView(VGroup):
    def __init__(self,portrait=False):
        cx,cy=(0,1.5) if portrait else (-3.7,.1)
        columns=VGroup(*[VGroup(*[Dot(p(cx+(i-1.5)*1.4,cy+(j-3)*.45),radius=.05,color=MUTED) for j in range(7)]) for i in range(4)])
        edges=VGroup(*[Line(a.get_center(),b.get_center(),color=ZERO,stroke_width=.8) for left,right in zip(columns,columns[1:]) for a in left for b in right])
        super().__init__(edges,columns,label('Attention · MLP · Residual Stream',cx,cy+2,23,MUTED,6.6))

class InterventionPanel(VGroup):
    prompt_unchanged=True
    target_model='original'
    before_output='Austin'
    after_output='Sacramento'
    def __init__(self,portrait=False):
        cx,cy=(0,1.5) if portrait else (-3.7,.05)
        self.input=card('Dallas 질문 · 입력 고정',cx,cy+2,6.6,.7,MUTED,24)
        self.model=card('Original Transformer\n원래 모델의 내부 활성화',cx,cy+.7,6.6,1,INK,25)
        self.feature=card('Texas 특징군',cx-1.7,cy-.5,2.9,.75,FEATURE,23)
        self.output=card('Austin',cx+1.7,cy-.5,2.9,.75,INK,25)
        self.connection=ContributionEdge(self.feature,self.output,ATTR)
        self.caption=label('개입 전 · 보고된 사례의 단순화',cx,cy-1.8,20,MUTED,6.8)
        super().__init__(self.input,self.model,self.connection,self.feature,self.output,self.caption)
    def swap(self,scene):
        x,y=self.feature.get_center()[:2];xx,yy=self.output.get_center()[:2]
        scene.play(Transform(self.feature,card('Texas 억제\nCalifornia 활성화',x,y,2.9,1,INTERVENTION,21)),run_time=.7)
        scene.play(Transform(self.output,card('Sacramento',xx,yy,2.9,.75,INTERVENTION,24)),
            Transform(self.caption,label('같은 Dallas 입력 · 내부 특징만 교체',self.caption.get_x(),self.caption.get_y(),20,INTERVENTION,6.8)),run_time=.7)

class CircuitTracingVideo(sae.SparseAutoencodersVideo):
    SECTION=None
    def construct(self):
        self.portrait=PORTRAIT;P=PORTRAIT;data=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
        selected=data['segments'] if self.SECTION is None else [data['segments'][self.SECTION]]
        self.offset=selected[0]['start'];self.view=VGroup();self.info=VGroup();self.aux=VGroup();self.heading=VGroup();self.caption=VGroup()
        self.fixed=VGroup(label('신경망 내부의 계산  06',x=0 if P else -5.2,y=7.4 if P else 4.08,size=20 if P else 18,color=MUTED,width=7.5 if P else 5),
            label('신경망이 답을 만드는\n계산 경로를 추적하는 방법' if P else '신경망이 답을 만드는 계산 경로를 추적하는 방법',
                x=0 if P else 2.4,y=6.5 if P else 4.08,size=29 if P else 21,width=7.5 if P else 9.8),
            Line(p(-3.9 if P else -7.4,5.75 if P else 3.65),p(3.9 if P else 7.4,5.75 if P else 3.65),color=ZERO),
            RoundedRectangle(width=7.9 if P else 15,height=1.85 if P else 1.04,corner_radius=.1,stroke_width=0,
                fill_color='#14212D',fill_opacity=.95).move_to(p(0,-6.2 if P else -3.65)),
            label('연구 사례의 단순화 도식 · Circuit Tracing, 2025',y=-7.45 if P else -4.3,size=15,color=MUTED,width=7.5 if P else 14))
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
    def set_view(self,obj):
        self.clear_aux();self.remove(*self.view.get_family());self.view=obj;self.add(obj)
    def setup_section(self,k):
        if k==0:
            cx,cy=(0,2.2) if self.portrait else (-3.7,.1)
            nodes=VGroup(*[feature_node(f'F{j+1}',cx+(j%3-1)*2.25,cy+(1 if j<3 else -1),w=1.6) for j in range(6)])
            self.set_view(nodes)
        elif k==1:self.set_view(TransformerComparison(self.portrait))
        elif k in (2,3):
            self.set_view(AttributionGraphView(self.portrait,named=k==3))
            if k==2:
                for n in self.view.nodes[2:5]:n.set_opacity(0)
                self.view.edges.set_opacity(0);self.view.error.set_opacity(0);self.view.error_edge.set_opacity(0)
        elif k==4:self.set_view(TransformerComparison(self.portrait,outputs=True))
        else:self.set_view(AttributionGraphView(self.portrait))
    def event(self,i):
        P=self.portrait;cx,cy=(0,1.5) if P else (-3.7,.05)
        if i==0:self.panel('Feature Candidates',['발견한 특징 노드들','아직 계산 관계는 모른다'])
        elif i==1:
            edges=VGroup(*[DashedLine(self.view[a].get_center(),self.view[b].get_center(),color=MUTED,dash_length=.15) for a,b in [(0,4),(1,3),(2,5)]])
            self.extra(edges);self.panel('Features ≠ Circuit',['어떤 연결이 실제 계산일까?','임의의 선은 아직 가설'])
        elif i==2:
            self.set_view(VGroup(card('댈러스가 속한 주의\n주도는 어디인가?',cx,cy+1,6.7,1.4,INK,30),
                card('Original Transformer\n내부 계산 ?',cx,cy-1.1,6.7,1.2,MUTED,27)))
            self.panel('연구 사례의 질문',['What is the capital of','the state containing Dallas?','Texas를 질문에 미리 주지 않는다'],[INK,INK,MUTED])
        elif i==3:
            self.panel('모델의 답: Austin',['정답은 보인다','중간 계산은 아직 보이지 않는다'],[INK,MUTED]);self.pulse(self.view[1])
        elif i==4:
            coords=[(cx,cy+1.5),(cx,cy),(cx,cy-1.5)] if P else [(cx-2.2,cy),(cx,cy),(cx+2.2,cy)]
            nodes=VGroup(*[feature_node(s,*xy,w=1.9) for s,xy in zip(['Dallas','Texas','Austin'],coords)])
            edges=VGroup(*[ContributionEdge(a,b,ACCENT) for a,b in zip(nodes,nodes[1:])])
            self.set_view(VGroup(edges,nodes));self.panel('가능한 두 단계 관계',['Dallas → Texas','Texas의 주도 → Austin','아직 실제 내부 계산이라는 결론은 아님'],[INK,INK,MUTED])
        elif i==5:self.panel('모델 안에서도 Texas를 거쳤을까?',['답변만으로는 알 수 없다','내부의 중간 계산을 조사한다']);self.pulse(self.view[1][1])
        elif i==6:self.panel('Circuit Tracing · 2025',['원래 모델 → 대체 모델 → 그래프','가설은 원래 모델에서 검증']);self.note('Circuit Tracing: Revealing Computational Graphs in Language Models')
        elif i==7:self.set_view(DenseNeuralView(P));self.panel('복잡하게 얽힌 뉴런과 연산',['Attention · MLP · Residual','어떤 기여가 출력을 만들었을까?'])
        elif i==8:self.panel('특징 식별 ✓  ·  특징 간 기여 ?',['의미를 알아보는 것','다음 계산에 대한 기여를 아는 것']);self.pulse(self.view)
        elif i==9:self.set_view(TransformerComparison(P));self.panel('일부 계산을 해석하기 쉽게 근사',['MLP의 입력·출력 관계를 학습','전체 모델을 그대로 복제하는 것은 아님'],[INK,MUTED])
        elif i==10:self.panel('Cross-Layer Transcoder · CLT',['층을 가로지르는 희소 특징','해석을 위한 분석 구조'],[FEATURE,INK]);self.pulse(self.view.replacement)
        elif i==11:
            self.set_view(VGroup(card('SAE\nh → z → ĥ',cx,cy+1.2,6.5,1.2,FEATURE,29),
                card('Transcoder\nx → z → f̂(x)',cx,cy-1,6.5,1.2,ATTR,29)))
            self.panel('희소 특징을 쓰지만 목표가 다르다',['SAE: 활성화 자체를 복원','Transcoder: 연산 출력을 근사'],[FEATURE,ATTR]);self.pulse(self.view[0]);self.to(57);self.pulse(self.view[1])
        elif i==12:
            self.set_view(CrossLayerTranscoderView(P));self.panel('한 층에서 읽고, 여러 층에 쓴다',['Fℓ: 해당 층 residual에서 읽기','MLPℓ, MLPℓ₊₁, … 출력에 기여','같은 층과 이후 층의 출력만 복원'],[FEATURE,ATTR,MUTED]);self.pulse(self.view.writes)
        elif i==13:
            self.set_view(TransformerComparison(P));self.panel('MLP 계산을 CLT로 대체',['Original ≈ Replacement','해석을 위한 근사 모델'],[INK,ATTR])
            self.note('Attention 패턴의 입력별 고정·선형화 및 근사 오차 항 등 추가 처리 포함')
        elif i==14:
            self.panel('특정 입력 · 목표 출력 지정',['Dallas 질문 → Austin logit','모든 입력의 공통 회로가 아니다'],[ATTR,MUTED]);self.pulse(self.view.nodes[-1])
        elif i==15:self.panel('노드와 방향성 기여 연결',['입력·특징·오차 항·출력','대체 모델 안에서 계산한 관계']);self.view.reveal(self)
        elif i==16:self.panel('Attribution Graph',['특정 출력에 대한 기여도 그래프','원 모델의 완전한 배선도는 아니다'],[ATTR,MUTED])
        elif i==17:
            a=feature_node('F1',cx-1.7,cy+1,w=1.8);b=feature_node('F2',cx+1.7,cy+1,w=1.8)
            c=feature_node('F1',cx-1.7,cy-1,w=1.8);d=feature_node('F2',cx+1.7,cy-1,w=1.8)
            self.set_view(VGroup(a,b,c,d,ContributionEdge(c,d,ATTR)))
            self.panel('공활성화 ≠ 계산상 기여',['위: 함께 활성화 · 방향성 없음','아래: 분석 모델의 방향성 기여'],[INK,ATTR])
        elif i==18:
            self.set_view(AttributionGraphView(P,named=False));self.view.edges[3].set_color(ERROR)
            self.panel('기여에는 크기와 부호가 있다',['보라: 양의 기여 예시','붉은 간선: 음의 기여 예시','두께·부호는 설명용, 실측값 아님'],[ATTR,ERROR,MUTED]);self.pulse(self.view.edges[2])
        elif i==19:self.panel('출력에서 후보 경로를 거슬러 추적',['Austin ← 중간 특징 ← 입력','이 단계는 대체 모델의 기여 분석']);self.view.trace(self)
        elif i==20:self.panel('Texas 관련 중간 특징군',['여러 관련 특징을 묶은 supernode','capital 가지와 지름길도 존재'],[FEATURE,MUTED]);self.pulse(self.view.nodes[2])
        elif i==21:self.panel('계산 경로에 관한 가설',['Texas + say capital → say Austin','Dallas → say Austin 지름길','원래 모델에서도 작동하는지 검증 필요'],[ACCENT,ATTR,MUTED]);self.view.trace(self)
        elif i==22:self.panel('그래프를 얻었지만, 분석 대상은?',['원래 모델과 대체 모델을 구별'],[ACCENT])
        elif i==23:self.panel('우리가 분석한 것은 대체 모델',['Original: 실제 검증 대상','Replacement: 해석을 위한 근사','둘의 내부 계산은 다를 수 있다'],[MUTED,ATTR,ERROR]);self.pulse(self.view.replacement)
        elif i==24:self.panel('Same Output ≠ Same Mechanism',['둘 다 Austin을 출력해도','동일한 내부 계산은 보장되지 않는다'],[INK,ERROR]);self.pulse(self.view.original,self.view.replacement)
        elif i==25:self.set_view(InterventionPanel(P));self.panel('가설을 원래 모델로 가져간다',['분석 그래프 → 실제 모델 개입','입력은 그대로 유지'],[ACCENT,INK]);self.pulse(self.view.model)
        elif i==26:
            self.panel('원래 모델의 관련 특징에 개입',['Texas 특징군 억제','California 특징군 활성화','Dallas 입력을 바꾸지 않는다'],[INTERVENTION,INTERVENTION,MUTED])
            self.view.swap(self);self.note('California 특징 식별용 별도 입력과, Dallas를 고정한 시험 입력을 구별')
        elif i==27:self.panel('Intervention Evidence',['개입 전: Texas → Austin','개입 후: California → Sacramento','경로 가설을 뒷받침하는 근거'],[FEATURE,INTERVENTION,INK])
        elif i==28:self.set_view(AttributionGraphView(P));self.panel('Partial Explanation',['모든 계산을 설명한 것은 아니다','모든 연결의 인과 역할이 확정된 것도 아님'],[ERROR,MUTED]);self.note('단순화 도식 · 검증된 주요 효과와 전체 회로의 완전성은 구별')
        elif i==29:self.panel('출력 관찰을 넘어 계산 관계로',['확인할 수 있는 분석의 수준이 달라진다'])
        elif i==30:self.panel('Output → Features → Circuits',['답변을 본다 → 특징을 찾는다','특징 사이의 계산 관계를 추적한다']);self.view.trace(self)
        elif i==31:self.panel('정보가 있다는 것과 사용한다는 것',['Information Present','Used in Computation?'],[FEATURE,ACCENT]);self.pulse(self.view.nodes[2])
        elif i==32:
            self.set_view(VGroup(card('Probing\n정보를 읽을 수 있는가?',cx,cy+1.15,6.6,1.3,FEATURE,28),
                card('Intervention\n바꾸면 계산이 달라지는가?',cx,cy-1,6.6,1.3,INTERVENTION,28)))
            self.panel('읽힌다는 사실 ≠ 실제 사용의 증거',['Readable','Causally Used?'],[FEATURE,INTERVENTION]);self.pulse(self.view[0]);self.to(162);self.pulse(self.view[1])

class CircuitTracing(CircuitTracingVideo):pass
class CircuitTracingShorts(CircuitTracingVideo):pass
class CircuitQuestionIntro(CircuitTracingVideo):SECTION=0
class TranscoderArchitecture(CircuitTracingVideo):SECTION=1
class AttributionGraphConstruction(CircuitTracingVideo):SECTION=2
class DallasTexasAustinCircuit(CircuitTracingVideo):SECTION=3
class InterventionValidation(CircuitTracingVideo):SECTION=4
class ProbingInterventionBridge(CircuitTracingVideo):SECTION=5
