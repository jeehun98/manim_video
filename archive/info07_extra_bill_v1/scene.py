"""Remove the baseline, inspect signed event costs, and swap source roles."""
import sys
from pathlib import Path
from manim import *

sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import txt,INK,MUTED,WEIGHT,PRUNE,GOOD,ACCENT
from episodes.info07_extra_bill.content import (
    CUES,DURATION,P,Q,BASE,TOTAL,EXTRA,REVERSE,DELTAS,CONTRIBUTIONS,kl,model,
)

SCALE = 1.8


class ExtraPredictionBill(Scene):
    DURATION = DURATION

    def construct(self):
        self.stage,self.caption = VGroup(),VGroup()
        self.add(
            txt("INFORMATION THEORY  /  07",20,MUTED).move_to(UP*7.25),
            txt("틀린 예측 때문에 더 낸 비트는?",33).move_to(UP*6.4),
            Line([-3.8,5.8,0],[3.8,5.8,0],color=MUTED,stroke_opacity=.3),
        )
        self.progress = Rectangle(width=.01,height=.04,stroke_width=0,fill_color=ACCENT,fill_opacity=1).move_to([-3.8,-7.35,0])
        self.add(self.progress)
        captions = [
            "총비용에서, 추가분만 떼어낸다면?", "분포를 알아도 결과는 아직 모름", "본래 비용 + 예측 오류의 추가비용",
            "KL = 평균 추가 정보 비용", "사건별 차이: log₂[p(x)/q(x)]", "사건별 할인 가능 / 평균 KL ≥ 0",
            "데이터의 빈도를 만드는 쪽이 달라짐", "방향 있는 비용 / 보통 거리와 구별", "q=p → 추가분 0 / 본래 비용은 유지",
            "고정 p: Cross Entropy 최소화 = KL 최소화", "다음: X를 알면 Y의 비용은 얼마나 줄까?",
        ]
        for index,(start,end,display,spoken) in enumerate(CUES):
            if index:
                self.play(FadeOut(self.stage),FadeOut(self.caption),run_time=.2)
            self.caption = txt(captions[index],27).move_to(DOWN*5.9)
            self.play(FadeIn(self.caption),run_time=.2)
            if index == 0:
                self.stage = self.two_bills()
                self.play(FadeIn(self.stage),run_time=.4)
            elif index == 1:
                distribution = self.distribution(P,"실제 p를 알아도").shift(UP*2)
                note = txt("어떤 결과가 나왔는지는 표현해야 함",30).move_to(DOWN*.2)
                cost = txt(f"H(p) = {BASE:.3f} bits/기호",38,GOOD).move_to(DOWN*2.1)
                scope = txt("알려진 분포에서의 이상적 평균 비용",24,MUTED).move_to(DOWN*3.6)
                self.stage = VGroup(distribution,note,cost,scope)
                self.play(FadeIn(self.stage),run_time=.4)
            elif index == 2:
                base,extra = self.segments(1.6)
                title = txt(f"총비용 {TOTAL:.3f} bits/기호",32,PRUNE).move_to(UP*3.5)
                first = txt(f"본래 {BASE:.3f}",29,GOOD).move_to([-2,0,0])
                second = txt(f"추가 {EXTRA:.3f}",29,ACCENT).move_to([2,0,0])
                self.stage = VGroup(base,extra,title,first,second)
                self.play(FadeIn(self.stage),run_time=.4)
                self.play(extra.animate.shift(DOWN*3),run_time=.6)
                question = txt("H(p,q) − H(p)",40,ACCENT).move_to(DOWN*3.6)
                self.stage.add(question)
                self.play(FadeIn(question),run_time=.3)
            elif index == 3:
                formula = txt("D_KL(p‖q) = H(p,q) − H(p)",36,ACCENT).move_to(UP*2.9)
                name = txt("KL DIVERGENCE",45,GOOD).move_to(UP*.8)
                value = txt(f"= {EXTRA:.3f} bits/기호",40,ACCENT).move_to(DOWN*1.1)
                scope = txt("이상적 평균 추가비용 / 실제 코드 길이와 구별",24,MUTED).move_to(DOWN*3.6)
                self.stage = VGroup(formula,name,value,scope)
                self.play(FadeIn(self.stage),run_time=.4)
            elif index == 4:
                old_price = txt("실제 p의 가격: −log₂ p(x)",33,GOOD).move_to(UP*3.1)
                model_price = txt("모형 q의 가격: −log₂ q(x)",33,PRUNE).move_to(UP*1.6)
                difference = txt("모형 가격 − 실제 가격",29,MUTED).move_to(UP*.1)
                ratio = txt("= log₂ [p(x) / q(x)]",40,ACCENT).move_to(DOWN*1.4)
                event = txt(f"A에서는 +{DELTAS[0]:.3f} bits",30,WEIGHT).move_to(DOWN*3.2)
                self.stage = VGroup(old_price,model_price,difference,ratio,event)
                self.play(FadeIn(self.stage),run_time=.4)
            elif index == 5:
                heading = txt("사건별 차이  ×  실제 빈도",30,ACCENT).move_to(UP*4.1)
                rows = VGroup()
                for row,(symbol,p,delta,contribution) in enumerate(zip("ABCD",P,DELTAS,CONTRIBUTIONS)):
                    color = PRUNE if delta>0 else GOOD
                    rows.add(txt(f"{symbol}: {delta:+.3f} × {p:g} = {contribution:+.3f}",29,color).move_to([0,2.7-row*1.05,0]))
                total = txt(f"합계  +{EXTRA:.3f} bits/기호",37,ACCENT).move_to(DOWN*2.5)
                note = txt("각 항은 음수 가능 / 평균 KL은 0 이상",25,MUTED).move_to(DOWN*3.8)
                formula = txt("D_KL(p‖q) = Σₓ p(x) log₂[p(x)/q(x)]",27,ACCENT).move_to(DOWN*4.6)
                self.stage = VGroup(heading,rows,total,note,formula)
                self.play(FadeIn(heading),FadeIn(rows),run_time=.4)
                self.play(FadeIn(total),FadeIn(note),FadeIn(formula),run_time=.4)
            elif index == 6:
                self.stage = self.direction_pair()
                self.play(FadeIn(self.stage),run_time=.4)
            elif index == 7:
                self.stage = VGroup(
                    txt("p → q의 가격표",34,WEIGHT).move_to(UP*3),
                    txt("q → p의 가격표",34,PRUNE).move_to(UP*1.4),
                    txt("D_KL(p‖q) ≠ D_KL(q‖p)",36,ACCENT).move_to(DOWN*.3),
                    txt("이 예시: 평균내는 세계부터 다르다",29).move_to(DOWN*2.3),
                    txt("비용에는 방향이 있다",32,GOOD).move_to(DOWN*3.7),
                )
                self.play(FadeIn(self.stage),run_time=.4)
            elif index == 8:
                chart = self.meter(Q)
                self.stage = chart
                self.play(FadeIn(chart),run_time=.4)
                for t in (.65,.3,0):
                    self.play(Transform(chart,self.meter(model(t))),run_time=.5)
                note = txt("q=p / 추가비용 0",34,ACCENT).move_to(DOWN*3.8)
                self.stage.add(note)
                self.play(FadeIn(note),run_time=.3)
            elif index == 9:
                base,extra = self.segments(.2)
                title = txt("H(p,qθ) = H(p) + D_KL(p‖qθ)",32,ACCENT).move_to(UP*3.6)
                fixed = txt("H(p): 고정된 본래 비용",29,GOOD).move_to(UP*2)
                adjustable = txt("KL: 모델이 줄일 수 있는 추가분",29,ACCENT).move_to(DOWN*1.4)
                conclusion = txt("모형 qθ만 바꾸는 학습",30).move_to(DOWN*3.3)
                self.stage = VGroup(base,extra,title,fixed,adjustable,conclusion)
                self.play(FadeIn(self.stage),run_time=.4)
                self.play(extra.animate.stretch_to_fit_width(SCALE*EXTRA*.45).move_to([-3.3+SCALE*(BASE+EXTRA*.45/2),.2,0]),run_time=.7)
            else:
                x = txt("X = ?",44,ACCENT).move_to(UP*3.4)
                cards = VGroup(*[self.card(s) for s in "ABCD"]).arrange(RIGHT,buff=.3).move_to(UP*.5)
                label = txt("Y의 네 후보 / 같은 확률",27,WEIGHT).move_to(DOWN*1.3)
                hint = txt("X=0이면 Y는 A 또는 B",31,GOOD).move_to(DOWN*2.8)
                scope = txt("이 예시: X가 Y의 후보 절반을 알려줌",23,MUTED).move_to(DOWN*4)
                self.stage = VGroup(x,cards,label,hint,scope)
                self.play(FadeIn(self.stage),run_time=.4)
                self.play(Transform(x,txt("X = 0",44,ACCENT).move_to(x)),cards[2].animate.set_opacity(.1),cards[3].animate.set_opacity(.1),run_time=.6)
            self.to(end)

    def two_bills(self):
        group = VGroup(txt("이상적 평균 정보 비용",26,MUTED).move_to(UP*4))
        for y,label,cost,color in ((2,"본래 H(p)",BASE,GOOD),(-.9,"전체 H(p,q)",TOTAL,PRUNE)):
            width = SCALE*cost
            group.add(txt(label,29,color).move_to([0,y+.9,0]),Rectangle(width=width,height=.6,stroke_width=0,fill_color=color,fill_opacity=.8).move_to([-3.3+width/2,y,0]),txt(f"{cost:.3f} bits/기호",28,color).move_to([0,y-.9,0]))
        return group

    def segments(self,y):
        first = Rectangle(width=SCALE*BASE,height=.7,stroke_width=0,fill_color=GOOD,fill_opacity=.8).move_to([-3.3+SCALE*BASE/2,y,0])
        second = Rectangle(width=SCALE*EXTRA,height=.7,stroke_width=0,fill_color=ACCENT,fill_opacity=.8).move_to([-3.3+SCALE*(BASE+EXTRA/2),y,0])
        return first,second

    def distribution(self,values,label):
        group = VGroup(txt(label,29).move_to(UP*1.1))
        left = -3.6
        for symbol,p,color in zip("ABCD",values,(WEIGHT,GOOD,PRUNE,ACCENT)):
            width = 7.2*p
            rectangle = Rectangle(width=width,height=.7,stroke_width=0,fill_color=color,fill_opacity=.8).move_to([left+width/2,0,0])
            group.add(rectangle,txt(symbol,24).move_to(rectangle),txt(f"{p:g}",21,MUTED).move_to(rectangle.get_center()+DOWN*.8))
            left += width
        return group

    def direction_pair(self):
        group = VGroup()
        for y,label,value,color in ((2.2,"현실 p / 가격표 q",EXTRA,WEIGHT),(-1.5,"현실 q / 가격표 p",REVERSE,PRUNE)):
            width = SCALE*value
            group.add(txt(label,31,color).move_to([0,y+1,0]),Rectangle(width=width,height=.6,stroke_width=0,fill_color=color,fill_opacity=.8).move_to([-3.3+width/2,y,0]),txt(f"KL = {value:.3f} bits/기호",28,color).move_to([0,y-.9,0]))
        return group

    def meter(self,q):
        extra = max(0.,kl(P,q))
        fixed = Rectangle(width=SCALE*BASE,height=.7,stroke_width=0,fill_color=GOOD,fill_opacity=.8).move_to([-3.3+SCALE*BASE/2,.1,0])
        adjustable = Rectangle(width=SCALE*extra,height=.7,stroke_width=0,fill_color=ACCENT,fill_opacity=.8 if extra>0 else 0).move_to([-3.3+SCALE*(BASE+extra/2),.1,0])
        return VGroup(txt("실제 p는 고정",29,MUTED).move_to(UP*4),txt(f"q(A)={q[0]:.3f}",33,WEIGHT).move_to(UP*2.4),fixed,adjustable,txt(f"본래 {BASE:.3f} / 추가 {extra:.3f} bits",28).move_to(DOWN*1.4),txt("q=["+", ".join(f"{a:.3f}" for a in q)+"]",25,MUTED).move_to(DOWN*2.5))

    def card(self,symbol):
        return VGroup(RoundedRectangle(width=1.5,height=1.6,corner_radius=.12,stroke_color=WEIGHT,fill_color=WEIGHT,fill_opacity=.08),txt(symbol,40,WEIGHT))

    def to(self,target):
        remain = target-self.time
        if remain < -.025:
            raise ValueError(f"Timeline overrun: {self.time} > {target}")
        width = max(.01,7.6*target/self.DURATION)
        if remain > 0:
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to([-3.8+width/2,-7.35,0]),run_time=min(.1,remain))
        if target-self.time > .001:
            self.wait(target-self.time)
