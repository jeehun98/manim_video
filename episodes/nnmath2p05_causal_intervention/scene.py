"""Neural Network Mathematics Part 2, episode 05: Causal intervention."""
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import (
    ACCENT, BG, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, ZERO, txt,
)


def label(value, size=27, color=INK, width=7.6, weight=NORMAL):
    return txt(value, size, color, width, weight)


def card(value, color=WEIGHT, width=3.0, height=.86, size=23, fill=.1):
    box = RoundedRectangle(
        width=width, height=height, corner_radius=.16,
        stroke_color=color, stroke_width=2,
        fill_color=color, fill_opacity=fill,
    )
    return VGroup(box, label(value, size, color, width - .24))


def route(points, color=MUTED, width=3, opacity=.65):
    line = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity)
    line.set_points_as_corners([np.array(p, dtype=float) for p in points])
    return line


def feature_token(value="v", color=ACCENT, radius=.28):
    circle = Circle(radius=radius, color=color, stroke_width=2.5,
                    fill_color=BG, fill_opacity=1)
    return VGroup(circle, label(value, 20, color).move_to(circle))


def probability_meter(name, value, color, center):
    title = label(name, 19, MUTED).move_to(np.array(center) + UP * .52)
    track = RoundedRectangle(width=3.0, height=.46, corner_radius=.12,
                             color=ZERO, fill_color=ZERO, fill_opacity=.16)
    track.move_to(center)
    fill = RoundedRectangle(width=max(.12, 2.72 * value), height=.28,
                            corner_radius=.08, stroke_width=0,
                            fill_color=color, fill_opacity=.9)
    fill.align_to(track, LEFT).shift(RIGHT * .14)
    number = label(f"{value:.2f}", 20, color).move_to(np.array(center) + DOWN * .52)
    return VGroup(title, track, fill, number)


class NeuralMathPart2CausalIntervention(Scene):
    DURATION = 112

    def construct(self):
        self.stage = VGroup()
        self.heading = VGroup()
        self.note = VGroup()
        self.caption = VGroup()
        self.caption_box = VGroup()
        self.chrome = VGroup(
            label("NEURAL NETWORK MATHEMATICS  /  PART 2 · 05", 17, MUTED).move_to(UP * 7.3),
            label("Feature가 진짜인지 직접 지워보면 알 수 있을까?", 27).move_to(UP * 6.45),
            Line([-3.8, 5.82, 0], [3.8, 5.82, 0], color=MUTED, stroke_opacity=.35),
        )
        self.progress = Line([-3.8, -7.36, 0], [-3.79, -7.36, 0],
                             color=ACCENT, stroke_width=4)
        self.add(self.chrome, self.progress)

        # 1 — Bridge from identifiability to intervention.
        self.copy(
            "의미를 붙이는 것만으로 충분할까요?", "OBSERVE  →  INTERVENE",
            "4화에서는 좋은 설명과 실제 메커니즘을 구분했습니다.\n이번에는 내부를 직접 바꿔봅니다.",
        )
        observed = card("v is active", WEIGHT, 2.15, .86, 22, .12).move_to([-2.6, .4, 0])
        action = card("change v", ACCENT, 1.9, .86, 22, .15).move_to([0, .4, 0])
        behavior = card("behavior changes?", GOOD, 2.35, .86, 20, .13).move_to([2.65, .4, 0])
        arrows = VGroup(
            Arrow(observed.get_right(), action.get_left(), buff=.12, color=MUTED, tip_length=.15),
            Arrow(action.get_right(), behavior.get_left(), buff=.12, color=GOOD, tip_length=.15),
        )
        self.show(VGroup(observed, action, behavior, arrows,
                         card("Observation is a clue · Intervention is a test", ACCENT, 6.9, .78, 22, .13)
                         .move_to([0, -2.7, 0])))
        self.to(7)

        # 2 — Wolf and snow correlate in observations.
        self.copy(
            "늑대와 함께 켜지는 방향을 찾았습니다", "WOLF  ↔  v",
            "늑대 사진에서 v가 강하고 다른 사진에서는 약합니다.\n하지만 v가 무엇을 담는지는 아직 모릅니다.",
        )
        wolf = self.image_card("WOLF", "늑대", WEIGHT).move_to([-2.25, .65, 0])
        snow = self.image_card("SNOW", "눈밭", SPARSE).move_to([2.25, .65, 0])
        v = feature_token("v", ACCENT, .38).move_to([0, -1.4, 0])
        links = VGroup(
            Arrow(wolf.get_bottom(), v.get_left(), buff=.12, color=WEIGHT, tip_length=.15),
            Arrow(snow.get_bottom(), v.get_right(), buff=.12, color=SPARSE, tip_length=.15),
        )
        self.show(VGroup(wolf, snow, v, links,
                         card("co-occur in the data", MUTED, 4.4, .72, 21, .08).move_to([0, -2.8, 0])))
        self.to(14)

        # 3 — Two causal stories, shown as parallel routes.
        self.copy(
            "같은 관찰을 두 이야기가 설명합니다", "WHAT DOES v REPRESENT?",
            "v가 늑대 자체를 나타낼 수도 있고,\n늑대와 함께 나온 눈을 나타낼 수도 있습니다.",
        )
        left = self.story_lane("STORY A", "wolf", WEIGHT, "v carries wolf evidence").move_to([-2.05, .3, 0])
        right = self.story_lane("STORY B", "snow", SPARSE, "snow drives prediction").move_to([2.05, .3, 0])
        self.show(VGroup(left, right,
                         card("same correlation · different mechanism", ACCENT, 6.4, .78, 21, .13)
                         .move_to([0, -2.8, 0])))
        self.to(21)

        # 4 — Remove the component by moving a stable token out of the stream.
        self.copy(
            "그러면 v 성분을 직접 지워봅니다", "h' = h − projᵥ(h)",
            "activation에서 v 방향 성분만 제거하고\n나머지 network를 그대로 실행합니다.",
        )
        h = card("activation h", WEIGHT, 2.2, .82, 23, .12).move_to([-2.7, .55, 0])
        gate = card("remove v", PRUNE, 2.0, .82, 23, .15).move_to([0, .55, 0])
        hp = card("h'", GOOD, 1.15, .82, 25, .14).move_to([2.55, .55, 0])
        main_path = route([h.get_right(), gate.get_left(), gate.get_right(), hp.get_left()], GOOD)
        exit_path = route([[0, .12, 0], [0, -1.7, 0], [1.1, -1.7, 0]], PRUNE, 3, .8)
        self.show(VGroup(main_path, exit_path, h, gate, hp,
                         label("keep the rest of the network fixed", 20, MUTED).move_to([0, -2.75, 0])))
        token = feature_token("v", ACCENT).move_to(h.get_right() + LEFT * .12)
        self.add_stage(token)
        self.play(MoveAlongPath(token, exit_path), run_time=1.15)
        self.to(28)

        # 5 — Ablation result.
        self.copy(
            "지웠더니 늑대 확률이 내려갑니다", "REMOVE v",
            "v가 단지 함께 나타난 것이 아니라\n모델의 판단에 영향을 주었다는 더 강한 증거입니다.",
        )
        before = probability_meter("before", .94, WEIGHT, [-1.9, .8, 0])
        after = probability_meter("after removal", .21, PRUNE, [1.9, .8, 0])
        minus = feature_token("−v", PRUNE, .42).move_to([0, -1.2, 0])
        self.show(VGroup(before, after, minus,
                         Arrow(before.get_right(), after.get_left(), buff=.18,
                               color=PRUNE, stroke_width=4, tip_length=.18),
                         card("P(wolf): 0.94  →  0.21", PRUNE, 5.0, .78, 25, .14)
                         .move_to([0, -2.8, 0])))
        self.to(35)

        # 6 — Add the same direction.
        self.copy(
            "반대로 v를 더해볼 수도 있습니다", "h' = h + αv",
            "애매한 activation에 v를 더했을 때\n늑대 판단이 강해지는지 확인합니다.",
        )
        before = probability_meter("before", .31, MUTED, [-1.9, .8, 0])
        after = probability_meter("after addition", .78, GOOD, [1.9, .8, 0])
        plus = feature_token("+v", GOOD, .42).move_to([0, -1.2, 0])
        self.show(VGroup(before, after, plus,
                         Arrow(before.get_right(), after.get_left(), buff=.18,
                               color=GOOD, stroke_width=4, tip_length=.18),
                         card("P(wolf): 0.31  →  0.78", GOOD, 5.0, .78, 25, .14)
                         .move_to([0, -2.8, 0])))
        self.to(42)

        # 7 — Hero comparison: necessity and sufficiency.
        self.copy(
            "제거와 추가는 서로 다른 질문입니다", "NECESSITY  /  SUFFICIENCY",
            "없앴을 때 행동이 사라지는가,\n넣었을 때 행동이 나타나는가를 나눠 묻습니다.",
        )
        remove_panel = self.test_panel("REMOVE v", "behavior ↓", "necessary?", PRUNE)
        remove_panel.move_to([-2.05, .35, 0])
        add_panel = self.test_panel("ADD v", "behavior ↑", "sufficient?", GOOD)
        add_panel.move_to([2.05, .35, 0])
        self.show(VGroup(remove_panel, add_panel,
                         card("correlation  <  intervention evidence", ACCENT, 6.7, .82, 23, .16)
                         .move_to([0, -2.8, 0])))
        self.to(49)

        # 8 — Intervention can be performed at several levels.
        self.copy(
            "개입은 여러 수준에서 할 수 있습니다", "ABLATION / PATCHING / STEERING",
            "뉴런, attention head, feature 방향,\nactivation 값 자체를 바꿀 수 있습니다.",
        )
        levels = VGroup(
            self.level_card("NEURON", "hᵢ ← 0", WEIGHT),
            self.level_card("HEAD", "remove", SPARSE),
            self.level_card("DIRECTION", "−projᵥ", PRUNE),
            self.level_card("ACTIVATION", "replace", GOOD),
        ).arrange_in_grid(rows=2, cols=2, buff=.38).move_to([0, .3, 0])
        self.show(VGroup(levels,
                         label("Manipulate  →  Run forward  →  Observe consequence", 20, ACCENT)
                         .move_to([0, -2.75, 0])))
        self.to(56)

        # 9 — The conceptual upgrade from observation to manipulation.
        self.copy(
            "관찰에서 조작으로 질문이 바뀝니다", "MANIPULATE  →  CONSEQUENCE",
            "무엇과 함께 켜지는지가 아니라\n그 값을 바꿨을 때 무엇이 달라지는지 봅니다.",
        )
        top = self.flow_row("OBSERVE", ("input", "v active", "wolf"), WEIGHT).move_to([0, 1.35, 0])
        bottom = self.flow_row("INTERVENE", ("input", "change v", "new output"), GOOD).move_to([0, -1.2, 0])
        self.show(VGroup(top, bottom,
                         card("a stronger test of causal relevance", GOOD, 5.7, .72, 21, .13)
                         .move_to([0, -2.95, 0])))
        self.to(63)

        # 10 — Redundant routes make a negative ablation ambiguous.
        self.copy(
            "그런데 지워도 결과가 그대로일 수 있습니다", "REDUNDANT PATHS",
            "같은 정보가 두 경로로 전달되면\n한 경로를 막아도 다른 경로가 대신합니다.",
        )
        source = card("A", WEIGHT, .9, .72, 24, .13).move_to([-3.0, .25, 0])
        mid = card("B", SPARSE, .9, .72, 24, .13).move_to([0, -1.15, 0])
        target = card("C", GOOD, .9, .72, 24, .13).move_to([3.0, .25, 0])
        upper = route([source.get_right(), [-.8, 1.35, 0], [.8, 1.35, 0], target.get_left()], PRUNE, 4)
        lower = route([source.get_right(), mid.get_left(), mid.get_right(), target.get_left()], GOOD, 4)
        block = VGroup(Line([-.25, 1.7, 0], [.25, 1.0, 0], color=PRUNE, stroke_width=7),
                       Line([-.25, 1.0, 0], [.25, 1.7, 0], color=PRUNE, stroke_width=7))
        self.show(VGroup(upper, lower, source, mid, target, block,
                         card("output unchanged", GOOD, 3.4, .72, 22, .12).move_to([0, -2.8, 0])))
        moving = feature_token("i", GOOD, .22).move_to(source.get_right())
        self.add_stage(moving)
        self.play(MoveAlongPath(moving, lower), run_time=1.25)
        self.play(FadeOut(moving), run_time=.15)
        self.to(70)

        # 11 — No-effect is not evidence of non-use.
        self.copy(
            "효과가 없다는 결론도 조심해야 합니다", "NO EFFECT  ≠  NOT USED",
            "ablation 뒤 변화가 없더라도\n중복 경로가 가린 것일 수 있습니다.",
        )
        left = card("Ablate path 1", PRUNE, 2.8, 1.0, 23, .14).move_to([-2.2, .55, 0])
        right = card("Output unchanged", GOOD, 3.1, 1.0, 22, .14).move_to([2.15, .55, 0])
        self.show(VGroup(left, right,
                         Arrow(left.get_right(), right.get_left(), buff=.15, color=MUTED, tip_length=.16),
                         label("≠", 58, ACCENT).move_to([0, -1.0, 0]),
                         card("the path carried no useful information", MUTED, 6.4, .8, 21, .08)
                         .move_to([0, -2.35, 0])))
        self.to(77)

        # 12 — Excessive interventions leave the activation distribution.
        self.copy(
            "너무 크게 바꾸면 다른 문제가 생깁니다", "OFF-DISTRIBUTION INTERVENTION",
            "학습 중 거의 보지 못한 activation으로 보내면\n출력 변화가 단순한 고장일 수 있습니다.",
        )
        cloud = self.activation_cloud().move_to([-1.45, .35, 0])
        outlier = Cross(stroke_color=PRUNE, stroke_width=7).scale(.28).move_to([2.65, .55, 0])
        shift_path = route([[-.5, .35, 0], [.7, .35, 0], [2.65, .55, 0]], PRUNE, 4, .85)
        self.show(VGroup(cloud, outlier, shift_path,
                         label("normal activations", 20, MUTED).move_to([-1.45, -1.75, 0]),
                         label("unfamiliar state", 20, PRUNE).move_to([2.55, -1.0, 0]),
                         card("output changed · cause still ambiguous", ACCENT, 6.3, .78, 21, .13)
                         .move_to([0, -2.8, 0])))
        mover = feature_token("h", WEIGHT, .23).move_to([-.5, .35, 0])
        self.add_stage(mover)
        self.play(MoveAlongPath(mover, shift_path), run_time=1.2)
        self.to(84)

        # 13 — Compare a controlled change with an excessive one.
        self.copy(
            "개입의 크기와 비교 조건이 중요합니다", "CONTROLLED  /  TOO LARGE",
            "작은 변화의 일관된 효과와\n범위를 벗어난 큰 충격을 구분해야 합니다.",
        )
        controlled = self.range_panel("CONTROLLED", .55, GOOD, "near data").move_to([-2.05, .25, 0])
        excessive = self.range_panel("TOO LARGE", 1.55, PRUNE, "off distribution").move_to([2.05, .25, 0])
        self.show(VGroup(controlled, excessive,
                         card("dose · controls · matched baselines", ACCENT, 6.2, .76, 21, .13)
                         .move_to([0, -2.8, 0])))
        self.to(91)

        # 14 — Superposition means removing v can change more than one feature.
        self.copy(
            "한 방향이 한 의미만 담는다는 보장도 없습니다", "SUPERPOSITION RETURNS",
            "v를 지웠을 때 늑대 정보뿐 아니라\n겹쳐 있던 다른 정보도 함께 바뀔 수 있습니다.",
        )
        before = self.direction_bundle("BEFORE", (1.0, .85, .7)).move_to([-2.05, .35, 0])
        after = self.direction_bundle("REMOVE v", (.1, .35, .15)).move_to([2.05, .35, 0])
        self.show(VGroup(before, after,
                         Arrow(before.get_right(), after.get_left(), buff=.12, color=PRUNE, tip_length=.17),
                         card("one intervention · several changed signals", PRUNE, 6.5, .78, 21, .13)
                         .move_to([0, -2.8, 0])))
        self.to(98)

        # 15 — Intervention is stronger, not final proof.
        self.copy(
            "개입은 더 강한 증거지만 마지막 답은 아닙니다", "EVIDENCE, NOT CERTAINTY",
            "중복, 범위 이탈, feature 얽힘을 통제해야\n인과적 해석이 더 설득력을 얻습니다.",
        )
        ladder = VGroup(
            card("1  Correlation", MUTED, 5.4, .7, 22, .08),
            card("2  Reconstruction", WEIGHT, 5.4, .7, 22, .11),
            card("3  Controlled intervention", GOOD, 5.4, .7, 22, .15),
        ).arrange(DOWN, buff=.34).move_to([0, .65, 0])
        self.show(VGroup(ladder,
                         card("Intervention worked  ≠  unique mechanism found", ACCENT, 7.0, .82, 22, .16)
                         .move_to([0, -2.55, 0])))
        self.to(105)

        # 16 — Lead into circuits.
        self.copy(
            "다음에는 방향이 아니라 계산 경로를 봅니다", "FROM FEATURES TO CIRCUITS",
            "하나의 feature보다 입력에서 출력까지\n어떤 구성요소들이 함께 계산하는지 묻습니다.",
        )
        nodes = VGroup(*[
            Circle(radius=.25, color=(WEIGHT, SPARSE, PRUNE, GOOD, ACCENT)[i],
                   fill_color=BG, fill_opacity=1, stroke_width=3)
            for i in range(5)
        ])
        positions = ([-3, .5, 0], [-1.5, 1.5, 0], [-1.3, -.8, 0], [.6, .45, 0], [2.8, .45, 0])
        for node, position in zip(nodes, positions):
            node.move_to(position)
        paths = VGroup(
            Arrow(nodes[0].get_right(), nodes[1].get_left(), buff=.08, color=MUTED, tip_length=.13),
            Arrow(nodes[0].get_right(), nodes[2].get_left(), buff=.08, color=MUTED, tip_length=.13),
            Arrow(nodes[1].get_right(), nodes[3].get_left(), buff=.08, color=SPARSE, tip_length=.13),
            Arrow(nodes[2].get_right(), nodes[3].get_left(), buff=.08, color=PRUNE, tip_length=.13),
            Arrow(nodes[3].get_right(), nodes[4].get_left(), buff=.08, color=GOOD, tip_length=.13),
        )
        self.show(VGroup(paths, nodes,
                         card("Which computation path causes the behavior?", ACCENT, 6.9, .86, 23, .16)
                         .move_to([0, -2.7, 0])))
        self.to(112)

    def image_card(self, title, subtitle, color):
        box = RoundedRectangle(width=3.1, height=3.2, corner_radius=.22,
                               color=color, fill_color=color, fill_opacity=.05, stroke_width=3)
        icon = VGroup(
            Circle(radius=.5, color=color, fill_color=color, fill_opacity=.15),
            VGroup(*[Line(ORIGIN, .7 * np.array([np.cos(a), np.sin(a), 0]),
                          color=color, stroke_width=2) for a in np.linspace(0, TAU, 8, endpoint=False)])
        ).move_to([0, .3, 0])
        return VGroup(box, label(title, 25, color).move_to([0, 1.15, 0]), icon,
                      label(subtitle, 20, MUTED).move_to([0, -1.15, 0]))

    def story_lane(self, title, cue, color, detail):
        box = RoundedRectangle(width=3.55, height=4.2, corner_radius=.22,
                               color=color, fill_color=color, fill_opacity=.04, stroke_width=2.5)
        source = card(cue, color, 1.55, .7, 22, .12).move_to([0, .65, 0])
        v = feature_token("v", color, .26).move_to([0, -.35, 0])
        output = card("wolf prediction", GOOD, 2.6, .68, 19, .1).move_to([0, -1.3, 0])
        arrows = VGroup(
            Arrow(source.get_bottom(), v.get_top(), buff=.08, color=color, tip_length=.13),
            Arrow(v.get_bottom(), output.get_top(), buff=.08, color=GOOD, tip_length=.13),
        )
        return VGroup(box, label(title, 20, color).move_to([0, 1.6, 0]), source, v, output, arrows,
                      label(detail, 16, MUTED).move_to([0, -1.75, 0]))

    def test_panel(self, title, effect, question, color):
        box = RoundedRectangle(width=3.55, height=4.25, corner_radius=.22,
                               color=color, fill_color=color, fill_opacity=.05, stroke_width=3)
        token = feature_token("v", color, .34).move_to([0, .65, 0])
        sign = label("−" if "REMOVE" in title else "+", 40, color).move_to([0, 1.45, 0])
        return VGroup(box, label(title, 23, color).move_to([0, 1.7, 0]), sign, token,
                      card(effect, color, 2.7, .72, 21, .13).move_to([0, -.55, 0]),
                      label(question, 22, ACCENT).move_to([0, -1.55, 0]))

    def level_card(self, title, operation, color):
        box = RoundedRectangle(width=3.15, height=2.05, corner_radius=.2,
                               color=color, fill_color=color, fill_opacity=.05, stroke_width=2.5)
        return VGroup(box, label(title, 21, color).move_to([0, .5, 0]),
                      label(operation, 25, INK).move_to([0, -.35, 0]))

    def flow_row(self, title, values, color):
        items = VGroup(*[card(v, color if i == 1 else WEIGHT, 1.5, .7, 17, .1)
                         for i, v in enumerate(values)])
        arrows = VGroup(label("→", 23, MUTED), label("→", 23, MUTED))
        row = VGroup(items[0], arrows[0], items[1], arrows[1], items[2]).arrange(RIGHT, buff=.16)
        tag = card(title, color, 1.35, .6, 16, .12).next_to(row, LEFT, buff=.18)
        return VGroup(tag, row)

    def activation_cloud(self):
        offsets = ((-1.2, -.55), (-1.0, .15), (-.75, .72), (-.45, -.35),
                   (-.2, .35), (.05, -.7), (.2, .8), (.55, .25),
                   (.75, -.25), (1.0, .55), (1.2, -.55), (.45, -.95))
        dots = VGroup(*[Dot([x, y, 0], radius=.095,
                            color=(WEIGHT, SPARSE, GOOD)[i % 3], fill_opacity=.7)
                        for i, (x, y) in enumerate(offsets)])
        frame = Ellipse(width=3.4, height=2.8, color=ZERO,
                        fill_color=ZERO, fill_opacity=.04)
        return VGroup(frame, dots)

    def range_panel(self, title, distance, color, subtitle):
        box = RoundedRectangle(width=3.55, height=4.25, corner_radius=.22,
                               color=color, fill_color=color, fill_opacity=.04, stroke_width=2.5)
        cloud = self.activation_cloud().scale(.55).move_to([-.35, .15, 0])
        start = cloud.get_center()
        end = start + RIGHT * distance
        arrow = Arrow(start, end, buff=.04, color=color, stroke_width=4, tip_length=.16)
        return VGroup(box, label(title, 22, color).move_to([0, 1.65, 0]), cloud, arrow,
                      label(subtitle, 19, MUTED).move_to([0, -1.65, 0]))

    def direction_bundle(self, title, strengths):
        box = RoundedRectangle(width=3.55, height=4.2, corner_radius=.22,
                               color=ZERO, fill_color=ZERO, fill_opacity=.035)
        origin = np.array([0, -.25, 0])
        colors = (WEIGHT, PRUNE, GOOD)
        angles = (18, 78, 142)
        rays = VGroup(*[
            Arrow(origin, origin + strength * 1.35 * np.array([np.cos(a * DEGREES), np.sin(a * DEGREES), 0]),
                  buff=.03, color=color, stroke_width=4, tip_length=.15)
            for strength, a, color in zip(strengths, angles, colors)
        ])
        return VGroup(box, label(title, 22, ACCENT).move_to([0, 1.55, 0]), rays,
                      label("wolf · snow · texture", 18, MUTED).move_to([0, -1.55, 0]))

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
            self.remove(self.stage)
        self.stage = new_stage
        self.add(self.stage)
        self.play(FadeIn(self.stage, shift=UP * .12), run_time=.4)

    def add_stage(self, *objects):
        self.stage.add(*objects)

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
