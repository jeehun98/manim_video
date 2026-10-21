"""Sparse dictionary learning: six replaceable sections, two native layouts."""
import json
import os
import sys
from pathlib import Path
import numpy as np
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.nncalc04_feature_superposition import scene as previous
from visual_library.manim import BG,INK,MUTED,ACCENT,GOOD,PRUNE,ZERO
config.pixel_width=int(os.environ.get('VIDEO_WIDTH','1920'))
config.pixel_height=int(os.environ.get('VIDEO_HEIGHT','1080'))
PORTRAIT=config.pixel_height>config.pixel_width
config.frame_width=9 if PORTRAIT else 16;config.frame_height=16 if PORTRAIT else 9
config.frame_rate=30;config.background_color=BG;config.disable_caching=True
HERE=Path(__file__).resolve().parent
COLORS=previous.COLORS;label=previous.label;card=previous.card;p=previous.p
arrow=previous.shared.arrow
DICT_ANGLES=np.deg2rad([20,100,170,280,330])
DICTIONARY=previous.vectors(DICT_ANGLES)
EXAMPLES=np.array([[.85,0,0,.62,0],[0,.7,0,0,.65],[.9,0,.4,0,0]])
ENCODER=GOOD;DECODER=COLORS[1];ERROR='#F7A65E'

class SparseAutoencoderView(VGroup):
    original_model_frozen=True
    latent_dimensions=5
    activation_dimensions=2
    def __init__(self,portrait=False):
        cx,cy=(0,1.4) if portrait else (-3.65,.1)
        xs=[cx-2.25,cx,cx+2.25]
        self.columns=VGroup()
        for col,(x,n) in enumerate(zip(xs,[2,5,2])):
            self.columns.add(VGroup(*[Circle(radius=.14 if n==5 else .12,color=COLORS[j] if n==5 else INK,
                stroke_width=2,fill_color=COLORS[j] if n==5 else INK,fill_opacity=.14).move_to(p(x,cy+(n-1)*.31-j*.62)) for j in range(n)]))
        self.edges=VGroup()
        for a,b,col in [(self.columns[0],self.columns[1],ENCODER),(self.columns[1],self.columns[2],DECODER)]:
            self.edges.add(VGroup(*[Line(n.get_center(),m.get_center(),color=col,stroke_opacity=.24,stroke_width=1.2) for n in a for m in b]))
        self.values=VGroup(*[label('?',cx+.65,cy+1.24-j*.62,20,MUTED,1) for j in range(5)])
        self.readout=label('h ∈ ℝ²   →   z ∈ ℝ⁵   →   ĥ ∈ ℝ²',cx,cy-2.12,23,INK,7 if portrait else 6.4)
        super().__init__(self.edges,self.columns,self.values,self.readout,
            label('Encoder',cx-1.35,cy+1.8,23,ENCODER,2.3),label('Decoder',cx+1.35,cy+1.8,23,DECODER,2.3),
            card('Frozen Transformer · 원래 모델 고정',cx,cy+2.3,6.5,.55,MUTED,20),
            arrow(p(cx-2.25,cy+2.0),p(cx-2.25,cy+.62),MUTED),
            label('활성화\n복사',cx-2.95,cy+1.3,16,MUTED,1.05))
    def activate(self,scene,z):
        scene.play(*[node.animate.set_fill(COLORS[j],opacity=.95 if v>.01 else .07).set_stroke(COLORS[j] if v>.01 else MUTED)
            for j,(node,v) in enumerate(zip(self.columns[1],z))],
            *[Transform(old,label(f'{v:.2f}',old.get_x(),old.get_y(),20,COLORS[j] if v>.01 else MUTED,1)) for j,(old,v) in enumerate(zip(self.values,z))],run_time=.65)

class DictionaryView(previous.FeaturePlane):
    ground_truth_recovery_claimed=False
    def __init__(self,portrait=False):
        super().__init__(portrait);self.angles=DICT_ANGLES.copy()
        self.vectors.add(*[self.glyph(i,a) for i,a in enumerate(DICT_ANGLES)])
        for j,g in enumerate(self.vectors):g[1].become(label(f'd{j+1}',g[1].get_x(),g[1].get_y(),23,COLORS[j],.6))
        self.result=VGroup();self.add(self.result)
    def compose(self,scene,z):
        self.select(scene,np.where(z>.01)[0])
        endpoint=self.point(DICTIONARY@z)
        new=VGroup(Arrow(self.origin,endpoint,buff=0,color=INK,stroke_width=5),Dot(endpoint,color=INK,radius=.07))
        if len(self.result):scene.play(Transform(self.result,new),run_time=.6)
        else:self.result.add(*new);scene.play(GrowArrow(self.result[0]),FadeIn(self.result[1]),run_time=.6)

class CandidateGraph(VGroup):
    causality_established=False
    def __init__(self,portrait=False):
        if portrait:coords=[(-2.7,3.4),(-1.6,1.7),(1.6,1.7),(0,.1),(0,-1.4)]
        else:coords=[(-6.2,.3),(-4.3,1.3),(-4.3,-.8),(-2.4,.3),(-.5,.3)]
        self.nodes=VGroup(*[card(s,*xy,1.7,.7,col,23) for s,xy,col in zip(['입력','F1','F2','F3','출력'],coords,[MUTED,*COLORS[:3],INK])])
        self.edges=VGroup()
        for a,b in [(0,1),(0,2),(1,3),(2,3),(3,4)]:
            delta=self.nodes[b].get_center()-self.nodes[a].get_center()
            self.edges.add(DashedLine(self.nodes[a].get_boundary_point(delta),self.nodes[b].get_boundary_point(-delta),
                color=MUTED,dash_length=.12,stroke_width=2,buff=.07))
        super().__init__(self.edges,self.nodes)
    def trace(self,scene):
        for j in [0,2,4]:scene.play(self.edges[j].animate.set_stroke(ACCENT,width=3),run_time=.35)

class SparseAutoencodersVideo(previous.SuperpositionVideo):
    SECTION=None
    def to(self,t):super().to(t-self.offset)
    def construct(self):
        self.portrait=PORTRAIT;P=PORTRAIT;data=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
        selected=data['segments'] if self.SECTION is None else [data['segments'][self.SECTION]]
        self.offset=selected[0]['start'];self.info=VGroup();self.aux=VGroup()
        self.heading=VGroup();self.caption=VGroup()
        self.fixed=VGroup(label('신경망 내부의 계산  05',x=0 if P else -5.2,y=7.4 if P else 4.08,size=20 if P else 18,color=MUTED,width=7.5 if P else 5),
            label('여러 뉴런에 겹쳐진 특징을\n다시 분리하는 방법' if P else '여러 뉴런에 겹쳐진 특징을 다시 분리하는 방법',
                x=0 if P else 2.4,y=6.5 if P else 4.08,size=29 if P else 21,width=7.5 if P else 9.8),
            Line(p(-3.9 if P else -7.4,5.75 if P else 3.65),p(3.9 if P else 7.4,5.75 if P else 3.65),color=ZERO),
            RoundedRectangle(width=7.9 if P else 15,height=1.85 if P else 1.04,corner_radius=.1,stroke_width=0,
                fill_color='#14212D',fill_opacity=.95).move_to(p(0,-6.2 if P else -3.65)),
            label('도식·활성값은 예시 · Bricken et al., 2023',y=-7.45 if P else -4.3,size=15,color=MUTED,width=7.5 if P else 14))
        self.add(self.fixed)
        for seg in selected:
            self.to(seg['start'])
            for obj in list(self.mobjects):
                if obj is not self.fixed:self.remove(obj)
            self.info=VGroup();self.aux=VGroup()
            self.heading=label(f'{seg["index"]:02}  {seg["title"]}',y=5.25 if P else 3.12,size=23 if P else 28,color=ACCENT,width=7.7 if P else 14.5)
            self.add(self.heading);self.setup_section(seg['index']-1)
            for q in seg['cues']:
                self.to(q['start']);self.remove(self.caption);self.caption=self.caption_obj(q['text']);self.add(self.caption)
                self.event(q['index']);self.to(q['end'])
        self.to(selected[-1]['end'])
    def setup_section(self,k):
        P=self.portrait
        if k==0:self.plane=previous.FeaturePlane(P);self.add(self.plane)
        elif k in (1,2):self.net=SparseAutoencoderView(P);self.add(self.net)
        elif k==3:
            self.plane=DictionaryView(P);self.add(self.plane)
        elif k==4:pass
        else:self.plane=DictionaryView(P);self.add(self.plane)
    def replace_left(self,obj):
        for name in ['net','plane','left']:
            old=getattr(self,name,None)
            if old is not None:self.remove(*old.get_family());setattr(self,name,None)
        self.left=obj;self.add(obj)
    def note(self,s):self.extra(label(s,y=-4.85 if self.portrait else -2.72,size=16,color=MUTED,width=7.4 if self.portrait else 14))
    def latent_panel(self,title,z):
        self.panel(title)
        P=self.portrait;x,y=(0,-3.1) if P else (3.8,.2)
        nodes=VGroup(*[card(f'z{j+1}\n{v:.2f}',x+(j-2)*1.22,y,1.05,1.15,COLORS[j] if v>.01 else MUTED,21) for j,v in enumerate(z)])
        self.extra(nodes)
    def event(self,i):
        P=self.portrait
        if i==0:self.panel('관찰한 활성화 뒤의 특징은?', ['여러 특징의 기여 → 하나의 좌표','특징 조합은 직접 보이지 않는다'])
        elif i==1:self.panel('두 뉴런 → 2차원 활성화',['Neuron 1 · Neuron 2','h = (h₁, h₂)']);self.pulse(self.plane.axes)
        elif i==2:
            self.plane.set_features(self,previous.REGULAR)
            self.panel('다섯 방향이 겹쳐 있을 수 있다',['가상의 생성 특징 · 설명용','SAE가 이 방향을 찾았다는 뜻은 아님'],[INK,MUTED])
        elif i==3:
            self.plane.select(self,[0,3]);v=previous.vectors(previous.REGULAR)@EXAMPLES[0]
            self.extra(Arrow(self.plane.origin,self.plane.point(v),buff=0,color=INK,stroke_width=5))
            self.panel('보이는 것은 두 좌표뿐',['h₁ · h₂','숨은 조합은 유일하지 않을 수 있다'])
        elif i==4:self.latent_panel('혼합된 h → 잠재값 z ?',np.zeros(5))
        elif i==5:self.panel('원래 모델과 분석 모델은 별개',['Original Transformer → h','h를 복사해 Analysis Model로','가중치를 옮기는 과정이 아니다'],[INK,GOOD,MUTED])
        elif i==6:self.panel('Sparse Autoencoder · SAE',['Encoder → Latents → Decoder','설명 예시 2 → 5 → 2']);self.pulse(self.net.columns[1])
        elif i==7:
            self.panel('원래 Transformer는 고정',['Input A → h⁽¹⁾','Input B → h⁽²⁾','Input C → h⁽³⁾'],[INK,INK,INK])
            self.note('원래 모델 가중치 고정 · 수집한 활성화로 SAE의 가중치만 학습')
            self.pulse(self.net.columns[0])
        elif i==8:self.clear_aux();self.panel('Encoder가 잠재 표현으로',['z = ReLU(W_enc(h − b_dec) + b_enc)','아직 의미가 확정된 특징은 아니다'],[ENCODER,MUTED]);self.pulse(self.net.edges[0])
        elif i==9:self.panel('2개의 활성값 → 5개의 잠재값',['h ∈ ℝ² → z ∈ ℝ⁵','잠재값의 수를 확장한다']);self.net.activate(self,[.5,.3,.4,.2,.6])
        elif i==10:self.panel('Decoder가 원래 공간을 복원',['ĥ = Dz + b_dec','5개 잠재값 → 2차원 복원'],[DECODER,INK]);self.pulse(self.net.edges[1])
        elif i==11:self.panel('복원 성공 ≠ 의미 발견',['Reconstruction ✓','Interpretation ?'],[DECODER,ACCENT]);self.net.activate(self,[.5,.3,.4,.2,.6])
        elif i==12:
            plane=previous.FeaturePlane(P);self.replace_left(plane);self.plane=plane
            a=plane.point([.9,.65]);mid=plane.point([.9,0])
            self.extra(Arrow(plane.origin,mid,buff=0,color=COLORS[0]),Arrow(mid,a,buff=0,color=COLORS[1]),Dot(a,color=INK))
            self.panel('다른 분해 · 같은 복원',['(0.9, 0) + (0, 0.65)','= (0.4, 0.65) + (0.5, 0)'])
            self.to(63.5);self.clear_aux()
            mid=plane.point([.4,.65]);self.extra(Arrow(plane.origin,mid,buff=0,color=COLORS[2]),Arrow(mid,a,buff=0,color=COLORS[3]),Dot(a,color=INK))
        elif i==13:
            self.clear_aux();net=SparseAutoencoderView(P);self.replace_left(net);self.net=net
            self.panel('추가 제약 · Sparsity',['각 입력에서 적은 잠재값 사용']);self.net.activate(self,[.5,.3,.4,.2,.6])
        elif i==14:self.panel('노드를 없애는 것이 아니다',['입력마다 활성화 패턴이 달라진다','적은 수의 잠재값을 사용']);self.net.activate(self,EXAMPLES[0])
        elif i==15:self.panel('첫 번째 · 네 번째 잠재값',['z ≈ (0.85, 0, 0, 0.62, 0)','값은 설명용 예시'],[GOOD,MUTED]);self.net.activate(self,EXAMPLES[0])
        elif i==16:
            self.clear_aux();plane=DictionaryView(P);self.replace_left(plane);self.plane=plane
            self.panel('학습: 공통 사전 방향을 찾는다',['Encoder와 Decoder를 함께 갱신','이후 고정 사전으로 입력별 복원'])
            self.pulse(plane.vectors);self.to(81)
            for j,z in enumerate(EXAMPLES):
                self.clear_aux();self.latent_panel(f'입력 {"ABC"[j]} · 같은 디코더 사전',z)
                plane.compose(self,z)
                self.note('학습 후 사용 단계 · 사전 방향은 고정 · 입력별 계수만 변화')
                self.to([83,85,87][j])
        elif i==17:
            self.clear_aux();self.panel('Dictionary = 학습된 방향들',['ĥ = Σᵢ zᵢ dᵢ + b_dec','샘플 목록이 아닌 공통 복원 방향'],[DECODER,INK]);self.plane.compose(self,EXAMPLES[0])
        elif i==18:self.panel('두 목표가 경쟁한다',['Reconstruction · 복원','Sparsity · 희소성'],[DECODER,GOOD])
        elif i==19:
            f=self.plane;v=DICTIONARY@EXAMPLES[0];point=f.point(v);far=f.point(v+np.array([.5,.45]))
            self.error_dot=Dot(far,color=ERROR);self.error_line=Line(point,far,color=ERROR,stroke_width=4)
            self.extra(Dot(point,color=INK),self.error_dot,self.error_line)
            self.panel('복원 오차를 줄인다',['L_recon = ‖h − ĥ‖²','원래 h와 복원 ĥ를 가깝게'],[DECODER,INK])
            self.play(self.error_dot.animate.move_to(point+RIGHT*.08),Transform(self.error_line,Line(point,point+RIGHT*.08,color=ERROR,stroke_width=4)),run_time=1)
        elif i==20:
            self.clear_aux();self.latent_panel('희소성 페널티를 더한다',[.85,0,0,.62,0])
            self.note('L_sparse = λ‖z‖₁ · 활성화 크기의 합을 억제 · 개수를 직접 세는 연산은 아님')
        elif i==21:
            self.clear_aux();self.panel('어느 한쪽만 강조하면?',['복원 중심: 많은 잠재값 사용 가능','과도한 희소성: 필요한 정보 손실','정도는 데이터와 제약에 따라 다름'],[DECODER,PRUNE,MUTED])
            self.plane.compose(self,EXAMPLES[0]);self.to(104.5);self.plane.compose(self,np.array([.3,0,0,0,0]))
        elif i==22:
            self.clear_aux();self.panel('복원 + 희소성의 균형',['L = ‖h − ĥ‖² + λ‖z‖₁','디코더 열 노름 제약을 함께 사용'],[INK,MUTED]);self.plane.compose(self,EXAMPLES[0])
        elif i==23:
            x,y=(0,1.7) if P else (-3.7,.3)
            self.left=VGroup(card('Toy Example\n2 → 5 → 2',x,y+1.3,6.2,1.1,GOOD,28),
                card('Research Model\n512뉴런 → 4,096 잠재 특징',x,y-1.1,6.7,1.2,DECODER,25))
            self.add(self.left);self.panel('Towards Monosemanticity · 2023',['작은 1층 Transformer의 MLP','사전 크기 4,096은 연구의 한 사례','모든 잠재값의 의미가 확정된 것은 아님'],[INK,MUTED,MUTED])
        elif i==24:
            self.remove(*self.left.get_family());x,y=(0,1.5) if P else (-3.7,.2)
            arabic=ImageMobject(str(HERE/'assets/arabic.png')).scale_to_fit_height(1.15).move_to(p(x,y+.82))
            arabic_card=VGroup(RoundedRectangle(width=6.2,height=1.3,corner_radius=.12,stroke_color=COLORS[0],
                fill_color=COLORS[0],fill_opacity=.06,stroke_width=1.5).move_to(p(x,y+1)),
                label('Arabic Script',x,y+1.35,29,COLORS[0],5.9))
            self.left=Group(arabic_card,card('Base64 Pattern\nSGVsbG8=',x,y-1,6.2,1.2,COLORS[1],32),arabic)
            self.add(self.left);self.panel('문자 체계 · 문자열 형식 후보',['관련 입력에서 선택적으로 반응','문자열은 설명용 예시','모든 관련 입력에 반응한다는 뜻은 아님'],[INK,MUTED,MUTED])
            self.pulse(self.left[0]);self.to(122);self.pulse(self.left[1])
        elif i==25:
            self.remove(*self.left.get_family());x,y=(0,1.5) if P else (-3.7,.2)
            self.left=VGroup(card('SAE에서 찾은 방향',x,y+1.5,6.3,.8,DECODER,25),
                card('원래 Transformer의\n활성화에 개입',x,y,6.3,1.1,ACCENT,27),
                card('이후 원래 모델 계산 → 출력 변화',x,y-1.6,6.7,.8,GOOD,23))
            self.add(self.left);self.panel('Feature Intervention',['조절 대상: 원래 모델 활성화','관찰 결과: 관련 출력 변화','SAE가 직접 텍스트를 생성하지 않는다'],[ACCENT,INK,MUTED]);self.pulse(self.left[1])
        elif i==26:self.panel('좋은 복원 ≠ 완전한 의미 발견',['Reconstruction ≠ Interpretation','복원 기준과 해석 근거를 구별'])
        elif i==27:
            self.panel('서로 다른 사전도 비슷하게 복원',['SAE A: 다른 방향과 계수','SAE B: 다른 방향과 계수','분해의 유일성은 보장되지 않는다'],[COLORS[0],COLORS[1],MUTED])
            self.plane.compose(self,EXAMPLES[0]);self.pulse(self.plane.vectors)
        elif i==28:
            self.replace_left(VGroup());x,y=(0,1.5) if P else (-3.8,.2)
            self.left=VGroup(card('Feature Splitting\nF → F₁, F₂, F₃',x,y+1.2,6.4,1.1,DECODER,27),
                card('Feature Merging\nA, B → AB',x,y-1,6.4,1.1,GOOD,27));self.add(self.left)
            self.panel('분해의 해상도가 달라질 수 있다',['다른 사전 크기 · 학습 조건 비교','한 SAE 안에서 노드가 분열하는 뜻은 아님'],[INK,MUTED])
        elif i==29:
            graph=CandidateGraph(P);self.replace_left(graph);self.graph=graph
            self.panel('반응한다 ≠ 계산에 사용한다',['이 특징을 바꾸면 출력도 달라질까?','점선은 아직 검증하지 않은 후보'],[ACCENT,MUTED])
            if P:self.remove(self.info);self.info=label('반응만으로 인과 역할을 확정할 수 없다',y=-3.4,size=25,color=ACCENT,width=7.4);self.add(self.info)
            self.note('후보 연결의 개념도 · 실제 인과적 경로를 확인한 그래프 아님');self.pulse(graph.nodes[1])
        elif i==30:
            self.panel('우리가 얻은 것은 특징 후보',['Features Found','Computational Roles Unknown'],[GOOD,ACCENT])
            if P:self.remove(self.info);self.info=label('특징 후보를 발견 · 계산 역할은 미확인',y=-3.4,size=25,color=GOOD,width=7.4);self.add(self.info)
        elif i==31:
            self.panel('특징의 역할은 어떻게 확인할까?',['입력 → 특징 사이의 영향 → 출력','경로마다 별도 근거가 필요하다'])
            if P:self.remove(self.info);self.info=label('특징 사이의 영향과 출력 경로를 검증',y=-3.4,size=25,color=ACCENT,width=7.4);self.add(self.info)
        elif i==32:
            self.panel('특징의 발견 → 계산 경로 추적',['강조한 선도 추적 대상인 후보','실제 기여는 개입 등으로 검증'],[ACCENT,MUTED])
            if P:self.remove(self.info);self.info=label('밝은 선은 추적할 후보 경로 · 인과 확정 아님',y=-3.4,size=23,color=ACCENT,width=7.4);self.add(self.info)
            self.graph.trace(self)

class SparseAutoencoders(SparseAutoencodersVideo):pass
class SparseAutoencodersShorts(SparseAutoencodersVideo):pass
class FeatureMixingIntro(SparseAutoencodersVideo):SECTION=0
class SparseAutoencoderArchitecture(SparseAutoencodersVideo):SECTION=1
class SparseDictionaryLearning(SparseAutoencodersVideo):SECTION=2
class ReconstructionSparsityTradeoff(SparseAutoencodersVideo):SECTION=3
class MonosemanticityFindings(SparseAutoencodersVideo):SECTION=4
class InterpretationLimits(SparseAutoencodersVideo):SECTION=5
