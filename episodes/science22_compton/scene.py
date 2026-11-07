"""Compton effect: independent portrait chapters, user timing, shared quantum palette."""
import json, os, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from manim import *
from quantum_series.shared.theme import configure, text, p, BG, INK, MUTED, DATA, GOLD, OLD, HEAT
from quantum_series.shared.components import wave
configure()
HERE=Path(__file__).resolve().parent
SCRIPT=json.loads((HERE/'script.json').read_text(encoding='utf-8'))

def wrapped(s,n=24):
    lines=[]; row=''
    for word in s.split():
        if len(row+' '+word)>n and row: lines.append(row); row=word
        else: row=(row+' '+word).strip()
    return '\n'.join(lines+[row])

def label(s,y=0,size=30,color=INK): return text(s,0,y,size,color,width=7.4)

class Chapter(Scene):
    section='hook'
    def construct(self):
        _,self.offset,self.end,title=next(s for s in SCRIPT['scenes'] if s[0]==self.section)
        self.add(text('과학 한조각',0,7.1,24,MUTED),label(title,5.65,34),Line(p(-3.7,4.9),p(3.7,4.9),color=MUTED,stroke_width=1))
        # A persistent mobject updater keeps Cairo from caching captions into
        # the static background of the current animation or wait.
        self.caption=VGroup().set_z_index(100)
        self.caption_key=None
        self.update_caption(self.caption,0)
        self.caption.add_updater(self.update_caption)
        self.add(self.caption)
        getattr(self,'draw_'+self.section)()
        self.to(self.end-self.offset)
        self.audit()
    def update_caption(self,mob,dt):
        t=self.time+self.offset
        index=next((i for i,(end,s) in enumerate(SCRIPT['sentences']) if t<end-1e-6),len(SCRIPT['sentences'])-1)
        if index!=self.caption_key:
            mob.remove(*mob.submobjects)
            mob.add(label(wrapped(SCRIPT['sentences'][index][1]),-6.0,28).set_z_index(100))
            self.caption_key=index
    def audit(self):
        caption_ids={id(obj) for obj in self.caption.get_family()}
        for mob in self.mobjects:
            for obj in mob.get_family():
                if isinstance(obj,Text) and obj.width:
                    assert obj.get_left()[0]>=-4.35 and obj.get_right()[0]<=4.35,(self.section,obj.text,'horizontal')
                    assert obj.get_bottom()[1]>=-7.55 and obj.get_top()[1]<=7.7,(self.section,obj.text,'vertical')
                    if id(obj) not in caption_ids:
                        assert obj.get_bottom()[1]>-4.75,(self.section,obj.text,'caption overlap')
    def play(self,*args,**kwargs):
        super().play(*args,**kwargs)
        self.audit()
    def to(self,t):
        remaining=t-self.time
        if remaining<-.017: raise ValueError((self.section,t,self.time))
        if remaining>1/60:self.wait(round(remaining*30)/30-1e-7)
    def comparison(self,cycles=4):
        a=wave(width=6.4,cycles=6,color=DATA).move_to(p(0,2.3))
        b=wave(width=6.4,cycles=cycles,color=GOLD).move_to(p(0,0))
        self.add(label('입사 X선 · λ',3.2,24,DATA),label('산란 X선 · λ′',.9,24,GOLD))
        self.play(Create(a),Create(b),run_time=.8)
        return a,b
    def geometry(self):
        e=Dot(p(0,0),radius=.2,color=GOLD)
        self.add(e,text('전자',0,-.6,24,GOLD))
        incoming=Arrow(p(-3.3,0),p(-.3,0),buff=0,color=DATA)
        self.play(GrowArrow(incoming),run_time=.5)
        return e
    def draw_hook(self):
        self.add(label('정지질량 0',3,36,DATA),label('운동량 ?',-2.5,42,GOLD))
        e=self.geometry()
        w=wave(width=1.7,cycles=3,color=DATA).move_to(p(-2.6,0))
        self.play(w.animate.shift(RIGHT*1.3),run_time=1)
    def draw_experiment(self):
        self.add(label('Arthur H. Compton',3.7,26,MUTED))
        source=RoundedRectangle(width=1.5,height=1,corner_radius=.12,color=DATA).move_to(p(-2.7,1))
        target=Rectangle(width=.6,height=1.8,color=GOLD,fill_color=GOLD,fill_opacity=.16).move_to(p(0,1))
        self.play(Create(source),Create(target),FadeIn(text('X선',-2.7,1,25,DATA)),FadeIn(text('흑연',0,-.45,26,GOLD)),run_time=.8)
        self.play(Create(wave(width=1.7,cycles=5,color=DATA).move_to(p(-1.4,1))),run_time=1)
        self.to(6)
        self.play(FadeIn(label('가시광선',-1.6,25,OLD)),Create(wave(width=5.6,cycles=3,color=OLD).move_to(p(0,-2.3))),run_time=.6)
        self.play(FadeIn(label('X선 · 훨씬 짧은 파장',-3.2,25,DATA)),Create(wave(width=5.6,cycles=12,color=DATA).move_to(p(0,-3.9))),run_time=.7)
        self.to(11)
        rays=VGroup(*[Arrow(p(.3,1),p(2.8*np.cos(a),1+2.8*np.sin(a)),buff=0,color=DATA,stroke_width=3) for a in [-.7,0,.7]])
        self.play(LaggedStart(*[GrowArrow(r) for r in rays],lag_ratio=.3),run_time=1.5)
    def draw_shift(self):
        a,b=self.comparison(6)
        self.play(Transform(b,wave(width=6.4,cycles=4,color=GOLD)),run_time=1.5)
        self.add(label('일부는 λ′ > λ',-1.1,34,GOLD))
        self.to(5)
        bars=VGroup()
        for x,angle in zip([-2.4,0,2.4],[45,90,135]):
            h=1.0*(1-np.cos(angle*DEGREES))
            bar=Rectangle(width=.65,height=h,color=GOLD,fill_opacity=.7).move_to(p(x,-4.0+h/2))
            bars.add(bar)
            self.add(text(str(angle)+'°',x,-4.4,23,MUTED))
        self.play(LaggedStart(*[GrowFromEdge(b,DOWN) for b in bars],lag_ratio=.3),run_time=1)
        self.add(label('산란 각도 ↑  →  파장 변화 ↑',-2,25))
    def draw_energy(self):
        a,b=self.comparison(6)
        self.add(label('E = hc / λ',-1.4,42),label('광자 하나의 에너지',-2.3,23,MUTED))
        bar=Rectangle(width=5,height=.4,color=DATA,fill_opacity=.8).move_to(p(0,-3.1))
        self.add(bar)
        self.play(Transform(b,wave(width=6.4,cycles=4,color=GOLD)),bar.animate.stretch_to_fit_width(5*4/6).set_color(GOLD),run_time=2)
        self.to(4)
        self.play(FadeIn(label('에너지는 어디로 갔을까?',-4.1,29,GOLD)),run_time=.6)
    def draw_classical(self):
        self.add(label('전자기파 → 전자 진동 → 재방출',3.4,25),label('톰슨 산란 · 정지 자유전자 근사',-3.7,23,MUTED))
        e=self.geometry()
        self.add(wave(width=2.8,cycles=4,color=DATA).move_to(p(-1.9,0)))
        self.to(6)
        self.play(e.animate.shift(UP*.35),rate_func=there_and_back,run_time=1)
        self.play(Create(wave(width=2.8,cycles=4,color=OLD).move_to(p(1.9,0))),run_time=1)
        for r in [.6,1.1,1.6]:
            self.play(Create(Arc(radius=r,start_angle=-.7,angle=1.4,color=OLD)),run_time=.4)
        self.to(13)
        self.play(FadeIn(label('f′ = f',-1.8,45,OLD)),run_time=.6)
        self.to(19)
        self.play(FadeIn(label('λ′ = λ',-2.8,42,OLD)),run_time=.6)
    def draw_mismatch(self):
        self.add(label('고전 예측',3.5,27,OLD),label('실험에서 관찰된 성분',-.25,27,GOLD))
        for cy,observed in [(2,False),(-1.8,True)]:
            ax=Axes(x_range=[0,5,1],y_range=[0,1.2,.5],x_length=6.3,y_length=1.9,tips=False,axis_config={'color':MUTED,'include_ticks':False}).move_to(p(0,cy))
            curve=ax.plot(lambda x:np.exp(-((x-1.5)/.19)**2)+(.85*np.exp(-((x-3.3)/.22)**2) if observed else 0),x_range=[.1,4.9,.025],color=GOLD if observed else OLD)
            self.add(ax,text('λ',*ax.c2p(1.5,-.16)[:2],size=24,color=DATA))
            self.play(Create(curve),run_time=.8)
            if observed:self.add(text('λ′',*ax.c2p(3.3,-.16)[:2],size=24,color=GOLD))
        self.add(label('파장 →  ·  스펙트럼 개념도',-3.6,22,MUTED),label('이동한 성분을 설명해야 한다',-4.35,27,GOLD))
    def draw_photon(self):
        w=wave(width=6.2,cycles=7,color=DATA).move_to(p(0,1.5))
        self.play(Create(w),run_time=1)
        self.to(3)
        dots=VGroup(*[Dot(p(x,1.5),radius=.11,color=DATA) for x in np.linspace(-3,3,9)])
        self.play(ReplacementTransform(w,dots),run_time=1)
        self.add(label('광자 · photon',3,32,DATA),label('E = hf',-.4,44),label('p = h / λ',-1.9,44,GOLD),label('정지질량이 0이어도 운동량을 갖는다',-3.6,25))
    def draw_billiards(self):
        self.add(RoundedRectangle(width=7,height=4,corner_radius=.25,color=MUTED).move_to(p(0,.4)),label('에너지 전달의 비유',3.3,26,MUTED))
        a=Dot(p(-2.6,.5),radius=.3,color=DATA); b=Dot(p(0,.5),radius=.3,color=GOLD)
        self.add(a,b)
        self.play(a.animate.move_to(p(-.6,.5)),run_time=1.6,rate_func=linear)
        self.play(a.animate.move_to(p(.8,1.9)),b.animate.move_to(p(1.7,-1.2)),run_time=2,rate_func=linear)
        self.to(5)
        self.play(FadeIn(label('처음 움직이던 공 → 정지해 있던 공',-2.8,27)),FadeIn(label('운동에너지 전달',-3.8,34,GOLD)),run_time=.7)
    def draw_collision(self):
        e=self.geometry()
        photon=Dot(p(-3,0),radius=.12,color=DATA)
        self.add(label('광자 + 전자',3.5,34),label('광자는 언제나 빛의 속력 c로 이동',-4.5,22,MUTED))
        self.play(FadeIn(photon),run_time=.5)
        self.to(5)
        self.play(photon.animate.move_to(p(0,0)),run_time=1.2,rate_func=linear)
        # λ=0.071 nm and θ=60°; exact relativistic momentum-vector direction.
        ratio=1/(1+2.42631023867/71*(1-np.cos(PI/3)))
        recoil=np.array([1-ratio*.5,-ratio*np.sin(PI/3),0]); recoil/=np.linalg.norm(recoil)
        outgoing=Arrow(ORIGIN,p(1.6,2.77),buff=0,color=DATA)
        electron_path=Arrow(ORIGIN,recoil*2.8,buff=0,color=GOLD)
        self.add(outgoing,electron_path)
        self.play(photon.animate.move_to(p(1.6,2.77)),e.animate.move_to(recoil*2.4),run_time=1.6,rate_func=linear)
        self.add(label('에너지 · 운동량 전달',-2.8,28,GOLD))
        self.to(12)
        self.play(FadeIn(label('E′ < E     λ′ > λ',-3.65,36,DATA)),run_time=.7)
    def draw_prediction(self):
        self.add(label('에너지 보존',3.8,24,MUTED),label('E = E′ + Kₑ',2.9,36),label('운동량 보존',1.8,24,MUTED),label('p⃗ = p⃗′ + p⃗ₑ',.9,34))
        self.to(4)
        formula=label('Δλ = h/(mₑc) · (1 − cos θ)',-.6,32,GOLD)
        self.play(FadeIn(formula),run_time=.8)
        ax=Axes(x_range=[0,180,45],y_range=[0,5,1],x_length=5.8,y_length=2.5,tips=False,axis_config={'color':MUTED,'include_ticks':False}).move_to(p(0,-2.8))
        curve=ax.plot(lambda x:2.42631023867*(1-np.cos(x*DEGREES)),x_range=[0,180,1],color=DATA)
        self.add(ax,text('0°',*ax.c2p(0,-.4)[:2],size=20,color=MUTED),text('180°',*ax.c2p(180,-.4)[:2],size=20,color=MUTED),text('Δλ (pm)',-2.7,-1.1,20,MUTED))
        self.play(Create(curve),run_time=2)
        self.to(12)
        dots=VGroup(*[Dot(ax.c2p(x,2.42631023867*(1-np.cos(x*DEGREES))),radius=.07,color=GOLD) for x in [45,90,135]])
        self.play(FadeIn(dots),run_time=.5)
        self.add(label('각도 θ → · 점은 이론식 위의 설명용',-4.45,20,MUTED))
    def draw_meaning(self):
        self.add(label('파동으로 나타나는 성질',3.6,30,DATA),wave(width=5.8,cycles=5,color=DATA).move_to(p(0,2.5)),label('간섭 · 회절',1.5,26,DATA))
        self.add(label('입자로 주고받는 것',-.2,30,GOLD),Dot(p(-2,-1.5),radius=.16,color=DATA),Dot(p(.4,-1.5),radius=.23,color=GOLD),Arrow(p(-1.7,-1.5),p(0,-1.5),color=DATA),Arrow(p(.6,-1.5),p(2,-2.5),color=GOLD),label('에너지 · 운동량',-3.3,30,GOLD))
        self.to(6)
        closing=label('빛은 두 성질을 모두 드러낸다',-4.3,30)
        self.play(FadeIn(closing),run_time=.7)
        self.to(11)
        # Answer the opening question inside the existing closing narration interval.
        self.play(Transform(closing,label('정지질량 0, 그래도 운동량은 있다',-4.3,28,GOLD)),run_time=.7)

class ComptonHook(Chapter): section='hook'
class ComptonExperiment(Chapter): section='experiment'
class ComptonShift(Chapter): section='shift'
class ComptonEnergy(Chapter): section='energy'
class ComptonClassical(Chapter): section='classical'
class ComptonMismatch(Chapter): section='mismatch'
class ComptonPhoton(Chapter): section='photon'
class ComptonBilliards(Chapter): section='billiards'
class ComptonCollision(Chapter): section='collision'
class ComptonPrediction(Chapter): section='prediction'
class ComptonMeaning(Chapter): section='meaning'
