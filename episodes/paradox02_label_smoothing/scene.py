"""Label smoothing on the probability simplex and its reverse-KL penalty."""
import json
import sys
from pathlib import Path
from manim import *

sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visual_library.manim import FONT,BG,INK,MUTED,WEIGHT,PRUNE,SPARSE,ACCENT,GOOD,configure_vertical
configure_vertical()
config.disable_caching=True
ROOT=Path(__file__).resolve().parent
VERTICES=np.array([[0,3.1,0],[-3.1,-2.27,0],[3.1,-2.27,0]])
HARD=np.array([1.,0.,0.])
UNIFORM=np.ones(3)/3
SMOOTH=np.array([.9,.05,.05])

def t(s,y=0,x=0,size=29,color=INK,width=7.7):
    obj=Text(s,font=FONT,font_size=size,color=color,line_spacing=1.2)
    if obj.width>width:obj.scale_to_fit_width(width)
    return obj.move_to([x,y,0])

def pos(p):return np.array(p)@VERTICES

def card(s,y=0,color=WEIGHT,w=7,h=1.2):
    return VGroup(RoundedRectangle(width=w,height=h,corner_radius=.13,color=color,stroke_width=1.5,fill_color=color,fill_opacity=.07).move_to([0,y,0]),t(s,y,size=27,color=color,width=w-.35))

def simplex():
    g=VGroup(Polygon(*VERTICES,color=MUTED,stroke_width=2,fill_color=WEIGHT,fill_opacity=.035))
    for a in [.2,.4,.6,.8]:
        for k in range(3):
            others=[j for j in range(3) if j!=k]
            p=np.zeros(3);p[k]=a;p[others[0]]=1-a
            q=np.zeros(3);q[k]=a;q[others[1]]=1-a
            g.add(Line(pos(p),pos(q),color=MUTED,stroke_width=.7,stroke_opacity=.18))
    g.add(t('고양이',3.62,size=25),t('강아지',-2.8,-2.9,size=25,width=2.2),t('자동차',-2.8,2.9,size=25,width=2.2))
    return g

def target(p=HARD):
    return Circle(.13,color=WEIGHT,stroke_width=3).move_to(pos(p))

def bars(p):
    g=VGroup()
    for i,(name,prob) in enumerate(zip(['고양이','강아지','자동차'],p)):
        y=2.2-i*1.5
        g.add(t(name,y,-2.9,size=26,width=1.5),RoundedRectangle(width=4,height=.46,corner_radius=.06,color=MUTED,stroke_width=1).move_to([.1,y,0]))
        if prob>0:
            g.add(Rectangle(width=4*prob,height=.43,stroke_width=0,fill_color=WEIGHT,fill_opacity=.85).move_to([-1.9+2*prob,y,0]))
        g.add(t(f'{100*prob:g}%',y,3,size=26,color=WEIGHT,width=1.5))
    return g

class LabelSmoothingSimplex(Scene):
    def chrome(self,i):
        titles=['정답을 일부러 흐린다면?','Label Smoothing','정답 목표 · One-Hot','정답 클래스는 그대로','왜 100%를 목표로 하지 않을까?',
                '확률분포를 하나의 점으로','꼭짓점 · 하나의 클래스에 100%','다가갈 수 있지만 닿을 수 없는 목표','99%에도 남아 있는 간격','경계의 목표를 내부로',
                '목표의 이동을 손실로 읽으면','정답 손실 + 균등분포 쪽의 제약','서로 다른 두 방향','두 목표의 균형','정확도 밖에서도 달라지는 것','틀린 클래스를 가르치는 걸까?',
                '바뀌는 것은 목표 확률분포','정답으로 집중 · 과도한 확신은 억제','Label Smoothing의 수학']
        return VGroup(t('신경망의 역설  /  02',7.35,size=20,color=MUTED),t('AI는 정답을 틀리게 가르쳐야\n더 잘 배운다',6.45,size=31),
                      Line([-3.85,5.65,0],[3.85,5.65,0],color=MUTED,stroke_opacity=.3),t(titles[i],5.05,size=25,color=ACCENT),
                      t('Label Smoothing · 확률분포의 기하학',-7.45,size=18,color=MUTED))

    def construct(self):
        data=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))
        caps=['정답을 일부러 틀리게 알려줘\n더 잘 학습시키는 방법이 있습니다.','바로 Label Smoothing입니다.',
              '일반적인 목표는 고양이 100%,\n나머지는 0%입니다.','목표를 고양이 90%, 강아지 5%,\n자동차 5%로 바꿉니다.','왜 정확한 정답을\n일부러 흐리게 만들까요?',
              '세 확률의 합은 1. 모든 확률분포를\n삼각형 안의 점으로 나타낼 수 있습니다.','각 꼭짓점은 한 종류를\n100% 확신하는 상태입니다.',
              'One-Hot 목표는 꼭짓점. 유한한 Softmax\n로짓으로는 정확히 도달할 수 없습니다.','99%에 도달해도\n목표까지 간격이 남아 있습니다.',
              'Label Smoothing은 목표를\n삼각형 내부로 옮깁니다.','손실 함수로 표현하면\n더 흥미로운 사실이 나타납니다.',
              '정답을 향하는 손실에, 균등분포에서\n과도하게 멀어지는 것을 억제하는 항이 더해집니다.',
              '하나는 정답으로 확률을 집중시키고,\n다른 하나는 과도한 집중을 억제합니다.','두 목표의 균형이\n새로운 목표 확률분포를 만듭니다.',
              '일반화뿐 아니라 확률의 신뢰도와\n내부 특징 표현에도 영향을 줄 수 있습니다.','처음에는 정답을 틀리게\n가르치는 것처럼 보였습니다.',
              '바꾸는 것은 정답 클래스가 아니라\n학습해야 하는 확률분포입니다.','정답을 향해 학습하면서\n과도한 확신을 억제합니다.','이것이 Label Smoothing의\n수학적 원리입니다.']
        for i,seg in enumerate(data['segments']):
            self.clear();self.add(self.chrome(i),t(caps[i],-6.15,size=24))
            panel=self.panel(i)
            self.play(FadeIn(panel,shift=UP*.06),run_time=.35)
            if i==3:
                self.play(Transform(panel[0],bars(SMOOTH)),run_time=1.2)
            if i==5:
                dot=Dot(pos([.5,.3,.2]),color=ACCENT,radius=.11);self.add(dot)
                self.play(dot.animate.move_to(pos([.25,.6,.15])),run_time=1)
                self.play(dot.animate.move_to(pos([.7,.15,.15])),run_time=1.1)
            if i==6:
                for v in VERTICES:self.play(Flash(v,color=WEIGHT,flash_radius=.3),run_time=.4)
            if i==7:
                dot=Dot(pos([.55,.225,.225]),color=ACCENT,radius=.11);self.add(dot)
                for p in [[.8,.1,.1],[.95,.025,.025],[.99,.005,.005]]:
                    self.play(dot.animate.move_to(pos(p)),run_time=.9)
            if i==9:
                self.play(panel[1].animate.move_to(pos(SMOOTH)),run_time=1.1)
                self.play(Flash(pos(SMOOTH),color=WEIGHT,flash_radius=.3),run_time=.5)
            if i==12:
                self.play(Indicate(panel[2],color=ACCENT),run_time=.8)
                self.play(Indicate(panel[3],color=SPARSE),run_time=.8)
            if i==13:
                dot=Dot(pos([.65,.175,.175]),color=ACCENT,radius=.1);self.add(dot)
                self.play(dot.animate.move_to(pos(SMOOTH)),run_time=1.2)
            if i==16:
                self.play(Transform(panel[2],target(SMOOTH)),run_time=1)
            remain=seg['end']-self.time
            if remain<-.04:raise RuntimeError(f'Timing overrun {i}: {self.time}')
            if remain>0:self.wait(remain)
        assert abs(self.time-96)<1/30+.001

    def panel(self,i):
        if i in [0,1,4,15]:
            return VGroup(t('정답 클래스',3,size=25,color=MUTED),card('고양이',1.7,color=GOOD),t('100%  →  90%',-.4,size=52,color=WEIGHT),
                          t('정답을 바꾼 걸까?\n확률 목표를 바꾼 걸까?',-2.6,size=32,color=ACCENT))
        if i in [2,3]:return VGroup(bars(HARD),t('q = (1, 0, 0)' if i==2 else 'q = (0.9, 0.05, 0.05)',-3,size=35,color=WEIGHT),t('정답 클래스: 고양이',-4.25,size=25,color=GOOD))
        if i in [5,6,7]:
            return VGroup(simplex(),target(),t('p고양이 + p강아지 + p자동차 = 1',-3.6,size=28,color=WEIGHT),
                          t('유한한 Softmax 출력은 삼각형 내부' if i==7 else '점의 위치 = 세 꼭짓점의 확률 가중합',-4.5,size=22,color=MUTED))
        if i==8:
            # Near-vertex inset: magnify coordinates about the vertex by 10.
            frame=RoundedRectangle(width=5.5,height=2.6,corner_radius=.1,color=MUTED).move_to([0,-2.55,0])
            apex=np.array([0,-1.5,0]);pred=apex+10*(pos([.99,.005,.005])-VERTICES[0])
            return VGroup(simplex().scale(.63).shift(UP*1.25),t('꼭짓점 주변 ×10 확대',-.8,size=22,color=MUTED),frame,
                          Circle(.1,color=WEIGHT,stroke_width=3).move_to(apex),Dot(pred,color=ACCENT,radius=.08),
                          Line(apex,pred,color=PRUNE,stroke_width=2),t('목표 100%',-1.5,1.3,size=22,color=WEIGHT,width=2.2),
                          t('예측 99%',-2.3,-1.4,size=22,color=ACCENT,width=2.2),t('남은 간격 1% · 목표는 고정',-4.4,size=24,color=PRUNE))
        if i==9:
            return VGroup(simplex(),target(),t('목표 q = (0.9, 0.05, 0.05)',-3.6,size=30,color=WEIGHT),t('내부 목표는 유한한 로짓으로 표현 가능',-4.5,size=22,color=GOOD))
        if i in [10,11]:
            return VGroup(card('L = 0.85 CE(y, p)',2.5,color=ACCENT),t('+',1.25,size=40),card('0.15 KL(u ∥ p)',.1,color=SPARSE),
                          t('+ 예측 p와 무관한 상수',-1.25,size=26,color=MUTED),t('y: One-Hot 정답 · u: 균등분포',-2.6,size=24),
                          t('p: 예측 확률 · KL의 방향은 u → p',-3.5,size=23,color=MUTED),t('예시의 혼합계수 ε = 0.15',-4.4,size=24,color=WEIGHT))
        if i in [12,13]:
            u=pos(UNIFORM);q=pos(SMOOTH)
            return VGroup(simplex(),DashedLine(u,VERTICES[0],color=MUTED,stroke_width=2),
                          Arrow(pos([.55,.225,.225]),pos([.85,.075,.075]),buff=0,color=ACCENT,stroke_width=5),
                          Arrow(pos([.85,.075,.075])+RIGHT*.22,u+RIGHT*.22,buff=0,color=SPARSE,stroke_width=5),
                          Dot(u,color=SPARSE,radius=.09),target(SMOOTH),t('u · 균등',-.95,1.1,size=22,color=SPARSE,width=2),
                          t('0.85 × 정답 + 0.15 × 균등',-3.5,size=27,color=WEIGHT),t('q = (0.9, 0.05, 0.05)',-4.35,size=30,color=WEIGHT),
                          t('정답으로',1.5,-1.35,size=20,color=ACCENT,width=1.6),t('균등으로',.45,1.45,size=20,color=SPARSE,width=1.6))
        if i==14:
            return VGroup(card('일반화 · 보지 못한 데이터',2.7,color=GOOD),card('확률의 신뢰도 · Calibration',.7,color=WEIGHT),card('내부 특징 표현 · Representation',-1.3,color=SPARSE),
                          t('효과는 모델·데이터·학습 조건에 따라 다름',-3.3,size=23,color=MUTED),t('항상 개선된다는 보장은 없음',-4.4,size=23,color=MUTED))
        if i==16:return VGroup(simplex(),t('정답 클래스: 고양이',-3.6,size=30,color=GOOD),target(),t('목표 확률분포만 변경',-4.5,size=24,color=WEIGHT))
        return VGroup(t('정답 클래스는 그대로',2.9,size=32,color=GOOD),t('목표 확률분포는 내부로',1.65,size=34,color=WEIGHT),
                      card('∂L/∂zᵢ = pᵢ − qᵢ',-.1,color=ACCENT,h=1.5),t('p = q 이면 해당 샘플의 로짓 기울기 0',-1.7,size=23,color=MUTED),
                      t('p: 예측 · q: 목표 · z: Softmax 이전 점수',-2.45,size=20,color=MUTED),
                      t('정답을 맞히는 것\n≠ 끝없이 확신하는 것',-3.8,size=33,color=INK))
