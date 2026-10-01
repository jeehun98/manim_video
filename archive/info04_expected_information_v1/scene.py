"""Entropy as the expectation of the random variable I(X)."""
import sys
from pathlib import Path
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import txt,INK,MUTED,WEIGHT,PRUNE,GOOD,ACCENT
from episodes.info04_expected_information.content import CUES,DURATION,PROBABILITIES,INFORMATION,entropy

class ExpectedInformation(Scene):
    DURATION=DURATION
    def construct(self):
        self.stage=VGroup();self.caption=VGroup()
        self.add(txt('INFORMATION THEORY  /  04',20,MUTED).move_to(UP*7.25),txt('결과 전의 정보량, 어떻게 말할까?',32).move_to(UP*6.4),Line([-3.8,5.8,0],[3.8,5.8,0],color=MUTED,stroke_opacity=.3))
        self.progress=Rectangle(width=.01,height=.04,stroke_width=0,fill_color=ACCENT,fill_opacity=1).move_to([-3.8,-7.35,0]);self.add(self.progress)
        captions=['결과를 보기 전의 정보량은?','X의 분포: 아직 선택되지 않은 결과','I(x) = −log₂ p(x)  /  단위 bit','최대값이나 최빈 결과만으로는 부족','I(X)도 확률변수','같은 분포에서 독립 반복 관측','단순 평균이 아닌, 확률로 가중한 평균','1.5 bits = 앞으로 받을 정보량의 기대값','엔트로피 = 평균 자기정보량','확실함: 0  /  네 결과 균등: 2 bits','H(X) = E[I(X)]','다음: 왜 균등할수록 엔트로피가 클까?']
        for i,(start,end,display,spoken) in enumerate(CUES):
            if i:self.play(FadeOut(self.stage),FadeOut(self.caption),run_time=.2)
            self.caption=txt(captions[i],27,INK).move_to(DOWN*5.9);self.play(FadeIn(self.caption),run_time=.2)
            if i==0:
                self.stage=VGroup(txt('아직 결과를 모른다면',36,MUTED).move_to(UP*2.3),txt('정보량 = ?',54,ACCENT).move_to(DOWN*.5))
                self.play(FadeIn(self.stage),run_time=.4)
            elif i in (1,2):
                self.stage=self.cards(i==2)
                self.play(FadeIn(self.stage),run_time=.4)
                if i==2:self.play(LaggedStart(*[Indicate(c[-1],color=GOOD) for c in self.stage],lag_ratio=.25),run_time=1)
            elif i==3:
                values=txt('1      2      2',57,GOOD).move_to(UP*2.2)
                maximum=txt('최대값: 2 ?',34,PRUNE).move_to(UP*.3)
                mode=txt('가장 흔한 결과: 1 ?',34,WEIGHT).move_to(DOWN*1.3)
                note=txt('어느 결과가 나올지 아직 모름',30,ACCENT).move_to(DOWN*3)
                self.stage=VGroup(values,maximum,mode,note);self.play(FadeIn(self.stage),run_time=.4)
            elif i==4:
                tree=self.tree();self.stage=tree;self.play(FadeIn(tree),run_time=.4)
                # Merge the two outcomes with the same self-information.
                dist=VGroup(txt('P(I(X)=1) = 0.5',29,WEIGHT).move_to(DOWN*2.4),txt('P(I(X)=2) = 0.5',29,GOOD).move_to(DOWN*3.4))
                self.stage.add(dist);self.play(FadeIn(dist),run_time=.4)
            elif i==5:
                # Deliberately constructed illustration, not a random-sample convergence claim.
                sequence='ABACABAC'
                columns=VGroup()
                for s in sequence:
                    columns.add(VGroup(txt(s,35,WEIGHT),txt('1' if s=='A' else '2',33,GOOD).shift(DOWN*1.25)))
                columns.arrange(RIGHT,buff=.45).move_to(UP*.8)
                title=txt('결과 → 정보량',31,ACCENT).move_to(UP*3)
                note=txt('반복 관측의 예시',26,MUTED).move_to(DOWN*2.6)
                self.stage=VGroup(columns,title,note)
                self.play(FadeIn(title),FadeIn(note),LaggedStart(*[FadeIn(c) for c in columns],lag_ratio=.15),run_time=1.5)
            elif i==6:
                self.stage=self.weighted_tiles();self.play(FadeIn(self.stage),run_time=.4)
                self.play(LaggedStart(*[Indicate(t,color=ACCENT) for t in self.stage[1]],lag_ratio=.15),run_time=.8)
                equation=txt('0.5×1 + 0.25×2 + 0.25×2',31,ACCENT).move_to(DOWN*3)
                self.stage.add(equation);self.play(FadeIn(equation),run_time=.4)
            elif i==7:
                self.stage=VGroup(txt('0.5×1 + 0.25×2 + 0.25×2',31).move_to(UP*3),txt('= 1.5 bits',55,ACCENT).move_to(UP*1.3),txt('1회 관측: 1 또는 2 bits',30,WEIGHT).move_to(DOWN*.6),txt('관측 전 기대값: 1.5 bits',33,GOOD).move_to(DOWN*2.2))
                self.play(FadeIn(self.stage),run_time=.4)
            elif i==8:
                expectation=txt('H(X) = E[I(X)]',44,ACCENT).move_to(UP*3)
                average=txt('= Σₓ p(x) I(x)',39,GOOD).move_to(UP*1.4)
                formula=txt('= −Σₓ p(x) log₂ p(x)',36,INK).move_to(DOWN*.2)
                name=txt('ENTROPY  /  엔트로피',38,ACCENT).move_to(DOWN*2.6)
                self.stage=VGroup(expectation,average,formula,name)
                self.play(FadeIn(expectation),FadeIn(average),run_time=.4)
                self.play(FadeIn(formula),FadeIn(name),run_time=.5)
            elif i==9:
                top=self.probability_bar((1,0,0),['A','B','C']).move_to(UP*2.7)
                h0=txt('P(A)=1  →  I(A)=0  →  H(X)=0',28,WEIGHT).move_to(UP*1.3)
                bottom=self.probability_bar((.25,)*4,list('ABCD')).move_to(DOWN*.6)
                h2=txt('각 결과: 2 bits  →  H(X)=2 bits',28,GOOD).move_to(DOWN*2)
                note=txt('고정된 결과 개수에서는 균등할 때 최대',24,MUTED).move_to(DOWN*3.6)
                self.stage=VGroup(top,h0,bottom,h2,note);self.play(FadeIn(self.stage),run_time=.4)
            elif i==10:
                left=self.summary('결과 x를 관측','I(x)','그 결과의 자기정보량',WEIGHT).move_to([-1.95,1,0])
                right=self.summary('결과를 보기 전','H(X)','I(X)의 기대값',GOOD).move_to([1.95,1,0])
                equation=txt('H(X) = E[I(X)]',40,ACCENT).move_to(DOWN*2.7)
                self.stage=VGroup(left,right,equation);self.play(FadeIn(self.stage),run_time=.4)
            else:
                uniform=(.25,)*4;peaked=(.97,.01,.01,.01)
                top=self.entropy_row(uniform,'균등한 네 결과').shift(UP*1.95)
                bottom=self.entropy_row(peaked,'한 결과에 집중').shift(DOWN*2.15)
                question=txt('같은 4개, 다른 엔트로피',32,ACCENT).move_to(UP*4.5)
                self.stage=VGroup(top,bottom,question);self.play(FadeIn(self.stage),run_time=.4)
            self.to(end)
    def cards(self,information):
        group=VGroup()
        for letter,p,value,color in zip('ABC',PROBABILITIES,INFORMATION,(WEIGHT,GOOD,PRUNE)):
            card=VGroup(RoundedRectangle(width=2.25,height=3.7,corner_radius=.15,stroke_color=color,fill_opacity=0),txt(letter,49,color).shift(UP*1),txt(f'p={p:g}',25,INK).shift(DOWN*.1))
            if information:card.add(txt(f'{value:g} '+('bit' if value==1 else 'bits'),30,ACCENT).shift(DOWN*1.2))
            group.add(card)
        return group.arrange(RIGHT,buff=.3).move_to(UP*.6)
    def tree(self):
        group=VGroup(txt('X → I(X)',39,ACCENT).move_to(UP*3.6))
        root=np.array([0,2.8,0])
        for x,letter,p,value in zip((-2.7,0,2.7),'ABC',PROBABILITIES,INFORMATION):
            end=np.array([x,.3,0])
            group.add(Line(root,end,color=WEIGHT,stroke_width=12*p),txt(str(p),24,MUTED).move_to((root+end)/2+RIGHT*(.45 if x>=0 else -.45)),txt(letter,37,WEIGHT).move_to([x,-.2,0]),txt(f'{value:g} bit'+('s' if value!=1 else ''),29,GOOD).move_to([x,-1.1,0]))
        return group
    def weighted_tiles(self):
        bar=self.probability_bar(PROBABILITIES,list('ABC')).move_to(UP*2.7)
        tiles=VGroup()
        # Four equiprobable tiles: A,A,B,C. Height is information, count is weight.
        for j,(letter,value,color) in enumerate(zip('AABC',(1,1,2,2),(WEIGHT,WEIGHT,GOOD,PRUNE))):
            x=(j-1.5)*1.5
            boxes=VGroup(*[Square(side_length=.65,stroke_color=color,fill_color=color,fill_opacity=.25).move_to([x,k*.75-.7,0]) for k in range(value)])
            tile=VGroup(boxes,txt(letter,29,color).move_to([x,-1.5,0]),txt('p=0.25',20,MUTED).move_to([x,-2.1,0]));tiles.add(tile)
        note=txt('4개의 같은 확률 조각',26,ACCENT).move_to(UP*1.5)
        return VGroup(bar,tiles,note)
    def probability_bar(self,probabilities,labels):
        group=VGroup();left=-3.6
        for p,label,color in zip(probabilities,labels,(WEIGHT,GOOD,PRUNE,ACCENT)):
            if p>0:
                width=7.2*p
                box=Rectangle(width=width,height=.65,stroke_width=0,fill_color=color,fill_opacity=.8).move_to([left+width/2,0,0]);group.add(box)
                if p>=.1:group.add(txt(label,24,INK).move_to(box))
                left+=width
        return group
    def entropy_row(self,probabilities,label):
        h=entropy(probabilities)
        top=self.probability_bar(probabilities,list('ABCD'))
        probability=txt('['+', '.join(f'{p:g}' for p in probabilities)+']',25,MUTED).move_to(UP*.8)
        title=txt(label,28,INK).move_to(UP*1.5)
        width=3*h
        bar=Rectangle(width=width,height=.4,stroke_width=0,fill_color=ACCENT,fill_opacity=.85).move_to([-3.6+width/2,-.9,0])
        value=txt(f'H = {h:.3f} bits',25,ACCENT).move_to([2.3,-.9,0])
        # Equal fixed scale: 3 frame units per bit. Labels are below to avoid overlap.
        value.move_to([0,-1.55,0])
        return VGroup(top,probability,title,bar,value)
    def summary(self,title,symbol,note,color):
        return VGroup(RoundedRectangle(width=3.6,height=3.7,corner_radius=.15,stroke_color=color,fill_opacity=0),txt(title,25,color,3.2).shift(UP*1.2),txt(symbol,44,ACCENT),txt(note,22,INK,3.2).shift(DOWN*1.2))
    def to(self,target):
        remain=target-self.time
        if remain<-.025:raise ValueError(f'Timeline overrun: {self.time} > {target}')
        width=max(.01,7.6*target/self.DURATION)
        if remain>0:self.play(self.progress.animate.stretch_to_fit_width(width).move_to([-3.8+width/2,-7.35,0]),run_time=min(.1,remain))
        if target-self.time>.001:self.wait(target-self.time)
