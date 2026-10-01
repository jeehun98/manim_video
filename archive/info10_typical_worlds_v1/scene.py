"""Probability per candidate versus the mass of many candidates."""
import sys,math
from pathlib import Path
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import txt,MUTED,WEIGHT,PRUNE,GOOD,ACCENT,SPARSE
from episodes.info10_typical_worlds.content import CUES,DURATION,H,MODE_PROB,ONE_TEN,TEN_COUNT,TEN_MASS,BAND_MASS,EXAMPLES,RADII,ANGLES,SHELL_MASS

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

    def construct(self):
        self.add(self.label('INFORMATION THEORY / 10',7.25,20,MUTED),self.label('가장 유력한 한 줄이 핵심일까?',6.4,33),
            Line([-3.8,5.8,0],[3.8,5.8,0],color=MUTED,stroke_opacity=.3))
        caps=['가장 높은 단일 확률과, 많은 확률질량은 다르다','모두 H인 100회 결과 / 약 0.00266%','비슷한 비율이어도, T의 위치마다 다른 줄','한 줄은 작지만, 같은 유형의 줄은 약 17.3조 개','100회 예시와, 긴 데이터의 전형집합을 구분','Typical Set ≠ 가장 유력한 한 줄','긴 데이터: 작은 확률 × 많은 후보 ≈ 1','전형적인 후보에 번호를 붙이면 약 nH bits','바깥 예외도 별도 표현 → 무손실','전체 가능한 세계와, 주로 만나는 세계','점의 밀도 최대인 원점 ≠ 질량이 모이는 껍질','밀도 × 공간의 부피 → 거리별 확률질량','mode와 typical region은 다를 수 있다']
        self.stage=VGroup();cap=VGroup()
        for i,(start,end,_,__) in enumerate(CUES):
            if i:self.play(FadeOut(cap),run_time=.2)
            cap=self.label(caps[i],-5.95,25);self.play(FadeIn(cap),run_time=.2)
            if i==0:
                coin=VGroup(Circle(radius=.9,color=WEIGHT,fill_color=WEIGHT,fill_opacity=.08),txt('H',65,WEIGHT)).move_to(UP*2.5)
                self.swap(VGroup(self.label('P(H)=0.9   /   P(T)=0.1',4.85,32),coin,self.label('가장 유력한 결과부터 고르면?',.2,33,ACCENT),self.label('압축의 한계도 보일까?',-2,36,ACCENT)))
            elif i==1:
                all_h=self.grid('H'*100,.32).move_to(UP*1.4)
                self.swap(VGroup(self.label('가장 유력한 한 줄: 전부 H',4.7,31,WEIGHT),all_h,self.label('10회: 0.9¹⁰ ≈ 34.87%',3.4,28,MUTED),
                    self.label('100회: 0.9¹⁰⁰',-.5,36,ACCENT),self.label(f'≈ {MODE_PROB*100:.5f}%',-1.75,44,PRUNE),self.label('1등인 줄도, 거의 발생하지 않는다',-3.65,29,PRUNE)))
                self.play(Indicate(all_h,color=WEIGHT),run_time=.6)
            elif i==2:
                examples=VGroup()
                for j,sequence in enumerate(EXAMPLES):
                    grid=self.grid(sequence,.145).move_to([(-1 if j%2==0 else 1)*1.8,2.5-(j//2)*2.4,0])
                    note=txt('H 90개 / T 10개',21,MUTED).next_to(grid,DOWN,buff=.35)
                    examples.add(VGroup(grid,note))
                self.swap(VGroup(self.label('T가 놓인 위치마다 다른 시퀀스',4.65,29),examples,self.label('같은 비율, 다른 순서',-2.1,34,ACCENT),self.label('90:10 유형의 배치 예시',-3.65,25,MUTED)))
                self.play(LaggedStart(*(Indicate(example[0],color=PRUNE) for example in examples),lag_ratio=.1),run_time=.8)
            elif i==3:
                self.swap(VGroup(self.label('100회 중 T가 정확히 10개인 경우',4.7,28,MUTED),self.grid(EXAMPLES[0],.27).move_to(UP*3.2),
                    self.label('한 줄의 확률 ≈ 7.62 × 10⁻¹⁵',1.8,31,WEIGHT),self.label('×  가능한 위치: 약 17.3조 개',.25,32,ACCENT),
                    self.label(f'= 전체 확률 {TEN_MASS*100:.2f}%',-1.4,40,GOOD),self.label('정확히 90:10인 유형만으로는 13.2%',-3.5,24,MUTED)))
            elif i==4:
                graph=VGroup(self.label('100회: T의 개수별 확률질량',4.75,29),self.label('같은 T개수의 모든 위치를 합산',3.85,23,MUTED))
                base_y=-.6;left=-3.6;width=.3
                from scipy.stats import binom
                for k in range(25):
                    prob=float(binom.pmf(k,100,.1));height=prob*22
                    color=GOOD if 5<=k<=15 else MUTED
                    bar=Rectangle(width=.22,height=max(.003,height),stroke_width=0,fill_color=color,fill_opacity=.9).move_to([left+k*width,base_y+height/2,0]);graph.add(bar)
                for k in range(0,25,5):graph.add(txt(str(k),20,MUTED).move_to([left+k*width,-1.05,0]))
                graph.add(Line([left,base_y,0],[3.6,base_y,0],color=MUTED),self.label('T 개수',-1.6,21,MUTED),
                    self.label(f'T 5~15개 → 확률 {BAND_MASS*100:.2f}%',-2.4,34,GOOD),self.label('이 주변을 모은 전형적인 결과들의 집합',-3.55,27,GOOD),self.label('정확히 10개만 모은 집합과 다르다',-4.6,22,MUTED))
                self.swap(graph)
            elif i==5:
                dots=VGroup(*(Dot([((j%12)-5.5)*.4,(j//12-2.5)*.45,0],radius=.07,color=GOOD) for j in range(72))).shift(DOWN*.3)
                box=RoundedRectangle(width=6.6,height=3.35,corner_radius=.22,stroke_color=GOOD).move_to(DOWN*.3)
                mode=Dot([-3.2,3.1,0],radius=.12,color=PRUNE)
                self.swap(VGroup(self.label('긴 i.i.d. 데이터의 Typical Set',4.8,30,GOOD),mode,txt('단일 최빈열',25,PRUNE).move_to([-.75,3.1,0]),box,dots,
                    self.label('중요한 것은 점 하나의 순위가 아니라',-2.9,27,MUTED),self.label('어느 집합에 질량이 모이는가',-4.15,31,ACCENT)))
                self.play(Indicate(box,color=GOOD),run_time=.7)
            elif i==6:
                self.swap(VGroup(self.label('충분히 긴 데이터 / 작은 허용오차',4.85,27,MUTED),self.label('전형적인 한 후보의 확률',3.4,29,WEIGHT),
                    self.label('≈ 2⁻ⁿᴴ',2.05,48,WEIGHT),self.label('×  전형적인 후보 수',.3,29,ACCENT),self.label('≈ 2ⁿᴴ',-1.05,48,ACCENT),
                    self.label('전체 확률질량 ≈ 1',-2.9,35,GOOD),self.label('지수 수준의 근사 / 유한 길이의 정확한 등식 아님',-4.45,22,MUTED)))
            elif i==7:
                items=VGroup()
                for row in range(4):
                    grid=self.grid(EXAMPLES[row],.1).move_to([-1.65,3.6-row*1.25,0])
                    code=txt(f'번호 {row:04b}',29,ACCENT).move_to([2,3.6-row*1.25,0]);items.add(VGroup(grid,code))
                self.swap(VGroup(self.label('후보마다 서로 다른 번호를 붙인다',4.9,29),items,self.label('log₂(2ⁿᴴ) = nH bits',-2.4,38,GOOD),
                    self.label('기호 하나당 ≈ H bits',-3.6,31,GOOD),self.label('번호는 개념도 / 실제 100회 코드의 길이와 구별',-4.65,21,MUTED)))
            elif i==8:
                self.swap(VGroup(self.label('전형적인 줄 → 짧은 번호',4.25,33,GOOD),self.label('드문 예외 → 별도 표시 + 원래 줄',2.5,29,PRUNE),
                    self.label('예외도 복원할 수 있어야 무손실',.55,29,ACCENT),self.label(f'평균 길이 / 기호 → H ≈ {H:.3f}',-1.6,32,GOOD),
                    self.label('긴 i.i.d. 데이터의 압축 한계',-3.3,31,GOOD),self.label('모든 100회 결과를 47비트에 넣는다는 뜻 아님',-4.6,21,MUTED)))
            elif i==9:
                outer=RoundedRectangle(width=7,height=5,corner_radius=.2,stroke_color=MUTED).move_to(UP*.65)
                inner=RoundedRectangle(width=3.9,height=2.3,corner_radius=.2,stroke_color=GOOD,fill_color=GOOD,fill_opacity=.08).move_to(DOWN*.1)
                self.swap(VGroup(self.label('같은 분포에서 n이 충분히 커지면',4.85,26,MUTED),outer,inner,
                    self.label('전체 가능한 줄: 2ⁿ',2.7,35,MUTED),self.label('전형적인 줄',.35,29,GOOD),self.label('≈ 2ⁿᴴ',-.75,44,GOOD),
                    self.label(f'편향된 동전: H ≈ {H:.3f} < 1',-2.9,29,ACCENT),self.label('그림의 면적은 후보 수의 실제 비율이 아님',-4.55,21,MUTED)))
            elif i==10:
                self.swap(self.shell())
                self.play(LaggedStart(*(Indicate(dot,scale_factor=1.3) for dot in self.shell_dots[:20]),lag_ratio=.03),run_time=.7)
            elif i==11:
                self.play(FadeOut(self.stage),run_time=.2)
                shell=self.shell();self.stage=shell
                self.play(FadeIn(shell),run_time=.4)
                self.play(FadeOut(shell[6]),FadeOut(shell[5]),run_time=.2)
                volume=self.label('밀도는 낮아져도\n사용할 공간은 커진다',.75,27,ACCENT)
                volume.scale_to_fit_width(3);self.stage.add(volume);self.play(FadeIn(volume),run_time=.3)
                self.play(Indicate(shell[2],color=ACCENT),run_time=.7)
            else:
                self.swap(VGroup(self.label('생성 모델에서도',4.7,28,MUTED),self.label('최고 likelihood ≠ 전형적인 샘플',3.25,30,PRUNE),
                    self.label('mode ≠ typical region',1.7,34,ACCENT),self.label('엔트로피가 결정하는 것은',-.2,32,GOOD),self.label('긴 데이터에서 구별할',-1.6,34,GOOD),
                    self.label('전형적인 세계의 수',-3.05,37,GOOD),self.label('후보 수 ≈ 2ⁿᴴ  →  번호 길이 ≈ nH',-4.5,26,ACCENT)))
            self.to(end)
