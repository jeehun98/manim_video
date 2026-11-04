"""Orthographic 3D vector model; camera angles never alter the model vectors."""
import os,json,textwrap
from pathlib import Path
from manim import *
P=Path(__file__).resolve().parent
SHORT=os.environ.get('BATTLE_LAYOUT','shorts')=='shorts'
config.frame_width=9 if SHORT else 16
config.frame_height=16 if SHORT else 9
config.background_color='#0B1120'
BG='#0B1120';INK='#EEF4FF';MUTED='#91A4BF';BLUE='#55AEFF';GREEN='#59DFAC';ORANGE='#FFB15A';PURPLE='#BB97FF'
A1=np.array([1.,1,0]);A2=np.array([0.,2,0]);A3=np.array([1.,2,2]);Q1=A1/np.sqrt(2);Q2=np.array([-1.,1,0])/np.sqrt(2);Q3=OUT

def label(s,size=27,color=INK,width=7.5):
    m=Text(s,font='Malgun Gothic',font_size=size,color=color,line_spacing=.8)
    if m.width>width:m.scale_to_fit_width(width)
    return m

class QRBase(Scene):
    INDEX=0
    def construct(self):
        self.m=json.loads((P/'manifest.json').read_text(encoding='utf-8'))[self.INDEX]
        self.start=self.m['start'];self.end=self.m['end'];self.clock=self.start
        self.az=ValueTracker(-55*DEGREES);self.el=ValueTracker(28*DEGREES)
        self.center=np.array([-.6,1.,0]) if SHORT else np.array([-3.9,-.5,0])
        self.scale3=1.45 if SHORT else 1.15
        self.stage=VGroup()
        self.add(label('QR / 04     최소제곱과 수치 안정성',20,MUTED).move_to([0,7.35 if SHORT else 3.95,0]))
        self.add(label(self.m['title'],34,INK,8 if SHORT else 14).move_to([0,6.35 if SHORT else 3.1,0]))
        self.add(Line([-3.9,5.7,0],[3.9,5.7,0],color=MUTED,stroke_opacity=.22) if SHORT else Line([-7,2.55,0],[7,2.55,0],color=MUTED,stroke_opacity=.22))
        self.add(always_redraw(self.axes))
        cues=json.loads((P/'timing.json').read_text(encoding='utf-8'))
        cap=next(c for c in cues if c['start']<=self.start<c['end'])['caption']
        cap='\n'.join(textwrap.wrap(cap,width=29 if SHORT else 56,break_long_words=True))
        self.add(label(cap,25 if SHORT else 24,INK,8 if SHORT else 14).move_to([0,-6.4 if SHORT else -3.5,0]))
        self.add(label('열 전체 계수 · ε > 0 · 2-노름 조건수',18,MUTED).move_to([0,-7.4 if SHORT else -4.1,0]))
        self.shot()
        self.to(self.end)

    def proj(self,v):
        x,y,z=np.asarray(v);a=self.az.get_value();e=self.el.get_value()
        return self.center+self.scale3*np.array([-np.sin(a)*x+np.cos(a)*y,-np.sin(e)*(np.cos(a)*x+np.sin(a)*y)+np.cos(e)*z,0])
    def axes(self):
        g=VGroup()
        for v,t in [(RIGHT,'x'),(UP,'y'),(OUT,'z')]:
            if self.INDEX in [4,7,8,9,10] and t=='z':continue
            g.add(Line(self.proj(-2.2*v),self.proj(2.6*v),color=MUTED,stroke_width=1,stroke_opacity=.4))
            g.add(label(t,18,MUTED).move_to(self.proj(2.8*v)))
        return g
    def plane(self):
        g=VGroup(Polygon(*[self.proj(v) for v in [(-1.2,-1.2,0),(2,-1.2,0),(2,2,0),(-1.2,2,0)]],fill_color=PURPLE,fill_opacity=.09,stroke_width=1,stroke_color=PURPLE,stroke_opacity=.35))
        for t in [-1,0,1,2]:
            g.add(Line(self.proj((t,-1.2,0)),self.proj((t,2,0)),color=PURPLE,stroke_opacity=.18,stroke_width=1),Line(self.proj((-1.2,t,0)),self.proj((2,t,0)),color=PURPLE,stroke_opacity=.18,stroke_width=1))
        return g
    def vec(self,v,color,name='',origin=ORIGIN,dashed=False,opacity=1):
        a=self.proj(origin);b=self.proj(np.array(origin)+v)
        line=Arrow(a,b,buff=0,color=color,stroke_width=5,max_tip_length_to_length_ratio=.18)
        if dashed:line=DashedVMobject(line,num_dashes=12)
        g=VGroup(line)
        if name:
            offset=np.array([.16,.3,0])
            if name=='q₁':offset=np.array([.05,-.38,0])
            if name=='q₂':offset=np.array([-.32,.12,0])
            if name.startswith('p'):offset=np.array([.38,-.12,0])
            if name=='u₂':b=(a+b)/2;offset=np.array([-.4,.1,0])
            g.add(label(name,25,color,2).move_to(b+offset))
        return g.set_opacity(opacity)
    def livevec(self,tracker,color,name):return always_redraw(lambda:self.vec(tracker.get_value(),color,name))
    def put(self,*ms):
        for m in ms:self.add(m);self.stage.add(m)
    def animate(self,*anims,d=1):self.play(*anims,run_time=d)
    def to(self,t):
        remaining=t-self.start-self.time
        if remaining<-.04:raise RuntimeError(f'Overflow cut {self.INDEX+1}: {self.time} > {t-self.start}')
        if remaining>.001:self.wait(remaining)
    def equation(self,s,note='',color=INK):
        pos=[0,-3.5,0] if SHORT else [3.65,.6,0]
        eq=label(s,32,color,8 if SHORT else 6.4).move_to(pos)
        g=VGroup(eq)
        if note:g.add(label(note,23,MUTED,7.8 if SHORT else 6.2).next_to(eq,DOWN,buff=.42))
        self.put(g);return g
    def rightmark(self,o,u,v):
        u=np.array(u)/np.linalg.norm(u)*.23;v=np.array(v)/np.linalg.norm(v)*.23;o=np.array(o)
        return VMobject(color=INK,stroke_width=2).set_points_as_corners([self.proj(o+u),self.proj(o+u+v),self.proj(o+v)])
    def bases(self,third=False):
        self.put(self.vec(Q1,BLUE,'q₁'),self.vec(Q2,GREEN,'q₂'))
        if third:self.put(self.vec(Q3,ORANGE,'q₃'))
