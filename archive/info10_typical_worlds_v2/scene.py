"""Probability per candidate versus the mass of many candidates."""
import sys,math
from pathlib import Path
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import txt,MUTED,WEIGHT,PRUNE,GOOD,ACCENT,SPARSE
from episodes.info10_typical_worlds.content import CUES,DURATION,H,MODE_PROB,ONE_TEN,TEN_COUNT,TEN_MASS,BAND_MASS,EXAMPLES,RADII,ANGLES,SHELL_MASS,DEMO,CODE,RAW

class TypicalWorlds(Scene):
    DURATION=DURATION

    def label(self,text,y,size=30,color=WHITE):
        item=txt(text,size,color)
        if item.width>7.7:item.scale_to_fit_width(7.7)
        return item.move_to([0,y,0])

    def grid(self,sequence,cell=.13):
        group=VGroup()
        for i,s in enumerate(sequence):
            color=WEIGHT if s=='H' else PRUNE
            square=Square(side_length=cell*.8,stroke_width=0,fill_color=color,fill_opacity=.85)
            square.move_to([((i%20)-9.5)*cell,(2-i//20)*cell,0]);group.add(square)
        return group

    def swap(self,stage):
        if len(self.stage):self.play(FadeOut(self.stage),run_time=.2)
        self.stage=stage;self.play(FadeIn(stage),run_time=.4)

    def to(self,target):
        remain=target-self.time
        if remain < -1/30:raise RuntimeError(f'Cue overrun {remain}')
        frames=round(remain*30)
        if frames>0:self.wait(frames/30)

    def shell(self):
        center=np.array([0,.75,0]);scale=.2
        ring=Annulus(inner_radius=8*scale,outer_radius=12*scale,color=GOOD,fill_opacity=.12,stroke_width=0).move_to(center)
        inner=Circle(radius=8*scale,color=GOOD,stroke_opacity=.5).move_to(center)
        outer=Circle(radius=12*scale,color=GOOD,stroke_opacity=.5).move_to(center)
        dots=VGroup(*(Dot(center+np.array([scale*r*math.cos(a),scale*r*math.sin(a),0]),radius=.025,color=GOOD) for r,a in zip(RADII,ANGLES)))
        origin=Dot(center,radius=.065,color=PRUNE)
        origin_note=txt('원점: 밀도 최대',25,PRUNE).move_to([0,.75,0]).shift(DOWN*.65)
        self.shell_dots=dots
        return VGroup(self.label('100차원 표준 가우시안',4.9,30),self.label('x ~ N(0, I₁₀₀)',3.9,31,WEIGHT),ring,inner,outer,origin,origin_note,dots,
            self.label('샘플 거리 ≈ √100 = 10',-2.65,31,GOOD),self.label(f'거리 8~12에 확률 {SHELL_MASS*100:.2f}%',-3.65,27,GOOD),
            self.label('거리 분포의 개념도 / 실제 2차원 투영 아님',-4.7,21,MUTED))

    def bit_text(self,bits,size=30,columns=20):
        return txt('\n'.join(bits[i:i+columns] for i in range(0,len(bits),columns)),size,WEIGHT)

    def meter(self,value,y,color):
        bar=Rectangle(width=6.8*value/100,height=.62,stroke_width=0,fill_color=color,fill_opacity=.8)
        bar.move_to([-3.4+bar.width/2,y,0])
        note=txt(f'{value} bits',34,color).next_to(bar,DOWN,buff=.22)
        return VGroup(bar,note)

    def construct(self):
        self.add(self.label('INFORMATION THEORY / 10',7.25,20,MUTED),self.label('100비트 대신 번호를 보내면?',6.4,34),
            Line([-3.8,5.8,0],[3.8,5.8,0],color=MUTED,stroke_opacity=.3))
        caps=['100비트 → 47비트 / 같은 데이터로 복원할 수 있을까?','그대로 보내기: H=0, T=1 → 100 bits','실제 47-bit 부호를 해독하면 같은 100개가 나온다','H 90개 / T 10개: 위치만 달라도 다른 후보','100회에서 T 5~15개의 확률은 93.64%','긴 데이터: 전형적인 후보에 번호를 붙인다','100개당 약 47비트 / 긴 데이터의 평균 한계 환산','모든 100비트 문자열을 47비트에 넣는 것은 아니다','후보 수의 증가율이, 번호의 길이를 결정한다','드문 예외도 보내야 무손실이다','한 줄의 순위보다, 많은 줄에 모인 확률질량','다음 확장: 최고 밀도와 전형적인 영역은 다를 수 있다','엔트로피 = 전형적인 후보 수의 증가율']
        self.stage=VGroup();cap=VGroup()
        for i,(start,end,_,__) in enumerate(CUES):
            if i:self.play(FadeOut(cap),run_time=.2)
            cap=self.label(caps[i],-5.95,24);self.play(FadeIn(cap),run_time=.2)
            if i==0:
                self.swap(VGroup(self.label('앞면 90%인 동전 / 100번',4.7,30,MUTED),
                    self.meter(100,3,WEIGHT),self.meter(47,.65,GOOD),
                    self.label('덜 보냈는데, 같은 줄이 돌아온다?',-1.5,32,ACCENT),
                    self.label('47비트 실제 예시부터 확인',-3.5,29,GOOD)))
            elif i==1:
                bits=self.bit_text(RAW,25).move_to(UP*1.25)
                self.swap(VGroup(self.label('이번 결과: H 90개 / T 10개',4.8,29,MUTED),self.grid(DEMO,.29).move_to(UP*3.5),
                    bits,self.label('H = 0     T = 1',-.9,29,ACCENT),self.label('20개 × 5줄 = 100 bits',-2.5,37,WEIGHT),
                    self.label('기호마다 1비트씩 그대로 전송',-4.2,27,MUTED)))
                self.play(Indicate(bits,color=WEIGHT),run_time=.6)
            elif i==2:
                code=self.bit_text(CODE,31,16).move_to(UP*2.2)
                recovered=self.grid(DEMO,.3).move_to(DOWN*1.8)
                box=RoundedRectangle(width=6.8,height=2.05,corner_radius=.2,stroke_color=GOOD).move_to(DOWN*1.7)
                self.swap(VGroup(self.label('보내는 번호: 실제 47 bits',4.6,33,GOOD),code,
                    Arrow([0,.7,0],[0,.15,0],buff=.03,color=ACCENT),self.label('수신자: 같은 번호표로 해독',-.35,26,ACCENT),box,recovered,
                    self.label('원래 100개, 하나도 다르지 않다',-3.15,30,GOOD),self.label('공유 조건: P(H)=0.9 / 길이=100',-4.15,23,MUTED),
                    self.label('산술 부호화의 실제 예시 / 모든 줄이 47비트인 것은 아님',-4.9,19,MUTED)))
                self.play(Indicate(recovered,color=GOOD),run_time=.6)
            elif i==3:
                rows=VGroup()
                for j,seq in enumerate(EXAMPLES[:3]):
                    rows.add(self.grid(seq,.28).move_to(UP*(3.4-j*1.55)))
                self.swap(VGroup(self.label('T의 위치마다 다른 데이터열',4.9,29),rows,
                    self.label('뒷면이 정확히 10개인 후보만',-1.85,29,MUTED),self.label('약 17.3조 개',-3.25,48,ACCENT),
                    self.label('C(100,10) = 17,310,309,456,440',-4.5,24,MUTED)))
                self.play(LaggedStart(*(Indicate(r,color=PRUNE) for r in rows),lag_ratio=.1),run_time=.6)
            elif i==4:
                from scipy.stats import binom
                graph=VGroup(self.label('같은 개수의 모든 위치를 모으면',4.9,28),self.label('T가 정확히 10개: 확률 13.19%',3.95,27,MUTED))
                for k in range(25):
                    h=float(binom.pmf(k,100,.1))*22
                    graph.add(Rectangle(width=.22,height=max(.003,h),stroke_width=0,fill_color=GOOD if 5<=k<=15 else MUTED,fill_opacity=.85).move_to([-3.6+k*.3,-.5+h/2,0]))
                for k in range(0,25,5):graph.add(txt(str(k),21,MUTED).move_to([-3.6+k*.3,-.95,0]))
                graph.add(self.label('뒷면 개수',-1.5,23,MUTED),self.label('5~15개까지 모으면',-2.4,31,GOOD),self.label('확률 93.64%',-3.5,43,GOOD),
                    self.label('100회에서의 실제 수치 / 10개만으로 전형집합 전체가 아님',-4.7,20,MUTED))
                self.swap(graph)
            elif i==5:
                box=RoundedRectangle(width=6.8,height=3.4,corner_radius=.2,stroke_color=GOOD).move_to(UP*.8)
                rows=VGroup()
                for j in range(4):
                    y=1.95-j*.75
                    rows.add(self.grid(EXAMPLES[j],.095).move_to([-1.6,y,0]),txt(f'번호 {j+1}',25,ACCENT).move_to([2,y,0]))
                self.swap(VGroup(self.label('긴 i.i.d. 데이터의 Typical Set',4.8,30,GOOD),self.label('거의 모든 확률이 모이는 후보들',3.65,28,MUTED),box,rows,
                    self.label('줄 전체 대신, 몇 번째인지 보낸다',-1.8,31,ACCENT),self.label('후보 수 ≈ 2ⁿᴴ',-3.15,38,GOOD),
                    self.label('긴 데이터 / 작은 허용오차 / 지수 수준 근사',-4.6,21,MUTED)))
            elif i==6:
                self.swap(VGroup(self.label('앞면 90%인 동전의 엔트로피',4.8,28,MUTED),self.label('H ≈ 0.469 bit / 기호',3.45,36,ACCENT),
                    self.meter(100,1.7,WEIGHT),self.meter(47,-.55,GOOD),self.label('100 × 0.469 ≈ 46.9 bits',-2.45,34,GOOD),
                    self.label('긴 데이터의 평균 한계를 100개당 환산',-3.7,26,ACCENT),self.label('100개짜리 모든 블록의 정확한 코드 길이가 아님',-4.8,21,MUTED)))
            elif i==7:
                self.swap(VGroup(self.label('더 긴 묶음으로 보내면',4.7,32),self.label('10,000개를 그대로: 10,000 bits',3.25,30,WEIGHT),
                    self.label('평균 압축 한계: 약 4,690 bits',1.65,32,GOOD),self.label('100개당 약 47 bits',-.1,42,GOOD),
                    self.label('기호당 평균 길이 → 0.469 bit',-1.95,31,ACCENT),self.label('분포와 블록 길이는 양쪽에서 알고 있음',-3.65,24,MUTED),
                    self.label('유한 길이의 오버헤드 포함 실제 길이와 구별',-4.75,21,MUTED)))
            elif i==8:
                self.swap(VGroup(self.label('후보마다 다른 번호가 필요하다',4.9,30),self.label('2ⁿᴴ개 후보',3.4,41,GOOD),
                    Arrow([0,2.65,0],[0,1.75,0],color=ACCENT),self.label('log₂(2ⁿᴴ) = nH bits',.95,38,ACCENT),
                    self.label('번호가 너무 짧으면?',-.65,31,PRUNE),self.label('서로 다른 줄이 같은 번호로 겹친다',-2.15,28,PRUNE),
                    self.label('더 긴 데이터 → 더 많은 후보 → 더 긴 번호',-3.65,26,MUTED),self.label('i.i.d. 전형집합의 점근적 압축 한계',-4.8,22,MUTED)))
            elif i==9:
                self.swap(VGroup(self.label('전형적인 줄 → 짧은 번호',4.3,33,GOOD),self.label('드문 예외 → 별도 표시 + 원래 줄',2.6,30,PRUNE),
                    self.grid(DEMO,.3).move_to(UP*.7),self.label('같은 결과를 완전히 복원',-1,35,GOOD),
                    self.label('줄이는 것은 데이터의 내용이 아니라',-2.6,29,MUTED),self.label('데이터를 가리키는 번호의 길이',-4,32,ACCENT)))
            elif i==10:
                self.swap(VGroup(self.label('전부 H: 단일 시퀀스 확률 1등',4.8,29,WEIGHT),self.grid('H'*100,.3).move_to(UP*3.3),
                    self.label(f'하지만 100회 확률은 {MODE_PROB*100:.5f}%',1.65,31,PRUNE),self.label('한 줄의 순위',-.1,33,MUTED),
                    self.label('≠',-1.1,37,PRUNE),self.label('많은 줄에 모인 확률질량',-2.45,34,GOOD),self.label('중요한 것은 어느 집합에 질량이 모이는가',-4.1,26,ACCENT)))
            elif i==11:
                self.swap(self.shell())
            else:
                self.swap(VGroup(self.label('100개를 보내는 원시 표현',4.75,27,MUTED),self.label('100 bits',3.45,48,WEIGHT),
                    self.label('긴 데이터의 한계를 100개당 환산',1.85,27,MUTED),self.label('약 47 bits',.45,53,GOOD),
                    self.label('덜 보냈지만, 같은 결과를 복원한다',-1.4,32,ACCENT),self.label('엔트로피가 결정하는 것은',-2.85,30,GOOD),
                    self.label('전형적인 세계에 붙일 번호의 길이',-4.2,31,GOOD)))
            self.to(end)
