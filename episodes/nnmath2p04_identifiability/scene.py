"""Neural Network Mathematics Part 2, episode 04: Identifiability."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import (
    ACCENT, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, ZERO, txt,
)


FEATURE_COLORS = (WEIGHT, PRUNE, GOOD, SPARSE, ACCENT)


def label(value, size=27, color=INK, width=7.6, weight=NORMAL):
    return txt(value, size, color, width, weight)


def card(value, color=WEIGHT, width=3.0, height=.86, size=23, fill=.1):
    box = RoundedRectangle(
        width=width, height=height, corner_radius=.16,
        stroke_color=color, stroke_width=2,
        fill_color=color, fill_opacity=fill,
    )
    return VGroup(box, label(value, size, color, width - .25))


class NeuralMathPart2Identifiability(Scene):
    DURATION = 112

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.caption = VGroup()
        self.caption_box = VGroup()
        self.chrome = VGroup(
            label("NEURAL NETWORK MATHEMATICS  /  PART 2 · 04", 17, MUTED).move_to(UP * 7.3),
            label("모델의 진짜 Feature를 찾았다는 걸 어떻게 알까?", 28).move_to(UP * 6.45),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0], color=MUTED, stroke_opacity=.35),
        )
        self.progress = Line(
            [-3.8, -7.36, 0], [-3.79, -7.36, 0],
            color=ACCENT, stroke_width=4,
        )
        self.add(self.chrome, self.progress)

        # 1 — Start where Polysemanticity ended.
        self.copy(
            "뉴런은 좌표축, feature는 그 사이의 방향", "FROM NEURONS TO FEATURES",
            "그렇다면 이제 해야 할 일은 간단해 보입니다.\n그 feature 방향을 찾으면 될까요?",
        )
        neurons = VGroup(
            card("h₁", WEIGHT, 1.0, .62, 21, .12),
            card("h₂", PRUNE, 1.0, .62, 21, .12),
            card("h₃", GOOD, 1.0, .62, 21, .12),
        ).arrange(DOWN, buff=.45).move_to([-2.75, .2, 0])
        transition = Arrow([-1.9, .2, 0], [-.95, .2, 0], buff=0,
                           color=ACCENT, stroke_width=4, tip_length=.2)
        space = self.feature_space(2.0, five=True).move_to([1.25, .2, 0])
        self.show(VGroup(neurons, transition, space,
                         card("Find the feature directions", ACCENT, 5.3, .78, 23, .14)
                         .move_to([0, -2.8, 0])))
        self.to(7)

        # 2 — Apparently interpretable features are found.
        self.copy(
            "해석하기 좋은 방향을 찾았습니다", "ACTIVATION ANALYSIS",
            "고양이, 털, 귀와 연결되는 방향들.\n이제 모델의 feature를 발견한 걸까요?",
        )
        cloud = self.activation_cloud().move_to([-1.95, .25, 0])
        found = VGroup(
            self.feature_tag("v₁", "CAT", WEIGHT),
            self.feature_tag("v₂", "FUR", PRUNE),
            self.feature_tag("v₃", "EAR", GOOD),
        ).arrange(DOWN, buff=.35).move_to([2.15, .25, 0])
        arrow = Arrow([-.5, .25, 0], [.6, .25, 0], buff=0,
                      color=ACCENT, stroke_width=4, tip_length=.2)
        check = label("✓", 48, GOOD).move_to([3.3, -2.0, 0])
        self.show(VGroup(cloud, arrow, found, check,
                         label("interpretable directions", 20, ACCENT).move_to([0, -2.75, 0])))
        self.to(14)

        # 3 — The first dictionary reconstructs h.
        self.copy(
            "원래 activation도 정확히 설명합니다", "h = z₁v₁ + z₂v₂ + z₃v₃",
            "세 방향을 조합하자 h에 도착합니다.\n상당히 좋은 증거처럼 보입니다.",
        )
        origin = np.array([-2.4, -1.1, 0])
        steps = VGroup(
            Arrow(origin, origin + np.array([1.55, 0, 0]), buff=.03,
                  color=WEIGHT, stroke_width=5, tip_length=.18),
            Arrow(origin + np.array([1.55, 0, 0]), origin + np.array([1.55, 1.45, 0]),
                  buff=.03, color=PRUNE, stroke_width=5, tip_length=.18),
            Arrow(origin + np.array([1.55, 1.45, 0]), origin + np.array([3.6, 2.35, 0]),
                  buff=.03, color=GOOD, stroke_width=5, tip_length=.18),
        )
        target = Dot(origin + np.array([3.6, 2.35, 0]), radius=.13, color=ACCENT)
        h_tag = card("h", ACCENT, .9, .68, 25, .14).next_to(target, RIGHT, buff=.25)
        legend = VGroup(
            card("z₁v₁", WEIGHT, 1.45, .58, 18, .1),
            card("z₂v₂", PRUNE, 1.45, .58, 18, .1),
            card("z₃v₃", GOOD, 1.45, .58, 18, .1),
        ).arrange(RIGHT, buff=.25).move_to([0, 2.5, 0])
        success = card("Reconstruction successful", GOOD, 5.3, .78, 23, .14).move_to([0, -2.8, 0])
        self.show(VGroup(legend, success))
        self.play(
            LaggedStart(
                *[FadeIn(step) for step in steps],
                AnimationGroup(FadeIn(target), FadeIn(h_tag)),
                lag_ratio=.2,
            ),
            run_time=1.2,
        )
        # FadeIn adds the animated arrows as top-level scene objects.  Re-own
        # everything through one stage group so the next scene removes it all.
        self.remove(*steps, steps, target, h_tag, self.stage)
        self.stage = VGroup(legend, success, steps, target, h_tag)
        self.add(self.stage)
        self.to(21)

        # 4 — A second dictionary reaches the same h.
        self.copy(
            "그런데 다른 방향들도 같은 h를 만듭니다", "h = q₁u₁ + q₂u₂ + q₃u₃",
            "전혀 다른 feature 방향의 조합도\n같은 activation을 똑같이 복원합니다.",
        )
        left = self.decomposition_panel("DECOMPOSITION A", (0, 90, 28),
                                        (WEIGHT, PRUNE, GOOD)).move_to([-2.0, .25, 0])
        right = self.decomposition_panel("DECOMPOSITION B", (35, 145, 300),
                                         (SPARSE, ACCENT, PRUNE)).move_to([2.0, .25, 0])
        equals = card("same h", ACCENT, 1.55, .68, 20, .13)
        self.show(VGroup(left, right, equals,
                         label("different directions  ·  same reconstruction", 20, MUTED)
                         .move_to([0, -2.8, 0])))
        self.to(28)

        # 5 — Thumbnail-friendly hold: both answers fit.
        self.copy(
            "둘 다 정답이라면?", "WHICH ONE DOES THE MODEL USE?",
            "둘 다 관측을 설명합니다.\n좋은 복원은 유일한 설명을 뜻하지 않습니다.",
        )
        left = self.answer_panel("A", "h = Σ zᵢvᵢ", WEIGHT).move_to([-2.05, .5, 0])
        right = self.answer_panel("B", "h = Σ qⱼuⱼ", SPARSE).move_to([2.05, .5, 0])
        question = label("?", 72, ACCENT).move_to([0, .55, 0])
        thumbnail_line = card("좋은 복원  ≠  유일한 설명", ACCENT, 6.8, .92, 28, .18)
        thumbnail_line.move_to([0, -2.55, 0])
        self.show(VGroup(left, right, question, thumbnail_line))
        self.to(35)

        # 6 — A minimal 2D counterexample.
        self.copy(
            "가장 단순한 예", "h = (1, 1)",
            "두 축 방향의 합으로도, 대각선 하나로도\n같은 벡터를 설명할 수 있습니다.",
        )
        axes_left = self.axes_panel("A + B", WEIGHT).move_to([-2.05, .25, 0])
        origin_l = axes_left[1].get_center()
        target_l = axes_left[3].get_center()
        corner_l = np.array([target_l[0], origin_l[1], 0])
        parts = VGroup(
            Arrow(origin_l, corner_l, buff=.03,
                  color=WEIGHT, stroke_width=4, tip_length=.16),
            Arrow(corner_l, target_l,
                  buff=.03, color=PRUNE, stroke_width=4, tip_length=.16),
        )
        axes_right = self.axes_panel("C", SPARSE).move_to([2.05, .25, 0])
        origin_r = axes_right[1].get_center()
        target_r = axes_right[3].get_center()
        diagonal = Arrow(origin_r, target_r, buff=.03,
                         color=SPARSE, stroke_width=5, tip_length=.18)
        formulas = VGroup(
            label("(1,0) + (0,1)", 19, WEIGHT).move_to([-2.05, -2.0, 0]),
            label("√2 · (1,1)/√2", 19, SPARSE).move_to([2.05, -2.0, 0]),
        )
        self.show(VGroup(axes_left, axes_right, parts, diagonal, formulas,
                         card("same vector  ·  different interpretation", ACCENT, 6.1, .74, 20, .12)
                         .move_to([0, -2.8, 0])))
        self.to(42)

        # 7 — Observed effect, hidden cause.
        self.copy(
            "결과를 보고 숨은 원인을 추론합니다", "OBSERVED h  →  HIDDEN ?",
            "관찰하는 것은 activation h.\n알고 싶은 것은 h를 만든 숨은 feature입니다.",
        )
        hidden = VGroup(
            card("z₁", WEIGHT, 1.15, .65, 20, .1),
            card("z₂", PRUNE, 1.15, .65, 20, .1),
            card("z₃", SPARSE, 1.15, .65, 20, .1),
        ).arrange(DOWN, buff=.32).move_to([-2.25, .35, 0])
        cover = RoundedRectangle(width=2.2, height=3.7, corner_radius=.2,
                                 color=ZERO, fill_color=ZERO, fill_opacity=.92)
        cover.move_to(hidden)
        cover_label = label("hidden cause", 20, MUTED).move_to(cover)
        forward = Arrow([-.9, .35, 0], [.65, .35, 0], buff=0,
                        color=MUTED, stroke_width=3, tip_length=.18)
        observed = card("activation h", ACCENT, 2.7, 1.0, 25, .16).move_to([2.1, .35, 0])
        reverse = CurvedArrow([1.45, -1.0, 0], [-1.35, -1.0, 0], angle=-.5,
                              color=PRUNE, stroke_width=3, tip_length=.18)
        self.show(VGroup(hidden, cover, cover_label, forward, observed, reverse,
                         label("inverse problem", 21, PRUNE).move_to([0, -2.35, 0])))
        self.to(49)

        # 8 — Name identifiability.
        self.copy(
            "숨은 구조를 유일하게 알아낼 수 있는가", "IDENTIFIABILITY  ·  식별 가능성",
            "같은 관측으로 들어오는 설명이 여럿이라면\n숨은 원인은 아직 식별되지 않았습니다.",
        )
        causes = VGroup(
            card("z⁽¹⁾", WEIGHT, 1.45, .68, 22, .1),
            card("z⁽²⁾", SPARSE, 1.45, .68, 22, .1),
            card("z⁽³⁾", PRUNE, 1.45, .68, 22, .1),
        ).arrange(DOWN, buff=.42).move_to([-2.25, .35, 0])
        target = card("same h", ACCENT, 2.5, .95, 27, .16).move_to([2.2, .35, 0])
        links = VGroup(*[
            Arrow(cause.get_right(), target.get_left(), buff=.08,
                  color=FEATURE_COLORS[(0, 3, 1)[i]], stroke_width=3, tip_length=.15)
            for i, cause in enumerate(causes)
        ])
        term = card("IDENTIFIABILITY", ACCENT, 5.2, .9, 29, .17).move_to([0, -2.75, 0])
        self.show(VGroup(causes, links, target, term))
        self.to(56)

        # 9 — One activation cloud, multiple coordinate systems.
        self.copy(
            "왜 우리가 찾은 방향이 특별할까요?", "SAME DATA  ·  MULTIPLE FEATURE SYSTEMS",
            "같은 activation cloud를 여러 좌표계가 설명하면\n추가 조건이 필요합니다.",
        )
        cloud = self.activation_cloud(20, 1.35)
        frames = VGroup(
            self.rotated_basis(0, WEIGHT),
            self.rotated_basis(28, SPARSE),
            self.rotated_basis(-35, PRUNE),
        )
        self.show(VGroup(cloud, frames,
                         card("Which basis is special?", ACCENT, 4.9, .8, 24, .14)
                         .move_to([0, -2.75, 0])))
        self.to(63)

        # 10 — Sparsity selects among explanations; SAE stays minimal.
        self.copy(
            "가능한 설명에 조건을 추가합니다", "PREFER A SPARSE EXPLANATION",
            "Sparse Autoencoder는 잘 복원하는 설명 중\n적은 latent를 쓰는 분해를 선호합니다.",
        )
        candidates = VGroup(
            self.usage_card("A", 8, WEIGHT),
            self.usage_card("B", 6, SPARSE),
            self.usage_card("C", 2, GOOD),
        ).arrange(RIGHT, buff=.35).move_to([0, .65, 0])
        pipeline = VGroup(
            card("h", INK, .75, .65, 23, .08),
            label("→", 25, MUTED),
            card("sparse z", GOOD, 2.1, .65, 21, .13),
            label("→", 25, MUTED),
            card("ĥ", INK, .75, .65, 23, .08),
        ).arrange(RIGHT, buff=.25).move_to([0, -1.65, 0])
        self.show(VGroup(candidates, pipeline,
                         label("Sparse Autoencoder", 20, ACCENT).move_to([0, -2.55, 0])))
        self.to(70)

        # 11 — The crucial inferential structure.
        self.copy(
            "정답을 읽은 것이 아니라 설명을 선택했습니다", "INDUCTIVE BIAS",
            "관측에 sparsity라는 가정을 더해\n가능한 설명 중 하나를 선택했습니다.",
        )
        statement = VGroup(
            card("Observation", WEIGHT, 2.3, .82, 23, .12),
            label("+", 30, ACCENT),
            card("Assumption", PRUNE, 2.3, .82, 23, .12),
            label("→", 30, ACCENT),
            card("Explanation", GOOD, 2.4, .82, 23, .12),
        ).arrange(RIGHT, buff=.18).move_to([0, .5, 0])
        assumption = card("sparsity", PRUNE, 2.5, .7, 21, .14).move_to([0, -1.2, 0])
        pointer = Arrow([0, -.75, 0], [0, -.2, 0], buff=0,
                        color=PRUNE, stroke_width=3, tip_length=.15)
        caution = card("preference  ≠  proof", ACCENT, 4.6, .78, 24, .14).move_to([0, -2.75, 0])
        self.show(VGroup(statement, assumption, pointer, caution))
        self.to(77)

        # 12 — Discovery versus induced structure.
        self.copy(
            "원래 sparse했던 걸까요?", "TWO POSSIBILITIES",
            "실제 sparse 구조를 발견했을 수도,\n요구한 조건 때문에 sparse해졌을 수도 있습니다.",
        )
        left = self.possibility_panel("A", "DISCOVERED", "model was sparse", GOOD)
        left.move_to([-2.05, .25, 0])
        right = self.possibility_panel("B", "SELECTED", "we required sparse", PRUNE)
        right.move_to([2.05, .25, 0])
        versus = card("OR", ACCENT, 1.0, .7, 22, .12)
        self.show(VGroup(left, right, versus,
                         card("both fit the observation", MUTED, 4.8, .72, 20, .07)
                         .move_to([0, -2.8, 0])))
        self.to(84)

        # 13 — Predictive explanation is not automatically mechanism.
        self.copy(
            "좋은 설명과 실제 메커니즘은 다릅니다", "EXPLANATION  ≠  MECHANISM",
            "모델 동작을 잘 설명하는 표현이\n실제 계산 단위라는 보장은 없습니다.",
        )
        explanation = card("Predicts activation well", WEIGHT, 3.1, 1.25, 22, .13)
        explanation.move_to([-2.1, .35, 0])
        mechanism = card("Model actually uses it", GOOD, 3.1, 1.25, 22, .13)
        mechanism.move_to([2.1, .35, 0])
        broken = label("≠", 52, PRUNE).move_to([0, .35, 0])
        self.show(VGroup(explanation, broken, mechanism,
                         card("descriptive  ≠  causal", ACCENT, 4.8, .78, 24, .14)
                         .move_to([0, -2.75, 0])))
        self.to(91)

        # 14 — Intervention offers stronger evidence.
        self.copy(
            "관찰에서 개입으로", "INTERVENE ON THE DIRECTION",
            "방향을 직접 바꿨을 때 모델 행동도 예상대로 변하면\n더 강한 증거가 됩니다.",
        )
        before = self.output_meter("cat output", .22, MUTED).move_to([2.0, 1.3, 0])
        after = self.output_meter("cat output", .81, GOOD).move_to([2.0, -1.15, 0])
        activation = card("h", INK, 1.0, .78, 26, .08).move_to([-2.55, .9, 0])
        intervention = card("+ α vcat", ACCENT, 2.2, .78, 23, .14).move_to([-2.55, -.15, 0])
        result = card("h'", GOOD, 1.0, .78, 26, .12).move_to([-2.55, -1.2, 0])
        arrows = VGroup(
            Arrow(activation.get_bottom(), intervention.get_top(), buff=.08,
                  color=MUTED, tip_length=.14),
            Arrow(intervention.get_bottom(), result.get_top(), buff=.08,
                  color=ACCENT, tip_length=.14),
            Arrow(result.get_right(), after.get_left(), buff=.14,
                  color=GOOD, stroke_width=3, tip_length=.16),
        )
        self.show(VGroup(before, after, activation, intervention, result, arrows,
                         label("stronger evidence  ·  not a complete proof", 19, MUTED)
                         .move_to([0, -2.75, 0])))
        self.to(98)

        # 15 — Separate the three claims.
        self.copy(
            "세 문장은 서로 다른 주장입니다", "FIT  ·  UNIQUENESS  ·  MECHANISM",
            "관측을 설명하는 것, 설명이 유일한 것,\n실제 메커니즘인 것은 같지 않습니다.",
        )
        ladder = VGroup(
            self.claim_step("1", "Fits the data", WEIGHT, True),
            self.claim_step("2", "Unique explanation", ACCENT, False),
            self.claim_step("3", "Actual mechanism", GOOD, False),
        ).arrange(DOWN, buff=.38).move_to([0, .45, 0])
        links = VGroup(
            Arrow([0, 1.18, 0], [0, .73, 0], buff=0, color=MUTED, tip_length=.13),
            Arrow([0, -.38, 0], [0, -.83, 0], buff=0, color=MUTED, tip_length=.13),
        )
        self.show(VGroup(ladder, links,
                         card("Explanation  ≠  Identification", PRUNE, 5.9, .82, 25, .15)
                         .move_to([0, -2.8, 0])))
        self.to(105)

        # 16 — End on the durable identifiability question.
        self.copy(
            "의미 있어 보이는 구조는 시작일 뿐입니다", "IDENTIFIABILITY",
            "그 구조를 발견한 걸까요,\n아니면 설명 하나를 선택한 걸까요?",
        )
        origin = np.array([0, .65, 0])
        candidates = VGroup()
        for i, angle in enumerate((12, 48, 94, 143, 205, 258, 315)):
            rad = angle * DEGREES
            candidates.add(Arrow(origin, origin + np.array([2.1 * np.cos(rad), 2.1 * np.sin(rad), 0]),
                                 buff=.04, color=FEATURE_COLORS[i % 5],
                                 stroke_width=3, stroke_opacity=.38, tip_length=.15))
        selected = candidates[1].copy().set_stroke(opacity=1, width=6)
        mark = label("?", 58, ACCENT).next_to(selected.get_end(), UP, buff=.15)
        final = card("Did we discover the feature,\nor choose an explanation?",
                     ACCENT, 7.0, 1.25, 25, .17).move_to([0, -2.7, 0])
        self.show(VGroup(candidates, selected, mark, final))
        self.to(112)

    def feature_space(self, radius=2.0, five=True):
        axes = VGroup(
            Line([-radius * 1.15, 0, 0], [radius * 1.15, 0, 0], color=MUTED, stroke_opacity=.3),
            Line([0, -radius * 1.15, 0], [0, radius * 1.15, 0], color=MUTED, stroke_opacity=.3),
        )
        angles = (12, 62, 145, 225, 310) if five else (15, 125, 285)
        rays = VGroup(*[
            Arrow(ORIGIN, [radius * np.cos(a * DEGREES), radius * np.sin(a * DEGREES), 0],
                  buff=.04, color=FEATURE_COLORS[i], stroke_width=4, tip_length=.17)
            for i, a in enumerate(angles)
        ])
        return VGroup(axes, rays)

    def activation_cloud(self, count=16, scale=1.0):
        offsets = ((-1.2, -.7), (-.95, .15), (-.8, .75), (-.45, -.45),
                   (-.35, .35), (-.15, 1.0), (.1, -.85), (.2, -.05),
                   (.4, .55), (.65, -.55), (.75, .1), (.95, .8),
                   (1.2, -.15), (1.35, .45), (-1.35, .45), (.0, .72),
                   (-.65, -1.0), (1.0, -1.0), (-1.05, 1.05), (.55, 1.05))
        points = VGroup(*[
            Dot([x * scale, y * scale, 0], radius=.085,
                color=FEATURE_COLORS[i % 5], fill_opacity=.65)
            for i, (x, y) in enumerate(offsets[:count])
        ])
        frame = Ellipse(width=3.5 * scale, height=3.0 * scale,
                        color=ZERO, fill_color=ZERO, fill_opacity=.025)
        return VGroup(frame, points)

    def feature_tag(self, symbol, meaning, color):
        vector = Arrow(ORIGIN, RIGHT * .75, buff=0, color=color,
                       stroke_width=4, tip_length=.16)
        return VGroup(card(symbol, color, 1.0, .65, 20, .1), vector,
                      card(meaning, color, 1.7, .65, 20, .1)).arrange(RIGHT, buff=.22)

    def decomposition_panel(self, title, angles, colors):
        box = RoundedRectangle(width=3.45, height=4.55, corner_radius=.22,
                               color=ZERO, fill_color=ZERO, fill_opacity=.035)
        name = label(title, 19, MUTED).move_to([0, 1.75, 0])
        origin = np.array([0, -.15, 0])
        rays = VGroup(*[
            Arrow(origin, origin + np.array([1.15 * np.cos(a * DEGREES),
                                              1.15 * np.sin(a * DEGREES), 0]),
                  buff=.03, color=colors[i], stroke_width=4, tip_length=.15)
            for i, a in enumerate(angles)
        ])
        h = Dot(origin + np.array([.75, .95, 0]), radius=.11, color=ACCENT)
        error = label("error ≈ 0", 18, GOOD).move_to([0, -1.72, 0])
        return VGroup(box, name, rays, h, error)

    def answer_panel(self, name, formula, color):
        box = RoundedRectangle(width=3.25, height=4.4, corner_radius=.24,
                               color=color, fill_color=color, fill_opacity=.055,
                               stroke_width=3)
        name_tag = card(name, color, .9, .7, 25, .18).move_to([0, 1.55, 0])
        rays = VGroup(*[
            Arrow(ORIGIN, [1.05 * np.cos(a * DEGREES), 1.05 * np.sin(a * DEGREES), 0],
                  buff=.03, color=FEATURE_COLORS[(i + (0 if name == "A" else 2)) % 5],
                  stroke_width=3.5, tip_length=.14)
            for i, a in enumerate((15, 120, 285) if name == "A" else (45, 175, 320))
        ]).move_to([0, .15, 0])
        formula_text = label(formula, 19, color).move_to([0, -1.2, 0])
        error = label("error ≈ 0", 18, GOOD).move_to([0, -1.75, 0])
        return VGroup(box, name_tag, rays, formula_text, error)

    def axes_panel(self, name, color):
        box = RoundedRectangle(width=3.45, height=4.5, corner_radius=.22,
                               color=ZERO, fill_color=ZERO, fill_opacity=.025)
        axes = VGroup(
            Line([-1.35, 0, 0], [1.35, 0, 0], color=MUTED, stroke_opacity=.45),
            Line([0, -1.35, 0], [0, 1.35, 0], color=MUTED, stroke_opacity=.45),
        ).move_to([0, .25, 0])
        tag = card(name, color, 1.7, .65, 21, .12).move_to([0, 1.65, 0])
        target = Dot([1.0, 1.25, 0], radius=.1, color=ACCENT)
        return VGroup(box, axes, tag, target)

    def rotated_basis(self, angle, color):
        rad = angle * DEGREES
        ex = np.array([2.0 * np.cos(rad), 2.0 * np.sin(rad), 0])
        ey = np.array([-2.0 * np.sin(rad), 2.0 * np.cos(rad), 0])
        return VGroup(
            Line(-ex, ex, color=color, stroke_width=2.5, stroke_opacity=.62),
            Line(-ey, ey, color=color, stroke_width=2.5, stroke_opacity=.62),
        )

    def usage_card(self, name, active, color):
        box = RoundedRectangle(width=2.2, height=4.0, corner_radius=.2,
                               color=color, fill_color=color, fill_opacity=.035)
        title = label(name, 23, color).move_to([0, 1.45, 0])
        cells = VGroup()
        for i in range(8):
            on = i < active
            cells.add(RoundedRectangle(width=.62, height=.43, corner_radius=.08,
                                       color=color if on else ZERO,
                                       fill_color=color if on else ZERO,
                                       fill_opacity=.55 if on else .05))
        cells.arrange_in_grid(rows=4, cols=2, buff=.16).move_to([0, .05, 0])
        count = label(f"{active} active", 18, GOOD if active == 2 else MUTED).move_to([0, -1.48, 0])
        return VGroup(box, title, cells, count)

    def possibility_panel(self, name, title, subtitle, color):
        box = RoundedRectangle(width=3.45, height=4.45, corner_radius=.22,
                               color=color, fill_color=color, fill_opacity=.035)
        badge = card(name, color, .9, .65, 22, .14).move_to([0, 1.6, 0])
        heading = label(title, 22, color).move_to([0, .75, 0])
        icon = VGroup(*[
            Rectangle(width=.32, height=.35 + .18 * value,
                      color=color if value else ZERO,
                      fill_color=color if value else ZERO,
                      fill_opacity=.7 if value else .04)
            for value in (0, 0, 1, 0, 1, 0, 0)
        ]).arrange(RIGHT, buff=.11).move_to([0, -.2, 0])
        sub = label(subtitle, 18, MUTED).move_to([0, -1.55, 0])
        return VGroup(box, badge, heading, icon, sub)

    def output_meter(self, name, value, color):
        title = label(name, 19, color)
        track = RoundedRectangle(width=3.3, height=.42, corner_radius=.11,
                                 color=ZERO, fill_color=ZERO, fill_opacity=.12)
        fill = RoundedRectangle(width=max(.15, 3.0 * value), height=.27, corner_radius=.08,
                                stroke_width=0, fill_color=color, fill_opacity=.9)
        fill.align_to(track, LEFT).shift(RIGHT * .12)
        number = label(f"{value:.2f}", 18, color)
        return VGroup(title, VGroup(track, fill), number).arrange(DOWN, buff=.17)

    def claim_step(self, number, text, color, checked):
        badge = Circle(radius=.29, color=color, fill_color=color, fill_opacity=.13)
        n = label(number, 18, color).move_to(badge)
        statement = card(text, color, 4.4, .72, 22, .11)
        status = label("✓" if checked else "?", 28, GOOD if checked else ACCENT)
        return VGroup(VGroup(badge, n), statement, status).arrange(RIGHT, buff=.3)

    def copy(self, heading, note, caption):
        old = VGroup(self.heading, self.note, self.caption, self.caption_box)
        if len(old):
            self.play(FadeOut(old), run_time=.1)
        self.heading = label(heading, 29).move_to(UP * 5.12)
        self.note = label(note, 20, ACCENT).move_to(DOWN * 4.45)
        self.caption_box = RoundedRectangle(
            width=7.65, height=1.15, corner_radius=.14,
            stroke_color=ZERO, stroke_width=1.2,
            fill_color=ZERO, fill_opacity=.32,
        ).move_to([0, -5.65, 0])
        self.caption = label(caption, 19, INK, 7.2).move_to(self.caption_box)
        self.play(FadeIn(self.heading), FadeIn(self.note),
                  FadeIn(self.caption_box), FadeIn(self.caption), run_time=.2)

    def show(self, new_stage):
        if len(self.stage):
            self.play(FadeOut(self.stage), run_time=.18)
        self.stage = new_stage
        self.play(FadeIn(self.stage, shift=UP * .12), run_time=.4)

    def to(self, target):
        remaining = target - self.time
        if remaining < -.04:
            raise ValueError(f"Timeline overrun at {target}: {self.time:.2f}")
        end_x = -3.8 + max(.01, 7.6 * target / self.DURATION)
        if remaining > 0:
            self.play(self.progress.animate.put_start_and_end_on(
                np.array([-3.8, -7.36, 0]), np.array([end_x, -7.36, 0])),
                run_time=min(.25, remaining))
            self.wait(max(0, target - self.time))
