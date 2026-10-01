"""Stay with one sender, one receiver, and the same B through both transmissions."""
import sys
from pathlib import Path
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import txt,MUTED,WEIGHT,PRUNE,GOOD,ACCENT
from episodes.info08_known_bit.content import CUES,DURATION,CODE

class AlreadyKnownBit(Scene):
    DURATION=DURATION

    def label(self,text,y,size=30,color=WHITE):
        return txt(text,size,color).move_to([0,y,0])

    def token(self,value,color=WEIGHT):
        return VGroup(RoundedRectangle(width=.68,height=.8,corner_radius=.1,stroke_color=color,fill_color=color,fill_opacity=.13),txt(value,35,color))

    def person(self,x,name,color):
        head=Circle(radius=.23,color=color).move_to([x,1.35,0])
        body=Arc(radius=.6,start_angle=0,angle=PI,color=color).move_to([x,.7,0])
        name=txt(name,26,color).move_to([x,.05,0])
        return VGroup(head,body,name)

    def candidate(self,text,x,y,color=WEIGHT):
        return VGroup(RoundedRectangle(width=.62,height=.7,corner_radius=.08,stroke_color=color,fill_color=color,fill_opacity=.08),txt(text,26,color)).move_to([x,y,0])

    def communication(self):
        self.code=VGroup()
        for i,s in enumerate('ABCD'):
            box=RoundedRectangle(width=1.65,height=.95,corner_radius=.12,stroke_color=GOOD if i<2 else WEIGHT)
            entry=VGroup(box,txt(f'{s} = {CODE[s]}',27,GOOD if i<2 else WEIGHT)).move_to([(i-1.5)*1.85,4.1,0])
            self.code.add(entry)
        self.sender=self.person(-2.55,'보내는 사람',WEIGHT)
        self.receiver=self.person(2.55,'받는 사람',GOOD)
        self.result=self.label('이번 결과 Y = B',2.6,31,WEIGHT).move_to([-2.3,2.6,0])
        self.question=txt('아직 모름',31,MUTED).move_to([2.5,2.6,0])
        self.candidates=VGroup(*(self.candidate(s,1.5+i*.65,-3,GOOD if i<2 else WEIGHT) for i,s in enumerate('ABCD')))
        self.choices=txt('A / B / C / D ?',24,MUTED).move_to([2.55,-2.15,0])
        self.case=self.label('상황 1: 받는 사람에게 단서 없음',3.15,23,MUTED)
        self.path=Arrow([-2.55,-1,0],[2.55,-1,0],buff=0,color=MUTED,stroke_width=2)
        self.bits=VGroup(self.token('0',ACCENT).move_to([-2.9,-.95,0]),self.token('1').move_to([-2.1,-.95,0]))
        self.stage=VGroup(self.code,self.sender,self.receiver,self.result,self.question,self.candidates,self.choices,
            self.path,self.bits,self.case,self.label('코드표는 두 사람이 공유 / 네 결과는 같은 확률',5.05,22,MUTED))
        self.play(FadeIn(self.stage),run_time=.6)

    def to(self,target):
        remain=target-self.time
        if remain < -1/30: raise RuntimeError(f'Cue exceeded by {-remain}')
        frames=round(remain*30)
        if frames>0:self.wait(frames/30)

    def caption(self,i):
        text=['보낼 결과는 B / 받는 사람은 아직 모름','단서 없이 보내기: 0과 1을 모두 전송','이번에는 X=왼쪽을 이미 알고 있다','첫 비트 0은 받는 사람이 이미 안다','1만 전송 → 이미 아는 0과 합쳐 B 복원','두 경우 모두 같은 B / 설명할 부분만 감소','이 예: 어느 그룹을 알아도 평균 1 bit','상호정보량 = 이미 알아서 생략한 부분','단서 없음: 둘 다 / B를 이미 앎: 보낼 것 없음','X도 새로 전송: 1 bit + 1 bit = 2 bits','수신자가 이미 X를 알 때의 평균 절약량','다음: 이미 아는 정보를 가공한다면?'][i]
        if i:self.play(FadeOut(self.cap),run_time=.2)
        self.cap=self.label(text,-5.95,25)
        self.play(FadeIn(self.cap),run_time=.2)

    def construct(self):
        self.add(self.label('INFORMATION THEORY  /  08',7.25,20,MUTED),self.label('이미 아는 것은 다시 보내지 않는다',6.4,33),
            Line([-3.8,5.8,0],[3.8,5.8,0],color=MUTED,stroke_opacity=.3))
        self.cap=VGroup()
        for i,(start,end,_,__) in enumerate(CUES):
            self.caption(i)
            if i==0:
                self.communication()
                self.play(Indicate(self.result,color=WEIGHT),run_time=.6)
            elif i==1:
                self.play(Indicate(self.code[1],color=ACCENT),run_time=.6)
                for bit,x in zip(self.bits,[2.15,2.95]):
                    self.play(bit.animate.move_to([x,-1,0]),run_time=.8)
                recovered=txt('B 복원 ✓',32,GOOD).move_to([2.5,2.6,0])
                self.play(Transform(self.question,recovered),self.candidates[0].animate.set_opacity(.12),self.candidates[2].animate.set_opacity(.12),self.candidates[3].animate.set_opacity(.12),run_time=.4)
                self.notice=self.label('새로 보낸 것: 01  /  2 bits',-4.5,28,PRUNE)
                self.stage.add(self.notice);self.play(FadeIn(self.notice),run_time=.3)
            elif i==2:
                restored_candidates=VGroup(*(self.candidate(s,1.5+j*.65,-3,GOOD if j<2 else WEIGHT) for j,s in enumerate('ABCD')))
                self.play(FadeOut(self.bits),FadeOut(self.notice),FadeOut(self.choices),Transform(self.case,self.label('상황 2: 받는 사람은 X만 미리 앎',3.15,23,ACCENT)),Transform(self.question,txt('A 아니면 B',30,GOOD).move_to([2.5,2.6,0])),Transform(self.candidates,restored_candidates),run_time=.4)
                self.bits=VGroup(self.token('0',ACCENT).move_to([-2.9,-1,0]),self.token('1').move_to([-2.1,-1,0]))
                self.known=self.label('이미 아는 X: 왼쪽 그룹 {A, B}',-4.3,30,ACCENT)
                self.stage.add(self.bits,self.known)
                self.play(FadeIn(self.bits),FadeIn(self.known),self.candidates[2].animate.set_opacity(.08),self.candidates[3].animate.set_opacity(.08),run_time=.6)
                self.play(Indicate(VGroup(self.candidates[0],self.candidates[1]),color=GOOD),run_time=.6)
            elif i==3:
                self.zero=self.token('0',ACCENT).move_to([2.15,-1,0])
                zero_note=txt('X로 이미 앎',20,ACCENT).move_to([2.1,-1.8,0])
                self.stage.add(self.zero,zero_note)
                self.play(FadeIn(self.zero),FadeIn(zero_note),run_time=.5)
                cross=VGroup(Line(self.bits[0].get_corner(UL),self.bits[0].get_corner(DR),color=PRUNE),Line(self.bits[0].get_corner(DL),self.bits[0].get_corner(UR),color=PRUNE))
                self.stage.add(cross)
                self.play(Create(cross),run_time=.5)
                self.play(self.bits[0].animate.set_opacity(.15),run_time=.4)
                self.skip=self.label('0을 다시 보내지 않아도 된다',-3.7,28,ACCENT)
                self.stage.add(self.skip);self.play(FadeIn(self.skip),run_time=.3)
            elif i==4:
                self.play(self.bits[1].animate.move_to([2.95,-1,0]),run_time=1)
                new_note=txt('이번에 받은 1',20,WEIGHT).move_to([3,-2.3,0])
                self.stage.add(new_note);self.play(FadeIn(new_note),run_time=.3)
                self.play(Transform(self.question,txt('01 → B ✓',30,GOOD).move_to([2.45,2.6,0])),self.candidates[0].animate.set_opacity(.12),run_time=.5)
                self.play(Indicate(VGroup(self.zero,self.bits[1]),color=GOOD),run_time=.7)
            elif i==5:
                self.play(FadeOut(self.skip),run_time=.2)
                self.compare=self.label('보낸 01 → B    /    아는 0 + 보낸 1 → B',-3.75,27,GOOD)
                self.stage.add(self.compare);self.play(FadeIn(self.compare),run_time=.4)
                self.play(Indicate(self.result,color=WEIGHT),Indicate(self.question,color=GOOD),run_time=.7)
            else:
                self.play(FadeOut(self.stage),run_time=.3)
                if i==6:
                    self.stage=VGroup(self.label('이 예에서는 어느 그룹을 알아도',4.65,28,MUTED),
                        self.label('왼쪽: A / B  → 마지막 1 bit',3,30,GOOD),self.label('오른쪽: C / D → 마지막 1 bit',1.6,30,WEIGHT),
                        self.label('½ × 1 + ½ × 1 = 1 bit',-.1,34,ACCENT),self.label('남은 설명량',-1.6,37,GOOD),
                        self.label('조건부 엔트로피  H(Y|X)=1',-3.3,30,GOOD),self.label('일반적으로는 X의 확률로 가중평균',-4.45,23,MUTED))
                elif i==7:
                    original=VGroup(self.token('0',ACCENT),self.token('1')).arrange(RIGHT,buff=.15).move_to([0,3.5,0])
                    residual=self.token('1').move_to([0,1.3,0])
                    self.stage=VGroup(original,residual,self.label('원래 보낼 2 bits',4.65,29,PRUNE),self.label('X를 알면 1 bit만 더',2.4,29,GOOD),
                        self.label('2 − 1 = 1 bit 절약',-.4,35,ACCENT),self.label('상호정보량',-1.85,40,ACCENT),
                        self.label('I(X;Y) = H(Y) − H(Y|X)',-3.2,30,ACCENT),self.label('MUTUAL INFORMATION',-4.45,24,MUTED))
                elif i==8:
                    self.stage=VGroup(self.label('받는 사람이 이미 아는 것',4.6,30,MUTED))
                    for y,knowledge,payload,color in [(2.8,'단서 없음','01  /  2 bits',PRUNE),(.4,'왼쪽 그룹','1  /  1 bit',GOOD),(-2,'결과가 B','전송 없음 / 0 bits',ACCENT)]:
                        self.stage.add(txt(knowledge,29,color).move_to([-1.7,y,0]),txt('→',30,MUTED).move_to([0,y,0]),txt(payload,27,color).move_to([1.9,y,0]))
                    self.stage.add(self.label('절약량은 각각 0 / 1 / 2 bits',-4.1,27,ACCENT))
                elif i==9:
                    first=self.token('0',ACCENT).move_to([-1.9,2.8,0]);second=self.token('1').move_to([-1.9,1.1,0])
                    joined=txt('01 → B',32,GOOD).move_to([1.3,0,0])
                    total=self.label('1 bit + 1 bit = 2 bits',-1.65,36,ACCENT)
                    notes=VGroup(self.label('공짜 정보가 새로 생긴 것이 아니다',-2.95,27,MUTED),self.label('이미 아는 X를 다시 보내지 않은 것',-4.25,27,GOOD))
                    self.stage=VGroup(self.label('X도 새로 보내야 한다면?',4.6,32,ACCENT),first,second,
                        txt('그룹 X: 1 bit',29,ACCENT).move_to([.7,2.8,0]),txt('남은 Y: 1 bit',29,WEIGHT).move_to([.7,1.1,0]),joined,total,notes)
                elif i==10:
                    self.stage=VGroup(self.label('받는 사람이 X를 이미 알면',4,33,GOOD),self.label('Y를 설명할 때',2.3,33,GOOD),
                        self.label('평균적으로 얼마나 덜 말할까?',.5,34,ACCENT),self.label('상호정보량 I(X;Y)',-1.5,35,ACCENT),
                        self.label('일반적으로 X값마다 남는 양이 다름',-3.1,25,MUTED),self.label('어떤 관측은 오히려 더 불확실하게 만들기도 함',-4.3,23,MUTED))
                else:
                    self.stage=VGroup(self.label('이미 알고 있는 정보를',4.2,32,GOOD),self.label('다른 형태로 바꾸면?',2.8,32,GOOD),
                        self.label('이미 아는 X → 가공된 표현',.9,31,WEIGHT),self.label('원본에 대해 아는 양도',-1.3,33,ACCENT),self.label('더 늘어날까?',-2.8,38,ACCENT),self.label('새로운 관측 없이 가공만 하기',-4.25,24,MUTED))
                if i==9:
                    self.play(FadeIn(self.stage[:5]),run_time=.4)
                    self.play(Indicate(first,color=ACCENT),run_time=.6)
                    self.play(first.animate.move_to([-1.5,0,0]),run_time=.6)
                    self.play(Indicate(second,color=WEIGHT),run_time=.6)
                    self.play(second.animate.move_to([-.65,0,0]),run_time=.6)
                    self.play(FadeIn(joined),FadeIn(total),run_time=.4)
                    self.play(Indicate(total,color=ACCENT),run_time=.6)
                    self.play(FadeIn(notes),run_time=.4)
                else:self.play(FadeIn(self.stage),run_time=.4)
            self.to(end)
