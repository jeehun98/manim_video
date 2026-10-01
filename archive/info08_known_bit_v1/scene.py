"""Remove the code column already supplied by X, retaining exact recovery."""
import sys
from pathlib import Path
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import txt,MUTED,WEIGHT,PRUNE,GOOD,ACCENT
from episodes.info08_known_bit.content import (
    CUES,DURATION,CODE,MESSAGE,FULL,SIDE,RESIDUAL,WEATHER_CONDITIONAL,WEATHER_MI,
)

class AlreadyKnownBit(Scene):
    DURATION=DURATION

    def label(self,text,y,size=30,color=WHITE):
        return txt(text,size,color).move_to([0,y,0])

    def cards(self,y=1):
        cards=VGroup()
        for i,symbol in enumerate('ABCD'):
            x=(i-1.5)*1.85
            box=RoundedRectangle(width=1.55,height=1.8,corner_radius=.14,stroke_color=GOOD if i<2 else WEIGHT,fill_opacity=.07,fill_color=GOOD if i<2 else WEIGHT)
            symbol_text=txt(symbol,37).move_to([0,.45,0])
            first=txt(CODE[symbol][0],36,ACCENT).move_to([-.22,-.4,0])
            second=txt(CODE[symbol][1],36,WEIGHT).move_to([.22,-.4,0])
            cards.add(VGroup(box,symbol_text,first,second).move_to([x,y,0]))
        return cards

    def meter(self,bits,y,color):
        box=Rectangle(width=max(.001,bits*2.7),height=.5,stroke_width=0,fill_color=color,fill_opacity=1 if bits else 0)
        return box.move_to([-2.7+box.width/2,y,0])

    def transmission(self,recovery=False):
        group=VGroup(self.label('같은 16개 / A·B·C·D 각 4개',4.6,27,MUTED))
        for r in range(2):
            group.add(self.label('  '.join(MESSAGE[r*8:r*8+8]),3.65-r*.65,30,WEIGHT))
        group.add(self.label('X 모름   →   Y: 32 bits',1.7,34,PRUNE))
        group.add(self.meter(2,.75,PRUNE))
        group.add(self.label('X 이미 앎   →   Y: 16 bits',-.6,34,GOOD))
        group.add(self.meter(1,-1.55,GOOD))
        group.add(self.label('두 방식 모두 동일한 원본 복원 ✓' if recovery else '받는 쪽에 X열이 이미 있다',-3,28,ACCENT))
        group.add(self.label('본문 길이 / 코드표·기호 수·정렬 공유',-4.35,22,MUTED))
        return group

    def to(self,target):
        remaining=target-self.time
        if remaining < -1/30: raise RuntimeError(f'Timing overrun {remaining}')
        if remaining>1e-7: self.wait(remaining)

    def construct(self):
        self.add(self.label('INFORMATION THEORY  /  08',7.25,20,MUTED),
                 self.label('하나를 알면, 몇 비트나 싸질까?',6.4,34),
                 Line([-3.8,5.8,0],[3.8,5.8,0],color=MUTED,stroke_opacity=.3))
        captions=['이미 알려준 비트는 다시 보내지 않는다','네 결과 × 두 자리 비트','X가 알려주는 것: 왼쪽 / 오른쪽','첫 비트를 지워도, 마지막 비트로 구별','32 bits → 16 bits / 같은 원본 복원','X값별로 남는 정보량을 평균','상호정보량 = 아낀 평균 비트','독립: 0 절약 / 완전한 예측: 2 절약','후보가 그대로여도, 확률이 달라진다','X까지 새로 보내면, 전체는 32 bits','평균 절약량 / 관측마다 감소를 보장하지 않음','다음: 새 관측 없이 가공만 한다면?']
        self.stage=VGroup();caption=VGroup()
        for i,(start,end,_,__) in enumerate(CUES):
            if i: self.play(FadeOut(self.stage),FadeOut(caption),run_time=.2)
            caption=self.label(captions[i],-5.9,25)
            self.play(FadeIn(caption),run_time=.2)
            if i in (0,4):
                self.stage=self.transmission(i==4)
                self.play(FadeIn(self.stage),run_time=.4)
                self.play(Indicate(self.stage[4],color=PRUNE),Indicate(self.stage[6],color=GOOD),run_time=.6)
            elif i==1:
                cards=self.cards(.8)
                self.stage=VGroup(self.label('Y ∈ {A, B, C, D}',4.25,35),self.label('각 확률 1/4',3.05,29,MUTED),cards,
                    self.label('두 비트면, 네 결과를 구별',-1.9,32,ACCENT),self.label('Y 한 번당 2 bits',-3.4,36,PRUNE))
                self.play(FadeIn(self.stage),run_time=.4)
                self.play(LaggedStart(*(Indicate(c[2:4],color=ACCENT) for c in cards),lag_ratio=.12),run_time=.8)
            elif i==2:
                cards=self.cards(1)
                tag=self.label('X = left',3.85,40,GOOD)
                hint=self.label('Y ∈ {A, B}',-1.7,40,GOOD)
                self.stage=VGroup(cards,tag,hint,self.label('4후보 → 2후보',-3.5,32,ACCENT))
                self.play(FadeIn(cards),FadeIn(tag),run_time=.4)
                self.play(cards[2].animate.set_opacity(.08),cards[3].animate.set_opacity(.08),run_time=.6)
                self.play(FadeIn(hint),FadeIn(self.stage[-1]),run_time=.3)
            elif i==3:
                cards=self.cards(2)
                self.stage=VGroup(cards,self.label('X가 이미 알려준 첫 비트',4.15,30,ACCENT),
                    self.label('X=left: 0→A / 1→B',-.65,29,GOOD),self.label('X=right: 0→C / 1→D',-1.8,29,WEIGHT),
                    self.label('추가로 보낼 것은 한 비트',-3.55,32,ACCENT))
                self.play(FadeIn(self.stage),run_time=.4)
                self.play(*(FadeOut(card[2],shift=UP*.5) for card in cards),run_time=.7)
                self.play(*(card[3].animate.shift(LEFT*.22) for card in cards),run_time=.3)
            elif i==5:
                left=self.label('X=left   A/B   → 1 bit',2.8,32,GOOD)
                right=self.label('X=right  C/D   → 1 bit',1.3,32,WEIGHT)
                average=self.label('½ × 1 + ½ × 1 = 1',-.5,36,ACCENT)
                self.stage=VGroup(self.label('어느 X를 알게 되는지도 평균',4.35,28,MUTED),left,right,average,
                    self.label('CONDITIONAL ENTROPY',-2,34,GOOD),self.label('H(Y|X) = 1 bit',-3.35,37,GOOD))
                self.play(FadeIn(self.stage[:3]),run_time=.4)
                self.play(FadeIn(self.stage[3:]),run_time=.5)
            elif i==6:
                before=self.meter(2,2.15,PRUNE);after=self.meter(1,-.1,GOOD)
                saved=Rectangle(width=2.7,height=.5,stroke_color=ACCENT,fill_color=ACCENT,fill_opacity=.35).move_to([1.35,2.15,0])
                self.stage=VGroup(self.label('원래  H(Y)=2',3.5,33,PRUNE),before,
                    self.label('X를 안 뒤  H(Y|X)=1',1.1,33,GOOD),after,
                    self.label('2 − 1 = 1 bit',-1.75,38,ACCENT),self.label('MUTUAL INFORMATION',-3,32,ACCENT),
                    self.label('I(X;Y) = H(Y) − H(Y|X)',-4.2,27,ACCENT),saved)
                self.play(FadeIn(self.stage),run_time=.4)
                self.play(saved.animate.move_to([0,-.95,0]),run_time=.6)
                self.play(FadeOut(saved),run_time=.2)
            elif i==7:
                self.stage=VGroup(self.label('독립인 X',4.35,32,MUTED),self.label('A  B  C  D  그대로',3.15,32,WEIGHT),
                    self.label('2 → 2 bits    I = 0',1.8,35,PRUNE),self.label('Y를 완전히 알려주는 X=Y',-.3,29,GOOD),
                    self.label('예: X=A → Y=A',-1.55,33,GOOD),self.label('2 → 0 bits    I = 2',-2.9,35,ACCENT),
                    self.label('별도 비교 모형 / 최대 절약량은 H(Y)',-4.3,22,MUTED))
                self.play(FadeIn(self.stage[:3]),run_time=.4)
                self.play(FadeIn(self.stage[3:]),run_time=.5)
            elif i==8:
                self.stage=VGroup(self.label('날씨 X / 우산 사용 Y',4.4,31),self.label('가상 모형: 비·맑음 각각 50%',3.35,23,MUTED))
                bars=VGroup()
                for y,p,label in [(1.8,.5,'날씨 모름'),(-.25,.9,'비라고 앎')]:
                    a=Rectangle(width=6*p,height=.55,fill_color=GOOD,fill_opacity=.9,stroke_width=0).move_to([-3+3*p,y,0])
                    b=Rectangle(width=6*(1-p),height=.55,fill_color=PRUNE,fill_opacity=.9,stroke_width=0).next_to(a,RIGHT,buff=0)
                    bars.add(VGroup(a,b,self.label(f'{label}: 씀 {round(p*100)}% / 안 씀 {round((1-p)*100)}%',y+.7,27)))
                self.stage.add(bars,self.label('맑음일 때는 반대: 씀 10% / 안 씀 90%',-1.25,23,MUTED),
                    self.label('어느 후보도 사라지지 않았다',-2.15,27,ACCENT),
                    self.label(f'평균 1 → {WEATHER_CONDITIONAL:.3f} bits',-3.2,31,GOOD),self.label(f'I ≈ {WEATHER_MI:.3f} bits / 이상적 평균량',-4.3,23,MUTED))
                self.play(FadeIn(self.stage),run_time=.4)
                self.play(Indicate(bars[1][0],color=ACCENT),run_time=.6)
            elif i==9:
                self.stage=VGroup(self.label('X도 새로 보내야 한다면?',4,33,ACCENT),
                    self.label(f'X열   {SIDE[:8]}…',2.5,28,ACCENT),self.label('X: 16 bits',1.3,35,ACCENT),
                    self.label(f'남은 Y열   {RESIDUAL[:8]}…',-.15,28,WEIGHT),self.label('Y|X: 16 bits',-1.35,35,WEIGHT),
                    self.label('총 16 + 16 = 32 bits',-2.8,35),self.label('이미 알려진 X만 생략할 수 있다',-4.2,25,MUTED))
                self.play(FadeIn(self.stage[:3]),run_time=.4)
                self.play(FadeIn(self.stage[3:]),run_time=.5)
            elif i==10:
                self.stage=VGroup(self.label('I(X;Y) = H(Y) − H(Y|X)',3.7,34,ACCENT),
                    self.label('X를 알아서 Y에서 아낀',1.6,33,GOOD),self.label('평균 비트 수',.1,46,GOOD),
                    self.label('여러 X값에 대한 평균',-2,28,MUTED),self.label('특정 관측 뒤에는 더 불확실할 수도 있음',-3.5,25,MUTED))
                self.play(FadeIn(self.stage),run_time=.4)
            else:
                self.stage=VGroup(self.label('새 관측·외부 정보 없이',4.15,30,MUTED),
                    self.label('X  →  Y  →  Z',2.2,44,WEIGHT),self.label('원본        가공        가공',.95,25,MUTED),
                    self.label('원본에 대한 정보를',-1.5,33,ACCENT),self.label('더 만들어낼 수 있을까?',-3,35,ACCENT))
                self.play(FadeIn(self.stage),run_time=.4)
            self.to(end)
