"""Five replaceable chapters, 22 exact sentence boundaries, shared dual-ratio animation."""
import json
import os
from pathlib import Path
import numpy as np
from manim import *
from quantum_series.shared.theme import BG,INK,MUTED,DATA,GOLD,OLD,text,p,configure
from quantum_series.shared.components import oscillator,connecting_wave
from quantum_series.shared.photoelectric import (LOW,HIGH,METAL,energy_unit,travelling_wave,
    slider,PhotoelectricExperiment,energy_comparison)
from quantum_series.episodes.ep02_photoelectric.layouts import PhotoelectricLayout
from quantum_series.episodes.ep02_photoelectric.physics_model import PhotoelectricModel,LOW_FREQUENCY,HIGH_FREQUENCY

HERE=Path(__file__).resolve().parent
SCRIPT=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
LAYOUT=PhotoelectricLayout(configure().portrait)

def wrap(s,limit):
    lines=[];line=''
    for word in s.split():
        if line and len(line)+len(word)+1>limit:lines.append(line);line=word
        else:line=(line+' '+word).strip()
    return '\n'.join(lines+[line])

class PhotoelectricScene(Scene):
    offset=0
    def setup(self):
        self.L=LAYOUT;self.body=VGroup();self.caption=None;self.heading=None
        self.add(text('양자역학의 발견   /   1905',x=0 if self.L.portrait else -4.9,y=self.L.brand_y,size=18,color=MUTED))
        y=6.65 if self.L.portrait else 3.5;w=7.6 if self.L.portrait else 14.4
        self.add(Line(p(-w/2,y),p(w/2,y),color=MUTED,stroke_width=1,stroke_opacity=.25))
        phase={0:'01  현상과 질문',16:'02  기존 설명의 한계',39:'03  새로운 가설',62:'04  방출 조건',86:'05  실험을 설명하는 결론'}[self.offset]
        self.add(text(phase,x=0 if self.L.portrait else 4.7,y=-4.55 if self.L.portrait else self.L.brand_y,size=17,color=MUTED))

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

    def show(self,*objects,run_time=.6):
        self.body.add(*objects);self.play(*[FadeIn(o) for o in objects],run_time=run_time)

    def clear_body(self,run_time=.35):
        if len(self.body):self.play(FadeOut(self.body),run_time=run_time)
        self.body=VGroup()

    def note(self,s,y=None,color=MUTED):
        return text(s,y=(-3.65 if self.L.portrait else -2.85) if y is None else y,
                    size=18,color=color,width=self.L.body_width)

    def apparatus(self,model):
        return PhotoelectricExperiment(model).scale(self.L.apparatus_scale).move_to(self.L.apparatus_center)

    def flash_release(self,apparatus,index=1,run_time=.65):
        _,end,_=apparatus.anchors()
        self.play(*apparatus.release(index),Flash(end,color=DATA,flash_radius=.16,line_length=.08),run_time=run_time)

    def comparison(self,explained=False):
        groups=[];experiments=[]
        models=[PhotoelectricModel(frequency=LOW_FREQUENCY,intensity=4),PhotoelectricModel(frequency=HIGH_FREQUENCY,intensity=.35)]
        for i,(center,model) in enumerate(zip(self.L.comparison_centers,models)):
            cx,cy=center[:2]
            card=RoundedRectangle(width=self.L.panel_width,height=self.L.panel_height,corner_radius=.15,color=LOW if i==0 else HIGH,
                                  stroke_width=1.3,fill_color=BG,fill_opacity=.2).move_to(center)
            exp=PhotoelectricExperiment(model).scale(.55 if self.L.portrait else .72)
            exp.move_to(p(cx-2 if self.L.portrait else cx,cy-.15 if self.L.portrait else cy+.15))
            title=text('강한 저진동수 빛' if i==0 else '약한 고진동수 빛',cx,cy+(1.04 if self.L.portrait else 1.62),23,LOW if i==0 else HIGH,width=self.L.panel_width-.3)
            result=text('전자 방출 없음' if i==0 else '전자 방출 가능',cx+1.05 if self.L.portrait else cx,
                        cy-.1 if self.L.portrait else cy-1.25,25,MUTED if i==0 else DATA,width=3.2 if self.L.portrait else 5.8)
            group=VGroup(card,exp,title,result)
            if explained:
                group.add(text('E < Φ · 한 단위 에너지 부족' if i==0 else 'E > Φ · 한 단위 에너지 충분',
                               cx+1.05 if self.L.portrait else cx,cy-.7 if self.L.portrait else cy-1.8,
                               19,GOLD,width=3.4 if self.L.portrait else 5.8))
            groups.append(group);experiments.append(exp)
        return VGroup(*groups),experiments

    def conceptual_bridge(self):
        xl,xr=self.L.pair_columns
        # Exact EP.01 oscillator component and gold energy-unit palette.
        oscillators=VGroup(*[oscillator(x,0) for x in [-1.65,-.55,.55,1.65]]).scale(.62).move_to(p(xl,.35))
        tiles=VGroup(*[energy_unit(.27).move_to(p(xl+(i-1)*.38,1.45)) for i in range(3)])
        exp=PhotoelectricExperiment(PhotoelectricModel()).scale(.61).move_to(p(xr,.65))
        labels=VGroup(text('1900 · 플랑크',xl,2.35 if self.L.portrait else 2.05,25,GOLD,width=3.5),
                      text('에너지 분배 계산',xl,-1.3,23,MUTED,width=3.5),
                      text('1905 · 아인슈타인',xr,2.35 if self.L.portrait else 2.05,25,GOLD,width=3.6),
                      text('빛의 에너지 전달',xr,-1.3,23,MUTED,width=3.5))
        arrow=Arrow(p(-.45,.5),p(.45,.5),color=GOLD,buff=0,stroke_width=2)
        formula=text('E = hν',y=-2.35,size=39,color=GOLD)
        return VGroup(oscillators,tiles,exp,labels,arrow,formula)

class ObservationDirection(PhotoelectricScene):
    offset=0
    def construct(self):
        self.cue(0)
        exp=self.apparatus(PhotoelectricModel())
        self.show(exp,run_time=.45)
        label=text('금속 내부의 전자',x=0 if self.L.portrait else -3.8,
                   y=-.95 if self.L.portrait else -1.8,size=21,color=DATA)
        self.show(label,run_time=.25)
        self.flash_release(exp,run_time=.65)
        self.show(self.note('같은 가상 금속 · 일반적인 광전효과의 개념도'),run_time=.3)
        self.to(3)

        self.cue(1)
        self.play(Indicate(exp.plate,color=DATA,scale_factor=1.02),run_time=.55)
        self.to(5)

        self.cue(2)
        exp.reset_electrons()
        self.play(FadeOut(label),exp.change(frequency=LOW_FREQUENCY,intensity=.5),run_time=.4)
        self.body.remove(label)
        location=self.L.readout_center
        control=slider('빛의 세기',.15,x=location[0],y=location[1]+.25,width=3.3,color=LOW)
        result=text('전자 방출 없음',location[0],location[1]-.6,30,MUTED,width=4)
        self.show(control,result,run_time=.4)
        self.play(exp.change(intensity=4),Transform(control,slider('빛의 세기 ↑',1,x=location[0],y=location[1]+.25,width=3.3,color=LOW)),run_time=.8)
        self.to(9)

        self.cue(3)
        self.clear_body(.35)
        compare,experiments=self.comparison()
        self.show(compare,self.note('금속의 종류와 일함수는 고정 · 색은 진동수의 예시'),run_time=.55)
        self.flash_release(experiments[1],run_time=.7)
        self.to(14)

        self.cue(4)
        question=text('?',x=0,y=.275 if self.L.portrait else -.2,size=38,color=INK)
        self.show(question,run_time=.35)
        self.to(16)

class WavesDirection(PhotoelectricScene):
    offset=16
    def construct(self):
        self.cue(5)
        phase=ValueTracker(0)
        waveform=always_redraw(lambda:travelling_wave(width=6.5 if self.L.portrait else 10.5,amplitude=.38,cycles=4,phase=phase.get_value()).move_to(p(0,.8)))
        self.show(waveform,text('전자기파',y=-.45,size=34,color=HIGH),run_time=.5)
        self.play(phase.animate.set_value(TAU),run_time=1.05,rate_func=linear)
        waveform.clear_updaters();self.to(19)

        self.cue(6)
        self.clear_body(.3)
        xleft,xright=self.L.pair_columns
        if self.L.portrait:
            positions=[p(0,2.3),p(0,.55)];width=6.2
        else:positions=[p(xleft,.65),p(xright,.65)];width=5.4
        weak=travelling_wave(width=width,amplitude=.15,cycles=3,color=LOW).move_to(positions[0])
        strong=travelling_wave(width=width,amplitude=.15,cycles=3,color=LOW).move_to(positions[1])
        labels=VGroup(text('약한 빛',positions[0][0],positions[0][1]+.65,23,MUTED),
                      text('강한 빛',positions[1][0],positions[1][1]+.65,23,LOW))
        self.show(weak,strong,labels,run_time=.5)
        self.play(Transform(strong,travelling_wave(width=width,amplitude=.48,cycles=3,color=LOW).move_to(positions[1])),run_time=.8)
        gauge_outline=Rectangle(width=4.6,height=.32,color=MUTED,stroke_width=1.5).move_to(p(0,-1.3))
        fill=Rectangle(width=.04,height=.28,color=LOW,fill_color=LOW,fill_opacity=.6).move_to(p(-2.25,-1.3))
        self.show(gauge_outline,fill,text('같은 진동수 · 더 큰 진폭',y=-.6 if self.L.portrait else -1.9,size=23,color=LOW),run_time=.4)
        self.play(fill.animate.stretch_to_fit_width(4.5).move_to(p(0,-1.3)),run_time=1.0)
        self.show(self.note('고전적인 에너지 전달의 직관 · 전자의 에너지 축적 모형 아님'),run_time=.35)
        self.to(26)

        self.cue(7)
        self.clear_body(.3)
        amplitude=ValueTracker(.16);frequency=ValueTracker(2.4)
        controlled=always_redraw(lambda:travelling_wave(width=6.1 if self.L.portrait else 10,amplitude=amplitude.get_value(),cycles=frequency.get_value()).move_to(p(0,1.25)))
        self.show(controlled,run_time=.4)
        xl,xr=self.L.pair_columns
        a_slider=slider('세기 · 진폭 변화',.2,x=xl,y=-.6,width=3.1,color=LOW)
        f_slider=slider('진동수 변화',.2,x=xr,y=-.6,width=3.1,color=HIGH)
        self.show(a_slider,f_slider,run_time=.35)
        self.play(amplitude.animate.set_value(.45),Transform(a_slider,slider('세기 · 진폭 변화',.9,x=xl,y=-.6,width=3.1,color=LOW)),run_time=.7)
        self.play(frequency.animate.set_value(5),Transform(f_slider,slider('진동수 변화',.9,x=xr,y=-.6,width=3.1,color=HIGH)),run_time=.7)
        self.show(text('독립적으로 바꿀 수 있는 두 양',y=-2.1,size=28,color=INK),run_time=.35)
        controlled.clear_updaters();self.to(31)

        self.cue(8)
        self.clear_body(.25)
        # The horizontal axis below is TIME, not position. The dots explicitly
        # oscillate at fixed spatial positions, with the same playback interval.
        xl,xr=self.L.pair_columns
        clock=ValueTracker(0)
        slow=always_redraw(lambda:Dot(p(xl,.55+.6*np.sin(TAU*clock.get_value())),radius=.12,color=LOW))
        fast=always_redraw(lambda:Dot(p(xr,.55+.6*np.sin(3*TAU*clock.get_value())),radius=.12,color=HIGH))
        rails=VGroup(*[Line(p(x,-.12),p(x,1.22),color=MUTED,stroke_width=1.4) for x in (xl,xr)])
        self.show(rails,slow,fast,text('느린 진동',xl,2,25,LOW),text('빠른 진동',xr,2,25,HIGH),
                  text('진동수 = 1초 동안의 진동 횟수',y=-1.2,size=26,color=MUTED,width=self.L.body_width),run_time=.3)
        self.play(clock.animate.set_value(1),run_time=1.15,rate_func=linear)
        slow.clear_updaters();fast.clear_updaters();self.to(34)

        self.cue(9)
        self.clear_body(.3)
        xl,xr=self.L.pair_columns
        width=3.1 if self.L.portrait else 5.6
        left=travelling_wave(width=width,amplitude=.17,cycles=2.5,color=LOW).move_to(p(xl,.65))
        right=travelling_wave(width=width,amplitude=.3,cycles=2.5,color=HIGH).move_to(p(xr,.65))
        self.show(left,right,text('세기 변화',xl,2.1,26,LOW),text('진동수 변화',xr,2.1,26,HIGH),
                  text('진동수 고정',xl,-.75,21,MUTED),text('진폭 고정',xr,-.75,21,MUTED),run_time=.4)
        self.play(Transform(left,travelling_wave(width=width,amplitude=.48,cycles=2.5,color=LOW).move_to(p(xl,.65))),
                  Transform(right,travelling_wave(width=width,amplitude=.3,cycles=5,color=HIGH).move_to(p(xr,.65))),run_time=.95)
        self.show(self.note('파형은 개념도 · 두 변화는 서로 다르다'),run_time=.3)
        self.to(39)

class QuantaDirection(PhotoelectricScene):
    offset=39
    def construct(self):
        self.cue(10)
        wave=connecting_wave(self.L).shift(UP*.1)
        self.show(wave,text('Albert Einstein',y=1.9,size=39,color=INK),
                  text('1905',y=-1.35,size=45,color=GOLD),run_time=.6)
        self.to(43)

        self.cue(11)
        self.clear_body(.35)
        wave=connecting_wave(self.L)
        self.show(wave,run_time=.4)
        units=VGroup(*[energy_unit().move_to(p((i-2)*1.1,.25)) for i in range(5)])
        self.body.add(units)
        self.play(wave.animate.set_stroke(opacity=.3),LaggedStart(*[FadeIn(u,shift=UP*.15) for u in units],lag_ratio=.13),run_time=1.1)
        self.show(text('빛의 에너지를 개별 단위로 전달',y=-1.25,size=32,color=GOLD,width=self.L.body_width),
                  self.note('에너지 전달 관점의 비교 · 파동이 공으로 쪼개지는 과정 아님'),run_time=.45)
        self.to(48)

        self.cue(12)
        self.clear_body(.35)
        bridge=self.conceptual_bridge()
        self.show(bridge,self.note('분배 계산의 단위와 빛 자체에 관한 가설을 구별'),run_time=.75)
        self.to(54)

        self.cue(13)
        self.clear_body(.3)
        w=travelling_wave(width=5.8,cycles=2,amplitude=.26).move_to(p(0,1.25))
        bar=Rectangle(width=1.1,height=.3,color=GOLD,fill_color=GOLD,fill_opacity=.6).move_to(p(0,-.1))
        self.show(w,bar,text('E = hν',y=-1.45,size=42,color=GOLD),run_time=.35)
        self.play(Transform(w,travelling_wave(width=5.8,cycles=4,amplitude=.26).move_to(p(0,1.25))),bar.animate.stretch_to_fit_width(2.2),run_time=.65)
        self.show(self.note('막대의 길이 = 에너지 · 실제 입자의 크기가 아님'),run_time=.25)
        self.to(57)

        self.cue(14)
        self.clear_body(.3)
        xl,xr=self.L.pair_columns
        low=PhotoelectricModel(frequency=LOW_FREQUENCY)
        high=PhotoelectricModel()
        waves=VGroup(travelling_wave(width=3.1 if self.L.portrait else 5.5,cycles=2,color=LOW).move_to(p(xl,1.3)),
                     travelling_wave(width=3.1 if self.L.portrait else 5.5,cycles=2*high.frequency/low.frequency,color=HIGH).move_to(p(xr,1.3)))
        bars=VGroup(*[Rectangle(width=m.energy_ev*.65,height=.32,color=GOLD,fill_color=GOLD,fill_opacity=.65).move_to(p(x,-.15)) for x,m in [(xl,low),(xr,high)]])
        self.show(waves,bars,text('낮은 진동수',xl,2.2,24,LOW),text('높은 진동수',xr,2.2,24,HIGH),
                  text('작은 에너지',xl,-.85,25,GOLD),text('큰 에너지',xr,-.85,25,GOLD),run_time=.5)
        self.play(Indicate(bars[1],color=GOLD,scale_factor=1.08),run_time=.6)
        self.show(text('E = hν',y=-2.15,size=39,color=GOLD),run_time=.3)
        self.to(62)

class ThresholdDirection(PhotoelectricScene):
    offset=62
    def construct(self):
        self.cue(15)
        exp=self.apparatus(PhotoelectricModel(frequency=LOW_FREQUENCY,intensity=.6))
        cx,cy=self.L.readout_center[:2]
        readout=energy_comparison(exp.model,cx,cy,width=3.5 if not self.L.portrait else 4.4)
        self.show(exp,readout,self.note('같은 가상 금속 · 일함수 Φ 고정 · 단일 단위 흡수 모형'),run_time=.6)
        self.to(66)

        self.cue(16)
        condition=text('E < Φ   →   방출 없음',cx,cy-1.2,26,MUTED,width=5.9)
        self.show(condition,run_time=.35)
        unit,end=exp.incident_unit(index=0)
        self.show(unit,run_time=.2)
        self.play(unit.animate.move_to(end),run_time=.65)
        self.play(FadeOut(unit),run_time=.2);self.body.remove(unit)
        self.play(exp.change(intensity=4),run_time=.5)
        many=[];targets=[]
        for index in [0,1,2,3]:
            u,target=exp.incident_unit(index=index)
            u.shift(UP*(.12*index));many.append(u);targets.append(target)
        self.show(*many,run_time=.35)
        self.play(LaggedStart(*[u.animate.move_to(target) for u,target in zip(many,targets)],lag_ratio=.15),run_time=1.0)
        self.play(*[FadeOut(u) for u in many],run_time=.25)
        self.body.remove(*many)
        self.to(73)

        self.cue(17)
        self.play(exp.change(frequency=HIGH_FREQUENCY,intensity=.35),
                  Transform(readout,energy_comparison(PhotoelectricModel(intensity=.35),cx,cy,width=3.5 if not self.L.portrait else 4.4)),
                  Transform(condition,text('E > Φ   →   방출 가능',cx,cy-1.2,26,DATA,width=5.9)),run_time=.55)
        unit,end=exp.incident_unit(index=1)
        self.show(unit,run_time=.2)
        self.play(unit.animate.move_to(end),run_time=.75)
        self.play(FadeOut(unit),run_time=.15);self.body.remove(unit)
        self.flash_release(exp,run_time=.7)
        kinetic=text('Kmax = E − Φ',x=0 if self.L.portrait else -3.8,y=3.8 if self.L.portrait else -1.9,size=24,color=DATA,width=4.2)
        self.show(kinetic,run_time=.3)
        self.to(79)

        self.cue(18)
        self.clear_body(.35)
        xl,xr=self.L.pair_columns
        self.show(text('세기 증가',xl,1.95,28,LOW),text('진동수 증가',xr,1.95,28,HIGH),
                  text('진동수 고정',xl,1.3,21,MUTED),text('도달 단위 수 고정',xr,1.3,21,MUTED),run_time=.4)
        left=VGroup(*[energy_unit().move_to(p(xl+(i%3-1)*.55,.7-i//3*.55)) for i in range(3)])
        right=VGroup(*[energy_unit().move_to(p(xr+(i-1)*.55,.7)) for i in range(3)])
        self.show(left,right,run_time=.35)
        extra=VGroup(*[energy_unit().move_to(p(xl+(i-1)*.55,.15)) for i in range(3)])
        self.body.add(extra);self.play(LaggedStart(*[FadeIn(u) for u in extra],lag_ratio=.1),run_time=.6)
        energy=Rectangle(width=.8,height=.25,color=GOLD,fill_color=GOLD,fill_opacity=.65).move_to(p(xr,-.5))
        self.show(energy,run_time=.25)
        self.play(energy.animate.stretch_to_fit_width(1.6),run_time=.65)
        self.show(text('단위 수 ↑',xl,-1.2,30,GOLD),text('한 단위의 에너지 ↑',xr,-1.2,27,GOLD,width=3.5 if self.L.portrait else 6),
                  self.note('같은 면적·시간에서 비교 · 오른쪽 막대 길이는 에너지'),run_time=.45)
        self.to(86)

class ResolutionDirection(PhotoelectricScene):
    offset=86
    def construct(self):
        self.cue(19)
        comparison,experiments=self.comparison(explained=True)
        self.show(comparison,self.note('같은 금속 · 같은 일함수 · 개별 에너지의 차이'),run_time=.65)
        self.flash_release(experiments[1],run_time=.7)
        self.to(91)

        self.cue(20)
        self.clear_body(.35)
        self.show(self.conceptual_bridge(),self.note('플랑크의 분배 계산 ≠ 빛 자체의 광양자 가설'),run_time=.7)
        self.to(97)

        self.cue(21)
        self.clear_body(.35)
        wave=connecting_wave(self.L)
        unit=energy_unit(.4).move_to(p(-1.4,.25))
        self.show(wave,unit,text('광자  Photon',y=-1.15,size=43,color=GOLD),run_time=.5)
        self.play(unit.animate.move_to(p(1.4,.25)),run_time=.85,rate_func=linear)
        if os.environ.get('QUANTUM_ENDING','standalone')=='standalone':
            self.play(wave.animate.set_stroke(opacity=.65),run_time=.3)
        self.show(self.note('에너지 단위의 기호 · 실제 크기나 궤적을 뜻하지 않음'),run_time=.25)
        self.to(100);self.wait(1)
