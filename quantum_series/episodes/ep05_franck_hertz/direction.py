"""Six independent claims sharing fixed electrode geometry and exact sentence timing."""
import json,os
from pathlib import Path
from manim import *
from quantum_series.shared.theme import configure,text,p,INK,MUTED,GOLD
from quantum_series.shared.chapter_scene import ChapterScene
from quantum_series.shared.bohr import BohrAtom
from quantum_series.episodes.ep05_franck_hertz.layouts import AspectLayout
from quantum_series.episodes.ep05_franck_hertz.apparatus import *
from quantum_series.episodes.ep05_franck_hertz.experiment_model import *
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
L=AspectLayout(configure().portrait)
class FHScene(ChapterScene):
    script=DATA;layout=L;brand='양자역학의 발견  /  1914 · Franck–Hertz'
    def tube(self):
        tube=FranckHertzTube(self.L.tube);self.show(tube);return tube
    def stream(self,tube,count=4,blocked=0,run_time=2):
        dots=VGroup(*[tube.electron((i-(count-1)/2)*.15) for i in range(count)])
        self.body.add(dots);self.add(dots)
        animations=[]
        for i,dot in enumerate(dots):
            y=dot.get_y();x0=tube.cathode[0]+.12;xg=tube.grid[0];xc=tube.collector[0]
            # In the retarding gap the x(t) parabola decelerates; blocked electrons turn before the collector.
            def travel(obj,a,i=i,y=y,x0=x0,xg=xg,xc=xc):
                if a<.65:x=x0+(xg-x0)*(a/.65)**1.4
                else:
                    q=(a-.65)/.35
                    x=xg+((xc-xg)*(.5*4*q*(1-q)) if i<blocked else (xc-xg)*(1-(1-q)**1.4))
                obj.move_to(p(x,y))
            animations.append(UpdateFromAlphaFunc(dot,travel))
        self.play(*animations,run_time=run_time,rate_func=linear)
        self.play(FadeOut(dots),run_time=.15);self.body.remove(dots)
    def plot(self):
        graph=CurrentVoltagePlot(self.L.plot);self.show(graph);return graph
    def trace(self,graph,lo,hi,seconds=1.4):
        curve=graph.curve(lo,hi);dot=Dot(graph.point(lo),radius=.06,color=ELECTRON)
        self.body.add(curve,dot);self.add(dot)
        self.play(Create(curve),UpdateFromAlphaFunc(dot,lambda d,a:d.move_to(graph.point(lo+(hi-lo)*a))),run_time=seconds,rate_func=linear)
        self.remove(dot);self.body.remove(dot)
    def delta_label(self,y=None):
        return text('ΔE ≈ 4.9 eV',0 if self.L.portrait else 3.6,(-3.1 if self.L.portrait else -1.65) if y is None else y,30,GOLD)
class VoltageQuestionDirection(FHScene):
    def construct(self):
        self.cue(0);c=self.L.zoom
        dot=Dot(c+LEFT*2,radius=.08,color=ELECTRON);bar=energy_bar(1,self.L.info)
        self.show(dot,bar,text('ΔK = eΔU',c[0],c[1]+1.1,30,GOLD),self.note('에너지는 eV, 가속 전위차는 V로 구분'))
        self.play(dot.animate.move_to(c+RIGHT*1.7),Transform(bar,energy_bar(4.5,self.L.info)),run_time=1.3,rate_func=rate_functions.ease_in_quad)
        self.to(3);self.cue(1);self.clear_body()
        graph=self.plot();expected=DashedVMobject(graph.axes.plot(lambda u:.05+.06*u,x_range=[0,18],color=MUTED),num_dashes=40)
        self.show(expected,text('예상',*(self.L.plot+p(-1,0))[:2],size=24,color=MUTED));self.to(6)
class ApparatusDirection(FHScene):
    offset=6
    def construct(self):
        self.cue(2);tube=self.tube()
        name=text('James Franck · Gustav Hertz',0 if self.L.portrait else 3.6,-1.7 if self.L.portrait else .2,26,GOLD,width=6)
        self.show(name,self.note('수은 증기 실험관 · 전극과 입자의 크기는 개념도'));self.to(12)
        self.cue(3);self.stream(tube,5,run_time=2.5);self.to(17)
        self.cue(4);self.play(FadeOut(name),run_time=.2)
        self.show(self.info('검출부에 도달한 전자\n→ 검출 전류',ELECTRON))
        for i in range(2):
            self.stream(tube,4,run_time=1.6);self.play(Flash(tube.collector,color=ELECTRON,flash_radius=.18),run_time=.3)
        self.to(24)
class CurrentDropsDirection(FHScene):
    offset=24
    def construct(self):
        self.cue(5);tube=self.tube();graph=self.plot();self.show(self.note('전류–전압 형태를 설명하는 개념도 · 실측 데이터 아님'),run_time=.2)
        self.trace(graph,0,4.8,1.2);self.to(27)
        self.cue(6);self.trace(graph,4.8,6,1.5);self.show(text('U ↑    I ↓',self.L.tube[0],self.L.tube[1],26,LOSS));self.to(31)
        self.cue(7);self.trace(graph,6,10.9,2.6);self.to(36)
        self.cue(8);self.trace(graph,10.9,18,1.3);self.show(graph.intervals(),run_time=.3);self.to(40)
        self.cue(9);self.show(text('?',*graph.point(10.9)[:2],size=40,color=GOLD),run_time=.3);self.to(42)
class ExcitationCollisionDirection(FHScene):
    offset=42
    def construct(self):
        self.cue(10);c=self.L.zoom;atom=MercuryAtom(c,.65);electron=Dot(c+LEFT*2.2,radius=.09,color=ELECTRON)
        levels=MercuryEnergyLevels(self.L.levels,width=3.4,gap=1.45)
        gauge_center=p(0,3.7) if self.L.portrait else p(-3.5,1.45)
        gauge=energy_bar(3,gauge_center)
        self.show(atom,electron,levels,gauge,self.note('수은의 대표 들뜸 · 내부 상태 변화이며 원자의 공간 이동 아님'))
        self.play(electron.animate.move_to(c+LEFT*.8),run_time=1.3,rate_func=linear);self.to(46)
        self.cue(11);self.play(electron.animate.move_to(c+p(.9,.4)),run_time=1.3,rate_func=linear)
        no=text('3.0 eV < 4.9 eV · 들뜸 없음',0 if self.L.portrait else 3.6,-3 if self.L.portrait else -1.65,24,ELECTRON)
        self.show(no);self.to(52)
        self.cue(12);self.play(electron.animate.move_to(c+LEFT*.85),Transform(gauge,energy_bar(4.9,gauge_center)),FadeOut(no),run_time=1.4)
        delta=self.delta_label();self.show(delta);self.to(57)
        self.cue(13);self.play(Transform(gauge,energy_bar(5.2,gauge_center)),run_time=.5)
        self.play(electron.animate.move_to(c+LEFT*.1),run_time=.7,rate_func=linear)
        up=levels.transition();state=Dot(levels.low,radius=.09,color=GOLD)
        self.show(state);self.play(GrowArrow(up),Indicate(atom,color=GOLD),run_time=.7);self.body.add(up)
        self.play(state.animate.move_to(levels.high),Transform(gauge,energy_bar(.3,gauge_center)),run_time=.7)
        self.show(text('전자 → 수은 내부 에너지',c[0],c[1]-1.15,22,GOLD));self.to(64)
        self.cue(14);self.play(Indicate(gauge,color=LOSS),run_time=.5)
        self.show(text('5.2 − 4.9 = 0.3 eV',0 if self.L.portrait else -3.5,3.0 if self.L.portrait else -1.3,24,LOSS),run_time=.2)
        # v scales with sqrt(K): 0.3 / 5.2 eV gives speed ratio about 0.24.
        self.play(electron.animate.move_to(c+RIGHT*.45),run_time=1.5,rate_func=linear);self.to(67)
class RetardingDetectionDirection(FHScene):
    offset=67
    def construct(self):
        self.cue(15);tube=self.tube()
        gap=Rectangle(width=1.05,height=1.65,color=RETARD,fill_color=RETARD,fill_opacity=.08).move_to((tube.grid+tube.collector)/2)
        self.show(gap,self.note('감속 전위차는 전기적 장벽 · 실제 금속 벽 아님'))
        barrier=VGroup(Line(p(-2,-1.3),p(-.5,-1.3),color=MUTED),Line(p(-.5,-1.3),p(.5,-.5),color=RETARD),Line(p(.5,-.5),p(2,-.5),color=RETARD)) if self.L.portrait else VGroup(Line(p(1,1),p(3,1),color=MUTED),Line(p(3,1),p(4,1.8),color=RETARD),Line(p(4,1.8),p(6,1.8),color=RETARD))
        self.show(barrier,self.info('검출부 앞 감속 전위차\n예: Uᵣ = 0.8 V',RETARD));self.to(73)
        self.cue(16);self.play(FadeOut(barrier),FadeOut(self.body[-1]),run_time=.25)
        self.show(self.info('충돌 후 K = 0.3 eV\n장벽 0.8 eV보다 작으면 반전',LOSS))
        self.stream(tube,6,blocked=4,run_time=2.7)
        self.show(text('도달 비율 감소 · 전류는 0이 아님',0 if self.L.portrait else 3.6,-1.55 if self.L.portrait else -1.5,23,ELECTRON));self.to(80)
        self.cue(17);self.clear_body();tube=self.tube()
        self.show(self.note('재가속은 음극–격자 구간에서만 · 경로·충돌 횟수는 대표 사례'))
        dot=tube.electron();self.show(dot)
        # Two separated inelastic events before the grid; accelerate only in the remaining positive-voltage region.
        for x in [-1.2,.8]:
            at=tube.origin+p(x,0)
            self.play(dot.animate.move_to(at),run_time=.7,rate_func=rate_functions.ease_in_quad)
            self.play(Flash(at,color=GOLD,flash_radius=.22),run_time=.3)
            self.play(dot.animate.shift(RIGHT*.12),run_time=.4,rate_func=linear)
        self.play(dot.animate.move_to(tube.grid),run_time=.7,rate_func=rate_functions.ease_in_quad)
        self.play(dot.animate.move_to(tube.collector),run_time=.65,rate_func=rate_functions.ease_out_quad)
        self.show(self.info('가속 → 들뜸 → 재가속\n다른 원자와 다시 충돌 가능',GOLD));self.to(87)
        self.cue(18);self.clear_body();graph=self.plot();self.show(graph.curve(),graph.intervals(),self.note('충돌 위치·횟수는 전자마다 다름 · 설명용 전류 곡선'))
        self.show(text('반복되는 에너지 전달',0 if self.L.portrait else -3.5,2.1 if self.L.portrait else .3,26,GOLD));self.to(91)
class DiscreteStatesDirection(FHScene):
    offset=91
    def construct(self):
        self.cue(19);c=self.L.zoom
        levels=MercuryEnergyLevels(c,width=3.7,gap=1.65);self.show(levels,self.delta_label(),self.note('수은의 대표 내부 전자 상태 두 개를 표시 · 다른 준위·탄성 충돌은 생략'))
        arrow=levels.transition();self.play(GrowArrow(arrow),run_time=.7);self.body.add(arrow)
        self.show(self.info('ΔU ≈ 4.9 V\n전자 한 개: eΔU ≈ 4.9 eV',GOLD).shift(UP*1.6 if self.L.portrait else ORIGIN));self.to(101)
        self.cue(20);self.clear_body();a,b=self.L.comparison
        bohr=BohrAtom(a).scale(.53,about_point=a);hg=MercuryEnergyLevels(b,width=3.5,gap=1.3)
        self.show(bohr,hg,text('수소 · 보어의 역사적 모형',a[0],a[1]-1.65,21,MUTED),text('수은 · 대표 상태 차이',b[0],b[1]-1.65,21,MUTED),self.note('수소와 수은은 서로 다른 원자 · 동일한 준위 간격을 뜻하지 않음'))
        self.to(105);self.cue(21);self.clear_body()
        c=self.L.zoom;levels=MercuryEnergyLevels(c,width=3.7,gap=1.65);state=Dot(levels.high,radius=.09,color=GOLD)
        self.show(levels,state,self.note('자외선은 눈에 보이지 않음 · 보라색 파동은 식별용'))
        down=levels.transition(False);self.play(GrowArrow(down),run_time=.6);self.body.add(down)
        self.play(state.animate.move_to(levels.low),run_time=.8)
        wavecenter=p(.6,-1.5) if self.L.portrait else p(2.6,.4)
        self.show(uv_wave(wavecenter),self.delta_label())
        self.show(text('약 254 nm · 자외선 (UV)',0 if self.L.portrait else 3.6,-2.5 if self.L.portrait else -.7,27,UV));self.to(113)
        self.cue(22);self.clear_body();a,b=self.L.comparison
        upview=MercuryEnergyLevels(a,3.5,1.35);downview=MercuryEnergyLevels(b,3.5,1.35)
        self.show(upview,downview);arrows=VGroup(upview.transition(True),downview.transition(False));self.play(*[GrowArrow(ar) for ar in arrows],run_time=.65);self.body.add(arrows)
        self.show(text('충돌로 에너지 흡수',a[0],a[1]-1.25,23,ELECTRON),text('빛으로 에너지 방출',b[0],b[1]-1.25,23,UV),self.delta_label(-3.1 if self.L.portrait else -2.05))
        self.to(119);self.cue(23);self.clear_body()
        levels=MercuryEnergyLevels(self.L.zoom,width=4.2,gap=1.8)
        self.show(levels,self.info('왜 이 상태들만?',GOLD),self.note('불연속적인 내부 상태 · 허용되는 에너지의 근본적인 이유는?'),run_time=.4)
        if os.environ.get('QUANTUM_ENDING')=='standalone':self.play(levels.animate.set_stroke(opacity=.6),run_time=.3)
        self.to(121);self.to(122)
