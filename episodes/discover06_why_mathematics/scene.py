"""Answers can become a starting point for understanding."""
import json
from pathlib import Path
import numpy as np
from manim import *
from episodes.discover02_extra_analytic_continuation.scene import AnalyticContinuationDiscovery
from episodes.discover02_euler_product.scene import math, ORANGE
from episodes.prune_series.visuals import txt, INK, MUTED, WEIGHT, GOOD, SPARSE


class WhyMathematicsDiscovery(AnalyticContinuationDiscovery):
    def construct(self):
        self.cap=VGroup();self.cues=[]
        self.chrome=VGroup(txt('수학적 발견  /  06',22,MUTED).move_to(UP*7.25),
            txt('AI가 답을 찾아주는 시대',36).move_to(UP*6.5),
            txt('우리는 왜 수학을 할까?',37,GOOD).move_to(UP*5.8))
        self.add(self.chrome)
        self.subtitle('「AI가 수학 문제를 해결했다」','무엇이 해결됐는지, 그리고 무엇이 새로웠는지')
        headline=self.card('성과를 알리는 소식',txt('새로운 결과가 나왔습니다',35,GOOD),GOOD).move_to(UP*2.4)
        self.play(FadeIn(headline),run_time=.8)
        self.play(FadeIn(txt('기존 방법과 무엇이 달랐을까요?',34).move_to(DOWN*.1)),run_time=.7)
        self.play(FadeIn(txt('더 넓은 탐색? 더 나은 방법? 새로운 관점?',28,SPARSE).move_to(DOWN*2)),run_time=.7)
        self.play(FadeIn(txt('도입 문구는 개념적 예시 · 특정 난제의 완전 해결 주장 아님',20,MUTED).move_to(DOWN*4)),run_time=.5)
        self.transition(8)

        self.subtitle('발견의 형태에 따라, 새롭게 알게 되는 것도 다릅니다','우열이나 단계가 아닙니다 · 한 발견에 함께 나타날 수도 있습니다')
        kinds=[('방법의 최적화','더 효율적인 알고리즘 · 개선된 경계',WEIGHT),
               ('반례 또는 새로운 구성','추측의 반박 · 새로운 존재 결과',ORANGE),
               ('새로운 증명 방법','명제가 성립하는 새로운 설명',GOOD),
               ('새로운 수학적 관점','여러 현상을 연결하는 구조와 원리',SPARSE)]
        tiles=VGroup()
        for i,(label,detail,color) in enumerate(kinds):
            y=3.7-i*2.05
            tile=VGroup(RoundedRectangle(width=7.4,height=1.65,corner_radius=.16,color=color),
                        txt(label,29,color).move_to(UP*.3),txt(detail,23,MUTED).move_to(DOWN*.35)).move_to([0,y,0])
            self.play(FadeIn(tile,shift=UP*.1),run_time=.7);tiles.add(tile)
        self.transition(19)

        self.subtitle('더 많은 문제가 풀리는 시대, 우리는 무엇을 알고 싶을까요?','답을 얻는 것에서, 발견의 의미를 묻는 것으로')
        self.play(Write(txt('무엇을 해결했는가?',37,WEIGHT).move_to(UP*2.6)),run_time=.9)
        self.play(Write(txt('무엇이 달라졌는가?',39,GOOD).move_to(UP*.5)),run_time=.9)
        self.play(FadeIn(txt('지금까지의 발견을 돌아봅니다',28,MUTED).move_to(DOWN*2.4)),run_time=.6)
        self.transition(25)

        self.subtitle('정답을 넘어, 대상을 바라보는 방법이 달라졌습니다','개별에서 전체로 · 다른 표현 사이의 연결 · 표현의 한계 너머로')
        rows=[(r'\pi(x)','불규칙한 위치 → 전체 개수의 질서',WEIGHT),
              (r'\sum n^{-s}=\prod_p(1-p^{-s})^{-1}','자연수의 가중합 ↔ 소수들의 곱',GOOD),
              (r'\zeta(s)=\frac{\eta(s)}{1-2^{1-s}}','새 표현 → 다룰 수 있는 영역의 확장',SPARSE)]
        for i,(formula,label,color) in enumerate(rows):
            y=3.5-i*2.7
            group=VGroup(math(formula,38,color),txt(label,26,color)).arrange(DOWN,buff=.35).move_to([0,y,0])
            self.play(FadeIn(group),run_time=.8)
            if i==1:self.play(FadeIn(txt('합과 곱의 등식: Re(s) > 1',20,MUTED).move_to([0,y-1,0])),run_time=.4)
        self.play(FadeIn(txt('에타 몫: 실수 s > 0, s ≠ 1 · 복소수 분모 영점은 별도 처리',19,MUTED).move_to(DOWN*4.4)),run_time=.4)
        self.transition(37)

        self.subtitle('그 발견들이 남긴 것은 계산 결과만이 아니었습니다','이전에는 보이지 않던 관계와 구조가 드러났습니다')
        positions=[[-2.6,3,0],[2.6,3,0],[-2.6,-.2,0],[2.6,-.2,0]]
        nodes=VGroup(*[self.node(t,pos,WEIGHT) for t,pos in zip(['개별 소수','전체 분포','자연수의 가중합','소수의 곱'],positions)])
        self.play(FadeIn(nodes),run_time=.7)
        center=self.node('관계와 구조',[0,1.4,0],GOOD)
        links=VGroup(*[Line(pos,[0,1.4,0],color=GOOD,stroke_width=2).set_z_index(-1) for pos in positions])
        self.play(Create(links),FadeIn(center),run_time=1.4)
        self.play(FadeIn(txt('같은 대상을 다르게 볼 수 있게 되는 경험',29,GOOD).move_to(DOWN*3.4)),run_time=.5)
        self.transition(45)

        self.subtitle('AI도 구조와 새로운 관점의 발견에 기여할 수 있습니다','발견된 답이 우리에게 어떤 의미인지 묻는 일도 이어집니다')
        shared=self.node('수학적 탐구',[0,1.4,0],GOOD)
        ai=self.node('AI',[-2.4,3.8,0],WEIGHT);human=self.node('우리',[2.4,3.8,0],SPARSE)
        self.play(FadeIn(ai),FadeIn(human),FadeIn(shared),run_time=.7)
        self.play(GrowArrow(Arrow(ai.get_bottom(),shared.get_top(),color=WEIGHT,buff=.15)),
                  GrowArrow(Arrow(human.get_bottom(),shared.get_top(),color=SPARSE,buff=.15)),run_time=1)
        self.play(FadeIn(txt('답을 발견하기 ↔ 의미를 이해하기',32).move_to(DOWN*.8)),run_time=.6)
        self.play(FadeIn(txt('계산과 탐색, 증명도 새로운 이해를 열 수 있습니다',25,MUTED).move_to(DOWN*2.5)),run_time=.6)
        self.transition(54)

        self.subtitle('발견의 의미를 묻는 질문도 달라집니다','결과에서 멈추지 않고, 무엇을 배울 수 있는지 묻습니다')
        pairs=[('더 좋은 알고리즘','기존 방법과 무엇이 달랐을까?',WEIGHT),
               ('새로운 반례','우리는 무엇을 잘못 가정했을까?',ORANGE),
               ('새로운 증명','어떤 관계가 새롭게 드러났을까?',GOOD)]
        for i,(result,question,color) in enumerate(pairs):
            y=3.5-i*2.8
            group=VGroup(txt(result,29,color),txt(question,29)).arrange(DOWN,buff=.45).move_to([0,y,0])
            self.play(FadeIn(group),run_time=.8)
        self.transition(65)

        self.subtitle('하나의 답은 탐구의 끝이 아니라, 새로운 출발점입니다','더 많은 답은 더 넓은 질문을 열 수 있습니다')
        root=self.node('하나의 답',[0,2.8,0],GOOD)
        questions=[self.node(t,pos,SPARSE) for t,pos in [('왜 그런가?',[-2.4,.3,0]),('어디까지?', [2.4,.3,0]),('무엇과 연결될까?',[0,-2.4,0])]]
        self.play(FadeIn(root),run_time=.5)
        for node in questions:self.play(GrowArrow(Arrow(root.get_center(),node.get_center(),buff=.8,color=SPARSE).set_z_index(-1)),FadeIn(node),run_time=.8)
        self.transition(75)

        self.subtitle('AI가 수학을 얼마나 잘하는가와','우리가 왜 이해하고 싶은가는 서로 다른 질문입니다')
        self.play(FadeIn(txt('능력에 관한 질문',31,WEIGHT).move_to(UP*3.2)),
                  FadeIn(txt('AI는 무엇을 할 수 있을까?',32).move_to(UP*2.2)),run_time=.7)
        self.play(FadeIn(txt('이해의 가치에 관한 질문',31,SPARSE).move_to(DOWN*.1)),
                  FadeIn(txt('우리는 무엇을 알고 싶을까?',32).move_to(DOWN*1.1)),run_time=.7)
        self.transition(79)

        self.subtitle('정답을 찾는 것, 그리고 이전에는 보이지 않던 것을 이해하는 것','어쩌면 우리가 수학을 계속하는 이유는 여기에 있을지도 모릅니다')
        objects=VGroup(VGroup(math(r'\pi(x)',43,WEIGHT),txt('소수의 분포',22,MUTED)).arrange(DOWN,buff=.25),
                       VGroup(math(r'\zeta(s)',43,GOOD),txt('함수와 표현',22,MUTED)).arrange(DOWN,buff=.25),
                       VGroup(math(r'\rho=\tfrac12+it',35,SPARSE),txt('임계선 위의 영점',20,MUTED)).arrange(DOWN,buff=.25)).arrange(RIGHT,buff=.65).move_to(UP*3)
        if objects.width>7.7:objects.scale_to_fit_width(7.7)
        self.play(LaggedStart(*[FadeIn(m) for m in objects],lag_ratio=.3),run_time=1.5)
        self.play(FadeIn(txt('모든 비자명 영점이 임계선 위에 있다는 주장은 미해결',20,MUTED).move_to(UP*1.65)),run_time=.5)
        self.play(Write(txt('무엇을 해결했는가?',37,WEIGHT).move_to(DOWN*.2)),run_time=.9)
        self.play(Write(txt('무엇을 새롭게 이해했는가?',36,GOOD).move_to(DOWN*2.1)),run_time=.9)
        self.play(FadeIn(txt('정답을 찾는 것과 이해하는 것',29,SPARSE).move_to(DOWN*4)),run_time=.6)
        self.to(89);self.write_captions()

    def card(self,label,content,color):
        box=RoundedRectangle(width=7.2,height=2.5,corner_radius=.2,color=color,fill_opacity=.035)
        content.move_to(DOWN*.3)
        return VGroup(box,txt(label,25,color).move_to(UP*.75),content)

    def node(self,label,pos,color):
        text=txt(label,27,color,3)
        box=RoundedRectangle(width=max(text.width+.45,1.4),height=1.1,corner_radius=.18,color=color,fill_color='#091119',fill_opacity=1)
        return VGroup(box,text).move_to(pos)

    def write_captions(self):
        self.cues[-1]['end']=self.time
        def stamp(t):
            ms=round(t*1000); h,ms=divmod(ms,3600000); m,ms=divmod(ms,60000); s,ms=divmod(ms,1000)
            return f'{h:02}:{m:02}:{s:02},{ms:03}'
        out='\n\n'.join(f"{i}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}" for i,c in enumerate(self.cues,1))+'\n'
        Path(__file__).with_name('screen_captions.srt').write_text(out,encoding='utf-8')
        Path(__file__).with_name('screen_timing.json').write_text(json.dumps(self.cues,ensure_ascii=False,indent=2),encoding='utf-8')
