import os
from pathlib import Path
from textwrap import wrap

import numpy as np
from manim import (
    Arrow, Circle, DashedLine, Dot, Line, MathTex, Polygon, Rectangle,
    RoundedRectangle, Scene, Text, VGroup, VMobject, ValueTracker, config, linear,
)


HERE = Path(__file__).parent
NAVY, GRID, AXIS = "#0D1420", "#172437", "#3B526B"
WHITE, MUTED = "#EBF4FF", "#A6B8CD"
BLUE, ORANGE, GREEN, LILAC = "#49BFFF", "#FFAB59", "#55E3BC", "#C9A6FF"
FONT = "Malgun Gothic"
config.frame_width, config.frame_height = 9, 16
config.pixel_width = int(os.getenv("VIDEO_WIDTH", "1080"))
config.pixel_height = int(os.getenv("VIDEO_HEIGHT", "1920"))
config.frame_rate = 15 if config.pixel_width == 360 else 60
config.background_color = NAVY

SCENES = (0, 17, 34, 47, 62, 91, 110, 122, 137, 152, 168, 174)
X = np.linspace(-3.97, 3.97, 181)
WORLD = np.linspace(-12, 12, len(X))
FFT_X = np.arange(2048) * (96 / 2048) - 48
K = 2 * np.pi * np.fft.rfftfreq(len(FFT_X), 96 / 2048)


def initial(x):
    return 0.5 / np.cosh(x / 2) ** 2


SPECTRUM = np.fft.rfft(initial(FFT_X))


def advection(t):
    return X, initial(WORLD - t)


def dispersive(t):
    evolved = np.fft.irfft(SPECTRUM * np.exp(1j * K**3 * t), n=len(FFT_X))
    return X, np.interp(WORLD, FFT_X, evolved)


def nonlinear(t):
    height = initial(WORLD)
    return (WORLD + 6 * height * t) * (X[-1] / WORLD[-1]), height


def solitary(t):
    return X, initial(WORLD - t)


def texts():
    for row in (HERE / "narration.md").read_text(encoding="utf-8").splitlines():
        fields = row.split("|")
        if len(fields) == 4 and fields[1].strip().isdigit():
            yield int(fields[1]), fields[2].strip()


def caption_lines(sentence):
    return wrap(sentence, width=22, break_long_words=False)


def point(x, y):
    return np.array([x, y, 0.0])


def label(string, x, y, size=30, color=WHITE, bold=False):
    return Text(string, font=FONT, font_size=size, color=color,
                weight="BOLD" if bold else "NORMAL").move_to(point(x, y))


def segment(x1, y1, x2, y2, color=AXIS, width=1.5, dashed=False):
    style = {"dash_length": 0.10} if dashed else {}
    return (DashedLine if dashed else Line)(point(x1, y1), point(x2, y2),
                                           color=color, stroke_width=width, **style)


def arrow(x1, y1, x2, y2, color):
    return Arrow(point(x1, y1), point(x2, y2), buff=0, color=color,
                 stroke_width=2.5, max_tip_length_to_length_ratio=0.22)


def ramp(t, start, end):
    return np.clip((t - start) / (end - start), 0, 1)


class SolitaryWaveShort(Scene):
    def title(self, ko, en, color=WHITE):
        heading = label(ko, -0.18, 5.83, 52, color, True)
        if heading.width > 7.55:
            heading.scale_to_fit_width(7.55)
        return VGroup(label(en, -0.18, 6.64, 21, MUTED), heading)

    def math(self, *terms, y, size=45, colors=()):
        formula = MathTex(*terms, font_size=size, color=WHITE).move_to(point(-0.15, y))
        if formula.width > 7.55:
            formula.scale_to_fit_width(7.55)
        for term, color in zip(formula, colors):
            term.set_color(color)
        return formula

    def timed(self, obj, start, fade=0.35):
        return self.fade(obj, lambda t: ramp(t, start, start + fade))

    def window(self, obj, start, end, fade=0.32):
        return self.fade(obj, lambda t: ramp(t, start, start + fade)
                         * (1 - ramp(t, end - fade, end)))

    def fade(self, obj, opacity):
        styles = [(part, part.get_fill_opacity(), part.get_stroke_opacity())
                  for part in obj.family_members_with_points()]
        previous = None

        def update(_):
            nonlocal previous
            alpha = float(opacity(self.t.get_value()))
            if alpha != previous:
                for part, fill, stroke in styles:
                    part.set_fill(opacity=alpha * fill, family=False)
                    part.set_stroke(opacity=alpha * stroke, family=False)
                previous = alpha

        obj.add_updater(update, call_updater=True)
        return obj

    def trace(self, model, y, scale, color, *, xshift=0, opacity=1, width=4):
        line = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity)

        def update(curve):
            x, u = model(self.t.get_value())
            curve.set_points_as_corners(np.column_stack((x + xshift, y + scale * u, np.zeros_like(x))))

        line.add_updater(update, call_updater=True)
        return line

    def ghost(self, y, scale):
        points = [point(x, y + scale * u) for x, u in zip(X, initial(WORLD))]
        return VGroup(*(Line(points[i], points[i + 3], color=MUTED, stroke_width=1.5,
                             stroke_opacity=0.42) for i in range(0, len(points) - 3, 6)))

    def baseline(self, y):
        return segment(-3.97, y, 3.97, y)

    def caption(self, sentence):
        lines = VGroup(*(label(line, 0, 0, 26, WHITE, True)
                         for line in caption_lines(sentence)))
        lines.arrange(np.array([0, -1, 0]), buff=0.11).move_to(point(-0.45, -5.89))
        assert lines.width <= 7.25 and lines.get_bottom()[1] >= -7.0, sentence
        panel = RoundedRectangle(width=7.55, height=lines.height + 0.38, corner_radius=0.21,
                                 stroke_width=0, fill_color="#080E18", fill_opacity=0.96)
        return VGroup(panel.move_to(lines), lines)

    def construct(self):
        grid = VGroup(*(segment(x, -4.42, x, 7.20, GRID, 1) for x in range(-4, 5)),
                      *(segment(-4.2, y, 4.2, y, GRID, 1) for y in range(-4, 8)))
        self.add(grid)
        cues = list(texts())
        selected = os.getenv("SOLITARY_PREVIEW_SCENES") if config.pixel_width == 360 else None
        scenes = {int(value) for value in selected.split(",")} if selected else set(range(1, 12))
        for index, (start, end) in enumerate(zip(SCENES, SCENES[1:]), 1):
            if index not in scenes:
                continue
            self.t = ValueTracker(start)
            diagram = getattr(self, f"scene_{index:02}")()
            self.add(diagram)
            previous = start
            for stop, sentence in cues:
                if not start < stop <= end:
                    continue
                caption = self.caption(sentence)
                self.bring_to_back(caption)
                self.play(self.t.animate.set_value(stop), run_time=stop - previous,
                          rate_func=linear)
                self.remove(caption)
                previous = stop
            assert previous == end
            self.remove(diagram)

    def scene_01(self):
        actor = VGroup(Circle(radius=0.27, color=WHITE).move_to(point(-3.20, 3.7)),
                       segment(-3.22, 3.42, -3.4, 2.50, WHITE, 5),
                       segment(-3.4, 2.50, -3.83, 1.78, WHITE, 5),
                       segment(-3.4, 2.50, -2.93, 1.78, WHITE, 5),
                       segment(-3.20, 3.23, -2.40, 3.48, WHITE, 5),
                       segment(-3.24, 3.05, -2.38, 3.19, WHITE, 5))
        pulses = VGroup()
        for delay, strength in ((1.8, 0.20), (0.9, 0.38), (0, 0.96)):
            pulse = VGroup(*(Circle(radius=r, color=BLUE, stroke_width=sw,
                                    stroke_opacity=op, fill_color=BLUE, fill_opacity=fill)
                             for r, sw, op, fill in ((0.61, 0, 0, 0.05), (0.50, 0, 0, 0.09),
                                                     (0.40, 2.6, 1, 0.23), (0.21, 0, 0, 0.5))))
            if delay:
                pulse.set_opacity(strength * 0.45)
            pulse.add_updater(lambda m, d=delay: m.move_to(point(
                -1.91 + 5.12 * ramp(self.t.get_value(), 4 + d, 9 + d), 3.34)))
            pulses.add(pulse)
        energy = self.window(VGroup(actor, pulses), 0, 12)
        direction = self.window(arrow(-1.9, 2.25, 3.40, 2.25, BLUE), 4, 11)
        dots = VGroup()
        for i in range(12):
            angle = i * np.pi / 6
            dot = Dot(radius=0.037, color=BLUE)
            dot.add_updater(lambda m, a=angle: m.move_to(point(-1.91, 3.34) +
                            (1.1 - 0.92 * ramp(self.t.get_value(), 0, 4)) *
                            point(np.cos(a + self.t.get_value()), np.sin(a + self.t.get_value()))))
            dots.add(dot)
        waves = VGroup(self.baseline(-1.65))
        for offset, opacity in ((-5, 0.28), (-2.5, 0.48), (0, 1)):
            curve = self.trace(lambda t, d=offset: solitary(-2 + 9 * ramp(t, 9, 17) + d),
                               -1.65, 4.1, BLUE, opacity=opacity)
            curve.add_updater(lambda m, o=opacity: m.set_stroke(opacity=o * ramp(self.t.get_value(), 9, 10)))
            waves.add(curve)
        return VGroup(self.title("장풍이 형태를 유지한다면?", "SHAPE-PRESERVING PROPAGATION"),
                      self.window(dots, 0, 4.1), energy, direction, waves,
                      self.timed(self.math(r"u_t + 6uu_x + u_{xxx}=0", y=-3.65, size=38), 13, 1.2))

    def scene_02(self):
        lake = Circle(radius=1, stroke_width=1.6, color=AXIS, fill_color="#122A42",
                      fill_opacity=0.74).stretch_to_fit_width(7.35).stretch_to_fit_height(4.1)
        lake.move_to(point(0, 2.45))
        stone = Dot(radius=0.14, color=MUTED)
        stone.add_updater(lambda m: m.move_to(point(-2.05 * (1 - ramp(self.t.get_value(), 20, 23)),
                        2.45 + 1.1 * (1 - ramp(self.t.get_value(), 20, 23)) +
                        1.65 * np.sin(np.pi * ramp(self.t.get_value(), 20, 23)))))
        rings = VGroup()
        for i in range(5):
            ring = Circle(radius=1, color=BLUE, stroke_width=2.2)

            def expand(m, delay=i * 0.85):
                age = self.t.get_value() - 23 - delay
                radius = 0.12 + 0.34 * max(0, age)
                m.stretch_to_fit_width(2 * radius).stretch_to_fit_height(1.12 * radius)
                m.move_to(point(0, 2.45))
                m.set_stroke(opacity=float(ramp(age, 0, 0.4) * (1 - ramp(radius, 2.75, 3.65))))

            rings.add(ring.add_updater(expand, call_updater=True))

        def section(t):
            radius = 0.65 + 0.25 * (t - 28)
            d = np.abs(X) - radius
            return X, np.exp(-(d / 0.85)**2) * np.cos(9 * d)

        surface = VGroup(segment(-3.53, 2.45, 3.53, 2.45, WHITE, dashed=True),
                         arrow(0, 0.95, 0, 0.20, MUTED),
                         label("수면의 단면", 0, -0.56, 25, MUTED),
                         self.baseline(-2.20), self.trace(section, -2.20, 0.68, BLUE))
        return VGroup(self.title("호수에 돌을 던지면", "WATER SURFACE"), lake,
                      self.window(stone, 17, 23.2), rings, self.timed(surface, 28),
                      self.timed(label("←  바깥으로 전파  →", 0, -3.65, 26, BLUE), 31))

    def components(self, nondispersive):
        origin = 99 if nondispersive else 36
        colors = (GREEN, BLUE, LILAC)
        rows = (3.50, 1.52, -0.46)
        speeds = (0.30, 0.30, 0.30) if nondispersive else (0.13, 0.26, 0.40)

        def center(index, t):
            return -1.42 + speeds[index] * max(0, t - origin)

        def component(index, t):
            d = X - center(index, t)
            return np.cos((7.6, 4.9, 2.9)[index] * d) * np.exp(-(d / 1.25)**2)

        stack = VGroup()
        for i, (name, y, color) in enumerate(zip(("짧은 파장", "중간 파장", "긴 파장"), rows, colors)):
            stack.add(label(name, -2.92, y + 0.88, 24, color), self.baseline(y),
                      self.trace(lambda t, j=i: (X, component(j, t)), y, 0.42, color))
            dot = Dot(radius=0.058, color=color)
            dot.add_updater(lambda m, j=i, row=y: m.move_to(point(center(j, self.t.get_value()), row + 0.42)))
            velocity = arrow(0, 0, 0.32 + 2 * speeds[i], 0, color)
            velocity.add_updater(lambda m, j=i, row=y: m.move_to(point(
                center(j, self.t.get_value()) + m.width / 2, row + 0.73)))
            stack.add(self.timed(dot, origin), self.timed(velocity, origin))
        y = -2.88
        stack.add(label("합성 파형", -2.92, y + 0.87, 24, MUTED), self.baseline(y),
                  self.trace(lambda t: (X, sum(component(i, t) for i in range(3))), y, 0.24,
                             GREEN if nondispersive else WHITE))
        if not nondispersive:
            reference = self.trace(lambda t: (X, sum(component(i, origin) for i in range(3))),
                                   y, 0.24, MUTED, opacity=0.35, width=2)
            stack.add(reference)
        return stack

    def scene_03(self):
        return VGroup(self.window(self.title("파장에 따른 속도 차이", "WAVE COMPONENTS"), 34, 45.4),
                      self.timed(self.title("분산", "DISPERSION", BLUE), 45),
                      self.components(False),
                      self.timed(self.math(r"\lambda_1\ne\lambda_2,\quad v_p(\lambda_1)\ne v_p(\lambda_2)",
                                           y=-4.15, size=34), 36))

    def char_diagram(self, y, scale, time_model, cue, seeds):
        group = VGroup()
        for seed in seeds:
            height = float(initial(seed))
            mark = VGroup(Dot(radius=0.060, color="#FFE1B9"),
                          arrow(0.08, 0, 0.13 + 2.0 * height, 0, ORANGE))
            mark.add_updater(lambda m, xi=seed, u=height: m.shift(
                point((xi + 6 * u * time_model(self.t.get_value())) * (X[-1] / WORLD[-1]),
                      y + scale * u) - m[0].get_center()))
            group.add(mark)
        return self.timed(group, cue)

    def scene_04(self):
        evolve = lambda t: 0.71 * ramp(t, 50, 62)
        upper = VGroup(self.baseline(0.48), self.ghost(0.48, 5.05),
                       self.trace(lambda t: nonlinear(evolve(t)), 0.48, 5.05, ORANGE),
                       self.char_diagram(0.48, 5.05, evolve, 50, [-2.7, -1.25, 0, 1.25, 2.7]))
        amplitude = VGroup(segment(-0.15, 0.48, -0.15, 3.0, ORANGE, dashed=True),
                           label("A", -0.50, 1.75, 25, ORANGE))
        return VGroup(self.title("높이에 따라 달라지는 속도", "AMPLITUDE-DEPENDENT SPEED"),
                      upper, self.window(amplitude, 47, 50.3),
                      self.window(label("비선형성 · Nonlinearity", 0, -1.05, 32, ORANGE, True), 53, 58.4),
                      self.timed(VGroup(label("분산 · Dispersion", -2.18, -2.25, 26, BLUE),
                          self.baseline(-3.50), self.trace(lambda t: dispersive(4 * ramp(t, 58, 62)),
                                                          -3.50, 2.05, BLUE)), 58))

    def measure(self, y, scale, center_model, cue):
        half = 2 * np.arccosh(np.sqrt(2)) * (X[-1] / WORLD[-1])
        top = scale / 2
        ruler = VGroup(segment(-half, top / 2, half, top / 2, WHITE, 2),
                       segment(-half, top / 2 - 0.09, -half, top / 2 + 0.09, WHITE, 2),
                       segment(half, top / 2 - 0.09, half, top / 2 + 0.09, WHITE, 2),
                       segment(1.13, 0, 1.13, top, WHITE, dashed=True),
                       segment(0, top, 1.23, top, WHITE, dashed=True),
                       label("W", 0, top / 2 + 0.24, 23),
                       label("A", 1.40, top / 2, 23))
        origin = ruler.get_center().copy()
        ruler.add_updater(lambda m: m.move_to(origin + point(center_model(self.t.get_value()), y)))
        return self.timed(ruler, cue)

    def scene_05(self):
        y, scale = -0.90, 4.0
        ship_x = lambda t: -2.84 + 0.82 * ramp(t, 67, 71)
        ship = VGroup(Polygon(point(-1.02, 0.32), point(1.03, 0.32), point(0.59, -0.25),
                              point(-0.62, -0.25), color=WHITE, stroke_width=2,
                              fill_color="#8095AA", fill_opacity=1),
                      Rectangle(width=0.72, height=0.46, color=WHITE, stroke_width=2,
                                fill_color="#34465B", fill_opacity=1).move_to(point(-0.08, 0.55)),
                      segment(-0.17, 0.78, -0.17, 1.14, MUTED, 3))
        ship.add_updater(lambda m: m.move_to(point(ship_x(self.t.get_value()), y + 0.45)))
        channel = Rectangle(width=7.94, height=0.58, stroke_width=0, fill_color="#12304A",
                            fill_opacity=1).move_to(point(0, y - 0.29))
        water = VGroup(channel, segment(-3.97, y - 0.58, 3.97, y - 0.58, AXIS, 2), ship)
        center = lambda t: (-1.5 + 0.27 * (t - 62) if t < 67 else
                            -0.9 + 0.20 * (t - 67) if t < 71 else
                            -0.1 + 1.58 * ramp(t, 71, 85) + 0.41 * ramp(t, 85, 91))

        def pulse(t):
            return X, initial(WORLD - center(t) * WORLD[-1] / X[-1])

        wave = self.trace(pulse, y, scale, BLUE)
        wave.add_updater(lambda m: m.set_color(BLUE if self.t.get_value() < 88 else GREEN))
        trail = self.trace(lambda t: pulse(max(62, t - 5)), y, scale, GREEN, width=2)
        trail.add_updater(lambda m: m.set_stroke(opacity=0.35 * ramp(self.t.get_value(), 78, 81)))
        return VGroup(self.window(self.title("좁은 수로의 물결", "A WAVE IN A CHANNEL"), 62, 88.3),
                      self.timed(self.title("고립파", "SOLITARY WAVE", GREEN), 88),
                      self.baseline(y), self.window(water, 67, 85.3), trail, wave,
                      self.window(label("■  배가 멈춘다", -2.15, 2.60, 28, ORANGE), 71, 76),
                      self.measure(y, scale, center, 82),
                      self.timed(label("국소화된 파형", 0, -2.55, 29, GREEN), 85),
                      self.timed(self.math(r"u(x,t)=f(x-ct)", y=-3.78), 88))

    def scene_06(self):
        opening = VGroup(self.title("어떤 조건에서 형태가 유지될까?", "SHAPE PRESERVATION"),
                         self.baseline(0), self.trace(lambda t: solitary(4.5 + 0.18 * (t - 91)),
                                                      0, 4.2, GREEN))
        components = VGroup(self.title("비분산 선형파", "LINEAR NONDISPERSIVE WAVE"),
                            self.components(True))
        model = VGroup(self.title("비분산 선형파", "LINEAR NONDISPERSIVE WAVE"),
                       self.math(r"u_t+cu_x=0", y=3.67),
                       self.baseline(-0.68), self.ghost(-0.68, 4.0),
                       self.trace(lambda t: advection(6 * ramp(t, 104, 110)), -0.68, 4.0, GREEN),
                       arrow(-0.9, 2.2, 1.70, 2.2, GREEN),
                       self.math(r"u(x,t)=f(x-ct)", y=-2.88))
        return VGroup(self.window(opening, 90.5, 95.3),
                      self.window(components, 95, 104.3), self.timed(model, 104))

    def scene_07(self):
        y = -0.78
        return VGroup(self.title("분산이 있다면?", "LINEAR DISPERSION", BLUE),
                      self.window(label("분산 OFF", 0, 3.35, 32, MUTED), 109.6, 115.25),
                      self.timed(self.math(r"u_t+u_{xxx}=0", y=3.35), 115),
                      self.baseline(y), self.timed(self.ghost(y, 4.9), 115),
                      self.trace(lambda t: dispersive(6.0 * ramp(t, 115, 122)), y, 4.9, BLUE),
                      self.timed(VGroup(arrow(-0.7, -2.08, -2.7, -2.08, BLUE),
                                       label("진동 꼬리", -2.53, -2.60, 24, BLUE),
                                       label("파형의 퍼짐과 변형", 0, -3.68, 32, BLUE, True)), 118))

    def scene_08(self):
        y, scale = -0.68, 5.0
        evolve = lambda t: 0.82 * ramp(t, 125, 137)
        tangent = DashedLine(point(0, 0), point(1, 0), color=ORANGE, stroke_width=2)

        def place_tangent(m):
            xi = 2 * np.arctanh(1 / np.sqrt(3))
            height = initial(xi)
            der = -height * np.tanh(xi / 2)
            t = evolve(self.t.get_value())
            location = point((xi + 6 * height * t) * X[-1] / WORLD[-1], y + scale * height)
            direction = point((1 + 6 * der * t) * X[-1] / WORLD[-1], scale * der)
            direction *= 0.75 / np.linalg.norm(direction)
            m.put_start_and_end_on(location - direction, location + direction)

        tangent.add_updater(place_tangent)
        return VGroup(self.window(self.title("높은 부분이 더 빠르게", "NONLINEAR PROPAGATION"), 121.6, 134.3),
                      self.timed(self.title("파동의 급경사화", "WAVE STEEPENING", ORANGE), 134),
                      self.math(r"u_t+6uu_x=0", y=3.98),
                      self.baseline(y), self.ghost(y, scale),
                      self.trace(lambda t: nonlinear(evolve(t)), y, scale, ORANGE),
                      self.char_diagram(y, scale, evolve, 125, [-2.7, -1.3, 0, 1.3, 2.7]),
                      self.timed(tangent, 131),
                      self.timed(label("앞쪽 경사가 가팔라진다", 0, -3.05, 30, ORANGE), 131))

    def scene_09(self):
        group = VGroup(self.title("분산과 비선형성의 균형", "SAME INITIAL PROFILE", GREEN),
                       self.math(r"u_0(x)=\tfrac12\operatorname{sech}^2(x/2)", y=4.78, size=31))
        for name, y, color, model, reveal in (
            ("비선형 효과", 2.28, ORANGE, nonlinear, 137),
            ("분산 효과", -0.54, BLUE, dispersive, 138),
            ("두 효과가 함께 작용할 때", -3.32, GREEN, solitary, 139),
        ):
            row = VGroup(label(name, -2.32 if len(name) < 9 else -1.53, y + 1.35, 25, color, True),
                         self.baseline(y), self.ghost(y, 2.05),
                         self.trace(lambda t, fn=model: fn(0.83 * ramp(t, 141, 152)), y, 2.05, color))
            group.add(self.timed(row, reveal))
        group.add(self.timed(arrow(-0.75, -3.99, 0.80, -3.99, GREEN), 148))
        return group

    def scene_10(self):
        equation = self.math(r"u_t", "+", r"6uu_x", "+", r"u_{xxx}", "=0", y=3.92,
                             size=59, colors=(WHITE, MUTED, ORANGE, MUTED, BLUE, WHITE))
        diagram = VGroup(self.timed(self.title("KdV 방정식", "KORTEWEG–DE VRIES EQUATION"), 154),
                         self.baseline(-2.60),
                         self.trace(lambda t: solitary(-6.2 + 12.4 * ramp(t, 152, 168)),
                                    -2.60, 3.9, GREEN))
        for i, term in enumerate(equation):
            self.timed(term, 155 + 0.52 * i)
        diagram.add(equation)
        for cue, end, index, name, color, model in (
            (160, 162, 0, "시간 변화", WHITE, advection),
            (162, 165, 2, "비선형성", ORANGE, nonlinear),
            (165, 168, 4, "분산", BLUE, dispersive),
        ):
            term = equation[index]
            underline = segment(term.get_left()[0], 3.12, term.get_right()[0], 3.12, color, 4)
            mini = self.trace(lambda t, fn=model, a=cue, b=end: fn(0.81 * ramp(t, a, b)),
                              0.38, 2.2, color)
            diagram.add(self.window(VGroup(underline, label(name, 0, 2.49, 27, color),
                                            self.baseline(0.38), mini), cue, end))
        return diagram

    def scene_11(self):
        y, scale = -1.47, 4.85
        shift = lambda t: -5.7 + 10.2 * ramp(t, 168, 174)
        center = lambda t: shift(t) * X[-1] / WORLD[-1]
        diagram = VGroup(self.title("형태를 지키는 고립파 해", "SOLITARY WAVE SOLUTION", GREEN),
                         self.math(r"u_t+6uu_x+u_{xxx}=0", y=4.25, size=35),
                         self.timed(self.math(r"u(x,t)=\frac{c}{2}\operatorname{sech}^2"
                                              r"\!\left(\frac{\sqrt{c}}{2}(x-ct)\right)",
                                              y=2.92, size=43), 168),
                         label("c > 0", 0, 1.99, 23, MUTED), self.baseline(y))
        for delay, opacity in ((2.7, 0.24), (1.7, 0.36), (0.8, 0.51)):
            trail = self.trace(lambda t, d=delay: solitary(shift(t - d)), y, scale, GREEN, width=2.7)
            trail.add_updater(lambda m, o=opacity: m.set_stroke(opacity=o * ramp(self.t.get_value(), 172, 172.75)))
            diagram.add(trail)
        diagram.add(self.trace(lambda t: solitary(shift(t)), y, scale, GREEN, width=5.2),
                    self.measure(y, scale, center, 170),
                    self.timed(label("일정한 높이 · 폭 · 속도", 0, -3.45, 34, GREEN, True), 170),
                    self.timed(arrow(-2.85, -2.36, 2.83, -2.36, GREEN), 172))
        return diagram
