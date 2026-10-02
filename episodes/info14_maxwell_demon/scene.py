"""Selective-door thought experiment: information controls access to thermal work."""
import sys
from pathlib import Path
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import txt,MUTED,WEIGHT,PRUNE,GOOD,ACCENT
from episodes.info14_maxwell_demon.content import CUES,DURATION,FAST_SPEED,SLOW_SPEED

class MaxwellDemon(Scene):
    DURATION=DURATION

    def label(self,text,y,size=30,color=WHITE):
        return txt(text,size,color).move_to([0,y,0])

    def to(self,target):
        remaining=target-self.time
        if remaining < -1/30:raise RuntimeError(f'Cue overrun: {remaining}')
        if round(remaining*30)>0:self.wait(round(remaining*30)/30)

    def swap(self,stage):
        if len(self.stage):self.play(FadeOut(self.stage),run_time=.2)
        self.stage=stage;self.play(FadeIn(stage),run_time=.4)

    def observer(self,y=-1.55):
        head=RoundedRectangle(width=.85,height=.55,corner_radius=.15,stroke_color=GOOD,fill_color=GOOD,fill_opacity=.12).move_to(UP*y)
        eyes=VGroup(*(Dot([x,y+.03,0],radius=.05,color=GOOD) for x in (-.2,.2)))
        return VGroup(head,eyes,Line([0,y+.3,0],[0,-.15,0],color=GOOD,stroke_opacity=.5))

    def chambers(self,sorted=False,demon=False,moving=True):
        frame=Rectangle(width=7,height=3.3,stroke_color=WEIGHT,stroke_width=2).move_to(UP*1.6)
        walls=VGroup(Line([0,-.05,0],[0,1.18,0],color=MUTED),Line([0,2.02,0],[0,3.25,0],color=MUTED))
        door=Line([0,1.18,0],[0,2.02,0],color=GOOD,stroke_width=6)
        dots=VGroup();rng=np.random.default_rng(1401)
        for side in (-1,1):
            for j in range(8):
                fast=(side==1) if sorted else j%2==0
                lo,hi=(-3.3,-.22) if side==-1 else (.22,3.3)
                x=rng.uniform(lo+.12,hi-.12);y=rng.uniform(.13,3.05)
                color=ACCENT if fast else WEIGHT
                dot=Dot([x,y,0],radius=.085,color=color,fill_opacity=1 if fast else .55)
                angle=rng.uniform(0,TAU);speed=FAST_SPEED if fast else SLOW_SPEED
                dot.velocity=np.array([np.cos(angle),np.sin(angle),0])*speed
                dot.bounds=(lo,hi,.1,3.1)
                if moving:dot.add_updater(self.bounce)
                dots.add(dot)
        group=VGroup(frame,walls,door,dots)
        if demon:group.add(self.observer())
        return group,door,dots

    @staticmethod
    def bounce(dot,dt):
        point=dot.get_center()+dot.velocity*dt;lo,hi,bottom,top=dot.bounds
        for axis,low,high in [(0,lo,hi),(1,bottom,top)]:
            if point[axis]<low:point[axis]=2*low-point[axis];dot.velocity[axis]*=-1
            if point[axis]>high:point[axis]=2*high-point[axis];dot.velocity[axis]*=-1
        dot.move_to(point)

    def memory(self,values,y=-2.75):
        group=VGroup();letters=[]
        for j,value in enumerate(values):
            x=(j-(len(values)-1)/2)*.8
            box=Square(side_length=.68,stroke_color=MUTED,stroke_width=1.5).move_to([x,y,0])
            letter=txt(value,25,ACCENT if value=='F' else WEIGHT if value=='S' else GOOD).move_to(box)
            group.add(box,letter);letters.append(letter)
        return group,letters

    def engine(self,y=-2.35):
        body=RoundedRectangle(width=2.15,height=.85,corner_radius=.15,stroke_color=GOOD).move_to(UP*y)
        rotor=VGroup(*(Line([.4,y,0],[.4+.25*np.cos(a),y+.25*np.sin(a),0],color=ACCENT) for a in np.linspace(0,TAU,4,endpoint=False)))
        group=VGroup(body,txt('열기관',24,GOOD).move_to([-.4,y,0]),rotor,Arrow([2.1,-.2,0],[.8,y+.5,0],color=PRUNE,buff=.1),Arrow([-.8,y+.5,0],[-2.1,-.2,0],color=WEIGHT,buff=.1))
        return group,rotor

    def construct(self):
        self.add(self.label('INFORMATION THEORY / 14',7.25,20,MUTED),self.label('정보만 있으면 제2법칙을 깰 수 있을까?',6.4,30),Line([-3.8,5.8,0],[3.8,5.8,0],color=MUTED,stroke_opacity=.3))
        captions=['분자 속도는 제각각 / 양쪽의 평균 온도는 같다','속도를 관찰하고, 문을 선택적으로 제어한다','빠름: 왼쪽 → 오른쪽 / 느림: 오른쪽 → 왼쪽','온도는 분자 하나가 아니라 평균 운동 에너지와 연결','열기관: 뜨거운 쪽의 열 → 일 + 차가운 쪽으로 열','기체만 보면 제2법칙을 깬 것처럼 보인다','관찰 → 기록 → 문 제어','유한한 메모리를 계속 쓰려면 재사용 과정이 필요','Landauer: 비가역적 정보 삭제의 열역학적 하한','기체 + 제어 장치 + 메모리 + 환경을 함께 본다','한 순환 전체의 평균 / 측정 자체와 삭제는 구분','정보 → 제어 → 분자 분포 변화','정보는 열을 일로 활용하도록 돕는 물리적 자원']
        self.stage=VGroup();cap=VGroup()
        for i,(start,end,_,__) in enumerate(CUES):
            if i:
                self.stage.clear_updaters(recursive=True)
                self.play(FadeOut(cap),run_time=.2)
            cap=self.label(captions[i],-5.95,22);self.play(FadeIn(cap),run_time=.2)
            if i in (0,1):
                box,door,dots=self.chambers(demon=i==1)
                stage=VGroup(self.label('같은 온도의 두 공간' if i==0 else 'Maxwell’s Demon / 맥스웰의 도깨비',4.9,28),self.label('T왼쪽 = T오른쪽',3.8,30,GOOD),box,self.label('밝은 분자: 빠름 / 어두운 분자: 느림',-2.6,25,MUTED),self.label('같은 종류의 기체 / 색은 속도 분류',-4,24,MUTED),self.label('선별 과정을 보여주는 개념도',-4.9,20,MUTED));self.swap(stage)
            elif i==2:
                box,door,dots=self.chambers(demon=True,moving=False)
                dots.remove(dots[0],dots[9])
                dots.set_opacity(.13)
                fast=Dot([-2.3,1.6,0],radius=.13,color=ACCENT);slow=Dot([2.3,1.6,0],radius=.13,color=WEIGHT)
                stage=VGroup(self.label('속도에 따라 문을 열면?',4.9,31),box,fast,slow,self.label('빠름 → 오른쪽 / 느림 → 왼쪽',3.8,27),self.label('반대 조합은 통과시키지 않는다',-2.8,25,PRUNE),self.label('자동으로 열리는 문이 아니라, 정보를 쓰는 제어',-4.45,23,MUTED));self.swap(stage)
                self.play(door.animate.set_opacity(0),run_time=.2)
                self.play(fast.animate.move_to([2.7,1.6,0]),run_time=.6)
                self.play(door.animate.set_opacity(1),run_time=.2)
                self.play(door.animate.set_opacity(0),run_time=.2)
                self.play(slow.animate.move_to([-2.7,1.6,0]),run_time=1.1)
                self.play(door.animate.set_opacity(1),run_time=.2)
                self.play(fast.animate.move_to([.24,1.85,0]),slow.animate.move_to([-.24,1.35,0]),run_time=.7)
                self.play(fast.animate.move_to([2.7,1.85,0]),slow.animate.move_to([-2.7,1.35,0]),run_time=.7)
            elif i in (3,4,5):
                box,door,dots=self.chambers(sorted=True,demon=i==5)
                stage=VGroup(self.label(['평균 운동 에너지가 달라진다','온도 차이로 일을 꺼낸다','기체만 보면 이상합니다'][i-3],4.9,30),box,txt('차가움',27,WEIGHT).move_to([-1.8,3.85,0]),txt('뜨거움',27,PRUNE).move_to([1.8,3.85,0]))
                if i==3:stage.add(self.label('T왼쪽 < T오른쪽',-1.6,35,ACCENT),self.label('느린 분자 쪽 / 빠른 분자 쪽',-3.1,28),self.label('열평형이 깨진 분포 / 정량 온도 계산 아님',-4.7,21,MUTED))
                elif i==4:
                    engine,rotor=self.engine();stage.add(engine,self.label('온도 차이 → 꺼낼 수 있는 일',-4.1,31,ACCENT),self.label('열은 뜨거운 쪽에서 차가운 쪽으로 / 일부가 일로',-4.9,20,MUTED))
                else:stage.add(self.label('기체의 엔트로피가 줄었다면?',-2.8,31,PRUNE),self.label('제2법칙을 깬 걸까?',-4.3,36,ACCENT))
                self.swap(stage)
                if i==4:self.play(Rotate(rotor,angle=TAU,about_point=[.4,-2.35,0]),run_time=1.2)
            elif i in (6,7,8):
                box,door,dots=self.chambers(sorted=True,demon=True,moving=False)
                values=['F','S','F','F','S','F','S','S']
                memory,letters=self.memory(values)
                if i==6:
                    for letter in letters:letter.set_opacity(0)
                stage=VGroup(self.label(['도깨비도 물리계의 일부','메모리가 차면 어떻게 할까?','메모리를 다시 쓰는 단계'][i-6],4.9,31),box,memory,self.label('F: 빠름 / S: 느림',-3.65,24,MUTED),self.label(['기록을 이용해 문을 제어한다','같은 메모리로 반복하려면 초기화','비가역적 삭제 → 환경으로 열 방출'][i-6],-4.75,26,GOOD));self.swap(stage)
                if i==6:
                    self.play(LaggedStart(*(letter.animate.set_opacity(1) for letter in letters),lag_ratio=.15),run_time=1.2)
                    self.play(door.animate.set_opacity(.2),run_time=.2);self.play(door.animate.set_opacity(1),run_time=.2)
                elif i==7:self.play(Indicate(memory,color=PRUNE,scale_factor=1.05),run_time=.6)
                else:
                    self.play(*(Transform(letter,txt('0',25,GOOD).move_to(letter)) for letter in letters),run_time=.8)
                    waves=VGroup(*(VMobject(color=PRUNE,stroke_width=2,stroke_opacity=1-j*.2).set_points_as_corners([[sign*(3.35+j*.2)+.06*np.sin(t*9),-2.75+t,0] for t in np.linspace(-.45,.45,30)]) for sign in (-1,1) for j in range(3)))
                    self.stage.add(waves);self.play(FadeIn(waves),run_time=.6)
            elif i==9:
                gas=RoundedRectangle(width=4.8,height=1.7,corner_radius=.2,stroke_color=WEIGHT).move_to(UP*2.9)
                memory=RoundedRectangle(width=4.8,height=1.7,corner_radius=.2,stroke_color=GOOD).move_to(UP*.6)
                outer=RoundedRectangle(width=7.8,height=7.8,corner_radius=.35,stroke_color=PRUNE).move_to(UP*.6)
                stage=VGroup(self.label('함께 세야 할 범위를 넓힌다',4.9,31),gas,self.label('기체',2.9,31,WEIGHT),memory,self.label('제어 장치 + 메모리',.6,29,GOOD),outer,self.label('주변 환경도 포함',-2.2,28,PRUNE),self.label('장치 재사용까지 한 순환',-4.2,30,ACCENT));self.swap(stage)
                self.play(Indicate(outer,color=ACCENT,scale_factor=1.02),run_time=.6)
            elif i==10:
                self.swap(VGroup(self.label('전체 순환을 보면',4.9,33),self.label('기체 쪽: 엔트로피 감소 가능',3.1,29,WEIGHT),self.label('재사용 과정: 환경의 엔트로피 증가',1.7,29,PRUNE),self.label('⟨ΔS전체⟩ ≥ 0',-.15,43,GOOD),self.label('제2법칙은 깨지지 않는다',-1.8,32,GOOD),self.label('측정 자체가 반드시 같은 열을 내는 것은 아님',-3.4,23,MUTED),self.label('메모리·상관관계·환경까지 포함한 평균적 수지',-4.7,21,MUTED)))
            elif i==11:
                stage=VGroup(self.label('정보는 실제 제어에 쓰인다',4.9,32))
                for y,name,color in [(3.1,'분자의 속도를 안다',WEIGHT),(1.05,'문을 열지 결정한다',GOOD),(-1,'분자 분포가 바뀐다',PRUNE)]:
                    stage.add(RoundedRectangle(width=6.3,height=1.05,corner_radius=.15,stroke_color=color).move_to(UP*y),self.label(name,y,30,color))
                stage.add(Arrow([0,2.45,0],[0,1.7,0],color=ACCENT,buff=.05),Arrow([0,.4,0],[0,-.35,0],color=ACCENT,buff=.05),self.label('정보 → 제어 → 물리적 상태 변화',-3.05,30,ACCENT),self.label('기록으로 끝나지 않고, 행동을 바꾼다',-4.6,25,MUTED));self.swap(stage)
            else:
                box,door,dots=self.chambers(sorted=True,moving=False)
                box.scale(.7).move_to(UP*2.2)
                self.swap(VGroup(self.label('정보는 물리적 자원인가?',4.9,33,ACCENT),box,self.label('관측 정보 → 제어 → 꺼낼 수 있는 일',.3,29,GOOD),self.label('에너지의 원천은 기체의 열',-1.15,29,WEIGHT),self.label('정보는 그 열을 활용하는 제어 자원',-2.6,29,ACCENT),self.label('Information is physical.',-4.05,33,GOOD),self.label('열 · 엔트로피 · 일과 연결된 정보',-4.95,24,MUTED)))
            self.to(end)
