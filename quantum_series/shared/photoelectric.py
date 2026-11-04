"""Wave, metal, electron and energy-symbol components shared by both screen layouts."""
import numpy as np
from manim import *
from quantum_series.shared.theme import BG,INK,MUTED,DATA,GOLD,text,p

METAL='#8491A3'
LOW='#F18A54'
HIGH='#579CFF'

def energy_unit(width=.3):
    # The external outline is a symbol, not a literal size or shape of a photon.
    return RoundedRectangle(width=width,height=.27,corner_radius=.045,color=GOLD,
                            fill_color=GOLD,fill_opacity=.65,stroke_width=1.7)

def metal_plate(width=4.2):
    return VGroup(RoundedRectangle(width=width,height=.5,corner_radius=.08,color=METAL,
                  fill_color=METAL,fill_opacity=.25,stroke_width=2),
                  Line(p(-width/2,.25),p(width/2,.25),color=METAL,stroke_width=3))

def travelling_wave(width=6,amplitude=.25,cycles=3,phase=0,color=HIGH):
    return ParametricFunction(lambda x:p(x,amplitude*np.sin(TAU*cycles*(x/width+.5)-phase)),
                             t_range=[-width/2,width/2,.025],color=color,stroke_width=3)

def slider(label,value,x=0,y=0,width=3,color=HIGH):
    return VGroup(text(label,x,y+.35,22,MUTED,width=width),
                  Line(p(x-width/2,y),p(x+width/2,y),color=MUTED,stroke_width=2),
                  Dot(p(x-width/2+width*value,y),radius=.09,color=color))

class PhotoelectricExperiment(VGroup):
    def __init__(self,model):
        super().__init__()
        self.model=model
        self.plate=metal_plate().shift(DOWN*.7)
        self.electrons=VGroup(*[Dot(p(x,-.72),radius=.065,color=DATA) for x in [-1.2,-.4,.4,1.2]])
        self.beam=self.beam_for(model)
        self.trails=VGroup()
        self.add(self.plate,self.electrons,self.beam,self.trails)

    def anchors(self):
        scale=self.plate.width/4.2
        center=self.plate.get_center()
        return center+p(-1.7,2.9)*scale,center+p(0,.25)*scale,scale

    def beam_for(self,model,phase=0):
        start,end,scale=self.anchors()
        direction=end-start
        perpendicular=np.array([-direction[1],direction[0],0.])
        perpendicular=perpendicular/np.linalg.norm(perpendicular)
        amplitude=.08*np.sqrt(model.intensity)*scale
        cycles=2.6*model.frequency/(299792458./700e-9)
        color=LOW if model.energy_ev<model.work_function else HIGH
        curve=ParametricFunction(lambda t:start+t*direction+perpendicular*amplitude*np.sin(TAU*cycles*t-phase),
                                  t_range=[0,1,.012],color=color,stroke_width=2.5)
        axis=Arrow(start,end,buff=0,color=color,stroke_width=1.2,max_tip_length_to_length_ratio=.045,
                   stroke_opacity=.28)
        return VGroup(axis,curve)

    def change(self,**kwargs):
        self.model=self.model.changed(**kwargs)
        return Transform(self.beam,self.beam_for(self.model))

    def electron_destination(self,index=1):
        _,_,scale=self.anchors()
        start=self.electrons[index].get_center()
        kinetic=self.model.maximum_kinetic_energy_ev
        return start+p(1.05,1.55+.22*np.sqrt(kinetic))*scale

    def release(self,index=1):
        if not self.model.can_emit:raise ValueError('Below-threshold beam cannot release an electron')
        electron=self.electrons[index]
        target=self.electron_destination(index)
        trail=Line(electron.get_center(),target,color=DATA,stroke_width=1.5,stroke_opacity=.55)
        self.trails.add(trail)
        return [Create(trail),electron.animate.move_to(target)]

    def reset_electrons(self):
        _,_,scale=self.anchors()
        for x,electron in zip([-1.2,-.4,.4,1.2],self.electrons):
            electron.move_to(self.plate.get_center()+p(x,-.02)*scale)
        self.trails.remove(*list(self.trails))

    def incident_unit(self,width=.28,index=1):
        start,end,scale=self.anchors()
        # Distinct symbols end at distinct surface positions, never at a shared
        # storage gauge. No accumulation of subthreshold photon energies.
        end=self.electrons[index].get_center()+UP*.3*scale
        unit=energy_unit(width).scale(scale).move_to(start)
        return unit,end

def energy_comparison(model,x,y,width=3.4):
    """Same baseline and linear energy scale for E and Phi. Width means energy."""
    scale=width/3.3
    left=x-width/2
    phi=Rectangle(width=model.work_function*scale,height=.22,color=METAL,fill_color=METAL,fill_opacity=.45)
    phi.move_to(p(left+phi.width/2,y+.5))
    energy=Rectangle(width=model.energy_ev*scale,height=.22,color=GOLD,fill_color=GOLD,fill_opacity=.65)
    energy.move_to(p(left+energy.width/2,y-.55))
    mark=DashedLine(p(left+model.work_function*scale,y+.8),p(left+model.work_function*scale,y-.85),color=METAL,stroke_width=1.4)
    return VGroup(phi,energy,mark,
                  text('일함수 Φ · 필요한 최소 에너지',x,y+1.05,19,MUTED,width=width+.4),
                  text('한 단위의 에너지 E',x,y-.05,20,GOLD,width=width+.4))
