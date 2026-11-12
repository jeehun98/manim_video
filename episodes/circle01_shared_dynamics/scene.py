"""Compton effect: independent portrait chapters, user timing, shared quantum palette."""
import json, os, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from manim import *
from quantum_series.shared.theme import configure, text, p, BG, INK, MUTED, DATA, GOLD, OLD, HEAT

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
    section='geometry'
    def construct(self):
        _,self.offset,self.end,title=next(s for s in SCRIPT['scenes'] if s[0]==self.section)
        self.add(text('서로 다른 현상 · 같은 수학',0,7.1,24,MUTED),label(title,5.65,34),Line(p(-3.7,4.9),p(3.7,4.9),color=MUTED,stroke_width=1))
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
            mob.become(VGroup(label(wrapped(SCRIPT['sentences'][index][1]),-6.0,28).set_z_index(100)))
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

TEAL='#48D6C6'; BLUE='#61A8FF'; PURPLE='#C49BFF'; ORANGE='#FFB454'

def eq(s,y=3.6,size=36,color=INK):return label(s,y,size,color)

def axes(center,r=2.15,x='x',y='y'):
    cx,cy=center
    return VGroup(Line(p(cx-r-.25,cy),p(cx+r+.25,cy),color=MUTED,stroke_width=1.5),Line(p(cx,cy-r-.25),p(cx,cy+r+.25),color=MUTED,stroke_width=1.5),text(x,cx+r+.35,cy-.3,25,BLUE),text(y,cx-.55,cy+r+.32,25,PURPLE))

def orbit(t,center=(0,0),r=2.15,projection=False,tangent=False):
    c=p(*center)
    def state():return c+r*p(np.cos(t.get_value()),np.sin(t.get_value()))
    g=VGroup(Circle(r,color=TEAL,stroke_width=3).move_to(c),always_redraw(lambda:Line(c,state(),color=TEAL,stroke_opacity=.5)),always_redraw(lambda:Dot(state(),radius=.105,color=ORANGE)))
    if projection:
        g.add(always_redraw(lambda:DashedLine(state(),p(state()[0],c[1]),color=PURPLE)),always_redraw(lambda:Line(c,p(state()[0],c[1]),color=BLUE,stroke_width=6)),always_redraw(lambda:Line(p(state()[0],c[1]),state(),color=PURPLE,stroke_width=6)))
    if tangent:g.add(always_redraw(lambda:Arrow(state(),state()+.85*p(-np.sin(t.get_value()),np.cos(t.get_value())),buff=0,color=ORANGE,stroke_width=4)))
    return g

def spring(t,y=1.8):
    def blockpos():return .9+1.45*np.cos(t.get_value())
    wall=Line(p(-3.35,y-.7),p(-3.35,y+.7),color=MUTED,stroke_width=6)
    def zig():
        end=blockpos()-.4
        points=[p(-3.35,y),p(-3.05,y)]+[p(-3.05+(end+2.85)*i/16,y+(.22 if i%2 else -.22)) for i in range(17)]+[p(end,y)]
        return VMobject(color=BLUE,stroke_width=3).set_points_as_corners(points)
    return VGroup(wall,Line(p(-3.5,y-.52),p(3.2,y-.52),color=MUTED),DashedLine(p(.9,y-.7),p(.9,y+.8),color=MUTED),always_redraw(zig),always_redraw(lambda:Square(.8,color=BLUE,fill_opacity=.3).move_to(p(blockpos(),y))),text('평형 위치',.9,y-1,22,MUTED))

def circuit(t,y=1.9):
    # Capacitor at left, inductor at right; the signed arrow denotes I=dq/dt.
    g=VGroup(Line(p(-2.1,y+1),p(2.1,y+1),color=MUTED),Line(p(-2.1,y-1),p(2.1,y-1),color=MUTED),Line(p(-2.1,y+1),p(-2.1,y+.16),color=MUTED),Line(p(-2.1,y-.16),p(-2.1,y-1),color=MUTED),Line(p(-2.65,y+.16),p(-1.55,y+.16),color=BLUE,stroke_width=5),Line(p(-2.65,y-.16),p(-1.55,y-.16),color=BLUE,stroke_width=5))
    coil=ParametricFunction(lambda u:p(2.1+.23*np.sin(8*PI*u),y+1-2*u),t_range=[0,1],color=PURPLE,stroke_width=4)
    g.add(coil,text('C',-3,y,28,BLUE),text('L',2.85,y,28,PURPLE))
    g.add(always_redraw(lambda:VGroup(text('+' if np.cos(t.get_value())>=0 else '−',-2.85,y+.45,25,BLUE),text('−' if np.cos(t.get_value())>=0 else '+',-2.85,y-.45,25,BLUE)).set_opacity(abs(np.cos(t.get_value())))))
    def current():
        v=-np.sin(t.get_value());length=max(.025,1.5*abs(v))
        return Arrow(p(length/2*np.sign(v),y+1),p(-length/2*np.sign(v),y+1),buff=0,color=ORANGE,stroke_width=5).set_opacity(min(1,abs(v)*3))
    g.add(always_redraw(current),text('I = dq/dt',0,y+1.45,24,ORANGE))
    return g

class CircleGeometry(Chapter):
    section='geometry'
    def draw_geometry(self):
        t=ValueTracker(.35);self.add(axes((0,.3)))
        g=orbit(t,(0,.3),projection=True);self.play(FadeIn(g),run_time=.5)
        self.play(t.animate.set_value(2*PI+.35),run_time=5.5,rate_func=linear)
        trig=eq('x = r cos θ     y = r sin θ',3.6,31);self.play(FadeIn(trig),run_time=.4)
        self.play(t.animate.increment_value(PI),run_time=4,rate_func=linear);self.to(14)
        self.play(Transform(trig,eq('x² + y² = r²',3.6,46,TEAL)),run_time=1)
        self.to(19)
        # Squared components partition one fixed-width bar.
        def bars():
            a=4.8*np.cos(t.get_value())**2;b=4.8-a
            return VGroup(Rectangle(width=max(a,.001),height=.28,stroke_width=0,fill_color=BLUE,fill_opacity=1).move_to(p(-2.4+a/2,-3.3)),Rectangle(width=max(b,.001),height=.28,stroke_width=0,fill_color=PURPLE,fill_opacity=1).move_to(p(-2.4+a+b/2,-3.3)))
        self.add(always_redraw(bars),eq('x²                 y²',-3.9,25),eq('합은 언제나 r²',-2.65,27,TEAL))
        self.play(t.animate.increment_value(2*PI),run_time=9,rate_func=linear)

class CircleRule(Chapter):
    section='rule'
    def draw_rule(self):
        t=ValueTracker(.5);self.add(axes((0,.2)),orbit(t,(0,.2),tangent=True),eq('일정한 각속도 ω',3.65,27,MUTED))
        self.play(t.animate.increment_value(PI),run_time=6,rate_func=linear)
        self.play(FadeIn(eq('dx/dt = −ωy',-2.85,37,BLUE)),FadeIn(eq('dy/dt = +ωx',-3.65,37,PURPLE)),run_time=.6)
        self.play(t.animate.increment_value(2*PI),run_time=7.4,rate_func=linear)
        self.add(eq('반지름 ⟂ 변화 방향',3,29,TEAL))
        self.play(t.animate.increment_value(2*PI),run_time=8,rate_func=linear)

class CircleSpring(Chapter):
    section='spring'
    def draw_spring(self):
        t=ValueTracker(0);self.add(eq('마찰 없는 이상적 용수철',3.6,27,MUTED))
        self.to(4);self.play(FadeIn(spring(t)),run_time=.6);self.to(6)
        self.play(t.animate.increment_value(2*PI),run_time=6,rate_func=linear)
        self.play(FadeIn(eq('dx/dt = v',-.9,37,BLUE)),FadeIn(eq('dv/dt = −ω²x',-2.1,37,PURPLE)),FadeIn(eq('ω = √(k/m)',-3.3,28,MUTED)),run_time=.5)
        self.play(t.animate.increment_value(2*PI),run_time=7.5,rate_func=linear)

class CirclePhase(Chapter):
    section='phase'
    def draw_phase(self):
        t=ValueTracker(0);scale=ValueTracker(.6)
        phase_axes=axes((0,-1.3),1.65,'x','−v')
        self.add(spring(t,2.7),phase_axes)
        curve=always_redraw(lambda:Ellipse(width=3.3,height=3.3*scale.get_value(),color=TEAL).move_to(p(0,-1.3)))
        dot=always_redraw(lambda:Dot(p(1.65*np.cos(t.get_value()),-1.3+1.65*scale.get_value()*np.sin(t.get_value())),radius=.1,color=ORANGE))
        self.play(FadeIn(curve),FadeIn(dot),run_time=.5)
        note=eq('속도 축의 크기·방향 조정',-.0,25,MUTED);self.add(note)
        self.play(t.animate.increment_value(2*PI),run_time=4.5,rate_func=linear)
        self.play(scale.animate.set_value(1),t.animate.increment_value(PI/2),Transform(phase_axes[-1],text('−v/ω',-.55,.67,25,PURPLE)),FadeOut(note),run_time=2,rate_func=linear)
        self.add(eq('x² + (v/ω)² = A²',-3.85,34,TEAL))
        self.play(t.animate.increment_value(2*PI),run_time=7,rate_func=linear)

class CircleCircuit(Chapter):
    section='circuit'
    def draw_circuit(self):
        t=ValueTracker(0);self.add(eq('저항 없는 이상적 LC 회로',3.9,27,MUTED))
        self.to(3);self.play(FadeIn(circuit(t)),run_time=.6)
        self.play(t.animate.increment_value(2*PI),run_time=4.4,rate_func=linear)
        self.add(eq('전기장 에너지  ⇄  자기장 에너지',-.1,25,TEAL))
        self.play(t.animate.increment_value(2*PI),run_time=6,rate_func=linear)
        self.add(eq('dq/dt = I',-1.5,37,BLUE),eq('dI/dt = −ω²q',-2.65,37,PURPLE),eq('ω = 1/√(LC)',-3.8,28,MUTED))
        self.play(t.animate.increment_value(2*PI),run_time=5,rate_func=linear)

class CircleElectric(Chapter):
    section='electric'
    def draw_electric(self):
        t=ValueTracker(0);self.add(circuit(t,2.6),axes((0,-1.5),1.6,'q','−I/ω'))
        self.play(FadeIn(orbit(t,(0,-1.5),1.6)),run_time=.6)
        self.play(t.animate.increment_value(2*PI),run_time=5.4,rate_func=linear)
        self.add(eq('q² + (I/ω)² = Q²',-3.85,34,TEAL))
        self.play(t.animate.increment_value(2*PI),run_time=6,rate_func=linear)

class CircleMerge(Chapter):
    section='merge'
    def draw_merge(self):
        centers=[(-2.4,1),(0,1),(2.4,1)];gs=[]
        for c,name in zip(centers,['원운동','용수철','LC 회로']):
            g=VGroup(Circle(.85,color=TEAL).move_to(p(*c)),Dot(p(c[0]+.85,c[1]),color=ORANGE,radius=.075));gs.append(g)
            self.add(g,text(name,c[0],2.5,24))
        self.add(eq('진폭과 시간을 정규화',3.7,27,MUTED),eq('X = cos τ     Y = sin τ',-1.2,34))
        self.to(5)
        self.play(*[g.animate.move_to(p(0,1)).scale(2) for g in gs],run_time=1.5)
        self.add(eq('dX/dτ = −Y',-2.6,37,BLUE),eq('dY/dτ = +X',-3.65,37,PURPLE))

class CircleInvariant(Chapter):
    section='invariant'
    def draw_invariant(self):
        t=ValueTracker(.6);self.add(orbit(t,(0,1.1),1.65))
        a=eq('d(X² + Y²)/dτ',-1.3,36);b=eq('= −2XY + 2XY',-2.4,36)
        self.add(a,b);self.play(t.animate.increment_value(PI),run_time=2.8,rate_func=linear)
        self.play(Transform(b,eq('= 0',-2.4,42,TEAL)),run_time=.7)
        self.play(Transform(a,eq('X² + Y² = 1',-1.3,43,TEAL)),FadeOut(b),run_time=1.5)
        self.play(t.animate.increment_value(PI),run_time=2,rate_func=linear)

class CircleEnding(Chapter):
    section='ending'
    def draw_ending(self):
        t=ValueTracker(.5);self.add(axes((0,.3),2.15,'X','Y'),orbit(t,(0,.3),projection=True),eq('X² + Y² = R²',3.6,46,TEAL))
        self.add(eq('기하학 · 역학 · 전기',-2.75,29,MUTED))
        self.play(t.animate.increment_value(2*PI),run_time=8,rate_func=linear)
        self.play(FadeIn(eq('서로 다른 현상, 같은 변화의 규칙',-3.7,29,TEAL)),run_time=1)
        self.play(t.animate.increment_value(PI),run_time=7,rate_func=linear)
