"""A logarithm turns multiplicative contraction into additive depth."""
import sys
from pathlib import Path
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import txt,INK,MUTED,WEIGHT,PRUNE,GOOD,ACCENT
from episodes.info03_multiplication_depth.content import CUES,DURATION

class MultiplicationDepth(Scene):
    DURATION=DURATION
    def construct(self):
        self.stage=VGroup();self.caption=VGroup()
        self.add(txt('INFORMATION THEORY  /  03',20,MUTED).move_to(UP*7.25),txt('확률은 곱셈, 정보는 덧셈',35).move_to(UP*6.4),Line([-3.8,5.8,0],[3.8,5.8,0],color=MUTED,stroke_opacity=.3))
        self.progress=Rectangle(width=.01,height=.04,stroke_width=0,fill_color=ACCENT,fill_opacity=1).move_to([-3.8,-7.35,0]);self.add(self.progress)
        captions=['서로 다른 구조를 잇는 함수는?','서로 독립인 공정한 동전','독립일 때, 결합 확률은 곱셈','독립 관측의 자기정보량은 덧셈','곱셈 → 번역기 → 덧셈','확률은 반복해서 반으로','반으로 줄인 깊이는 한 칸씩','로그: 곱셈의 깊이를 세는 좌표계','−log₂ p: 낮은 확률 → 큰 값','단위 bit: 밑은 2','확률 1/4  ↔  정보량 2 bits','공식보다, 연결하는 구조','다음: 결과를 보기 전의 평균 정보량']
        for i,(start,end,display,spoken) in enumerate(CUES):
            # The key shrinking-bar sequence persists across its two narration cues.
            keep=i==6
            if i:
                self.play(FadeOut(self.caption),*([] if keep else [FadeOut(self.stage)]),run_time=.2)
            self.caption=txt(captions[i],28,INK).move_to(DOWN*5.9)
            self.play(FadeIn(self.caption),run_time=.2)
            if i==0:
                self.stage=VGroup(txt('×',100,WEIGHT).move_to(UP*2.2),txt('?',57,ACCENT),txt('+',100,GOOD).move_to(DOWN*2.2))
                self.play(FadeIn(self.stage),run_time=.4)
            elif i==1:
                coins=VGroup(self.coin('H','동전 1'),self.coin('T','동전 2')).arrange(RIGHT,buff=.9)
                note=txt('독립 · 공정',30,ACCENT).move_to(UP*3.6)
                self.stage=VGroup(coins,note);self.play(FadeIn(self.stage),run_time=.4)
                self.play(LaggedStart(*[Indicate(c[0],color=ACCENT) for c in coins],lag_ratio=.4),run_time=1)
            elif i==2:
                self.stage=VGroup(txt('P(H₁) = 1/2',35,WEIGHT).move_to(UP*2.8),txt('P(T₂) = 1/2',35,WEIGHT).move_to(UP*1.4),txt('P(H₁, T₂)',32,MUTED).move_to(DOWN*.2),txt('= 1/2 × 1/2 = 1/4',39,ACCENT).move_to(DOWN*1.7),txt('독립인 경우',24,MUTED).move_to(DOWN*3))
                self.play(FadeIn(self.stage),run_time=.4)
            elif i==3:
                b1=self.block('I₁');b2=self.block('I₂')
                blocks=VGroup(b1,b2).arrange(RIGHT,buff=.4)
                title=txt('독립 관측의 정보량',32,ACCENT).move_to(UP*3.3)
                equation=txt('I(첫 결과, 둘째 결과) = I₁ + I₂',31,GOOD).move_to(DOWN*2.3)
                self.stage=VGroup(blocks,title,equation);self.play(FadeIn(b1),FadeIn(title),run_time=.4)
                self.play(FadeIn(b2,shift=LEFT*.3),FadeIn(equation),run_time=.5)
            elif i==4:
                self.stage=self.translator('?')
                condition=txt('f(p₁p₂) = f(p₁) + f(p₂)',35,ACCENT).move_to(DOWN*3.2)
                self.stage.add(condition);self.play(FadeIn(self.stage),run_time=.4)
            elif i==5:
                self.depth=self.depth_chart(0)
                self.stage=self.depth
                self.play(FadeIn(self.stage),run_time=.4)
                for n in (1,2,3):
                    self.play(Transform(self.depth,self.depth_chart(n)),run_time=.6)
                    self.wait(.35)
            elif i==6:
                for n in (0,1,2,3):
                    self.play(Transform(self.depth,self.depth_chart(n)),run_time=.5)
                    self.wait(.25)
                note=txt('곱셈으로 줄어든 양 → 덧셈으로 센 깊이',27,ACCENT).move_to(DOWN*3.5)
                self.stage.add(note);self.play(FadeIn(note),run_time=.3)
            elif i==7:
                self.stage=self.translator('log₂')
                condition=txt('log₂(p₁p₂) = log₂p₁ + log₂p₂',32,ACCENT).move_to(DOWN*3.2)
                self.stage.add(condition);self.play(FadeIn(self.stage),run_time=.4)
            elif i==8:
                table=self.sign_table(False)
                title=txt('방향을 뒤집으면',33,ACCENT).move_to(UP*4)
                self.stage=VGroup(table,title);self.play(FadeIn(self.stage),run_time=.4)
                self.wait(1)
                self.play(Transform(table,self.sign_table(True)),run_time=.7)
            elif i==9:
                equation=txt('I(x) = −log₂ p(x)',49,ACCENT).move_to(UP*2.7)
                depth=self.depth_chart(3).scale(.8).move_to(DOWN*.5)
                unit=txt('1/2 → 1 bit   /   1/8 → 3 bits',28,GOOD).move_to(DOWN*3.7)
                self.stage=VGroup(equation,depth,unit);self.play(FadeIn(self.stage),run_time=.4)
            elif i==10:
                coins=VGroup(self.coin('H','1 bit'),self.coin('T','1 bit')).arrange(RIGHT,buff=.9).move_to(UP*1.5)
                probability=txt('1/2 × 1/2 = 1/4',40,WEIGHT).move_to(DOWN*.8)
                information=txt('1 bit + 1 bit = 2 bits',37,GOOD).move_to(DOWN*2.5)
                self.stage=VGroup(coins,probability,information);self.play(FadeIn(self.stage),run_time=.4)
            elif i==11:
                self.stage=self.translator('−log₂')
                formula=txt('I(x) = −log₂ p(x)',40,ACCENT).move_to(DOWN*3.2)
                self.stage.add(formula);self.play(FadeIn(self.stage),run_time=.4)
            else:
                self.stage=VGroup(txt('결과를 보기 전에는?',37,ACCENT).move_to(UP*3.5),txt('x₁     x₂     x₃     x₄',37,WEIGHT).move_to(UP*1.5),txt('I(x₁)  I(x₂)  I(x₃)  I(x₄)',31,GOOD).move_to(DOWN*.2),txt('얻게 될 정보량의 평균은?',34).move_to(DOWN*2),txt('04  /  엔트로피',30,MUTED).move_to(DOWN*3.6))
                self.play(FadeIn(self.stage),run_time=.4)
            self.to(end)
    def coin(self,result,label):
        return VGroup(VGroup(Circle(radius=1,stroke_color=WEIGHT,fill_color=WEIGHT,fill_opacity=.1),txt(result,62,INK)),txt(label,25,MUTED).shift(DOWN*1.6))
    def block(self,label):
        return VGroup(RoundedRectangle(width=2,height=1.3,corner_radius=.15,stroke_color=GOOD,fill_color=GOOD,fill_opacity=.1),txt(label,38,GOOD))
    def translator(self,label):
        title=txt('독립인 두 결과를 함께 관측',26,MUTED).move_to(UP*4)
        top=txt('확률:  p₁ × p₂',41,WEIGHT).move_to(UP*2.6)
        box=VGroup(RoundedRectangle(width=3.1,height=1.3,corner_radius=.16,stroke_color=ACCENT,fill_color=ACCENT,fill_opacity=.08),txt(label,42,ACCENT))
        arrows=VGroup(Arrow([0,1.8,0],[0,.8,0],buff=.08,color=MUTED),Arrow([0,-.8,0],[0,-1.8,0],buff=.08,color=MUTED))
        bottom=txt('정보량:  I₁ + I₂',41,GOOD).move_to(DOWN*2.3)
        # For unsigned log, the output is logarithmic values, not positive information.
        if label=='log₂':bottom=txt('log₂p₁ + log₂p₂',36,GOOD).move_to(DOWN*2.3)
        return VGroup(title,top,box,arrows,bottom)
    def depth_chart(self,n):
        group=VGroup(txt('확률',29,WEIGHT).move_to([-2,3,0]),txt('반으로 줄인 횟수',27,GOOD).move_to([1.7,3,0]))
        labels=('1','1/2','1/4','1/8')
        for j in range(4):
            y=1.7-j*1.1
            opacity=1 if j<=n else .13
            number=txt(labels[j],29,WEIGHT).move_to([-3.35,y,0])
            # Equal-ratio shrinkage on a fixed linear probability width.
            bar=Rectangle(width=2.4/(2**j),height=.35,stroke_width=0,fill_color=WEIGHT,fill_opacity=.85).move_to([-2.7+1.2/(2**j),y,0])
            count=txt(str(j),32,GOOD).move_to([.45,y,0])
            units=VGroup(*[Square(side_length=.48,stroke_color=GOOD,fill_color=GOOD,fill_opacity=.2).move_to([1.25+k*.58,y,0]) for k in range(j)])
            row=VGroup(number,bar,count,units);row.set_opacity(opacity);group.add(row)
        group.add(txt('× 1/2',25,WEIGHT).move_to([-2,-2.9,0]),txt('+ 1',25,GOOD).move_to([1.7,-2.9,0]))
        return group
    def sign_table(self,positive):
        group=VGroup(txt('p',28,WEIGHT).move_to([-2.7,2.7,0]),txt('−log₂p' if positive else 'log₂p',32,GOOD if positive else PRUNE).move_to([1.5,2.7,0]))
        for j,label in enumerate(('1','1/2','1/4','1/8')):
            y=1.5-j*1.05
            group.add(txt(label,32,WEIGHT).move_to([-2.7,y,0]),txt(str(j if positive else -j),36,GOOD if positive else PRUNE).move_to([1.5,y,0]))
        return group
    def to(self,target):
        remain=target-self.time
        if remain<-.025:raise ValueError(f'Timeline overrun: {self.time} > {target}')
        width=max(.01,7.6*target/self.DURATION)
        if remain>0:self.play(self.progress.animate.stretch_to_fit_width(width).move_to([-3.8+width/2,-7.35,0]),run_time=min(.1,remain))
        if target-self.time>.001:self.wait(target-self.time)
