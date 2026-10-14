"""Prime-power staircase, actual zeta-zero waves, and the explicit formula."""
import json
import sys
from pathlib import Path
import numpy as np
from manim import *

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from episodes.discover02_euler_product.scene import math, ORANGE, RED
from episodes.prune_series.visuals import txt, INK, MUTED, WEIGHT, GOOD, SPARSE
from episodes.discover03_prime_waves.data import prime_weights, pair_wave, correction, explicit_approx, GAMMAS


class PrimeWavesDiscovery(Scene):
    def construct(self):
        self.chrome=VGroup(txt('수학적 발견  /  03',22,MUTED).move_to(UP*7.25),
            txt('소수의 불규칙성을 설명하는',34).move_to(UP*6.5),
            txt('보이지 않는 파동',40).move_to(UP*5.8))
        self.cap=VGroup();self.cues=[]
        self.primes,self.weights,self.psi=prime_weights()
        self.add(self.chrome)
        self.subtitle('전체적인 규칙, 그 곁에 남는 차이','예상보다 많기도, 적기도 한 소수의 분포')
        a,labels=self.axes([0,100,20],[0,30,10])
        pi=np.cumsum(np.isin(np.arange(121),self.primes))
        step=self.staircase(a,pi)
        smooth_curve=self.curve(a,lambda x:x/np.log(x),2,100,ORANGE)
        self.play(Create(a),FadeIn(labels),Create(step),run_time=1.4)
        self.play(Create(smooth_curve),FadeIn(self.legend('실제 π(x)','근사 x / ln x').move_to(DOWN*3.5)),run_time=1.2)
        self.play(FadeIn(txt('이 차이에도 규칙이 있을까요?',31,GOOD).move_to(UP*4)),run_time=.6)
        self.transition(8)

        self.subtitle('소수를 세는 방식을 조금 바꿉니다','소수와 소수 거듭제곱을 가중해서 더한 계단')
        positions=(2,3,4,5,7,8,9)
        tiles=VGroup(*[VGroup(RoundedRectangle(width=.85,height=.85,corner_radius=.1,color=WEIGHT,
                        fill_color=WEIGHT,fill_opacity=.1),txt(str(n),28,WEIGHT)).move_to([-3.15+j*1.05,3.6,0])
                        for j,n in enumerate(positions)])
        self.play(LaggedStart(*[FadeIn(m) for m in tiles],lag_ratio=.12),run_time=1.2)
        self.play(FadeIn(txt('4 = 2², 8 = 2³, 9 = 3²도 포함',25,MUTED).move_to(UP*2.6)),run_time=.5)
        a,labels=self.axes([0,100,20],[-16,110,20])
        step=self.staircase(a,self.psi)
        trend=Line(a.c2p(0,0),a.c2p(100,100),color=ORANGE,stroke_width=4)
        self.play(Create(a),FadeIn(labels),Create(step),run_time=1.6)
        # A small label identifies the exact function without turning it into a derivation.
        self.play(FadeIn(math(r'\psi(x)',32,WEIGHT).move_to([-2.8,1.8,0])),run_time=.4)
        self.to(16)
        self.play(Create(trend),FadeIn(txt('주황색: 전체 추세 y = x',24,ORANGE).move_to(DOWN*3.5)),run_time=1)
        self.to(19)
        self.subtitle('계단에서 직선을 빼보겠습니다','같은 x, 같은 축척에서 전체 증가분을 제거합니다')
        # Subtract alpha*x point by point; the axes remain fixed during this operation.
        def subtract(m,alpha):
            pts=[a.c2p(0,0)]
            for n in range(1,101):
                pts.extend((a.c2p(n,self.psi[n-1]-alpha*n),a.c2p(n,self.psi[n]-alpha*n)))
            m.set_points_as_corners(pts)
        def lower_trend(m,alpha):
            m.put_start_and_end_on(a.c2p(0,0),a.c2p(100,(1-alpha)*100))
        self.play(UpdateFromAlphaFunc(step,subtract),UpdateFromAlphaFunc(trend,lower_trend),run_time=1.6,rate_func=smooth)
        self.to(21)
        self.subtitle('증가하던 모습이 사라지고, 흔들림만 남습니다','가중 계단의 실제 오차 ψ(x) − x')
        # Once subtraction is complete, expand the vertical scale explicitly.
        old=[m for m in self.mobjects if m is not self.chrome and m is not self.cap]
        ea,el=self.axes([0,100,20],[-16,12,4])
        error=self.staircase(ea,self.psi,subtract_x=True)
        self.play(*[FadeOut(m) for m in old if m is not step],Transform(step,error),Create(ea),FadeIn(el),run_time=1.5)
        self.play(FadeIn(txt('세로축 확대 · x 범위는 그대로',23,MUTED).move_to(DOWN*3.5)),run_time=.5)
        self.to(26)
        self.subtitle('이 복잡한 흔들림을 진동들의 합으로 표현할 수 있습니다','불규칙한 차이 속에서 찾는 또 하나의 구조')
        self.play(FadeIn(txt('복잡한 흔들림 속에, 여러 진동이 숨어 있습니다',27,GOOD).move_to(UP*4)),run_time=.5)
        self.transition(31)

        self.subtitle('하나의 진동을 그려보겠습니다','아직은 단순한 흔들림 하나')
        a,labels=self.axes([0,100,20],[-16,12,4])
        actual=self.staircase(a,self.psi,subtract_x=True)
        x=np.linspace(2,100,2400)
        current=self.polyline(a,x,explicit_approx(x,1)-x,ORANGE)
        counter=txt('진동 1개',31,ORANGE).move_to(UP*4)
        self.play(FadeIn(a),FadeIn(labels),FadeIn(actual),run_time=.35)
        self.play(Create(current),FadeIn(counter),run_time=.8)
        legend=self.legend('실제 가중 계단의 오차','진동의 합').move_to(DOWN*3.5)
        note=VGroup(txt('유한 절단 근사 · 보정항 포함',24,MUTED),
                    txt('모든 점에서 오차가 매번 줄어드는 것은 아닙니다',21,MUTED)).arrange(DOWN,buff=.2).move_to(DOWN*4.4)
        self.play(FadeIn(legend),FadeIn(note),run_time=.3)
        self.to(33)
        self.subtitle('다른 진동을 더하고, 또 더하면','서로 겹치며 처음의 불규칙한 흔들림에 가까워집니다')
        for count,target in ((5,35),(30,37)):
            nxt=self.polyline(a,x,explicit_approx(x,count)-x,ORANGE)
            self.play(Transform(current,nxt),Transform(counter,txt(f'진동 {count}개',31,ORANGE).move_to(counter)),run_time=1.2)
            self.to(target)
        self.subtitle('서로 다른 진동이 겹치면 세부 구조가 드러납니다','보정항을 포함한 유한한 근사입니다')
        self.to(44)
        self.subtitle('그렇다면 이 진동들은 어디서 온 걸까요?','임의의 파동을 골라 계단에 맞춘 것이 아닙니다')
        self.transition(47)

        self.subtitle('바로, 제타 함수의 영점입니다','전혀 다른 세계의 점이 진동항과 연결됩니다')
        reveal=VGroup(txt('제타 함수의 영점',31,ORANGE),math(r'\zeta(s)=0',39,ORANGE)).arrange(DOWN,buff=.25).move_to(UP*4.2)
        plane=Axes(x_range=[0,1,1],y_range=[0,55,10],x_length=2.1,y_length=3.1,
                   tips=False,axis_config={'color':MUTED}).move_to([-2.3,1.75,0])
        zeros=VGroup(*[Dot(plane.c2p(.5,g),color=ORANGE,radius=.06) for g in GAMMAS[:11]])
        plabels=VGroup(txt('Re(s)',19,MUTED).next_to(plane.c2p(1,0),DOWN,buff=.12),
                      txt('Im(s)',19,MUTED).next_to(plane.c2p(0,55),UP,buff=.1))
        wa=Axes(x_range=[np.log(4),np.log(100),1],y_range=[-2,2,1],x_length=3.4,y_length=2.5,
                tips=False,axis_config={'color':MUTED}).move_to([1.7,1.75,0])
        u=np.linspace(np.log(4),np.log(100),1000)
        component=self.polyline(wa,u,pair_wave(np.exp(u),GAMMAS[0]),ORANGE)
        wl=txt('x · 가로축은 로그 눈금',19,MUTED).move_to([1.7,.1,0])
        self.play(FadeIn(reveal),Create(plane),FadeIn(plabels),FadeIn(zeros),run_time=1.2)
        self.to(49)
        self.subtitle('복소평면의 점이 각각의 진동항과 연결됩니다','점 하나를 선택하면, 그 점에서 계산한 진동이 나타납니다')
        selected=SurroundingRectangle(zeros[0],color=GOOD,buff=.09)
        link=Arrow(plane.c2p(.5,GAMMAS[0])+RIGHT*.15,[-.25,1.75,0],color=GOOD,buff=.1,stroke_width=3)
        self.play(Create(selected),GrowArrow(link),Create(wa),FadeIn(wl),run_time=.4)
        self.play(Create(component),run_time=.6)
        self.play(FadeIn(txt('각 점은 켤레 영점과 함께 계산 · 실제 영점표 사용',21,MUTED).move_to(DOWN*.55)),run_time=.2)
        # Bottom: the same exact error, with the first selected pair plus the fixed correction.
        ba=Axes(x_range=[0,100,20],y_range=[-16,12,4],x_length=6.6,y_length=2.6,
                tips=False,axis_config={'color':MUTED}).move_to(DOWN*2.5)
        bottom_actual=self.staircase(ba,self.psi,subtract_x=True)
        bottom_sum=self.polyline(ba,x,explicit_approx(x,1)-x,ORANGE)
        self.play(Create(ba),Create(bottom_actual),Create(bottom_sum),run_time=.6)
        self.play(FadeIn(txt('실제 오차와 영점에서 계산한 합 · 보정항 포함',21,MUTED).move_to(DOWN*4.2)),run_time=.2)
        self.to(52)
        self.subtitle('점의 위치가 바뀌면, 대응하는 진동도 달라집니다','허수부는 로그 눈금의 빠르기, 실수부는 진폭 성장과 연결')
        newselected=SurroundingRectangle(zeros[1],color=GOOD,buff=.09)
        newlink=Arrow(plane.c2p(.5,GAMMAS[1])+RIGHT*.15,[-.25,1.75,0],color=GOOD,buff=.1,stroke_width=3)
        self.play(Transform(selected,newselected),Transform(link,newlink),
                  Transform(component,self.polyline(wa,u,pair_wave(np.exp(u),GAMMAS[1]),ORANGE)),
                  Transform(bottom_sum,self.polyline(ba,x,explicit_approx(x,2)-x,ORANGE)),run_time=1.5)
        self.to(56)
        self.subtitle('점들의 위치가 소수의 흔들림을 설명합니다','제타 함수의 영점 ↔ 가중 계단의 오차')
        self.play(Indicate(zeros,color=GOOD),
                  Transform(bottom_sum,self.polyline(ba,x,explicit_approx(x,30)-x,ORANGE)),run_time=1.7)
        self.play(FadeIn(txt('아래 곡선: 영점쌍 30개 절단 근사',22,ORANGE).move_to(DOWN*4.8)),run_time=.5)
        self.transition(62)

        self.subtitle('이 관계를 표현하는 것이 명시적 공식입니다','전체 추세 + 영점들의 진동 + 보정항')
        a,labels=self.axes([0,100,20],[0,110,20],height=3.8)
        a.shift(UP*.6);labels.shift(UP*.6)
        step=self.staircase(a,self.psi)
        approx=self.polyline(a,x,explicit_approx(x,30),ORANGE)
        self.play(Create(a),FadeIn(labels),Create(step),Create(approx),run_time=1.2)
        self.play(FadeIn(self.legend('실제 ψ(x)','영점쌍 30개 근사').move_to(DOWN*2.1)),run_time=.5)
        summary=VGroup(txt('전체적인 증가',27,INK),txt('＋',26,MUTED),txt('영점들에서 온 진동',27,ORANGE),
                       txt('＋ 보정항',23,MUTED)).arrange(DOWN,buff=.18).move_to(DOWN*3.6)
        self.play(FadeIn(summary),run_time=.7)
        self.to(70)
        self.subtitle('유한한 근사로 계단을 완전히 복원하지는 못합니다','점프 주변에 진동과 잔여 오차가 남습니다')
        self.play(FadeIn(txt('유한 근사에는 점프 주변의 진동과 잔여 오차가 남습니다',21,MUTED).move_to(UP*3.9)),run_time=.5)
        self.transition(75)

        self.subtitle('리만 가설은 이 점들의 위치에 관한 주장입니다','모든 비자명 영점이 실수부 1/2의 직선 위에 있을까?')
        rh=math(r'\operatorname{Re}(s)=\frac12',43,ORANGE).move_to(UP*4.2)
        plane=Axes(x_range=[0,1,1],y_range=[0,55,10],x_length=3.8,y_length=4.2,
                   tips=False,axis_config={'color':MUTED}).move_to(UP*.6)
        line=DashedLine(plane.c2p(.5,0),plane.c2p(.5,55),color=ORANGE)
        zeros=VGroup(*[Dot(plane.c2p(.5,g),color=ORANGE,radius=.06) for g in GAMMAS[:11]])
        labels=VGroup(txt('0',22,MUTED).next_to(plane.c2p(0,0),DOWN),
                      math(r'\frac12',28,ORANGE).next_to(plane.c2p(.5,0),DOWN),
                      txt('1',22,MUTED).next_to(plane.c2p(1,0),DOWN),
                      txt('Re(s)',20,MUTED).next_to(plane.c2p(1,0),RIGHT,buff=.12),
                      txt('Im(s)',20,MUTED).next_to(plane.c2p(0,55),UP,buff=.12))
        self.play(FadeIn(rh),Create(plane),Create(line),FadeIn(zeros),FadeIn(labels),run_time=1.2)
        self.play(FadeIn(txt('알려진 영점 일부 · 모든 영점에 대한 주장은 미해결',22,MUTED).move_to(DOWN*2.7)),run_time=.5)
        self.to(82)
        self.subtitle('참이라면, 오차가 커지는 범위도 더 강하게 제한됩니다','영점의 위치가 소수 분포의 오차와 연결됩니다')
        self.play(FadeIn(txt('점들의 위치 → 흔들림의 성장 범위',28,GOOD).move_to(DOWN*3.9)),run_time=.5)
        self.to(89)
        self.subtitle('소수의 불규칙성을 이해하는 열쇠','복소평면에 놓인 점들 속에 있었습니다')
        self.to(95)
        self.write_captions()

    def axes(self,xr,yr,height=4.6):
        a=Axes(x_range=xr,y_range=yr,x_length=6.6,y_length=height,tips=False,
               axis_config={'color':MUTED}).move_to(DOWN*.2)
        # Place x labels at the bottom of the plotting area, also for signed error plots.
        labels=VGroup(*[txt(f'{v:g}',21,MUTED).next_to(a.c2p(v,yr[0]),DOWN,buff=.12)
                       for v in np.arange(xr[0],xr[1]+.01,xr[2])],
            *[txt(str(v),20,MUTED).next_to(a.c2p(xr[0],v),LEFT,buff=.12) for v in (yr[0],yr[1])],
            txt('x',23,MUTED).next_to(a.c2p(xr[1],yr[0]),RIGHT,buff=.12))
        return a,labels

    def staircase(self,a,values,subtract_x=False):
        pts=[a.c2p(0,0)]
        for n in range(1,101 if len(values)>11 else 11):
            before=values[n-1]-(n if subtract_x else 0)
            after=values[n]-(n if subtract_x else 0)
            pts.extend((a.c2p(n,before),a.c2p(n,after)))
        return VMobject(color=WEIGHT,stroke_width=3).set_points_as_corners(pts)

    def polyline(self,a,x,y,color,width=3):
        pts=[a.c2p(float(i),float(j)) for i,j in zip(x,y)]
        return VMobject(color=color,stroke_width=width).set_points_as_corners(pts)

    def curve(self,a,f,lo,hi,color):
        x=np.linspace(lo,hi,700)
        return self.polyline(a,x,f(x),color)

    def legend(self,left,right):
        return VGroup(txt('● '+left,23,WEIGHT),txt('● '+right,23,ORANGE)).arrange(RIGHT,buff=.45)

    def subtitle(self,a,b):
        if self.cues:self.cues[-1]['end']=self.time
        new=VGroup(txt(a,29),txt(b,22,MUTED)).arrange(DOWN,buff=.24).move_to(DOWN*6.25)
        self.play(ReplacementTransform(self.cap,new) if len(self.cap) else FadeIn(new),run_time=.4)
        self.cap=new;self.cues.append(dict(start=self.time-.4,end=None,text=a+'\n'+b))

    def to(self,target):
        if self.time>target+.05:raise ValueError(f'Time exceeded: {self.time:.3f} > {target}')
        if target>self.time:self.wait(target-self.time)

    def transition(self,target):
        self.to(target-.5);self.wipe()

    def wipe(self):
        old=[m for m in self.mobjects if m is not self.chrome and m is not self.cap]
        self.play(*[FadeOut(m) for m in old],run_time=.5);self.remove(*old)

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
