"""Compare two persistent lanes before explaining the fused lane's internals."""
import sys
from pathlib import Path

from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import (
    ACCENT, BG, GOOD, INK, MUTED, PRUNE, SPARSE, WEIGHT, txt,
)

config.disable_caching = True


def at(x, y):
    return np.array([x, y, 0.0])


def label(value, size=27, color=INK, width=7.6):
    return txt(value, size, color, width)


def token(value, color=ACCENT, radius=.32, size=25):
    return VGroup(Circle(radius=radius, color=color, stroke_width=2.4,
                         fill_color=BG, fill_opacity=1),
                  label(value, size, INK, radius*1.75))


def track(points, color=MUTED):
    p = VMobject(stroke_color=color, stroke_width=2.2, stroke_opacity=.6)
    p.set_points_as_corners([np.array(x, dtype=float) for x in points])
    return p


def tensor(values=None, center=at(.15, 1.8)):
    """A real four-element probability tensor, used only in the upper lane."""
    values = values or ["0.1", "0.2", "0.3", "0.4"]
    frame = RoundedRectangle(width=3.55, height=1.24, corner_radius=.12,
                             stroke_color=WEIGHT, stroke_width=2.0,
                             fill_color=BG, fill_opacity=1).move_to(center)
    caption = label("Softmax output", 20, WEIGHT).move_to(center+UP*.4)
    circles = VGroup(*[token(v, ACCENT if i==3 else WEIGHT, .28, 23)
                           .move_to(center+at(-1.14+i*.76, -.13))
                       for i,v in enumerate(values)])
    return VGroup(frame, caption, circles)


class Comparison(VGroup):
    """Common four inputs and one common loss; upper materialization, lower state."""
    def __init__(self):
        super().__init__()
        self.bank = VGroup(*[token(v, ACCENT if i==3 else WEIGHT, .3, 26)
                            .move_to(at(-3.2, .9-i*.6)) for i,v in enumerate([1,2,3,4])])
        self.end = at(3.15, 0)
        self.loss = token("L", ACCENT, .57, 30).move_to(self.end)
        self.upper = track([at(-2.8, 0), at(-2.3, 0), at(-2.3, 1.8),
                            at(3.15, 1.8), self.end])
        self.lower = track([at(-2.3, 0), at(-2.3, -1.8), at(3.15, -1.8), self.end])
        self.memory = RoundedRectangle(width=3.9, height=1.5, corner_radius=.15,
                                       stroke_color=PRUNE, stroke_width=2,
                                       fill_color=PRUNE, fill_opacity=.045).move_to(at(.15, 3.35))
        self.memory.set_opacity(.25)
        self.memory_label = label("GPU Memory", 24, PRUNE).move_to(at(.15, 4.35))
        self.memory_label.set_opacity(.45)
        self.upper_hint = label("Softmax → 확률 4개", 26, WEIGHT, 3.6).move_to(at(.15, 1.8))
        self.lower_hint = label("필요한 정보만", 27, GOOD, 3.5).move_to(at(.15, -1.8))
        absent_frame = RoundedRectangle(width=3.6, height=.95, corner_radius=.12,
                                        color=MUTED, stroke_width=1.4).move_to(at(.15, -3.4))
        self.absent_frame = DashedVMobject(absent_frame, num_dashes=28)
        self.absent = VGroup(self.absent_frame,
                            label("중간 확률 Tensor\n생성하지 않음", 23, GOOD, 3.3)
                            .move_to(at(.15, -3.4)))
        self.add(self.upper, self.lower,
                 Line(at(-1.85, 0), at(2.25, 0), color=MUTED,
                      stroke_width=1, stroke_opacity=.18),
                 self.bank, self.loss, self.memory, self.memory_label,
                 self.upper_hint, self.lower_hint, self.absent,
                 label("지수값", 22, MUTED, 1.15).move_to(at(-3.2, 1.5)),
                 label("Separate\n일반 경로", 23, PRUNE, 1.7).move_to(at(-3.2, 2.75)),
                 label("Fused\n결합 경로", 23, GOOD, 1.7).move_to(at(-3.2, -2.75)),
                 label("같은 Loss", 24, ACCENT, 1.6).move_to(at(3.15, 2.75)),
                 label("−log", 23, MUTED, 1.0).move_to(at(2.0, .7)),
                 label("직접 계산", 23, GOOD, 1.35).move_to(at(2.0, -.8)))
        self.active_tensor = None
        self.stored_tensor = None
        self.target_state = None
        self.sum_state = None

    def upper_paths(self, targets):
        return [track([self.bank[i].get_center(), at(-2.3, self.bank[i].get_y()),
                       at(-2.3, 1.67), targets[i].get_center()]) for i in range(4)]

    def lower_paths(self, destination):
        return [track([self.bank[i].get_center(), at(-2.3, self.bank[i].get_y()),
                       at(-2.3, -1.8), destination]) for i in range(4)]


class GPUSoftmaxCrossEntropy(Scene):
    DURATION = 100

    def construct(self):
        self.stage = VGroup(); self.heading = VGroup(); self.note = VGroup()
        self.progress = Rectangle(width=.01, height=.035, fill_color=ACCENT,
                                  fill_opacity=1, stroke_width=0).move_to(at(-3.8, -7.36))
        self.add(VGroup(
            label("GPU OPERATIONS  /  11", 20, MUTED).move_to(UP*7.3),
            label("Softmax + Cross Entropy\n중간 확률 없이 Loss까지", 29).move_to(UP*6.5),
            Line(at(-3.8, 5.82), at(3.8, 5.82), color=MUTED, stroke_opacity=.35),
        ), self.progress)

        # 0–7: a short classification context, before any reduction mechanics.
        self.copy("Loss만 필요하다면?", "정답은 4번째 클래스 · 노란색으로 유지")
        classes = VGroup(*[token(v, ACCENT if i==3 else WEIGHT, .43, 29)
                              .move_to(at(-2.4+i*1.6, 2.7)) for i,v in enumerate("ABCD")])
        words = VGroup(*[label(v, 24, GOOD if i==4 else INK, 1.35)
                           .move_to(at(-3.2+i*1.6, .55))
                         for i,v in enumerate(["Model", "Logits", "Softmax", "Cross\nEntropy", "Loss"])])
        links = VGroup(*[Arrow(words[i].get_right(), words[i+1].get_left(), buff=.08,
                               color=MUTED, stroke_width=1.8, tip_length=.12) for i in range(4)])
        self.show(VGroup(classes, words, links,
                         label("최종적으로 원하는 값은 Loss 하나", 29, ACCENT)
                         .move_to(at(0, -2.1))))
        self.to(3.2)
        self.play(Indicate(classes[3], color=ACCENT), run_time=.6)
        self.to(7)

        # 7–14: the full comparison is visible first and stays through 65 s.
        self.copy("같은 출발점, 같은 도착점", "위: 확률 전체 저장 · 아래: 필요한 정보만")
        board = Comparison()
        self.show(board)
        self.to(10.0)
        self.play(Indicate(board.bank, color=WEIGHT),
                  Indicate(board.loss, color=ACCENT), run_time=.8)
        self.to(14)

        # 14–23: actual creation of ALL four probabilities in the upper lane.
        self.copy("위쪽은 확률 4개를 모두 만듭니다", "예시 입력은 logits가 아닌 지수값 [1, 2, 3, 4]")
        self.to(15.5)
        self.create_probabilities(board)
        self.to(19.5)
        self.play(Indicate(board.active_tensor, color=WEIGHT), run_time=.7)
        self.to(23)

        # 23–33: the whole tensor crosses into memory; reading makes a copy.
        self.copy("Tensor 전체를 쓰고, 다시 읽습니다", "WRITE → GPU MEMORY → READ")
        self.to(24.3)
        self.play(board.memory.animate.set_opacity(1),
                  board.memory_label.animate.set_opacity(1), run_time=.35)
        write = VGroup(Arrow(at(-2.1, 2.7), at(-2.1, 3.95), buff=0, color=PRUNE,
                             stroke_width=2.5, tip_length=.13),
                       label("WRITE", 21, PRUNE, 1.05).move_to(at(-2.85, 3.65)))
        read = VGroup(Arrow(at(2.4, 3.95), at(2.4, 2.7), buff=0, color=PRUNE,
                            stroke_width=2.5, tip_length=.13),
                      label("READ", 21, PRUNE, 1.0).move_to(at(3.1, 3.65)))
        self.reveal(write)
        self.play(board.active_tensor.animate.shift(UP*1.55), run_time=1.2)
        board.stored_tensor = board.active_tensor
        self.to(28.0)
        self.reveal(read)
        active = board.stored_tensor.copy()
        self.stage.add(active); self.add(active)
        self.play(active.animate.shift(DOWN*1.55), run_time=1.2)
        board.active_tensor = active
        self.to(33)

        # 33–41: keep the complete materialized tensors, select just the target.
        self.copy("4개를 저장했는데, 여기서는 하나만 사용", "정답 확률 0.4 → −log → Loss 0.916")
        self.to(34.2)
        self.play(*[board.active_tensor[2][i].animate.set_opacity(.22) for i in range(3)],
                  *[board.stored_tensor[2][i].animate.set_opacity(.35) for i in range(3)], run_time=.5)
        chosen = board.active_tensor[2][3].copy()
        self.stage.add(chosen); self.add(chosen)
        self.to(36)
        self.play(MoveAlongPath(chosen, track([chosen.get_center(), at(3.15, 1.67), board.end])),
                  run_time=1.25)
        self.play(FadeOut(chosen), run_time=.15)
        self.change(board.loss, "0.916", .4, ACCENT, .57)
        self.to(41)

        # 41–50: bottom lane never creates a normalized probability vector.
        self.copy("아래쪽은 최종 Loss에 필요한 정보만", "정답 값 4 + 모든 클래스에서 모은 합 10")
        self.to(42.2)
        self.create_loss_state(board)
        self.to(47.3)
        self.play(Indicate(board.target_state, color=ACCENT),
                  Indicate(board.sum_state, color=SPARSE), run_time=.7)
        self.to(50)

        # 50–58: direct loss meets the very same output, without a p tensor.
        self.copy("확률 4개가 등장하지 않습니다", "같은 Loss 0.916 · 중간 확률 Tensor 생성하지 않음")
        self.to(51.5)
        target_copy = board.target_state.copy()
        sum_copy = board.sum_state.copy().scale(.65)
        self.stage.add(target_copy, sum_copy); self.add(target_copy, sum_copy)
        self.play(*[MoveAlongPath(v, track([v.get_center(), at(3.15, -1.8), board.end]))
                    for v in [target_copy, sum_copy]], run_time=1.4)
        self.play(FadeOut(VGroup(target_copy, sum_copy)), run_time=.15)
        self.play(Indicate(board.loss, color=ACCENT), run_time=.6)
        self.play(Indicate(board.absent, color=GOOD), run_time=.3)
        self.to(58)

        # 58–65: recap the difference before zooming into numerical mechanics.
        self.copy("없애는 것은 중간 확률 Tensor", "입력 전체는 필요 · 출력 확률 전체는 생략 가능")
        self.to(59.0)
        self.play(Indicate(board.active_tensor, color=PRUNE), run_time=.7)
        self.to(61.5)
        self.play(Indicate(VGroup(board.target_state, board.sum_state), color=GOOD), run_time=.7)
        self.to(65)

        # 65–76: only now enter the bottom path's stable MAX reduction.
        self.copy("아래 경로의 내부: 먼저 큰 값을 안정화", "새 logits 예시 [1000, 999, 998] · 정답은 마지막")
        px = [-2.3, 0, 2.3]
        raw = VGroup(*[token(v, ACCENT if i==2 else WEIGHT, .5)
                         .move_to(at(px[i], 3.25)) for i,v in enumerate([1000,999,998])])
        partial = VGroup(token("?", SPARSE, .46).move_to(at(-1.2, 1.3)),
                         token("998", ACCENT, .46).move_to(at(2.3, 1.3)))
        maximum = token("?", SPARSE, .58).move_to(at(0, -.65))
        tree = VGroup(*[track([raw[i].get_center(), partial[0 if i<2 else 1].get_center()])
                        for i in range(3)],
                      *[track([p.get_center(), maximum.get_center()]) for p in partial])
        overflow = label("exp(1000) → overflow 위험", 25, PRUNE).move_to(at(0, 4.25))
        max_label = label("MAX Reduction", 26, SPARSE).move_to(at(0, -1.65))
        self.show(VGroup(tree, raw, partial, maximum, overflow, max_label))
        self.to(66.8)
        copies = VGroup(*[v.copy().scale(.6).set_opacity(.65) for v in raw])
        self.stage.add(copies); self.add(copies)
        self.play(*[MoveAlongPath(copies[i], tree[i]) for i in range(3)], run_time=.9)
        self.play(FadeOut(copies), run_time=.15)
        self.change(partial[0], "1000", .3, SPARSE, .46)
        pair_copies = VGroup(*[p.copy().scale(.7) for p in partial])
        self.stage.add(pair_copies); self.add(pair_copies)
        self.play(*[MoveAlongPath(pair_copies[i], tree[3+i]) for i in range(2)], run_time=.8)
        self.play(FadeOut(pair_copies), run_time=.15)
        self.change(maximum, "1000", .3, SPARSE, .58)
        self.to(70.5)
        self.play(FadeOut(VGroup(tree, partial, maximum, max_label, overflow)), run_time=.25)
        shifts = VGroup(*[label("−1000", 24, SPARSE).move_to(at(x, -.3)) for x in px])
        self.reveal(shifts)
        self.play(*[raw[i].animate.move_to(at(px[i], .7)) for i in range(3)], run_time=.6)
        self.play(*[Transform(raw[i], token(v, ACCENT if i==2 else WEIGHT, .5)
                              .move_to(at(px[i], .7))) for i,v in enumerate([0,-1,-2])], run_time=.4)
        self.play(FadeOut(shifts), run_time=.15)
        self.play(*[raw[i].animate.move_to(at(px[i], -2.3)) for i in range(3)], run_time=.65)
        self.reveal(label("최댓값을 빼도 클래스 간 차이는 유지", 25, GOOD).move_to(at(0, -3.55)))
        self.to(76)

        # 76–88: SUM tree plus retained target delta, log, and direct stable loss.
        self.copy("전체 합과 정답의 값을 마지막에 합칩니다", "MAX → EXP → SUM → LOG + 정답 값")
        leaves = VGroup(*[token(v, ACCENT if i==2 else WEIGHT, .43, 25)
                            .move_to(at(px[i], 2.55)) for i,v in enumerate([0,-1,-2])])
        kept = token("−2", ACCENT, .5).move_to(at(2.3, -2.7))
        pair = VGroup(token("?", SPARSE, .46).move_to(at(-1.2, .65)),
                      token("0.135", ACCENT, .46).move_to(at(2.3, .65)))
        total = token("?", SPARSE, .57).move_to(at(0, -1.25))
        tree = VGroup(*[track([leaves[i].get_center(), pair[0 if i<2 else 1].get_center()])
                        for i in range(3)], *[track([p.get_center(), total.get_center()]) for p in pair])
        keep_label = label("정답의 차이는 유지", 22, ACCENT, 2.4).move_to(at(2.3, -3.55))
        sum_label = label("SUM Reduction", 26, SPARSE).move_to(at(-1.5, -2.2))
        exp_label = label("exp", 24, MUTED).move_to(at(0, 3.8))
        self.show(VGroup(tree, leaves, pair, total, kept, keep_label,
                         sum_label, exp_label))
        self.to(77.5)
        self.play(*[Transform(leaves[i], token(v, ACCENT if i==2 else WEIGHT, .43, 25)
                              .move_to(at(px[i], 2.55))) for i,v in enumerate(["1","0.368","0.135"])],
                  run_time=.45)
        self.to(78.8)
        copies = VGroup(*[v.copy().scale(.65) for v in leaves])
        self.stage.add(copies); self.add(copies)
        self.play(*[MoveAlongPath(copies[i], tree[i]) for i in range(3)], run_time=.8)
        self.play(FadeOut(copies), run_time=.15)
        self.change(pair[0], "1.368", .3, SPARSE, .46)
        copies2 = VGroup(*[p.copy().scale(.65) for p in pair])
        self.stage.add(copies2); self.add(copies2)
        self.play(*[MoveAlongPath(copies2[i], tree[3+i]) for i in range(2)], run_time=.75)
        self.play(FadeOut(copies2), run_time=.15)
        self.change(total, "1.503", .3, SPARSE, .57)
        self.to(82.5)
        self.play(FadeOut(VGroup(leaves, tree, pair, keep_label, sum_label, exp_label)), run_time=.2)
        self.change(total, "0.408", .3, SPARSE, .57)
        self.change(kept, "2", .3, ACCENT, .5)
        self.play(total.animate.move_to(at(-1.25, -2.7)), run_time=.4)
        info = VGroup(label("log s", 23, SPARSE).move_to(at(-1.25, -1.8)),
                      label("−(−2)", 23, ACCENT).move_to(at(2.3, -1.8)))
        self.reveal(info, .2)
        self.to(84.6)
        self.play(total.animate.move_to(at(.25, -2.7)),
                  kept.animate.move_to(at(.25, -2.7)), run_time=.6)
        self.play(FadeOut(total), FadeOut(info), run_time=.15)
        self.change(kept, "2.408", .3, ACCENT, .6)
        self.reveal(label("L = −(zᵧ−m) + log s", 27).move_to(at(0, -4.1)), .3)
        self.to(88)

        # 88–100: the two lanes really run together, from the same four inputs.
        self.copy("필요 없는 중간 결과는 만들지 않는다", "결합 가능 여부와 Kernel 수는 구현·크기에 따라 다름")
        board = Comparison()
        self.show(board)
        self.to(89.25)
        self.race(board)
        self.to(100)

    def create_probabilities(self, board):
        result = tensor([1,2,3,4])
        targets = result[2]
        origins = VGroup(*[v.copy() for v in board.bank])
        self.stage.add(origins); self.add(origins)
        self.play(FadeOut(board.upper_hint),
                  *[MoveAlongPath(origins[i], board.upper_paths(targets)[i]) for i in range(4)],
                  run_time=1.1)
        self.play(*[Transform(origins[i], token(v, ACCENT if i==3 else WEIGHT, .28, 23)
                              .move_to(targets[i].get_center()))
                    for i,v in enumerate(["0.1","0.2","0.3","0.4"])], run_time=.4)
        self.remove(origins); self.stage.remove(origins)
        result = tensor()
        self.stage.add(result); self.add(result)
        self.play(FadeIn(VGroup(result[0], result[1])), run_time=.25)
        board.active_tensor = result

    def create_loss_state(self, board):
        target = board.bank[3].copy()
        aggregate = token("?", SPARSE, .4).move_to(at(.85, -1.8))
        copies = VGroup(*[v.copy().scale(.7).set_opacity(.7) for v in board.bank])
        self.stage.add(target, aggregate, copies); self.add(target, aggregate, copies)
        self.play(FadeOut(board.lower_hint),
                  MoveAlongPath(target, board.lower_paths(at(-.55, -1.8))[3]),
                  *[MoveAlongPath(copies[i], board.lower_paths(aggregate.get_center())[i]) for i in range(4)],
                  run_time=1.3)
        self.play(FadeOut(copies), run_time=.15)
        self.change(aggregate, "10", .35, SPARSE, .4)
        self.reveal(VGroup(label("정답 값", 22, ACCENT, 1.25).move_to(at(-.55, -2.5)),
                           label("공통 합", 22, SPARSE, 1.25).move_to(at(.85, -2.5))), .25)
        board.target_state = target; board.sum_state = aggregate

    def race(self, board):
        result = tensor([1,2,3,4]); slots = result[2]
        upper = VGroup(*[v.copy() for v in board.bank])
        lower = VGroup(*[v.copy().scale(.65).set_opacity(.7) for v in board.bank])
        target = board.bank[3].copy()
        total = token("10", SPARSE, .4).move_to(at(.85, -1.8))
        self.stage.add(upper, lower, target); self.add(upper, lower, target)
        self.play(FadeOut(VGroup(board.upper_hint, board.lower_hint)),
                  *[MoveAlongPath(upper[i], board.upper_paths(slots)[i]) for i in range(4)],
                  *[MoveAlongPath(lower[i], board.lower_paths(total.get_center())[i]) for i in range(4)],
                  MoveAlongPath(target, board.lower_paths(at(-.55, -1.8))[3]), run_time=1.0)
        self.play(*[Transform(upper[i], token(v, ACCENT if i==3 else WEIGHT, .28, 23)
                              .move_to(slots[i].get_center())) for i,v in enumerate(["0.1","0.2","0.3","0.4"])],
                  FadeOut(lower), run_time=.3)
        self.remove(upper); self.stage.remove(upper)
        result = tensor(); self.stage.add(result, total); self.add(result, total)
        self.play(FadeIn(VGroup(result[0], result[1], total)),
                  board.memory.animate.set_opacity(1), board.memory_label.animate.set_opacity(1), run_time=.2)
        self.reveal(VGroup(label("WRITE", 21, PRUNE, 1.05).move_to(at(-2.85, 3.65)),
                           label("READ", 21, PRUNE, 1.0).move_to(at(3.1, 3.65))), .2)
        lower_target = target.copy(); lower_sum = total.copy().scale(.7)
        self.stage.add(lower_target, lower_sum); self.add(lower_target, lower_sum)
        self.play(result.animate.shift(UP*1.55),
                  *[MoveAlongPath(v, track([v.get_center(), at(3.15, -1.8), board.end]))
                    for v in [lower_target, lower_sum]], run_time=1.0)
        self.play(FadeOut(VGroup(lower_target, lower_sum)), run_time=.1)
        self.change(board.loss, "0.916", .25, ACCENT, .57)
        read = result.copy(); self.stage.add(read); self.add(read)
        self.play(read.animate.shift(DOWN*1.55), run_time=.9)
        self.play(*[read[2][i].animate.set_opacity(.2) for i in range(3)], run_time=.2)
        chosen = read[2][3].copy(); self.stage.add(chosen); self.add(chosen)
        self.play(MoveAlongPath(chosen, track([chosen.get_center(), at(3.15, 1.67), board.end])), run_time=.85)
        self.play(FadeOut(chosen), run_time=.1)
        self.play(Indicate(board.loss, color=ACCENT), run_time=.45)
        self.play(Indicate(board.absent, color=GOOD), run_time=.25)
        self.reveal(label("정답 값 + 공통 합", 23, GOOD, 3.6).move_to(at(.15, -2.55)), .25)

    def copy(self, heading, note):
        self.play(FadeOut(VGroup(self.heading, self.note)), run_time=.1)
        self.heading = label(heading, 29).move_to(UP*5.12)
        self.note = label(note, 22, ACCENT).move_to(DOWN*4.95)
        self.play(FadeIn(self.heading), FadeIn(self.note), run_time=.22)

    def show(self, obj):
        if len(self.stage): self.play(FadeOut(self.stage), run_time=.18)
        self.stage = obj
        self.play(FadeIn(obj), run_time=.4)

    def reveal(self, obj, duration=.22):
        self.stage.add(obj)
        self.play(FadeIn(obj), run_time=duration)

    def change(self, obj, value, duration=.3, color=ACCENT, radius=.32):
        self.play(Transform(obj, token(value, color, radius).move_to(obj.get_center())), run_time=duration)

    def to(self, target):
        remaining = target-self.time
        if remaining < -.04: raise ValueError(f"Timeline overrun at {target}: {self.time:.3f}")
        width = max(.01, 7.6*target/self.DURATION)
        if remaining>0:
            self.play(self.progress.animate.stretch_to_fit_width(width)
                      .move_to(at(-3.8+width/2,-7.36)), run_time=min(.12,remaining))
            self.wait(max(0,target-self.time))
