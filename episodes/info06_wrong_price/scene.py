"""The source supplies occurrences; the model supplies log-cost prices."""
import sys
from pathlib import Path
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import txt, INK, MUTED, WEIGHT, PRUNE, GOOD, ACCENT
from episodes.info06_wrong_price.content import (
    CUES, DURATION, P, Q, COUNTS, MESSAGE, PRICES_P, PRICES_Q,
    H_P, H_PQ, EXTRA, cross_entropy, interpolated_q,
)

COLORS = dict(zip("ABCD", (WEIGHT, GOOD, PRUNE, ACCENT)))
SCALE = 1.8  # Fixed frame units per bit; all cost bars have the same scale.


class WrongProbabilityPrice(Scene):
    DURATION = DURATION

    def construct(self):
        self.stage, self.caption = VGroup(), VGroup()
        self.add(
            txt("INFORMATION THEORY  /  06", 20, MUTED).move_to(UP*7.25),
            txt("틀린 확률, 비싸진 현실의 청구서", 32).move_to(UP*6.4),
            Line([-3.8,5.8,0], [3.8,5.8,0], color=MUTED, stroke_opacity=.3),
        )
        self.progress = Rectangle(width=.01, height=.04, stroke_width=0, fill_color=ACCENT, fill_opacity=1).move_to([-3.8,-7.35,0])
        self.add(self.progress)
        captions = [
            "같은 현실, 다른 가격표", "실제 p와 예측 모형 q는 다름", "정보 가격 = −log₂ q(x)",
            "틀린 예측의 비용을 반복해서 지불", "p는 빈도 / q는 정보 가격", "Cross Entropy = 평균 정보 비용",
            "p는 고정 / q만 달라진 평균 비용", "q=p이면 H(p,q)=H(p)", "단일 정답 라벨: pᵧ=[1,0,0]",
            "정답에 낮은 확률을 줬을수록 큰 비용", "현실의 빈도에 가격표를 맞춘다", "다음: 총비용 중 추가분만 떼어낸다면?",
        ]
        for index, (start, end, display, spoken) in enumerate(CUES):
            if index:
                self.play(FadeOut(self.stage), FadeOut(self.caption), run_time=.2)
            self.caption = txt(captions[index], 27).move_to(DOWN*5.9)
            self.play(FadeIn(self.caption), run_time=.2)
            if index == 0:
                self.stage = VGroup(
                    txt("현실은 그대로", 38, WEIGHT).move_to(UP*2.7),
                    txt("가격표가 틀렸다면?", 44, ACCENT),
                    txt("비싼 곳을 자주 만나게 된다", 31, PRUNE).move_to(DOWN*2.5),
                )
                self.play(FadeIn(self.stage), run_time=.4)
            elif index == 1:
                actual = self.distribution(P, "실제 p(x)").shift(UP*1.9)
                model = self.distribution(Q, "예측 모형 q(x)").shift(DOWN*1.4)
                self.stage = VGroup(actual, model)
                self.play(FadeIn(self.stage), run_time=.4)
            elif index == 2:
                price = self.price_pair()
                formula = txt("−log₂ q(A)", 36, ACCENT).move_to(UP*3.9)
                scope = txt("이상적 정보 비용 / 단위 bits", 25, MUTED).move_to(DOWN*3.4)
                self.stage = VGroup(price, formula, scope)
                self.play(FadeIn(self.stage), run_time=.4)
            elif index == 3:
                message = VGroup(*[txt(s,29,COLORS[s]) for s in MESSAGE]).arrange_in_grid(2,10,buff=(.3,.25)).move_to(UP*3.2)
                title = txt("같은 20기호: A만 14번", 27, WEIGHT).move_to(UP*4.3)
                receipt = VGroup()
                for row, (symbol, count, price) in enumerate(zip("ABCD", COUNTS, PRICES_Q)):
                    receipt.add(txt(f"{symbol}: {count} × {price:.3f} = {count*price:.3f}", 29, COLORS[symbol]).move_to([0,1.4-row*1.0,0]))
                total = txt(f"총 이상적 비용: {20*H_PQ:.3f} bits", 30, ACCENT).move_to(DOWN*3.1)
                self.stage = VGroup(message, title, receipt, total)
                self.play(FadeIn(message), FadeIn(title), run_time=.4)
                self.play(LaggedStart(*[FadeIn(row) for row in receipt], lag_ratio=.15), FadeIn(total), run_time=.8)
            elif index == 4:
                left = self.role("p(x)", "실제로 얼마나 자주", WEIGHT).move_to([-1.95,1.2,0])
                right = self.role("−log₂ q(x)", "그때마다 얼마씩", PRUNE).move_to([1.95,1.2,0])
                multiply = txt("빈도 × 정보 가격", 38, ACCENT).move_to(DOWN*2.2)
                average = txt("그 비용을 실제 등장 비율로 평균", 29, GOOD).move_to(DOWN*3.6)
                self.stage = VGroup(left,right,multiply,average)
                self.play(FadeIn(self.stage), run_time=.4)
            elif index == 5:
                equation = txt("H(p,q) = Σₓ p(x)[−log₂ q(x)]", 36, ACCENT).move_to(UP*2.5)
                name = txt("CROSS ENTROPY", 44, GOOD).move_to(UP*.6)
                meaning = txt("현실 p를 모형 q의 가격표로\n표현할 때의 평균 정보 비용", 33).move_to(DOWN*1.5)
                scope = txt("실제 1기호 코드 길이와는 구별", 24, MUTED).move_to(DOWN*3.8)
                self.stage = VGroup(equation,name,meaning,scope)
                self.play(FadeIn(equation), run_time=.4)
                self.play(FadeIn(name), FadeIn(meaning), FadeIn(scope), run_time=.4)
            elif index == 6:
                chart = self.comparison()
                self.stage = chart
                self.play(FadeIn(chart), run_time=.4)
                detail = txt(f"같은 p: {H_P:.3f} → {H_PQ:.3f} bits/기호", 29, ACCENT).move_to(DOWN*3.5)
                self.stage.add(detail)
                self.play(FadeIn(detail), run_time=.3)
            elif index == 7:
                title = txt("실제 p를 고정", 29, MUTED).move_to(UP*4.2)
                model = self.model_meter(Q)
                self.stage = VGroup(title,model)
                self.play(FadeIn(self.stage), run_time=.4)
                # This specific mixture path monotonically returns to the minimum.
                for t in (.65,.3,0):
                    self.play(Transform(model,self.model_meter(interpolated_q(t))), run_time=.45)
                note = txt("q=p  →  H(p,q)=H(p)", 34, ACCENT).move_to(DOWN*3.8)
                self.stage.add(note)
                self.play(FadeIn(note), run_time=.3)
            elif index == 8:
                labels = txt("cat       dog       bird", 36, WEIGHT).move_to(UP*3.3)
                target = txt("정답 라벨 pᵧ = [1, 0, 0]", 31, GOOD).move_to(UP*1.9)
                prediction = txt("예측 q = [0.7, 0.2, 0.1]", 31).move_to(UP*.6)
                full = txt("−1 log₂q(cat) −0 log₂q(dog) −0 log₂q(bird)", 25, MUTED).move_to(DOWN*1)
                reduced = txt("= −log₂ q(cat)", 44, ACCENT).move_to(DOWN*2.5)
                scope = txt("이 관측의 정답 / 전체 데이터 분포와 구별", 23, MUTED).move_to(DOWN*4)
                self.stage = VGroup(labels,target,prediction,full,reduced,scope)
                self.play(FadeIn(labels), FadeIn(target), FadeIn(prediction), run_time=.4)
                self.play(FadeIn(full), FadeIn(reduced), FadeIn(scope), run_time=.5)
            elif index == 9:
                title = txt("같은 정답 cat", 34, WEIGHT).move_to(UP*4)
                first = self.classification_cost(.99).shift(UP*1.8)
                second = self.classification_cost(.01).shift(DOWN*1.7)
                self.stage = VGroup(title,first,second)
                self.play(FadeIn(self.stage), run_time=.4)
            elif index == 10:
                self.stage = VGroup(
                    txt("현실: 결과를 만들어낸다", 35, WEIGHT).move_to(UP*3),
                    txt("모형: 정보 가격을 매긴다", 35, PRUNE).move_to(UP*1.3),
                    txt("같은 p에서 q를 개선", 36, ACCENT).move_to(DOWN*.6),
                    txt("평균 정보 비용을 낮춘다", 32, GOOD).move_to(DOWN*2.5),
                )
                self.play(FadeIn(self.stage), run_time=.4)
            else:
                chart = self.comparison(show_extra=True)
                question = txt("본래 비용을 빼면?", 34, ACCENT).move_to(DOWN*3.1)
                formula = txt("H(p,q) − H(p)", 38, PRUNE).move_to(DOWN*4.2)
                self.stage = VGroup(chart,question,formula)
                self.play(FadeIn(self.stage), run_time=.4)
            self.to(end)

    def distribution(self, values, label):
        group = VGroup(txt(label,29).move_to(UP*1.15))
        left = -3.6
        for symbol,value in zip("ABCD",values):
            width = 7.2*value
            box = Rectangle(width=width,height=.75,stroke_width=0,fill_color=COLORS[symbol],fill_opacity=.8).move_to([left+width/2,0,0])
            group.add(box,txt(symbol,24).move_to(box),txt(f"{value:g}",21,MUTED).move_to(box.get_center()+DOWN*.8))
            left += width
        return group

    def price_pair(self):
        group = VGroup()
        for y,label,value,color in ((1.7,"q(A)=0.7",PRICES_P[0],GOOD),(-1.5,"q(A)=0.1",PRICES_Q[0],PRUNE)):
            group.add(txt(label,31,color).move_to([0,y+1,0]))
            width = SCALE*value
            group.add(Rectangle(width=width,height=.55,stroke_width=0,fill_color=color,fill_opacity=.8).move_to([-3.3+width/2,y,0]),txt(f"{value:.3f} bits",29,color).move_to([0,y-.9,0]))
        return group

    def role(self,symbol,label,color):
        return VGroup(RoundedRectangle(width=3.6,height=3.6,corner_radius=.15,stroke_color=color,fill_opacity=0),txt(symbol,36,color,3.2).shift(UP*.7),txt(label,24,INK,3.2).shift(DOWN*.8))

    def comparison(self,show_extra=False):
        group = VGroup(txt("평균 이상적 정보 비용",28,MUTED).move_to(UP*4))
        for y,label,cost,color in ((2,"q=p",H_P,GOOD),(-.7,"예측 q",H_PQ,PRUNE)):
            group.add(txt(label,29,color).move_to([0,y+.9,0]))
            width = SCALE*cost
            group.add(Rectangle(width=width,height=.55,stroke_width=0,fill_color=color,fill_opacity=.75).move_to([-3.3+width/2,y,0]),txt(f"{cost:.3f} bits/기호",27,color).move_to([0,y-.8,0]))
        if show_extra:
            segment = Rectangle(width=SCALE*EXTRA,height=.55,stroke_color=ACCENT,stroke_width=2,fill_color=ACCENT,fill_opacity=.35).move_to([-3.3+SCALE*(H_P+EXTRA/2),-.7,0])
            group.add(segment,txt(f"추가 {EXTRA:.3f} bits/기호",27,ACCENT).move_to(DOWN*2.2))
        return group

    def model_meter(self, q):
        qa = txt(f"q(A)={q[0]:.3f}",35,WEIGHT).move_to(UP*2.4)
        cost = cross_entropy(P,q)
        price = txt(f"H(p,q)={cost:.3f} bits/기호",33,ACCENT).move_to(UP*.5)
        width = SCALE*cost
        bar = Rectangle(width=width,height=.65,stroke_width=0,fill_color=ACCENT,fill_opacity=.8).move_to([-3.3+width/2,-1,0])
        vector = txt("q=["+", ".join(f"{v:.3f}" for v in q)+"]",25,MUTED).move_to(DOWN*2.3)
        return VGroup(qa,price,bar,vector)

    def classification_cost(self,probability):
        cost = -np.log2(probability)
        # Fixed 0.95 frame units/bit for both rows; no minimum visible width.
        width = .95*cost
        bar = Rectangle(width=width,height=.55,stroke_width=0,fill_color=ACCENT,fill_opacity=.8).move_to([-3.3+width/2,0,0])
        return VGroup(txt(f"q(cat)={probability:g}",31,WEIGHT).move_to(UP*.9),bar,txt(f"−log₂ q(cat) = {cost:.4f} bits",29,ACCENT).move_to(DOWN*.9))

    def to(self,target):
        remain = target-self.time
        if remain < -.025:
            raise ValueError(f"Timeline overrun: {self.time} > {target}")
        width = max(.01,7.6*target/self.DURATION)
        if remain > 0:
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to([-3.8+width/2,-7.35,0]),run_time=min(.1,remain))
        if target-self.time > .001:
            self.wait(target-self.time)
