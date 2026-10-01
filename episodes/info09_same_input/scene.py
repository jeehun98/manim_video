"""Visible arithmetic processing cannot recover a collision introduced upstream."""
import sys
from pathlib import Path
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import txt,BG,MUTED,WEIGHT,PRUNE,GOOD,ACCENT,SPARSE
from episodes.info09_same_input.content import CUES,DURATION,F,g,COORDS

class SameInputProcessing(Scene):
    DURATION=DURATION

    def label(self,text,y,size=30,color=WHITE):
        return txt(text,size,color).move_to([0,y,0])

    def raw(self,s):
        colors={'A':WEIGHT,'B':PRUNE,'C':GOOD,'D':SPARSE}
        shapes={'A':Circle(radius=.55),'B':Square(side_length=1.05),'C':Triangle().scale_to_fit_height(1.1),'D':RegularPolygon(5).scale_to_fit_height(1.1)}
        shape=shapes[s].set_stroke(colors[s],2).set_fill(colors[s],.09)
        return VGroup(shape,txt(s,34,colors[s]))

    def number(self,n,color=ACCENT):
        return VGroup(RoundedRectangle(width=1.15,height=1.05,corner_radius=.14,stroke_color=color,fill_color=color,fill_opacity=.08),txt(str(n),36,color))

    def arrow(self,a,b,color=MUTED):
        return Arrow(a.get_right(),b.get_left(),buff=.09,color=color,stroke_width=2,max_tip_length_to_length_ratio=.15)

    def swap(self,new):
        if len(self.stage):self.play(FadeOut(self.stage),run_time=.2)
        self.stage=new
        self.play(FadeIn(new),run_time=.4)

    def to(self,target):
        rest=target-self.time
        if rest < -1/30:raise RuntimeError(f'Timing overrun: {rest}')
        frames=round(rest*30)
        if frames>0:self.wait(frames/30)

    def processing_board(self):
        ops=VGroup()
        for i,op in enumerate(['×5','+3','제곱','+8']):
            box=RoundedRectangle(width=1.5,height=.9,corner_radius=.12,stroke_color=WEIGHT,fill_color=WEIGHT,fill_opacity=.08)
            ops.add(VGroup(box,txt(op,30,WEIGHT)).move_to([(i-1.5)*1.8,3.6,0]))
        self.row_a=VGroup(*(self.number(n).move_to([(i-1.5)*1.8,1.35,0]) for i,n in enumerate([0,3,9,17])))
        self.row_b=VGroup(*(self.number(n).move_to([(i-1.5)*1.8,-1.35,0]) for i,n in enumerate([0,3,9,17])))
        self.links_a=VGroup(*(self.arrow(self.row_a[i],self.row_a[i+1]) for i in range(3)))
        self.links_b=VGroup(*(self.arrow(self.row_b[i],self.row_b[i+1]) for i in range(3)))
        self.note=self.label('×5에서는 0 그대로 / 이후 3 → 9 → 17',-3.75,26,MUTED)
        self.stage=VGroup(self.label('다음 가공 g / 입력은 Y뿐',4.95,29),ops,
            self.label('A에서 온 입력 0',2.45,26,MUTED),self.row_a,self.links_a,
            self.label('B에서 온 입력 0',-.25,26,MUTED),self.row_b,self.links_b,self.note)
        self.play(FadeIn(self.stage[0]),FadeIn(ops),FadeIn(self.stage[2]),FadeIn(self.row_a[0]),FadeIn(self.note),run_time=.4)
        self.play(Indicate(ops[0],color=ACCENT),Indicate(self.row_a[0],color=ACCENT),run_time=.4)
        for i in range(1,4):
            self.play(FadeIn(self.links_a[i-1]),FadeIn(self.row_a[i]),Indicate(ops[i],color=ACCENT),run_time=.6)

    def construct(self):
        self.add(self.label('INFORMATION THEORY / 09',7.25,20,MUTED),self.label('계산이 복잡해지면, 단서도 늘까?',6.4,33),
            Line([-3.8,5.8,0],[3.8,5.8,0],color=MUTED,stroke_opacity=.3))
        captions=['A와 B를 같은 0으로 만든 뒤라면?','가공 f: 네 상태를 두 그룹으로 합친다','Y=0으로는 A인지 B인지 구별 불가','가공 g: ×5 → +3 → 제곱 → +8','같은 0은 같은 연산을 거쳐 같은 17이 된다','숫자가 커져도, A/B를 가를 단서는 없다','이 가공은 그룹 두 개를 보존한다','두 그룹마저 합치면 그 구분도 사라진다','비교하는 양: 원본 X에 대한 정보','조건: Z는 Y만 이용해 만든다','읽기 쉬운 표현 ≠ 더 많은 원본 정보','다음: 어떤 구분을 버리고 남길까?']
        self.stage=VGroup();cap=VGroup()
        for i,(start,end,_,__) in enumerate(CUES):
            if i:self.play(FadeOut(cap),run_time=.2)
            cap=self.label(captions[i],-5.95,25)
            self.play(FadeIn(cap),run_time=.2)
            if i==0:
                originals=VGroup(*(self.raw(s).move_to([(j-1.5)*1.8,2.3,0]) for j,s in enumerate('ABCD')))
                self.swap(VGroup(self.label('원본 X / 네 상태는 같은 확률',4.6,29,MUTED),originals,
                    self.label('A와 B가 똑같은 0이 되었다면',.1,32,ACCENT),self.label('다시 가공하면 구분이 돌아올까?',-2,31,ACCENT)))
                self.play(Indicate(VGroup(originals[0],originals[1]),color=ACCENT),run_time=.6)
            elif i==1:
                raw=VGroup(*(self.raw(s).move_to([-2.7,3.6-j*1.65,0]) for j,s in enumerate('ABCD')))
                zero=self.number(0).move_to([2.7,2.78,0]);one=self.number(1).move_to([2.7,-.52,0])
                machine=VGroup(RoundedRectangle(width=1.25,height=5.8,corner_radius=.16,stroke_color=MUTED,fill_color=BG,fill_opacity=.97).move_to([0,1.1,0]),txt('가공\nf',25).move_to([0,1.1,0]))
                arrows=VGroup(*(self.arrow(raw[j],zero if j<2 else one) for j in range(4)))
                self.swap(VGroup(self.label('X',4.85,32).move_to([-2.7,4.85,0]),self.label('Y',4.85,32).move_to([2.7,4.85,0]),arrows,machine,raw,zero,one,
                    self.label('원본을 보관하지 않고, 그룹 값만 남긴다',-3.2,26,ACCENT),self.label('A/B → 0     C/D → 1',-4.35,29,ACCENT)))
                copies=VGroup(*(token.copy() for token in raw));self.add(copies)
                self.play(*(Transform(copies[j],(zero if j<2 else one).copy()) for j in range(4)),run_time=1)
                self.remove(copies)
            elif i==2:
                a=self.raw('A').move_to([-2.7,1.4,0]);b=self.raw('B').move_to([-2.7,-1.5,0])
                za=self.number(0).move_to([0,1.4,0]);zb=self.number(0).move_to([0,-1.5,0])
                qa=txt('A? B?',30,MUTED).move_to([2.7,1.4,0]);qb=qa.copy().move_to([2.7,-1.5,0])
                self.swap(VGroup(self.label('Y=0을 보고 원본을 되짚으면',4.5,30),a,b,za,zb,qa,qb,
                    self.arrow(a,za),self.arrow(b,zb),self.arrow(za,qa),self.arrow(zb,qb),self.label('0에는 A/B를 가르는 표시가 없다',-3.8,29,ACCENT)))
                self.play(Indicate(VGroup(za,zb),color=ACCENT),run_time=.8)
            elif i==3:
                self.play(FadeOut(self.stage),run_time=.2)
                self.processing_board()
            elif i==4:
                self.play(FadeIn(self.stage[5]),FadeIn(self.row_b[0]),run_time=.3)
                for j in range(1,4):self.play(FadeIn(self.links_b[j-1]),FadeIn(self.row_b[j]),run_time=.6)
                self.play(Indicate(VGroup(self.row_a[-1],self.row_b[-1]),color=GOOD),run_time=.7)
            elif i==5:
                self.play(Transform(self.note,self.label('0이든 17이든, 원본은 A 또는 B',-3.75,28,ACCENT)),run_time=.4)
                self.play(Indicate(VGroup(self.row_a[-1],self.row_b[-1]),color=PRUNE),run_time=.8)
            elif i==6:
                z0=self.number(0).move_to([-2.7,2.7,0]);z1=self.number(1).move_to([-2.7,-.1,0])
                r0=self.number(17,GOOD).move_to([2.7,2.7,0]);r1=self.number(72,GOOD).move_to([2.7,-.1,0])
                self.swap(VGroup(self.label('모양을 바꿔도 그룹은 둘',4.65,32,GOOD),z0,z1,r0,r1,self.arrow(z0,r0),self.arrow(z1,r1),
                    txt('A / B',27,MUTED).move_to([2.7,1.5,0]),txt('C / D',27,MUTED).move_to([2.7,-1.3,0]),
                    self.label('17과 72를 보면, 0과 1을 구별할 수 있음',-2.85,26,ACCENT),self.label('가공해도 구분이 유지되는 경우',-4.15,27,GOOD)))
                self.play(Indicate(VGroup(r0,r1),color=GOOD),run_time=.6)
            elif i==7:
                zero=self.number(0).move_to([-2.7,2.2,0]);one=self.number(1).move_to([-2.7,-.4,0]);out=self.number(17,PRUNE).move_to([2.6,.9,0])
                candidates=VGroup(*(self.raw(s).scale(.65) for s in 'ABCD')).arrange(RIGHT,buff=.45).move_to(DOWN*3)
                self.swap(VGroup(self.label('다른 가공: 두 값 모두 17로',4.6,31,PRUNE),zero,one,out,self.arrow(zero,out),self.arrow(one,out),
                    self.label('어느 그룹에서 왔는지도 모른다',-1.65,28,PRUNE),candidates,self.label('원본 후보 A / B / C / D 전부 남음',-4.25,26,MUTED)))
                self.play(Indicate(out,color=PRUNE),run_time=.6)
            elif i==8:
                graph=VGroup(self.label('원본 X를 구별하는 데 남은 정보',4.9,28,MUTED))
                for row,(label,bits,color) in enumerate([('원본 X 자체',2,WEIGHT),('두 그룹 Y',1,ACCENT),('17 / 72로 보존',1,GOOD),('둘 다 17로 합침',0,PRUNE)]):
                    y=3.65-row*1.7
                    graph.add(self.label(f'{label}   {bits} bits',y,29,color))
                    bar=Rectangle(width=max(.001,bits*2.55),height=.4,stroke_width=0,fill_color=color,fill_opacity=1 if bits else 0).move_to([-2.55+bits*1.275,y-.65,0])
                    graph.add(bar)
                graph.add(self.label('숫자의 크기·연산 횟수를 세는 것이 아니다',-4.35,24,MUTED))
                self.swap(graph)
            elif i==9:
                self.swap(VGroup(self.label('X → Y → Z',4.15,42,WEIGHT),self.label('Z는 Y만 보고 계산',2.6,31,ACCENT),
                    self.label('I(X;Z) ≤ I(X;Y)',.65,40,GOOD),self.label('DATA PROCESSING',-1.15,34,GOOD),self.label('INEQUALITY',-2.15,34,GOOD),
                    self.label('새 관측·원본으로부터의 우회 입력 없음',-3.7,25,MUTED)))
            elif i==10:
                graphic=VGroup(self.label('신경망 표현도, 기존 입력을 가공한다',4.8,28,MUTED))
                left=Square(side_length=2.35,stroke_color=MUTED).move_to([-2.1,1.65,0]);right=Line([.85,1.65,0],[3.25,1.65,0],color=MUTED)
                graphic.add(left,right,txt('원본 X',27).move_to([-2.1,3.3,0]),txt('특징 h',27).move_to([2.1,3.3,0]),Arrow([-.65,1.65,0],[.7,1.65,0],buff=.05,color=ACCENT))
                for s,(x,y) in COORDS.items():
                    color=GOOD if F[s]==0 else PRUNE
                    point=Dot([-3.05+1.9*x,.7+1.9*y,0],radius=.12,color=color)
                    text=txt(s,22,color).next_to(point,DOWN,buff=.12)
                    graphic.add(point,text)
                graphic.add(Dot([1.25,1.65,0],radius=.12,color=GOOD),Dot([2.95,1.65,0],radius=.12,color=PRUNE),
                    txt('A/B',25,GOOD).move_to([1.25,.9,0]),txt('C/D',25,PRUNE).move_to([2.95,.9,0]),
                    self.label('대각선으로 섞인 그룹 → 쉽게 읽히는 두 그룹',-.5,25,ACCENT),
                    self.label('그룹은 읽기 쉬워져도',-2.1,32,GOOD),self.label('네 원본 좌표는 복원할 수 없다',-3.5,28,PRUNE),self.label('고정 변환 예시 / 새로운 관측 없음',-4.5,22,MUTED))
                self.swap(graphic)
            else:
                originals=VGroup(*(self.raw(s).scale(.6) for s in 'ABCD')).arrange(RIGHT,buff=.3).move_to(UP*3.1)
                self.swap(VGroup(self.label('어떤 구분을 남겨야 할까?',4.8,34,ACCENT),originals,
                    self.label('원본을 많이 남기기',.85,31,WEIGHT),self.label('목적에 필요한 그룹만 남기기',-1.5,31,GOOD),self.label('다음: 버릴 정보와 남길 정보',-3.9,28,ACCENT)))
            self.to(end)
