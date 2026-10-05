"""Neural Network Mathematics Part 2, episode 10: Catapult Mechanism."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.nnmath2p09_edge_of_stability.scene import (
    NeuralMathPart2EdgeOfStability, card, label,
)
from episodes.prune_series.visuals import ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, ZERO


class NeuralMathPart2Catapult(NeuralMathPart2EdgeOfStability):
    DURATION = 175

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.caption = VGroup()
        self.caption_box = VGroup()
        title = VGroup(label("Catapult Mechanism", 24, ACCENT),
                       label("Loss가 폭발했는데 왜 다시 학습될까?", 22))
        title.arrange(DOWN, buff=.1).move_to(UP * 6.55)
        self.chrome = VGroup(
            label("NEURAL NETWORK MATHEMATICS  /  PART 2 · 10", 16, MUTED).move_to(UP * 7.55),
            title,
            Line([-3.8, 5.75, 0], [3.8, 5.75, 0], color=MUTED, stroke_opacity=.35),
        )
        self.progress = Line([-3.8, -7.36, 0], [-3.79, -7.36, 0], color=ACCENT, stroke_width=4)
        self.add(self.chrome, self.progress)

        self.copy("안정성의 경계를 조금 더 넘어가면?", "BEYOND THE EDGE",
                  "Edge of Stability에서는 경계 부근에서 학습이 이어졌습니다.\n이번에는 Learning Rate를 경계 너머로 더 크게 만들어봅니다.")
        strip = self.boundary_pointer(False)
        self.show(strip)
        moved = self.boundary_pointer(True)
        self.play(ReplacementTransform(strip, moved), run_time=.9)
        self.stage = moved
        self.to(9.5)

        self.copy("고정 Quadratic이라면 그대로 발산합니다", "LARGE LR → DIVERGENCE",
                  "최소점을 반복해서 넘어가고 진동 폭이 커집니다.\n고정된 지형에서는 다시 안정될 이유가 없습니다.")
        panel = self.divergence_panel()
        self.show(panel)
        self.play(Create(panel[2]), run_time=.9)
        self.to(16)

        self.copy("실제 신경망도 처음에는 실패처럼 보입니다", "LOSS  ↑↑↑",
                  "Loss가 내려가기는커녕 몇 step 만에 급격하게 치솟습니다.\n보통이라면 여기서 training이 실패했다고 판단할 만합니다.")
        spike_only = self.catapult_plot(.49, show_kernel=False)
        failed = card("DIVERGED?", PRUNE, 3.4, .72, 25, .12).move_to([0, -2.35, 0])
        self.show(VGroup(spike_only, failed))
        self.to(25.5)

        self.copy("그런데 Loss가 다시 내려올 수 있습니다", "SPIKE → RECOVERY",
                  "특정한 큰 Learning Rate 영역에서는 치솟은 Loss가 다시 빠르게 내려와\n낮은 Loss의 학습 상태로 돌아올 수 있습니다.")
        half = self.catapult_plot(.49, False)
        full = self.catapult_plot(1.0, False)
        self.show(half)
        self.play(ReplacementTransform(half, full), run_time=1.2)
        self.stage = full
        self.to(34)

        self.copy("다른 학습 상태로 크게 튕겨 이동합니다", "CATAPULT MECHANISM",
                  "새총으로 한 번 크게 튕겨져 다른 상태에 안착하는 것처럼 보입니다.\n그래서 Catapult Mechanism이라고 부릅니다.")
        arc = self.catapult_arc()
        self.show(arc)
        self.play(MoveAlongPath(arc[-1], arc[-2]), run_time=1.2, rate_func=smooth)
        self.to(41.5)

        self.copy("신경망은 움직이며 학습 구조도 바꿉니다", "FIXED QUADRATIC  vs  NEURAL NETWORK",
                  "Quadratic에서는 점이 움직여도 지형이 그대로입니다.\n신경망에서는 큰 parameter 변화가 다음 training dynamics도 바꿀 수 있습니다.")
        compare = self.fixed_vs_network()
        self.show(compare)
        self.play(Indicate(compare[1], color=SPARSE), run_time=.8)
        self.to(51)

        self.copy("처음에는 현재 Learning Rate가 너무 큽니다", "CURRENT LR  >  CRITICAL LR",
                  "초기 NTK의 최대 eigenvalue가 크면 critical Learning Rate는 작습니다.\n현재 η가 초기 네트워크의 안정 범위를 넘어설 수 있습니다.")
        bars = self.lr_critical_bars(False)
        self.show(bars)
        self.to(62)

        self.copy("Spike는 상위 eigenmode에 집중될 수 있습니다", "TOP NTK EIGENSPACE",
                  "모든 방향의 오차가 똑같이 폭발하는 것은 아닙니다.\n관찰 연구에서는 top eigenspace의 Loss가 튀고 나머지는 감소했습니다.")
        modes = self.mode_spike_panel()
        self.show(modes)
        self.play(Indicate(modes[0], color=PRUNE), run_time=.85)
        self.to(73.5)

        self.copy("큰 업데이트가 NTK도 바꿉니다", "LOSS ↑  ·  λₘₐₓ(K) ↓",
                  "Catapult 구간에서 NTK의 최대 eigenvalue는 크게 변할 수 있습니다.\n대표적인 관찰에서는 spike를 거치며 그 값이 감소합니다.")
        coupled = self.coupled_plot()
        self.show(coupled)
        self.play(Create(coupled[0][2]), Create(coupled[1][2]), run_time=1.1)
        self.to(84)

        self.copy("Learning Rate를 줄인 것이 아닙니다", "SAME η · DIFFERENT NETWORK",
                  "네트워크 자체가 변하면서 같은 Learning Rate를\n견딜 수 있는 상태로 이동한 것입니다.")
        before = self.lr_critical_bars(False)
        after = self.lr_critical_bars(True)
        self.show(before)
        self.play(ReplacementTransform(before, after), run_time=1.15)
        self.stage = after
        self.to(92.5)

        self.copy("λₘₐₓ가 작아지면 critical LR은 올라갑니다", "THE KEY REVERSAL",
                  "처음에는 너무 컸던 같은 η가, 변화한 네트워크에서는\n다시 감당 가능한 Learning Rate가 될 수 있습니다.")
        relation = VGroup(card("λₘₐₓ(K)  ↓", SPARSE, 4.5, .9, 31, .14), label("↓", 31, MUTED),
                          card("η_crit  ↑", GOOD, 4.5, .9, 31, .14), label("↓", 31, MUTED),
                          card("same η becomes tolerable", ACCENT, 6.2, .9, 25, .15))
        relation.arrange(DOWN, buff=.24).move_to([0, .2, 0])
        self.show(relation)
        self.to(102.5)

        self.copy("Spike의 정점에서 학습 조건이 바뀌었습니다", "DYNAMICS CHANGED",
                  "Loss peak는 단순히 발산 도중의 한 순간만이 아닐 수 있습니다.\n그 사이 network가 변했고 이후의 학습 조건도 달라졌습니다.")
        turning = self.turning_point_plot()
        self.show(turning)
        self.play(Indicate(turning[-1], color=ACCENT), run_time=.8)
        self.to(111)

        self.copy("Lazy Learning과는 반대되는 그림입니다", "Kₜ ≈ K₀  vs  Kₜ ≠ K₀",
                  "Lazy regime에서는 초기 kernel 구조가 거의 유지됩니다.\nCatapult에서는 큰 업데이트와 함께 kernel spectrum이 의미 있게 변할 수 있습니다.")
        self.show(self.lazy_vs_catapult())
        self.to(121.5)

        self.copy("학습하면서 Learning Rate에 대한 반응도 바뀝니다", "MODEL A → CATAPULT → MODEL B",
                  "같은 architecture라도 spike 전에는 η가 너무 컸고\nspike 후에는 같은 η가 감당 가능해질 수 있습니다.")
        states = VGroup(card("MODEL A\nsame η = too large", PRUNE, 3.1, 1.45, 21, .11),
                        label("↗  CATAPULT  ↘", 24, ACCENT),
                        card("MODEL B\nsame η = acceptable", GOOD, 3.3, 1.45, 21, .12))
        states.arrange(RIGHT, buff=.25)
        states.scale_to_fit_width(7.0).move_to([0, .15, 0])
        self.show(states)
        self.to(132.5)

        self.copy("모든 큰 Learning Rate가 살아나는 것은 아닙니다", "CATAPULT ≠ ARBITRARILY LARGE LR",
                  "더 크게 만들면 실제로 그대로 발산할 수 있습니다.\nCatapult는 특정한 large-LR 영역에서 나타나는 현상입니다.")
        self.show(self.three_regimes())
        self.to(143)

        self.copy("Edge와 Catapult는 다른 dynamics입니다", "NEAR THE EDGE  vs  CROSS AND RECOVER",
                  "Edge of Stability는 경계 부근에서 지속되는 학습입니다.\nCatapult는 경계를 넘어 spike가 난 뒤 다시 학습 가능한 상태로 돌아옵니다.")
        self.show(self.edge_vs_catapult())
        self.to(153)

        self.copy("전체 mechanism을 한 줄로 압축해봅시다", "THE CATAPULT SEQUENCE",
                  "Large LR이 Loss를 튀어 올리고 network dynamics를 바꿉니다.\nλₘₐₓ가 낮아지면 같은 η로도 Loss가 다시 감소할 수 있습니다.")
        flow = self.flow_chain()
        self.show(flow)
        self.play(LaggedStart(*[Indicate(flow[i], color=[PRUNE, ACCENT, SPARSE, GOOD][i // 2])
                                for i in range(0, 8, 2)], lag_ratio=.18), run_time=1.2)
        self.to(164)

        self.copy("실패처럼 보인 spike 안에서 조건이 바뀌었습니다", "TRAINING CHANGES THE SYSTEM",
                  "parameter update는 같은 지형 위에서 점만 옮기는 것이 아닐 수 있습니다.\n그 이동이 다음 학습의 반응 자체를 바꿀 수 있습니다.")
        plot = self.catapult_plot(1.0, True)
        self.show(VGroup(plot, card("λₘₐₓ ↓  ·  STABLE AGAIN", GOOD, 5.7, .78, 23, .14)
                         .move_to([0, -2.45, 0])))
        self.to(175)

    def boundary_pointer(self, crossed):
        stable = card("STABLE", GOOD, 2.5, .95, 24, .13)
        unstable = card("UNSTABLE", PRUNE, 2.8, .95, 23, .13)
        pair = VGroup(stable, unstable).arrange(RIGHT, buff=.18)
        x = unstable.get_center()[0] if crossed else stable.get_right()[0] - .15
        pointer = Triangle(color=ACCENT, fill_color=ACCENT, fill_opacity=1).scale(.18).rotate(PI)
        pointer.move_to([x, 1.25, 0])
        return VGroup(pair, pointer,
                      card("η λₘₐₓ  ≈  2", ACCENT, 4.1, .76, 28, .14).move_to([0, -1.25, 0]),
                      label("η increases  →", 20, MUTED).move_to([0, -2.1, 0])).move_to([0, .2, 0])

    def divergence_panel(self):
        bowl = self.bowl(WEIGHT, 6.2, 2.55).move_to([0, .35, 0])
        values = [-.7, 1.0, -1.35, 1.75, -2.25, 2.85]
        points = [np.array([x, -1.0 + .3 * x * x, 0]) for x in values]
        path = VMobject(stroke_color=PRUNE, stroke_width=4, stroke_opacity=.95)
        path.set_points_as_corners(points)
        return VGroup(bowl, card("AMPLITUDE GROWS", PRUNE, 3.8, .7, 21, .12).move_to([0, -2.25, 0]), path)

    def catapult_plot(self, fraction=1.0, show_kernel=False):
        origin = np.array([-3.0, -1.5, 0])
        axes = VGroup(Line(origin, origin + RIGHT * 6.0, color=MUTED, stroke_width=1.7),
                      Line(origin, origin + UP * 3.65, color=MUTED, stroke_width=1.7))
        ts = np.linspace(0, max(.08, fraction), 160)
        ys = .25 + 2.7 * np.exp(-((ts - .42) / .16) ** 2) + .9 * np.exp(-2.8 * ts)
        points = [np.array([origin[0] + 5.85 * t, origin[1] + y, 0]) for t, y in zip(ts, ys)]
        curve = VMobject(stroke_color=GOOD, stroke_width=4, stroke_opacity=.95)
        curve.set_points_smoothly(points)
        group = VGroup(axes, curve, label("Loss", 19, GOOD).move_to([-3.2, 2.35, 0]),
                       label("step", 18, MUTED).move_to([2.55, -1.85, 0]))
        if show_kernel:
            group.add(label("λₘₐₓ ↓", 22, ACCENT).move_to([0, 2.55, 0]),
                      Arrow([.25, 2.28, 0], [-.15, 1.55, 0], color=ACCENT, tip_length=.16))
        return group

    def catapult_arc(self):
        start = np.array([-2.8, -1.55, 0])
        end = np.array([2.6, -1.1, 0])
        arc = CubicBezier(start, [-1.7, 2.45, 0], [.9, 2.65, 0], end)
        arc.set_stroke(ACCENT, width=4, opacity=.9)
        point = Dot(start, radius=.13, color=GOOD)
        return VGroup(Dot(start, radius=.12, color=WEIGHT), Dot(end, radius=.14, color=GOOD),
                      label("INITIAL", 18, WEIGHT).move_to(start + DOWN * .55),
                      label("NEW STATE", 18, GOOD).move_to(end + DOWN * .55), arc, point)

    def fixed_vs_network(self):
        fixed = VGroup(card("FIXED QUADRATIC", WEIGHT, 3.4, .72, 20, .1),
                       self.bowl(WEIGHT, 3.1, 1.5).scale(.85),
                       label("landscape fixed", 18, MUTED)).arrange(DOWN, buff=.55)
        changing = VGroup(card("NEURAL NETWORK", SPARSE, 3.4, .72, 20, .12),
                          self.bowl(ACCENT, 2.2, 2.2).scale(.85),
                          label("dynamics change", 18, SPARSE)).arrange(DOWN, buff=.55)
        fixed.move_to([-2.05, .15, 0]); changing.move_to([2.05, .15, 0])
        return VGroup(fixed, changing)

    def lr_critical_bars(self, after):
        current = self.simple_bar("CURRENT η", .72, ACCENT)
        critical = self.simple_bar("CRITICAL η", .9 if after else .42, GOOD)
        bars = VGroup(current, critical).arrange(DOWN, buff=.8).move_to([0, .4, 0])
        relation = "CURRENT < NEW CRITICAL" if after else "CURRENT > CRITICAL"
        color = GOOD if after else PRUNE
        return VGroup(bars, card(relation, color, 5.2, .78, 23, .14).move_to([0, -2.05, 0]))

    def simple_bar(self, name, value, color):
        track = RoundedRectangle(width=5.5, height=.44, corner_radius=.1,
                                 stroke_width=0, fill_color=ZERO, fill_opacity=.48)
        fill = RoundedRectangle(width=5.1 * value, height=.26, corner_radius=.07,
                                stroke_width=0, fill_color=color, fill_opacity=.95)
        fill.move_to([track.get_left()[0] + .18 + fill.width / 2, 0, 0])
        return VGroup(label(name, 20, color).move_to([-1.8, .55, 0]), track, fill)

    def mode_spike_panel(self):
        top = self.error_mode("TOP EIGENSPACE", PRUNE, True)
        rest = self.error_mode("OTHER DIRECTIONS", GOOD, False)
        return VGroup(top, rest).arrange(DOWN, buff=.55).move_to([0, .2, 0])

    def error_mode(self, name, color, spike):
        frame = RoundedRectangle(width=6.6, height=1.75, corner_radius=.18,
                                 color=color, fill_color=color, fill_opacity=.025, stroke_width=1.8)
        xs = np.linspace(-2.0, 2.0, 100)
        ys = (.15 + .95 * np.exp(-((xs + .15) / .35) ** 2)) if spike else (.75 * np.exp(-.35 * (xs + 2)))
        pts = [np.array([x + .7, -.45 + y, 0]) for x, y in zip(xs, ys)]
        curve = VMobject(stroke_color=color, stroke_width=3.2).set_points_smoothly(pts)
        return VGroup(frame, label(name, 18, color).move_to([-2.2, .5, 0]), curve)

    def coupled_plot(self):
        return VGroup(self.mini_curve("LOSS", PRUNE, True), self.mini_curve("λₘₐₓ(K)", SPARSE, False))

    def mini_curve(self, title, color, spike):
        origin = np.array([-2.65, -1.0, 0])
        axes = VGroup(Line(origin, origin + RIGHT * 5.25, color=MUTED, stroke_width=1.4),
                      Line(origin, origin + UP * 1.85, color=MUTED, stroke_width=1.4))
        ts = np.linspace(0, 1, 100)
        ys = (.25 + 1.4 * np.exp(-((ts - .45) / .17) ** 2)) if spike else (1.55 - 1.05 / (1 + np.exp(-10 * (ts - .45))))
        pts = [np.array([origin[0] + 5.05 * t, origin[1] + y, 0]) for t, y in zip(ts, ys)]
        curve = VMobject(stroke_color=color, stroke_width=3.5).set_points_smoothly(pts)
        group = VGroup(axes, label(title, 18, color).move_to([-2.85, .95, 0]), curve)
        group.scale(.95)
        group.move_to([0, 1.25 if spike else -1.15, 0])
        return group

    def turning_point_plot(self):
        plot = self.catapult_plot(1.0, False)
        divider = DashedLine([-.55, -1.5, 0], [-.55, 2.1, 0], color=ACCENT, dash_length=.12)
        return VGroup(plot, divider,
                      label("η > η_crit", 18, PRUNE).move_to([-1.8, 2.45, 0]),
                      label("η < new η_crit", 18, GOOD).move_to([1.35, 2.45, 0]),
                      card("DYNAMICS CHANGED", ACCENT, 3.8, .62, 19, .12).move_to([0, -2.45, 0]))

    def lazy_vs_catapult(self):
        lazy = VGroup(card("LAZY", WEIGHT, 3.2, .82, 25, .12),
                      card("Kₜ ≈ K₀", WEIGHT, 3.2, .82, 27, .08),
                      label("kernel almost fixed", 18, MUTED)).arrange(DOWN, buff=.42)
        catapult = VGroup(card("CATAPULT", ACCENT, 3.2, .82, 25, .14),
                          card("Kₜ ≠ K₀", SPARSE, 3.2, .82, 27, .1),
                          label("spectrum changes", 18, SPARSE)).arrange(DOWN, buff=.42)
        return VGroup(lazy, catapult).arrange(RIGHT, buff=.45).move_to([0, .2, 0])

    def three_regimes(self):
        panels = VGroup(self.regime("SMALL LR", GOOD, "CONVERGE", 0),
                        self.regime("CATAPULT", ACCENT, "SPIKE → RECOVER", 1),
                        self.regime("TOO LARGE", PRUNE, "DIVERGE", 2))
        return panels.arrange(RIGHT, buff=.16).scale(.93).move_to([0, .15, 0])

    def regime(self, title, color, result, kind):
        frame = RoundedRectangle(width=2.45, height=4.1, corner_radius=.18,
                                 color=color, fill_color=color, fill_opacity=.025, stroke_width=1.8)
        xs = np.linspace(-.9, .9, 80)
        if kind == 0:
            ys = .75 * np.exp(-1.5 * (xs + .9))
        elif kind == 1:
            ys = .15 + 1.15 * np.exp(-((xs + .05) / .28) ** 2)
        else:
            ys = .25 + .45 * (xs + .9) ** 1.6
        pts = [np.array([x, -.55 + y, 0]) for x, y in zip(xs, ys)]
        curve = VMobject(stroke_color=color, stroke_width=3).set_points_smoothly(pts)
        return VGroup(frame, label(title, 16, color).move_to([0, 1.55, 0]), curve,
                      label(result, 15, color).move_to([0, -1.55, 0]))

    def edge_vs_catapult(self):
        edge = VGroup(card("EDGE", WEIGHT, 3.3, .75, 23, .11),
                      self.mini_curve("near boundary", WEIGHT, False).scale(.55),
                      label("stay near the edge", 17, MUTED)).arrange(DOWN, buff=.35)
        cat = VGroup(card("CATAPULT", ACCENT, 3.3, .75, 23, .14),
                     self.mini_curve("spike", PRUNE, True).scale(.55),
                     label("cross → recover", 17, ACCENT)).arrange(DOWN, buff=.35)
        return VGroup(edge, cat).arrange(RIGHT, buff=.35).move_to([0, .2, 0])

    def flow_chain(self):
        items = [card("LARGE LR", PRUNE, 4.2, .62, 20, .11), label("↓", 24, MUTED),
                 card("LOSS SPIKE", ACCENT, 4.2, .62, 20, .12), label("↓", 24, MUTED),
                 card("NTK SPECTRUM CHANGES", SPARSE, 5.2, .62, 19, .12), label("↓", 24, MUTED),
                 card("λₘₐₓ ↓ · LOSS ↓", GOOD, 4.4, .66, 21, .13)]
        return VGroup(*items).arrange(DOWN, buff=.17).move_to([0, .2, 0])
