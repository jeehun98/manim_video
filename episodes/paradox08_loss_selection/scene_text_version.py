"""Loss is a selection signal; distinguish LossHF from the Wikipedia result."""
import json,sys
from pathlib import Path
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visual_library.manim import FONT,BG,INK,MUTED,WEIGHT,PRUNE,SPARSE,ACCENT,GOOD,configure_vertical
configure_vertical()
config.disable_caching=True
ROOT=Path(__file__).resolve().parent
def t(s,y=0,x=0,size=28,color=INK,width=7.7):
    o=Text(s,font=FONT,font_size=size,color=color,line_spacing=1.2)
    if o.width>width:o.scale_to_fit_width(width)
    return o.move_to([x,y,0])
def box(s,y=0,color=WEIGHT,w=7.2,x=0):
    return VGroup(RoundedRectangle(width=w,height=1,corner_radius=.12,color=color,fill_color=BG,fill_opacity=1).move_to([x,y,0]),t(s,y,x,26,color,w-.3))
def selection(v):return v if 0<=v<=1 else 0
def curve():
    a=Axes(x_range=[0,1.6,.5],y_range=[0,1.1,.5],x_length=6.3,y_length=3.3,tips=False,axis_config={'color':MUTED}).move_to([0,1,0])
    g=VGroup(a,Line(a.c2p(0,0),a.c2p(1,1),color=GOOD,stroke_width=5),Line(a.c2p(1.01,0),a.c2p(1.6,0),color=PRUNE,stroke_width=5),Dot(a.c2p(1,1),color=GOOD),Circle(radius=.07,color=PRUNE,fill_color=BG,fill_opacity=1).move_to(a.c2p(1,0)),DashedLine(a.c2p(1,0),a.c2p(1,1),color=ACCENT))
    g.add(t('LossHF · 선택 확률',4,size=27,color=GOOD))
    g.add(t('1',2.6,-3.55,size=21,color=MUTED),t('0',-.65,-3.55,size=21,color=MUTED),t('τ',-1,1,size=26,color=ACCENT),t('사실의 손실 ℓ  →',-1.7,size=25,color=MUTED))
    g.add(t('ℓ ≤ τ : P = ℓ / τ',-2.65,size=30,color=GOOD),t('ℓ > τ : P = 0',-3.55,size=30,color=PRUNE),t('τ는 현재 배치의 손실 백분위수로 갱신',-4.5,size=21,color=MUTED))
    g.axis=a
    return g
def pipeline():
    g=VGroup()
    for s,y,c in [('학습 데이터',3.7,WEIGHT),('현재 신경망이 손실 계산',1.7,SPARSE),('손실 조건으로 선택',-.3,ACCENT),('선택된 신호로 신경망 갱신',-2.3,GOOD)]:g.add(box(s,y,c))
    for y in [3.1,1.1,-.9]:g.add(Arrow([0,y,0],[0,y-.7,0],color=MUTED,buff=.04))
    g.add(t('반복할 때마다 손실과 선택 기준도 달라진다',-4.3,size=23,color=MUTED))
    return g
def extremes(which=0):
    g=VGroup()
    rows=[('낮은 손실','반복되었거나 쉬운 사실일 수 있음','반복 비중 축소',WEIGHT),('임계값 이하','남겨진 사실의 학습 비중 조절','손실에 비례해 선택',GOOD),('임계값 초과','드물거나 어려운 사실일 수 있음','이번 학습 신호에서 제외',PRUNE)]
    for k,(s,d,r,c) in enumerate(rows):
        y=3.25-k*2.4
        g.add(box(s,y,c),t(d,y-.85,size=22,color=MUTED),t(r,y-1.5,size=25,color=c))
    g.add(t('손실은 빈도·난도의 대리 지표 · 일대일 대응 아님',-4.5,size=20,color=MUTED))
    return g
def roles():
    return VGroup(t('같은 필터, 서로 다른 역할',3.9,size=30,color=ACCENT),box('높은 손실을 제외 · Head',2.4,PRUNE),t('학습에 반영할 사실의 범위를 제한',1.25,size=27,color=PRUNE),box('매우 낮은 손실을 덜 반복 · Flatten',-.4,WEIGHT),t('남겨진 사실의 빈도 편중을 완화',-1.65,size=27,color=WEIGHT),t('빈도 평탄화의 이득은 데이터 분포에 따라 달라짐',-3.5,size=23,color=MUTED),t('LossHF = Head + Flattening',-4.45,size=26,color=GOOD))
def records():
    g=VGroup(t('레코드',3.9,-2.4,size=25),t('ℓ / τ',3.9,0,size=25),t('선택 확률',3.9,2.4,size=25,color=GOOD))
    for k,(v,p) in enumerate([(0.1,.1),(.45,.45),(.9,.9),(1.3,0)]):
        y=2.6-k*1.4;c=PRUNE if p==0 else GOOD
        g.add(t(chr(65+k),y,-2.4,color=MUTED),t(f'{v:.2f}',y,0),t(f'{p:.0%}',y,2.4,color=c),Line([-3.5,y-.6,0],[3.5,y-.6,0],color=MUTED,stroke_opacity=.25))
    g.add(t('LossHF · 설명용 레코드와 손실값',-3.8,size=23,color=MUTED))
    g.add(t('조건에 따른 필터링이라는 비유',-4.6,size=22,color=ACCENT))
    return g
def capacity():
    g=VGroup(t('모델의 크기는 그대로',3.8,size=31,color=GOOD),RoundedRectangle(width=6.8,height=4.2,color=SPARSE,fill_opacity=.03).move_to([0,.7,0]),t('유한한 파라미터',1.5,size=35,color=SPARSE),t('기억할 정보량에도 한계',-.2,size=30),t('어떤 사실을 얼마나 학습할 것인가?',-2.7,size=30,color=ACCENT),t('상자는 용량의 개념도 · 사실별 저장 슬롯이 아님',-4.4,size=20,color=MUTED))
    return g
def objective():
    return VGroup(box('학습 데이터의 평균 손실 ↓',2.9,WEIGHT),t('≠',1.2,size=48,color=ACCENT),box('정확히 답하는 사실 수의 직접 최대화',-.5,GOOD),t('많이 반복되는 데이터는',-2.4,size=29),t('목적함수에도 많이 반영된다',-3.5,size=29,color=WEIGHT),t('손실 최소화와 기억 성능은 같은 지표가 아니다',-4.5,size=21,color=MUTED))
def result():
    g=VGroup(t('Wikipedia · 110M 파라미터',4,size=29,color=ACCENT),t('동일 크기 모델 · 처음부터 사전학습',3.1,size=23,color=MUTED))
    for x,h,label,num,c in [(-1.8,2.5,'전체 데이터','1.0',MUTED),(1.8,3.25,'LossH-Wiki','약 1.3',GOOD)]:
        g.add(Rectangle(width=1.65,height=h,color=c,fill_color=c,fill_opacity=.6).move_to([x,-1.3+h/2,0]),t(num,-1.3+h+.4,x,size=32,color=c,width=2.9),t(label,-1.78,x,size=24,color=c,width=3.2))
    g.add(t('개체 사실 정확도 · 전체 학습을 1로 정규화',-2.4,size=23),t('이 결과는 LossHF가 아닌 LossH-Wiki',-3.35,size=25,color=ACCENT),t('테스트 문맥에서 정답 문자열을 생성할 확률로 평가',-4.15,size=20,color=MUTED),t('Ye · Feldman · Talwar (2026), §4.2',-4.7,size=20,color=MUTED))
    return g
def conclusion():
    return VGroup(box('손실 · 얼마나 틀렸는가',3.2,WEIGHT),t('↓',1.8,size=42,color=ACCENT),box('선택 · 무엇을 계속 가르칠 것인가',.3,ACCENT),t('↓',-1.1,size=42,color=GOOD),box('분포 · 무엇을 얼마나 학습하는가',-2.6,GOOD),t('더 많이 기억하려면, 배울 대상을 고른다',-4.4,size=28,color=INK))
TITLES=['손실로 학습 데이터를 고른다면?','2026 · 손실 기반 데이터 선택','손실 분포의 양쪽 극단','낮은 손실 · 반복 또는 쉬움','높은 손실 · 희소성 또는 어려움','손실에 따라 선택 확률을 바꾼다','제외와 반복 축소는 다른 역할','조건으로 레코드를 거르는 것처럼','왜 필터링이 도움이 될까?','기억 용량은 유한하다','손실 최소화와 사실 정확도의 차이','반복과 과부하를 함께 줄인다','사실의 범위와 학습 빈도를 조절','같은 크기로 약 1.3배','핵심은 단순한 데이터 감소가 아니다','학습 신호가 다음 선택을 바꾼다','무엇을 배우지 않을지 고른다']
CAPS=['자신의 손실값으로\n학습할 데이터를 선택합니다.','손실 기반 선택으로\n사실 기억 성능을 개선한 연구입니다.','아주 낮거나 높은 손실에\n서로 다른 역할을 부여합니다.','낮은 손실은 반복되었거나\n쉽게 예측되는 사실일 수 있습니다.','높은 손실은 드물거나\n기억하기 어려운 사실일 수 있습니다.','손실은 빈도와 난도를\n추정하는 대리 지표입니다.','높은 손실은 제외하고,\n매우 낮은 손실은 덜 반복합니다.','데이터베이스의 조건 필터처럼\n학습 신호를 선별합니다.','왜 더 적게 골라도\n더 많이 기억할 수 있을까요?','기억할 수 있는\n정보량에는 한계가 있습니다.','학습은 기억한 사실 수가 아니라\n데이터의 손실을 줄입니다.','반복의 편중과 과도한 사실의 양은\n용량 활용을 비효율적으로 만들 수 있습니다.','학습할 사실의 범위를 제한하고\n남겨진 사실의 비중도 조절합니다.','Wikipedia 실험에서는 같은 크기로\n약 1.3배의 개체 사실 성능을 얻었습니다.','단순히 데이터를\n줄인 것만이 핵심은 아닙니다.','손실이 선택을 바꾸고,\n선택이 다시 학습을 바꿉니다.','더 많이 기억하기 위해\n무엇을 배우지 않을지 고릅니다.']
class LossBasedSelection(Scene):
    def panel(self,i):
        if i in [0,1,15]:return pipeline()
        if i in [2,3,4]:return extremes(i)
        if i==5:return curve()
        if i in [6,11,12]:return roles()
        if i==7:return records()
        if i in [8,9]:return capacity()
        if i==10:return objective()
        if i==13:return result()
        return conclusion()
    def construct(self):
        data=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))
        for i,s in enumerate(data['segments']):
            self.clear()
            self.add(t('신경망의 역설  /  08',7.35,size=20,color=MUTED),t('무엇을 배우지 않을지\n고르는 신경망',6.45,size=33),Line([-3.85,5.65,0],[3.85,5.65,0],color=MUTED,stroke_opacity=.3),t(TITLES[i],5.05,size=25,color=ACCENT),t(CAPS[i],-6.15,size=24),t('Loss-based Data Selection · Cram Less to Fit More',-7.45,size=18,color=MUTED))
            p=self.panel(i);self.play(FadeIn(p,shift=UP*.1),run_time=.35)
            if i in [0,1,15]:
                for j in range(4):self.play(Circumscribe(p[j],color=ACCENT),run_time=.35)
            if i==5:
                dot=Dot(p.axis.c2p(.12,.12),color=ACCENT);self.add(dot)
                self.play(dot.animate.move_to(p.axis.c2p(.9,.9)),run_time=1.3)
                self.play(dot.animate.move_to(p.axis.c2p(1.3,0)).set_color(PRUNE),run_time=.5)
            if i==13:self.play(Circumscribe(p[6],color=GOOD),run_time=.7)
            remaining=s['end']-self.time
            if remaining<-.03:raise RuntimeError(f'Timing overrun: {i}')
            self.wait(max(0,remaining))
        assert abs(self.time-98)<.04
