"""Historical Bohr symbols and hydrogen calculations. Orbits are schematic."""
import numpy as np
from manim import *
from quantum_series.shared.theme import text,p,INK,MUTED,GOLD,BG
from quantum_series.shared.rutherford import RutherfordAtom,NUCLEUS,ELECTRON
ALLOWED='#4DB6AC'
LOSS='#F18A54'
CLASSICAL='#95A0B3'
# Reduced-mass hydrogen Rydberg energy, eV; gross structure, vacuum wavelengths.
RYDBERG_EV=13.598287
HC_EV_NM=1239.841984
OBSERVED_NM={3:656.28,4:486.13,5:434.05,6:410.17} # representative air wavelengths
COLORS={3:'#FF5C68',4:'#44D6DE',5:'#8973FF',6:'#B16BFF'}
def energy(n):return -RYDBERG_EV/n**2
def wavelength(n,lower=2):return HC_EV_NM/(energy(n)-energy(lower))
class BohrAtom(VGroup):
    def __init__(self,center=ORIGIN,allowed=True):
        super().__init__()
        self.center_point=np.array(center)
        self.rings=VGroup(*[Circle(radius=r,color=ALLOWED if allowed else CLASSICAL,stroke_width=2).move_to(center) for r in [.7,1.4,2.1]])
        self.core=RutherfordAtom(electrons=False,nucleus_radius=.13).nucleus.move_to(center)
        self.electron=Dot(center+p(1.4,0),radius=.085,color=ELECTRON)
        self.add(self.rings,self.core,self.electron)
class EnergyLevelDiagram(VGroup):
    def __init__(self,center=ORIGIN,width=3.1,height=4.0):
        super().__init__();self.center_point=np.array(center);self.width_value=width
        self.ys={n:center[1]-height/2+(energy(n)-energy(1))/(-energy(1))*height for n in range(1,7)}
        self.lines=VGroup();self.labels=VGroup()
        for n,y in self.ys.items():
            self.lines.add(Line(p(center[0]-width/2,y),p(center[0]+width/2,y),color=ALLOWED,stroke_width=2))
            # Label high states on alternating sides to preserve actual nonuniform spacing.
            x=center[0]+width/2+.45 if n%2 else center[0]-width/2-.45
            label_y=y if n<5 else y+(.25 if n==5 else .4)
            self.labels.add(text(f'n={n}',x,label_y,16))
            if n>=5:self.labels.add(Line(p(x + (-.25 if n%2 else .25),label_y),p(center[0]+(width/2 if n%2 else -width/2),y),color=MUTED,stroke_width=.7))
        self.add(self.lines,self.labels)
    def point(self,n,x=0):return p(self.center_point[0]+x,self.ys[n])
class HydrogenSpectrum(VGroup):
    def __init__(self,center=ORIGIN,width=6.5,observed=False,continuous=False,labels=True):
        super().__init__();self.center_point=np.array(center);self.span=width;self.lines={}
        self.add(Rectangle(width=width,height=.65,color=MUTED,stroke_width=1,fill_color='#050812',fill_opacity=1).move_to(center))
        if continuous:
            for i in range(80):
                nm=400+300*(i+.5)/80
                color=interpolate_color(PURPLE,RED,i/79)
                if 450<nm<530:color=interpolate_color(BLUE,GREEN,(nm-450)/80)
                elif 530<=nm<600:color=interpolate_color(GREEN,YELLOW,(nm-530)/70)
                self.add(Rectangle(width=width/80+.005,height=.6,stroke_width=0,fill_color=color,fill_opacity=1).move_to(p(self.x(nm),center[1])))
        else:
            for n in [6,5,4,3]:
                nm=OBSERVED_NM[n] if observed else wavelength(n)
                line=Line(p(self.x(nm),center[1]-.29),p(self.x(nm),center[1]+.29),color=COLORS[n],stroke_width=4)
                self.lines[n]=line;self.add(line)
                if labels:self.add(text(str(round(nm)),self.x(nm),center[1]-.55,15,COLORS[n]))
        self.add(text('400',self.x(400),center[1]+.55,15,MUTED),text('700 nm',self.x(700)-.2,center[1]+.55,15,MUTED))
    def x(self,nm):return self.center_point[0]+((nm-400)/300-.5)*self.span
def photon(center,color=GOLD,width=1.3):
    return ParametricFunction(lambda t:center+p(t,.13*np.sin(t*TAU*2.5)),t_range=[0,width,.02],color=color,stroke_width=3)
