"""Six independent claims, calculated Coulomb motion, and responsive dual-ratio staging."""
import json
import os
from pathlib import Path
import numpy as np
from manim import *
from quantum_series.shared.theme import BG,INK,MUTED,GOLD,text,p,configure
from quantum_series.shared.rutherford import (ALPHA,FOIL,POSITIVE,ELECTRON,NUCLEUS,EXPECTED,OBSERVED,
    AlphaParticle,ThomsonAtom,RutherfordAtom,CoulombTrajectory,foil_apparatus,atom_mosaic,classical_spiral)
from quantum_series.episodes.ep03_rutherford.layouts import RutherfordLayout

HERE=Path(__file__).resolve().parent
SCRIPT=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
LAYOUT=RutherfordLayout(configure().portrait)

def wrap(s,limit):
    result=[];line=''
    for word in s.split():
        if line and len(line)+1+len(word)>limit:result.append(line);line=word
        else:line=(line+' '+word).strip()
    return '\n'.join(result+[line])

class RutherfordScene(Scene):
    offset=0
    def setup(self):
        self.L=LAYOUT;self.body=VGroup();self.caption=None;self.heading=None
        self.add(text('양자역학의 발견   /   원자 구조',x=0 if self.L.portrait else -4.9,y=self.L.brand_y,size=18,color=MUTED))
        w=7.6 if self.L.portrait else 14.4;y=6.65 if self.L.portrait else 3.5
        self.add(Line(p(-w/2,y),p(w/2,y),color=MUTED,stroke_width=1,stroke_opacity=.25))
        stage={0:'01  현상과 질문',16:'02  기존 원자 모형',40:'03  실험과의 차이',51:'04  새로운 해석',77:'05  원자핵 모형',91:'06  남은 물리적 질문'}[self.offset]
        self.add(text(stage,x=0 if self.L.portrait else 4.7,y=-4.55 if self.L.portrait else self.L.brand_y,size=17,color=MUTED))

    def to(self,target):
        remaining=target-self.offset-self.time
        if remaining<-.018:raise RuntimeError(f'Timing overrun {self.offset+self.time:.3f} > {target}')
        frames=round(remaining*30)
        if frames>0:self.wait((frames+1e-5)/30)

    def cue(self,index):
        sentence=SCRIPT['sentences'][index];self.to(sentence['start'])
        if self.caption:self.remove(self.caption)
        self.caption=text(wrap(sentence['text'],26 if self.L.portrait else 62),y=self.L.caption_y,
                          size=24 if self.L.portrait else 25,width=7.6 if self.L.portrait else 14.1)
        self.add(self.caption)
        heading=text(sentence['heading'],y=self.L.heading_y,size=33 if self.L.portrait else 34,width=self.L.body_width)
        if self.heading:self.play(Transform(self.heading,heading),run_time=.25)
        else:self.heading=heading;self.play(FadeIn(heading,shift=UP*.1),run_time=.3)

    def show(self,*objects,run_time=.55):
        self.body.add(*objects);self.play(*[FadeIn(o) for o in objects],run_time=run_time)

    def clear_body(self,run_time=.35):
        if len(self.body):self.play(FadeOut(self.body),run_time=run_time)
        self.body=VGroup()

    def note(self,s,y=None,color=MUTED):
        return text(s,y=(-3.65 if self.L.portrait else -2.85) if y is None else y,
                    size=18,color=color,width=self.L.body_width)

    def callout(self,s,color=INK,size=30):
        center=self.L.callout_center
        return text(s,center[0],center[1],size,color,width=7.3 if self.L.portrait else 5.6)

    def launch(self,b,distribution='point',run_time=1.0,force=False,detector=False,color=OBSERVED):
        scale=self.L.detector_scale if detector else self.L.scatter_scale
        view=CoulombTrajectory(b,distribution,self.L.plot_center,scale,detector)
        dot=AlphaParticle(view.at(0))
        trace=TracedPath(dot.get_center,stroke_color=color,stroke_width=2.2)
        self.body.add(dot,trace);self.add(trace,dot)
        extras=[]
        if force:
            def radial_arrow():
                r=dot.get_center()-self.L.plot_center
                unit=r/max(np.linalg.norm(r),1e-9)
                length=.24+.5/(1+4*np.dot(r,r))
                return Arrow(dot.get_center(),dot.get_center()+unit*length,buff=.025,color=GOLD,
                             stroke_width=2.6,max_tip_length_to_length_ratio=.28)
            arrow=always_redraw(radial_arrow)
            sign=always_redraw(lambda:text('+',*(dot.get_center()[:2]+np.array([0,.22])),size=21,color=ALPHA))
            extras=[arrow,sign];self.body.add(*extras);self.add(*extras)
        self.play(UpdateFromAlphaFunc(dot,lambda obj,a:obj.move_to(view.at(a))),run_time=run_time,rate_func=linear)
        trace.clear_updaters()
        finished=view.path.copy().set_color(color)
        if distribution=='diffuse':finished=DashedVMobject(finished,num_dashes=50)
        trace.become(finished)
        for extra in extras:extra.clear_updaters()
        if detector:
            self.play(Flash(dot.get_center(),color=OBSERVED,flash_radius=.13,line_length=.06),run_time=.22)
        return view,dot,trace,extras

    def scatter_atom(self):
        atom=RutherfordAtom(electrons=False).scale(self.L.scatter_scale).move_to(self.L.plot_center)
        # Enlarge the symbol for legibility; the persistent scale warning applies.
        atom.nucleus.scale(1.15)
        return atom

class FoilObservationDirection(RutherfordScene):
    offset=0
    def construct(self):
        self.cue(0)
        apparatus=foil_apparatus(self.L.plot_center,self.L.scatter_scale)
        self.show(apparatus,self.note('대표 경로를 강조한 개념도 · 실제 산란 비율 아님'),run_time=.45)
        dot=AlphaParticle(self.L.plot_center+p(-4.8*.65,.65))
        self.show(dot,run_time=.2)
        self.play(dot.animate.move_to(self.L.plot_center+p(-.15,.65)),run_time=.9,rate_func=linear)
        self.to(3)

        self.cue(1)
        self.play(FadeOut(dot),run_time=.2);self.body.remove(dot)
        for b in [-1.8,-1.0,.9,1.7]:self.launch(b,run_time=.48)
        self.launch(.17,run_time=.95)
        label=self.callout('대부분 통과\n일부는 큰 방향 변화',OBSERVED,29)
        self.show(label,run_time=.3)
        self.to(9)

        self.cue(2)
        self.play(FadeOut(label),run_time=.2);self.body.remove(label)
        self.launch(.025,run_time=1.35)
        self.show(self.callout('후방 산란',OBSERVED,31),run_time=.3)
        self.to(12)

        self.cue(3)
        self.clear_body(.35)
        mosaic=atom_mosaic().scale(1.6).move_to(self.L.main_center)
        self.show(mosaic,run_time=.5)
        question=text('?',*self.L.main_center[:2],size=65,color=INK)
        self.show(question,self.note('아직 원자 내부는 알 수 없었다'),run_time=.45)
        self.play(mosaic.animate.scale(1.15),run_time=.6)
        self.to(16)

class ThomsonDirection(RutherfordScene):
    offset=16
    def construct(self):
        self.cue(4)
        center=self.L.main_center
        outline=Circle(radius=1.7,color=MUTED,stroke_width=1.7).move_to(center)
        plus=text('+',center[0]-.65,center[1],60,POSITIVE)
        minus=text('−',center[0]+.65,center[1],60,ELECTRON)
        self.show(outline,plus,minus,self.callout('전체 전하 = 0',INK,36),run_time=.6)
        self.to(19)

        self.cue(5)
        self.clear_body(.35)
        electron=Dot(center,radius=.16,color=ELECTRON)
        self.show(electron,text('−',center[0],center[1]+.45,45,ELECTRON),
                  text('1897 · J. J. Thomson',center[0],center[1]+1.45,29,INK,width=6),run_time=.6)
        self.show(self.callout('음전하를 가진 전자\n중성인 원자라면 양전하도 필요',POSITIVE,29),run_time=.5)
        self.to(26)

        self.cue(6)
        self.clear_body(.35)
        atom=ThomsonAtom().move_to(center)
        self.show(atom,self.callout('양전하가 넓게 분포\n그 안에 들어 있는 전자',POSITIVE,28),
                  self.note('톰슨 모형의 개념도 · 전자 궤도를 나타내지 않음'),run_time=.75)
        self.to(32)

        self.cue(7)
        self.clear_body(.35)
        atom=ThomsonAtom().scale(self.L.scatter_scale).move_to(self.L.plot_center)
        self.show(atom,self.note('양전하 분포만 비교한 모형 · 초기 에너지·전체 양전하량 고정'),run_time=.5)
        expected=VGroup(*[DashedVMobject(CoulombTrajectory(b,'diffuse',self.L.plot_center,self.L.scatter_scale).path.set_color(EXPECTED),num_dashes=50)
                         for b in [-.7,.1,.8]])
        self.show(expected,run_time=.6)
        for b in [-.7,.1,.8]:self.launch(b,'diffuse',run_time=.9,color=EXPECTED)
        self.show(self.callout('예상: 비교적 작은 방향 변화',EXPECTED,28),run_time=.4)
        self.to(40)

class GeigerMarsdenDirection(RutherfordScene):
    offset=40
    def construct(self):
        self.cue(8)
        apparatus=foil_apparatus(self.L.plot_center,self.L.detector_scale,detector=True)
        self.show(apparatus,self.note('실험 장치의 개념도 · 검출면의 빛으로 입자 도착을 관측'),run_time=.65)
        description=self.callout('Geiger · Marsden\n러더퍼드의 지도 아래',INK,28)
        self.show(description,run_time=.4)
        self.launch(.9,run_time=1.0,detector=True)
        self.launch(-1.6,run_time=.8,detector=True)
        self.to(47)

        self.cue(9)
        self.play(FadeOut(description),run_time=.2);self.body.remove(description)
        expected=DashedVMobject(CoulombTrajectory(.17,'diffuse',self.L.plot_center,self.L.detector_scale,True).path.set_color(EXPECTED),num_dashes=50)
        self.show(expected,run_time=.3)
        self.launch(.17,run_time=1.3,detector=True)
        key=VGroup(text('회색 점선: 기존 예상',size=19,color=EXPECTED),text('청록색: 큰 산란의 대표 경로',size=19,color=OBSERVED)).arrange(DOWN,buff=.15)
        key.move_to(self.L.callout_center+(ORIGIN if self.L.portrait else DOWN*.9))
        self.show(key,run_time=.35)
        self.to(51)

class CoulombDirection(RutherfordScene):
    offset=51
    def construct(self):
        self.cue(10)
        center=self.L.main_center
        atom=ThomsonAtom().move_to(center)
        self.show(atom,self.note('양전하 분포를 바꾸어 비교하는 개념도 · 축척 비례 아님'),run_time=.55)
        core=Dot(center,radius=.11,color=NUCLEUS)
        self.play(ReplacementTransform(atom.cloud,core),*[symbol.animate.move_to(center) for symbol in atom.positives],run_time=1.15)
        self.play(FadeOut(atom.positives),run_time=.3)
        atom.remove(atom.cloud,atom.positives);atom.add(core)
        self.show(self.callout('퍼진 양전하 → 작은 중심부',NUCLEUS,30),run_time=.4)
        self.to(58)

        self.cue(11)
        self.clear_body(.35)
        self.show(self.scatter_atom(),self.note('쿨롱 반발력으로 계산한 경로 · 핵의 크기는 개념적 확대'),
                  self.callout('양전하 + 양전하\n서로 밀어낸다',GOLD,30),run_time=.55)
        center=self.L.plot_center
        self.show(text('+',center[0],center[1]+.3,23,NUCLEUS),run_time=.2)
        self.launch(.09,run_time=2.6,force=True)
        self.to(65)

        self.cue(12)
        self.clear_body(.3)
        self.show(self.scatter_atom(),self.note('초기 에너지·핵 전하량 고정 · 접근 거리만 다르게'),run_time=.4)
        for b in [1.0,1.7,2.3]:self.launch(b,run_time=.72)
        self.show(self.callout('멀리 지나가면 작은 방향 변화',OBSERVED,28),run_time=.35)
        self.to(70)

        self.cue(13)
        self.clear_body(.3)
        self.show(self.scatter_atom(),self.note('선택한 경로의 개념도 · 실제 빈도·거리 비율을 재현한 그림 아님'),run_time=.4)
        for b in [-2.2,-1.65,-1.1,1.1,1.65,2.2]:self.launch(b,run_time=.4)
        self.launch(.035,run_time=1.05)
        self.show(self.callout('먼 경로는 거의 직진\n가까운 경로는 큰 산란',OBSERVED,28),run_time=.3)
        self.to(77)

class NuclearModelDirection(RutherfordScene):
    offset=77
    def construct(self):
        self.cue(14)
        atom=RutherfordAtom().move_to(self.L.main_center)
        self.show(atom,self.callout('1911\nErnest Rutherford',INK,33),
                  self.note('전자 기호의 위치는 개념도 · 안정된 원형 궤도를 가정하지 않음'),run_time=.7)
        self.play(Indicate(atom.nucleus,color=NUCLEUS,scale_factor=1.8),run_time=.8)
        self.to(84)

        self.cue(15)
        self.clear_body(.3)
        xl,xr=self.L.pair_columns
        left=ThomsonAtom().scale(.6).move_to(p(xl,.35))
        right=RutherfordAtom().scale(.6).move_to(p(xr,.35))
        self.show(left,right,text('톰슨 모형',xl,2.1,26,POSITIVE),text('러더퍼드 모형',xr,2.1,26,NUCLEUS),
                  text('퍼진 양전하',xl,-1.3,23,MUTED),text('중심에 집중된 양전하',xr,-1.3,23,MUTED,width=3.6 if self.L.portrait else 6),
                  self.note('모형 비교 · 축척 비례 아님'),run_time=.55)
        self.to(87)

        self.cue(16)
        self.clear_body(.3)
        center=self.L.main_center
        outer=Circle(radius=2.1 if self.L.portrait else 1.8,color=MUTED,stroke_width=1.7).move_to(center)
        core=Dot(center,radius=.025,color=NUCLEUS)
        self.show(outer,core,self.callout('원자 전체에 비해\n매우 작은 중심부',NUCLEUS,30),
                  self.note('축척 비례 아님 · 실제 크기 차이는 훨씬 크다'),run_time=.5)
        self.play(Indicate(core,color=NUCLEUS,scale_factor=3),run_time=.7)
        self.to(91)

class StabilityDirection(RutherfordScene):
    offset=91
    def construct(self):
        self.cue(17)
        nx,ex=(-1.15,1.55) if self.L.portrait else (-2.3,2.3)
        y=.65 if self.L.portrait else .35
        nucleus=Dot(p(nx,y),radius=.18,color=NUCLEUS)
        electron=Dot(p(ex,y),radius=.1,color=ELECTRON)
        signs=VGroup(text('+',nx,y+.5,35,NUCLEUS),text('−',ex,y+.5,35,ELECTRON))
        self.show(nucleus,electron,signs,text('핵과 전자만으로는 남아 있는 질문',y=-1.3,size=29,color=MUTED,width=self.L.body_width),run_time=.65)
        self.to(95)

        self.cue(18)
        arrows=VGroup(Arrow(p(nx+.3,y),p(nx+1.0,y),buff=0,color=GOLD,stroke_width=3),
                      Arrow(p(ex-.25,y),p(ex-.95,y),buff=0,color=GOLD,stroke_width=3))
        self.show(arrows,text('서로 끌어당기는 전기적 인력',y=-.45,size=28,color=GOLD,width=self.L.body_width),run_time=.6)
        self.to(100)

        self.cue(19)
        self.clear_body(.3)
        center=self.L.spiral_center
        path=classical_spiral(center,self.L.spiral_radius)
        nucleus=Dot(center,radius=.15,color=NUCLEUS)
        electron=Dot(path.get_start(),radius=.075,color=ELECTRON)
        self.show(nucleus,electron,self.note('고전적 궤도 모형의 복사 손실 문제 · 실제 전자의 궤도 아님'),run_time=.4)
        trace=TracedPath(electron.get_center,stroke_color=ELECTRON,stroke_width=2)
        self.body.add(trace);self.add(trace)
        self.play(MoveAlongPath(electron,path),run_time=1.7,rate_func=linear)
        trace.clear_updaters();trace.become(path)
        question=text('원자는 왜 안정적으로\n존재할 수 있을까?',x=0 if self.L.portrait else 3.6,
                      y=-2.25 if self.L.portrait else .3,size=33,color=INK,width=7.3 if self.L.portrait else 6)
        self.show(question,run_time=.3)
        if os.environ.get('QUANTUM_ENDING','standalone')=='standalone':
            self.play(trace.animate.set_stroke(opacity=.6),run_time=.25)
        self.to(104);self.wait(1)
