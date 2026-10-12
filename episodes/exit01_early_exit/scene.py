"""Dynamic inference 01: Early Exit changes executed depth per input."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import ACCENT, GOOD, INK, MUTED, PRUNE, WEIGHT, ZERO, pill, txt

ASSETS = Path(__file__).resolve().parent / "assets"


def photo(name, label, color=ACCENT, size=1.35):
    image = ImageMobject(str(ASSETS / name)).scale_to_fit_width(size)
    frame = RoundedRectangle(width=size + .12, height=size + .12, corner_radius=.14,
                             stroke_color=color, stroke_width=2)
    caption = txt(label, 18, color).next_to(frame, DOWN, buff=.13)
    return Group(image, frame, caption)


def layers(count=12, width=.49, y=0):
    row = VGroup()
    for i in range(count):
        box = RoundedRectangle(width=width, height=.68, corner_radius=.08,
                               stroke_color=WEIGHT, stroke_width=1.3,
                               fill_color=WEIGHT, fill_opacity=.08)
        row.add(VGroup(box, txt(str(i + 1), 15, MUTED)))
    row.arrange(RIGHT, buff=.11).move_to([0, y, 0])
    return row


def path_on(row, depth, color, offset=0):
    marks = VGroup()
    centers = [cell.get_center() + UP * offset for cell in row[:depth]]
    for a, b in zip(centers, centers[1:]):
        marks.add(Arrow(a, b, buff=.2, color=color, stroke_width=2.5, tip_length=.09))
    marks.add(*[Dot(p, radius=.07, color=color) for p in centers])
    return marks


class EarlyExit(Scene):
    DURATION = 82

    def construct(self):
        self.head = VGroup(); self.sub = VGroup(); self.note = VGroup()
        self.chrome = VGroup(
            txt("DYNAMIC INFERENCE  /  01", 20, MUTED).move_to(UP * 7.25),
            txt("모든 입력이 신경망의 끝까지 갈 필요가 있을까?", 30).move_to(UP * 6.45),
            Line([-3.8, 5.8, 0], [3.8, 5.8, 0], color=MUTED, stroke_opacity=.3),
        )
        self.add(self.chrome)
        self.progress = Rectangle(width=.01, height=.035, fill_color=ACCENT,
                                  fill_opacity=1, stroke_width=0).move_to([-3.8, -7.35, 0])
        self.add(self.progress)

        # 0-7: different inputs, identical full-depth route.
        self.text("난이도는 달라도 계산 경로는 같습니다",
                  "선명한 입력도, 애매한 입력도, 흐릿한 입력도\n일반적인 모델에서는 모든 Layer를 통과합니다.",
                  "3 INPUTS  ·  SAME 12 LAYERS")
        pics = Group(photo("easy_cat.png", "EASY", GOOD, 1.22),
                     photo("ambiguous_animal.png", "AMBIGUOUS", ACCENT, 1.22),
                     photo("blurry_animal.png", "HARD", PRUNE, 1.22))
        pics.arrange(RIGHT, buff=.55).move_to([0, 1.7, 0])
        row = layers(y=-.15)
        routes = VGroup(path_on(row, 12, GOOD, .19), path_on(row, 12, ACCENT, 0),
                        path_on(row, 12, PRUNE, -.19))
        self.play(LaggedStart(*[FadeIn(p, shift=UP*.15) for p in pics], lag_ratio=.1), run_time=.75)
        self.play(FadeIn(row), LaggedStart(*[Create(r) for r in routes], lag_ratio=.12), run_time=1.15)
        self.keep(pics, row, routes); self.to(9)

        # 7-14: easy input is already confident at L4.
        self.text("쉬운 입력은 L4에서 이미 답이 선명합니다",
                  "몇 개의 Layer만 지나도\n고양이라는 예측이 강하게 나타납니다.",
                  "CAT  97%")
        cat = photo("easy_cat.png", "CLEAR INPUT", GOOD, 1.9).move_to([0, 2.0, 0])
        row2 = layers(y=-.2)
        early = path_on(row2, 4, GOOD)
        score = pill("CAT 97%", GOOD, 2.4).move_to([0, -1.55, 0])
        pointer = Arrow(row2[3].get_bottom(), score.get_top(), buff=.12, color=GOOD,
                        stroke_width=3, tip_length=.12)
        self.play(FadeOut(Group(pics, row, routes)), FadeIn(cat), FadeIn(row2), run_time=.7)
        self.play(Create(early), GrowArrow(pointer), FadeIn(score), run_time=.85)
        self.keep(cat, row2, early, pointer, score); self.to(15)

        # 14-20: fixed inference still computes the tail.
        self.text("하지만 일반적인 모델은 계속 계산합니다",
                  "중간 예측이 확실해 보여도\nL12까지 실행한 뒤 최종 답을 냅니다.",
                  "COMPUTE  4 / 12  →  12 / 12")
        tail = path_on(row2, 12, ACCENT)
        counter = txt("12 / 12 LAYERS", 30, ACCENT, weight=BOLD).move_to([0, -1.6, 0])
        self.play(FadeOut(early), FadeOut(pointer), Transform(score, counter),
                  Create(tail), run_time=1.15)
        self.keep(cat, row2, tail, score); self.to(21)

        # 20-26: add a classifier head at L4.
        self.text("중간 표현 옆에 작은 출구를 만듭니다",
                  "L4의 특징으로도 분류할 수 있도록\n작은 Classifier Head를 연결합니다.",
                  "INTERMEDIATE CLASSIFIER  →  EXIT")
        exit_box = VGroup(RoundedRectangle(width=2.25, height=.86, corner_radius=.14,
                                           stroke_color=GOOD, fill_color=GOOD, fill_opacity=.1),
                          txt("EXIT", 25, GOOD, weight=BOLD)).move_to([-1.65, -1.65, 0])
        branch = Arrow(row2[3].get_bottom(), exit_box.get_top(), buff=.1, color=GOOD,
                       stroke_width=3, tip_length=.12)
        clf = txt("classifier", 18, MUTED).next_to(exit_box, DOWN, buff=.16)
        stage = Group(cat, row2, exit_box, branch, clf)
        self.play(FadeOut(tail), FadeOut(score), GrowArrow(branch), FadeIn(exit_box), FadeIn(clf), run_time=.85)
        self.keep(stage); self.to(26)

        # 26-32: easy input exits and the tail turns off.
        self.text("충분히 확실하면 여기서 종료합니다",
                  "쉬운 입력은 L4에서 빠져나가고\n뒤쪽 여덟 Layer는 실행하지 않습니다.",
                  "4 LAYERS USED  ·  8 LAYERS SKIPPED")
        prefix = path_on(row2, 4, GOOD)
        off = VGroup(*row2[4:])
        skip = pill("SKIP L5—L12", PRUNE, 3.1).move_to([1.55, -1.7, 0])
        self.play(Create(prefix), cat.animate.scale(.72).move_to(row2[0].get_center()+UP*1.45), run_time=.75)
        self.play(off.animate.set_opacity(.12), FadeIn(skip), Indicate(exit_box, color=GOOD), run_time=.75)
        self.keep(stage, prefix, skip); self.to(31)

        # 32-39: ambiguous input fails threshold.
        self.text("애매한 입력은 같은 출구를 통과하지 못합니다",
                  "Cat과 Dog 점수가 비슷하면\n중간 예측만으로 결정하기 어렵습니다.",
                  "CAT 48%  ·  DOG 44%  →  CONTINUE")
        amb = photo("ambiguous_animal.png", "AMBIGUOUS", ACCENT, 1.75).move_to([0, 2.0, 0])
        row3 = layers(y=-.2)
        first = path_on(row3, 4, ACCENT)
        bars = VGroup(pill("CAT 48%", ACCENT, 2.2), pill("DOG 44%", PRUNE, 2.2))
        bars.arrange(RIGHT, buff=.4).move_to([0, -1.65, 0])
        cont = txt("CONTINUE →", 24, ACCENT, weight=BOLD).move_to([0, -2.55, 0])
        ambiguous = Group(amb, row3, first, bars, cont)
        self.play(FadeOut(Group(stage, prefix, skip)), FadeIn(amb), FadeIn(row3), Create(first), run_time=.8)
        self.play(FadeIn(bars), FadeIn(cont), run_time=.55)
        self.keep(ambiguous); self.to(38)

        # 39-46: hard input goes deeper and separates.
        self.text("어려운 입력은 더 깊은 계산을 사용합니다",
                  "뒤쪽 Layer를 지나며 특징이 더 정리되고\n두 클래스의 점수가 점차 벌어집니다.",
                  "48 : 44   →   63 : 31   →   91 : 7")
        full = path_on(row3, 12, ACCENT)
        s1 = txt("CAT 48   /   DOG 44", 27, MUTED).move_to([0, -1.55, 0])
        s2 = txt("CAT 63   /   DOG 31", 27, ACCENT).move_to(s1)
        s3 = txt("CAT 91   /   DOG 7", 29, GOOD, weight=BOLD).move_to(s1)
        self.play(FadeOut(first), FadeOut(bars), FadeOut(cont), Create(full), FadeIn(s1), run_time=.85)
        self.play(Transform(s1, s2), run_time=.55); self.play(Transform(s1, s3), run_time=.55)
        self.keep(amb, row3, full, s1); self.to(43)

        # 46-54: same network, different executed depth.
        self.text("같은 모델도 입력마다 실행 깊이가 달라질 수 있습니다",
                  "최대 깊이는 12로 고정되어 있지만\n실제로 사용한 Layer 수는 입력에 따라 달라집니다.",
                  "MODEL DEPTH = 12   ·   EXECUTED DEPTH = 4 OR 12")
        easy = photo("easy_cat.png", "EASY", GOOD, 1.25).move_to([-2.7, 2.0, 0])
        hard = photo("blurry_animal.png", "HARD", PRUNE, 1.25).move_to([-2.7, -.4, 0])
        top = layers(width=.38, y=2.05).scale(.82).shift(RIGHT*.65)
        bottom = layers(width=.38, y=-.35).scale(.82).shift(RIGHT*.65)
        top_path = path_on(top, 4, GOOD); bottom_path = path_on(bottom, 12, PRUNE)
        counts = VGroup(pill("4 LAYERS", GOOD, 2.0).move_to([2.35, 1.1, 0]),
                        pill("12 LAYERS", PRUNE, 2.2).move_to([2.35, -1.3, 0]))
        split = Group(easy, hard, top, bottom, top_path, bottom_path, counts)
        self.play(FadeOut(Group(amb, row3, full, s1)), FadeIn(easy), FadeIn(hard),
                  FadeIn(top), FadeIn(bottom), run_time=.75)
        self.play(Create(top_path), Create(bottom_path), FadeIn(counts), run_time=.75)
        self.keep(split); self.to(52)

        # 54-63: compare optimization questions.
        self.text("Early Exit은 계산 자체의 필요성을 묻습니다",
                  "Quantization은 계산을 작게, Pruning은 Weight를 적게.\nEarly Exit은 뒤의 계산 전체를 건너뜁니다.",
                  "DOES THIS INPUT NEED THIS COMPUTATION?")
        cards = VGroup()
        for title, desc, color in (("QUANTIZATION", "각 계산을 작게", ACCENT),
                                   ("PRUNING", "일부 Weight 제거", PRUNE),
                                   ("EARLY EXIT", "뒤의 계산을 생략", GOOD)):
            box = RoundedRectangle(width=5.9, height=1.12, corner_radius=.16,
                                   stroke_color=color, fill_color=color, fill_opacity=.07)
            cards.add(VGroup(box, txt(title, 20, color).move_to(box.get_center()+LEFT*1.75),
                             txt(desc, 23).move_to(box.get_center()+RIGHT*.9)))
        cards.arrange(DOWN, buff=.3).move_to([0, .4, 0])
        self.play(FadeOut(split), LaggedStart(*[FadeIn(c, shift=LEFT*.15) for c in cards], lag_ratio=.12), run_time=1.0)
        self.play(Indicate(cards[2], color=GOOD, scale_factor=1.03), run_time=.65)
        self.keep(cards); self.to(62)

        # 63-73: threshold tradeoff.
        self.text("출구의 기준에는 Trade-off가 있습니다",
                  "기준이 낮으면 더 많이 줄이지만 오판 위험이 커지고,\n높으면 신중하지만 계산 절감이 작아집니다.",
                  "CONFIDENCE ≥ τ  →  EXIT")
        axis = NumberLine(x_range=[0, 100, 20], length=6.2, include_numbers=False,
                          color=MUTED).move_to([0, .9, 0])
        axis_labels = VGroup(txt("0%", 17, MUTED).next_to(axis.get_left(), DOWN, buff=.16),
                             txt("CONFIDENCE", 17, MUTED).next_to(axis, DOWN, buff=.16),
                             txt("100%", 17, MUTED).next_to(axis.get_right(), DOWN, buff=.16))
        low = Triangle(color=PRUNE, fill_color=PRUNE, fill_opacity=1).scale(.13).rotate(PI)
        low.next_to(axis.n2p(45), UP, buff=.08)
        high = low.copy().set_color(GOOD).next_to(axis.n2p(85), UP, buff=.08)
        tau = txt("τ", 28, PRUNE, weight=BOLD).next_to(low, UP, buff=.1)
        effects = VGroup(pill("LOW τ  →  EXIT ↑  /  RISK ↑", PRUNE, 4.3),
                         pill("HIGH τ →  EXIT ↓  /  CARE ↑", GOOD, 4.3))
        effects.arrange(DOWN, buff=.35).move_to([0, -1.0, 0])
        self.play(FadeOut(cards), Create(axis), FadeIn(axis_labels), FadeIn(low),
                  FadeIn(tau), FadeIn(effects[0]), run_time=.8)
        self.play(Transform(low, high), tau.animate.set_color(GOOD).next_to(high, UP, buff=.1),
                  FadeOut(effects[0]), FadeIn(effects[1]), run_time=.85)
        self.keep(axis, axis_labels, low, tau, effects[1]); self.to(70)

        # 73-79: core idea, three inputs on one fixed network.
        self.text("모델의 깊이와 실제 사용 깊이는 다릅니다",
                  "네트워크는 하나지만 입력의 난이도에 따라\nL3, L7, L12처럼 서로 다른 지점에서 끝납니다.",
                  "FIXED MAX DEPTH  ·  INPUT-DEPENDENT COMPUTE")
        final_row = layers(y=.5)
        r3 = path_on(final_row, 3, GOOD, .2); r7 = path_on(final_row, 7, ACCENT, 0)
        r12 = path_on(final_row, 12, PRUNE, -.2)
        exits = VGroup(pill("EXIT L3", GOOD, 1.65).move_to(final_row[2].get_center()+DOWN*1.25),
                       pill("EXIT L7", ACCENT, 1.65).move_to(final_row[6].get_center()+DOWN*1.85),
                       pill("EXIT L12", PRUNE, 1.8).move_to(final_row[11].get_center()+DOWN*1.25))
        self.play(FadeOut(Group(axis, axis_labels, low, tau, effects[1])), FadeIn(final_row), run_time=.5)
        self.play(Create(r3), Create(r7), Create(r12), FadeIn(exits), run_time=1.0)
        self.keep(final_row, r3, r7, r12, exits); self.to(78)

        # 79-82: token pruning teaser.
        self.text("그렇다면 입력의 일부만 먼저 멈출 수도 있을까요?",
                  "다음은 전체 입력이 아니라\n필요 없어진 Token만 계산에서 제거합니다.",
                  "NEXT  ·  TOKEN PRUNING")
        tokens = VGroup(*[RoundedRectangle(width=.72, height=.72, corner_radius=.1,
                                           stroke_color=ACCENT, fill_color=ACCENT,
                                           fill_opacity=.12) for _ in range(8)])
        tokens.arrange(RIGHT, buff=.16).move_to([0, .35, 0])
        labels = VGroup(*[txt(f"T{i+1}", 16, ACCENT).move_to(tokens[i]) for i in range(8)])
        self.play(FadeOut(Group(final_row, r3, r7, r12, exits)), FadeIn(tokens), FadeIn(labels), run_time=.55)
        self.play(*[tokens[i].animate.set_opacity(.08) for i in (1, 4, 6)],
                  *[labels[i].animate.set_opacity(.12) for i in (1, 4, 6)], run_time=.6)
        self.keep(tokens, labels); self.to(82)

    def text(self, head, sub, note):
        old = VGroup(self.head, self.note, self.sub)
        if len(old):
            self.play(FadeOut(old, shift=UP*.06), run_time=.14)
        self.head = txt(head, 29).move_to(UP * 5.15)
        self.note = txt(note, 20, ACCENT).move_to(DOWN * 4.72)
        self.sub = txt(sub, 25).move_to(DOWN * 6.08)
        self.play(FadeIn(self.head), FadeIn(self.note), FadeIn(self.sub), run_time=.28)

    def keep(self, *allowed):
        roots = (self.chrome, self.progress, self.head, self.note, self.sub, *allowed)
        keep = set()
        for root in roots:
            keep.update(root.get_family())
        for mob in list(self.mobjects):
            if mob not in keep:
                self.remove(mob)

    def to(self, target):
        remain = target - self.time
        if remain < -.04:
            raise ValueError(f"Timeline overrun {target}: {self.time:.2f}")
        width = max(.01, 7.6 * target / self.DURATION)
        if remain > 0:
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to(
                [-3.8 + width/2, -7.35, 0]), run_time=min(.22, remain))
            self.wait(max(0, target - self.time))
