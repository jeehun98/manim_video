"""Generalization needs an inductive bias that matches the world."""
import sys
from pathlib import Path
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import txt,MUTED,WEIGHT,PRUNE,GOOD,ACCENT,ZERO
from episodes.info16_no_free_lunch.content import CUES,DURATION,COMPLETIONS

class NoFreeLunch(Scene):
    DURATION=DURATION

    def label(self,text,y,size=30,color=WHITE):
        return txt(text,size,color).move_to(UP*y)

    def to(self,target):
        remaining=target-self.time
        if remaining < -1/30:raise RuntimeError(f'Cue overrun: {remaining}')
        if round(remaining*30)>0:self.wait(round(remaining*30)/30)

    def swap(self,stage):
        if len(self.stage):self.play(FadeOut(self.stage),run_time=.2)
        self.stage=stage
        self.play(FadeIn(stage),run_time=.4)

    def row(self,values,y=2,width=.85,gap=.16):
        result=VGroup()
        for i,value in enumerate(values):
            x=(i-(len(values)-1)/2)*(width+gap)
            color=MUTED if value=='?' else WEIGHT if i<3 else GOOD if value==1 else PRUNE
            cell=RoundedRectangle(width=width,height=1,corner_radius=.08,stroke_color=color,fill_color=color,fill_opacity=.08).move_to([x,y,0])
            result.add(VGroup(cell,txt(value,31,color).move_to(cell),txt(f'x{i+1}',19,MUTED).move_to([x,y-.85,0])))
        return result

    def worlds(self):
        group=VGroup()
        for i,world in enumerate(COMPLETIONS):
            x=(i%4-1.5)*1.85;y=2.8-(i//4)*1.45
            color=PRUNE if world[0]==0 else GOOD
            card=RoundedRectangle(width=1.65,height=1.15,corner_radius=.1,stroke_color=color,fill_color=color,fill_opacity=.09).move_to([x,y,0])
            digits=VGroup(*(txt(bit,24,color if j==0 else MUTED).move_to([x+(j-1.5)*.33,y+.12,0]) for j,bit in enumerate(world)))
            group.add(VGroup(card,digits,txt(f'세계 {i+1}',15,MUTED).move_to([x,y-.34,0])))
        return group

    @staticmethod
    def world_visibility(worlds,opacity_for):
        animations=[]
        for j,world in enumerate(worlds):
            opacity=opacity_for(j)
            animations.extend([world[0].animate.set_stroke(opacity=opacity).set_fill(opacity=.09*opacity),world[1].animate.set_opacity(opacity),world[2].animate.set_opacity(opacity)])
        return animations

    def construct(self):
        self.add(self.label('INFORMATION THEORY / 16',7.25,20,MUTED),self.label('학습이 가능하려면 세상이 특별해야 합니다',6.4,29),self.label('No Free Lunch',5.97,21,ACCENT),Line([-3.8,5.65,0],[3.8,5.65,0],color=MUTED,stroke_opacity=.3))
        captions=['본 정답 3개 / 새 정답은 아직 미관측','같은 학습 데이터만으로 다음 답을 고를 수 없다','새로운 4개 정답: 2⁴ = 16가지','x4=0인 세계 8개 / x4=1인 세계 8개','모든 함수를 균등하게 평균 / 미관측 점의 이진 분류','예측에는 데이터 밖으로 이어지는 가정이 들어간다','잘 맞는 구조가 있을 때 편향이 힘을 발휘한다','Inductive Bias / 보지 못한 답에 대한 선호','공유 필터 / 지역성과 반복되는 패턴','비유: 짧은 설명과 새로운 곳의 예측을 돕는 구조','새 정답이 독립적이고 등확률일 때 정확도 1/2','현실의 모든 학습법이 같다는 주장이 아니다','일반화에는 세계에 대한 가정이 필요하다']
        self.stage=VGroup();cap=VGroup()
        for i,(start,end,display,spoken) in enumerate(CUES):
            if i:self.play(FadeOut(cap),run_time=.2)
            cap=self.label(captions[i],-5.95,22);self.play(FadeIn(cap),run_time=.2)
            if i==0:
                stage=VGroup(self.label('본 것에서 / 보지 못한 곳으로',4.9,31),self.row([0,1,1,'?'],1.8),self.label('학습 데이터',-.25,28,WEIGHT),self.label('x4의 답은 어디서 올까?',-2.1,36,ACCENT),self.label('한 번도 본 적 없는 정답',-4.2,27,MUTED))
                self.swap(stage);self.play(Indicate(stage[1][3],color=ACCENT),run_time=.7)
            elif i==1:
                top=self.row([0,1,1,1],2.5);bottom=self.row([0,1,1,0],-.55)
                self.swap(VGroup(self.label('같은 증거로 두 세계가 가능하다',4.9,30),top,bottom,self.label('세계 A / 다음 답은 1',3.6,27,GOOD),self.label('세계 B / 다음 답은 0',.55,27,PRUNE),self.label('앞의 세 답은 완전히 같다',-2.35,29,WEIGHT),self.label('데이터만으로는 둘 중 하나가 결정되지 않는다',-4.25,25,ACCENT)))
            elif i in (2,3):
                worlds=self.worlds()
                stage=VGroup(self.label('남은 네 답을 채우는 모든 방법',4.9,29),self.label('공통으로 본 답: 0  1  1',4.1,27,WEIGHT),worlds,self.label('각 카드: x4  x5  x6  x7',-2.55,23,MUTED),self.label('16개 모두 학습 데이터와 일치' if i==2 else '1로 예측: 8/16 / 0으로 예측: 8/16',-3.65,28,ACCENT),self.label('각 세계를 같은 무게로 셀 때',-4.8,23,MUTED))
                self.swap(stage)
                if i==3:
                    self.play(*self.world_visibility(worlds,lambda j:.15 if j<8 else 1),run_time=.6)
                    self.wait(.6)
                    self.play(*self.world_visibility(worlds,lambda j:1 if j<8 else .15),run_time=.6)
                    self.wait(.6)
                    self.play(*self.world_visibility(worlds,lambda j:1),run_time=.4)
            elif i==4:
                self.swap(VGroup(self.label('No Free Lunch 정리',4.65,40,ACCENT),self.label('조건을 먼저 보자',3.4,30),self.label('가능한 모든 정답 함수',1.95,33,WEIGHT),self.label('균등하게 평균낸다',.8,31,WEIGHT),self.label('아직 보지 못한 점에서 비교',-.55,29,MUTED),self.label('어느 학습법도 평균 우위가 없다',-2.2,32,GOOD),self.label('이진 분류 예제: 정답 확률 1/2',-4,26,ACCENT)))
            elif i==5:
                row=self.row([0,1,1,'?'],1.5)
                stage=VGroup(self.label('우리는 이미 가정을 쓰고 있다',4.9,31),self.label('가까운 입력 → 비슷한 답',3.6,32,GOOD),row,Arrow(row[2].get_top()+UP*.25,row[3].get_top()+UP*.25,color=GOOD,buff=.03),self.label('x3가 1이니 / x4도 1일 것',-.75,31,ACCENT),self.label('보지 못한 답을 이어주는 연결',-2.65,28,GOOD),self.label('관측한 사실 + 세계에 대한 가정',-4.35,27,WEIGHT))
                self.swap(stage);self.play(Transform(row[3][1],txt('1',31,GOOD).move_to(row[3][1])),run_time=.6)
            elif i==6:
                self.swap(VGroup(self.label('같은 예측 / 다른 결과',4.9,33),self.label('가까운 답이 비슷한 세계',3.65,27,GOOD),self.row([0,1,1,1,1,1,1],2.4),self.label('x4=1 예측 → 맞음',.85,29,GOOD),self.label('답이 제멋대로 바뀌는 세계',-.35,27,PRUNE),self.row([0,1,1,0,1,0,0],-1.6),self.label('x4=1 예측 → 틀림',-3.15,29,PRUNE),self.label('이 예측법의 가정이 어느 세계와 맞는가?',-4.7,25,ACCENT)))
            elif i==7:
                self.swap(VGroup(self.label('Inductive Bias / 귀납 편향',4.65,34,ACCENT),self.label('관측하지 않은 답에 대한 선호',3.15,29),self.label('가까운 것은 비슷할 것이다',1.55,30,GOOD),self.label('같은 패턴은 다른 위치에서도 반복될 것이다',-.1,27,WEIGHT),self.label('더 단순한 설명을 먼저 시도할 것이다',-1.75,28,GOOD),self.label('편향이 있어야 / 보지 못한 곳으로 이어간다',-3.95,28,ACCENT)))
            elif i==8:
                pixels=VGroup()
                for r in range(3):
                    for c in range(7):
                        on=(c in (1,5) or (r==1 and c in (2,6)))
                        pixels.add(Square(side_length=.62,stroke_color=MUTED,fill_color=WEIGHT if on else ZERO,fill_opacity=.8).move_to([(c-3)*.68,2.3+(1-r)*.68,0]))
                window=Rectangle(width=2.04,height=2.04,stroke_color=GOOD,stroke_width=4).move_to([-1.36,2.3,0])
                stage=VGroup(self.label('CNN: 같은 필터를 다른 위치에',4.9,29),pixels,window,self.label('같은 작은 패턴',.4,31,GOOD),self.label('지역성 + 필터 공유',-1.2,32,WEIGHT),self.label('이미지의 구조와 잘 맞는 가정',-3,29,ACCENT),self.label('모든 문제에 대한 만능 구조라는 뜻은 아니다',-4.7,23,MUTED))
                self.swap(stage);self.play(window.animate.shift(RIGHT*2.72),run_time=1.3)
            elif i==9:
                self.swap(VGroup(self.label('압축과 학습이 닮은 부분',4.9,32),self.label('ABABABABABAB',3.4,37,WEIGHT),Arrow([0,2.8,0],[0,2.05,0],color=GOOD),self.label('AB를 6번 반복',1.55,32,GOOD),self.label('압축: 반복을 짧게 설명',-.2,31,WEIGHT),self.label('학습: 반복을 새 곳으로 연결',-1.9,31,GOOD),self.label('구조가 두 작업을 돕는다',-3.65,31,ACCENT),self.label('닮은점이며 / 두 작업의 완전한 동치 주장은 아니다',-4.9,20,MUTED)))
            elif i==10:
                self.swap(VGroup(self.label('외웠다고 다음 답을 아는 건 아니다',4.9,29),self.row([0,1,1,'?'],2.4),self.label('훈련 데이터: 모두 기억',.45,31,WEIGHT),self.label('새 정답: 독립적인 반반',-1.05,31,PRUNE),self.label('정확도 = 1/2',-2.65,39,PRUNE),self.label('암기와 일반화는 다른 일',-4.4,30,ACCENT)))
            elif i==11:
                stage=VGroup(self.label('No Free Lunch가 남기는 메시지',4.9,31,ACCENT),self.label('좋은 알고리즘이 없다는 뜻?',3.05,31,MUTED),self.label('어떤 세계에서나 통하는 만능 학습법은 없다',1.15,27,WEIGHT),self.label('일반화에는',-1.15,38,GOOD),self.label('세계에 대한 가정이 필요하다',-2.65,34,GOOD),self.label('그리고 그 가정이 실제 구조와 맞아야 한다',-4.5,26,ACCENT))
                self.swap(stage);self.play(stage[1].animate.set_opacity(.2),run_time=.6)
            else:
                worlds=self.worlds().scale(.65).move_to(UP*2.1)
                stage=VGroup(self.label('학습이 가능하려면 세상이 특별해야 한다',4.9,29),worlds,self.label('모든 세계를 똑같이 취급하는 대신',-.45,28,MUTED),self.label('현실에서 반복되는 구조',-1.8,32,WEIGHT),self.label('그 구조와 맞는 모델의 가정',-3.05,32,GOOD),self.label('학습은 그 만남에서 시작된다',-4.6,32,ACCENT))
                self.swap(stage)
                self.play(*self.world_visibility(worlds,lambda j:1 if j in (14,15) else .12),run_time=.8)
            self.to(end)
