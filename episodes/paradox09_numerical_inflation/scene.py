"""Softmax symmetry, numerical residuals and a conditional feedback mechanism."""
import json,sys
from pathlib import Path
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visual_library.manim import FONT,BG,INK,MUTED,WEIGHT,PRUNE,SPARSE,ACCENT,GOOD,configure_vertical
configure_vertical();config.disable_caching=True
ROOT=Path(__file__).resolve().parent
ORANGE='#FFAA66'
def t(s,y=0,x=0,size=27,color=INK,width=7.7):
    o=Text(s,font=FONT,font_size=size,color=color,line_spacing=1.2)
    if o.width>width:o.scale_to_fit_width(width)
    return o.move_to([x,y,0])
def softmax(z,dtype=np.float64):
    a=np.asarray(z,dtype=dtype);e=np.exp(a-a.max());return e/e.sum(dtype=dtype)
def label(s,y,c=WEIGHT):return VGroup(RoundedRectangle(width=7.1,height=.85,corner_radius=.1,color=c,fill_color=BG,fill_opacity=1).move_to([0,y,0]),t(s,y,size=26,color=c))
def chart(fn,x,y,w=6.6,h=3.5,color=WEIGHT):
    a=Axes(x_range=[0,10,2],y_range=[0,1.2,.4],x_length=w,y_length=h,tips=False,axis_config={'color':MUTED,'stroke_width':1.2}).move_to([x,y,0])
    return a,a.plot(fn,x_range=[0,10,.025],color=color,stroke_width=3)
def spike(v):return .78*np.exp(-v)+.025+.96*np.exp(-((v-8.2)/.19)**2)
def loss_intro():
    a,c=chart(spike,0,.8)
    p=VGroup(a,t('Training Loss',3.4,color=WEIGHT),t('학습 단계 →',-1.5,color=MUTED),t('잘 학습되던 순간, 갑작스러운 급등',-2.9,size=29,color=ORANGE),t('설명용 곡선 · 실제 실험 데이터가 아님',-4.4,size=21,color=MUTED))
    p.curve=c;return p
def logits(shift=0):
    z=np.array([2.,1.,.5]);prob=softmax(z);p=VGroup(t('클래스 점수',3.95,-2,size=28,color=WEIGHT),t('Softmax 확률',3.95,2,size=28,color=GOOD))
    bars=VGroup();nums=VGroup();targets=VGroup()
    base=-.9
    for i,(zz,pp) in enumerate(zip(z,prob)):
        x=-3.15+i*.95;h=(zz+shift)*.72
        b=Rectangle(width=.58,height=h,color=WEIGHT if i==0 else ORANGE,fill_color=WEIGHT if i==0 else ORANGE,fill_opacity=.7).move_to([x,base+h/2,0]);bars.add(b)
        nums.add(t(f'{zz+shift:g}',base+h+.3,x,size=23))
        hh=(zz+2)*.72
        targets.add(Rectangle(width=.58,height=hh,color=b.get_color(),fill_color=b.get_color(),fill_opacity=.7).move_to([x,base+hh/2,0]))
        xp=1.05+i*.95;hp=pp*3.4
        p.add(Rectangle(width=.58,height=hp,color=GOOD,fill_color=GOOD,fill_opacity=.65).move_to([xp,base+hp/2,0]),t(f'{pp:.1%}',base+hp+.3,xp,size=20,color=GOOD),t(str(i+1),base-.4,xp,size=20,color=MUTED),t(str(i+1),base-.4,x,size=20,color=MUTED))
    p.add(Line([-3.65,base,0],[-.6,base,0],color=MUTED),Line([.65,base,0],[3.65,base,0],color=MUTED),bars,nums,t('Softmax(z + c·1) = Softmax(z)',-2.25,size=29,color=ACCENT),t('세 점수 + 같은 수  →  확률은 그대로',-3.3,size=27))
    p.add(t('막대의 기준선 고정 · 높이만 같은 양만큼 증가',-4.5,size=21,color=MUTED))
    p.bars=bars;p.nums=nums;p.targets=targets;p.base=base;p.z=z
    return p
def balance(broken=False,rounding=False):
    p=VGroup(t('정답 클래스',3.9,-1.9,size=26,color=WEIGHT),t('나머지 클래스',3.9,1.9,size=26,color=ORANGE),t('−2ε',2.9,-1.9,size=36,color=WEIGHT),t('+ε  +ε',2.9,1.9,size=36,color=ORANGE),Line([-3.3,.8,0],[3.3,.8,0],color=MUTED,stroke_opacity=.4))
    neg=Arrow([0,1.5,0],[-2.6,1.5,0],buff=0,color=WEIGHT,stroke_width=6)
    pos=Arrow([0,.2,0],[2.6,.2,0],buff=0,color=ORANGE,stroke_width=6)
    p.add(neg,pos,t('Σᵢ (pᵢ − yᵢ) = 0',-1.35,size=37,color=GOOD),t('공통 이동 방향의 기울기 = 0',-2.7,size=29,color=GOOD),t('ε는 오답 하나의 작은 확률 · 화살표 크기는 확대',-4.5,size=20,color=MUTED))
    if broken:
        neg.set_opacity(0);p[2].become(t('0',2.9,-1.9,size=36,color=PRUNE));p[-3].become(t('Σᵢ gᵢ = 2ε > 0',-1.35,size=37,color=PRUNE));p[-2].become(t('상쇄되지 않은 잔여 성분',-2.7,size=30,color=PRUNE))
    if rounding:p.add(t('0.9999999959 → 1.0',-3.65,size=30,color=PRUNE))
    p.neg=neg;p.pos=pos
    return p
def rounded():
    p=VGroup(t('고확신 상태 · z = (20, 0, 0)',4,size=28,color=ACCENT),t('정확한 확률 ≈ 0.9999999959',2.85,size=31,color=WEIGHT),t('↓  float32 계산',1.65,size=27,color=MUTED),t('정답 확률 = 1.0',.5,size=40,color=PRUNE),t('정답 기울기  1.0 − 1.0 = 0',-1,size=31,color=WEIGHT),t('오답 기울기  ≈ 2.06 × 10⁻⁹  (각각)',-2.35,size=28,color=ORANGE),t('1 근처의 작은 차이는 사라져도',-3.6,size=25),t('작은 양수 자체는 표현될 수 있다',-4.35,size=25,color=ORANGE))
    return p
def geometry(broken=False):
    origin=np.array([-.4,-.1,0]);p=VGroup(t('로짓 공간의 2차원 정사영',4,size=27,color=ACCENT))
    for x in [-2.8,-1.4,0,1.4,2.8]:p.add(DashedLine([x,-2.15,0],[x,2.8,0],color=MUTED,stroke_opacity=.25))
    p.add(Arrow(origin+DOWN*1.6,origin+UP*2.7,buff=0,color=SPARSE),t('공통 방향',3.1,-.2,size=24,color=SPARSE),t('u ∝ (1, 1, 1)',2.5,1.8,size=23,color=SPARSE,width=3.3),Arrow(origin,origin+RIGHT*2.9,buff=0,color=GOOD,stroke_width=5),t('분류 방향',-.65,2,size=24,color=GOOD,width=3))
    if broken:
        p.add(Arrow(origin,origin+RIGHT*2.9+UP*1.1,buff=0,color=ORANGE,stroke_width=5),Arrow(origin+RIGHT*2.9,origin+RIGHT*2.9+UP*1.1,buff=0,color=PRUNE,stroke_width=6),t('생겨난 성분',1.5,2.5,size=23,color=PRUNE,width=3),t('g · u = (Σgᵢ) / √3 ≠ 0',-3,size=30,color=PRUNE))
    else:p.add(t('g · u = 0',-3,size=36,color=GOOD))
    p.add(t('화살표는 기울기 · 경사하강 갱신은 반대 방향',-4.3,size=20,color=MUTED))
    return p
def classifier(backward=False):
    p=VGroup(label('앞선 층의 특징 h',3.4,WEIGHT),label('마지막 분류기 W',1.25,ORANGE),label('클래스 점수 z = Wh',-.9,SPARSE),Arrow([0,2.9,0],[0,1.8,0],color=MUTED),Arrow([0,.7,0],[0,-.35,0],color=MUTED),t('특징 공간 → 클래스 로짓 공간',-3.7,size=27,color=MUTED))
    if backward:p.add(Arrow([3.85,-.9,0],[3.85,3.4,0],color=PRUNE,buff=0),t('역전파: ∇h L = Wᵀg',-2.45,size=32,color=PRUNE))
    else:p.add(t('특징과 가중치의 내적으로 점수를 계산',-2.45,size=28,color=ACCENT))
    p.add(t('이후 평균 벡터는 특징 공간에서 표시',-4.5,size=21,color=MUTED))
    return p
def means(length=.8):
    center=np.array([0,1,0]);p=VGroup(t('특징 공간의 두 평균',4,size=29,color=ACCENT),t('분류기 행 평균 W̄',2.9,-1.85,size=24,color=ORANGE,width=3.7),t('특징 평균 h̄',2.9,1.85,size=24,color=WEIGHT,width=3.7),Line([-3.5,1,0],[3.5,1,0],color=MUTED,stroke_opacity=.4),Dot(center,color=MUTED,radius=.05))
    w=Arrow(center,center+LEFT*length,buff=0,color=ORANGE,stroke_width=7)
    h=Arrow(center,center+RIGHT*length,buff=0,color=WEIGHT,stroke_width=7)
    p.add(w,h,CurvedArrow([-2.4,.3,0],[2.4,.3,0],angle=PI/3,color=ORANGE),CurvedArrow([2.4,1.7,0],[-2.4,1.7,0],angle=PI/3,color=WEIGHT),t('가중치가 다음 특징 업데이트에 영향',-1.9,size=27,color=ORANGE),t('특징이 다음 가중치 업데이트에 영향',-2.95,size=27,color=WEIGHT),t('SC·근사 NC 등 조건 아래의 개념도',-4.3,size=21,color=MUTED))
    p.w=w;p.h=h;p.center=center;return p
def growth():
    p=VGroup(t('고정된 증가',3.95,-1.9,size=26,color=MUTED),t('다음 증가도 커짐',3.95,1.9,size=26,color=PRUNE))
    a,c=chart(lambda v:.07+.065*v,-1.95,1,3.15,3.5,MUTED)
    b,d=chart(lambda v:.04*1.38**v,1.95,1,3.15,3.5,PRUNE)
    p.add(a,b,c,d,t('단순 누적',-1.5,-1.95,size=25,color=MUTED),t('양의 피드백',-1.5,1.95,size=25,color=PRUNE),t('Numerical Feature Inflation',-2.8,size=30,color=ACCENT),t('NFI',-3.65,size=39,color=PRUNE),t('성장 곡선은 설명용 · 보편적 성장률을 뜻하지 않음',-4.5,size=20,color=MUTED))
    return p
def trigger():
    p=VGroup(t('평균 벡터의 크기',4,-1.9,size=25,color=ORANGE),t('손실',4,1.9,size=25,color=PRUNE))
    a,c=chart(lambda v:.035*1.4**v,-1.95,2,3.1,2.2,ORANGE);b,d=chart(spike,1.95,2,3.1,2.2,PRUNE)
    p.add(a,b,c,d,DashedLine(b.c2p(8.2,0),b.c2p(8.2,1.15),color=ACCENT),label('일부 표본의 정답 기울기 재등장',-.2,ACCENT),label('Adam의 큰 파라미터 업데이트',-1.7,ORANGE),label('이후 손실 급등',-3.2,PRUNE),t('NFI 성장 ≠ 즉시 손실 급등 · 설명용 곡선',-4.5,size=21,color=MUTED))
    return p
def caveat():
    return VGroup(t('모든 손실 급등',3.5,size=34,color=PRUNE),t('≠',2,size=48,color=ACCENT),t('이 반올림 메커니즘',.5,size=34,color=WEIGHT),t('구조 · 정밀도 · 학습 조건에 따라 다름',-1.7,size=28,color=MUTED),t('NFI가 있어도 눈에 보이는 급등은 없을 수 있음',-3.1,size=24,color=MUTED),t('Liu et al. (2026) · arXiv:2605.06152',-4.45,size=21,color=MUTED))
def closing():
    return VGroup(t('수학적 대칭성',3.6,size=29,color=GOOD),label('공통 방향의 기울기 = 0',2.2,GOOD),t('유한 정밀도',.6,size=29,color=PRUNE),label('상쇄되지 않은 잔여 → 피드백',-.8,PRUNE),t('반올림이 만든 작은 차이를',-2.7,size=30),t('학습 과정이 증폭시킬 수 있다',-3.8,size=30,color=ACCENT))
TITLES=['잘 학습되다가 갑자기 치솟는 손실','2026 · Grokking or Glitching?','작은 반올림이 왜 문제가 될까?','먼저 Softmax의 대칭성을 보자','점수를 확률로 바꾸는 함수','확률의 합은 1','또 하나의 대칭성','모든 점수에 같은 수를 더하면?','함께 움직여도 예측은 그대로','손실도 그대로여야 한다','로짓 기울기의 합은 0','음수와 양수가 정확히 상쇄','거의 완벽하게 맞히기 시작하면','1에 가까운 확률이 1로 반올림','정답의 음수 기울기는 0','오답의 작은 양수는 남는다','기울기 합이 0이 아니게 된다','이 잔여 성분이 중요한 이유','공통 방향에는 기울기가 없어야 한다','없어야 할 방향의 성분이 생긴다','로짓 공간에서 특징 공간으로','마지막 층이 점수를 계산한다','가중치는 특징의 학습에도 영향','가중치 평균과 특징 평균','서로의 다음 변화를 키운다','단순한 누적을 넘어선 피드백','Numerical Feature Inflation','기울기 재등장 → 큰 갱신 → 급등','모든 급등의 원인은 아니다','작은 오차에서 시작된 변화','수학적 대칭성과 수치적 학습의 차이','작은 차이를 증폭하는 학습','숫자의 차이가 움직임의 차이로','단 하나의 반올림이었을까?']
CAPS=['안정적으로 줄던 손실이\n갑자기 치솟을 수 있습니다.','특정한 손실 급등의 원인을\n유한 정밀도 계산에서 찾은 연구입니다.','작은 반올림이\n어떻게 학습을 뒤흔들까요?','Softmax의 특별한 성질부터\n살펴보겠습니다.','여러 클래스의 점수가\n예측 확률로 바뀝니다.','정확한 수학에서\n예측 확률의 합은 1입니다.','확률의 합 외에도\n대칭성이 하나 더 있습니다.','모든 점수에 같은 숫자를 더해도\n예측 확률은 변하지 않습니다.','공통 이동 방향에서는\n예측에 변화가 없습니다.','예측이 같으므로\n해당 손실도 변하지 않습니다.','Softmax와 Cross Entropy의\n로짓 기울기를 더하면 0입니다.','정답의 음수와 나머지 양수가\n정확하게 상쇄됩니다.','그런데 고확신 상태의 계산에서는\n문제가 생길 수 있습니다.','유한 정밀도에서는 1에 가까운 값이\n정확히 1로 반올림될 수 있습니다.','정답 클래스의 음수 기울기가\n0이 됩니다.','다른 클래스들의 작은 양수는\n남아 있을 수 있습니다.','반드시 0이어야 할 합이\n실제 계산에서는 0이 아니게 됩니다.','이 작은 잔여가\n왜 중요할까요?','모든 점수가 함께 움직이는 방향에는\n학습할 기울기가 없어야 합니다.','상쇄가 깨지면 원래 없던 방향으로\n가중치가 움직일 수 있습니다.','이 불균형이 가중치 업데이트를 거쳐\n앞선 특징 표현에도 영향을 줍니다.','마지막 분류층은 특징을 이용해\n클래스 점수를 계산합니다.','역전파에서는 분류층의 가중치가\n앞선 특징의 학습에도 영향을 줍니다.','가중치 평균의 이동은\n특징 평균의 학습에도 영향을 줄 수 있습니다.','특징이 가중치를 바꾸고,\n그 가중치가 다시 특징을 바꿉니다.','이미 커진 변화가\n다음 변화를 더 크게 만듭니다.','이러한 양의 피드백을\nNumerical Feature Inflation이라 부릅니다.','특정 조건에서는 기울기 재등장과 큰 갱신이\n손실 급등으로 이어질 수 있습니다.','모든 손실 급등이\n이 반올림에서 비롯되는 것은 아닙니다.','이 연구는 학습을 이해하는 데\n계산 정밀도도 중요함을 보여줍니다.','아무 변화도 없어야 할 방향이\n수치적 학습에서는 새 성분으로 나타납니다.','신경망의 학습 과정은\n그 작은 차이도 증폭시킬 수 있습니다.','숫자가 조금 달라진 것을 넘어\n없어야 할 방향의 움직임이 생긴 것입니다.','작은 반올림과 그것을 증폭한 학습.\n그 연결이 핵심입니다.']
class NumericalFeatureInflation(Scene):
    def panel(self,i):
        if i<3:return loss_intro()
        if 3<=i<=9:return logits(2 if i>=8 else 0)
        if i in [10,11,12]:return balance()
        if i==13:return rounded()
        if i in [14,15,16]:return balance(True)
        if i in [17,18,19,30,32]:return geometry(i in [19,30,32])
        if i in [20,21,22]:return classifier(i!=21)
        if i in [23,24]:return means()
        if i in [25,26,31]:return growth()
        if i==27:return trigger()
        if i==28:return caveat()
        return closing()
    def construct(self):
        data=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))
        for i,s in enumerate(data['segments']):
            self.clear();self.add(t('신경망의 역설  /  09',7.35,size=20,color=MUTED),t('신경망을 무너뜨린 것은\n단 하나의 반올림이었다?',6.45,size=31),Line([-3.85,5.65,0],[3.85,5.65,0],color=MUTED,stroke_opacity=.3),t(TITLES[i],5.05,size=25,color=ACCENT),t(CAPS[i],-6.15,size=24),t('Grokking or Glitching? · Numerical Feature Inflation',-7.45,size=17,color=MUTED))
            p=self.panel(i);self.play(FadeIn(p),run_time=.25)
            if i<3:self.play(Create(p.curve),run_time=1.7)
            if i in [6,7]:
                self.play(*[Transform(b,new) for b,new in zip(p.bars,p.targets)],FadeOut(p.nums),run_time=1.5)
                for j,z in enumerate(p.z):self.add(t(f'{z+2:g}',p.base+(z+2)*.72+.3,-3.15+j*.95,size=23))
            if i==5:self.play(Indicate(p[-3],color=GOOD),run_time=.7)
            if i==11:self.play(p.neg.animate.shift(RIGHT*1.2),p.pos.animate.shift(LEFT*1.2),run_time=1)
            if i==14:
                p.neg.set_opacity(1);self.play(FadeOut(p.neg),run_time=.9)
            if i in [15,16]:self.play(Indicate(p.pos,color=PRUNE),run_time=.8)
            if i in [23,24]:
                for length in [1.05,1.55,2.5]:
                    self.play(Transform(p.w,Arrow(p.center,p.center+LEFT*length,buff=0,color=ORANGE,stroke_width=7)),run_time=.32)
                    self.play(Transform(p.h,Arrow(p.center,p.center+RIGHT*length,buff=0,color=WEIGHT,stroke_width=7)),run_time=.32)
            if i in [25,26,31]:
                self.play(Create(p[4]),Create(p[5]),run_time=1.2)
            if i==27:
                for j in [7,8,9]:self.play(Circumscribe(p[j],color=PRUNE),run_time=.6)
            remaining=s['end']-self.time
            if remaining<-.03:raise RuntimeError(f'Timing overrun {i}: {self.time}')
            self.wait(max(remaining,0))
        assert abs(self.time-173)<.04
