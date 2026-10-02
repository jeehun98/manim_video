"""One bit steers an isothermal expansion that lifts a load."""
import sys
from pathlib import Path
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import txt,MUTED,WEIGHT,PRUNE,GOOD,ACCENT
from episodes.info15_szilard_engine.content import CUES,DURATION

class SzilardEngine(Scene):
    DURATION=DURATION

    def label(self,text,y,size=30,color=WHITE):
        return txt(text,size,color).move_to([0,y,0])

    def to(self,target):
        remaining=target-self.time
        if remaining < -1/30:raise RuntimeError(f'Cue overrun {remaining}')
        if round(remaining*30)>0:self.wait(round(remaining*30)/30)

    def swap(self,stage):
        if len(self.stage):self.play(FadeOut(self.stage),run_time=.2)
        self.stage=stage;self.play(FadeIn(stage),run_time=.4)

    def vessel(self,partition=True,moving=True,full=False):
        frame=Rectangle(width=6,height=2.4,stroke_color=WEIGHT,stroke_width=2).move_to(UP*1.4)
        divider=Line([0,.2,0],[0,2.6,0],color=MUTED,stroke_width=3)
        if not partition:divider.set_opacity(0)
        particle=Dot([-1.5,1.4,0],radius=.13,color=ACCENT)
        particle.velocity=np.array([1.15,.8,0])
        particle.limit=2.8 if full else -.2
        if moving:particle.add_updater(self.bounce)
        bath=RoundedRectangle(width=6.25,height=.65,corner_radius=.15,stroke_color=PRUNE,fill_color=PRUNE,fill_opacity=.06).move_to(DOWN*2.55)
        group=VGroup(frame,divider,particle,bath,self.label('온도 T의 열환경',-2.55,26,PRUNE))
        return group,divider,particle

    @staticmethod
    def bounce(dot,dt):
        point=dot.get_center()+dot.velocity*dt
        right=dot.limit() if callable(dot.limit) else dot.limit
        for axis,lo,hi in [(0,-2.8,right),(1,.38,2.42)]:
            if point[axis]<lo:point[axis]=2*lo-point[axis];dot.velocity[axis]*=-1
            if point[axis]>hi:point[axis]=2*hi-point[axis];dot.velocity[axis]*=-1
        dot.move_to(point)

    def piston_load(self,tracker):
        piston=Line([0,.2,0],[0,2.6,0],color=GOOD,stroke_width=7)
        rod=Line([0,2.6,0],[0,2.9,0],color=GOOD)
        pulley=Circle(radius=.17,color=GOOD).move_to([-3.9,2.9,0])
        load=VGroup(RoundedRectangle(width=.57,height=.6,corner_radius=.06,stroke_color=ACCENT,fill_color=ACCENT,fill_opacity=.12),txt('추',18,ACCENT)).move_to([-3.9,-1.9,0])
        horizontal=Line([0,2.9,0],[-3.9,2.9,0],color=MUTED)
        vertical=Line([-3.9,2.9,0],[-3.9,-1.6,0],color=MUTED)
        piston.add_updater(lambda mob:mob.put_start_and_end_on([tracker.get_value(),.2,0],[tracker.get_value(),2.6,0]))
        rod.add_updater(lambda mob:mob.put_start_and_end_on([tracker.get_value(),2.6,0],[tracker.get_value(),2.9,0]))
        load.add_updater(lambda mob:mob.move_to([-3.9,-1.9+tracker.get_value(),0]))
        horizontal.add_updater(lambda mob:mob.put_start_and_end_on([tracker.get_value(),2.9,0],[-3.9,2.9,0]))
        vertical.add_updater(lambda mob:mob.put_start_and_end_on([-3.9,2.9,0],[-3.9,-1.6+tracker.get_value(),0]))
        return VGroup(piston,rod,pulley,load,horizontal,vertical),load

    def comparison(self):
        stage=VGroup(self.label('같은 열과 팽창 / 다른 제어',4.9,31))
        tracker=ValueTracker(0);free_parts=[];work_status=None
        for known,cx in [(False,-2.25),(True,2.25)]:
            stage.add(txt('1 bit로 위치 확인' if known else '위치 미확인',27,GOOD if known else MUTED,max_width=3.6).move_to([cx,4.05,0]))
            stage.add(txt('L 확인 → 오른쪽 연결' if known else '칸막이만 제거',20,GOOD if known else MUTED,max_width=3.7).move_to([cx,3.25,0]))
            frame=Rectangle(width=2.8,height=1.8,stroke_color=WEIGHT).move_to([cx,1.6,0])
            wall=Line([cx,.7,0],[cx,2.5,0],color=GOOD if known else MUTED,stroke_width=4)
            ball=Dot([cx-.7,1.6,0],radius=.09,color=ACCENT)
            ball.velocity=np.array([.8,.55,0])
            def local_bounce(mob,dt,c=cx,k=known):
                point=mob.get_center()+mob.velocity*dt
                right=c+tracker.get_value()-.12 if k else c+1.28
                for axis,lo,hi in [(0,c-1.28,right),(1,.83,2.37)]:
                    if point[axis]<lo:point[axis]=2*lo-point[axis];mob.velocity[axis]*=-1
                    if point[axis]>hi:point[axis]=2*hi-point[axis];mob.velocity[axis]*=-1
                mob.move_to(point)
            bath=RoundedRectangle(width=3.1,height=.6,corner_radius=.1,stroke_color=PRUNE).move_to([cx,-1.5,0])
            stage.add(frame,wall,ball,bath,txt('같은 온도 T',22,PRUNE).move_to(bath))
            load=VGroup(RoundedRectangle(width=.37,height=.46,corner_radius=.05,stroke_color=ACCENT if known else MUTED),txt('추',15,ACCENT if known else MUTED)).move_to([cx-1.75,-.55,0])
            stage.add(load)
            if known:
                wall.add_updater(lambda mob,c=cx:mob.put_start_and_end_on([c+tracker.get_value(),.7,0],[c+tracker.get_value(),2.5,0]))
                ball.add_updater(local_bounce)
                pulley=Circle(radius=.1,color=GOOD).move_to([cx-1.75,2.75,0])
                horizontal=Line([cx,2.75,0],[cx-1.75,2.75,0],color=MUTED)
                vertical=Line([cx-1.75,2.75,0],[cx-1.75,-.32,0],color=MUTED)
                rod=Line([cx,2.5,0],[cx,2.75,0],color=GOOD)
                load.add_updater(lambda mob,c=cx:mob.move_to([c-1.75,-.55+tracker.get_value(),0]))
                horizontal.add_updater(lambda mob,c=cx:mob.put_start_and_end_on([c+tracker.get_value(),2.75,0],[c-1.75,2.75,0]))
                vertical.add_updater(lambda mob,c=cx:mob.put_start_and_end_on([c-1.75,2.75,0],[c-1.75,-.32+tracker.get_value(),0]))
                rod.add_updater(lambda mob,c=cx:mob.put_start_and_end_on([c+tracker.get_value(),2.5,0],[c+tracker.get_value(),2.75,0]))
                stage.add(pulley,horizontal,vertical,rod,Arrow([cx-1.15,-1.15,0],[cx-1.15,.73,0],color=PRUNE,buff=.05))
                work_status=txt('Work > 0',28,GOOD,max_width=3.5).move_to([cx,-2.65,0]);stage.add(work_status)
            else:
                ball.set_opacity(0)
                questions=VGroup(*(txt('?',31,ACCENT).move_to([cx+x,1.6,0]) for x in (-.7,.7)))
                stage.add(questions,txt('Work = 0',28,PRUNE,max_width=3.4).move_to([cx,-2.65,0]))
                free_parts=[wall,ball,questions,local_bounce]
        stage.add(Line([0,4.4,0],[0,-3.1,0],color=MUTED,stroke_opacity=.25),self.label('열환경은 같다 / 위치 정보가 연결 방향을 정한다',-3.8,25,ACCENT),self.label('특정 두 제어 방법의 비교 / 추 높이는 개념도',-4.8,20,MUTED))
        return stage,tracker,free_parts

    def construct(self):
        self.add(self.label('INFORMATION THEORY / 15',7.25,20,MUTED),self.label('1비트의 정보는 얼마의 일을 만들 수 있을까?',6.4,28),Line([-3.8,5.8,0],[3.8,5.8,0],color=MUTED,stroke_opacity=.3))
        captions=['에너지원은 이미 존재하는 열환경','위치를 모르면 일을 꺼낼 방향이 정해지지 않는다','칸막이만 제거한 자유팽창 / 이 과정의 Work = 0','정확한 위치 측정으로 얻는 1 bit','L이면 오른쪽 / R이면 왼쪽으로 피스톤 연결','피스톤 이동을 추 상승으로 이용한다','에너지원 = 열환경 / 정보 = 연결 방향의 선택','같은 열환경과 팽창 / 측정에 맞춰 연결한 쪽은 일 추출','이상적 준정적 등온 팽창의 최대 평균 일','V/2 → V / 부피 두 배에서 ln 2','같은 T / 등확률 측정 기록과 표준 메모리 초기화','장치와 메모리까지 복원하는 전체 순환','1 bit가 한 일: 일을 꺼낼 방향을 정한다']
        self.stage=VGroup();cap=VGroup()
        for i,(start,end,_,__) in enumerate(CUES):
            if i:
                self.stage.clear_updaters(recursive=True)
                self.play(FadeOut(cap),run_time=.2)
            cap=self.label(captions[i],-5.95,22);self.play(FadeIn(cap),run_time=.2)
            if i in (0,1,2,3):
                box,divider,particle=self.vessel(partition=i>0,full=i==0)
                stage=VGroup(self.label(['열은 이미 입자를 움직이고 있다','문제는 어느 쪽인지 모른다는 것','그냥 칸막이를 빼면 퍼질 뿐','이번에는 먼저 위치를 확인한다'][i],4.9,29),box,self.label('전체 부피 V' if i==0 else '왼쪽 V/2 / 오른쪽 V/2',-.65,28,WEIGHT))
                if i==0:stage.add(self.label('에너지를 공급하는 열환경',-1.55,30,PRUNE),self.label('입자 하나 / 운동은 개념도',-4.15,23,MUTED))
                elif i==1:
                    particle.set_opacity(0)
                    stage.add(txt('?',42,ACCENT).move_to([-1.5,1.4,0]),txt('?',42,ACCENT).move_to([1.5,1.4,0]),self.label('P(L) = P(R) = 1/2',-1.55,31,ACCENT),self.label('방향을 정할 정보가 아직 없다',-4.15,28,MUTED))
                elif i==2:
                    particle.set_opacity(0)
                    questions=VGroup(*(txt('?',42,ACCENT).move_to([x,1.4,0]) for x in (-1.5,1.5)))
                    stage.add(questions)
                    stage.add(self.label('Work = 0',-1.55,39,PRUNE),self.label('외부 부하를 연결하지 않은 자유팽창',-4.15,24,MUTED))
                else:
                    stage.add(self.label('측정값 L / 1 bit',-1.55,34,GOOD),self.label('입자의 힘을 꺼낼 방향이 알려졌다',-4.15,28,ACCENT))
                self.swap(stage)
                if i==2:
                    particle.limit=2.8;self.play(divider.animate.set_opacity(0),questions.animate.set_opacity(0),particle.animate.set_opacity(1),run_time=.4)
                elif i==3:self.play(Indicate(particle,color=GOOD,scale_factor=1.5),run_time=.7)
            elif i==4:
                stage=VGroup(self.label('1비트가 선택하는 것은 방향',4.9,32))
                for y,left in [(2.65,True),(-.2,False)]:
                    frame=Rectangle(width=4.8,height=1.4,stroke_color=WEIGHT).move_to(UP*y)
                    wall=Line([0,y-.7,0],[0,y+.7,0],color=GOOD,stroke_width=4)
                    ball=Dot([-1.2 if left else 1.2,y,0],radius=.13,color=ACCENT)
                    arrow=Arrow([.18 if left else -.18,y,0],[1.9 if left else -1.9,y,0],color=GOOD,buff=.03)
                    stage.add(frame,wall,ball,arrow,self.label('L 확인 → 오른쪽으로 연결' if left else 'R 확인 → 왼쪽으로 연결',y+1.1,27,GOOD))
                stage.add(self.label('위치 정보 → 장치의 연결 방향',-2.9,30,ACCENT),self.label('입자가 있는 쪽의 공간이 넓어지게 선택',-4.25,25,MUTED));self.swap(stage)
            elif i in (5,6):
                box,divider,particle=self.vessel();divider.set_opacity(0)
                tracker=ValueTracker(0);mechanism,load=self.piston_load(tracker)
                particle.limit=lambda:tracker.get_value()-.2
                stage=VGroup(self.label('선택한 방향으로 힘을 꺼낸다' if i==5 else '열은 에너지 / 정보는 제어',4.9,31),box,mechanism,self.label('L → 피스톤 오른쪽 → 추는 위로',3.9,26,GOOD),self.label('V/2 → V',-.65,32,WEIGHT),self.label('추를 들어 올림 = 일 추출',-1.55,28,ACCENT),self.label('입자 운동과 추 높이는 개념도',-4.7,20,MUTED))
                if i==6:stage.add(Arrow([-2.7,-2.2,0],[-2.7,.35,0],color=PRUNE,buff=.06),txt('열',24,PRUNE).move_to([-3.2,-1.1,0]),self.label('정보는 에너지를 꺼낼 방향을 알려준다',-3.95,27,GOOD))
                else:stage.add(self.label('추와 줄은 피스톤의 힘을 전달한다',-3.95,25,MUTED))
                self.swap(stage);self.play(tracker.animate.set_value(3),run_time=2,rate_func=linear)
            elif i==7:
                stage,tracker,parts=self.comparison();self.swap(stage)
                wall,ball,questions,updater=parts
                self.play(wall.animate.set_opacity(0),questions.animate.set_opacity(0),ball.animate.set_opacity(1),run_time=.3)
                ball.add_updater(updater)
                self.play(tracker.animate.set_value(1.4),run_time=2.2,rate_func=linear)
            elif i==8:
                self.swap(VGroup(self.label('그렇다면 얼마나 많은 일을 꺼낼까?',4.9,29),self.label('완전한 위치 측정 / 아주 느린 등온 팽창',3.35,25,MUTED),self.label('⟨W꺼냄⟩max = k_B T ln 2',1.5,37,GOOD),self.label('1 bit가 가능한 일의 상한',-.4,31,ACCENT),self.label('에너지 공급원은 온도 T의 열환경',-2.05,27,PRUNE),self.label('이상적인 최대 평균 / 각 시행의 일은 요동',-4.2,22,MUTED)))
            elif i==9:
                half=Rectangle(width=3,height=1.4,stroke_color=WEIGHT).move_to(UP*2.8)
                full=Rectangle(width=6,height=1.4,stroke_color=GOOD).move_to(UP*.2)
                self.swap(VGroup(self.label('2는 공간이 두 배라는 뜻',4.9,32),half,self.label('처음 V/2',2.8,31,WEIGHT),Arrow([0,1.95,0],[0,1.05,0],color=ACCENT),full,self.label('마지막 V',.2,31,GOOD),self.label('V / (V/2) = 2',-1.4,37,ACCENT),self.label('W = k_B T ln(V최종 / V처음)',-2.9,29,WEIGHT),self.label('부피 두 배 → k_B T ln 2',-4.35,31,GOOD)))
            elif i==10:
                self.swap(VGroup(self.label('같은 T에서 Landauer와 맞물린다',4.9,28),self.label('이 엔진에서 얻는 평균 일',3.35,28,WEIGHT),self.label('⟨W꺼냄⟩ ≤ k_B T ln 2',2,35,GOOD),self.label('기록을 지울 때 환경으로 내는 평균 열',.05,25,PRUNE),self.label('⟨Q환경⟩ ≥ k_B T ln 2',-1.3,35,PRUNE),self.label('최대 일과 삭제 열 하한이 같은 크기',-3.2,29,ACCENT),self.label('등확률 기록 / 표준 대칭 메모리 / 동일 온도',-4.6,22,MUTED)))
            elif i==11:
                memory=VGroup(Square(side_length=1.1,stroke_color=GOOD),txt('L',39,GOOD)).move_to(UP*2.4)
                stage=VGroup(self.label('같은 장치로 반복하려면?',4.9,31),memory,self.label('팽창 후에도 메모리에는 기록이 남음',.85,27,MUTED),self.label('장치와 메모리를 원래 상태로',-.75,30,PRUNE),self.label('전체 순환의 순이득 ≤ 0',-2.45,32,ACCENT),self.label('제2법칙은 유지된다',-3.8,30,GOOD),self.label('같은 T / 메모리 삭제의 일 비용까지 포함',-4.95,21,MUTED));self.swap(stage)
                self.play(Transform(memory[1],txt('0',39,PRUNE).move_to(memory[1])),run_time=.7)
            else:
                self.swap(VGroup(self.label('그래서 1비트가 한 일은?',4.9,33),self.label('열환경',3.25,38,PRUNE),self.label('에너지를 공급한다',2.15,29,PRUNE),self.label('1 bit의 위치 정보',.25,36,WEIGHT),self.label('일을 꺼낼 방향을 선택한다',-1.15,32,GOOD),self.label('열 → 일로 활용하는 제어권',-3.05,31,ACCENT),self.label('정보는 물리계에서 사용할 수 있는 자원',-4.65,27,GOOD)))
            self.to(end)
