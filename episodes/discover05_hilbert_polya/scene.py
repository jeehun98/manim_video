"""From checking examples to a structure that would force the critical line."""
import json
import sys
from pathlib import Path
import numpy as np
from manim import *
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from episodes.discover03_prime_waves.scene import PrimeWavesDiscovery
from episodes.discover03_prime_waves.data import GAMMAS
from episodes.discover02_euler_product.scene import math,ORANGE,RED
from episodes.prune_series.visuals import txt,INK,MUTED,WEIGHT,GOOD,SPARSE


class HilbertPolyaDiscovery(PrimeWavesDiscovery):
    def construct(self):
        self.cap=VGroup();self.cues=[]
        self.chrome=VGroup(txt('수학적 발견  /  05',22,MUTED).move_to(UP*7.25),
            txt('리만 가설을 양자역학으로',34).move_to(UP*6.5),
            txt('증명할 수 있을까?',39).move_to(UP*5.8))
        self.add(self.chrome)
        self.subtitle('수많은 점이 하나의 직선 위에 나타납니다','리만 가설: 모든 비자명 영점의 실수부가 1/2인가?')
        plane=Axes(x_range=[0,1,1],y_range=[0,110,20],x_length=3.2,y_length=5.1,
                   tips=False,axis_config={'color':MUTED}).move_to([-.5,.9,0])
        critical=DashedLine(plane.c2p(.5,0),plane.c2p(.5,110),color=ORANGE)
        dots=VGroup(*[Dot(plane.c2p(.5,g),radius=.045,color=ORANGE) for g in GAMMAS])
        labels=VGroup(txt('Im(s)',21,MUTED).next_to(plane.c2p(0,110),UP,buff=.12),
                      txt('Re(s)',21,MUTED).next_to(plane.c2p(1,0),RIGHT,buff=.12),
                      math(r'\frac12',30,ORANGE).next_to(plane.c2p(.5,0),DOWN,buff=.15),
                      txt('⋮',34,MUTED).next_to(plane.c2p(.5,110),UP,buff=.12))
        self.play(Create(plane),Create(critical),FadeIn(labels),run_time=1)
        self.play(LaggedStart(*[FadeIn(m) for m in dots],lag_ratio=.07),run_time=2)
        self.play(FadeIn(txt('알려진 영점 일부 · 점검할 범위는 계속 남습니다',23,MUTED).move_to(DOWN*3)),run_time=.5)
        question=VGroup(txt('?',44,RED),txt('예외가 없다는 증명은?',23,MUTED)).arrange(DOWN,buff=.2).move_to([2.25,2.1,0])
        self.play(FadeIn(question),run_time=.6)
        self.play(FadeIn(txt('물음표는 가상의 가능성 · 실제 영점이 아닙니다',21,MUTED).move_to(DOWN*4.2)),run_time=.5)
        self.to(7)
        self.subtitle('확인한 점이 아무리 많아도, 무한 전체는 남습니다','유한한 사례의 확인과 모든 경우의 증명은 다릅니다')
        self.transition(14)

        self.subtitle('점의 위치 대신, 위치를 결정하는 규칙을 찾는다면?','하나씩 확인하기 → 전체를 제한하는 구조 찾기')
        observed=self.panel('하나씩 확인',[-2.05,1,0],WEIGHT)
        structure=self.panel('규칙을 찾기',[2.05,1,0],GOOD)
        checks=VGroup(*[VGroup(Dot([-2.6,2-j*.75,0],color=ORANGE),txt('확인',25,WEIGHT).move_to([-1.8,2-j*.75,0])) for j in range(4)])
        h=self.device([2.05,1.2,0],GOOD)
        self.play(FadeIn(observed),FadeIn(structure),run_time=.6)
        self.play(LaggedStart(*[FadeIn(m) for m in checks],lag_ratio=.2),FadeIn(h),run_time=1.5)
        self.play(FadeIn(txt('계속 확인해도 …',24,MUTED).move_to([-2.05,-1.4,0])),
                  FadeIn(txt('가능한 값을 제한할 수 있을까?',23,GOOD,3.15).move_to([2.05,-1.4,0])),run_time=.5)
        self.to(21)
        self.subtitle('양자역학에서 에너지를 설명하는 도구, 연산자','결과의 위치를 제한하는 수학적 구조를 찾습니다')
        self.play(FadeIn(txt('양자역학에서 에너지를 설명하는 수학적 도구: 연산자',25,INK).move_to(DOWN*3.9)),run_time=.5)
        self.transition(25)

        self.subtitle('자기수반이면, 고유값은 반드시 실수입니다','개별 계산이 아니라 구조가 보장하는, 증명된 성질')
        badge=self.badge('자기수반 조건',GOOD).move_to(UP*4)
        h=self.device([-1.2,2.2,0],GOOD)
        inp=Arrow([-3.9,2.2,0],[-2.3,2.2,0],color=MUTED,buff=.1)
        out=Arrow([-.2,2.2,0],[1.4,2.2,0],color=GOOD,buff=.1)
        io=VGroup(txt('입력 벡터',23,MUTED).move_to([-3.1,2.9,0]),txt('고유값',28,GOOD).move_to([2.4,2.2,0]))
        self.play(FadeIn(badge),FadeIn(h),GrowArrow(inp),GrowArrow(out),FadeIn(io),run_time=1)
        axis=Line([-3.2,-.6,0],[3.2,-.6,0],color=MUTED)
        values=(-3,-1,1,3)
        realdots=VGroup(*[Dot([e*.8,-.6,0],color=GOOD,radius=.08) for e in values])
        nums=VGroup(*[txt(str(e),24,GOOD).move_to([e*.8,-1.1,0]) for e in values])
        self.play(Create(axis),LaggedStart(*[FadeIn(m) for m in realdots],lag_ratio=.2),FadeIn(nums),run_time=1.2)
        self.play(FadeIn(txt('허용되는 고유값은 실수축 위에',29,GOOD).move_to(DOWN*2.4)),run_time=.5)
        self.to(29)
        self.subtitle('하나하나 확인하는 대신, 구조 자체가 보장합니다','자기수반이면 고유값이 실수라는 것은 증명된 성질입니다')
        self.play(FadeIn(txt('H → 고유값은 개념도 · 값은 설명용 예시',22,MUTED).move_to(DOWN*3.65)),run_time=.5)
        self.play(FadeIn(txt('연산자는 벡터에 작용하며, 고유값은 그 작용의 성질입니다',21,MUTED).move_to(DOWN*4.4)),run_time=.5)
        self.transition(37)

        self.subtitle('실수값을 세로 방향의 높이로 옮겨봅니다','그리고 가로 위치를 1/2로 고정합니다')
        plane=Axes(x_range=[-4,4,1],y_range=[-4,4,1],x_length=6.4,y_length=6.4,
                   tips=False,axis_config={'color':MUTED}).move_to(UP*.4)
        track=Line(plane.c2p(-4,0),plane.c2p(4,0),color=GOOD,stroke_width=4)
        dots=VGroup(*[Dot(plane.c2p(e,0),color=GOOD,radius=.08) for e in values])
        spectrum=VGroup(track,dots)
        labels=VGroup(txt('실수 방향',23,MUTED).next_to(plane.c2p(4,0),DOWN,buff=.12),
                      txt('허수 방향',23,MUTED).next_to(plane.c2p(0,4),UP,buff=.12),
                      txt('0',22,MUTED).next_to(plane.c2p(0,0),DOWN+LEFT,buff=.22))
        self.play(Create(plane),FadeIn(labels),FadeIn(spectrum),run_time=.8)
        self.play(Rotate(spectrum,PI/2,about_point=plane.c2p(0,0)),run_time=1.8)
        self.to(40)
        self.subtitle('가로 위치를 1/2로 고정합니다','모든 예시 점이 하나의 직선 위에 놓입니다')
        self.play(spectrum.animate.shift(plane.c2p(.5,0)-plane.c2p(0,0)),run_time=1.6)
        half=math(r'\frac12',30,GOOD).next_to(plane.c2p(.5,-4),DOWN,buff=.15)
        formula=math(r'\rho=\frac12+iE,\qquad E\in\mathbb R',43,GOOD).move_to(UP*4.65)
        self.play(FadeIn(half),FadeIn(formula),run_time=.6)
        self.play(FadeIn(txt('좌표 변환 개념도 · 설명용 값이며 실제 영점이 아닙니다',22,MUTED).move_to(DOWN*4.4)),run_time=.5)
        self.to(46)
        self.subtitle('좌표 변환만으로 리만 가설이 증명되지는 않습니다','영점 전체와의 정확한 대응이 추가로 필요합니다')
        self.transition(50)

        self.subtitle('가장 중요한 조건: 모든 영점과 빠짐없이 대응해야 합니다','리만 가설을 미리 가정하지 않은 대응의 증명이 필요합니다')
        left=self.panel('모든 비자명 영점',[-2.05,1,0],ORANGE)
        right=self.panel('자기수반 H의 고유값',[2.05,1,0],GOOD)
        self.play(FadeIn(left),FadeIn(right),run_time=.7)
        for j in range(3):
            y=2-j*1.05
            r=math(rf'\rho_{{{j+1}}}',37,ORANGE).move_to([-2.05,y,0])
            e=math(rf'E_{{{j+1}}}',37,GOOD).move_to([2.05,y,0])
            bridge=DashedLine([-1.35,y,0],[1.35,y,0],color=MUTED,stroke_width=2)
            q=txt('?',27,RED).move_to([0,y,0])
            self.play(FadeIn(r),FadeIn(e),Create(bridge),FadeIn(q),run_time=.5)
        self.play(FadeIn(txt('⋮',31,MUTED).move_to([-2.05,-1.3,0])),FadeIn(txt('⋮',31,MUTED).move_to([2.05,-1.3,0])),run_time=.4)
        note=VGroup(txt('영점 전체를 설명하는 연산자를 찾고',27,INK),
                    txt('그 연산자의 자기수반성까지 증명한다면',27,INK),
                    txt('리만 가설을 증명할 수 있습니다',28,GOOD)).arrange(DOWN,buff=.22).move_to(DOWN*3.5)
        self.to(57)
        self.subtitle('임계선 위 영점 일부의 높이만 재현해서는 부족합니다','리만 가설을 미리 가정하지 않고 영점 전체의 대응을 증명해야 합니다')
        self.to(65)
        self.play(FadeIn(note),run_time=.6)
        self.subtitle('이것이 힐베르트–푈리야 접근입니다','개별 위치의 확인을, 구조와 대응의 증명 문제로 바꿉니다')
        self.play(FadeIn(txt('Hilbert–Pólya',34,INK).move_to(UP*4.6)),run_time=.6)
        self.transition(76)

        self.subtitle('실제로 여러 연산자 후보가 연구되고 있습니다','필요한 구조를 찾기 위한 연구 방향입니다')
        self.play(FadeIn(txt('후보들은 연구되고 있습니다',30,INK).move_to(UP*3.8)),run_time=.5)
        first=self.condition_card('자기수반성', '적절한 공간과 정의역에서 증명',GOOD).move_to(UP*1.8)
        second=self.condition_card('모든 비자명 영점과 정확한 대응','임계선 밖의 가능성까지 빠짐없이 다루기',ORANGE).move_to(DOWN*.7)
        self.play(FadeIn(first),FadeIn(second),run_time=1)
        self.to(79)
        self.subtitle('두 조건을 함께 확립하는 단계는 아직 미해결입니다','자기수반성과 영점 전체의 정확한 대응이 모두 필요합니다')
        self.play(FadeIn(txt('두 조건을 함께 확립하는 단계는 미해결',29,RED).move_to(DOWN*3.5)),run_time=.5)
        self.play(FadeIn(txt('통계가 닮았다는 관찰만으로 이 대응이 증명되지는 않습니다',21,MUTED).move_to(DOWN*4.5)),run_time=.5)
        self.transition(86)

        self.subtitle('답을 더 많이 확인하는 것과, 이유를 찾는 것','무한히 많은 경우를 하나의 구조로 다루려는 발상')
        a=self.panel('개별 확인',[-2.05,1,0],WEIGHT)
        b=self.panel('구조의 증명',[2.05,1,0],GOOD)
        self.play(FadeIn(a),FadeIn(b),run_time=.6)
        checks=VGroup(*[txt('확인',25,WEIGHT).move_to([-2.05,2.1-j*.8,0]) for j in range(3)],
                      txt('⋮',33,MUTED).move_to([-2.05,-.9,0]))
        h=self.device([2.05,1.7,0],GOOD)
        axis=Line([.9,-.6,0],[3.2,-.6,0],color=GOOD)
        dots=VGroup(*[Dot([x,-.6,0],color=GOOD,radius=.055) for x in (1.1,1.5,2.15,2.8,3.05)])
        self.play(LaggedStart(*[FadeIn(m) for m in checks],lag_ratio=.2),FadeIn(h),Create(axis),FadeIn(dots),run_time=1.5)
        self.play(FadeIn(txt('아직 확인하지 못한 경우',22,MUTED,3.15).move_to([-2.05,-1.35,0])),
                  FadeIn(txt('모든 경우를 제한하는 원리',22,GOOD,3.15).move_to([2.05,-1.35,0])),run_time=.5)
        self.play(FadeIn(txt('오른쪽은 접근이 성공했을 때의 목표 · 아직 증명되지 않음',21,MUTED).move_to(DOWN*3.7)),run_time=.5)
        self.to(90)
        self.subtitle('그 점들이 다른 위치에 존재할 수 없는 이유를 찾는 것입니다','하나의 수학적 구조가 무한한 경우를 설명할 수 있다면')
        self.to(96)
        self.subtitle('수학적 이해는 때로 더 많은 답을 확인하는 것이 아니라','그 답들을 하나의 구조로 설명하는 데서 시작됩니다')
        self.to(102)
        self.write_captions()

    def panel(self,title,position,color):
        box=RoundedRectangle(width=3.6,height=5.5,corner_radius=.16,color=color,
                             fill_color=color,fill_opacity=.045).move_to(position)
        heading=txt(title,25,color,3.15).move_to(box.get_top()+DOWN*.45)
        return VGroup(box,heading)

    def device(self,position,color):
        box=RoundedRectangle(width=1.7,height=1.5,corner_radius=.15,color=color,
                             fill_color=color,fill_opacity=.13)
        return VGroup(box,math('H',54,color)).move_to(position)

    def badge(self,text,color):
        label=txt(text,28,color)
        return VGroup(SurroundingRectangle(label,color=color,buff=.18,corner_radius=.1),label)

    def condition_card(self,title,detail,color):
        box=RoundedRectangle(width=7,height=1.7,corner_radius=.14,color=color,
                             fill_color=color,fill_opacity=.06)
        words=VGroup(txt(title,29,color),txt(detail,23,MUTED)).arrange(DOWN,buff=.25)
        return VGroup(box,words)

    def write_captions(self):
        self.cues[-1]['end']=self.time
        def stamp(t):
            ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
            return f'{h:02}:{m:02}:{s:02},{ms:03}'
        out='\n\n'.join(f"{i}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}" for i,c in enumerate(self.cues,1))+'\n'
        Path(__file__).with_name('screen_captions.srt').write_text(out,encoding='utf-8')
        timeline=json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))
        narration='\n\n'.join(f"{i}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}" for i,c in enumerate(timeline,1))+'\n'
        Path(__file__).with_name('captions.srt').write_text(narration,encoding='utf-8')
        Path(__file__).with_name('screen_timing.json').write_text(json.dumps(self.cues,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
