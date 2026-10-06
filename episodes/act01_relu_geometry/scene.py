"""Activation Geometry 01: follow one ReLU coordinate through a fixed plane."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import (
    ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, ZERO, txt,
)


def label(value, size=27, color=INK, width=7.6, weight=NORMAL):
    return txt(value, size, color, width, weight)


def card(value, color=WEIGHT, width=3.0, height=.85, size=23, fill=.1):
    box = RoundedRectangle(
        width=width, height=height, corner_radius=.16,
        stroke_color=color, stroke_width=2,
        fill_color=color, fill_opacity=fill,
    )
    return VGroup(box, label(value, size, color, width - .2))


class ReLUGeometry(Scene):
    DURATION = 94

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.caption = VGroup()
        self.caption_box = VGroup()
        self.chrome = VGroup(
            label("ACTIVATION GEOMETRY  /  01", 18, MUTED).move_to(UP * 7.3),
            label("ReLU는 좌표를 어떻게 압축할까?", 30).move_to(UP * 6.46),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0], color=MUTED, stroke_opacity=.35),
        )
        self.progress = Rectangle(
            width=.01, height=.035, fill_color=ACCENT, fill_opacity=1, stroke_width=0,
        ).move_to([-3.8, -7.36, 0])
        self.base_plane = self.coordinate_plane(opacity=.2)
        self.add(self.base_plane, self.chrome, self.progress)
        self.add_foreground_mobjects(self.chrome, self.progress)

        self.copy("숫자 하나가 아니라 좌표평면 전체에서", "ReLU(z) = max(0, z)",
                  "ReLU는 음수를 0으로 만들고, 양수는 그대로 둡니다.\n이번에는 이 연산을 좌표평면 전체에서 보겠습니다.")
        formula = card("ReLU(z) = max(0, z)", ACCENT, 5.8, .95, 30, .14).move_to([0, 2.35, 0])
        flows = VGroup(
            card("−2  →  0", PRUNE, 2.2, .72, 23, .12),
            card("+2  →  +2", GOOD, 2.2, .72, 23, .12),
        ).arrange(RIGHT, buff=.5).move_to([0, -1.95, 0])
        self.show(VGroup(formula, flows))
        self.to(9)

        self.copy("뉴런은 공간에서 한 방향을 바라봅니다", "w  ·  DIRECTION",
                  "뉴런의 w는 공간에서 바라보는 방향입니다.\n점 x를 그 방향에 투영해 wᵀx+b를 계산합니다.")
        boundary = self.boundary(color=MUTED, opacity=.35, width=2.5)
        w_arrow = Arrow([-2.45, -2.15, 0], [-.75, -1.215, 0], buff=0,
                        color=WEIGHT, stroke_width=6, tip_length=.22)
        w_tag = card("weight  w", WEIGHT, 2.05, .65, 20, .12).next_to(w_arrow, DOWN, buff=.18)
        u_tracker = ValueTracker(-1.6)
        v_value = .55
        point = always_redraw(lambda: Dot(
            self.uv_point(u_tracker.get_value(), v_value), radius=.14, color=ACCENT
        ))
        point_tag = always_redraw(lambda: label("x", 24, ACCENT).next_to(point, RIGHT, buff=.15))
        projection = always_redraw(lambda: DashedLine(
            self.uv_point(0, v_value), point.get_center(),
            color=ACCENT, stroke_width=4, dash_length=.14,
        ))
        foot_dot = Dot(self.uv_point(0, v_value), radius=.08, color=INK)
        u_box = RoundedRectangle(width=2.9, height=.72, corner_radius=.16,
                                 stroke_color=ACCENT, stroke_width=2,
                                 fill_color=ACCENT, fill_opacity=.13).move_to([1.75, 2.95, 0])
        u_readout = always_redraw(lambda: label(
            f"u = {u_tracker.get_value():+.2f}", 23, ACCENT
        ).move_to(u_box))
        self.show(VGroup(boundary, w_arrow, w_tag, projection, foot_dot,
                         point, point_tag, u_box, u_readout))
        self.play(u_tracker.animate.set_value(1.8), run_time=1.6, rate_func=smooth)
        self.play(u_tracker.animate.set_value(.65), run_time=1.0, rate_func=smooth)
        self.to(18)

        self.copy("w 방향을 새로운 좌표 u로", "(x₁, x₂)  →  (u, v)",
                  "w 방향을 u축으로 잡고, 경계와 평행한 방향을\nv축으로 잡으면 u=0이 곧 활성화 경계입니다.")
        uv_target = self.uv_axes()
        moving_grid = self.cartesian_dense_grid()
        moving_grid.set_opacity(.48)
        axis_note = VGroup(
            card("u = wᵀx+b", WEIGHT, 2.8, .68, 21, .12),
            card("v = boundary direction", GOOD, 3.35, .68, 19, .12),
        ).arrange(DOWN, buff=.18).move_to([1.85, 2.85, 0])
        self.add(moving_grid)
        self.play(
            FadeOut(VGroup(w_tag, projection, foot_dot, point, point_tag, u_box, u_readout)),
            FadeIn(moving_grid),
            run_time=.55,
        )
        self.play(
            Transform(w_arrow, uv_target[0]),
            Transform(boundary, uv_target[1]),
            Transform(moving_grid, self.uv_grid()),
            FadeIn(uv_target[2]), FadeIn(uv_target[3]), FadeIn(axis_note),
            self.base_plane.animate.set_opacity(.26),
            run_time=2.0, rate_func=smooth,
        )
        u_label, v_label = uv_target[2], uv_target[3]
        self.stage = VGroup(moving_grid, w_arrow, boundary, u_label, v_label, axis_note)
        self.play(Indicate(w_arrow, color=WEIGHT), Indicate(boundary, color=GOOD), run_time=1.0)
        self.to(29)

        self.copy("u=0을 건너면 부호가 바뀝니다", "u < 0  /  u > 0",
                  "u=0 직선을 건너면 좌표의 부호가 바뀝니다.\n양수 쪽에서는 뉴런이 켜지고, 음수 쪽에서는 꺼집니다.")
        inactive, active = self.uv_half_planes()
        tags = VGroup(
            card("u < 0  ·  OFF", PRUNE, 2.3, .68, 20, .13).move_to([-2.25, -2.65, 0]),
            card("u > 0  ·  ON", GOOD, 2.3, .68, 20, .13).move_to([2.25, 2.65, 0]),
        )
        point = Dot(self.uv_point(1.45, .2), radius=.13, color=INK)
        self.add(inactive, active)
        self.bring_to_front(moving_grid, w_arrow, boundary, u_label, v_label)
        self.play(FadeOut(axis_note), FadeIn(inactive), FadeIn(active), FadeIn(tags), FadeIn(point),
                  Transform(boundary, self.boundary(color=ACCENT, opacity=1, width=5)),
                  run_time=.7)
        self.stage = VGroup(inactive, active, moving_grid, w_arrow, boundary,
                            u_label, v_label, tags, point)
        self.play(point.animate.move_to(self.uv_point(-1.35, .2)), run_time=1.5)
        self.to(35)

        self.copy("ReLU는 음수 u를 경계로 붕괴시킵니다", "(u, v)  →  (max(0,u), v)",
                  "양수인 u는 그대로 남지만, 음수인 u는 모두 0이 됩니다.\n서로 다른 위치들이 u 방향에서는 경계에 겹칩니다.")
        self.play(self.base_plane.animate.set_opacity(.14), run_time=.35)
        samples = VGroup(*[
            Dot(self.uv_point(u, .75), radius=.085, color=PRUNE)
            for u in (-2.0, -1.45, -.9, -.35)
        ])
        sample_arrows = VGroup(*[
            Arrow(dot.get_center(), self.uv_point(0, .75), buff=.08,
                  color=PRUNE, stroke_width=2.5, tip_length=.14)
            for dot in samples
        ])
        self.play(FadeOut(VGroup(inactive, active, tags, point, w_arrow)),
                  FadeIn(samples), FadeIn(sample_arrows), run_time=.55)
        self.stage = VGroup(moving_grid, boundary, u_label, v_label, samples, sample_arrows)
        self.play(FadeOut(sample_arrows), FadeOut(samples),
                  moving_grid.animate.apply_function(self.relu_uv),
                  run_time=3.5, rate_func=smooth)
        collapse = card("u<0  →  u=0", PRUNE, 2.7, .7, 22, .14).move_to([-1.65, -3.15, 0])
        keep = card("u>0  →  unchanged", GOOD, 3.1, .7, 20, .14).move_to([1.65, 3.15, 0])
        self.play(FadeIn(collapse), FadeIn(keep), Indicate(boundary, color=INK), run_time=1.1)
        self.stage.add(collapse, keep)
        self.restore_layers()
        self.to(47)

        self.copy("사라진 것은 u 방향의 위치 정보입니다", "MANY u VALUES  →  ONE VALUE",
                  "v 방향은 구분해 둔 채, u<0의 서로 다른 좌표들이\n모두 같은 u=0으로 눌려 붙습니다.")
        grid = self.uv_grid()
        grid.apply_function(self.relu_uv)
        boundary = self.boundary(color=ACCENT, opacity=1, width=7)
        row_points = VGroup(*[
            Dot(self.uv_point(0, v), radius=.095, color=PRUNE)
            for v in (-1.5, -.75, 0, .75, 1.5)
        ])
        note = card("lost coordinate: negative u", PRUNE, 4.1, .76, 21, .14).move_to([0, -3.15, 0])
        self.show(VGroup(grid, boundary, row_points, note))
        self.play(LaggedStart(*[Indicate(p, color=INK) for p in row_points], lag_ratio=.12), run_time=1.4)
        self.to(56)

        self.copy("뉴런 하나는 방향·좌표·경계를 만듭니다", "wᵢ  →  uᵢ  →  uᵢ=0",
                  "뉴런 하나는 방향 wᵢ와 좌표 uᵢ를 만들고,\n그 좌표가 0인 경계를 공간에 남깁니다.")
        self.play(self.base_plane.animate.set_opacity(.34), run_time=.3)
        triples = self.neuron_triples()
        self.show(VGroup())
        visible = VGroup()
        arrow, line, badge = triples[0]
        self.play(GrowArrow(arrow), Create(line), FadeIn(badge), run_time=1.2)
        visible.add(arrow, line, badge)
        self.stage = visible
        self.to(63)

        self.copy("여러 좌표의 경계가 공간을 조각냅니다", "u₁=0  ·  u₂=0  ·  u₃=0",
                  "뉴런이 여러 개라면 좌표와 경계도 여러 개 생깁니다.\n그 경계들의 조합이 공간을 여러 조각으로 나눕니다.")
        for arrow, line, badge in triples[1:]:
            self.play(GrowArrow(arrow), Create(line), FadeIn(badge), run_time=.85)
            visible.add(arrow, line, badge)
        regions = self.region_tints()
        self.play(LaggedStart(*[FadeIn(r) for r in regions], lag_ratio=.12), run_time=1.0)
        self.stage.add(regions)
        self.to(71)

        self.copy("각 조각은 부호 좌표를 가집니다", "sign(u₁, u₂, u₃)",
                  "같은 조각 안에서는 각 uᵢ의 부호가 바뀌지 않습니다.\n즉 어떤 ReLU가 켜지고 꺼지는지가 고정됩니다.")
        lines = self.multi_boundaries()
        region = Polygon([.15, .1, 0], [2.55, 1.85, 0], [1.22, 2.75, 0], [.58, .93, 0],
                         color=GOOD, fill_color=GOOD, fill_opacity=.2, stroke_width=2)
        point = Dot([.78, .92, 0], radius=.13, color=INK)
        pattern = card("(+ , + , −)", GOOD, 3.0, .76, 26, .15).move_to([0, 3.25, 0])
        coords = label("(u₁, u₂, u₃)", 22, MUTED).move_to([0, 2.62, 0])
        self.show(VGroup(region, lines, point, pattern, coords))
        path = VMobject().set_points_smoothly([[.78, .92, 0], [1.25, 1.18, 0], [1.75, 1.42, 0]])
        self.play(MoveAlongPath(point, path), run_time=1.6)
        self.to(78)

        self.copy("경계 하나를 넘으면 부호 하나가 뒤집힙니다", "ONE BOUNDARY  ·  ONE SIGN FLIP",
                  "경계를 하나 넘는 순간 활성화 패턴의 한 부호가 바뀌고,\n적용되는 affine 규칙도 함께 바뀝니다.")
        lines = self.multi_boundaries()
        point = Dot([1.35, 1.2, 0], radius=.14, color=GOOD)
        pattern = card("(+,+,−)", GOOD, 2.3, .7, 23, .13).move_to([-1.8, 3.15, 0])
        rule = card("f(x)=Aᵣx+cᵣ", GOOD, 3.0, .72, 22, .13).move_to([1.75, 3.15, 0])
        arrow = Arrow([1.35, 1.12, 0], [1.35, .77, 0], color=ACCENT,
                      stroke_width=4, buff=.1, tip_length=.18)
        self.show(VGroup(lines, point, pattern, rule, arrow))
        self.play(point.animate.move_to([1.35, .70, 0]),
                  Transform(pattern, card("(+,−,−)", SPARSE, 2.3, .7, 23, .13).move_to(pattern)),
                  Transform(rule, card("f(x)=Aₛx+cₛ", SPARSE, 3.0, .72, 22, .13).move_to(rule)),
                  run_time=1.8)
        self.to(84)

        self.copy("방향에서 좌표로, 좌표에서 규칙으로", "DIRECTION → COORDINATE → SIGN → REGION",
                  "ReLU 신경망은 방향별 좌표의 부호로 공간을 나누고,\n각 조각에 서로 다른 affine 규칙을 연결합니다.")
        lines = self.multi_boundaries(opacity=.65)
        patterns = VGroup(
            card("(+,+,−)", GOOD, 2.0, .62, 19, .12).move_to([1.65, 1.8, 0]),
            card("(+,−,−)", SPARSE, 2.0, .62, 19, .12).move_to([1.65, -.75, 0]),
            card("(−,−,+)", PRUNE, 2.0, .62, 19, .12).move_to([-1.55, -.9, 0]),
        )
        final = label("같은 부호 조각  →  같은 affine rule", 26, ACCENT).move_to([0, -3.15, 0])
        self.show(VGroup(lines, patterns, final))
        self.play(LaggedStart(*[Indicate(p) for p in patterns], lag_ratio=.15), run_time=1.1)
        self.to(94)

    def coordinate_plane(self, opacity=.25):
        grid = VGroup()
        for x in np.linspace(-3, 3, 9):
            grid.add(Line([x, -2.75, 0], [x, 2.75, 0], color=ZERO,
                          stroke_width=1.15, stroke_opacity=opacity))
        for y in np.linspace(-2.75, 2.75, 9):
            grid.add(Line([-3, y, 0], [3, y, 0], color=ZERO,
                          stroke_width=1.15, stroke_opacity=opacity))
        x_axis = Arrow([-3.2, 0, 0], [3.35, 0, 0], color=MUTED,
                       stroke_width=2, buff=0, tip_length=.14)
        y_axis = Arrow([0, -2.95, 0], [0, 3.05, 0], color=MUTED,
                       stroke_width=2, buff=0, tip_length=.14)
        return VGroup(grid, x_axis, y_axis,
                      label("x₁", 18, MUTED).move_to([3.35, -.28, 0]),
                      label("x₂", 18, MUTED).move_to([-.27, 3.0, 0]))

    @property
    def normal(self):
        n = np.array([1.0, .55, 0.0])
        return n / np.linalg.norm(n)

    @property
    def tangent(self):
        n = self.normal
        return np.array([-n[1], n[0], 0.0])

    @property
    def uv_origin(self):
        return self.normal * (.3 / np.sqrt(1 + .55 ** 2))

    def uv_point(self, u, v):
        return self.uv_origin + u * self.normal + v * self.tangent

    def boundary(self, color=ACCENT, opacity=1, width=5):
        return Line(self.uv_point(0, -3.05), self.uv_point(0, 3.05),
                    color=color, stroke_width=width, stroke_opacity=opacity)

    def project_to_boundary(self, point):
        u = np.dot(self.normal, point - self.uv_origin)
        return point - u * self.normal

    def uv_axes(self, labels_only=False):
        u_axis = Arrow(self.uv_point(-2.85, 0), self.uv_point(2.95, 0), buff=0,
                       color=WEIGHT, stroke_width=4, tip_length=.18)
        v_axis = Arrow(self.uv_point(0, -2.85), self.uv_point(0, 2.95), buff=0,
                       color=GOOD, stroke_width=4, tip_length=.18)
        u_tag = card("u", WEIGHT, .62, .55, 21, .12).move_to(self.uv_point(2.55, -.35))
        v_tag = card("v", GOOD, .62, .55, 21, .12).move_to(self.uv_point(.35, 2.55))
        return VGroup(u_tag, v_tag) if labels_only else VGroup(u_axis, v_axis, u_tag, v_tag)

    def uv_half_planes(self):
        neg = Polygon(self.uv_point(-2.7, -2.7), self.uv_point(0, -2.7),
                      self.uv_point(0, 2.7), self.uv_point(-2.7, 2.7),
                      stroke_width=0, fill_color=PRUNE, fill_opacity=.17)
        pos = Polygon(self.uv_point(0, -2.7), self.uv_point(2.7, -2.7),
                      self.uv_point(2.7, 2.7), self.uv_point(0, 2.7),
                      stroke_width=0, fill_color=GOOD, fill_opacity=.17)
        return neg, pos

    def cartesian_dense_grid(self):
        """Transformable foreground copy of the persistent x1,x2 grid."""
        grid = VGroup()
        for x in np.linspace(-2.45, 2.45, 13):
            line = VMobject(color=WEIGHT, stroke_width=1.55, stroke_opacity=.55)
            line.set_points_as_corners([
                [x, y, 0] for y in np.linspace(-2.45, 2.45, 45)
            ])
            grid.add(line)
        for y in np.linspace(-2.45, 2.45, 13):
            line = VMobject(color=WEIGHT, stroke_width=1.55, stroke_opacity=.55)
            line.set_points_as_corners([
                [x, y, 0] for x in np.linspace(-2.45, 2.45, 49)
            ])
            grid.add(line)
        return grid

    def uv_grid(self):
        grid = VGroup()
        for u in np.linspace(-2.45, 2.45, 13):
            line = VMobject(color=WEIGHT, stroke_width=1.55, stroke_opacity=.55)
            line.set_points_as_corners([self.uv_point(u, v) for v in np.linspace(-2.45, 2.45, 45)])
            grid.add(line)
        for v in np.linspace(-2.45, 2.45, 13):
            line = VMobject(color=WEIGHT, stroke_width=1.55, stroke_opacity=.55)
            line.set_points_as_corners([self.uv_point(u, v) for u in np.linspace(-2.45, 2.45, 49)])
            grid.add(line)
        return grid

    def relu_uv(self, point):
        q = point - self.uv_origin
        u = np.dot(q, self.normal)
        v = np.dot(q, self.tangent)
        return self.uv_point(max(0.0, u), v)

    def neuron_triples(self):
        specs = (
            (ACCENT, [-2.7, -1.35, 0], [-2.0, -2.33, 0], [-3.0, -2.15, 0], [3.0, 2.15, 0], "u₁", [-2.35, -3.15, 0]),
            (GOOD, [-2.75, 1.45, 0], [-1.7, 2.5, 0], [-2.65, 2.65, 0], [2.65, -2.65, 0], "u₂", [-2.3, 3.15, 0]),
            (SPARSE, [1.75, -2.0, 0], [2.9, -2.4, 0], [-.75, -2.75, 0], [1.15, 2.75, 0], "u₃", [2.35, -3.15, 0]),
        )
        groups = []
        for color, a0, a1, l0, l1, name, badge_pos in specs:
            arrow = Arrow(a0, a1, buff=0, color=color, stroke_width=5, tip_length=.19)
            line = Line(l0, l1, color=color, stroke_width=4)
            badge = card(f"{name}=wᵢᵀx+bᵢ", color, 2.5, .62, 18, .12).move_to(badge_pos)
            groups.append((arrow, line, badge))
        return groups

    def multi_boundaries(self, opacity=1):
        return VGroup(
            Line([-3.0, -2.15, 0], [3.0, 2.15, 0], color=ACCENT, stroke_width=4, stroke_opacity=opacity),
            Line([-2.65, 2.65, 0], [2.65, -2.65, 0], color=GOOD, stroke_width=4, stroke_opacity=opacity),
            Line([-.75, -2.75, 0], [1.15, 2.75, 0], color=SPARSE, stroke_width=4, stroke_opacity=opacity),
        )

    def region_tints(self):
        return VGroup(
            Polygon([-2.8, 2.25, 0], [-.35, .45, 0], [-.75, -.55, 0], fill_color=PRUNE, fill_opacity=.13, stroke_width=0),
            Polygon([-.35, .45, 0], [.35, -.1, 0], [1.0, 1.8, 0], fill_color=GOOD, fill_opacity=.14, stroke_width=0),
            Polygon([.35, -.1, 0], [2.6, -1.75, 0], [.82, 1.28, 0], fill_color=SPARSE, fill_opacity=.14, stroke_width=0),
        )

    def copy(self, heading, note, caption):
        old = VGroup(self.heading, self.note, self.caption, self.caption_box)
        if len(old):
            self.remove_foreground_mobjects(self.heading, self.note,
                                            self.caption_box, self.caption)
            self.play(FadeOut(old), run_time=.1)
        self.heading = label(heading, 29).move_to(UP * 5.12)
        self.note = label(note, 19, ACCENT).move_to(DOWN * 4.42)
        self.caption_box = RoundedRectangle(
            width=7.65, height=1.15, corner_radius=.14,
            stroke_color=ZERO, stroke_width=1.2, fill_color=ZERO, fill_opacity=.32,
        ).move_to([0, -5.65, 0])
        self.caption = label(caption, 19, INK, 7.2).move_to(self.caption_box)
        self.play(FadeIn(self.heading), FadeIn(self.note), FadeIn(self.caption_box),
                  FadeIn(self.caption), run_time=.2)
        self.add_foreground_mobjects(self.chrome, self.heading, self.note,
                                    self.caption_box, self.caption, self.progress)
        self.restore_layers()

    def show(self, new_stage):
        if len(self.stage):
            self.play(FadeOut(self.stage), run_time=.18)
        self.stage = new_stage
        if len(self.stage):
            self.play(FadeIn(self.stage, shift=UP * .12), run_time=.4)
        self.restore_layers()

    def restore_layers(self):
        self.chrome[0].set_opacity(1)
        self.chrome[1].set_opacity(1)
        self.chrome[2].set_stroke(opacity=.35)
        self.add(self.base_plane, self.chrome, self.progress)
        self.bring_to_front(self.chrome, self.heading, self.note,
                            self.caption_box, self.caption, self.progress)

    def to(self, target):
        # Reassert persistent coordinate/chrome layers after any transform.
        # Most of each timed section is the hold created below, so this keeps
        # the fixed frame visible throughout the narrated interval.
        self.restore_layers()
        remaining = target - self.time
        if remaining < -.04:
            raise ValueError(f"Timeline overrun at {target}: {self.time:.2f}")
        width = max(.01, 7.6 * target / self.DURATION)
        if remaining > 0:
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to(
                [-3.8 + width / 2, -7.36, 0]), run_time=min(.25, remaining))
            self.wait(max(0, target - self.time))
