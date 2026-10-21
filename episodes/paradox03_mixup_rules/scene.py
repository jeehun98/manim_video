"""Mixup imposes behavior between examples, rather than observing new truths."""
import json
import sys
from pathlib import Path
from PIL import Image,ImageOps
from manim import *

sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visual_library.manim import FONT,BG,INK,MUTED,WEIGHT,PRUNE,SPARSE,ACCENT,GOOD,configure_vertical
configure_vertical()
config.disable_caching=True
ROOT=Path(__file__).resolve().parent

def t(s,y=0,x=0,size=28,color=INK,width=7.7):
    obj=Text(s,font=FONT,font_size=size,color=color,line_spacing=1.2)
    if obj.width>width:obj.scale_to_fit_width(width)
    return obj.move_to([x,y,0])

def photo_array(name):
    image=Image.open(ROOT/'assets'/name).convert('RGBA')
    image=ImageOps.contain(image,(320,384))
    canvas=Image.new('RGBA',(320,384),'#162431')
    canvas.alpha_composite(image,((320-image.width)//2,(384-image.height)//2))
    return np.array(canvas.convert('RGB'),dtype=float)

def mixed_image(lam,height=3.1,x=0,y=1):
    # Mathematical input interpolation, using the same lambda as the labels.
    array=np.rint(lam*photo_array('cat_photo.png')+(1-lam)*photo_array('dog_photo.png')).astype(np.uint8)
    return ImageMobject(array).set_height(height).move_to([x,y,0])

def photo_panel(lam=.5):
    return Group(mixed_image(1,2.3,-2.5,2.2),mixed_image(0,2.3,2.5,2.2),
                 t('고양이 A',.65,-2.5,size=24,color=WEIGHT,width=2),t('강아지 B',.65,2.5,size=24,color=SPARSE,width=2),
                 Arrow([-1.35,1.8,0],[-.65,.1,0],color=MUTED,buff=.1),Arrow([1.35,1.8,0],[.65,.1,0],color=MUTED,buff=.1),
                 mixed_image(lam,2.9,0,-1.5),t(f'입력 혼합  {100*lam:g} : {100*(1-lam):g}',-3.45,size=28,color=ACCENT),
                 t('픽셀값의 선형 혼합',-4.3,size=21,color=MUTED))

def prediction(lam,amount=1):
    return .02+.96*lam+amount*.29*np.sin(4*np.pi*lam)*np.sin(np.pi*lam)

def chart(amount=1,show_target=False):
    ax=Axes(x_range=[0,1,.25],y_range=[0,1,.25],x_length=6.35,y_length=3.9,tips=False,axis_config={'color':MUTED,'stroke_width':1.5}).move_to([0,.6,0])
    curve=ax.plot(lambda v:prediction(v,amount),x_range=[0,1,.005],color=PRUNE,stroke_width=3)
    labels=VGroup(t('고양이 예측 확률',3.25,size=25,color=PRUNE),t('0',-1.75,-3.15,size=20,color=MUTED),t('1',-1.75,3.15,size=20,color=MUTED),
                  t('0',-1.35,-3.65,size=20,color=MUTED),t('1',2.55,-3.65,size=20,color=MUTED),
                  t('강아지 B',-2.4,-2.65,size=23,color=SPARSE,width=2),t('고양이 A',-2.4,2.65,size=23,color=WEIGHT,width=2),
                  t('λ · 고양이 A의 혼합 비율',-3.15,size=24,color=MUTED),t('설명용 함수 · 실제 실험 결과가 아님',-4.45,size=20,color=MUTED))
    endpoints=VGroup(*[Dot(ax.c2p(v,prediction(v)),color=GOOD,radius=.09) for v in [0,1]])
    target=DashedVMobject(ax.plot(lambda v:v,x_range=[0,1],color=WEIGHT,stroke_width=3),num_dashes=25) if show_target else VGroup()
    legend=t('실선: 예측 p     점선: 설정한 목표 q',4.08,size=21,color=MUTED) if show_target else t('양 끝의 분류가 맞아도 중간 행동은 미정',4.08,size=22,color=MUTED)
    return VGroup(ax,curve,labels,endpoints,target,legend)

def segment(y=1.3):
    return VGroup(Line([-3.1,y,0],[3.1,y,0],color=MUTED,stroke_width=3),Dot([-3.1,y,0],color=SPARSE,radius=.12),Dot([3.1,y,0],color=WEIGHT,radius=.12),
                  t('강아지 B',y-.6,-2.8,size=24,color=SPARSE,width=2),t('고양이 A',y-.6,2.8,size=24,color=WEIGHT,width=2),
                  t('λ = 0',y+.6,-2.8,size=22,color=MUTED,width=2),t('λ = 1',y+.6,2.8,size=22,color=MUTED,width=2))

class MixupRules(Scene):
    def chrome(self,i):
        titles=['고양이와 강아지를 절반씩','현실에 없는 혼합 입력','목표도 50 대 50','가상의 입력이 실제 예측을 돕는다?','Mixup','왜 도움이 될까?',
                '각 데이터의 정답을 알려준다','양 끝만 맞히면 충분할까?','중간의 예측은 불규칙할 수 있다','Mixup · 새로운 규칙을 더한다','70 대 30 입력 · 70 대 30 목표','50 대 50 입력 · 50 대 50 목표',
                '이미지를 입력 공간의 점으로','두 점 사이의 무수한 입력','입력 비율과 목표 비율을 함께','실제 정답을 발견한 것은 아니다','우리가 정한 행동 규칙','그 규칙에 가까워지도록 학습','데이터 사이의 불규칙성을 억제','예측 함수에 가하는 정규화','키메라의 정체를 다시 보면','새로운 생명체에 대한 지식일까?','데이터 사이의 행동 규칙까지']
        return VGroup(t('신경망의 역설  /  03',7.35,size=20,color=MUTED),t('신경망은 키메라를 학습할 때\n더 똑똑해진다?',6.45,size=31),
                      Line([-3.85,5.65,0],[3.85,5.65,0],color=MUTED,stroke_opacity=.3),t(titles[i],5.05,size=25,color=ACCENT),t('Mixup · 입력 사이의 예측 규칙',-7.45,size=18,color=MUTED))

    def construct(self):
        data=json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))
        caps=['고양이와 강아지 사진을\n절반씩 섞었습니다.','현실에서는 보기 어려운\n이상한 이미지입니다.','이 입력의 목표를 고양이 50%,\n강아지 50%로 정합니다.','가상의 데이터로 실제 이미지의\n예측 성능도 개선할 수 있습니다.','이것이 Mixup입니다.','왜 존재하지 않는 데이터를\n학습하는 것이 도움이 될까요?',
              '보통은 고양이에는 고양이,\n강아지에는 강아지라는 정답을 줍니다.','양 끝의 사진을 정확히 구분해도\n그 사이의 합리적인 예측은 보장되지 않습니다.','중간의 예측은 갑자기 뒤집히거나\n불규칙하게 변할 수 있습니다.','Mixup은 여기에\n새로운 규칙을 부여합니다.',
              '70 대 30으로 섞은 입력에는\n고양이 70%, 강아지 30%라는 목표를 줍니다.','절반씩 섞으면\n목표도 50 대 50입니다.','두 이미지를\n입력 공간의 점으로 보겠습니다.','두 점을 잇는 선분 위에는\n무수히 많은 점이 있습니다.',
              '선분 위에 입력을 만들고, 목표 확률도\n혼합 비율에 따라 선형적으로 정합니다.','혼합 입력에 실제로\n그런 정답이 존재한다는 뜻은 아닙니다.','데이터 사이에서 따라야 할 예측 규칙을\n우리가 인위적으로 정한 것입니다.',
              '예측도 입력의 혼합 비율에 맞춰\n부드럽게 변하도록 학습시킵니다.','학습 데이터의 정답뿐 아니라,\n그 사이의 불규칙한 행동도 억제합니다.','이것이 Mixup의\n정규화 효과입니다.','처음에는 존재하지 않는\n키메라를 학습시키는 것처럼 보였습니다.',
              'Mixup이 추가하는 것은\n새로운 생명체에 대한 지식이 아닙니다.','알고 있는 데이터 사이에서\n신경망이 따라야 할 새로운 행동 규칙입니다.']
        for i,s in enumerate(data['segments']):
            self.clear();self.add(self.chrome(i),t(caps[i],-6.15,size=24))
            panel=self.panel(i)
            self.play(FadeIn(panel),run_time=.3)
            if i==7:
                self.play(Transform(panel[1],panel[0].plot(lambda v:prediction(v,.25),x_range=[0,1,.005],color=PRUNE,stroke_width=3)),run_time=1)
                self.play(Transform(panel[1],panel[0].plot(lambda v:prediction(v),x_range=[0,1,.005],color=PRUNE,stroke_width=3)),run_time=1)
            if i==9:
                q=DashedVMobject(panel[0].plot(lambda v:v,x_range=[0,1],color=WEIGHT,stroke_width=3),num_dashes=25)
                self.play(Create(q),Transform(panel[5],t('실선: 예측 p     점선: 설정한 목표 q',4.08,size=21,color=MUTED)),run_time=1.1)
                self.play(FadeIn(t('설정한 목표: q고양이 = λ',-3.85,size=24,color=WEIGHT)),run_time=.4)
            if i==13:
                self.play(LaggedStart(*[FadeIn(Dot([-3.1+6.2*v,1.3,0],color=ACCENT,radius=.055)) for v in np.linspace(.05,.95,19)],lag_ratio=.04),run_time=1.4)
            if i==14:
                dot=Dot([-3.1+6.2*.3,1.3,0],color=ACCENT,radius=.11)
                self.add(dot)
                self.play(dot.animate.move_to([-3.1+6.2*.7,1.3,0]),run_time=1.3)
                self.play(dot.animate.move_to([0,1.3,0]),run_time=.8)
            if i in [17,18]:
                a=ValueTracker(1 if i==17 else .22)
                curve=always_redraw(lambda:panel[0].plot(lambda v:prediction(v,a.get_value()),x_range=[0,1,.01],color=PRUNE,stroke_width=3))
                panel[1].set_opacity(0);self.add(curve)
                self.play(a.animate.set_value(.22 if i==17 else .07),run_time=2)
                curve.clear_updaters()
            if i==22:
                self.play(FadeIn(t('기존 학습: 각 데이터의 정답을 알려준다',-.5,size=27,color=MUTED)),run_time=.5)
                self.wait(.5)
                self.play(FadeIn(t('Mixup: 데이터 사이의 예측 규칙까지 알려준다',-2,size=27,color=WEIGHT)),run_time=.6)
            remain=s['end']-self.time
            if remain<-.04:raise RuntimeError(f'Timing overrun {i}: {self.time}')
            if remain>0:self.wait(remain)
        assert abs(self.time-109)<1/30+.001

    def panel(self,i):
        if i in [0,1,2,4,5,10,11,20]:
            lam=.7 if i==10 else .5
            p=photo_panel(lam)
            if i in [2,10,11]:
                p.remove(p[-1]);p.add(t(f'목표  고양이 {100*lam:g}% · 강아지 {100*(1-lam):g}%',-4.3,size=25,color=WEIGHT))
            return p
        if i==3:return Group(mixed_image(.5,3,0,1.9),Arrow([0,.1,0],[0,-1.2,0],color=MUTED),t('실제 이미지의 예측에도 도움',-2,size=32,color=GOOD),t('효과는 데이터·모델·학습 조건에 따라 다름',-3.6,size=22,color=MUTED))
        if i==6:return Group(mixed_image(0,3,-2,1.5),mixed_image(1,3,2,1.5),t('강아지 → 강아지',-.65,-2,size=25,color=SPARSE,width=3.5),t('고양이 → 고양이',-.65,2,size=25,color=WEIGHT,width=3.5),segment(-2.6),t('양 끝에서의 정답',-4.4,size=27,color=GOOD))
        if i in [7,8,9,17,18]:return chart(1 if i!=18 else .22,i in [17,18])
        if i in [12,13,14]:
            return VGroup(segment(),t('입력 공간의 두 점과 선분',3.6,size=28,color=MUTED),t('x̃ = λxA + (1−λ)xB',-.6,size=32,color=ACCENT),
                          t('q̃ = λyA + (1−λ)yB',-1.85,size=32,color=WEIGHT),t('같은 λ로 입력과 목표를 함께 혼합',-3.1,size=25,color=GOOD),t('입력 공간의 1차원 단면 · 모든 선분을 전수 학습하지 않음',-4.4,size=19,color=MUTED))
        if i in [15,16,21]:
            return VGroup(segment(2.5),t('관측한 정답',.8,size=30,color=MUTED),t('≠',-.05,size=35,color=PRUNE),t('혼합 비율로 설정한 목표',-1.05,size=32,color=WEIGHT),
                          t('우리가 부여한 선형 행동의 가정',-2.6,size=28,color=ACCENT),t('실제 세계의 중간 정답을 발견한 것이 아님',-4.1,size=23,color=MUTED))
        if i==19:return VGroup(t('혼합 입력에서',3,size=31,color=MUTED),t('f(λxA + (1−λ)xB)',1.5,size=36,color=PRUNE),t('≈',.2,size=45,color=ACCENT),t('λyA + (1−λ)yB',-1.1,size=36,color=WEIGHT),
                              t('f: 예측 확률 · 선형 거동을 유도하는 목표',-2.6,size=22,color=MUTED),t('가정이 유용할 때 일반화에 도움',-4,size=27,color=GOOD))
        return VGroup(segment(2.5),t('혼합 데이터를 통해 예측 함수에 제약을 추가',-3.7,size=25,color=ACCENT),t('중간의 실제 정답 발견이 아닌, 행동 규칙의 설정',-4.5,size=21,color=MUTED))
