"""A two-compartment memory reset; formulas name the cost only at the end."""
import sys
from pathlib import Path
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import txt,MUTED,WEIGHT,PRUNE,GOOD,ACCENT
from episodes.info12_landauer.content import CUES,DURATION

class LandauerErasure(Scene):
    DURATION=DURATION

    def label(self,text,y,size=30,color=WHITE):
        return txt(text,size,color).move_to([0,y,0])

    def to(self,target):
        left=target-self.time
        if left < -1/30:raise RuntimeError(f'Cue overrun: {left}')
        if round(left*30)>0:self.wait(round(left*30)/30)

    def swap(self,stage):
        if len(self.stage):self.play(FadeOut(self.stage),run_time=.2)
        self.stage=stage;self.play(FadeIn(stage),run_time=.4)

    def box(self,center=UP*1.8,side='left',width=6,height=2):
        center=np.array(center,dtype=float)
        frame=Rectangle(width=width,height=height,stroke_color=WEIGHT,stroke_width=2).move_to(center)
        divider=Line(center+DOWN*height/2,center+UP*height/2,color=MUTED,stroke_width=3)
        ball=Dot(center+RIGHT*(width/4*(1 if side=='right' else -1)),radius=.17,color=ACCENT)
        group=VGroup(frame,divider,ball)
        return group,frame,divider,ball

    def heat(self,center=UP*1.8):
        waves=VGroup()
        for sign in (-1,1):
            for j in range(3):
                x=sign*(3.4+j*.3)
                waves.add(VMobject(color=PRUNE,stroke_width=2,stroke_opacity=1-j*.2).set_points_as_corners([[x+.09*np.sin(t*6),center[1]+t,0] for t in np.linspace(-.7,.7,30)]))
        return waves

    def construct(self):
        self.add(self.label('INFORMATION THEORY / 12',7.25,20,MUTED),self.label('정보 1비트를 지우는 데 필요한 최소 비용',6.4,29),Line([-3.8,5.8,0],[3.8,5.8,0],color=MUTED,stroke_opacity=.3))
        captions=['공의 위치로 저장하는 0과 1','공은 하나 / 두 그림은 가능한 시작 상태','어디에서 시작해도, 마지막에는 왼쪽','같은 마지막 모습에서는 처음 위치를 구별할 수 없다','공은 남고, 처음 위치에 대한 구분이 사라진다','메모리의 가능한 위치: 두 개 → 하나','메모리의 엔트로피 감소 / 환경의 엔트로피 증가','열 방출은 개념도 / 실제 열의 크기를 그린 것이 아님','등확률 미지 비트의 확실한 삭제 / 평균 열의 하한','300 K에서 약 3 × 10⁻²¹ J / bit','삭제의 하한과 전체 컴퓨터 소비는 다르다','두 상태를 맞바꾸면, 구분을 보존할 수 있다','논리적 가역성만으로 실제 소비가 0이 되는 것은 아니다']
        self.stage=VGroup();cap=VGroup()
        for i,(start,end,_,__) in enumerate(CUES):
            if i:self.play(FadeOut(cap),run_time=.2)
            cap=self.label(captions[i],-5.95,23);self.play(FadeIn(cap),run_time=.2)
            if i==0:
                box,frame,divider,ball=self.box()
                self.swap(VGroup(self.label('두 칸짜리 메모리',4.9,34),box,txt('왼쪽 = 0',30,WEIGHT).move_to([-1.5,.1,0]),txt('오른쪽 = 1',30,PRUNE).move_to([1.5,.1,0]),self.label('상자 안에 공 하나',-2.1,34,ACCENT),self.label('공의 위치가 정보를 저장한다',-3.7,30)))
                self.play(ball.animate.set_opacity(0),run_time=.2)
                ball.move_to([1.5,1.8,0])
                self.play(ball.animate.set_opacity(1),run_time=.2)
            elif i==1:
                stage=VGroup(self.label('처음 위치는 모릅니다',4.9,33),self.label('둘 중 하나 / 각각 50%',3.9,28,MUTED))
                for y,side in [(2,'left'),(-1,'right')]:
                    box,*_=self.box(UP*y,side)
                    stage.add(box,txt('가능한 시작 '+('①' if side=='left' else '②'),24,MUTED).move_to([0,y-1.45,0]))
                stage.add(self.label('공 두 개가 아니라, 두 가지 가능성',-4.55,27,ACCENT));self.swap(stage)
            elif i==2:
                box,frame,divider,ball=self.box(side='right')
                piston=Line([3,.8,0],[3,2.8,0],color=GOOD,stroke_width=7)
                stage=VGroup(self.label('어느 쪽에 있든 왼쪽으로 초기화',4.9,29),box,piston,self.label('외부에서 장치를 움직인다',3.75,25,MUTED),self.label('칸막이 열기 → 밀기 → 장치 복원',-1.2,29,GOOD),self.label('시작 위치를 읽지 않고, 같은 제어를 적용',-2.6,25,MUTED),self.label('초기화 후: 항상 왼쪽',-4.2,34,ACCENT));self.swap(stage)
                self.play(divider.animate.set_opacity(0),run_time=.5)
                self.play(piston.animate.move_to([0,1.8,0]),ball.animate.move_to([-1.5,1.8,0]),run_time=1)
                self.play(divider.animate.set_opacity(1),run_time=.5)
                self.play(piston.animate.move_to([3,1.8,0]),run_time=.5)
                self.play(FadeOut(piston),run_time=.2);stage.remove(piston)
            elif i in (3,4):
                stage=VGroup(self.label('두 시작이 같은 끝으로',4.9,33))
                for y,side in [(2.6,'left'),(.1,'right')]:
                    before,*_=self.box(np.array([-2.15,y,0]),side,width=2.8,height=1.3)
                    after,*_=self.box(np.array([2.15,y,0]),'left',width=2.8,height=1.3)
                    stage.add(before,after,Arrow([-.6,y,0],[.6,y,0],buff=.05,color=GOOD))
                stage.add(self.label('왼쪽에서 왔을까?  오른쪽에서 왔을까?',-2.1,28),self.label('공은 그대로 / 처음 위치의 구분은 사라짐',-3.6,28,ACCENT),self.label('출력만으로 입력을 되찾을 수 없다',-4.7,24,MUTED));self.swap(stage)
                if i==4:
                    self.play(stage[1].animate.set_opacity(.2),stage[4].animate.set_opacity(.2),run_time=.6)
            elif i==5:
                stage=VGroup(self.label('가능한 위치를 모아보면',4.9,32))
                left,*_=self.box(np.array([-1.85,2.5,0]),'left',width=3,height=1.5)
                right,*_=self.box(np.array([1.85,2.5,0]),'right',width=3,height=1.5)
                result,*_=self.box(UP*-.3,'left',width=4,height=1.6)
                stage.add(left,right,result,Arrow([-1.7,1.5,0],[-.5,.65,0],color=WEIGHT,buff=.1),Arrow([1.7,1.5,0],[.5,.65,0],color=PRUNE,buff=.1),self.label('두 위치 → 한 위치',-2.3,38,GOOD),self.label('메모리의 엔트로피 감소',-3.65,31,PRUNE),self.label('입자는 남아 있지만, 가능한 저장 상태는 줄었다',-4.7,23,MUTED));self.swap(stage)
            elif i in (6,7):
                box,frame,divider,ball=self.box(side='right')
                environment=RoundedRectangle(width=8,height=6.4,corner_radius=.4,stroke_color=PRUNE,stroke_opacity=.45).move_to(UP*.85)
                particles=VGroup(*(Dot([x,y,0],radius=.035,color=PRUNE) for x,y in [(-3.5,3.3),(3.5,3.3),(-3.5,.3),(3.5,.3),(-2.9,-1.5),(-1.9,-1.7),(-.8,-1.5),(.8,-1.7),(1.9,-1.5),(2.9,-1.7)]))
                status=self.label('메모리: 두 위치가 가능',-.1,28,WEIGHT)
                stage=VGroup(self.label('상자 밖에도 환경이 있습니다',4.9,31),environment,box,status,particles,self.label('환경의 엔트로피 증가',-2.85,30,PRUNE),self.label('메모리의 감소를 환경이 보상',-4.25,29,ACCENT));self.swap(stage)
                self.play(divider.animate.set_opacity(.15),ball.animate.move_to([-1.5,1.8,0]),run_time=.8)
                self.play(divider.animate.set_opacity(1),Transform(status,self.label('메모리: 이제 왼쪽만 가능',-.1,28,GOOD)),run_time=.4)
                waves=self.heat();self.stage.add(waves)
                self.play(FadeIn(waves),*(dot.animate.shift(UP*(.17 if j%2 else -.17)) for j,dot in enumerate(particles)),run_time=.6)
                if i==7:self.play(Indicate(waves,color=ACCENT,scale_factor=1.12),run_time=.6)
            elif i==8:
                box,*_=self.box(UP*3.1,'left',width=4.4,height=1.5)
                self.swap(VGroup(self.label('이 장면의 최소 비용에 이름 붙이기',4.9,28),box,self.label('환경으로 내보내는 평균 열',1.35,30,PRUNE),self.label('⟨Q환경⟩ ≥ kᵦ T ln 2',-.3,42,GOOD),self.label('Landauer’s Principle',-1.8,33,ACCENT),self.label('처음 0과 1이 반반 / 확실한 초기화',-3.45,23,MUTED),self.label('온도 T / 대칭 메모리 / 장치는 원래 조건으로 복원',-4.65,20,MUTED)))
            elif i==9:
                stage=VGroup(self.label('실온에서는 얼마나 작을까?',4.9,31),self.label('300 K',3.75,38,ACCENT),self.label('한 비트당 약',2.3,28),self.label('3 × 10⁻²¹ J',.9,46,GOOD),self.label('작지만, 0은 아니다',-.7,33,PRUNE),self.label('지우는 비트 수가 늘면, 하한도 누적',-4.35,26,MUTED))
                boxes=VGroup()
                for j in range(6):
                    box,*_=self.box(np.array([(j-2.5)*1.1,-2.6,0]),'left',width=.95,height=.7);boxes.add(box)
                stage.add(boxes);self.swap(stage)
            elif i==10:
                box,*_=self.box(UP*2.5,'left',width=4.5,height=1.6)
                self.swap(VGroup(self.label('컴퓨터의 모든 소비를 뜻할까?',4.9,30),box,self.label('정보 삭제의 최소 비용',.8,33,GOOD),self.label('실제 소비는 이보다 더 크다',-1,30,PRUNE),self.label('회로 구동 · 누설 · 배선 등 다른 손실',-2.4,25,MUTED),self.label('삭제의 하한 ≠ 전체 소비 에너지',-4.15,29,ACCENT)))
            elif i==11:
                stage=VGroup(self.label('두 위치를 맞바꾸기만 한다면?',4.9,30))
                balls=[];dividers=[]
                for y,side in [(2.5,'left'),(-.2,'right')]:
                    box,frame,divider,ball=self.box(UP*y,side,width=5,height=1.7);stage.add(box);balls.append(ball);dividers.append(divider)
                stage.add(self.label('왼쪽 ↔ 오른쪽',-2.4,33,GOOD),self.label('지우지 않고, 구분을 보존한다',-3.65,30,GOOD),self.label('현재 위치로 처음 위치를 되찾을 수 있다',-4.7,23,MUTED));self.swap(stage)
                self.play(*(divider.animate.set_opacity(0) for divider in dividers),run_time=.2)
                self.play(balls[0].animate.shift(RIGHT*2.5),balls[1].animate.shift(LEFT*2.5),run_time=.8)
                self.play(balls[0].animate.shift(LEFT*2.5),balls[1].animate.shift(RIGHT*2.5),run_time=.8)
                self.play(*(divider.animate.set_opacity(1) for divider in dividers),run_time=.2)
            else:
                box,*_=self.box(UP*2.7,'left',width=5,height=1.8)
                self.swap(VGroup(self.label('입력을 끝까지 보존하는 계산',4.9,31),box,self.label('정보 삭제 비용은 필수가 아니다',.7,30,GOOD),self.label('실제 장치의 소비가 0이라는 뜻은 아님',-1.1,26,PRUNE),self.label('가역적 계산은 이 비용을',-3.15,30),self.label('어디까지 피할 수 있을까?',-4.35,33,ACCENT)))
            self.to(end)
