"""Compression reallocates bit costs using a shared predictive model."""
import sys
from pathlib import Path
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import txt, INK, MUTED, WEIGHT, PRUNE, GOOD, ACCENT
from episodes.info05_predictable_cost.content import (
    CUES, DURATION, MESSAGE, FIXED, VARIABLE, FIXED_BITS, VARIABLE_BITS, ENTROPY, MEAN_LENGTH,
)

COLORS = dict(zip("ABCD", (WEIGHT, GOOD, PRUNE, ACCENT)))


class PredictableBitCosts(Scene):
    DURATION = DURATION

    def construct(self):
        self.stage, self.caption = VGroup(), VGroup()
        self.add(
            txt("INFORMATION THEORY  /  05", 20, MUTED).move_to(UP * 7.25),
            txt("압축: 예상 가능한 것을 짧게 쓴다", 32).move_to(UP * 6.4),
            Line([-3.8, 5.8, 0], [3.8, 5.8, 0], color=MUTED, stroke_opacity=.3),
        )
        self.progress = Rectangle(width=.01, height=.04, stroke_width=0, fill_color=ACCENT, fill_opacity=1).move_to([-3.8, -7.35, 0])
        self.add(self.progress)
        captions = [
            "원문은 그대로, 비트 비용을 바꾼다면?", "A 14개 / B·C·D 각 2개", "자주 쓰는 이름을 싸게 만든다",
            "짧은 질문 경로 → 짧은 코드", "코드표를 공유하면 정확히 복원", "본문: 40 → 30 bits / 25% 절약",
            "모두 짧게가 아니라, 비용 재배분", "예측 가능성 → 적은 평균 비트 비용", "반복도, 규칙도 예측의 단서",
            "평균 코드 길이와 엔트로피는 구별", "압축은 예측 가능성을 이용한다", "다음: 예측이 틀렸을 때의 비용",
        ]
        for i, (start, end, display, spoken) in enumerate(CUES):
            if i:
                self.play(FadeOut(self.stage), FadeOut(self.caption), run_time=.2)
            self.caption = txt(captions[i], 27).move_to(DOWN * 5.9)
            self.play(FadeIn(self.caption), run_time=.2)
            if i == 0:
                self.stage = VGroup(
                    txt("기호를 지울까?", 39, MUTED).move_to(UP * 2.6),
                    txt("같은 원문, 더 싼 표현", 41, ACCENT),
                    txt("비트의 지출을 다시 배분", 31, GOOD).move_to(DOWN * 2.4),
                )
                self.play(FadeIn(self.stage), run_time=.4)
            elif i == 1:
                message = self.message_grid().move_to(UP * 2.4)
                table = self.code_table(FIXED).move_to(DOWN * .5)
                total = txt(f"20 × 2 = {len(FIXED_BITS)} bits", 37, ACCENT).move_to(DOWN * 3.5)
                self.stage = VGroup(message, table, total)
                self.play(FadeIn(self.stage), run_time=.4)
            elif i == 2:
                distribution = self.distribution((.7, .1, .1, .1)).move_to(UP * 2.8)
                table = self.code_table(FIXED).move_to(DOWN * .2)
                question = txt("A에 쓰는 비용부터 줄인다면?", 32, ACCENT).move_to(DOWN * 3.4)
                self.stage = VGroup(distribution, table, question)
                self.play(FadeIn(self.stage), run_time=.4)
                self.play(Transform(table, self.code_table(VARIABLE).move_to(table)), run_time=.65)
            elif i == 3:
                tree = self.code_tree()
                self.stage = tree
                self.play(FadeIn(tree), run_time=.4)
                note = txt("A: 1 / B: 2 / C·D: 3 bits", 30, ACCENT).move_to(DOWN * 3.8)
                self.stage.add(note)
                self.play(FadeIn(note), run_time=.3)
            elif i == 4:
                example = "ABCD"
                bits = "".join(VARIABLE[s] for s in example)
                top = txt(bits, 55, ACCENT).move_to(UP * 2.9)
                chunks = VGroup(*[txt(VARIABLE[s], 46, COLORS[s]) for s in example]).arrange(RIGHT, buff=.6).move_to(UP * .7)
                letters = VGroup(*[txt(s, 42, COLORS[s]).move_to([c.get_x(), -1, 0]) for s, c in zip(example, chunks)])
                note = txt("끝이 정해지는 코드 / 공유된 코드표", 27, MUTED).move_to(DOWN * 3)
                self.stage = VGroup(top, chunks, letters, note)
                self.play(FadeIn(top), FadeIn(note), run_time=.4)
                self.play(LaggedStart(*[FadeIn(c) for c in chunks], lag_ratio=.2), FadeIn(letters), run_time=.8)
            elif i == 5:
                message = self.message_grid().move_to(UP * 3.6)
                fixed = self.bit_grid(FIXED_BITS, MUTED).move_to(UP * .6)
                count = txt("40 bits", 30, MUTED).move_to(UP * 2.1)
                original = txt("같은 원문 20개", 24, WEIGHT).move_to(UP * 4.6)
                self.stage = VGroup(message, fixed, count, original)
                self.play(FadeIn(self.stage), run_time=.4)
                compressed = self.bit_grid(VARIABLE_BITS, GOOD).move_to(DOWN * 2.1)
                result = txt("30 bits  /  25% 절약", 35, ACCENT).move_to(DOWN * 3.7)
                overhead = txt("코드표 공유 가정 / 본문 비트만 비교", 22, MUTED).move_to(DOWN * 4.5)
                self.stage.add(compressed, result, overhead)
                self.play(FadeIn(compressed), FadeIn(result), FadeIn(overhead), run_time=.7)
            elif i == 6:
                rows = VGroup()
                for symbol, count in zip("ABCD", (14, 2, 2, 2)):
                    delta = (len(VARIABLE[symbol]) - 2) * count
                    row = txt(f"{symbol}  ×{count} :  {2*count} → {count*len(VARIABLE[symbol])} bits", 31, COLORS[symbol])
                    rows.add(row)
                rows.arrange(DOWN, buff=.65).move_to(UP * .8)
                note = txt("A의 −14  +  C·D의 +4  =  −10 bits", 28, ACCENT).move_to(DOWN * 2.8)
                self.stage = VGroup(rows, note)
                self.play(FadeIn(self.stage), run_time=.4)
                self.play(Indicate(rows[0], color=WEIGHT), run_time=.6)
            elif i == 7:
                self.stage = VGroup(
                    txt("자주 만날 결과", 35, WEIGHT).move_to(UP * 2.8),
                    txt("↓", 36, MUTED).move_to(UP * 1.4),
                    txt("짧은 이름 / 적은 비트", 40, ACCENT),
                    txt("절약은 자주 쓰는 곳에서", 32, GOOD).move_to(DOWN * 2.5),
                )
                self.play(FadeIn(self.stage), run_time=.4)
            elif i == 8:
                sequence = txt("A B A C A D A E A F", 36, WEIGHT).move_to(UP * 2.6)
                rule = txt("홀수 위치: A\n짝수 위치: 다음 알파벳", 33, ACCENT).move_to(UP * .2)
                continuation = txt("다음은  A G A H", 39, GOOD).move_to(DOWN * 2.3)
                shared = txt("규칙을 아는 모형에서는 예측 가능", 26, MUTED).move_to(DOWN * 3.8)
                self.stage = VGroup(sequence, rule, continuation, shared)
                self.play(FadeIn(sequence), FadeIn(rule), FadeIn(shared), run_time=.4)
                self.play(FadeIn(continuation), run_time=.4)
            elif i == 9:
                self.stage = VGroup(
                    txt("실제 길이: 1, 2, 3, 3 bits", 31, WEIGHT).move_to(UP * 3.3),
                    txt(f"평균 L = {MEAN_LENGTH:g} bits/기호", 36, GOOD).move_to(UP * 1.7),
                    txt(f"H(X) = {ENTROPY:.3f} bits/기호", 36, ACCENT).move_to(UP * .1),
                    txt("H(X) ≤ 최적 평균 코드 길이", 28).move_to(DOWN * 1.7),
                    txt("여러 독립 기호를 묶으면\n기호당 평균 길이가 H(X)에 접근", 27, MUTED).move_to(DOWN * 3.4),
                )
                self.play(FadeIn(self.stage), run_time=.4)
            elif i == 10:
                self.stage = VGroup(
                    txt("COMPRESSION", 37, MUTED).move_to(UP * 3.5),
                    txt("예상 가능한 것을\n짧게 쓰는 설계", 43, ACCENT),
                    txt("같은 내용을, 적은 평균 비트로", 30, GOOD).move_to(DOWN * 2.8),
                )
                self.play(FadeIn(self.stage), run_time=.4)
            else:
                actual = self.distribution((.7, .1, .1, .1)).move_to(UP * 1.7)
                model = self.distribution((.1, .7, .1, .1)).move_to(DOWN * 1.6)
                title = txt("예상한 확률이 틀렸다면?", 36, ACCENT).move_to(UP * 4.4)
                p_label = txt("실제 p(x)", 29, WEIGHT).move_to(UP * 2.8)
                q_label = txt("예측 q(x)", 29, PRUNE).move_to(DOWN * .5)
                question = txt("잘못 배분한 비트는 얼마나 비쌀까?", 30).move_to(DOWN * 3.8)
                self.stage = VGroup(actual, model, title, p_label, q_label, question)
                self.play(FadeIn(self.stage), run_time=.4)
            self.to(end)

    def message_grid(self):
        return VGroup(*[txt(s, 30, COLORS[s]) for s in MESSAGE]).arrange_in_grid(2, 10, buff=(.3, .25))

    def code_table(self, codes):
        return VGroup(*[txt(f"{s}  →  {codes[s]}", 33, COLORS[s]) for s in "ABCD"]).arrange(DOWN, buff=.35)

    def bit_grid(self, bits, color):
        cells = VGroup()
        for bit in bits:
            cells.add(VGroup(Square(side_length=.4, stroke_color=color, stroke_width=1, fill_color=color, fill_opacity=.09), txt(bit, 22, color)))
        return cells.arrange_in_grid(len(bits) // 10, 10, buff=.12)

    def distribution(self, probabilities):
        group, left = VGroup(), -3.6
        for symbol, probability in zip("ABCD", probabilities):
            width = 7.2 * probability
            box = Rectangle(width=width, height=.75, stroke_width=0, fill_color=COLORS[symbol], fill_opacity=.8).move_to([left+width/2, 0, 0])
            group.add(box, txt(symbol, 24).move_to(box), txt(f"{probability:g}", 21, MUTED).move_to(box.get_center()+DOWN*.8))
            left += width
        return group

    def code_tree(self):
        points = {"root": [0,3.4,0], "A": [-2.7,1.6,0], "qB": [1.1,1.6,0], "B": [-.8,-.2,0], "qC": [2.3,-.2,0], "C": [1.1,-2,0], "D": [3.35,-2,0]}
        group = VGroup()
        for parent, child, bit in (("root","A","0"),("root","qB","1"),("qB","B","0"),("qB","qC","1"),("qC","C","0"),("qC","D","1")):
            edge = Line(points[parent], points[child], color=WEIGHT, stroke_width=2.4)
            group.add(edge, txt(bit, 24, ACCENT).move_to(edge.get_center()+UP*.15))
        for node in ("root", "qB", "qC"):
            group.add(Dot(points[node], radius=.07, color=INK))
        for symbol in "ABCD":
            position = np.array(points[symbol])
            group.add(txt(symbol, 30, COLORS[symbol]).move_to(position+DOWN*.1), txt(VARIABLE[symbol], 26, ACCENT).move_to(position+DOWN*.7))
        return group

    def to(self, target):
        remain = target - self.time
        if remain < -.025:
            raise ValueError(f"Timeline overrun: {self.time} > {target}")
        width = max(.01, 7.6 * target / self.DURATION)
        if remain > 0:
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to([-3.8+width/2, -7.35, 0]), run_time=min(.1, remain))
        if target-self.time > .001:
            self.wait(target-self.time)
