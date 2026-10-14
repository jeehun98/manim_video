"""An alternative representation, not an ordinary sum of a divergent series."""
import json
from pathlib import Path
import numpy as np
from scipy.special import zetac
from manim import *
from episodes.discover03_prime_waves.scene import PrimeWavesDiscovery
from episodes.discover02_euler_product.scene import math, ORANGE, RED
from episodes.prune_series.visuals import txt, INK, MUTED, WEIGHT, GOOD, SPARSE


class AnalyticContinuationDiscovery(PrimeWavesDiscovery):
    def construct(self):
        self.cap=VGroup(); self.cues=[]
        self.chrome=VGroup(txt('수학적 발견  /  02 보충편',22,MUTED).move_to(UP*7.25),
            txt('계산이 막히면, 대상도 끝일까?',34).move_to(UP*6.5),
            txt('같은 함수, 새로운 표현',32,GOOD).move_to(UP*5.8))
        self.add(self.chrome)
        self.subtitle('계산할 수 없다면, 대상도 더 이상 다룰 수 없을까요?','제타 함수라는 하나의 대상, 그것을 표현하는 방법')
        formula=math(r'\zeta(s)=1+\frac1{2^s}+\frac1{3^s}+\cdots',45).move_to(UP*3.9)
        self.play(Write(formula),run_time=1.4)
        n=np.arange(1,247)
        convergent=np.cumsum(n.astype(float)**-2)
        positive=np.cumsum(n.astype(float)**-.5)
        alternating=np.cumsum((-1.)**(n-1)*n.astype(float)**-.5)
        eta=(1-np.sqrt(2))*(1+zetac(.5))
        a=Axes(x_range=[0,246,82],y_range=[0,32,8],x_length=6.5,y_length=4.2,tips=False,
               axis_config={'color':MUTED}).move_to(DOWN*.1)
        self.add(txt('0',19,MUTED).next_to(a.c2p(0,0),LEFT),txt('32',19,MUTED).next_to(a.c2p(0,32),LEFT),txt('246',19,MUTED).next_to(a.c2p(246,0),DOWN),txt('N',21,MUTED).next_to(a.c2p(246,0),RIGHT))
        self.play(Create(a),FadeIn(txt('부분합 · 같은 세로축',23,MUTED).move_to(UP*2.5)),run_time=.7)
        self.play(Create(self.polyline(a,n,convergent,GOOD)),run_time=1.2)
        self.play(FadeIn(txt('s = 2  →  약 1.645로 수렴',27,GOOD).move_to(DOWN*3.1)),run_time=.5)
        self.to(8)
        self.subtitle('s = 1/2에서, 처음의 무한합은 발산합니다','함수의 한계일까요? 이 표현의 한계일까요?')
        self.play(Create(self.polyline(a,n,positive,ORANGE)),run_time=4)
        self.play(FadeIn(txt('s = 1/2  ·  N = 246  →  29.940',27,ORANGE).move_to(DOWN*4)),run_time=.5)
        self.transition(15)

        self.subtitle('항의 부호를 바꿔, 새로운 급수를 만들어봅니다','순서를 바꾸는 것이 아니라, 더하고 빼는 부호를 바꿉니다')
        self.play(Write(math(r'\eta(s)=1-\frac1{2^s}+\frac1{3^s}-\frac1{4^s}+\cdots',42,GOOD).move_to(UP*4.2)),run_time=1)
        self.play(FadeIn(txt('s = 1/2',29).move_to(UP*3.25)),run_time=.4)
        b=Axes(x_range=[0,246,82],y_range=[0,1.1,.5],x_length=6.5,y_length=4.5,tips=False,
               axis_config={'color':MUTED}).move_to(DOWN*.1)
        ref=DashedLine(b.c2p(0,eta),b.c2p(246,eta),color=MUTED)
        self.play(Create(b),Create(ref),run_time=.7)
        self.add(txt('0',19,MUTED).next_to(b.c2p(0,0),LEFT),txt('1',19,MUTED).next_to(b.c2p(0,1),LEFT),txt('246',19,MUTED).next_to(b.c2p(246,0),DOWN))
        path=self.polyline(b,n[:2],alternating[:2],GOOD)
        self.add(path)
        # Keep every consecutive integer: sampling even N alone hides the oscillation.
        tracker=ValueTracker(2)
        path.add_updater(lambda m:m.become(self.polyline(b,n[:int(tracker.get_value())],alternating[:int(tracker.get_value())],GOOD)))
        self.play(tracker.animate.set_value(246),run_time=4.5,rate_func=linear)
        path.clear_updaters()
        self.to(23)
        self.subtitle('이번에는 위아래로 흔들리며 한 값에 가까워집니다','교대급수의 극한은 약 0.6049입니다')
        self.play(FadeIn(txt('N = 246: 0.5731  →  극한: 0.6049',27,GOOD).move_to(DOWN*3.1)),
                  FadeIn(txt('가로축: 항의 개수 N · 세로축: 교대 부분합',22,MUTED).move_to(DOWN*4)),run_time=.6)
        self.transition(30)

        self.subtitle('하지만 부호를 바꿨다면, 다른 함수 아닌가요?','두 함수가 어떻게 연결되는지 확인해봅니다')
        self.play(Write(math(r'\zeta(s)\quad\overset{?}{\longleftrightarrow}\quad\eta(s)',57).move_to(UP*1.8)),run_time=1.3)
        self.play(FadeIn(txt('연결을 증명할 곳: 원래 급수가 수렴하는 영역',27,GOOD).move_to(DOWN*.1)),
                  FadeIn(math(r'\operatorname{Re}(s)>1',38,GOOD).move_to(DOWN*1.3)),run_time=.7)
        self.transition(34)

        self.subtitle('먼저 수렴하는 영역에서, 짝수 항만 골라냅니다','짝수 항의 합은 원래 합의 2⁻ˢ배입니다')
        badge=txt('이 계산은 Re(s) > 1에서',25,GOOD).move_to(UP*4.6)
        terms=VGroup(*[math('1' if k==1 else rf'\frac1{{{k}^s}}',38,ORANGE if k%2==0 else INK) for k in range(1,7)])
        terms.arrange(RIGHT,buff=.63).move_to(UP*2.9)
        signs=VGroup(*[math('+',27).move_to((terms[k].get_right()+terms[k+1].get_left())/2) for k in range(5)])
        self.play(FadeIn(badge),FadeIn(terms),FadeIn(signs),run_time=.8)
        even=VGroup(*[terms[k].copy() for k in (1,3,5)])
        self.play(even.animate.arrange(RIGHT,buff=1.1).move_to(UP*.8),run_time=.7)
        self.play(FadeIn(VGroup(*[math('+',27,ORANGE).move_to((even[k].get_right()+even[k+1].get_left())/2) for k in range(2)])),run_time=.25)
        self.play(Write(math(r'\sum_{n\ge1}(2n)^{-s}=2^{-s}\zeta(s)',41,ORANGE).move_to(DOWN*.7)),run_time=1)
        self.to(38)
        self.subtitle('이제 짝수 항을 두 번 빼보겠습니다','한 번 빼면 0, 한 번 더 빼면 음수 항이 됩니다')
        self.play(FadeIn(txt('짝수 항을 한 번 빼기',26,ORANGE).move_to(DOWN*2.2)),run_time=.5)
        self.play(*[terms[k].animate.set_opacity(.15) for k in (1,3,5)],run_time=1)
        self.play(FadeIn(txt('두 번째 빼기 → 짝수 항의 부호가 −로',26,GOOD).move_to(DOWN*3.2)),run_time=.5)
        self.play(*[terms[k].animate.set_opacity(1).set_color(GOOD) for k in (1,3,5)],
                  *[Transform(signs[k],math('-' if k%2==0 else '+',27,GOOD).move_to(signs[k])) for k in range(5)],run_time=1.2)
        self.transition(45)

        self.subtitle('교대급수는 원래 함수와 정확히 연결됩니다','짝수 항을 두 번 빼면 이 관계가 나옵니다')
        self.play(FadeIn(txt('Re(s) > 1에서 증명한 관계',25,GOOD).move_to(UP*4.3)),run_time=.5)
        derivation=VGroup(math(r'\eta(s)=\zeta(s)-2\cdot2^{-s}\zeta(s)',43),
            math(r'\eta(s)=(1-2^{1-s})\zeta(s)',45,GOOD),
            math(r'\zeta(s)=\frac{\eta(s)}{1-2^{1-s}}',54,GOOD)).arrange(DOWN,buff=.8).move_to(UP*.5)
        for line in derivation:self.play(Write(line),run_time=1.3)
        self.play(FadeIn(txt('s = 2: 두 표현 모두 π²/6 ≈ 1.644934',26,GOOD).move_to(DOWN*2.7)),run_time=.5)
        self.play(FadeIn(txt('원래 영역에서 일치 → 같은 함수를 이어가는 표현',26,SPARSE).move_to(DOWN*3.7)),run_time=.6)
        self.transition(53)

        self.subtitle('같은 입력, 서로 다른 표현의 한계','s = 1/2에서 원래 급수는 발산하지만, 새 표현은 유한합니다')
        self.play(FadeIn(txt('하나의 대상: 제타 함수',31).move_to(UP*4.5)),run_time=.5)
        panels=VGroup()
        for x,label,color in [(-2,'표현 A · 양수항 급수',ORANGE),(2,'표현 B · 에타 함수의 몫',GOOD)]:
            panels.add(RoundedRectangle(width=3.7,height=5.7,corner_radius=.18,color=color,fill_opacity=.04).move_to([x,.65,0]))
            self.play(FadeIn(txt(label,24,color,3.4).move_to([x,2.9,0])),run_time=.3)
        self.play(FadeIn(panels),run_time=.5)
        self.play(Write(math(r"\sum_{n=1}^{\infty}n^{-1/2}",38,ORANGE,width=3.2).move_to([-2,1.4,0])),
                  Write(math(r"\frac{\eta(1/2)}{1-\sqrt2}",43,GOOD,width=3.2).move_to([2,1.4,0])),run_time=1)
        self.play(FadeIn(txt('1 + 1/√2 + 1/√3 + …',21,ORANGE,3.2).move_to([-2,.2,0])),
                  FadeIn(txt('0.6048986… ÷ (1 − √2)',21,GOOD,3.2).move_to([2,.2,0])),run_time=.6)
        self.play(FadeIn(txt('끝없이 증가 ↑',29,ORANGE,3.2).move_to([-2,-1.1,0])),
                  FadeIn(txt('−1.46035…',34,GOOD,3.2).move_to([2,-1.1,0])),run_time=.8)
        self.to(61)
        self.subtitle('양수들을 모두 더했더니 음수가 됐다는 뜻은 아닙니다','원래 합의 값과 확장된 함수의 값은 구분해야 합니다')
        self.play(FadeIn(txt('같은 함수의 표현이라도, 유효한 영역은 다릅니다',27,SPARSE).move_to(DOWN*3.6)),run_time=.6)
        self.transition(68)

        self.subtitle('같은 대상을 다루는 두 표현, 서로 다른 유효 범위','원래 영역에서 일치하면서 해석적 성질을 유지해 이어갑니다')
        self.play(FadeIn(txt('실수 입력 s에서 비교',25,MUTED).move_to(UP*4.2)),run_time=.5)
        axis=NumberLine(x_range=[0,2.5,.5],length=6.5,include_numbers=True,font_size=25,color=MUTED).move_to(UP*2.5)
        self.play(Create(axis),run_time=.7)
        for y,lo,color,label in [(1,1,ORANGE,'표현 A: s > 1'),(-.8,0,GOOD,'표현 B: s > 0, s ≠ 1')]:
            left=axis.n2p(lo);right=axis.n2p(2.5)
            track=Line([left[0],y,0],[right[0],y,0],color=color,stroke_width=7)
            self.play(Create(track),FadeIn(txt(label,27,color).move_to([0,y+.5,0])),run_time=.8)
            self.add(Circle(radius=.08,color=color,fill_color='#091119',fill_opacity=1).move_to([left[0],y,0]))
        self.add(Circle(radius=.09,color=RED,fill_color='#091119',fill_opacity=1).move_to([axis.n2p(1)[0],-.8,0]))
        self.play(FadeIn(txt('s > 1에서는 두 표현이 정확히 일치',26,SPARSE).move_to(DOWN*2.1)),run_time=.6)
        self.play(FadeIn(txt('해석적 연속',36,GOOD).move_to(DOWN*3.3)),
                  FadeIn(txt('값과 해석적 성질을 유지하는 확장',23,MUTED).move_to(DOWN*4.15)),run_time=.6)
        self.transition(79)

        self.subtitle('한계에 도달한 것은 함수일까요, 표현일까요?','때로는 새로운 답보다, 대상을 바라보는 방법을 바꿔야 합니다')
        conclusion=VGroup(txt('하나의 대상',29,MUTED),math(r"\zeta(s)",64,INK),
            txt('서로 다른 표현',35,GOOD),txt('서로 다른 유효 영역',31,SPARSE)).arrange(DOWN,buff=.65).move_to(UP*1.2)
        self.play(FadeIn(conclusion,shift=UP*.2),run_time=1.2)
        self.play(FadeIn(txt('표현의 한계 ≠ 대상의 한계',36,GOOD).move_to(DOWN*3.3)),run_time=.6)
        self.to(88)
        self.write_captions()

    def write_captions(self):
        self.cues[-1]['end']=self.time
        def stamp(t):
            ms=round(t*1000); h,ms=divmod(ms,3600000); m,ms=divmod(ms,60000); s,ms=divmod(ms,1000)
            return f'{h:02}:{m:02}:{s:02},{ms:03}'
        out='\n\n'.join(f"{i}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}" for i,c in enumerate(self.cues,1))+'\n'
        Path(__file__).with_name('screen_captions.srt').write_text(out,encoding='utf-8')
        Path(__file__).with_name('screen_timing.json').write_text(json.dumps(self.cues,ensure_ascii=False,indent=2),encoding='utf-8')
