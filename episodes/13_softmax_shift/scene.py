"""Softmax 02: shift invariance, 84 seconds, narration-paced cuts."""
import os
import numpy as np
from manim import *

config.pixel_width = int(os.getenv('VIDEO_WIDTH', '1080'))
config.pixel_height = int(os.getenv('VIDEO_HEIGHT', '1920'))
config.frame_width, config.frame_height = 9, 16
config.frame_rate = 30
config.background_color = '#091119'
INK, MUTED, MINT = '#EDF3F7', '#94A7B7', '#61E4CF'
BLUE, GOLD, PINK = '#68D9F0', '#F3CF75', '#FF8C9D'
DURATION = 84
# Cue spacing follows spoken phrase length; transitions are included in each cue.
CAPTIONS = [
 (0, '앞에서 Softmax는 여러 개의 점수를\n하나의 분포로 바꾼다고 했습니다.'),
 (5, '그런데 조금 이상한 성질이 있습니다.'),
 (7.5, '[1, 2, 3]과\n[101, 102, 103]을 비교해보겠습니다.'),
 (13, '두 입력의 크기는 완전히 다르게 보입니다.'),
 (16, '하지만 Softmax를 적용하면\n두 경우 모두 같은 결과가 나옵니다.'),
 (21, '대략 [0.09, 0.24, 0.67]입니다.'),
 (24.5, '왜 이런 일이 생길까요?'),
 (26.5, 'Softmax 식을 다시 보겠습니다.'),
 (29, '모든 값에 같은 수 c를 더해보겠습니다.'),
 (32.5, '그러면 분자는\ne의 xᵢ제곱에 e의 c제곱을 곱한 값이 됩니다.'),
 (38, '분모의 모든 항에도\n똑같이 e의 c제곱이 곱해집니다.'),
 (42.5, '결국 위와 아래의 e의 c제곱이 약분되면서\n원래 Softmax와 완전히 같은 값이 남습니다.'),
 (49, '즉 Softmax는 숫자가 얼마나 큰지보다,\n서로 얼마나 차이나는지를 봅니다.'),
 (54, '[1, 2, 3]과 [101, 102, 103]은\n각 값 사이의 차이가 같기 때문에\n같은 분포를 만듭니다.'),
 (61, '이 성질은 단순히\n신기한 특징으로 끝나지 않습니다.'),
 (64.5, '실제로 Softmax를 계산할 때는\n아주 큰 수 때문에 생기는 문제를 피하기 위해'),
 (70, '모든 값에서 같은 값을 빼기도 합니다.'),
 (73, '그렇게 해도 결과는 변하지 않기 때문입니다.'),
 (77, '다음에는 이 차이가 Softmax 안에서\n얼마나 강하게 증폭되는지 살펴보겠습니다.'),
]

def txt(s, size=29, color=INK):
    m = Text(s, font='Malgun Gothic', font_size=size, color=color, line_spacing=1.15)
    if m.width > 7.5:
        m.scale_to_fit_width(7.5)
    return m

def exp(power, color=INK):
    base = txt('e', 38, color)
    exponent = txt(power, 22, color).next_to(base, UR, buff=.02).shift(DOWN*.1)
    return VGroup(base, exponent)

def product(*parts):
    return VGroup(*parts).arrange(RIGHT, buff=.17)

def fraction(top, bottom):
    line = Line(LEFT, RIGHT, color=INK).set_width(max(top.width, bottom.width)+.35)
    top.next_to(line, UP, buff=.16)
    bottom.next_to(line, DOWN, buff=.16)
    return VGroup(top, line, bottom)

def formula(shift=False, factored=False):
    if factored:
        top = product(exp('c', GOLD), exp('xᵢ'))
        bottom = product(exp('c', GOLD), txt('Σⱼ', 32), exp('xⱼ'))
    else:
        top = exp('xᵢ + c' if shift else 'xᵢ')
        bottom = product(txt('Σⱼ', 32), exp('xⱼ + c' if shift else 'xⱼ'))
    return fraction(top, bottom)

def distribution(y):
    p = np.exp(np.array([-2., -1., 0.])); p /= p.sum()
    group = VGroup()
    left = -3.2
    for v, c in zip(p, [BLUE, GOLD, PINK]):
        w = 6.4*v
        group.add(Rectangle(width=w, height=.42, stroke_width=0, fill_color=c, fill_opacity=.9).move_to([left+w/2, y, 0]))
        left += w
    return group

class SoftmaxShift(Scene):
    def until(self, t):
        if self.time > t+.05:
            raise ValueError(f'Timing overrun {self.time} > {t}')
        if t > self.time:
            self.wait(t-self.time)

    def cue(self, i):
        self.until(CAPTIONS[i][0])
        new = txt(CAPTIONS[i][1]).move_to(DOWN*5.85)
        self.play(FadeOut(self.sub), FadeIn(new), run_time=.18)
        self.sub = new

    def heading(self, s):
        self.play(Transform(self.head, txt(s, 31, MINT).move_to(UP*3.65)), run_time=.35)

    def construct(self):
        self.sub = txt(CAPTIONS[0][1]).move_to(DOWN*5.85)
        self.head = txt('점수 → 하나의 분포', 31, MINT).move_to(UP*3.65)
        self.add(txt('ACTIVATION FUNCTION SERIES', 19, MUTED).move_to(UP*6.85),
                 txt('Softmax', 66).move_to(UP*5.65),
                 txt('02  /  숫자가 달라도 결과가 같은 이유', 23, MINT).move_to(UP*4.65), self.head, self.sub)
        a = txt('[1, 2, 3]', 43, BLUE).move_to(UP*2.1)
        b = txt('[101, 102, 103]', 43, PINK).move_to(DOWN*.7)
        outa = txt('[0.09, 0.24, 0.67]', 32).move_to(UP*.7)
        bara = distribution(.05)
        self.play(FadeIn(a), FadeIn(outa), FadeIn(bara), run_time=.6)
        self.cue(1)
        self.heading('입력이 달라도, 결과는 같을까요?')
        self.cue(2)
        self.play(FadeOut(outa), FadeOut(bara), FadeIn(b), run_time=.45)
        offset = txt('모든 원소에 +100', 27, GOLD).move_to(UP*.7)
        self.play(FadeIn(offset), run_time=.4)
        self.cue(3)
        self.play(Indicate(a), Indicate(b), run_time=.6)
        self.cue(4)
        self.play(FadeOut(offset), FadeIn(outa), FadeIn(bara), run_time=.45)
        outb = outa.copy().move_to(DOWN*2.1)
        barb = distribution(-2.75)
        self.play(FadeIn(outb), FadeIn(barb), run_time=.5)
        self.cue(5)
        rounded = txt('출력은 동일 · 표시값은 반올림', 22, MUTED).move_to(DOWN*3.6)
        self.play(FadeIn(rounded), run_time=.3)
        self.cue(6)
        self.heading('왜 같을까요?')
        self.cue(7)
        self.play(*[FadeOut(m) for m in [a,b,outa,outb,bara,barb,rounded]], run_time=.35)
        f = formula().move_to(UP*.6)
        label = txt('softmax(x)ᵢ =', 31).next_to(f, LEFT, buff=.35)
        eq = VGroup(label, f).move_to(UP*.9)
        self.play(FadeIn(eq), run_time=.4)
        self.cue(8)
        self.heading('모든 원소에 같은 c를 더하면')
        shift = txt('xᵢ → xᵢ + c', 38, GOLD).move_to(UP*2.5)
        self.play(FadeIn(shift), FadeOut(label), Transform(f, formula(shift=True).move_to(UP*.9)), run_time=.5)
        self.cue(9)
        identity = product(exp('xᵢ + c'), txt('=', 34), exp('xᵢ'), exp('c', GOLD)).move_to(DOWN*1.6)
        self.play(FadeIn(identity), run_time=.5)
        self.cue(10)
        self.play(FadeOut(eq), FadeOut(identity), run_time=.3)
        factored = formula(factored=True).move_to(UP*.3)
        self.play(FadeIn(factored), run_time=.55)
        common = txt('분자와 분모에 공통 인자', 27, GOLD).move_to(DOWN*2)
        self.play(FadeIn(common), run_time=.35)
        self.cue(11)
        factors = [factored[0][0], factored[2][0]]
        slashes = VGroup(*[Line(m.get_corner(DL), m.get_corner(UR), color=PINK, stroke_width=4) for m in factors])
        self.play(Create(slashes), run_time=.5)
        self.play(FadeOut(slashes), Transform(factored, formula().move_to(factored)), FadeOut(common), run_time=.65)
        invariant = txt('softmax(x + c·1) = softmax(x)', 32, MINT).move_to(DOWN*2)
        note = txt('1: 모든 원소가 1인 벡터', 21, MUTED).move_to(DOWN*2.85)
        self.play(FadeIn(invariant), FadeIn(note), run_time=.45)
        self.cue(12)
        self.play(FadeOut(factored), FadeOut(shift), FadeOut(note), invariant.animate.move_to(DOWN*3.25), run_time=.4)
        self.heading('같은 이동은 차이를 바꾸지 않습니다')
        gap = txt('(xᵢ + c) − (xⱼ + c) = xᵢ − xⱼ', 31, GOLD).move_to(UP*.6)
        self.play(FadeIn(gap), run_time=.5)
        self.cue(13)
        self.play(FadeOut(gap), run_time=.2)
        rows = VGroup()
        for y, values, color in [(1.9, ['1','2','3'], BLUE), (-.8, ['101','102','103'], PINK)]:
            for x, v in zip([-2.6,0,2.6], values):
                rows.add(txt(v, 40, color).move_to([x,y,0]))
            for x in [-1.3,1.3]:
                rows.add(txt('+1', 25, GOLD).move_to([x,y-.65,0]))
                rows.add(Arrow([x-.55,y,0],[x+.55,y,0],buff=0,color=MUTED,stroke_width=2,tip_length=.12))
        self.play(FadeIn(rows), run_time=.5)
        self.cue(14)
        self.heading('계산을 안정적으로 만드는 성질')
        self.cue(15)
        self.play(FadeOut(rows), FadeOut(invariant), run_time=.3)
        big = txt('[1001, 1002, 1003]', 38, PINK).move_to(UP*2)
        warning = txt('지수값이 너무 커지면 → 오버플로', 27, PINK).move_to(UP*.85)
        self.play(FadeIn(big), FadeIn(warning), run_time=.5)
        self.cue(16)
        subtract = txt('모든 원소에서 최댓값 1003 빼기', 27, GOLD).move_to(DOWN*.3)
        stable = txt('[−2, −1, 0]', 42, BLUE).move_to(DOWN*1.45)
        self.play(FadeIn(subtract), FadeIn(stable), run_time=.5)
        self.cue(17)
        result = txt('같은 분포  [0.09, 0.24, 0.67]', 29, MINT).move_to(DOWN*2.7)
        self.play(FadeIn(result), run_time=.4)
        self.cue(18)
        self.play(*[FadeOut(m) for m in [big,warning,subtract,stable,result]], run_time=.35)
        self.heading('다음: 차이가 비중이 되는 방식')
        end = VGroup(txt('입력의 차이', 37, BLUE), txt('↓  지수함수', 28, MUTED),
                     txt('출력의 비율', 37, GOLD)).arrange(DOWN,buff=.45).move_to(UP*.2)
        self.play(FadeIn(end), run_time=.5)
        self.until(DURATION)
