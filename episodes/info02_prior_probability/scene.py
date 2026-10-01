"""Prior predictive probabilities and self-information of exact outcomes."""
import sys
from pathlib import Path
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import txt,INK,MUTED,WEIGHT,PRUNE,GOOD,ACCENT
from episodes.info02_prior_probability.content import CUES,DURATION

class PriorProbabilityInformation(Scene):
    DURATION=DURATION
    def construct(self):
        self.stage=VGroup();self.caption=VGroup()
        self.add(txt('INFORMATION THEORY  /  02',20,MUTED).move_to(UP*7.25),txt('같은 결과, 다른 정보량',36).move_to(UP*6.4),Line([-3.8,5.8,0],[3.8,5.8,0],color=MUTED,stroke_opacity=.3))
        self.progress=Rectangle(width=.01,height=.04,stroke_width=0,fill_color=ACCENT,fill_opacity=1).move_to([-3.8,-7.35,0]);self.add(self.progress)
        captions=['같은 A, 같은 정보?','결과는 같고, 관측 전 예측은 다름','믿음 → 확률분포로 표현한 예측','확률과 믿음은 같은 말이 아님','첫 사람: B의 사전 확률 0.5','두 번째 사람: B의 사전 확률 0.01','제외한 후보는 둘 다 B 하나','이번 결과: B','낮은 사전 확률 → 큰 자기정보량','결과 + 관측 전 확률','다음: 확률을 정보량으로']
        for i,(start,end,display,spoken) in enumerate(CUES):
            if i:self.play(FadeOut(self.stage),FadeOut(self.caption),run_time=.2)
            self.caption=txt(captions[i],28,INK).move_to(DOWN*5.9);self.play(FadeIn(self.caption),run_time=.2)
            if i==0:
                left=self.result('첫 사람');right=self.result('두 번째 사람')
                self.stage=VGroup(left,right).arrange(RIGHT,buff=.6)
                self.play(FadeIn(self.stage),run_time=.4)
            elif i in (1,4,5,6):
                top=self.row('첫 사람',.5).move_to(UP*1.8)
                bottom=self.row('두 번째 사람',.99).move_to(DOWN*1.5)
                self.stage=VGroup(top,bottom)
                self.play(FadeIn(self.stage),run_time=.4)
                if i in (4,5):
                    active=top if i==4 else bottom
                    inactive=bottom if i==4 else top
                    self.play(inactive.animate.set_opacity(.22),run_time=.3)
                    self.wait(.5)
                    self.play(active[2].animate.set_fill(opacity=.06).set_stroke(opacity=.1),run_time=.5)
                    observed=txt('A 관측 → B 제외',27,GOOD).next_to(active,DOWN,buff=.3)
                    self.stage.add(observed);self.play(FadeIn(observed),run_time=.3)
                if i==6:
                    note=txt('제외한 개수: 1 = 1',30,ACCENT).move_to(DOWN*3.8)
                    self.stage.add(note);self.play(FadeIn(note),run_time=.35)
            elif i==2:
                self.stage=VGroup(txt('믿음',44,ACCENT).move_to(UP*3),txt('관측 전에 가진 예측',32).move_to(UP*1.7),txt('↓ 数値化'.replace('数値化','수치로 표현'),30,MUTED).move_to(UP*.4),txt('확률분포',44,WEIGHT).move_to(DOWN*.9),txt('P(A) = 0.99   /   P(B) = 0.01',28).move_to(DOWN*2.2))
                self.play(FadeIn(self.stage),run_time=.4)
            elif i==3:
                self.stage=VGroup(txt('확률: 사건에 부여한 수치',36,WEIGHT).move_to(UP*2.7),txt('0 ≤ P(x) ≤ 1',36).move_to(UP*1.3),txt('개인의 예측을 표현할 수도',29).move_to(DOWN*.3),txt('확률 모형의 특성을 나타낼 수도',29).move_to(DOWN*1.5),txt('이 예시: 관측 전 예측분포',27,ACCENT).move_to(DOWN*3))
                self.play(FadeIn(self.stage),run_time=.4)
            elif i==7:
                row=self.row('두 번째 사람 · 관측 전',.99).move_to(UP*1.3)
                self.stage=VGroup(row)
                self.play(FadeIn(row),run_time=.4);self.wait(.8)
                result=txt('Result = B',40,PRUNE).move_to(DOWN*1.5)
                self.stage.add(result);self.play(FadeIn(result),run_time=.3)
                self.play(row[1].animate.set_fill(opacity=.04).set_stroke(opacity=.1),run_time=.6)
                note=txt('사전 확률 0.01인 결과를 관측',28,ACCENT).move_to(DOWN*3)
                self.stage.add(note);self.play(FadeIn(note),run_time=.3)
            elif i==8:
                rows=VGroup(*[VGroup(txt(f'P(x) = {s}',32,WEIGHT),txt(label,29,ACCENT)).arrange(RIGHT,buff=.7) for s,label in [('0.99','정보량 작음'),('0.5','중간'),('0.01','정보량 큼')]])
                # Qualitative ordering only; no arbitrary linear information bars.
                rows.arrange(DOWN,buff=.9).move_to(UP*.7)
                note=txt('심리적 놀라움의 크기를 재는 값은 아님',25,MUTED).move_to(DOWN*3)
                self.stage=VGroup(rows,note);self.play(FadeIn(self.stage),run_time=.4)
            elif i==9:
                self.stage=VGroup(txt('관측한 결과 x',37,ACCENT).move_to(UP*2.8),txt('+',40,MUTED).move_to(UP*1.3),txt('관측 전 P(x)',37,WEIGHT).move_to(DOWN*.2),txt('↓',36,MUTED).move_to(DOWN*1.5),txt('이 결과의 자기정보량',35,GOOD).move_to(DOWN*2.8))
                self.play(FadeIn(self.stage),run_time=.4)
            else:
                labels=VGroup(*[txt(f'P(x) = {s}',30,WEIGHT) for s in ('0.99','0.5','0.01')]).arrange(DOWN,buff=.8).move_to(LEFT*1.7)
                boxes=VGroup(*[RoundedRectangle(width=2.3,height=.55,corner_radius=.1,stroke_color=ACCENT,fill_opacity=0).move_to([1.7,t.get_y(),0]) for t in labels])
                question=txt('확률 → 정보량 ?',37,ACCENT).move_to(UP*3.6)
                note=txt('03  /  정보량을 숫자로 만드는 법',28).move_to(DOWN*3)
                self.stage=VGroup(labels,boxes,question,note);self.play(FadeIn(self.stage),run_time=.4)
            self.to(end)
    def result(self,label):
        return VGroup(RoundedRectangle(width=3.2,height=3.8,corner_radius=.2,stroke_color=MUTED,fill_opacity=0),txt(label,26,MUTED).shift(UP*1.25),txt('A',72,ACCENT))
    def row(self,label,pa):
        width=7.2
        a=Rectangle(width=width*pa,height=.75,stroke_width=0,fill_color=WEIGHT,fill_opacity=.85).move_to([-width/2+width*pa/2,0,0])
        b=Rectangle(width=width*(1-pa),height=.75,stroke_width=0,fill_color=PRUNE,fill_opacity=.85).move_to([width/2-width*(1-pa)/2,0,0])
        title=txt(label,27,MUTED).move_to(UP*1.35)
        numbers=txt(f'P(A) = {pa:g}    P(B) = {1-pa:.2g}',29,INK).move_to(UP*.75)
        keys=txt('A',24,WEIGHT).move_to([-3.3,-.8,0]);keyb=txt('B',24,PRUNE).move_to([3.3,-.8,0])
        return VGroup(title,a,b,numbers,keys,keyb)
    def to(self,target):
        remain=target-self.time
        if remain<-.02:raise ValueError(f'Timeline overrun: {self.time} > {target}')
        width=max(.01,7.6*target/self.DURATION)
        if remain>0:self.play(self.progress.animate.stretch_to_fit_width(width).move_to([-3.8+width/2,-7.35,0]),run_time=min(.1,remain))
        if target-self.time>.001:self.wait(target-self.time)
