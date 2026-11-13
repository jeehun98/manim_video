"""Six replaceable claims; exact user sentence times; separate responsive positions."""
import json,os
from pathlib import Path
import numpy as np
from manim import *
from quantum_series.shared.theme import configure,text,p,INK,MUTED,GOLD,BG
from quantum_series.shared.bohr import *
from quantum_series.episodes.ep04_bohr.layouts import AspectLayout
SCRIPT=json.loads((Path(__file__).parent/'script.json').read_text(encoding='utf-8'))
LAYOUT=AspectLayout(configure().portrait)
def wrap(s,limit):
    lines=[];line=''
    for word in s.split():
        if line and len(line)+len(word)+1>limit:lines.append(line);line=word
        else:line=(line+' '+word).strip()
    return '\n'.join(lines+[line])
class BohrScene(Scene):
    offset=0
    def setup(self):
        self.L=LAYOUT;self.body=VGroup();self.caption=None;self.heading=None
        self.add(text('양자역학의 발견  /  1913 · Niels Bohr',y=self.L.brand_y,size=18,color=MUTED))
        self.add(Line(p(-3.8 if self.L.portrait else -7.2,6.65 if self.L.portrait else 3.5),p(3.8 if self.L.portrait else 7.2,6.65 if self.L.portrait else 3.5),color=MUTED,stroke_width=1,stroke_opacity=.3))
    def to(self,target):
        dt=target-self.offset-self.time
        if dt<-.018:raise RuntimeError(f'Timing overrun {self.offset+self.time} > {target}')
        frames=round(dt*30)
        if frames>0:self.wait((frames+1e-5)/30)
    def cue(self,i):
        s=SCRIPT['sentences'][i];self.to(s['start'])
        if self.caption:self.remove(self.caption)
        self.caption=text(wrap(s['text'],26 if self.L.portrait else 62),y=self.L.caption_y,size=24 if self.L.portrait else 25,width=7.6 if self.L.portrait else 14.1)
        self.add(self.caption)
        h=text(s['heading'],y=self.L.heading_y,size=32,width=self.L.body_width)
        if self.heading:self.play(Transform(self.heading,h),run_time=.3)
        else:self.heading=h;self.play(FadeIn(h),run_time=.3)
    def show(self,*objects,run_time=.5):
        self.body.add(*objects);self.play(*[FadeIn(o) for o in objects],run_time=run_time)
    def clear(self):
        if len(self.body):
            for o in self.body.get_family():o.clear_updaters()
            self.play(FadeOut(self.body),run_time=.3)
        self.body=VGroup()
    def note(self,s):return text(wrap(s,37 if self.L.portrait else 85),y=-3.9 if self.L.portrait else -2.7,size=17,color=MUTED,width=self.L.body_width)
    def info(self,s,color=INK):return text(s,*self.L.info[:2],size=29,color=color,width=7.1 if self.L.portrait else 6)
    def orbit(self,atom,seconds,radius=1.4,turns=1):
        a=ValueTracker(0);c=atom.center_point
        atom.electron.add_updater(lambda d:d.move_to(c+p(radius*np.cos(a.get_value()),radius*np.sin(a.get_value()))))
        self.play(a.animate.set_value(TAU*turns),run_time=seconds,rate_func=linear)
        atom.electron.clear_updaters()
    def gauge(self,fraction,color=LOSS):
        c=self.L.info+p(0,.3);w=3.5
        return VGroup(text('에너지',c[0],c[1]+.65,23,color),Rectangle(width=w,height=.28,color=MUTED,stroke_width=1).move_to(c),Rectangle(width=max(.02,w*fraction),height=.25,stroke_width=0,fill_color=color,fill_opacity=1).move_to(c+p(-w*(1-fraction)/2,0)))
    def radiation(self,point):
        waves=VGroup(*[Circle(radius=.2+i*.15,color=LOSS,stroke_width=1.4,stroke_opacity=.8-i*.15).move_to(point) for i in range(4)])
        self.body.add(waves);self.play(FadeIn(waves),run_time=.25);self.play(waves.animate.scale(2.5).set_opacity(0),run_time=.75);self.remove(waves);self.body.remove(waves)
class ChargeQuestionDirection(BohrScene):
    def construct(self):
        self.cue(0);c=self.L.atom
        atom=BohrAtom(c);atom.rings.set_stroke(opacity=0);self.show(atom)
        self.show(text('+',c[0],c[1]+.4,32,NUCLEUS),text('−',c[0]+1.4,c[1]+.35,32,ELECTRON),self.note('원자핵과 전자의 크기는 실제 축척 아님'))
        self.to(3);self.cue(1)
        self.show(Arrow(c+p(.25,0),c+p(.9,0),buff=0,color=GOLD),Arrow(c+p(1.2,-.3),c+p(.45,-.3),buff=0,color=GOLD),self.info('인력 ↔ 안정성',GOLD))
        self.to(7)
class ClassicalFailureDirection(BohrScene):
    offset=7
    def construct(self):
        self.cue(2);c=self.L.atom;atom=BohrAtom(c,False);atom.rings[0].set_stroke(opacity=0);atom.rings[2].set_stroke(opacity=0)
        self.show(atom,self.note('고전적 궤도 모형의 가정 · 실제 전자 경로 아님'));self.orbit(atom,2.3)
        self.to(11);self.cue(3)
        gauge=self.gauge(1);self.show(gauge);self.radiation(atom.electron.get_center());self.play(Transform(gauge,self.gauge(.65)),run_time=.7);self.orbit(atom,1.4)
        self.to(16);self.cue(4)
        theta=ValueTracker(0)
        atom.electron.add_updater(lambda d:d.move_to(c+p(1.4*np.cos(theta.get_value()),1.4*np.sin(theta.get_value()))))
        velocity=always_redraw(lambda:Arrow(atom.electron.get_center(),atom.electron.get_center()+p(-np.sin(theta.get_value()),np.cos(theta.get_value()))*.9,buff=.04,color=ELECTRON))
        accel=always_redraw(lambda:Arrow(atom.electron.get_center(),c,buff=.15,color=GOLD))
        self.show(velocity,accel,text('파랑: 속도 방향 / 금색: 중심 가속도',0 if self.L.portrait else 3.7,3.9 if self.L.portrait else 1.6,23,GOLD,width=7),run_time=.4)
        self.play(theta.animate.set_value(TAU*.8),run_time=3.5,rate_func=linear)
        atom.electron.clear_updaters();velocity.clear_updaters();accel.clear_updaters()
        self.to(21);self.cue(5)
        self.play(FadeOut(velocity),FadeOut(accel),FadeOut(self.body[-1]),run_time=.3)
        spiral=ParametricFunction(lambda t:c+p(1.4*(1-.87*t)*np.cos(TAU*3*t),1.4*(1-.87*t)*np.sin(TAU*3*t)),t_range=[0,1,.003],color=ELECTRON,stroke_width=2)
        self.show(spiral,run_time=.4)
        self.play(MoveAlongPath(atom.electron,spiral),Transform(gauge,self.gauge(.04)),atom.rings.animate.set_stroke(opacity=.2),run_time=4,rate_func=linear)
        self.radiation(c)
        self.to(28);self.cue(6);self.clear()
        stable=VGroup(Dot(c,radius=.15,color=NUCLEUS),Circle(radius=1.3,color=MUTED,fill_color=ALLOWED,fill_opacity=.08),text('H',c[0],c[1],58,INK))
        stable[1].move_to(c);stable[0].shift(DOWN*.65);self.show(stable,self.info('실제 관찰\n안정적인 원자',ALLOWED),self.note('안정성을 나타내는 기호 · 전자 궤도나 오비탈 아님'))
        self.to(32);self.cue(7);self.show(text('?',c[0],c[1]+1.9,52,GOLD));self.to(34)
class BohrPostulatesDirection(BohrScene):
    offset=34
    def construct(self):
        self.cue(8);c=self.L.atom;atom=BohrAtom(c)
        if not self.L.portrait:atom.scale(self.L.emphasis_scale,about_point=c)
        self.show(atom,self.info('1913\nNiels Bohr',GOLD),self.note('보어의 역사적 모형 · 궤도 반지름은 축척 비례 아님'))
        self.to(39);self.cue(9)
        self.play(FadeOut(self.body[1]),run_time=.3)
        candidates=VGroup(*[Circle(radius=r*self.L.emphasis_scale,color=CLASSICAL,stroke_width=1,stroke_opacity=.5).move_to(c) for r in np.linspace(.4,2.3,17)])
        self.show(candidates);self.play(atom.rings.animate.set_stroke(opacity=.2),run_time=.4)
        self.play(FadeOut(candidates),atom.rings.animate.set_stroke(opacity=1),run_time=1.4)
        self.show(self.info('허용된 궤도만 남는다',ALLOWED));self.play(Indicate(atom.rings,color=ALLOWED),run_time=1)
        self.to(46);self.cue(10);self.play(FadeOut(self.body[-1]),run_time=.25);g=self.gauge(.75,ALLOWED);self.show(g);self.orbit(atom,4.3,radius=1.4*self.L.emphasis_scale,turns=1.3)
        self.to(52);self.cue(11);self.clear()
        centers=[p(0,2),p(0,-1)] if self.L.portrait else [p(-3.4,.2),p(3.4,.2)]
        for center,color,label in zip(centers,[LOSS,ALLOWED],['고전 궤도 모형\n복사 · 에너지 감소','보어의 정상상태\n복사 없음 · 에너지 유지']):
            a=BohrAtom(center).scale(.5,about_point=center);a.rings.set_color(color)
            self.show(a,text(label,center[0],center[1]-1.55,23,color),run_time=.3)
        self.radiation(centers[0]+p(.7,0))
        self.to(55)
class HydrogenObservationDirection(BohrScene):
    offset=55
    def construct(self):
        self.cue(12);c=self.L.atom;atom=BohrAtom(c);self.show(atom)
        blank=Rectangle(width=self.L.spectrum_width,height=.65,color=MUTED).move_to(self.L.spectrum);self.show(blank,self.note('수소의 가시광 영역 · 파장에 따라 빛을 나눈다'))
        self.to(59);self.cue(13);self.play(FadeOut(atom),run_time=.3)
        tube=RoundedRectangle(width=.5,height=2.8,corner_radius=.17,color='#E384E8',fill_color='#B950AD',fill_opacity=.4).move_to(c)
        self.show(tube,text('수소 방전관',c[0],c[1]-1.9,24),Arrow(c+p(.55,0),self.L.spectrum+p(-2,0),color=GOLD,buff=.1))
        self.play(Indicate(tube,color='#EF9ADF'),run_time=1.5)
        self.to(65);self.cue(14);self.clear()
        upper=p(0,1.8) if self.L.portrait else p(0,1.0)
        lower=p(0,-1.1) if self.L.portrait else p(0,-1.3)
        width=6.6 if self.L.portrait else 10
        continuous=HydrogenSpectrum(upper,width,continuous=True);spectrum=HydrogenSpectrum(lower,width,observed=True)
        self.show(continuous,text('연속 스펙트럼',upper[0],upper[1]+1.15,25,MUTED))
        self.show(spectrum,text('수소의 선 스펙트럼',lower[0],lower[1]+1.15,25,ALLOWED),self.note('대표 관측 파장 위치 · NIST 자료의 약 410 / 434 / 486 / 656 nm'))
        self.play(LaggedStart(*[Indicate(line) for line in spectrum.lines.values()],lag_ratio=.25),run_time=1.8);self.to(71)
class EnergyTransitionsDirection(BohrScene):
    offset=71
    def construct(self):
        self.cue(15);c=self.L.atom+(UP*.6 if self.L.portrait else DOWN*.35)
        diagram=EnergyLevelDiagram(c,width=3.2,height=4.4 if self.L.portrait else 3.6)
        sp=HydrogenSpectrum(self.L.spectrum,self.L.spectrum_width)
        self.show(diagram,sp,self.note('수소의 에너지 준위 · 전이 화살표는 공간 이동이 아닌 상태 변화'))
        formula=text('Eₙ ≈ −13.6 / n² eV',0 if self.L.portrait else 3.7,4.35 if self.L.portrait else 1.7,26,GOLD)
        self.show(formula);self.to(76);self.cue(16)
        arrow=Arrow(diagram.point(3),diagram.point(2),color=GOLD,buff=.02)
        dot=Dot(diagram.point(3),radius=.09,color=ELECTRON);self.show(dot);self.play(GrowArrow(arrow),run_time=.7);self.body.add(arrow)
        self.play(FadeOut(dot),run_time=.25);dot.move_to(diagram.point(2));self.play(FadeIn(dot),run_time=.25)
        wave=photon(diagram.point(2)+RIGHT*.5,COLORS[3]);self.show(wave)
        label=text('ΔE = hν = hc / λ',0 if self.L.portrait else 3.7,-3.0 if self.L.portrait else 1.0,28,GOLD)
        self.show(label);self.play(TransformFromCopy(wave,sp.lines[3]),run_time=1)
        self.to(83);self.cue(17)
        for n in [4,5,6]:
            x=(n-4)*.55-.5
            arr=Arrow(diagram.point(n,x),diagram.point(2,x),buff=.015,color=COLORS[n],stroke_width=3)
            self.body.add(arr);self.play(GrowArrow(arr),run_time=.45)
            self.play(TransformFromCopy(arr,sp.lines[n]),run_time=.6)
        self.to(90)
        self.cue(18);self.clear()
        width=6.5 if self.L.portrait else 10
        top=p(0,1.9) if self.L.portrait else p(0,1)
        bottom=p(0,-.9) if self.L.portrait else p(0,-1.3)
        obs=HydrogenSpectrum(top,width,observed=True);calc=HydrogenSpectrum(bottom,width)
        self.show(obs,calc,run_time=.4)
        self.show(text('관측 · 대표 파장',0,top[1]+1,25,INK),text('보어 모형 · 계산',0,bottom[1]-1,25,ALLOWED),self.note('같은 선형 파장축 · 약 nm 단위에서 일치 / 미세구조 생략'),run_time=.35)
        connectors=VGroup(*[DashedLine(obs.lines[n].get_bottom(),calc.lines[n].get_top(),color=COLORS[n],stroke_width=1.5) for n in [3,4,5,6]])
        self.show(connectors);self.play(Indicate(calc,color=GOLD),run_time=.8);self.to(95)
class OpenQuestionDirection(BohrScene):
    offset=95
    def construct(self):
        self.cue(19);c=self.L.atom;atom=BohrAtom(c)
        if not self.L.portrait:atom.scale(self.L.emphasis_scale,about_point=c)
        self.show(atom,self.note('보어의 허용 궤도 · 크기는 축척 비례 아님').shift(DOWN*.6 if self.L.portrait else ORIGIN));self.play(Indicate(atom.rings,color=ALLOWED),run_time=1)
        self.to(98);self.cue(20)
        candidates=VGroup(*[DashedVMobject(Circle(radius=r*self.L.emphasis_scale,color=CLASSICAL,stroke_width=1).move_to(c),num_dashes=45) for r in [1.05,1.75]])
        self.show(candidates);self.play(FadeOut(candidates),run_time=.7);self.show(self.info('왜 이 상태들만?',GOLD));self.to(102)
        self.cue(21);self.play(atom.rings.animate.set_stroke(opacity=.3),run_time=1.2)
        self.show(text('설명한 것: 수소의 파장\n남은 것: 허용 상태의 이유',*(self.L.info+p(0,-.9))[:2],size=24,color=INK,width=6.6));self.to(108)
        self.cue(22)
        self.play(FadeOut(atom.rings),FadeOut(atom.electron),run_time=1)
        waves=VGroup(*[Arc(radius=r,start_angle=.2,angle=2.4,color=ALLOWED,stroke_opacity=.16,stroke_width=1.5).move_arc_center_to(c) for r in [.7,1.2,1.7]])
        self.show(waves,run_time=.5)
        # Suggest an unresolved wave description; never draw a completed orbital.
        self.play(waves.animate.rotate(.15,about_point=c),run_time=1)
        if os.environ.get('QUANTUM_ENDING')=='standalone':self.play(waves.animate.set_stroke(opacity=.09),run_time=.5)
        self.to(112);self.to(113)
