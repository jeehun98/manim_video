"""Reusable physical diagrams. All graph samples are theoretical, never measured data."""
import numpy as np
from manim import *
from quantum_series.shared.theme import BG, INK, MUTED, HEAT, DATA, OLD, GOLD, text, p

H = 6.62607015e-34
C = 299792458.
K = 1.380649e-23
TEMPERATURE = 1500.

def radiance(wavelength_um, *, wien=False, temperature=TEMPERATURE):
    wavelength = np.asarray(wavelength_um) * 1e-6
    exponent = H*C/(wavelength*K*temperature)
    return 2*H*C*C/wavelength**5 * (np.exp(-exponent) if wien else 1/np.expm1(exponent))

NORMALIZATION = float(radiance(2897.771955/TEMPERATURE))

def distribution(wavelength_um, wien=False):
    return float(radiance(wavelength_um, wien=wien)/NORMALIZATION)

def metal(width=3.2, hot=1.):
    color = interpolate_color(ManimColor('#4E5365'), ManimColor(HEAT), hot)
    glow = VGroup(*[RoundedRectangle(width=width+.12*i, height=.6+.1*i, corner_radius=.12,
                  stroke_width=0, fill_color=HEAT, fill_opacity=hot*.022*(9-i)) for i in range(8, 0, -1)])
    bar = RoundedRectangle(width=width, height=.6, corner_radius=.1, stroke_color=color,
                           fill_color=color, fill_opacity=1, stroke_width=2)
    shine = Line(p(-width/2+.16,.18),p(width/2-.16,.18),color=INK,stroke_opacity=.45*hot,stroke_width=2)
    return VGroup(glow,bar,shine)

def wave(width=2.6, amplitude=.2, cycles=3, color=HEAT, phase=0):
    return ParametricFunction(lambda t: p(t, amplitude*np.sin(TAU*cycles*(t/width+.5)+phase)),
                             t_range=[-width/2,width/2,.025], color=color,stroke_width=3)

class Spectrum(VGroup):
    def __init__(self, layout, zoom=False):
        super().__init__()
        self.zoom = zoom
        xr, yr = ([5, 12, 2], [0, .25, .05]) if zoom else ([0,12,2], [0,1.1,.2])
        self.axes = Axes(x_range=xr,y_range=yr,x_length=layout.graph_width,y_length=3.3,
                         tips=False,axis_config={'color':MUTED,'stroke_width':1.5,'include_ticks':True},
                         x_axis_config={'include_numbers':False},y_axis_config={'include_numbers':False})
        self.axes.move_to(layout.graph_center)
        self.labels = VGroup(text('파장 λ (μm)',size=20,color=MUTED).next_to(self.axes,DOWN,buff=.27),
                             text('파장별 복사 강도 · 상대값',size=18,color=MUTED).next_to(self.axes,UP,buff=.15))
        for v in ([6,8,10,12] if zoom else [2,4,6,8,10,12]):
            self.labels.add(text(str(v),size=16,color=MUTED).move_to(self.axes.c2p(v,0)+DOWN*.16))
        ymax = yr[1]
        for v in ([.1,.2] if zoom else [.5,1.]):
            self.labels.add(text(f'{v:g}',size=15,color=MUTED).move_to(self.axes.c2p(xr[0],v)+LEFT*.24))
        xstart = 5 if zoom else .32
        self.old = self.axes.plot(lambda x:distribution(x,True),x_range=[xstart,12,.035],color=OLD,stroke_width=3)
        self.reference = self.axes.plot(lambda x:distribution(x),x_range=[xstart,12,.035],color=DATA,stroke_width=3)
        self.planck = self.axes.plot(lambda x:distribution(x),x_range=[xstart,12,.035],color=GOLD,stroke_width=3.5)
        self.note = text('T = 1500 K · 흑체 근사 · 이론적 분포',size=17,color=MUTED).next_to(self.labels[0],DOWN,buff=.23)
        # Dots sample Planck's law; the adjacent label explicitly identifies their origin.
        self.samples = VGroup(*[Dot(self.axes.c2p(x,distribution(x)),radius=.045,color=DATA)
                               for x in np.linspace(5.4,11.5,7)])
        xs=np.linspace(5,12,100)
        self.gap = Polygon(*[self.axes.c2p(x,distribution(x)) for x in xs],
                           *[self.axes.c2p(x,distribution(x,True)) for x in xs[::-1]],
                           stroke_width=0,fill_color=DATA,fill_opacity=.2)
        self.add(self.axes,self.labels,self.note)

def legend(layout, planck=False):
    y=-3.2 if layout.portrait else -2.85
    x=0 if layout.portrait else 3.25
    items=VGroup(text('빈 법칙',size=20,color=OLD),text('이론적 기준 분포',size=20,color=DATA))
    if planck: items.add(text('플랑크 법칙',size=20,color=GOLD))
    items.arrange(RIGHT,buff=.28).move_to(p(x,y))
    if items.width>layout.graph_width:items.scale_to_fit_width(layout.graph_width)
    return items

def oscillator(x,y=0):
    base=Line(p(x-.53,y-.55),p(x+.53,y-.55),color=MUTED,stroke_width=2)
    vertices=[p(x,y-.55),p(x,y-.45)]
    for i in range(9):vertices.append(p(x+(.13 if i%2 else -.13),y-.4+i*.065))
    vertices.append(p(x,y+.2))
    spring=VMobject(color=MUTED,stroke_width=2).set_points_as_corners(vertices)
    mass=Circle(radius=.16,color=DATA,fill_color=BG,fill_opacity=1,stroke_width=3).move_to(p(x,y+.38))
    return VGroup(base,spring,mass)

def energy_tiles(layout, counts, y=-.7):
    blocks=VGroup()
    for x,n in zip(layout.column_x,counts):
        for j in range(n):
            blocks.add(RoundedRectangle(width=.42,height=.35,corner_radius=.04,color=GOLD,
                        fill_color=GOLD,fill_opacity=.8,stroke_width=1.3).move_to(p(x,y+j*.42)))
    return blocks

def count_labels(layout, counts, y=-1.48):
    return VGroup(*[text(str(n),x,y,30,GOLD) for x,n in zip(layout.column_x,counts)])

def connecting_wave(layout):
    width=6.3 if layout.portrait else 11.5
    return wave(width=width,amplitude=.32,cycles=6,color=DATA).move_to(p(0,.25))
