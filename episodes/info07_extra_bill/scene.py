"""Same recoverable message, two probability tables and binary payloads."""
import sys
from pathlib import Path
from manim import *
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from episodes.prune_series.visuals import txt,MUTED,WEIGHT,PRUNE,GOOD,ACCENT
from episodes.info07_extra_bill.content import *

class ExtraPredictionBill(Scene):
    DURATION=DURATION

    def lines(self,*rows):
        return VGroup(*(txt(text,size,color).move_to([0,y,0]) for text,size,color,y in rows))

    def payloads(self):
        group=VGroup(txt('같은 원본  /  A 750개 + B 250개',29).move_to(UP*4.4))
        for name,bits,color,y in [('P',BITS_P,GOOD,2.7),('Q',BITS_Q,PRUNE,-.5)]:
            label=txt(f'{name}로 인코딩   {len(bits)} bits',36,color).move_to([0,y,0])
            stream=txt(bits[:24]+'…',23,color).move_to([0,y-.9,0])
            bar=Rectangle(width=len(bits)*.0068,height=.45,stroke_width=0,fill_color=color,fill_opacity=.85)
            bar.move_to([-3.4+bar.width/2,y-1.65,0])
            group.add(label,stream,bar)
        group.add(txt('모형·기호 수 공유 / 헤더 제외 / 산술 부호화',22,MUTED).move_to(DOWN*4.3))
        return group

    def construct(self):
        self.add(txt('INFORMATION THEORY  /  07',20,MUTED).move_to(UP*7.25),
                 txt('같은 데이터, 187비트 차이',35).move_to(UP*6.4),
                 Line([-3.8,5.8,0],[3.8,5.8,0],color=MUTED,stroke_opacity=.3))
        captions=['같은 1000개를 보냈다','실제 확률 P / 모델의 가정 Q','같은 데이터열 + 다른 확률표','813 bits vs 1000 bits / 원본 복원 확인','같은 원본, 달라진 표현','실제 187 bits / 이상적 약 188.7 bits','KL = 기호당 평균 추가 비트','B는 짧아도, 자주 나오는 A가 길어진다','데이터가 나오는 쪽이 평균의 기준','Q=P → 추가분 0','다음: 정보를 주면 얼마나 덜 보낼까?']
        old=VGroup(); cap=VGroup()
        for i,(start,end,_,__) in enumerate(CUES):
            if i: self.play(FadeOut(old),FadeOut(cap),run_time=.2)
            cap=txt(captions[i],26).move_to(DOWN*5.9)
            self.play(FadeIn(cap),run_time=.2)
            if i in (0,3):
                old=self.payloads()
                if i==0: old.add(txt('+187 bits',43,ACCENT).move_to(DOWN*3.35))
                else: old.add(txt('P 복원 = Q 복원 = 같은 원본 ✓',27,GOOD).move_to(DOWN*3.35))
            elif i==1:
                old=self.lines(('실제 P',35,GOOD,4),('A 75%   /   B 25%',36,GOOD,2.9),('모델 Q의 가정',35,PRUNE,.5),('A 50%   /   B 50%',36,PRUNE,-.6),('확률표는 믿음·가정을 수치로 표현',25,MUTED,-3.5))
                for ratio,color,y in [(.75,GOOD,1.65),(.5,PRUNE,-1.85)]:
                    a=Rectangle(width=6.8*ratio,height=.5,fill_color=color,fill_opacity=.8,stroke_width=0).move_to([-3.4+3.4*ratio,y,0])
                    b=Rectangle(width=6.8*(1-ratio),height=.5,fill_color=WEIGHT,fill_opacity=.8,stroke_width=0).next_to(a,RIGHT,buff=0)
                    old.add(a,b)
            elif i==2:
                old=self.lines(('A  A  B  A  A  A  B  A …',35,WEIGHT,4),('1000개의 동일한 원본',36,ACCENT,2.4),('A × 750       B × 250',34,WEIGHT,.9),('↙                      ↘',50,MUTED,-.4),('P로 묶어 표현       Q로 묶어 표현',29,GOOD,-1.8),('단일 기호 코드 대신, 데이터열 전체를 부호화',24,MUTED,-3.7))
            elif i==4:
                old=self.lines(('원본',30,MUTED,4),('A  A  B  A  A  A  B  A …',34,WEIGHT,2.8),('P → 813 bits',40,GOOD,.9),('Q → 1000 bits',40,PRUNE,-.6),('데이터는 그대로',36,ACCENT,-2.5),('확률표가 표현의 길이를 바꾼다',29,ACCENT,-3.7))
            elif i==5:
                old=self.lines(('1000개 / 같은 데이터열',30,MUTED,4.2),('실제 본문: 813 → 1000 bits',33,GOOD,2.7),('차이 187 bits',36,GOOD,1.4),('이상적 길이: 811.278 → 1000',30,ACCENT,-.5),('차이 ≈ 188.7 bits',36,ACCENT,-1.8),('유한 코드의 마무리 비트로 차이가 생김',24,MUTED,-3.5))
            elif i==6:
                old=self.lines(('Cross Entropy   H(P,Q) = 1',30,PRUNE,4),('Entropy   H(P) ≈ 0.811',30,GOOD,2.6),('1 − 0.811 ≈ 0.189',39,ACCENT,.9),('KL DIVERGENCE',41,ACCENT,-.6),('D_KL(P‖Q) = H(P,Q) − H(P)',30,ACCENT,-2.2),('bits/기호  /  실제 P의 빈도로 평균',24,MUTED,-3.6))
            elif i==7:
                old=self.lines(('기호당 이상적 길이  P → Q',29,MUTED,4.2),('A: 0.415 → 1 bit',35,PRUNE,2.8),('750회 × (+0.585) ≈ +438.7',29,PRUNE,1.6),('B: 2 → 1 bit',35,GOOD,-.1),('250회 × (−1) = −250',29,GOOD,-1.3),('합계 ≈ +188.7 bits',36,ACCENT,-2.8),('사건별 차이는 음수 가능 / KL ≥ 0',23,MUTED,-4))
            elif i==8:
                old=self.lines(('P에서 뽑고 Q로 표현',31,GOOD,4),('75:25로 평균 → 0.189',35,GOOD,2.5),('Q에서 뽑고 P로 표현',31,PRUNE,.4),('50:50으로 평균 → 0.208',35,PRUNE,-1.1),('이 예시: D_KL(P‖Q) ≠ D_KL(Q‖P)',28,ACCENT,-3),('단위: bits/기호',23,MUTED,-4.1))
            elif i==9:
                old=self.lines(('Q = P',49,GOOD,3.5),('추가분  0',44,ACCENT,1.5),('원래 정보량  ≈ 0.811 bits/기호',30,GOOD,-.6),('모델을 맞추면, 더 쓰던 비트가 사라진다',28,ACCENT,-2.8),('고정 P에서 CE 감소 = KL 감소',24,MUTED,-4))
            else:
                old=self.lines(('다른 변수 X를 알려준다면?',34,WEIGHT,3.7),('X  →  Y',52,ACCENT,1.6),('Y를 보내는 데 필요한 비트는',31,GOOD,-.8),('얼마나 줄어들까?',39,GOOD,-2.4))
            if i in (0,3):
                self.play(FadeIn(old[0]),FadeIn(old[7]),run_time=.3)
                for label,stream,bar in [(old[1],old[2],old[3]),(old[4],old[5],old[6])]:
                    self.play(FadeIn(label),AddTextLetterByLetter(stream),GrowFromEdge(bar,LEFT),run_time=.6)
                self.play(FadeIn(old[8]),run_time=.3)
            elif i==7:
                self.play(FadeIn(old[0]),FadeIn(VGroup(*old[1:3])),run_time=.5)
                self.play(FadeIn(VGroup(*old[3:5])),run_time=.5)
                self.play(FadeIn(VGroup(*old[5:])),run_time=.4)
            else:
                self.play(FadeIn(old,shift=UP*.1),run_time=.4)
            remaining=end-self.time
            if remaining < -1/30: raise RuntimeError(f'Cue {i} overrun {remaining}')
            if remaining>0: self.wait(remaining)
