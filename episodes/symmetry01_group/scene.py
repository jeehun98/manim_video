"""Portrait animation for the seven independently rendered claims."""
import json
import sys
from pathlib import Path

from manim import *

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from longforms.qcs01_speed.direction import QCSScene, label
from quantum_series.shared.theme import FONT

DATA = json.loads((HERE / 'timing.json').read_text(encoding='utf-8'))
BG, INK, MUTED = '#0C1425', '#EDF3FC', '#8B9CB7'
MOVE, KEEP, RULE = '#61AEFF', '#52E2A8', '#FFD275'
config.background_color = BG


def caption(value, y, color=INK, size=37, x=0, width=7.6):
    return label(value, x=x, y=y, color=color, size=size, width=width)


def square(y=0.6, side=3.6):
    center = UP * y
    shape = Square(side_length=side, color=MOVE, fill_opacity=.22, stroke_width=5).move_to(center)
    marker = Dot(center + (UP + RIGHT) * side / 2, radius=.13, color=RULE).set_z_index(4)
    outline = DashedVMobject(shape.copy().set_fill(opacity=0).set_stroke(MUTED, width=3), num_dashes=32)
    return center, VGroup(shape, marker), outline


def row(title, formula, y, color=RULE):
    box = RoundedRectangle(width=7.5, height=1.28, corner_radius=.18,
                           color=color, stroke_opacity=.45, fill_color=color, fill_opacity=.07)
    box.shift(UP * y)
    return VGroup(box, caption(title, y, color, 29, -2.24, 2.65),
                  caption(formula, y, INK, 32, 1.31, 4.0))


def number_line(a, b, origin=-1.3):
    axis = NumberLine(x_range=[1, 13, 1], length=7.1, color=MUTED).shift(UP * origin)
    dots = VGroup(*[Dot(axis.n2p(n), color=MOVE, radius=.13) for n in (a, b)])
    nums = VGroup(*[caption(str(n), origin - .61, x=axis.n2p(n)[0]) for n in (a, b)])
    left, right = [axis.n2p(n) + UP * .85 for n in (a, b)]
    bracket = DoubleArrow(left, right, color=KEEP, buff=0, stroke_width=4)
    distance = caption('차이 4', origin + 1.45, KEEP, x=(left[0]+right[0])/2)
    return axis, VGroup(dots, nums, bracket, distance)


class SymmetryScene(QCSScene):
    data = DATA

    def setup(self):
        super().setup()
        self.remove(self.mobjects[0], self.caption_panel, self.caption)
        self.title.move_to(UP * 5.2)
        self.add(caption('대칭의 진짜 의미', 6.95, MUTED, 22))

    def update_caption(self, mob, dt=0):
        pass


class Shot01(SymmetryScene):
    shot = 0

    def s01(self):
        wing = Polygon([0,.5,0], [-.95,1.95,0], [-2.6,2.25,0], [-2.18,.55,0],
                       [-.9,.05,0], [-1.85,-.8,0], [-1.38,-1.75,0], [-.48,-1.45,0],
                       [0,-.43,0], color=MOVE, fill_opacity=.29, stroke_width=4)
        mirror = wing.copy().flip(UP, about_point=ORIGIN).set_color(KEEP)
        axis = DashedLine(DOWN*2.1, UP*2.8, color=MUTED)
        self.play(Create(wing), Create(axis), run_time=1.1)
        self.play(TransformFromCopy(wing, mirror), run_time=1.1)
        reflection = caption('좌우 반사', -3, KEEP)
        self.show(reflection)
        self.to(4)
        self.play(Indicate(axis, color=KEEP), run_time=.8)
        self.to(7)
        center, rotating, outline = square()
        self.play(FadeOut(VGroup(wing, mirror, axis, reflection)), FadeIn(rotating), Create(outline))
        self.to(10)
        angle = caption('30°', -2.62, MOVE, 55)
        self.play(Rotate(rotating, 30*DEGREES, about_point=center), FadeIn(angle), run_time=1.25)
        match = caption('원래 윤곽과 어긋남', -3.62, MUTED)
        self.show(match)
        self.to(14)
        self.play(Rotate(rotating, 60*DEGREES, about_point=center),
                  Transform(angle, caption('90°', -2.62, KEEP, 55)),
                  Transform(match, caption('원래 윤곽과 일치', -3.62, KEEP)), run_time=1.2)
        self.play(rotating[0].animate.set_color(KEEP), run_time=.45)
        self.to(18)
        for degrees in (180,270):
            self.play(Rotate(rotating, PI/2, about_point=center),
                      Transform(angle, caption(f'{degrees}°', -2.62, KEEP, 55)), run_time=.85)
        self.to(21)
        self.play(Transform(match, caption('회전해도 윤곽이 보존된다', -3.62, KEEP)), run_time=.55)
        self.play(Indicate(outline, color=KEEP), run_time=.8)


class Shot02(SymmetryScene):
    shot = 1

    def s02(self):
        axis, points = number_line(3,7)
        self.show(axis, caption('수직선 위의 두 점', 2.8, MUTED))
        self.to(32)
        difference = caption('7 − 3 = 4', 1.48, KEEP, 52)
        self.show(points, difference)
        self.to(34)
        _, shifted = number_line(8,12)
        badge = caption('두 점 모두 +5', -3.12, MOVE, 34)
        self.play(Transform(points, shifted), FadeIn(badge),
                  Transform(difference, caption('12 − 8 = 4', 1.48, KEEP, 52)), run_time=1.6)
        self.to(38)
        self.play(Indicate(points[2], color=KEEP), run_time=1)
        self.to(41)
        symbolic = VGroup(*[
            caption(value, -1.91, size=26, x=number.get_center()[0])
            for value, number in zip(('3 + n', '7 + n'), points[1])
        ])
        self.play(Transform(points[1], symbolic),
                  Transform(badge, caption('두 점 모두 +n', -3.12, MOVE, 34)),
                  Transform(difference, caption('(7 + n) − (3 + n) = 4', 1.48, KEEP, 41)))
        self.to(45)
        self.show(caption('보존되는 관계 · 두 수의 차이', -4.16, KEEP, 30))


def track(y, city):
    start, end = LEFT*2.25+UP*y, RIGHT*2.25+UP*(y-1.1)
    ramp = Line(start, end, color=MUTED, stroke_width=4)
    ball = Dot(start+UP*.22, radius=.18, color=MOVE)
    return VGroup(ramp, caption(city, y+.75, INK, 36)), ball, end+UP*.22


class Shot03(SymmetryScene):
    shot = 2

    def s03(self):
        seoul, blue, end1 = track(2.48,'서울')
        busan, other, end2 = track(-.55,'부산')
        self.show(seoul, blue)
        self.to(51)
        self.play(FadeIn(busan), FadeIn(other), run_time=.85)
        self.play(blue.animate.move_to(end1), other.animate.move_to(end2),
                  rate_func=lambda t: t*t, run_time=1.75)
        condition = caption('같은 장치 · 같은 시작 조건', -3.16, MUTED, 33)
        self.show(condition)
        self.to(57)
        self.show(caption('보존되는 것 · 물리 법칙', -4.2, KEEP, 34))
        self.to(62)
        self.play(FadeOut(VGroup(seoul,busan,blue,other,condition)), run_time=.6)
        self.show(row('회전','정사각형의 윤곽',2.3,KEEP),
                  row('평행이동','두 수의 차이',.68,KEEP),
                  row('실험 위치 이동','물리 법칙',-.94,KEEP))
        self.title.become(caption('변환 후에도 무엇이 남을까?', 5.2, INK, 39))


class Shot04(SymmetryScene):
    shot = 3

    def s04(self):
        center, rotating, outline = square()
        self.show(outline, rotating)
        self.to(72)
        result = caption('90°', -2.76, MOVE, 56)
        self.play(Rotate(rotating, PI/2, about_point=center), FadeIn(result))
        self.play(Rotate(rotating, PI/2, about_point=center),
                  Transform(result, caption('90° + 90° = 180°', -2.76, RULE, 49)))
        self.to(77)
        self.play(Rotate(rotating, -PI, about_point=center), FadeOut(result), run_time=.55)
        result = caption('90° × 4 = 360°', -2.76, RULE, 48)
        for _ in range(4):
            self.play(Rotate(rotating, PI/2, about_point=center), run_time=.41)
        reset = caption('처음 상태', -3.78, KEEP, 32)
        self.show(result, reset)
        self.to(81)
        self.play(Rotate(rotating, PI/2, about_point=center),
                  Transform(result, caption('+90°', -2.76, MOVE, 52)), FadeOut(reset), run_time=.86)
        self.play(Rotate(rotating, -PI/2, about_point=center),
                  Transform(result, caption('+90° − 90° = 0°', -2.76, RULE, 46)), run_time=.88)


class Shot05(SymmetryScene):
    shot = 4

    def s05(self):
        value = caption('x', 1.9, MOVE, 67)
        self.show(value)
        self.to(89)
        self.play(Transform(value, caption('x + 3', 1.9, MOVE, 60)), run_time=.7)
        self.play(Transform(value, caption('x + 3 + 5', 1.9, MOVE, 58)), run_time=.7)
        self.show(row('합성','x + 8',.2))
        self.to(93)
        self.show(row('항등','x + 0 = x',-1.45))
        self.show(row('역연산','x + 3 − 3 = x',-3.1))
        self.to(99)
        self.play(Transform(value, caption('회전과 덧셈', 1.9, KEEP, 46)), run_time=.55)


class Shot06(SymmetryScene):
    shot = 5

    def s06(self):
        compare = VGroup(
            row('합성','90° + 90°   /   +3, +5',2.7),
            row('그대로','0°   /   +0',1.05),
            row('되돌리기','−90°   /   −3',-.6),
        )
        for item in compare:
            self.show(item)
        self.to(110)
        name = caption('군  Group', -2.78, RULE, 59)
        self.show(name)
        self.to(116)
        self.play(FadeOut(compare), name.animate.move_to(UP*3.5).scale(.8), run_time=.55)
        cards = [('닫힘','a ∗ b ∈ G'),('결합법칙','(a ∗ b) ∗ c = a ∗ (b ∗ c)'),
                 ('항등원','e ∗ a = a ∗ e = a'),('역원','a ∗ a⁻¹ = a⁻¹ ∗ a = e')]
        for at, y, (title, formula) in zip((117,120,123,125), (1.92,.23,-1.46,-3.15), cards):
            self.to(at)
            self.show(row(title,formula,y),run_time=.55)


class Shot07(SymmetryScene):
    shot = 6

    def s07(self):
        examples = VGroup(row('정수','덧셈 · 항등원 0',2.45,MOVE),
                         row('0 이외의 실수','곱셈 · 항등원 1',.6,MOVE),
                         row('도형의 대칭','변환의 합성',-1.25,MOVE))
        for example in examples:
            self.show(example, run_time=.66)
        self.to(133)
        shared = caption('모두 같은 군 공리를 만족한다', -3.21, RULE, 34)
        self.show(shared)
        self.to(140)
        self.play(*[Indicate(example[0], color=RULE, scale_factor=1) for example in examples], run_time=.8)
        self.play(Transform(shared, caption('변환은 달라도, 지켜지는 규칙이 있다', -3.21, KEEP, 36)))

