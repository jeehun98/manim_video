"""A fixed-data experiment: confidence scaling versus function change."""
import json, sys
from pathlib import Path
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visual_library.manim import FONT, BG, INK, MUTED, configure_vertical
configure_vertical()
ROOT=Path(__file__).resolve().parent
BLUE='#4DA9FF'; GREEN='#27D3AF'; ORANGE='#FFB454'; PURPLE='#A78BFA'; GOOD='#58D68D'
POINTS=[(-2.3,1.6),(-1.7,.5),(-2,-1.4),(-1.2,-.6),(-1.4,1.9),(1.4,1.6),(2.2,.6),(1.3,-.8),(2.4,-1.6),(1.8,2)]

def text(s,y=0,x=0,size=28,color=INK,width=7.7):
    o=Text(s,font=FONT,font_size=size,color=color,line_spacing=1.2)
    if o.width>width:o.scale_to_fit_width(width)
    return o.move_to([x,y,0])

def box(s,y,color=PURPLE):
    return VGroup(RoundedRectangle(width=7.4,height=.85,corner_radius=.14,color=color,fill_color=BG,fill_opacity=1),text(s,size=26,color=color)).move_to([0,y,0])

def space(y=1,scale=1,rotated=False,unknown=False):
    a=Axes(x_range=[-3,3,1],y_range=[-2.5,2.5,1],x_length=6.8,y_length=4.7,tips=False,axis_config={'color':MUTED,'stroke_width':1,'include_ticks':False}).move_to([0,y,0])
    # The complete plotting frame, including its origin, is shared by both experiments.
    p=VGroup(a)
    p.dots=VGroup(*[Dot(a.c2p(x,v),radius=.095,color=BLUE if i<5 else GREEN) for i,(x,v) in enumerate(POINTS)])
    p.boundary=Line(a.c2p(.25*-2.4 if rotated else 0,-2.4),a.c2p(.25*2.4 if rotated else 0,2.4),color=ORANGE,stroke_width=4)
    if rotated:p.add(DashedLine(a.c2p(0,-2.4),a.c2p(0,2.4),color=MUTED,stroke_width=2))
    p.add(p.dots,p.boundary)
    if unknown:
        q=a.c2p(.3,2.05)
        p.add(Circle(radius=.18,color=WHITE).move_to(q),text('?',q[1],q[0],size=22,color=WHITE))
    p.axes=a
    p.scale(scale,about_point=[0,y,0])
    return p

def curves(kind='intro'):
    p=VGroup()
    for y,title,c,fn in [(2.6,'테스트 정확도' if kind=='conclusion' else '훈련 정확도',GOOD,(lambda x:.56+.02*np.sin(x*.5)) if kind=='conclusion' else (lambda x:min(1,.15+x*.35))),(-1.1,'훈련 손실',PURPLE,lambda x:.85*np.exp(-x*.5)+.04)]:
        a=Axes(x_range=[0,8,2],y_range=[0,1.1,.5],x_length=6.5,y_length=2.1,tips=False,axis_config={'color':MUTED,'stroke_width':1}).move_to([0,y,0])
        curve=a.plot(fn,x_range=[0,8,.05],color=c,stroke_width=4)
        p.add(a,curve,text(title,y+1.4,size=26,color=c))
    p.add(text('학습 단계 →',-2.7,size=22,color=MUTED))
    p.curves=[p[1],p[4]]
    return p

def comparison():
    p=VGroup(space(2.35,.67),space(-1.9,.67,True,True),text('① 로짓 확대 · 경계 고정',4.3,size=27,color=PURPLE),text('② 경계 회전 · 예측 변화 가능',.1,size=27,color=ORANGE),text('두 실험 모두 훈련 정확도 100%',-4.25,size=26,color=GOOD))
    return p

def vectors(projected=False):
    origin=np.array([-2.4,-.7,0]);end=origin+np.array([4,2.5,0]);other=origin+np.array([3.4,3.1,0])
    p=VGroup(text('파라미터 공간 · 2차원 개념도',4.2,size=24,color=MUTED))
    for r in [1,1.7,2.4,3.1]:p.add(Ellipse(width=r*2,height=r*1.15,color=MUTED,stroke_opacity=.3).rotate(.45).move_to([.5,.4,0]))
    p.add(Dot(origin,color=WHITE),Arrow(origin,end,buff=0,color=PURPLE,stroke_width=6),text('로짓 확대 방향 (NLM)',-2.25,size=27,color=PURPLE))
    p.update_arrow=Arrow(origin,other,buff=0,color=ORANGE,stroke_width=5)
    p.add(p.update_arrow,text('손실 감소 방향 −∇L',2.8,size=26,color=ORANGE))
    if projected:p.add(DashedLine(end,other,color=MUTED),text('평행 성분 억제 → 남은 성분으로 갱신',-3.65,size=25,color=GREEN))
    return p

def generalization():
    a=Axes(x_range=[0,10,2],y_range=[0,1.1,.5],x_length=6.6,y_length=4,tips=False,axis_config={'color':MUTED,'stroke_width':1}).move_to([0,.4,0])
    return VGroup(a,a.plot(lambda x:.12+.86/(1+np.exp(-2*(x-7.5))),x_range=[0,10,.05],color=MUTED),a.plot(lambda x:.12+.86/(1+np.exp(-2*(x-3.5))),x_range=[0,10,.05],color=GREEN),text('테스트 정확도',3.4,size=27),text('기존 갱신',-2.3,-1.7,size=24,color=MUTED),text('NLM 성분 억제',-2.3,1.7,size=24,color=GREEN),text('학습 단계 →',-3.2,size=23,color=MUTED),text('개념도 · 실제 실험 수치 아님',-4.3,size=22,color=MUTED))

TITLES=['정답은 모두 맞혔다','그런데 손실은 계속 감소한다','그다음, 무엇이 바뀔까?','동일한 데이터에서 시작','결정경계와 훈련 정확도','첫 번째 변화','로짓: 분류기가 출력하는 점수','점수의 크기만 키운다면?','클래스 예측과 경계는 그대로','정답 확률 ↑  손실 ↓','같은 예측, 더 낮은 손실','두 번째 변화','결정경계를 회전한다','훈련 정확도는 여전히 100%','훈련 데이터가 없는 곳에서는?','같은 정확도, 다른 예측 함수','두 변화의 차이','확신도의 변화와 규칙의 변화','경사하강법은 어디로 갈까?','현재 손실의 기울기를 따른다','2025 · 논문에서 관찰한 방향','Naive Loss Minimization','NLM 성분을 억제한 실험','예측 변화 ≠ 일반화 개선','이 연구가 보여주는 차이','손실 감소 ≠ 일반화','정답 이후에도 변화는 계속된다','학습은 무엇을 바꾸었는가?']
CAPS=['훈련 데이터의 정답을 모두 맞혔습니다.\n훈련 정확도 100%.','손실을 줄일 수 있는 방향은\n아직 남아 있습니다.','정답을 모두 맞힌 신경망은\n그다음 무엇을 배울까요?','파란 점과 초록 점을\n구분하는 분류기를 봅시다.','모든 점이 올바른 쪽에 있습니다.\n훈련 정확도 100%.','먼저, 점수의 크기만\n바꿔보겠습니다.','로짓의 부호로\n두 클래스를 구분합니다.','양수와 음수 로짓 모두\n동일한 양의 배율로 키웁니다.','예측 결과도, 결정경계도\n달라지지 않습니다.','정답 확률은 높아지고\n크로스 엔트로피 손실은 줄어듭니다.','새 분류 규칙 없이도\n손실은 감소합니다.','이번에는 결정경계 자체를\n바꿔보겠습니다.','훈련 점을 넘지 않는 범위에서\n경계를 조금 회전합니다.','모든 훈련 점의 분류는 그대로.\n정확도는 계속 100%.','같은 새 입력의 예측이\n다른 클래스로 바뀔 수 있습니다.','훈련 정확도가 같아도\n예측 함수는 달라질 수 있습니다.','무엇이 달라졌는지\n직접 비교해 봅시다.','첫 번째는 확신도, 두 번째는\n클래스를 구분하는 방식의 변화입니다.','실제 경사하강법은\n어느 방향을 선택할까요?','일반화를 직접 고르는 대신\n현재 손실을 줄이는 기울기를 따릅니다.','일부 신경망에서, 훈련 정답을 모두 맞힌 뒤\n로짓 확대 방향과 강한 정렬을 관찰했습니다.','예측을 유지하며 로짓을 키워\n손실을 줄이는 방향입니다.','이 성분을 억제하자 실험에서는\n일반화가 훨씬 빨리 진행됐습니다.','모든 경계 변화가 유익한 것은 아닙니다.\n두 변화가 늘 독립적인 것도 아닙니다.','손실과 일반화는\n서로 다른 사실을 말합니다.','손실이 줄어드는 것과 새 데이터를\n더 잘 구분하는 것은 같지 않습니다.','정답을 모두 맞힌 뒤에도\n신경망은 계속 변합니다.','얼마나 더 학습했는가보다,\n그 학습이 무엇을 바꾸었는가.']

class AfterAccuracy(Scene):
    def panel(self,i):
        if i<2:return curves()
        if i in [2,18,26]:return VGroup(Dot([0,-1,0],color=WHITE),*[Arrow([0,-1,0],[x,2,0],buff=.15,color=c) for x,c in [(-2.5,PURPLE),(2.5,ORANGE)]],text('훈련 정확도 100%',-3,size=32,color=GOOD))
        if 3<=i<=15:
            p=space(rotated=i>=12,unknown=i>=14)
            if i>=4:p.add(text('훈련 정확도 100%',4,size=30,color=GOOD))
            if i==3:p.remove(p.boundary)
            if 5<=i<=10:
                p.add(text('z < 0 → A',-1.9,-2,size=25,color=BLUE),text('z > 0 → B',-1.9,2,size=25,color=GREEN))
                if i in [6,7]:
                    p.numbers=VGroup(text('−2',2,-2,size=35,color=PURPLE),text('+2',2,2,size=35,color=PURPLE));p.add(p.numbers,text('z → kz   (k > 1)',-3.3,size=32,color=PURPLE))
                if i==8:p.add(box('경계 z = 0 · 위치 고정',-3.3,ORANGE))
                if i==9:
                    p.add(text('두 클래스 로짓 [z, 0] · 정답은 첫 클래스',-2.8,size=21,color=MUTED),text('z          2         4           8',-3.5,size=27,color=PURPLE),text('확률   88.1% → 98.2% → 99.97%',-4.2,size=25,color=GREEN),text('CE     0.127 → 0.018 → 0.00034',-4.8,size=24,color=PURPLE))
                if i==10:p.add(box('같은 예측 · 더 낮은 손실',-3.5))
            if i>=13:p.add(box('100% → 100%',-2.5,GOOD))
            if i>=14:p.add(text('새 입력: B → A',-3.6,size=31,color=ORANGE),text('참값 미정 · 예측 변화만 확인',-4.45,size=22,color=MUTED))
            return p
        if i in [16,17]:return comparison()
        if i==19:
            p=vectors();p.add(text('θ(t+1) = θ(t) − η∇L',-4.5,size=32));return p
        if i in [20,21]:
            p=vectors();p.add(text('Grokking at the Edge\nof Numerical Stability',-4,size=27,color=INK));return p
        if i==22:return generalization()
        if i==23:return VGroup(space(1,.85,True,True),box('예측이 바뀜 ≠ 더 잘 맞힘',-2.3,ORANGE),text('일반화 개선에는 새 데이터의 정답이 필요',-3.4,size=25,color=MUTED),text('확신도 변화와 경계 변화는 결합될 수 있음',-4.4,size=24,color=MUTED))
        if i in [24,25]:
            p=curves('conclusion');p.add(text('개념도 · 실제 실험 수치 아님',-3.35,size=21,color=MUTED),box('손실 최소화 ≠ 일반화',-4.25,ORANGE));return p
        return VGroup(text('얼마나 더 학습했는가?',2.5,size=32,color=MUTED),text('그 학습은',.7,size=40),text('무엇을 바꾸었는가?',-.6,size=40,color=ORANGE))

    def construct(self):
        segments=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))['segments']
        for i,s in enumerate(segments):
            if i not in range(4,16):self.clear()
            else:
                # Reconstruct at exactly identical coordinates; no camera movement or data movement.
                self.clear()
            self.add(text('정답 이후의 신경망',7.25,size=22,color=MUTED),text('정답을 모두 맞혔다면,\n학습은 끝난 걸까?',6.25,size=34),Line([-3.8,5.4,0],[3.8,5.4,0],color=MUTED,stroke_opacity=.3),text(TITLES[i],4.9,size=26,color=ORANGE),text(CAPS[i],-6.15,size=25),text('Prieto et al. · ICLR 2025  |  arXiv:2501.04697',-7.4,size=17,color=MUTED))
            p=self.panel(i)
            if 4<=i<=15:self.add(p)
            else:self.play(FadeIn(p),run_time=.3)
            if i in [0,1]:
                for c in p.curves:self.remove(c)
                self.play(*[Create(c) for c in p.curves],run_time=1.8)
            if i==7:
                for value in [4,8]:
                    self.play(Transform(p.numbers,VGroup(text(f'−{value}',2,-2,size=35,color=PURPLE),text(f'+{value}',2,2,size=35,color=PURPLE))),run_time=1.3)
            if i==12:
                target=p.boundary.copy();p.boundary.put_start_and_end_on(p.axes.c2p(0,-2.4),p.axes.c2p(0,2.4))
                self.play(Transform(p.boundary,target),run_time=1.5)
            if i==14:
                q=Dot(p.axes.c2p(.3,2.05),radius=.10,color=GREEN);self.add(q);self.play(q.animate.set_color(BLUE),run_time=1.4)
            if i in [20,21]:self.play(Indicate(p.update_arrow,color=ORANGE),run_time=1)
            if i==17:
                boundary=p[1].boundary;target=boundary.copy()
                center=boundary.get_center();length=boundary.get_length()
                boundary.put_start_and_end_on(center+DOWN*length/2,center+UP*length/2)
                counter=text('z × 1',.7,-2.7,size=23,color=PURPLE)
                self.add(counter)
                self.play(Transform(boundary,target),Transform(counter,text('z × 4',.7,-2.7,size=23,color=PURPLE)),run_time=2)
            if i==22:
                self.remove(p)
                v=vectors(True);self.add(v)
                origin=v.update_arrow.get_start();end=v.update_arrow.get_end()
                radial=np.array([4,2.5,0]);delta=end-origin
                perpendicular=delta-np.dot(delta,radial)/np.dot(radial,radial)*radial
                self.play(Transform(v.update_arrow,Arrow(origin,origin+perpendicular*3,buff=0,color=GREEN,stroke_width=5)),run_time=1.1)
                self.play(FadeOut(v),FadeIn(p),run_time=.4)
                self.remove(p[1],p[2]);self.play(Create(p[1]),Create(p[2]),run_time=2.1)
            if i==27:
                self.wait(max(0,s['end']-self.time-1));self.clear();self.add(text('그 학습은\n무엇을 바꾸었는가?',0,size=41,color=ORANGE))
            remaining=s['end']-self.time
            if remaining<-.04:raise RuntimeError(f'Timing overrun {i}: {self.time}')
            self.wait(max(0,remaining))
        assert abs(self.time-141)<.04
