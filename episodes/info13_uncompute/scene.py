"""A saved answer survives a rewind of the working register."""
import sys
from pathlib import Path
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import txt,MUTED,WEIGHT,PRUNE,GOOD,ACCENT
from episodes.info13_uncompute.content import CUES,DURATION,TRACE

class ReversibleUncompute(Scene):
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

    def register(self,state,y=1.4):
        group=VGroup();digits=[];boxes=[]
        for j,(value,name,color) in enumerate(zip(state,['입력 a','입력 b','작업 t','결과 r'],[WEIGHT,WEIGHT,PRUNE,GOOD])):
            x=(j-1.5)*1.8
            box=RoundedRectangle(width=1.5,height=1.5,corner_radius=.15,stroke_color=color,fill_color=color,fill_opacity=.08).move_to([x,y,0])
            digit=txt(str(value),48,color).move_to([x,y,0])
            group.add(box,digit,txt(name,24,color,max_width=1.6).move_to([x,y+1.3,0]));digits.append(digit);boxes.append(box)
        return group,digits,boxes

    def circuit(self,active=None):
        group=VGroup();ys=[2.7,1.6,.5,-.6]
        for y,name in zip(ys,['a','b','t','r']):
            group.add(Line([-2.7,y,0],[3.4,y,0],color=MUTED),txt(name,27,WEIGHT).move_to([-3.15,y,0]))
        gates=VGroup()
        for j,x in enumerate([-1.5,.2,1.9]):
            color=ACCENT if j==active else GOOD
            if j in (0,2):
                gate=VGroup(Line([x,ys[0],0],[x,ys[2],0],color=color),Dot([x,ys[0],0],radius=.09,color=color),Dot([x,ys[1],0],radius=.09,color=color),Circle(radius=.2,color=color).move_to([x,ys[2],0]),Line([x-.2,ys[2],0],[x+.2,ys[2],0],color=color),Line([x,ys[2]-.2,0],[x,ys[2]+.2,0],color=color))
            else:
                gate=VGroup(Line([x,ys[2],0],[x,ys[3],0],color=color),Dot([x,ys[2],0],radius=.09,color=color),Circle(radius=.2,color=color).move_to([x,ys[3],0]),Line([x-.2,ys[3],0],[x+.2,ys[3],0],color=color),Line([x,ys[3]-.2,0],[x,ys[3]+.2,0],color=color))
            gates.add(gate)
            group.add(txt(['계산','보존','되감기'][j],22,color).move_to([x,-1.35,0]))
        group.add(gates)
        return group,gates

    def construct(self):
        self.add(self.label('INFORMATION THEORY / 13',7.25,20,MUTED),self.label('삭제하지 말고 되감아라',6.4,36),Line([-3.8,5.8,0],[3.8,5.8,0],color=MUTED,stroke_opacity=.3))
        captions=['AND의 출력 0만으로는 원래 입력을 구분할 수 없다','입력을 보존하면 되돌릴 단서가 남는다','입력 1, 1은 보존 / 작업 칸 0 → 1','지금 되감으면 결과도 원래 0으로 돌아간다','중간 계산값을 그냥 삭제하지 않는다','먼저 별도 결과 칸에 보존한다','작업 칸만 되감으면, 보존한 결과는 남는다','남겨둔 입력으로 원래 상태를 복원한다','Toffoli: 같은 연산을 두 번 하면 원래 상태','같은 세 게이트를 양자 회로에서도 사용할 수 있다','보조 큐빗은 분리된 |0〉로 / 결과는 남는다','측정과 리셋은 이상적인 유니터리 게이트와 다르다','가역성 ≠ 실제 소비 에너지 0','결과 보존 → 중간 계산 되감기 → 작업 칸 재사용']
        self.stage=VGroup();cap=VGroup()
        for i,(start,end,_,__) in enumerate(CUES):
            if i:self.play(FadeOut(cap),run_time=.2)
            cap=self.label(captions[i],-5.95,23);self.play(FadeIn(cap),run_time=.2)
            if i==0:
                stage=VGroup(self.label('결과만 남긴 AND',4.9,33))
                for x,value in [(-2.5,'00'),(0,'01'),(2.5,'10')]:
                    stage.add(txt(value,43,WEIGHT).move_to([x,2.8,0]),Arrow([x,2.15,0],[0,.65,0],color=MUTED,buff=.15))
                out=txt('0',62,PRUNE).move_to([0,.05,0]);stage.add(out,self.label('입력은 어느 것이었을까?',-1.75,32),self.label('세 입력이 같은 결과로 합쳐진다',-3.25,28,MUTED),self.label('11 → 1 / 나머지 세 입력 → 0',-4.65,24,MUTED));self.swap(stage)
                self.play(Indicate(out,color=PRUNE),run_time=.6)
            elif i==1:
                stage=VGroup(self.label('삭제하지 않고 계산하려면?',4.9,32))
                before,*_=self.register((1,1,0,0),y=2.45)
                stage.add(before,self.label('입력은 그대로 / 작업 칸만 바꾼다',.25,30,WEIGHT),self.label('입력을 남기면 되돌릴 단서가 있다',-1.5,30,GOOD),self.label('앞 편: 여러 상태를 하나로 지우면 물리적 비용',-3.15,25,MUTED),self.label('이번 편: 삭제 대신 역연산',-4.55,30,ACCENT));self.swap(stage)
            elif i in (2,3,5,6):
                old,new,heading,operation={2:(TRACE[0],TRACE[1],'먼저 작업 칸에서 계산','두 입력이 모두 1 → 작업 칸 뒤집기'),3:(TRACE[1],TRACE[0],'그냥 되감으면 결과도 되돌아간다','같은 연산을 다시 적용'),5:(TRACE[1],TRACE[2],'결과를 별도 칸에 먼저 보존','작업 칸이 1 → 결과 칸 뒤집기'),6:(TRACE[2],TRACE[3],'작업 칸의 계산만 되감는다','입력 1, 1로 작업 칸을 다시 뒤집기')}[i]
                registers,digits,boxes=self.register(old)
                stage=VGroup(self.label(heading,4.9,29),registers,self.label(operation,-.2,31,ACCENT))
                if i==2:stage.add(self.label('작업 칸: 0 → 1',-1.55,34,PRUNE),self.label('입력은 변하지 않는다',-3.1,30,WEIGHT))
                elif i==3:stage.add(self.label('작업 칸: 1 → 0',-1.55,34,PRUNE),self.label('아직 별도 결과를 보존하지 않았기 때문',-3.1,26,MUTED))
                elif i==5:stage.add(self.label('작업 t = 1 → 결과 r = 1',-1.55,31,GOOD),self.label('빈 결과 칸은 0에서 시작',-3.1,27,MUTED))
                else:stage.add(self.label('작업 t: 1 → 0',-1.55,32,PRUNE),self.label('결과 r: 1 그대로',-3.1,34,GOOD))
                stage.add(self.label('입력 a, b / 작업 t / 보존한 결과 r',-4.65,22,MUTED));self.swap(stage)
                target=3 if i==5 else 2
                if i==5:
                    arrow=Arrow(boxes[2].get_bottom()+DOWN*.08,boxes[3].get_bottom()+DOWN*.08,path_arc=.5,color=GOOD,buff=.1);self.stage.add(arrow);self.play(Create(arrow),run_time=.5)
                self.play(Transform(digits[target],txt(str(new[target]),48,GOOD if target==3 else PRUNE).move_to(digits[target])),run_time=.8)
                self.play(Indicate(boxes[target],color=GOOD,scale_factor=1.07),run_time=.5)
            elif i==4:
                stage=VGroup(self.label('긴 계산에서는 중간값이 쌓인다',4.9,30))
                for j in range(6):
                    block=RoundedRectangle(width=4.7,height=.7,corner_radius=.1,stroke_color=PRUNE,fill_color=PRUNE,fill_opacity=.07).move_to([0,3.45-j*.86,0])
                    stage.add(block,txt(f'중간값 t{j+1}',26,PRUNE).move_to(block))
                stage.add(self.label('garbage bits / 남은 중간 상태',-2.45,27,MUTED),self.label('그냥 지우면 다시 비가역적',-3.7,30,PRUNE),self.label('계산 기록을 어떻게 정리할까?',-4.75,25,ACCENT));self.swap(stage)
            elif i==7:
                stage=VGroup(self.label('Uncomputation / 삭제 대신 되감기',4.9,29))
                for y,name,state,color in [(3.2,'계산',TRACE[1],WEIGHT),(1.2,'결과 보존',TRACE[2],GOOD),(-.8,'작업만 되감기',TRACE[3],ACCENT)]:
                    stage.add(txt(name,25,color).move_to([-2.5,y,0]),txt(' '.join(map(str,state)),38,color).move_to([1.3,y,0]))
                stage.add(self.label('순서: 입력 a b / 작업 t / 결과 r',-2.1,23,MUTED),self.label('작업 칸의 0은 역연산으로 복원한 0',-3.35,29,GOOD),self.label('남겨둔 입력이 되돌릴 단서를 제공한다',-4.65,25,MUTED));self.swap(stage)
            elif i==8:
                self.swap(VGroup(self.label('Toffoli gate',4.9,34,GOOD),self.label('(a, b, t) ↔ (a, b, t ⊕ ab)',3.65,30,WEIGHT),self.label('입력 a, b는 보존',2.4,27,MUTED),self.label('110 → 111 → 110',.7,38,ACCENT),self.label('a = b = 1일 때만 t를 뒤집는다',-1.05,29),self.label('8개 입력 ↔ 8개 출력',-2.65,34,GOOD),self.label('같은 게이트를 다시 적용하면 처음 상태',-4.3,26,MUTED)))
            elif i==9:
                circuit,gates=self.circuit()
                self.swap(VGroup(self.label('이 회로는 양자 계산에도 쓰인다',4.9,29),circuit,self.label('Toffoli → CNOT → Toffoli',-2.5,29,GOOD),self.label('이상적 게이트: U† U = I',-3.65,29,WEIGHT),self.label('역회로: 역순으로, 각 게이트의 역연산 적용',-4.7,22,MUTED)))
                self.play(LaggedStart(*(Indicate(gate,color=ACCENT,scale_factor=1.08) for gate in gates),lag_ratio=.3),run_time=1.2)
            elif i==10:
                upper,ud,ub=self.register((0,0,0,0),y=2.3)
                lower,ld,lb=self.register((1,1,1,1),y=-.5)
                lower.remove(*(lower[j] for j in (2,5,8,11)))
                plus=txt('+',36,ACCENT).move_to([0,.9,0])
                stage=VGroup(self.label('중첩에서도 같은 회로로 되감는다',4.9,29),upper,lower,plus,self.label('한 양자상태의 두 항 / 같은 크기의 중첩',-2.05,23,MUTED),self.label('두 항 모두 작업 t가 0으로',-3.25,30,GOOD),self.label('결과 r은 그대로 / 보조 큐빗은 분리된 |0〉',-4.35,23,GOOD),self.label('알 수 없는 양자상태의 복제가 아님 / 기저값의 저장',-5.05,19,MUTED))
                self.swap(stage)
                self.play(Transform(ld[2],txt('0',48,PRUNE).move_to(ld[2])),run_time=.8)
                self.play(Indicate(ub[2],color=GOOD),Indicate(lb[2],color=GOOD),run_time=.6)
            elif i==11:
                self.swap(VGroup(self.label('측정과 리셋은 다른 과정',4.9,32),self.label('|ψ〉 → 측정 → 고전적 기록',2.9,31,PRUNE),self.label('같은 역게이트만으로 복원할 수 없음',1.4,28,PRUNE),self.label('이상적인 게이트 계산: 가역적',-.65,31,GOOD),self.label('측정 · 리셋 · 실제 잡음: 별도 고려',-2.25,27,MUTED),self.label('양자컴퓨터 전체가 항상 가역적인 것은 아님',-4.1,24,ACCENT)))
            elif i==12:
                self.swap(VGroup(self.label('가역적 ≠ 실제 소비 에너지 0',4.9,30,PRUNE),self.label('삭제를 피할 수 있는 계산 구성',2.8,32,GOOD),self.label('대신 필요한 것',1.25,27,MUTED),self.label('추가 작업 칸 + 결과 보존 칸',-.25,30,WEIGHT),self.label('정방향 계산 + 역방향 계산',-1.75,30,ACCENT),self.label('실제 장치는 여전히 구동·손실 비용을 가진다',-3.65,25,MUTED),self.label('Landauer 삭제 하한 ≠ 전체 시스템 소비',-4.7,22,MUTED)))
            else:
                registers,*_=self.register(TRACE[3],y=2.1)
                self.swap(VGroup(self.label('결과는 남기고, 중간 계산은 되감는다',4.9,28),registers,self.label('입력 보존 / 작업 0 / 결과 1',.3,29,GOOD),self.label('계산 → 결과 보존 → 되감기',-1.45,32,ACCENT),self.label('Don’t erase. Uncompute.',-3.1,34,GOOD),self.label('정보를 지우지 않고도 계산을 구성할 수 있다',-4.65,26)))
            self.to(end)
