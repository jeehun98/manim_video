"""Fixed electrodes and explanatory views, in schematic units."""
import numpy as np
from manim import *
from quantum_series.shared.theme import text,p,INK,MUTED,GOLD
from quantum_series.episodes.ep05_franck_hertz.experiment_model import current,MINIMA
ELECTRON='#43C5F4';MERCURY='#D6A25B';ACCEL='#4DB6AC';RETARD='#E47F66';LOSS='#F18A54';LEVEL='#739CE8';UV='#B28CFF'
class MercuryAtom(VGroup):
    def __init__(self,center=ORIGIN,radius=.4):
        super().__init__(Circle(radius=radius,color=MERCURY,stroke_width=2,fill_color=MERCURY,fill_opacity=.06).move_to(center),text('Hg',*center[:2],size=22,color=MERCURY))
class FranckHertzTube(VGroup):
    def __init__(self,center=ORIGIN):
        super().__init__();self.origin=np.array(center);self.cathode=center+p(-2.7,0);self.grid=center+p(1.55,0);self.collector=center+p(2.7,0)
        shell=RoundedRectangle(width=6.2,height=2,corner_radius=.2,color=MUTED,stroke_width=1.5).move_to(center)
        electrodes=VGroup(Line(self.cathode+DOWN*.65,self.cathode+UP*.65,color=LOSS,stroke_width=5),DashedLine(self.grid+DOWN*.72,self.grid+UP*.72,color=ACCEL,stroke_width=3),Line(self.collector+DOWN*.65,self.collector+UP*.65,color=INK,stroke_width=5))
        self.atoms=VGroup(*[MercuryAtom(center+p(x,y),.23).scale(.7) for x,y in [(-1.6,.45),(-.55,-.45),(.6,.45)]])
        self.labels=VGroup(*[text(label,point[0],center[1]-1.3,19,color) for label,point,color in [('음극',self.cathode,LOSS),('격자',self.grid,ACCEL),('검출부',self.collector,INK)]])
        self.fields=VGroup(Arrow(center+p(-2.1,.83),center+p(.95,.83),color=ACCEL,buff=0,stroke_width=2),Arrow(center+p(2.5,.82),center+p(1.8,.82),color=RETARD,buff=0,stroke_width=2))
        self.add(shell,electrodes,self.atoms,self.labels,self.fields,text('가속',center[0]-.7,center[1]+1.25,19,ACCEL),text('감속',center[0]+2.1,center[1]+1.25,19,RETARD))
    def electron(self,y=0):return Dot(self.cathode+p(.12,y),radius=.065,color=ELECTRON)
class CurrentVoltagePlot(VGroup):
    def __init__(self,center=ORIGIN,width=6,height=2.2):
        super().__init__();self.axes=Axes(x_range=[0,18,3],y_range=[0,1.3,.5],x_length=width,y_length=height,tips=False,axis_config={'color':MUTED,'stroke_width':1.3,'include_ticks':False}).move_to(center)
        self.add(self.axes,text('가속 전압 U (V)',center[0],center[1]-height/2-.5,20),text('검출 전류 · 상대값',center[0],center[1]+height/2+.8,20,ELECTRON))
        for u in [0,5,10,15]:self.add(text(str(u),*self.axes.c2p(u,-.13)[:2],size=16,color=MUTED))
    def curve(self,lo=0,hi=18):return self.axes.plot(current,x_range=[lo,max(lo+.001,hi),.04],color=ELECTRON,stroke_width=3)
    def point(self,u):return self.axes.c2p(u,current(u))
    def intervals(self):
        marks=VGroup()
        for u in MINIMA:marks.add(DashedLine(self.axes.c2p(u,0),self.axes.c2p(u,1.22),color=GOLD,stroke_width=1))
        y=self.axes.c2p(0,1.23)[1]
        for a,b in zip(MINIMA,MINIMA[1:]):marks.add(DoubleArrow(p(self.axes.c2p(a,0)[0],y),p(self.axes.c2p(b,0)[0],y),buff=.02,color=GOLD,stroke_width=2),text('4.9 V',*(self.axes.c2p((a+b)/2,1.43))[:2],size=19,color=GOLD))
        return marks
class MercuryEnergyLevels(VGroup):
    def __init__(self,center=ORIGIN,width=3.6,gap=1.6):
        super().__init__();self.low=center+p(0,-gap/2);self.high=center+p(0,gap/2)
        self.add(Line(self.low+LEFT*width/2,self.low+RIGHT*width/2,color=LEVEL,stroke_width=3),Line(self.high+LEFT*width/2,self.high+RIGHT*width/2,color=LEVEL,stroke_width=3),text('바닥 상태',self.low[0],self.low[1]-.35,20,MUTED),text('들뜬 상태',self.high[0],self.high[1]+.35,20,MUTED))
    def transition(self,up=True,x=0):return Arrow((self.low if up else self.high)+RIGHT*x,(self.high if up else self.low)+RIGHT*x,buff=.05,color=GOLD,stroke_width=3)
def energy_bar(value,center,width=3.5):
    fraction=min(1,max(0,value/6))
    return VGroup(text(f'전자 운동에너지  {value:.1f} eV',center[0],center[1]+.5,22,ELECTRON),Rectangle(width=width,height=.23,color=MUTED,stroke_width=1).move_to(center),Rectangle(width=max(.015,width*fraction),height=.2,stroke_width=0,fill_color=ELECTRON,fill_opacity=1).move_to(center+p(-width*(1-fraction)/2,0)))
def uv_wave(center):return VGroup(ParametricFunction(lambda t:center+p(t,.12*np.sin(t*TAU*2)),t_range=[0,1.4,.02],color=UV,stroke_width=3),text('UV',center[0]+.7,center[1]+.4,21,UV))
