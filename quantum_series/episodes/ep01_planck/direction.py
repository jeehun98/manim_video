"""Four replaceable scenes, shared choreography, separate responsive layout."""
import json
import os
from pathlib import Path
from manim import *
from quantum_series.shared.theme import BG, INK, MUTED, HEAT, DATA, OLD, GOLD, text, p, configure
from quantum_series.shared.components import (Spectrum, metal, wave, legend, oscillator,
    energy_tiles, count_labels, connecting_wave)

HERE=Path(__file__).resolve().parent
SCRIPT=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
LAYOUT=configure()

def wrap(s, limit):
    lines=[]
    current=''
    for word in s.split():
        if current and len(current)+len(word)+1>limit:
            lines.append(current);current=word
        else:current=(current+' '+word).strip()
    if current:lines.append(current)
    return '\n'.join(lines)

class DocumentaryScene(Scene):
    offset=0

    def setup(self):
        self.L=LAYOUT
        self.body=VGroup()
        self.caption=None
        self.heading=None
        self.brand=text('양자역학의 시작   /   1900',x=0 if self.L.portrait else -4.9,y=self.L.brand_y,size=18,color=MUTED)
        self.add(self.brand)
        w=7.6 if self.L.portrait else 14.4
        y=6.65 if self.L.portrait else 3.5
        self.add(Line(p(-w/2,y),p(w/2,y),color=MUTED,stroke_width=1,stroke_opacity=.25))
        # A static phase indicator avoids visual jumps between independently rendered scenes.
        self.stage=text({0:'01  현상과 질문',24:'02  기존 설명의 한계',49:'03  새로운 계산',72:'04  남은 물리적 질문'}[self.offset],
                        x=0 if self.L.portrait else 4.7,y=-4.55 if self.L.portrait else self.L.brand_y,size=17,color=MUTED)
        self.add(self.stage)

    def to(self,global_target):
        remaining=global_target-self.offset-self.time
        if remaining < -.018:
            raise RuntimeError(f'Timing overrun: {self.offset+self.time:.3f} > {global_target}')
        frames=round(remaining*30)
        if frames>0:
            # Cairo's frozen-frame path floors duration/dt; avoid losing a frame to float error.
            self.wait((frames+1e-5)/30)

    def cue(self,index):
        sentence=SCRIPT['sentences'][index]
        self.to(sentence['start'])
        if self.caption:self.remove(self.caption)
        self.caption=text(wrap(sentence['text'],26 if self.L.portrait else 62),
                          y=self.L.caption_y,size=24 if self.L.portrait else 25,
                          width=7.6 if self.L.portrait else 14.1)
        self.add(self.caption)
        new=text(sentence['heading'],y=self.L.heading_y,size=33 if self.L.portrait else 34,
                 width=self.L.body_width)
        if self.heading:
            self.play(Transform(self.heading,new),run_time=.3)
        else:
            self.heading=new;self.play(FadeIn(new,shift=UP*.1),run_time=.4)

    def show(self,*objects,run_time=.8):
        self.body.add(*objects)
        self.play(*[FadeIn(o) for o in objects],run_time=run_time)

    def clear_body(self,run_time=.5):
        if len(self.body):self.play(FadeOut(self.body),run_time=run_time)
        self.body=VGroup()

    def context_metal(self):
        obj=VGroup(metal(width=2.65),text('뜨거운 물체',y=-.83,size=22,color=HEAT))
        return obj.move_to(self.L.context)

    def theory_panels(self):
        xl,xr=self.L.comparison_x
        panel_w=3.35 if self.L.portrait else 5.7
        left=VGroup(RoundedRectangle(width=panel_w,height=3,corner_radius=.16,color=OLD,stroke_width=1.4),
                    wave(width=panel_w-.45,color=DATA).shift(UP*.4),
                    wave(width=panel_w-.45,color=OLD,phase=PI/2).shift(UP*.4),
                    text('전자기파',y=-.85,size=27,color=DATA)).move_to(p(xl,.45))
        right=VGroup(RoundedRectangle(width=panel_w,height=3,corner_radius=.16,color=HEAT,stroke_width=1.4),
                     text('열과 에너지',y=-.85,size=27,color=HEAT)).move_to(p(xr,.45))
        dots=VGroup(*[Dot(p(xr+((i%4)-1.5)*(panel_w-.7)/4,1.05+(i//4-.5)*.65),radius=.065,color=HEAT) for i in range(8)])
        note=text('열운동의 개념도 · 플랑크의 진동자 모형과 구별',y=-2.15,size=18,color=MUTED,width=self.L.body_width)
        return left,right,dots,note

    def graph_with_context(self,zoom=False,planck=False):
        graph=Spectrum(self.L,zoom)
        context=self.context_metal()
        key=legend(self.L,planck)
        self.body.add(graph,context,key)
        self.add(graph,context,key)
        return graph,context,key

    def graph_finish(self):
        graph,context,key=self.graph_with_context(planck=True)
        self.add(graph.old,graph.reference,graph.planck)
        self.body.add(graph.old,graph.reference,graph.planck)
        return graph,context,key

class ThermalDirection(DocumentaryScene):
    offset=0

    def construct(self):
        self.cue(0)
        cold=metal(width=4.3,hot=0).move_to(p(0,.8))
        self.show(cold,run_time=.4)
        red=metal(width=4.3,hot=.62).move_to(cold)
        # The hot end appears first, then the entire rod brightens.
        hot_edge=RoundedRectangle(width=.5,height=.6,corner_radius=.09,fill_color='#C93932',fill_opacity=.9,stroke_width=0).move_to(p(-1.8,.8))
        self.show(hot_edge,run_time=.25)
        self.play(Transform(cold,red),hot_edge.animate.stretch_to_fit_width(4.3).move_to(p(0,.8)).set_opacity(.15),run_time=1.1)
        final=metal(width=4.3).move_to(cold)
        self.play(Transform(cold,final),FadeOut(hot_edge),run_time=.9)
        self.body.remove(hot_edge)
        heat_arrow=VGroup(Arrow(p(-2,-1),p(2,-1),color=HEAT,buff=0),text('온도 상승',y=-1.45,size=25,color=HEAT))
        self.show(heat_arrow,run_time=.35)
        self.to(4)

        self.cue(1)
        self.play(FadeOut(heat_arrow),cold.animate.scale(.62).move_to(p(-2,.8)),run_time=.6)
        self.body.remove(heat_arrow)
        rays=VGroup(*[wave(width=2.3,color=HEAT if i%2 else MUTED,cycles=3+i*.5).rotate(a).move_to(p(.45, .8)+p(1.4*np.cos(a),1.4*np.sin(a)))
                      for i,a in enumerate([-.8,0,.8])])
        self.show(rays,run_time=.9)
        self.play(LaggedStart(*[r.animate.shift(RIGHT*.5).set_opacity(.35) for r in rays],lag_ratio=.15),run_time=1.2)
        thermal=text('열 → 빛',y=-1.8,size=40,color=HEAT)
        self.show(thermal,run_time=.5)
        self.to(9)

        self.cue(2)
        self.play(self.body.animate.set_opacity(.24),run_time=.5)
        question=text('온도만 알면\n빛도 계산할 수 있을까?',y=.2,size=44,width=self.L.body_width)
        self.show(question,run_time=.7)
        self.to(13)

        self.cue(3)
        self.clear_body(.45)
        context=self.context_metal()
        g=Spectrum(self.L)
        self.show(context,g,run_time=.8)
        # A spectrum analyser is schematic; spectral plot retains wavelength throughout.
        if self.L.portrait:
            prism=Triangle(color=DATA,fill_color=DATA,fill_opacity=.12).scale(.26).move_to(p(1.95,3.15))
            colors=['#9C77FF','#4775FF','#32C5FF','#82DDA4','#FFD166','#FF9F43','#F26765']
            beam=VGroup(*[Line(p(2.18,3.2),p(3.45,3.65-i*.15),color=c,stroke_width=2) for i,c in enumerate(colors)])
        else:
            prism=Triangle(color=DATA,fill_color=DATA,fill_opacity=.12).scale(.32).move_to(p(-1.6,.5))
            colors=['#9C77FF','#4775FF','#32C5FF','#82DDA4','#FFD166','#FF9F43','#F26765']
            beam=VGroup(*[Line(p(-1.35,.5),p(-.65,1.1-i*.2),color=c,stroke_width=2) for i,c in enumerate(colors)])
        self.show(prism,run_time=.3)
        self.body.add(beam);self.play(Create(beam),run_time=.6)
        hint=text('파장별로 빛을 분석',x=0 if self.L.portrait else -4.6,
                  y=-3.2 if self.L.portrait else -1.3,size=22,color=DATA)
        self.show(hint,run_time=.3)
        self.to(18)

        self.cue(4)
        self.clear_body(.4)
        left,right,dots,note=self.theory_panels()
        self.show(left,right,dots,note,run_time=.6)
        self.play(LaggedStart(*[d.animate.shift(p(.15*(-1)**i,.18*(-1)**(i//2))) for i,d in enumerate(dots)],lag_ratio=.04),run_time=1.1)
        plus=text('+',y=.4,size=34,color=MUTED)
        self.show(plus,run_time=.3)
        calculation=text('예측할 수 있을까?',y=-1.6,size=27,color=INK)
        self.show(calculation,run_time=.5)
        self.to(24)

class SpectrumDirection(DocumentaryScene):
    offset=24

    def construct(self):
        self.cue(5)
        # Continuous thematic hand-off: same metal, axes, colors and normalization.
        graph,context,key=self.graph_with_context()
        self.body.add(graph.old,graph.reference)
        self.play(Create(graph.old),run_time=1.15)
        self.play(Create(graph.reference),run_time=1.2)
        self.to(30)

        self.cue(6)
        zoom=Spectrum(self.L,zoom=True)
        # The y axis is explicitly rescaled, with numeric tick labels kept visible.
        old_pair=VGroup(graph.old,graph.reference)
        new_pair=VGroup(zoom.old,zoom.reference)
        self.play(Transform(graph,zoom),Transform(old_pair,new_pair),run_time=1.15)
        self.show(zoom.gap,run_time=.5)
        self.body.add(zoom.samples)
        self.play(LaggedStart(*[FadeIn(d,scale=.5) for d in zoom.samples],lag_ratio=.12),run_time=1.0)
        caption=text('5–12 μm · 세로축 확대',
                     x=0 if self.L.portrait else -4.6,y=-3.8 if self.L.portrait else -1.25,size=21,color=DATA,width=4)
        self.show(caption,run_time=.4)
        self.to(37)

        self.cue(7)
        self.play(FadeOut(zoom.gap),FadeOut(zoom.samples),FadeOut(caption),run_time=.4)
        self.body.remove(zoom.gap,zoom.samples,caption)
        full=Spectrum(self.L)
        self.play(Transform(graph,full),Transform(old_pair,VGroup(full.old,full.reference)),run_time=.75)
        name=text('Max Planck\n1900',x=0 if self.L.portrait else -4.6,
                  y=3.35 if self.L.portrait else .5,size=32,color=GOLD,width=3.9)
        self.play(FadeOut(context),FadeIn(name),run_time=.6)
        self.body.remove(context);self.body.add(name)
        self.body.add(full.planck)
        self.play(Create(full.planck),run_time=1.2)
        newkey=legend(self.L,True)
        self.play(Transform(key,newkey),run_time=.4)
        self.to(43)

        self.cue(8)
        self.clear_body(.5)
        # Keep the successful distribution in view while asking for its mechanism.
        tiny=VGroup(full.axes.copy(),full.planck.copy()).scale(.55).move_to(p(0,2 if self.L.portrait else 1.2))
        q=text('?',y=.25 if self.L.portrait else -.5,size=90,color=GOLD)
        self.show(tiny,q,run_time=.65)
        dots=VGroup(*[Dot(p((i-1.5)*1.3,-1.3 if self.L.portrait else -1.6),radius=.12,color=DATA) for i in range(4)])
        self.body.add(dots)
        self.play(LaggedStart(*[FadeIn(d,shift=DOWN*.25) for d in dots],lag_ratio=.18),run_time=1.1)
        self.show(text('에너지를 나누어 세는 방법',y=-2.25,size=26,color=MUTED),run_time=.5)
        self.to(49)

class EnergyDirection(DocumentaryScene):
    offset=49

    def construct(self):
        self.cue(9)
        xs=self.L.column_x
        oscillators=VGroup(*[oscillator(x,.15) for x in xs])
        labels=VGroup(*[text(f'진동자 {i+1}',x,-.85,20,MUTED) for i,x in enumerate(xs)])
        model=text('같은 진동수 · 에너지 분배의 개념적 모형',y=-2.6,size=19,color=MUTED,width=self.L.body_width)
        self.show(oscillators,labels,model,run_time=.75)
        bar_y=2.65 if self.L.portrait else 1.75
        reservoir=Rectangle(width=5.8,height=.42,color=HEAT,fill_color=HEAT,fill_opacity=.45).move_to(p(0,bar_y))
        label=text('분배할 전체 에너지',y=3.25 if self.L.portrait else 2.15,size=24,color=HEAT)
        self.show(reservoir,label,run_time=.5)
        heights=[.63,.98,.4,.79]
        if not self.L.portrait:heights=[h*.6 for h in heights]
        base=1.1 if self.L.portrait else .8
        continuous=VGroup(*[Rectangle(width=.48,height=h,color=HEAT,fill_color=HEAT,fill_opacity=.55).move_to(p(x,base+h/2))
                           for x,h in zip(xs,heights)])
        self.body.add(continuous)
        self.play(TransformFromCopy(reservoir,continuous),run_time=1.15)
        self.play(*[o[2].animate.shift(UP*.12) for o in oscillators],run_time=.4,rate_func=there_and_back)
        self.play(*[o[2].animate.shift(UP*.12) for o in oscillators],run_time=.4,rate_func=there_and_back)
        self.to(56)

        self.cue(10)
        self.play(FadeOut(continuous),FadeOut(reservoir),FadeOut(label),run_time=.4)
        self.body.remove(continuous,reservoir,label)
        bar=Rectangle(width=3.42,height=.38,color=HEAT,fill_color=HEAT,fill_opacity=.6).move_to(p(0,bar_y))
        row=VGroup(*[RoundedRectangle(width=.48,height=.38,corner_radius=.035,color=GOLD,fill_color=GOLD,fill_opacity=.8)
                    .move_to(p((j-2.5)*.57,bar_y)) for j in range(6)])
        self.show(bar,run_time=.25)
        self.play(ReplacementTransform(bar,row),run_time=.7)
        self.body.remove(bar);self.body.add(row)
        labels2=VGroup(*[text(f'진동자 {i+1}',x,-1.95,20,MUTED) for i,x in enumerate(xs)])
        self.play(oscillators.animate.shift(DOWN*1.05),Transform(labels,labels2),run_time=.4)
        blocks=energy_tiles(self.L,[3,2,1,0],y=.05)
        self.play(ReplacementTransform(row,blocks),run_time=.65)
        self.body.remove(row);self.body.add(blocks)
        counts=count_labels(self.L,[3,2,1,0],y=-2.45)
        self.play(FadeOut(model),run_time=.2);self.body.remove(model)
        note=text('조각 6개 · 총량 일정 · 각 조각의 크기 동일',y=3.45 if self.L.portrait else 2.05,size=21,color=GOLD,width=self.L.body_width)
        self.show(counts,note,run_time=.35)
        for values in ([2,2,1,1],[0,1,3,2]):
            new=energy_tiles(self.L,values,y=.05)
            self.play(Transform(blocks,new),Transform(counts,count_labels(self.L,values,y=-2.45)),run_time=.7)
            self.wait(.25)
        unit=text('에너지 분배량의 기호 · 전자나 광자가 아님',y=-3.25 if self.L.portrait else -2.85,size=18,color=MUTED,width=self.L.body_width)
        self.show(unit,run_time=.25)
        self.to(63)

        self.cue(11)
        self.clear_body(.4)
        xl,xr=self.L.comparison_x
        small=wave(width=3,cycles=2,color=DATA).move_to(p(xl,1.3))
        fast=wave(width=3,cycles=5,color=DATA).move_to(p(xr,1.3))
        a=Rectangle(width=.6,height=.5,color=GOLD,fill_color=GOLD,fill_opacity=.8).move_to(p(xl,-.1))
        b=Rectangle(width=1.5,height=.5,color=GOLD,fill_color=GOLD,fill_opacity=.8).move_to(p(xr,-.1))
        self.show(small,fast,text('낮은 진동수',xl,2.1,24,DATA),text('높은 진동수',xr,2.1,24,DATA),a,b,run_time=.6)
        self.show(text('ε = hν',y=-1.45,size=46,color=GOLD),
                  text('같은 진동수에서는 같은 크기의 단위',y=-2.5,size=22,color=MUTED,width=self.L.body_width),run_time=.4)
        self.to(67)

        self.cue(12)
        self.clear_body(.4)
        g,context,key=self.graph_with_context(planck=True)
        dashed=DashedVMobject(g.old,num_dashes=45)
        self.add(dashed,g.reference);self.body.add(dashed,g.reference,g.planck)
        self.play(Create(g.planck),run_time=1.25)
        self.play(Indicate(g.planck,color=GOLD,scale_factor=1.025),run_time=.75)
        match=text('관측 분포를 설명한 공식\n그래프: 플랑크 법칙으로 계산',
                   x=0 if self.L.portrait else -4.6,y=3.3 if self.L.portrait else -.35,size=25,color=GOLD,width=3.9)
        self.play(FadeOut(context),FadeIn(match),run_time=.5)
        self.body.remove(context);self.body.add(match)
        self.to(72)

class InterpretationDirection(DocumentaryScene):
    offset=72

    def construct(self):
        self.cue(13)
        xl,xr=self.L.comparison_x
        panels=VGroup(*[RoundedRectangle(width=3.35 if self.L.portrait else 5.5,height=2.4,corner_radius=.16,
                        color=MUTED,stroke_width=1.4).move_to(p(x,1.15)) for x in (xl,xr)])
        calc=VGroup(*[Rectangle(width=.3,height=.3,color=GOLD,fill_color=GOLD,fill_opacity=.7).move_to(p(xl+(j-1)*.45,1.3)) for j in range(3)])
        natural=wave(width=2.5,color=DATA).move_to(p(xr,1.3))
        self.show(panels,calc,natural,text('계산상의 단위',xl,.35,23,MUTED),text('자연의 실제 성질',xr,.35,23,MUTED),run_time=.75)
        q=text('?',y=-1.4,size=66,color=GOLD)
        self.show(q,text('성공한 계산 ≠ 물리적 의미의 확정',y=-2.65,size=24,color=MUTED,width=self.L.body_width),run_time=.6)
        self.to(77)

        self.cue(14)
        self.clear_body(.45)
        span=3.1 if self.L.portrait else 5
        line=Line(p(-span,1.65),p(span,1.65),color=OLD,stroke_width=6)
        self.show(line,text('연속적인 에너지값',y=2.4 if self.L.portrait else 2.1,size=25,color=OLD),run_time=.6)
        points=VGroup(*[Dot(p(x,.1),radius=.075,color=GOLD) for x in np.linspace(-span,span,9)])
        self.body.add(points)
        self.play(LaggedStart(*[FadeIn(d,scale=.5) for d in points],lag_ratio=.08),line.animate.set_opacity(.2),run_time=.9)
        self.show(text('일정한 단위로 세는 에너지값',y=-.8,size=28,color=GOLD,width=self.L.body_width),
                  text('에너지값의 개념도 · 공간이 끊어진다는 뜻이 아님',y=-2.1,size=19,color=MUTED,width=self.L.body_width),run_time=.5)
        self.to(82)

        self.cue(15)
        # Finish in a reusable physical image, not a title card or next-episode preview.
        self.clear_body(.35)
        tokens=VGroup(*[Rectangle(width=.25,height=.25,color=GOLD,fill_color=GOLD,fill_opacity=.75)
                       .move_to(p((i-2)*.6,1.65)) for i in range(5)])
        light=connecting_wave(self.L)
        self.show(tokens,run_time=.4)
        self.body.add(light);self.play(Create(light),run_time=.75)
        self.show(text('에너지를 연속적으로만 생각할 필요는 없다',y=-1.15,size=30,color=GOLD,width=self.L.body_width),run_time=.4)
        if os.environ.get('QUANTUM_ENDING','standalone')=='standalone':
            self.play(light.animate.set_stroke(opacity=.7),run_time=.4)
        # Join mode preserves the exact same framing and all spoken content.
        # The final one second is stable in both versions, ready for a matched cut.
        self.to(85)
        self.wait(1)
