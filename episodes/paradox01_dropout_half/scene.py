"""Dropout: expected loss, linear penalty and the symmetry at r=1/2."""
import json
import sys
from pathlib import Path
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from visual_library.manim import FONT, BG, INK, MUTED, WEIGHT, PRUNE, SPARSE, ACCENT, GOOD, configure_vertical

configure_vertical()
config.disable_caching = True
ROOT = Path(__file__).resolve().parent


def t(s, y=0, x=0, size=29, color=INK, width=7.7):
    obj = Text(s, font=FONT, font_size=size, color=color, line_spacing=1.2)
    if obj.width > width:
        obj.scale_to_fit_width(width)
    return obj.move_to([x, y, 0])


def network(mask=None, scale=1):
    mask = [1]*8 if mask is None else mask
    layers = [VGroup(*[Circle(.17, color=WEIGHT, fill_color=WEIGHT, fill_opacity=.8)
                        .move_to([x, (n-1)*.39-j*.78, 0]) for j in range(n)])
              for x, n in [(-2.8, 4), (0, 8), (2.8, 3)]]
    edges = VGroup()
    for k in range(2):
        for i, a in enumerate(layers[k]):
            for j, b in enumerate(layers[k+1]):
                on = mask[j] if k == 0 else mask[i]
                edges.add(Line(a.get_center(), b.get_center(), stroke_width=1.3,
                               color=WEIGHT if on else ZERO_COLOR, stroke_opacity=.5 if on else .12))
    for i, node in enumerate(layers[1]):
        if not mask[i]:
            node.set_fill(BG, opacity=1).set_stroke(PRUNE, opacity=.6)
    return VGroup(edges, *layers).scale(scale)


ZERO_COLOR = '#31404D'


def bits(mask, y=0, size=.56):
    return VGroup(*[VGroup(Square(size, color=GOOD if b else PRUNE, stroke_width=1.5,
                                  fill_color=GOOD if b else PRUNE, fill_opacity=.13),
                          t(str(b), size=22, color=GOOD if b else PRUNE))
                   for b in mask]).arrange(RIGHT, buff=.12).move_to([0, y, 0])


def mask_grid(r):
    grid = VGroup()
    probabilities = []
    for m in range(256):
        alive = m.bit_count()
        p = (1-r)**alive * r**(8-alive)
        probabilities.append(p)
    peak = max(probabilities)
    for m, p in enumerate(probabilities):
        grid.add(Square(.355, color=WEIGHT, stroke_width=.65,
                        fill_color=WEIGHT, fill_opacity=.07+.88*p/peak)
                 .move_to([(m%16-7.5)*.395, (7.5-m//16)*.395+.4, 0]))
    return grid


class DropoutHalf(Scene):
    def chrome(self, i):
        titles = ['얼마나 꺼도 학습할 수 있을까?', '절반이 사라져도 학습한다',
                  '매번 달라지는 0과 1', '숨어 있는 수학적 구조', '8개의 스위치 · 256가지 조합',
                  '매번 하나의 마스크로 학습', '공유된 가중치 · 평균 손실', '평균을 내면 나타나는 벌점',
                  '선형 모델에서 정확히 계산하면', '큰 기여에는 큰 벌점', '그런데 왜 50%일까?',
                  '0/1 마스크의 분산', '50%에서 가장 불확실하다', '256개 마스크 · 같은 확률',
                  '어떤 조합도 특별하지 않다', '초기 연구의 효과적인 기본 설정', '50%의 특별함은 확률의 대칭성']
        return VGroup(t('신경망의 역설  /  01', 7.35, size=20, color=MUTED),
                      t('Dropout 50%가\n수학적으로 특별한 이유', 6.45, size=32),
                      Line([-3.85, 5.65, 0], [3.85, 5.65, 0], color=MUTED, stroke_opacity=.3),
                      t(titles[i], 5.08, size=26, color=ACCENT),
                      t('Dropout · 확률과 평균 손실', -7.45, size=18, color=MUTED))

    def construct(self):
        data = json.loads((ROOT/'timing.json').read_text(encoding='utf-8'))
        caps = [
            '신경망을 더 잘 학습시키려면\n뉴런을 얼마나 제거하는 것이 좋을까요?',
            '놀랍게도 절반, 50%를 제거하는 설정이\n효과적일 수 있습니다.',
            '학습 중 출력을 무작위로 0으로 만듭니다.\n매번 다른 뉴런이 꺼집니다.',
            '여기에는 흥미로운\n수학적 원리가 숨어 있습니다.',
            '뉴런 8개를 켜거나 끄는 조합은\n256가지입니다.',
            '매번 조합 하나를 선택하고\n그 상태의 손실을 줄입니다.',
            '가중치를 공유하는 부분 신경망들의\n평균 손실을 줄이는 학습입니다.',
            '이 무작위 학습 과정은\n정규화 효과도 만듭니다.',
            '선형 모델의 평균 제곱오차에는\n추가적인 벌점 항이 나타납니다.',
            '특정 뉴런의 기여가 커질수록\n벌점도 커집니다.',
            '그렇다면 제거율은\n왜 50%일까요?',
            '제거 확률이 r이면\n0/1 마스크의 분산은 r(1−r)입니다.',
            '50%에서 생존과 제거가\n가장 불확실해집니다.',
            '이때 256가지 마스크는\n모두 같은 확률로 선택됩니다.',
            '어떤 뉴런 조합도\n특별히 자주 선택되지 않습니다.',
            '초기 연구에서도 은닉 뉴런을 절반씩\n제거하는 설정을 기본값으로 사용했습니다.',
            '뉴런의 절반을 제거하는 50%.\n모든 마스크 조합이 균등해지는 지점입니다.'
        ]
        for i, seg in enumerate(data['segments']):
            self.clear()
            self.add(self.chrome(i), t(caps[i], -6.15, size=25))
            panel = self.panel(i)
            self.play(FadeIn(panel, shift=UP*.1), run_time=.4)
            if i == 0:
                for r, mask in [(20, [1,1,0,1,1,1,0,1]), (50, [1,0,1,0,0,1,0,1])]:
                    self.play(Transform(panel, VGroup(network(mask).shift(UP*.4),
                              t(f'Dropout Rate = {r}%', -3.25, size=35, color=ACCENT),
                              t('r = 각 뉴런의 제거 확률', -4.3, size=20, color=MUTED))), run_time=.65)
            if i == 2:
                for mask in [[0,1,0,1,1,0,1,0], [1,0,1,0,0,1,0,1]]:
                    self.play(Transform(panel[0], network(mask).shift(UP*.5)), run_time=.55)
                    self.play(Transform(panel[1], bits(mask, -3)), run_time=.3)
                self.wait(.6)
                self.play(Transform(panel, VGroup(network().scale(.75).shift(UP*.6),
                          t('평가 · Dropout을 끈다', -2.8, color=GOOD),
                          t('학습 중 생존 출력은 1/(1−r)배 보정', -3.7, size=22, color=MUTED))), run_time=.6)
            if i == 5:
                for k, mask in enumerate([[1,0,1,0,0,1,0,1], [0,1,0,1,1,0,1,0], [1,1,0,0,1,0,1,0]]):
                    self.play(Transform(panel[0], network(mask).scale(.8).shift(UP*.7)), run_time=.4)
                    self.play(Indicate(panel[1], color=GOOD), run_time=.4)
            if i == 9:
                self.play(Transform(panel[1], t('기여 2 → 벌점 4배', -1.35, size=37, color=PRUNE)),
                          panel[2].animate.stretch_to_fit_height(2.8).move_to([0,.5,0]), run_time=1.2)
            if i in [11, 12]:
                tracker = ValueTracker(.15 if i == 11 else .3)
                ax = panel[0]
                dot = always_redraw(lambda: Dot(ax.c2p(tracker.get_value(), tracker.get_value()*(1-tracker.get_value())), color=ACCENT, radius=.1))
                self.add(dot)
                self.play(tracker.animate.set_value(.5), run_time=1.5)
                if i == 12:
                    self.play(Circumscribe(panel[2], color=ACCENT), run_time=.7)
                dot.clear_updaters()
            if i == 13:
                self.wait(1)
                self.play(Transform(panel[0], mask_grid(.5)),
                          Transform(panel[1], t('r = 50% · 모든 조합이 균등', 4.05, size=25, color=GOOD)), run_time=1.5)
                self.play(Transform(panel[2], t('P(m) = (1/2)⁸ = 1/256', -3.65, size=32, color=GOOD)), run_time=.5)
            remaining = seg['end'] - self.time
            if remaining < -.04:
                raise RuntimeError(f'Timing overrun {i}: {self.time}')
            if remaining > 0:
                self.wait(remaining)
        assert abs(self.time-98) < 1/30+.001

    def panel(self, i):
        if i in [0,1]:
            return VGroup(network(None if i==0 else [1,0,1,0,0,1,0,1]).shift(UP*.4),
                          t('Dropout Rate = 0%' if i==0 else 'Dropout Rate = 50%', -3.25, size=35, color=ACCENT),
                          t('r = 각 뉴런의 제거 확률 · 정확히 절반을 강제하지 않음', -4.3, size=19, color=MUTED))
        if i == 2:
            return VGroup(network([1,0,1,0,0,1,0,1]).shift(UP*.5), bits([1,0,1,0,0,1,0,1],-3),
                          t('0 = 출력 차단 · 가중치는 보존', -4.15, size=23, color=MUTED))
        if i == 3:
            return VGroup(bits([1,0,1,0,0,1,0,1],1.8), t('무작위 선택',.3,color=WEIGHT),
                          Arrow([0,-.2,0],[0,-1.2,0],color=MUTED),t('평균 손실의 수학',-2,color=ACCENT,size=38))
        if i == 4:
            rows = VGroup(*[bits([(k>>j)&1 for j in range(8)]) for k in [0,1,2,3,170,255]]).arrange(DOWN,buff=.22).shift(UP*.6)
            return VGroup(rows,t('2 × 2 × 2 × 2 × 2 × 2 × 2 × 2',-2.8,size=25,color=MUTED),t('2⁸ = 256',-3.8,size=48,color=ACCENT))
        if i == 5:
            return VGroup(network([1,0,1,0,0,1,0,1]).scale(.8).shift(UP*.7),t('선택한 마스크 → 손실 → θ 갱신',-2.8,color=GOOD),t('θ는 다음 마스크에서도 이어서 사용',-3.9,size=23,color=MUTED))
        if i in [6,7]:
            nets=VGroup(*[network(m, .34) for m in [[1,0,1,0,0,1,0,1],[0,1,0,1,1,0,1,0],[1,1,0,0,1,0,1,0]]]).arrange(RIGHT,buff=.4).shift(UP*2)
            return VGroup(nets,t('L₁                L₂                L₃',.4,color=SPARSE),t('공유된 가중치 θ',-1,size=28,color=WEIGHT),t('min  Eₘ[L(fθ,ₘ(x), y)]',-2.35,size=35,color=ACCENT),t('매번 표본 하나로 평균 목표를 향해 갱신',-3.6,size=22,color=MUTED))
        if i == 8:
            return VGroup(t('독립 마스크 · 생존 확률 1−r',3.6,size=24,color=MUTED),
                          t('ŷₘ = Σᵢ wᵢxᵢ mᵢ/(1−r)',2.35,size=34,color=WEIGHT),
                          t('L = (y − ŷₘ)²',1.15,size=30),
                          t('Eₘ[L] = L₀ +',-.3,size=36),
                          t('r/(1−r) · Σᵢ(wᵢxᵢ)²',-1.5,size=39,color=PRUNE),
                          t('원래 손실 L₀ = (y − Σᵢwᵢxᵢ)²',-2.85,size=24,color=MUTED),
                          t('고정 입력의 기댓값 · 깊은 신경망 전체의 등식은 아님',-4,size=19,color=MUTED))
        if i == 9:
            return VGroup(t('r 고정 · 계수 r/(1−r)는 일정',3.6,size=24,color=MUTED),t('기여 1 → 벌점 1배',-1.35,size=37,color=PRUNE),
                          Rectangle(width=1.8,height=.7,color=PRUNE,fill_opacity=.5,fill_color=PRUNE).move_to([0,1.4,0]),
                          t('벌점 ∝ (wᵢxᵢ)²',-2.65,size=35,color=ACCENT),t('선형 모델의 기여 항을 비교',-4,size=23,color=MUTED))
        if i == 10:
            return VGroup(t('50%',1.5,size=100,color=ACCENT),t('성능의 최적값일까?\n확률의 특별한 지점일까?',-1.3,size=32),t('두 질문을 구분합니다',-3.5,size=24,color=MUTED))
        if i in [11,12]:
            ax=Axes(x_range=[0,1,.25],y_range=[0,.3,.1],x_length=6.6,y_length=3.7,tips=False,axis_config={'color':MUTED,'stroke_width':2}).shift(UP*.3)
            curve=ax.plot(lambda r:r*(1-r),x_range=[0,1],color=WEIGHT)
            label=t('Var(m) = r(1−r)',3.6,size=37,color=WEIGHT)
            return VGroup(ax,curve,label,t('0                    0.5                    1',-2.1,size=23,color=MUTED),
                          t('제거 확률 r',-2.8,size=24,color=MUTED),t('최대 1/4 · r = 0.5',-3.6,size=29,color=ACCENT),
                          t('0/1 마스크 분산 ≠ 보정 출력의 정규화 강도',-4.5,size=20,color=PRUNE))
        if i in [13,14]:
            return VGroup(mask_grid(.2 if i==13 else .5),t('r = 20% · 조합마다 다른 확률' if i==13 else 'r = 50% · 모든 조합이 같은 확률',4.05,size=25,color=GOOD),
                          t('P(m) = (1−r)ᵏ r⁸⁻ᵏ · k는 켜진 뉴런 수',-3.65,size=25,color=MUTED),
                          t('각 칸 = 8비트 마스크 하나 · 밝기는 상대 확률',-4.45,size=20,color=MUTED))
        if i == 15:
            return VGroup(network([1,0,1,0,0,1,0,1],.7).shift(UP*1.3),t('은닉 뉴런 유지 확률 0.5',-1.7,size=33,color=ACCENT),t('Srivastava et al. · JMLR 2014',-2.8,size=24,color=MUTED),
                          t('효과적인 기본 설정 · 보편적 최적값은 아님',-4,size=23,color=GOOD))
        return VGroup(t('50%',2.5,size=95,color=ACCENT),t('256가지 마스크\n각각 확률 1/256',.3,size=38,color=GOOD),t('독립적인 0/1 선택의\n엔트로피가 최대',-2,size=29,color=WEIGHT),
                      t('확률의 대칭성 ≠ 성능 최적성의 증명',-4,size=25,color=PRUNE))
