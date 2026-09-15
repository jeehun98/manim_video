"""Softmax 01 — scores to a distribution. Silent portrait master, 90s."""
import os
import numpy as np
from manim import *

config.pixel_width = int(os.getenv('VIDEO_WIDTH', '1080'))
config.pixel_height = int(os.getenv('VIDEO_HEIGHT', '1920'))
config.frame_width, config.frame_height = 9, 16
config.frame_rate = 30
config.background_color = '#091119'
INK, MUTED = '#EDF3F7', '#94A7B7'
COLORS = ['#68D9F0', '#F3CF75', '#FF8C9D']
MINT = '#61E4CF'
CAPTIONS = [
    (0, '여러 개의 값이 있을 때,\n어떤 값이 더 중요한지'),
    (5, '하나의 분포로 표현하고 싶다면\n어떻게 할까요?'),
    (11, '예를 들어 세 개의 점수가\n[1, 2, 3]이라고 해보겠습니다.'),
    (18, 'Softmax는 각각의 값에\n지수함수를 적용한 뒤,'),
    (25, '그 값들을 전체 합으로 나눕니다.'),
    (33, '그러면 모든 출력은 0보다 크고,\n전체를 더하면 정확히 1이 됩니다.'),
    (41, '[1, 2, 3]은 대략\n[0.09, 0.24, 0.67]로 바뀝니다.'),
    (48, '가장 큰 입력이 가장 큰 비중을 가지지만,\n나머지 값들도 완전히 사라지지는 않습니다.'),
    (57, '즉 Softmax는 여러 개의 점수를\n서로 비교 가능한 하나의 분포로 바꿉니다.'),
    (64, '그래서 분류 모델의 출력뿐만 아니라,'),
    (69, 'Attention처럼 여러 값에\n서로 다른 중요도를 부여할 때도 사용됩니다.'),
    (76, '하지만 여기서 한 가지 흥미로운 점이 있습니다.\nSoftmax가 실제로 중요하게 보는 것은\n각 숫자의 절대적인 크기가 아닙니다.'),
    (84, '다음에는 Softmax가 무엇을 기준으로\n이 분포를 만드는지 살펴보겠습니다.'),
]

def txt(s, size=29, color=INK):
    t = Text(s, font='Malgun Gothic', font_size=size, color=color, line_spacing=1.15)
    if t.width > 7.6:
        t.scale_to_fit_width(7.6)
    return t

def row(values, y, size=40):
    return VGroup(*[txt(v, size, c).move_to([x, y, 0])
                   for v, x, c in zip(values, [-2.5, 0, 2.5], COLORS)])

class SoftmaxIntroduction(Scene):
    def until(self, t):
        if self.time > t + .05:
            raise ValueError(f'Timing overrun: {self.time} > {t}')
        if t > self.time:
            self.wait(t - self.time)

    def cue(self, i):
        self.until(CAPTIONS[i][0])
        self.play(Transform(self.sub, txt(CAPTIONS[i][1]).move_to(DOWN*5.85)), run_time=.4)

    def construct(self):
        self.sub = txt(CAPTIONS[0][1]).move_to(DOWN*5.85)
        title = txt('Softmax', 66).move_to(UP*5.65)
        heading = txt('여러 점수, 하나의 분포', 32, MINT).move_to(UP*3.65)
        self.add(txt('ACTIVATION FUNCTION SERIES', 19, MUTED).move_to(UP*6.85),
                 title, txt('01  /  점수에서 분포로', 25, MINT).move_to(UP*4.65), heading, self.sub)
        scores = row(['1', '2', '3'], 1.9, 54)
        bars = VGroup(*[Rectangle(width=1.2, height=v*.65, stroke_width=0,
            fill_color=c, fill_opacity=.8).move_to([x, -.9+v*.325, 0])
            for v, x, c in zip([1, 2, 3], [-2.5, 0, 2.5], COLORS)])
        question = txt('어떤 값에 얼마나 비중을 줄까요?', 29, MUTED).move_to(DOWN*2.5)
        self.play(FadeIn(scores), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=.2), FadeIn(question), run_time=1.5)
        self.cue(1)
        self.cue(2)
        self.play(Indicate(scores), run_time=1)
        self.cue(3)
        self.play(FadeOut(bars), FadeOut(question), Transform(heading, txt('01  각각 지수함수 적용', 32, MINT).move_to(heading)), run_time=.6)
        arrows = row(['↓', '↓', '↓'], .9, 30)
        exps = row(['e¹ ≈ 2.72', 'e² ≈ 7.39', 'e³ ≈ 20.09'], -.1, 27)
        self.play(FadeIn(arrows), TransformFromCopy(scores, exps), run_time=1.4)
        self.cue(4)
        total = txt('e¹ + e² + e³ ≈ 30.19', 32, MINT).move_to(DOWN*1.3)
        numerator = txt('eˣⁱ', 36)
        denominator = txt('Σⱼ eˣʲ', 34)
        line = Line(LEFT*1.15, RIGHT*1.15, color=INK)
        fraction = VGroup(numerator.next_to(line, UP, buff=.15), line,
                          denominator.next_to(line, DOWN, buff=.15))
        formula = VGroup(txt('softmax(xᵢ) =', 32), fraction).arrange(RIGHT, buff=.3).move_to(DOWN*3.2)
        self.play(Transform(heading, txt('02  전체 합으로 나누기', 32, MINT).move_to(heading)), FadeIn(total), FadeIn(formula), run_time=1)
        self.cue(5)
        self.play(FadeOut(scores), FadeOut(arrows), FadeOut(exps), FadeOut(total), formula.animate.move_to(UP*1.9), run_time=.7)
        properties = VGroup(txt('모든 출력 > 0', 34, MINT), txt('모든 출력의 합 = 1', 34, MINT)).arrange(DOWN, buff=.5).move_to(DOWN*.4)
        self.play(FadeIn(properties), run_time=.8)
        self.cue(6)
        self.play(FadeOut(formula), FadeOut(properties), Transform(heading, txt('점수 → 분포', 32, MINT).move_to(heading)), run_time=.6)
        scores = row(['1', '2', '3'], 2.3, 42)
        output = row(['0.09', '0.24', '0.67'], .2, 39)
        mapping = txt('↓  Softmax', 27, MUTED).move_to(UP*1.25)
        p = np.exp(np.array([1., 2., 3.]) - 3)
        p /= p.sum()
        segments = VGroup()
        left = -3.6
        for value, c in zip(p, COLORS):
            w = 7.2*value
            segments.add(Rectangle(width=w, height=.7, stroke_width=0, fill_color=c, fill_opacity=.9).move_to([left+w/2, -1.4, 0]))
            left += w
        note = txt('합 = 1  ·  표시값은 소수 둘째 자리 반올림', 22, MUTED).move_to(DOWN*2.6)
        self.play(FadeIn(scores), FadeIn(mapping), FadeIn(output), FadeIn(segments), FadeIn(note), run_time=1.2)
        self.cue(7)
        self.play(Indicate(output[2]), Indicate(segments[2]), run_time=1.2)
        self.play(Indicate(segments[0]), Indicate(segments[1]), run_time=1.2)
        self.cue(8)
        self.play(Transform(heading, txt('서로 비교 가능한 비중', 32, MINT).move_to(heading)), run_time=.7)
        self.cue(9)
        labels = row(['클래스 A', '클래스 B', '클래스 C'], -3.6, 25)
        self.play(FadeIn(labels), Transform(heading, txt('분류 모델의 출력', 32, MINT).move_to(heading)), run_time=.7)
        self.cue(10)
        self.play(Transform(labels, row(['값 A', '값 B', '값 C'], -3.6, 25)), Transform(heading, txt('Attention의 가중치', 32, MINT).move_to(heading)), run_time=.7)
        self.cue(11)
        self.play(*[FadeOut(m) for m in [scores, mapping, output, segments, note, labels]], Transform(heading, txt('분포를 결정하는 것은?', 32, MINT).move_to(heading)), run_time=.8)
        end = VGroup(txt('숫자의 절대적인 크기?', 36, MUTED), txt('그 안의 관계를 살펴봅니다', 33, MINT)).arrange(DOWN, buff=.8).move_to(UP*.4)
        self.play(FadeIn(end), run_time=.8)
        self.cue(12)
        self.play(FadeIn(txt('NEXT  /  Softmax가 비교하는 것', 26, COLORS[1]).move_to(DOWN*3)), run_time=.8)
        self.until(90)
