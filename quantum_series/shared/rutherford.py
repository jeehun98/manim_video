"""Atomic symbols and calculated trajectory views; scales and selected counts are illustrative."""
import numpy as np
from manim import *
from quantum_series.shared.theme import BG,INK,MUTED,GOLD,text,p
from quantum_series.shared.coulomb import display_segment

ALPHA='#FFB347'
FOIL='#D6AF59'
POSITIVE='#E7A16D'
ELECTRON='#48A9E6'
NUCLEUS='#F26C65'
EXPECTED='#8F9BAD'
OBSERVED='#43C4E5'

class AlphaParticle(Dot):
    def __init__(self,point=ORIGIN):super().__init__(point,radius=.06,color=ALPHA)

class ThomsonAtom(VGroup):
    def __init__(self,radius=1.8):
        super().__init__()
        self.boundary=Circle(radius=radius,color=MUTED,stroke_width=1.5,stroke_opacity=.6)
        self.cloud=Circle(radius=radius,color=POSITIVE,stroke_width=0,fill_color=POSITIVE,fill_opacity=.17)
        self.positives=VGroup(*[text('+',x,y,27,POSITIVE) for x,y in [(-.8,.25),(-.15,1.1),(.85,.2),(.05,-1.0)]])
        self.electrons=VGroup(*[VGroup(Dot(p(x,y),radius=.075,color=ELECTRON),
                                     text('−',x,y+.18,17,ELECTRON)) for x,y in [(-1,-.65),(.75,-.65),(-.6,.8),(1,.85)]])
        self.add(self.boundary,self.cloud,self.positives,self.electrons)

class RutherfordAtom(VGroup):
    def __init__(self,radius=1.8,electrons=True,nucleus_radius=.1):
        super().__init__()
        self.boundary=DashedVMobject(Circle(radius=radius,color=MUTED,stroke_width=1.4,stroke_opacity=.65),num_dashes=65)
        self.nucleus=Dot(radius=nucleus_radius,color=NUCLEUS)
        self.electrons=VGroup()
        if electrons:
            self.electrons.add(*[Dot(p(x,y),radius=.075,color=ELECTRON) for x,y in [(-1.15,-.7),(.75,-1.1),(-.55,1.2),(1.25,.6)]])
        self.add(self.boundary,self.nucleus,self.electrons)

class CoulombTrajectory:
    def __init__(self,b,distribution='point',center=ORIGIN,scale=.65,detector=False):
        values=display_segment(b,distribution)
        if detector:
            r=values[:,:2];outgoing=np.sum(r*values[:,2:],axis=1)>0
            hits=np.flatnonzero((np.linalg.norm(r,axis=1)>=4.35)&outgoing)
            if len(hits):values=values[:hits[0]+1]
        self.values=values
        self.center=np.array(center);self.scale=scale
        self.positions=np.c_[values[:,:2]*scale,np.zeros(len(values))]+self.center
        stride=max(1,len(values)//240)
        sampled=np.vstack([self.positions[::stride],self.positions[-1]])
        self.path=VMobject(color=OBSERVED,stroke_width=2.2).set_points_as_corners(sampled)

    def at(self,alpha):
        t=np.clip(alpha,0,1)*(len(self.positions)-1)
        i=min(int(t),len(self.positions)-2)
        return interpolate(self.positions[i],self.positions[i+1],t-i)

def foil_apparatus(center,scale=.65,detector=False):
    source=RoundedRectangle(width=.58,height=.82,corner_radius=.1,color=MUTED,fill_color=MUTED,fill_opacity=.2)
    source.move_to(center+p(-5.3*scale,0))
    slot=Line(source.get_right()+UP*.2,source.get_right()+DOWN*.2,color=ALPHA,stroke_width=3)
    foil=Rectangle(width=.12,height=3.4,color=FOIL,fill_color=FOIL,fill_opacity=.7).move_to(center)
    labels=VGroup(text('입자원',size=18,color=MUTED).next_to(source,DOWN,buff=.18),
                  text('금박',size=19,color=FOIL).next_to(foil,DOWN,buff=.18))
    group=VGroup(source,slot,foil,labels)
    if detector:
        arc=Arc(radius=4.35*scale,start_angle=-PI,angle=TAU,color=OBSERVED,stroke_width=1.6,stroke_opacity=.55).move_arc_center_to(center)
        group.add(arc)
    return group

def atom_mosaic():
    return VGroup(*[Circle(radius=.23,color=FOIL,fill_color=BG,fill_opacity=1,stroke_width=1.1)
                   .move_to(p((i%5-2)*.57,(i//5-1)*.57)) for i in range(15)])

def classical_spiral(center,radius):
    # A schematic consequence of the classical radiating-orbit assumption,
    # not a simulated or observed electron trajectory.
    return ParametricFunction(lambda t:center+p(radius*(1-.84*t)*np.cos(TAU*1.4*t),
                                                 radius*(1-.84*t)*np.sin(TAU*1.4*t)),
                              t_range=[0,1,.004],color=ELECTRON,stroke_width=2)
