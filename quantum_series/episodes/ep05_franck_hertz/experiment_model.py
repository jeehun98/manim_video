"""Illustrative transport state; the I-U curve is a schematic, not measured or simulated data."""
from dataclasses import dataclass
import math
EXCITATION_EV=4.9
RETARDING_V=.8
HC_EV_NM=1239.841984
UV_NM=253.7
@dataclass
class ElectronState:
    kinetic_energy:float=0
    excitations:int=0
    def accelerate(self,voltage):
        self.kinetic_energy+=voltage # one electron: numeric eV gain equals voltage drop in V
    def collide(self):
        if self.kinetic_energy+1e-9<EXCITATION_EV:return False
        self.kinetic_energy=max(0,self.kinetic_energy-EXCITATION_EV);self.excitations+=1;return True
    @property
    def relative_speed(self):return math.sqrt(max(0,self.kinetic_energy))
    def collected(self,retarding_voltage=RETARDING_V):return self.kinetic_energy>retarding_voltage
# Smooth schematic with arbitrary current units and shifted absolute minima.
KNOTS=[(0,.03),(4.8,.65),(6,.22),(9.7,.88),(10.9,.37),(14.6,1.1),(15.8,.53),(18,1.15)]
MINIMA=[6,10.9,15.8]
def current(u):
    u=max(0,min(18,u))
    for (a,va),(b,vb) in zip(KNOTS,KNOTS[1:]):
        if a<=u<=b:
            t=(u-a)/(b-a);return va+(vb-va)*(3*t*t-2*t*t*t)
    return KNOTS[-1][1]
