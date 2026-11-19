"""Independent shots for the 172-second factorial-to-Gamma short."""
import json
import math
import re
import sys
from html import escape
from pathlib import Path

from manim import (
    Axes, Brace, Circle, Create, DashedLine, DecimalNumber, Dot, DOWN,
    FadeOut, Indicate, LaggedStart, Line, MarkupText, Scene, SurroundingRectangle, Text,
    Transform, UP, ValueTracker, VGroup, always_redraw, config, linear,
)

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
import longforms.qcs01_speed.direction as shared
from longforms.qcs01_speed.direction import QCSScene, label

shared.FPS = config.frame_rate = 30
config.background_color = "#0B1020"
DATA = json.loads((HERE / "timing.json").read_text(encoding="utf-8"))
GOLD, BLUE, RED, GREEN, PURPLE = "#F6C85F", "#58C4DD", "#FC766D", "#65D6AC", "#B189F5"
INK, MUTED = "#E8EDF5", "#8B9CB7"
FORMULA_COLORS = {"t²": BLUE, "t³": BLUE, "tⁿ": BLUE, "e⁻ᵗ": RED}


def formula(value, y=0, color=INK, size=43, x=0, colors=None):
    tokens = {**(colors or {}), "₀∞": None}
    pattern = "|".join(re.escape(token) for token in sorted(tokens, key=len, reverse=True))
    parts = re.split(f"({pattern})", value)
    markup = "".join(
        '<sub>0</sub><sup>∞</sup>' if part == "₀∞"
        else f'<span foreground="{tokens[part]}">{escape(part)}</span>' if part in tokens
        else escape(part)
        for part in parts
    )
    mob = MarkupText(markup, font="Cambria Math", font_size=size, color=color)
    if mob.width > 7.6:
        mob.scale_to_fit_width(7.6)
    return mob.move_to([x, y, 0])


def graph_axes(xr, yr, y=0, height=4.1):
    axes = Axes(x_range=xr, y_range=yr, x_length=6.65, y_length=height,
                tips=False, axis_config={"color": MUTED, "stroke_width": 2})
    return axes.move_to([0, y, 0])


def curve(axes, fn, start, end, color):
    return axes.plot(fn, x_range=[start, end, (end-start)/100],
                     color=color, stroke_width=4)


def factorial_panel():
    axes = graph_axes([0, 4.2, 1], [0, 26, 6], .6, 5.2)
    ticks = VGroup(*(formula(str(n), size=22).next_to(axes.c2p(n, 0), DOWN, buff=.15)
                     for n in range(5)))
    points = VGroup(*(Dot(axes.c2p(n, math.factorial(n)), radius=.075, color=GOLD)
                      for n in range(5)))
    axes.add(ticks)
    axes.add(label("입력 x", 3.0, -2.85, 21, MUTED))
    return axes, points


class GammaShot(QCSScene):
    data = DATA
    replace = Scene.replace

    def setup(self):
        super().setup()
        for mob in list(self.mobjects):
            if mob not in (self.caption, self.caption_panel, self.title):
                self.remove(mob)
        self.title.move_to(UP * 6.08)
        self.header = VGroup(
            label("CALCULUS   /   GAMMA FUNCTION", 0, 7.15, 17, MUTED),
            Line([-3.8, 6.65, 0], [3.8, 6.65, 0], color=MUTED,
                 stroke_opacity=.28, stroke_width=1),
        )
        self.add(self.header)

    def clear_body(self):
        fixed = (self.title, self.caption, self.caption_panel, self.header)
        self.play(*(FadeOut(mob) for mob in self.mobjects if mob not in fixed),
                  run_time=.4)

    def footer(self, value, color=GREEN):
        self.show(label(value, 0, -4.2, 27, color, width=7.55), run_time=.4)


class Shot01(GammaShot):
    shot = 0

    def s01(self):
        symbol = formula("n !", 2.35, size=72, colors={"!": GOLD})
        self.show(symbol)
        product = VGroup(*(formula(part, color=GOLD if part != "=" else INK, size=42)
                           for part in ("=", "1", "×", "2", "×", "⋯", "×", "n")))
        product.arrange([1, 0, 0], buff=.19).move_to([0, .6, 0])
        self.play(LaggedStart(*(Create(part) for part in product), lag_ratio=.16), run_time=1.4)
        self.to(3)
        self.clear_body()
        examples = VGroup(
            formula("3! = 1 × 2 × 3 = 6", 2.1, colors={"6": GOLD}),
            formula("4! = 1 × 2 × 3 × 4 = 24", .55, colors={"24": GOLD}),
            formula("5! = 1 × 2 × 3 × 4 × 5 = 120", -1, size=36, colors={"120": GOLD}),
        )
        for line in examples:
            self.show(line)
        self.to(9)
        self.play(*[FadeOut(line) for line in examples], run_time=.4)
        self.show(formula("(2.5)! = ?", 2.1, PURPLE, 63))
        self.show(formula("(0.5)! = ?", .1, PURPLE, 63))
        self.footer("정수 사이에서는 무엇을 곱해야 할까?", PURPLE)
        self.to(14)


class Shot02(GammaShot):
    shot = 1

    def s02(self):
        axes, points = factorial_panel()
        self.show(axes, formula("y = n!", 4.35, GOLD))
        self.to(17)
        self.play(LaggedStart(*(Create(dot) for dot in points), lag_ratio=.35), run_time=1.6)
        guide = VGroup(DashedLine(axes.c2p(2.5, 0), axes.c2p(2.5, 8), color=PURPLE),
                       formula("?", size=32, color=PURPLE).next_to(axes.c2p(2.5, 8), UP))
        self.show(guide)
        self.to(23)
        self.play(FadeOut(guide), run_time=.3)

        def segment(x, exponent):
            n = min(int(x), 3)
            start = math.factorial(n)
            return start + (math.factorial(n+1)-start)*(x-n)**exponent

        line = curve(axes, lambda x: segment(x, 1), 0, 4, BLUE)
        self.play(Create(line), run_time=1.3)
        self.to(26)
        for exponent, color in ((2.8, PURPLE), (.45, GREEN)):
            self.play(Transform(line, curve(axes, lambda x: segment(x, exponent), 0, 4, color)),
                      run_time=1.1)
        self.to(30)
        self.play(line.animate.set_opacity(.24), run_time=.4)
        self.footer("어떤 연결이 팩토리얼에 적합할까?", PURPLE)
        self.to(34)


class Shot03(GammaShot):
    shot = 2

    def s03(self):
        self.show(formula("3! = 1 × 2 × 3 = 6", 3.2, GOLD))
        self.to(38)
        for previous, expanded, factor, y in (("3!", "1 × 2 × 3", 4, 1.35),
                                                ("4!", "1 × 2 × 3 × 4", 5, -1.05)):
            product = formula(expanded, size=36)
            row = VGroup(formula(f"{factor}! =", size=36), product,
                         formula(f"× {factor}", color=GOLD, size=36))
            row.arrange([1, 0, 0], buff=.23).move_to([0, y, 0])
            brace = Brace(product, DOWN, buff=.12, color=GOLD)
            self.show(row, brace, formula(previous, color=GOLD, size=25).next_to(brace, DOWN, buff=.12))
        self.to(44)
        self.clear_body()
        rule = formula("n! = n × (n−1)!", 2.55, GOLD, 52)
        self.show(rule, SurroundingRectangle(rule, color=GOLD, buff=.25))
        self.to(49)
        self.show(formula("F(x) = x F(x−1)   (x ≥ 1)", .2, PURPLE, 42),
                  formula("F(0) = 1", -1.4, PURPLE, 38))
        self.footer("값과 함께 계산 규칙도 유지한다")
        self.to(54)


class Shot04(GammaShot):
    shot = 3

    def s04(self):
        self.show(formula("n! = n × (n−1)!", 3.3, GOLD),
                  label("거듭제곱을 한 번 미분하면", 0, 1.85, 30, BLUE))
        derivative = formula("d/dt  t³", .25, size=50, colors={"³": GOLD})
        self.show(derivative)
        self.to(58)
        for power, factor, result in (("³", 3, "t²"), ("²", 2, "t"), ("", 1, "1")):
            if factor != 3:
                self.play(Transform(derivative, formula(f"d/dt  t{power}", .25, size=50,
                                                        colors={power: GOLD} if power else {})),
                          run_time=.5)
            moving = formula(str(factor), color=GOLD, size=44).move_to(derivative.get_right())
            target = formula(f"{factor} × {result}" if factor > 1 else "1", -1.5, BLUE, 50,
                             colors={str(factor): GOLD})
            self.add(moving)
            self.play(Transform(moving, target), run_time=.8)
            self.wait(.5)
            self.play(FadeOut(moving), run_time=.3)
        self.to(65)
        self.play(Transform(derivative, formula("d/dt  tⁿ  =  n × tⁿ⁻¹", .4, BLUE, 48,
                                                colors={"n ×": GOLD})), run_time=.6)
        self.footer("n을 곱하고, 단계를 하나 낮춘다", GOLD)
        self.to(71)
        self.show(formula("∫₀∞  …  dt", -2.0, GREEN, 51))
        self.to(74)


class Shot05(GammaShot):
    shot = 4

    def s05(self):
        top = graph_axes([0, 4, 1], [0, 16, 4], 2.05, 2.3)
        bottom = graph_axes([0, 4, 1], [0, 1.1, .5], -1.55, 2.3)
        self.show(top, bottom, formula("t²", 3.48, BLUE, 36, -2.65),
                  formula("e⁻ᵗ", -.05, RED, 36, -2.65))
        self.play(Create(curve(top, lambda t: t*t, 0, 4, BLUE)),
                  Create(curve(bottom, lambda t: math.exp(-t), 0, 4, RED)), run_time=1.1)
        self.to(78)
        self.clear_body()
        axes = graph_axes([0, 13, 2], [0, .6, .2], .1)
        product = curve(axes, lambda t: t*t*math.exp(-t), 0, 13, GREEN)
        self.show(axes, formula("t² × e⁻ᵗ", 3.75, size=48, colors=FORMULA_COLORS))
        self.play(Create(product), run_time=1.4)
        self.show(Dot(axes.c2p(2, 4/math.exp(2)), color=GREEN),
                  label("t = 2에서 최대", 1.6, 2.5, 23, MUTED))
        self.to(84)
        upper = ValueTracker(.15)
        area = always_redraw(lambda: axes.get_area(product, x_range=(0, upper.get_value()),
                                                  color=GREEN, opacity=.33))
        value = DecimalNumber(0, num_decimal_places=4, font_size=35, mob_class=Text, color=GREEN)
        value.add_updater(lambda mob: mob.set_value(
            2-math.exp(-upper.get_value())*(upper.get_value()**2+2*upper.get_value()+2)
        ).move_to([2.4, -3.15, 0]))
        self.add(area, label("색칠한 구간의 넓이", -1.0, -3.15, 29, GREEN), value)
        self.play(upper.animate.set_value(6), run_time=2.0, rate_func=linear)
        self.play(upper.animate.set_value(13), run_time=2.0, rate_func=linear)
        area.clear_updaters()
        value.clear_updaters()
        self.footer("상한 T → ∞  ·  전체 넓이 → 2")
        self.to(90)


class Shot06(GammaShot):
    shot = 5

    def s06(self):
        self.show(formula("∫ e⁻ᵗ dt  =  −e⁻ᵗ + C", 3.25, size=47, colors=FORMULA_COLORS))
        self.show(label("미분 · 차수 감소", 0, 1.7, 27, BLUE),
                  formula("tⁿ   →   n tⁿ⁻¹", .75, BLUE, 44, colors={"n ": GOLD}))
        self.show(label("적분 · 형태 유지", 0, -.8, 27, RED),
                  formula("e⁻ᵗ   →   −e⁻ᵗ", -1.8, RED, 44))
        self.to(97)
        self.clear_body()
        self.show(formula("∫ u dv  =  uv − ∫ v du", 4, MUTED, 34))
        integral = formula("Iₙ = ∫₀∞ tⁿe⁻ᵗ dt", 2.6, size=46, colors=FORMULA_COLORS)
        self.show(integral)
        boundary = formula("=  [−tⁿe⁻ᵗ]₀∞", 1.05, size=51, colors=FORMULA_COLORS)
        remainder = formula("+ ∫₀∞ n tⁿ⁻¹e⁻ᵗ dt", -1.2, size=49,
                            colors={"n ": GOLD, "tⁿ⁻¹": BLUE, "e⁻ᵗ": RED})
        self.show(boundary, remainder)
        brace = Brace(boundary, DOWN, buff=.12, color=MUTED)
        self.show(brace, formula("0   (n > 0)", color=MUTED, size=29).next_to(brace, DOWN, buff=.1))
        self.footer("t → 0과 t → ∞에서 경계항이 사라진다", MUTED)
        self.to(105)
        self.clear_body()
        self.show(formula("Iₙ = n × ∫₀∞ tⁿ⁻¹e⁻ᵗ dt", 2.2, size=46,
                          colors={"n ×": GOLD, "tⁿ⁻¹": BLUE, "e⁻ᵗ": RED}))
        self.show(formula("Iₙ = n Iₙ₋₁", .15, GREEN, 61, colors={"n ": GOLD}),
                  formula("n! = n (n−1)!", -2.0, GOLD, 44))
        self.to(109)


class Shot07(GammaShot):
    shot = 6

    def s07(self):
        axes = graph_axes([0, 13, 2], [0, 5.1, 1], .7)
        plot = curve(axes, lambda t: math.exp(-t), 0, 13, GREEN)
        area = axes.get_area(plot, x_range=(0, 13), color=GREEN, opacity=.29)
        tag = formula("e⁻ᵗ", 3.65, RED, 46)
        result = formula("I₀ = ∫₀∞ e⁻ᵗ dt = 1", -2.35, GREEN, 43, colors=FORMULA_COLORS)
        self.show(axes, tag)
        self.play(Create(plot), run_time=1)
        self.show(area, result, label("색칠은 그래프에 보이는 구간", 0, -3.5, 23, MUTED))
        self.to(118)
        labels = {1: ("t e⁻ᵗ", "I₁ = 1 × I₀ = 1"), 2: ("t²e⁻ᵗ", "I₂ = 2 × I₁ = 2"),
                  3: ("t³e⁻ᵗ", "I₃ = 3 × I₂ = 6"), 4: ("t⁴e⁻ᵗ", "I₄ = 4 × I₃ = 24")}
        for n, target in ((1, 122), (2, 124), (3, 127), (4, 128)):
            new_plot = curve(axes, lambda t: t**n*math.exp(-t), 0, 13, GREEN)
            new_tag, new_result = labels[n]
            self.play(Transform(plot, new_plot),
                      Transform(area, axes.get_area(new_plot, x_range=(0, 13), color=GREEN, opacity=.29)),
                      Transform(tag, formula(new_tag, 3.65, size=46, colors=FORMULA_COLORS)),
                      Transform(result, formula(new_result, -2.35, GREEN, 43)), run_time=.7)
            self.to(target)
        self.show(formula("1  →  1  →  2  →  6  →  24", -4.23, GOLD, 38))
        self.to(131)
        self.clear_body()
        self.show(formula("1 × 2 × ⋯ × n", 2.5, GOLD, 50),
                  formula("=", .65, INK, 54), formula("∫₀∞ tⁿe⁻ᵗ dt", -1.3, GREEN, 53,
                                                       colors=FORMULA_COLORS))
        self.footer("곱셈으로 구한 값이 곡선 아래의 넓이가 된다")
        self.to(135)


class Shot08(GammaShot):
    shot = 7

    def s08(self):
        old = formula("∫₀∞ tⁿe⁻ᵗ dt", 1.8, size=60, colors={"ⁿ": GOLD, "e⁻ᵗ": RED})
        self.show(old)
        self.play(Transform(old, formula("∫₀∞ tˣe⁻ᵗ dt", 1.8, size=60,
                                         colors={"ˣ": PURPLE, "e⁻ᵗ": RED})), run_time=1.2)
        self.footer("정수 지수 n에서 실수 지수 x로", PURPLE)
        self.to(139)
        self.clear_body()
        axes = graph_axes([0, 13, 2], [0, .9, .2], .15)
        exponent = ValueTracker(1)
        graph = always_redraw(lambda: curve(axes, lambda t: t**exponent.get_value()*math.exp(-t),
                                            0, 13, GREEN))
        area = always_redraw(lambda: axes.get_area(graph, x_range=(0, 13), color=GREEN, opacity=.3))
        number = DecimalNumber(1, num_decimal_places=2, mob_class=Text, font_size=39, color=PURPLE)
        total = DecimalNumber(1, num_decimal_places=4, mob_class=Text, font_size=37, color=GREEN)
        number.add_updater(lambda mob: mob.set_value(exponent.get_value()).move_to([.65, 3.65, 0]))
        total.add_updater(lambda mob: mob.set_value(math.gamma(exponent.get_value()+1)).move_to([2.35, -3.4, 0]))
        self.add(axes, area, graph, label("지수 x =", -1.05, 3.65, 31, PURPLE),
                 number, label("0부터 ∞까지의 넓이", -1.3, -3.4, 29, GREEN), total,
                 label("색칠은 화면에 보이는 구간", 0, -4.25, 22, MUTED))
        self.play(exponent.animate.set_value(2.5), run_time=5.4, rate_func=linear)
        for mob in (graph, area, number, total):
            mob.clear_updaters()
        self.to(145)
        self.clear_body()
        self.show(formula("Γ(x) = ∫₀∞ tˣ⁻¹e⁻ᵗ dt", 2.15, GREEN, 52,
                          colors={"ˣ⁻¹": PURPLE, "e⁻ᵗ": RED}),
                  formula("x > 0", .75, MUTED, 31),
                  formula("F(x) = Γ(x+1)   (x ≥ 0)", -1.6, PURPLE, 48))
        self.to(148)
        self.clear_body()
        axes, points = factorial_panel()
        self.show(axes, points, formula("F(x) = Γ(x+1)", 4.2, PURPLE, 46))
        self.play(Create(curve(axes, lambda x: math.gamma(x+1), 0, 4, PURPLE)), run_time=1.4)
        self.footer("정수에서는 원래 팩토리얼과 일치", GOLD)
        self.to(154)


class Shot09(GammaShot):
    shot = 8

    def s09(self):
        axes = graph_axes([0, 1.03, .25], [.84, 1.03, .04], 2, 3.3)
        graph = curve(axes, lambda x: math.gamma(x+1), 0, 1, PURPLE)
        dot = Dot(axes.c2p(.5, math.gamma(1.5)), color=GOLD)
        axis_labels = VGroup(*(formula(str(x), size=23).next_to(axes.c2p(x, .84), DOWN, buff=.12)
                              for x in (0, .5, 1)))
        self.show(axes, graph, axis_labels, dot,
                  formula("F(x) = Γ(x+1)", 4.35, PURPLE, 37))
        self.show(formula("(0.5)! = Γ(3/2)", -1, PURPLE, 46))
        answer = formula("0.886226925…", -2.7, GREEN, 47)
        self.show(answer)
        ring = Circle(radius=.73, color=PURPLE, stroke_opacity=.3).move_to([2.55, -2.7, 0])
        self.play(Transform(answer, formula("√π / 2", -2.7, GREEN, 61)), Create(ring), run_time=.9)
        self.play(Indicate(answer, color=GOLD), run_time=.6)
        self.to(161)
        self.clear_body()
        rule = formula("n! = n (n−1)!", 2.7, GOLD, 50)
        self.show(rule)
        self.show(formula("Γ(x+1) = x Γ(x)", .65, PURPLE, 53, colors={"x ": GOLD}),
                  formula("x > 0", -.6, MUTED, 32))
        self.footer("현재 값을 곱하고 한 단계 낮춘다", GOLD)
        self.to(166)
        self.clear_body()
        axes, points = factorial_panel()
        self.show(axes, points, formula("Γ(x+1) = x Γ(x)   (x > 0)", 4.45, PURPLE, 40))
        self.play(Create(curve(axes, lambda x: math.gamma(x+1), 0, 4, PURPLE)), run_time=1.2)
        self.footer("정의역은 확장하고, 계산 규칙은 유지한다")
        self.to(172)
