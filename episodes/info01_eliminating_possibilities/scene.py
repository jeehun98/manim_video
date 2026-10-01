"""Information 01: exact observations eliminate incompatible outcomes."""
import sys
from pathlib import Path
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import txt, INK, MUTED, WEIGHT, PRUNE, GOOD, ACCENT
from episodes.info01_eliminating_possibilities.content import CUES, DURATION

class InformationEliminates(Scene):
    DURATION=DURATION
    def construct(self):
        self.stage=VGroup()
        self.add(txt('INFORMATION THEORY  /  01',20,MUTED).move_to(UP*7.25),
                 txt('정보는 무엇을 줄이는가?',36).move_to(UP*6.4),
                 Line([-3.8,5.8,0],[3.8,5.8,0],color=MUTED,stroke_opacity=.3))
        self.caption=VGroup()
        self.progress=Rectangle(width=.01,height=.04,fill_color=ACCENT,fill_opacity=1,stroke_width=0).move_to([-3.8,-7.35,0])
        self.add(self.progress)
        for i,(start,end,display,spoken) in enumerate(CUES):
            if i: self.play(FadeOut(self.stage),FadeOut(self.caption),run_time=.18)
            # Short semantic captions leave room for separately supplied SRT.
            captions=['모름 = 아직 열린 가능성','관측 전: {A, B}','관측 후: {A}','같은 결과, 같은 정보?','B를 제외할 수 있음','이미 확실했다면 변화 없음','정보량은 관측 전 확률에 달림','드문 결과일수록 정보량 ↑','정보는 가능성을 좁힌다','다음: 확률로 정보량 재기']
            self.caption=txt(captions[i],29,INK).move_to(DOWN*5.9)
            self.play(FadeIn(self.caption),run_time=.2)
            if i in (0,1,2):
                a,b=self.card('A',WEIGHT),self.card('B',PRUNE)
                a.move_to([-1.9,.5,0]); b.move_to([1.9,.5,0])
                label=txt('가능한 세계' if i<2 else 'Result = A',32,ACCENT).move_to(UP*3.4)
                self.stage=VGroup(a,b,label)
                self.play(FadeIn(self.stage),run_time=.45)
                if i==1: self.play(a.animate.shift(LEFT*.3),b.animate.shift(RIGHT*.3),run_time=.6)
                if i==2:
                    self.wait(.75)
                    cross=Cross(b,stroke_color=PRUNE,stroke_width=5)
                    self.stage.add(cross)
                    self.play(Create(cross),run_time=.3)
                    self.play(b.animate.set_opacity(.08),cross.animate.set_opacity(.15),a.animate.set_color(GOOD),run_time=.65)
            elif i in (3,4,5,6):
                left=self.comparison('둘 다 가능','{A, B} → {A}',WEIGHT).move_to([-1.95,.3,0])
                right=self.comparison('A가 확실','{A} → {A}',GOOD).move_to([1.95,.3,0])
                title=txt('Result = A',40,ACCENT).move_to(UP*3.8)
                self.stage=VGroup(left,right,title)
                self.play(FadeIn(self.stage),run_time=.45)
                if i in (4,5):
                    active=left if i==4 else right
                    other=right if i==4 else left
                    self.play(other.animate.set_opacity(.2),Indicate(active,color=ACCENT),run_time=.7)
                if i==6:
                    note=txt('같은 데이터  /  다른 사전 확률',27,ACCENT).move_to(DOWN*2.7)
                    self.stage.add(note); self.play(FadeIn(note),run_time=.4)
            elif i==7:
                title=txt('P(A) = 0.9     P(B) = 0.1',30).move_to(UP*3.7)
                top=self.bar('A 관측',False).move_to(UP*1.4)
                bottom=self.bar('B 관측',True).move_to(DOWN*1.6)
                self.stage=VGroup(title,top,bottom)
                self.play(FadeIn(self.stage),run_time=.45)
                self.wait(.6)
                self.play(top[2].animate.set_opacity(.08),run_time=.5)
                self.wait(.65)
                self.play(bottom[1].animate.set_opacity(.08),Indicate(bottom[2],color=PRUNE),run_time=.6)
            elif i==8:
                dots=VGroup(*[Dot(radius=.12,color=WEIGHT) for _ in range(16)]).arrange_in_grid(2,8,buff=.45).move_to(UP*.9)
                title=txt('정보는 가능성을 제거한다',36,ACCENT).move_to(UP*3.5)
                note=txt('제거한 개수 ≠ 정보량',30).move_to(DOWN*2)
                self.stage=VGroup(dots,title,note)
                self.play(FadeIn(self.stage),run_time=.45)
                self.play(*[dots[j].animate.set_opacity(.08) for j in range(1,16)],run_time=.8)
            else:
                dots=VGroup(*[Dot(radius=r,color=c) for r,c in zip((.65,.38,.23,.12),(WEIGHT,GOOD,ACCENT,PRUNE))]).arrange(RIGHT,buff=.65)
                labels=VGroup(*[txt(s,23,MUTED).next_to(d,DOWN,buff=.4) for s,d in zip(('p₁','p₂','p₃','p₄'),dots)])
                title=txt('모든 가능성의 무게가 같을까?',34,ACCENT).move_to(UP*3.5)
                note=txt('02  /  확률 → 정보량',30).move_to(DOWN*2.5)
                self.stage=VGroup(dots,labels,title,note)
                self.play(FadeIn(self.stage),run_time=.5)
            self.to(end)
    def card(self,s,color):
        return VGroup(RoundedRectangle(width=2.6,height=2.5,corner_radius=.2,stroke_color=color,fill_color=color,fill_opacity=.12),txt(s,65,color))
    def comparison(self,label,formula,color):
        return VGroup(RoundedRectangle(width=3.6,height=3.9,corner_radius=.2,stroke_color=color),txt(label,27,color,3.2).shift(UP*1.2),txt('A',60,ACCENT),txt(formula,25,INK,3.2).shift(DOWN*1.25))
    def bar(self,label,rare):
        a=Rectangle(width=6.3,height=.8,stroke_width=0,fill_color=WEIGHT,fill_opacity=.8).move_to([-.35,0,0])
        b=Rectangle(width=.7,height=.8,stroke_width=0,fill_color=PRUNE,fill_opacity=.8).move_to([3.15,0,0])
        return VGroup(txt(label,28,PRUNE if rare else WEIGHT).move_to([0,1,0]),a,b,txt('드문 결과 → 정보량 큼' if rare else '예상한 결과 → 정보량 작음',24).move_to([0,-1,0]))
    def to(self,target):
        if self.time>target+.04: raise ValueError(f'Timeline overrun: {self.time} > {target}')
        width=max(.01,7.6*target/self.DURATION)
        remain=target-self.time
        if remain>0:
            self.play(self.progress.animate.stretch_to_fit_width(width).move_to([-3.8+width/2,-7.35,0]),run_time=min(.15,remain))
        if target-self.time>.001: self.wait(target-self.time)
