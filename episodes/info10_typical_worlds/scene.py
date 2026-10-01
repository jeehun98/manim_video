"""Why a shared candidate number is shorter, and why entropy fixes its rate."""
import sys
from pathlib import Path
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import txt,BG,MUTED,WEIGHT,PRUNE,GOOD,ACCENT
from episodes.info10_typical_worlds.content import CUES,DURATION,H,ONE_TEN,TEN_COUNT,TEN_MASS,BAND_MASS,EXAMPLES,TOY,TOY_CODES

class TypicalWorlds(Scene):
    DURATION=DURATION

    def label(self,text,y,size=30,color=WHITE):
        return txt(text,size,color).move_to([0,y,0])

    def grid(self,sequence,cell=.13):
        group=VGroup()
        for i,s in enumerate(sequence):
            square=Square(side_length=cell*.8,stroke_width=0,fill_color=WEIGHT if s=='H' else PRUNE,fill_opacity=.9)
            square.move_to([((i%20)-9.5)*cell,(2-i//20)*cell,0]);group.add(square)
        return group

    def strip(self,bits,cell=.22,numbers=True):
        group=VGroup()
        for i,bit in enumerate(bits):
            square=Square(side_length=cell*.9,stroke_width=.6,stroke_color=MUTED,fill_color=WEIGHT if bit=='0' else PRUNE,fill_opacity=.15)
            if numbers:square=VGroup(square,txt(bit,24,WEIGHT if bit=='0' else PRUNE,max_width=cell*.65))
            square.move_to([(i-(len(bits)-1)/2)*cell,0,0]);group.add(square)
        return group

    def chip(self,code,color=ACCENT,width=1.05):
        return VGroup(RoundedRectangle(width=width,height=.64,corner_radius=.12,stroke_color=color,fill_color=BG,fill_opacity=1),txt(code,30,color,max_width=width-.2))

    def monitors(self):
        group=VGroup()
        for x,name in [(-1.85,'보내는 사람'),(1.85,'받는 사람')]:
            panel=RoundedRectangle(width=3.35,height=3.7,corner_radius=.15,stroke_color=MUTED).move_to([x,1.65,0])
            group.add(panel,Line([x,-.2,0],[x,-.55,0],color=MUTED),Line([x-.6,-.55,0],[x+.6,-.55,0],color=MUTED),txt(name,26).move_to([x,4,0]),
                txt('번호',17,MUTED).move_to([x-1.06,3.13,0]),txt('원본 8 bits',17,MUTED).move_to([x+.4,3.13,0]))
            for row,(bits,code) in enumerate(zip(TOY,TOY_CODES)):
                y=2.7-row*.75
                group.add(txt(code,26,ACCENT).move_to([x-1.06,y,0]),self.strip(bits,.27).move_to([x+.4,y,0]))
        return group

    def meter(self,value,y,color):
        bar=Rectangle(width=6.8*value/100,height=.62,stroke_width=0,fill_color=color,fill_opacity=.85)
        bar.move_to([-3.4+bar.width/2,y,0])
        return VGroup(bar,txt(f'{value} bits',34,color).next_to(bar,DOWN,buff=.22))

    def swap(self,stage):
        if len(self.stage):self.play(FadeOut(self.stage),run_time=.2)
        self.stage=stage;self.play(FadeIn(stage),run_time=.4)

    def to(self,target):
        remaining=target-self.time
        if remaining < -1/30:raise RuntimeError(f'Cue overrun {remaining}')
        frames=round(remaining*30)
        if frames>0:self.wait(frames/30)

    def construct(self):
        self.add(self.label('INFORMATION THEORY / 10',7.25,20,MUTED),self.label('엔트로피가 압축 한계가 되는 이유',6.4,31),
            Line([-3.8,5.8,0],[3.8,5.8,0],color=MUTED,stroke_opacity=.3))
        captions=['100비트 → 가능한 문자열 2¹⁰⁰개','가능한 줄의 수와, 각 줄의 확률은 다르다','한 줄의 확률 × 그런 줄의 개수 = 전체 확률','뒷면 5, 6, …, 15개까지 모으면 93.64%','거의 항상 만나는 전형적인 집합: Typical Set','설명용 예시: 가능한 8비트 줄이 4개뿐일 때','같은 목록의 01번 → 같은 8비트 줄로 복원','1비트 번호 2개로는 후보 4개를 구별할 수 없다','4후보 → 2비트 / 8후보 → 3비트','전형적인 후보 수 ≈ 2ⁿᴴ → 번호 길이 ≈ nH','100개당 약 47비트: 긴 데이터의 평균 한계 환산','드문 결과에는 긴 표현 / 예외도 완전히 복원','후보의 수가 번호의 길이를 결정한다']
        self.stage=VGroup();cap=VGroup()
        for i,(start,end,_,__) in enumerate(CUES):
            if i:self.play(FadeOut(cap),run_time=.2)
            cap=self.label(captions[i],-5.95,24);self.play(FadeIn(cap),run_time=.2)
            if i==0:
                self.swap(VGroup(self.label('H=0 / T=1로 100번 기록하면',4.8,28,MUTED),self.grid(EXAMPLES[0],.32).move_to(UP*3.3),
                    self.label('100 bits',1.8,44,WEIGHT),self.label('가능한 줄은 몇 개?',.2,31,ACCENT),self.label('2¹⁰⁰개',-1.4,53,ACCENT),
                    self.label('각 자리에 0 또는 1 / 2 × 2 × … × 2',-3.3,27,MUTED)))
            elif i==1:
                coin=VGroup(Circle(radius=.8,color=WEIGHT,fill_color=WEIGHT,fill_opacity=.12),txt('H',52,WEIGHT)).move_to(UP*3.1)
                rows=VGroup(*(self.grid(seq,.21).move_to(UP*(1.25-j*1.15)) for j,seq in enumerate(EXAMPLES[:3])))
                self.swap(VGroup(self.label('앞면 H 90% / 뒷면 T 10%',4.85,31),coin,rows,self.label('모든 줄을 똑같이 자주 볼까?',-2.55,31,ACCENT),
                    self.label('주로 H 약 90개, T 약 10개 근처',-4.1,27,GOOD)))
            elif i==2:
                self.swap(VGroup(self.label('뒷면의 위치까지 정해진 한 줄',4.8,27,MUTED),self.grid(EXAMPLES[0],.27).move_to(UP*3.55),
                    self.label('한 줄의 확률',2.2,27,WEIGHT),self.label('0.9⁹⁰ × 0.1¹⁰ ≈ 7.62 × 10⁻¹⁵',1.3,30,WEIGHT),
                    self.label('×  뒷면 10개인 모든 위치 조합',-.05,28,ACCENT),self.label('약 17.3조 개',-1.15,39,ACCENT),
                    self.label('= 뒷면이 총 10개일 확률',-2.45,28,GOOD),self.label('13.19%',-3.55,47,GOOD),
                    self.label('위치는 상관없이, T가 정확히 10개인 모든 줄의 합',-4.75,21,MUTED)))
            elif i==3:
                from scipy.stats import binom
                graph=VGroup(self.label('정확히 10개뿐 아니라',4.9,28,MUTED),self.label('T = 5, 6, 7, …, 14, 15',3.9,30,ACCENT))
                for k in range(25):
                    h=float(binom.pmf(k,100,.1))*22
                    graph.add(Rectangle(width=.22,height=max(.003,h),stroke_width=0,fill_color=GOOD if 5<=k<=15 else MUTED,fill_opacity=.85).move_to([-3.6+k*.3,-.65+h/2,0]))
                for k in range(0,25,5):graph.add(txt(str(k),21,MUTED).move_to([-3.6+k*.3,-1.1,0]))
                graph.add(Line([-2.1,-1.6,0],[.9,-1.6,0],color=GOOD,stroke_width=4),Line([-2.1,-1.45,0],[-2.1,-1.65,0],color=GOOD),Line([.9,-1.45,0],[.9,-1.65,0],color=GOOD),self.label('이 범위의 모든 줄을 합치면',-2.35,29,GOOD),
                    self.label(f'{BAND_MASS*100:.2f}%',-3.45,46,GOOD),self.label('100회에서의 실제 수치 / 정확히 10개만 모은 집합과 다름',-4.75,20,MUTED))
                self.swap(graph)
            elif i==4:
                box=RoundedRectangle(width=6.5,height=2.7,corner_radius=.2,stroke_color=GOOD,fill_color=GOOD,fill_opacity=.08).move_to(UP*1.9)
                dots=VGroup(*(Dot([((j%12)-5.5)*.42,1.9+(j//12-2)*.4,0],radius=.065,color=GOOD) for j in range(60)))
                self.swap(VGroup(self.label('더 긴 i.i.d. 데이터에서는',4.9,27,MUTED),self.label('Typical Set / 전형집합',3.95,31,GOOD),box,dots,
                    self.label('거의 모든 확률이 이 집합에 모인다',-.15,29,GOOD),self.label('모든 줄에 똑같이 긴 표현이 필요할까?',-1.85,30,ACCENT),
                    self.label('주로 만나는 후보를 짧게 구별하면?',-3.5,29,ACCENT),self.label('긴 데이터의 개념도 / 100회 집합의 정확한 크기가 아님',-4.75,20,MUTED)))
            elif i==5:
                self.swap(VGroup(self.label('작은 목록으로 먼저 이해해보자',4.95,29,ACCENT),self.monitors(),
                    self.label('양쪽이 같은 목록을 알고 있다',-1.75,30,GOOD),self.label('가능한 원본: 이 4개뿐인 예시',-3.15,29,MUTED),
                    self.label('실제 압축에서는 거대한 표 대신 같은 부호화 규칙을 공유',-4.65,21,MUTED)))
            elif i==6:
                packet=self.chip('01',ACCENT,1.15).move_to([-2.2,-1.4,0])
                restored=self.strip(TOY[1],.5).move_to(DOWN*3.1)
                highlight=VGroup(*(RoundedRectangle(width=3.05,height=.62,corner_radius=.08,stroke_color=GOOD).move_to([x,1.95,0]) for x in (-1.85,1.85)))
                arrow=Arrow([-2.5,-1.4,0],[2.5,-1.4,0],buff=.02,color=ACCENT)
                self.swap(VGroup(self.label('줄 전체 대신 번호만 보낸다',4.95,30,ACCENT),self.monitors(),highlight,arrow,packet,self.label('01번을 찾으면 원본 8비트가 돌아온다',-2.35,27,GOOD),
                    self.label('번호 2비트 / 원본 8비트 / 같은 내용',-4.5,26,GOOD)))
                self.play(packet.animate.move_to([2.2,-1.4,0]),run_time=.8)
                self.stage.add(restored);self.play(FadeIn(restored),run_time=.4)
            elif i==7:
                stage=VGroup(self.label('1비트로는 번호가 0, 1 두 개뿐',4.9,29,PRUNE))
                for j,bits in enumerate(TOY):
                    y=3.2-j*1.0
                    strip=self.strip(bits,.23).move_to([-1.85,y,0]);stage.add(strip)
                    stage.add(Arrow([-.65,y,0],[1.1,2.7 if j<2 else .7,0],buff=.1,color=PRUNE,stroke_width=2))
                stage.add(self.chip('0',PRUNE).move_to([1.85,2.7,0]),self.chip('1',PRUNE).move_to([1.85,.7,0]),
                    self.label('0을 받으면, 두 줄 중 어느 것일까?',-1.45,29,PRUNE),self.label('복원하려면 서로 다른 번호가 필요',-2.9,28,MUTED),
                    self.label('4후보 → 00, 01, 10, 11 → 2 bits',-4.25,29,GOOD))
                self.swap(stage)
            elif i==8:
                top=VGroup(*(self.chip(format(j,'02b'),GOOD).move_to([(j%2-.5)*1.6,3.45-j//2*.9,0]) for j in range(4)))
                bottom=VGroup(*(self.chip(format(j,'03b'),WEIGHT,1.2).move_to([(j%4-1.5)*1.65,-.65-j//4*.9,0]) for j in range(8)))
                self.swap(VGroup(self.label('후보 4개 → 번호 2비트',4.85,31,GOOD),top,self.label('후보 8개 → 번호 3비트',.7,31,WEIGHT),bottom,
                    self.label('후보 수가 2ᴸ개라면 번호는 L비트',-3.2,31,ACCENT),self.label('후보가 늘어나면 번호도 길어진다',-4.6,28,MUTED)))
            elif i==9:
                box=RoundedRectangle(width=6.5,height=2.4,corner_radius=.16,stroke_color=GOOD).move_to(UP*2.7)
                rows=VGroup()
                for j in range(3):rows.add(self.grid(EXAMPLES[j],.1).move_to([-1.65,3.3-j*.6,0]),txt(f'번호 {j+1}',25,ACCENT).move_to([1.9,3.3-j*.6,0]))
                self.swap(VGroup(self.label('긴 데이터의 전형적인 후보로 돌아가면',4.95,28),self.label('n = 기호 수 / H = 엔트로피',4.25,23,MUTED),box,rows,self.label('…',1.7,30,MUTED),
                    self.label('후보 수 |Tₙ| ≈ 2ⁿᴴ',.4,35,GOOD),Arrow([0,-.15,0],[0,-.9,0],buff=.03,color=ACCENT),
                    self.label('번호 길이 ≈ log₂|Tₙ| ≈ nH bits',-1.55,32,ACCENT),self.label('기호 n개 → 약 nH비트',-3.1,29,GOOD),
                    self.label('기호 하나당 → 약 H비트',-4.35,30,GOOD)))
            elif i==10:
                self.swap(VGroup(self.label('앞면 90%인 동전: H ≈ 0.469',4.9,30,ACCENT),self.meter(100,3.15,WEIGHT),self.meter(47,.8,GOOD),
                    self.label('100 × 0.469 ≈ 46.9 bits',-1.35,35,GOOD),self.label('긴 데이터의 평균 한계를 100개당 환산',-3.05,26,ACCENT),
                    self.label('모든 100개 블록이 47비트라는 뜻은 아님',-4.55,23,MUTED)))
            elif i==11:
                box=RoundedRectangle(width=6.2,height=1.7,corner_radius=.2,stroke_color=GOOD).move_to(UP*2.85)
                codes=VGroup(*(self.chip(format(j,'03b'),GOOD,.8).scale(.8).move_to([(j-2)*1,2.7,0]) for j in range(5)))
                self.swap(VGroup(self.label('주로 만나는 줄 → 짧은 번호',4.75,31,GOOD),box,codes,
                    self.label('드문 줄도 존재한다',1.1,29,PRUNE),self.grid('T'*100,.25).move_to(DOWN*.05),
                    Arrow([0,-.9,0],[0,-1.8,0],buff=.03,color=PRUNE),self.label('별도 표시 + 더 긴 표현',-2.4,32,PRUNE),
                    self.label('예외도 버리지 않고 완전히 복원',-4.05,28,GOOD)))
            else:
                self.swap(VGroup(self.label('전형적인 후보 ≈ 2ⁿᴴ개',4.35,36,GOOD),Arrow([0,3.65,0],[0,2.95,0],buff=.03,color=ACCENT),
                    self.label('번호 길이 ≈ nH bits',2.2,37,ACCENT),Arrow([0,1.5,0],[0,.8,0],buff=.03,color=ACCENT),
                    self.label('기호당 압축 한계: H bits',.05,35,GOOD),self.label('후보의 수가',-1.8,33),self.label('번호의 길이를 결정한다',-3.15,35,GOOD),
                    self.label('독립 동일분포의 긴 데이터 / 점근적 평균 한계',-4.7,22,MUTED)))
            self.to(end)
