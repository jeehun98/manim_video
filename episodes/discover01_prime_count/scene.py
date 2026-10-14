"""Prime positions -> exact counting staircase -> asymptotic ratio."""
import sys
from pathlib import Path
import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import txt, INK, MUTED, WEIGHT, GOOD

ORANGE = "#FFAA61"


def prime_data(n=1_000_000):
    mask = np.ones(n + 1, dtype=bool)
    mask[:2] = False
    for p in range(2, int(n ** .5) + 1):
        if mask[p]:
            mask[p*p::p] = False
    return np.flatnonzero(mask), np.cumsum(mask)


class PrimeCountDiscovery(Scene):
    def construct(self):
        self.primes, self.counts = prime_data()
        self.add(txt("정답을 찾는 것과 이해하는 것  /  01", 21, MUTED).move_to(UP*7.25))
        self.add(txt("소수는 불규칙한데,", 37).move_to(UP*6.5),
                 txt("왜 개수는 예측할 수 있을까?", 34).move_to(UP*5.85))
        self.cap = VGroup()
        self.heading = VGroup()
        self.subtitle("다음 소수는 어디에 있을까?", "간격만으로 간단히 예측하기는 어렵습니다")
        grid = VGroup(*[txt(str(i), 24, MUTED).move_to(
            [-3.3 + ((i-1)%10)*.73, 3.65-((i-1)//10)*.67, 0]) for i in range(1,101)])
        self.play(LaggedStart(*[FadeIn(m) for m in grid], lag_ratio=.012), run_time=2)
        self.play(*[m.animate.set_color(WEIGHT) if i in self.primes else m.animate.set_opacity(.12)
                    for i,m in enumerate(grid,1)], run_time=1.5)
        self.wait(2)
        self.subtitle("위치 대신, 개수를 세면?", "소수 하나를 지날 때마다 1씩 올라갑니다")
        axis = NumberLine(x_range=[0,100,20], length=7.2, include_numbers=False).move_to(DOWN*3.8)
        dots = VGroup(*[Dot(axis.n2p(p), radius=.043, color=WEIGHT) for p in self.primes[self.primes<=100]])
        self.play(FadeIn(axis), *[ReplacementTransform(grid[p-1], dots[j]) for j,p in enumerate(self.primes[self.primes<=100])],
                  *[FadeOut(grid[i-1]) for i in range(1,101) if i not in self.primes], run_time=1.5)
        graph = self.graph(100)
        axes, labels, step, curve = graph
        self.play(Create(axes), FadeIn(labels), run_time=.8)
        tracker = ValueTracker(0)
        counter = always_redraw(lambda: txt(f"π(x) = {int(self.counts[min(100,int(tracker.get_value()))])}", 37, WEIGHT).move_to(UP*3.9))
        marker = always_redraw(lambda: Dot(axis.n2p(tracker.get_value()), color=ORANGE, radius=.075))
        self.add(counter, marker)
        self.play(Create(step), tracker.animate.set_value(100), run_time=6, rate_func=linear)
        counter.clear_updaters(); marker.clear_updaters()
        self.wait(1)
        definition = txt("π(x) = x 이하 소수의 개수", 28, WEIGHT).move_to(UP*3.1)
        self.play(FadeIn(definition), FadeOut(marker), run_time=.6)
        self.wait(2)
        self.subtitle("불규칙한 계단, 매끄러운 곡선", "숫자 하나하나에서 전체 흐름으로")
        formula = txt("x / ln x", 42, ORANGE).move_to(UP*4)
        legend = VGroup(txt("● 실제 개수 π(x)", 23, WEIGHT), txt("● 근사 x / ln x", 23, ORANGE)).arrange(RIGHT,buff=.5).move_to(DOWN*3)
        self.play(FadeOut(counter), FadeIn(formula), FadeIn(legend), run_time=.7)
        self.play(Create(curve), run_time=3)
        self.wait(3)
        values = self.values(100)
        self.play(FadeOut(axis), FadeOut(dots), FadeIn(values), run_time=.8)
        self.remove(axis, *dots)
        self.subtitle("정확히 같지는 않습니다", "100 이하: 실제 25개, 근사 약 22개")
        self.wait(4)
        self.subtitle("범위를 더 넓혀보면", "축의 범위도 함께 바뀝니다")
        current = VGroup(axes,labels,step,curve)
        for maximum in (10_000,1_000_000):
            new = VGroup(*self.graph(maximum))
            newvalues = self.values(maximum)
            self.play(FadeOut(current), FadeOut(values), run_time=.5)
            self.remove(*current)
            self.play(FadeIn(new), FadeIn(newvalues), run_time=1.5)
            current, values = new, newvalues
            self.wait(2)
        self.subtitle("값의 차이보다 비율을 봅니다", "실제 개수 ÷ 근삿값")
        self.play(FadeOut(current),FadeOut(definition),FadeOut(formula),FadeOut(legend),FadeOut(values),run_time=.8)
        ratio_axes = Axes(x_range=[2,6,1], y_range=[1,1.2,.05],x_length=6.8,y_length=4.8,
                          tips=False,axis_config={"color":MUTED,"include_ticks":True}).move_to(DOWN*.1)
        reference = DashedLine(ratio_axes.c2p(2,1),ratio_axes.c2p(6,1),color=GOOD)
        ratio_labels=VGroup(*[txt(s,21,MUTED).move_to(ratio_axes.c2p(k,1)+DOWN*.4)
            for k,s in zip(range(2,7),("100","1천","1만","10만","100만"))],
            txt("1.00",22,GOOD).next_to(ratio_axes.c2p(2,1),LEFT,buff=.12),
            txt("1.20",22,MUTED).next_to(ratio_axes.c2p(2,1.2),LEFT,buff=.12),
            txt("x  ·  로그 눈금",21,MUTED).move_to(DOWN*3.3))
        self.play(Create(ratio_axes),Create(reference),FadeIn(ratio_labels),run_time=1)
        pts=[]
        for k in range(2,7):
            n=10**k
            ratio=self.counts[n]/(n/np.log(n))
            pt=ratio_axes.c2p(k,ratio); pts.append(pt)
            dot=Dot(pt,color=WEIGHT,radius=.07)
            label=txt(f"{ratio:.3f}",22,WEIGHT).move_to(pt+UP*.38)
            self.play(FadeIn(dot),FadeIn(label),run_time=.35)
            if k>2:
                self.play(Create(Line(pts[-2],pt,color=WEIGHT,stroke_width=3)),run_time=.45)
        note=txt("100 → 1,000에서는 비율이 잠시 커집니다",23,ORANGE).move_to(UP*3.6)
        self.play(FadeIn(note),run_time=.6); self.wait(2.5)
        self.subtitle("소수정리  ·  Prime Number Theorem", "x가 무한히 커질 때, 비율은 1로 수렴합니다")
        theorem=txt("π(x) / (x / ln x) → 1",38,INK).move_to(UP*4.3)
        self.play(FadeIn(theorem),FadeOut(note),run_time=.8)
        error=txt("상대 오차 → 0",33,GOOD).move_to(DOWN*4)
        caution=txt("모든 구간에서 단조롭게 줄어든다는 뜻은 아닙니다",21,MUTED).move_to(DOWN*4.7)
        self.play(FadeIn(error),FadeIn(caution),run_time=.8); self.wait(4)
        self.subtitle("불규칙성과 질서는 공존합니다", "개별 위치 ≠ 전체 분포")
        self.play(*[FadeOut(m) for m in list(self.mobjects) if m not in [self.cap] and m.get_center()[1]<5.3],run_time=1)
        finalgraph=VGroup(*self.graph(100)).scale(.84).move_to(DOWN*.7)
        finaldots=VGroup(*[Dot([-3.3+p/100*6.6,3.4,0],radius=.047,color=WEIGHT) for p in self.primes[self.primes<=100]])
        self.play(FadeIn(finaldots),Create(finalgraph),run_time=2)
        conclusion=txt("하나씩 보면 불규칙 · 함께 보면 규칙",28,GOOD).move_to(DOWN*4.5)
        self.play(FadeIn(conclusion),run_time=.8); self.wait(4)

    def subtitle(self,a,b):
        new=VGroup(txt(a,30,INK),txt(b,23,MUTED)).arrange(DOWN,buff=.25).move_to(DOWN*6.25)
        if self.cap.submobjects:
            self.play(ReplacementTransform(self.cap,new),run_time=.4)
        else:
            self.play(FadeIn(new),run_time=.4)
        self.cap=new

    def graph(self,maximum):
        ymax={100:30,10_000:1400,1_000_000:90000}[maximum]
        axes=Axes(x_range=[0,maximum,maximum/5],y_range=[0,ymax,ymax/3],
                  x_length=6.8,y_length=4.6,tips=False,axis_config={"color":MUTED}).move_to(DOWN*.05)
        labels=VGroup(txt("0",20,MUTED).next_to(axes.c2p(0,0),DOWN),
                      txt(f"{maximum:,}",23,MUTED).next_to(axes.c2p(maximum,0),DOWN),
                      txt(f"{ymax:,}",22,MUTED).next_to(axes.c2p(0,ymax),LEFT,buff=.12),
                      txt("x",24,MUTED).next_to(axes.c2p(maximum,0),RIGHT,buff=.15))
        # Every vertical rise is at an actual prime. Large ranges are pixel-dense.
        ps=self.primes[self.primes<=maximum]
        points=[axes.c2p(0,0)]
        for j,p in enumerate(ps):
            points.extend((axes.c2p(p,j),axes.c2p(p,j+1)))
        points.append(axes.c2p(maximum,len(ps)))
        step=VMobject(color=WEIGHT,stroke_width=3).set_points_as_corners(points)
        curve=axes.plot(lambda x:x/np.log(x),x_range=[2,maximum,maximum/500],color=ORANGE,stroke_width=4,use_smoothing=False)
        return axes,labels,step,curve

    def values(self,n):
        return VGroup(txt(f"x = {n:,}",27,MUTED),
                      txt(f"실제  {self.counts[n]:,}   /   근사  {n/np.log(n):,.1f}",29,INK)).arrange(DOWN,buff=.25).move_to(DOWN*4.1)
