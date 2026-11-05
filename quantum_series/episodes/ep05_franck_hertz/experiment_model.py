"""Illustrative one-dimensional mercury transport; generated curves are never measurements."""
from dataclasses import dataclass,replace
from functools import lru_cache
import numpy as np

EXCITATION_EV=4.9
UV_WAVELENGTH_NM=253.7
HC_EV_NM=1239.841984
E_CHARGE=1.602176634e-19
E_MASS=9.1093837139e-31

@dataclass(frozen=True)
class ExperimentModel:
    excitation_ev: float=EXCITATION_EV
    retarding_voltage: float=.8
    contact_offset: float=1.3

    def effective_voltage(self,voltage):return max(0.,voltage-self.contact_offset)
    def speed(self,kinetic_ev):return np.sqrt(2*max(0.,kinetic_ev)*E_CHARGE/E_MASS)
    def collision(self,kinetic_ev):
        if kinetic_ev<self.excitation_ev:return kinetic_ev,False
        return kinetic_ev-self.excitation_ev,True
    def collected(self,grid_kinetic_ev):return grid_kinetic_ev>=self.retarding_voltage

MODEL=ExperimentModel()

@dataclass(frozen=True)
class ElectronState:
    x: float=0.
    kinetic_ev: float=.1
    excitation_count: int=0
    transferred_ev: float=0.

    def accelerate(self,new_x,voltage):
        if new_x<self.x or new_x>1 or self.x>1:
            raise ValueError('Acceleration is allowed only towards the grid, before x=1')
        return replace(self,x=new_x,kinetic_ev=self.kinetic_ev+MODEL.effective_voltage(voltage)*(new_x-self.x))

    def collide(self):
        kinetic,excited=MODEL.collision(self.kinetic_ev)
        return replace(self,kinetic_ev=kinetic,excitation_count=self.excitation_count+int(excited),
                       transferred_ev=self.transferred_ev+MODEL.excitation_ev*int(excited)),excited

    def enter_retarding_region(self,new_x):
        if self.x<1 or not 1<=new_x<=1.22:raise ValueError('Retarding region is x=1..1.22')
        potential_gain=MODEL.retarding_voltage*(new_x-self.x)/.22
        if potential_gain>self.kinetic_ev:
            return replace(self,x=self.x+.22*self.kinetic_ev/MODEL.retarding_voltage,kinetic_ev=0.),False
        return replace(self,x=new_x,kinetic_ev=max(0.,self.kinetic_ev-potential_gain)),True

@lru_cache(maxsize=1)
def current_curve():
    """Common-random-number ensemble: excitation events and detector eligibility share MODEL."""
    rng=np.random.default_rng(1914)
    electrons=2048;steps=240;dx=1/steps
    thermal=rng.uniform(.03,.3,electrons)
    # A small weakly interacting subensemble prevents a selected failed electron
    # from implying zero total current. This is not a fitted mercury cross section.
    mean_free_path=np.where(rng.random(electrons)<.1,2.5,.025)
    probability=1-np.exp(-dx/mean_free_path)
    samples=rng.random((steps,electrons))
    voltages=np.linspace(0,20,401)
    values=[];fractions=[]
    for voltage in voltages:
        energy=thermal.copy()
        gain=MODEL.effective_voltage(float(voltage))*dx
        for i in range(steps):
            energy+=gain
            collision=(energy>=MODEL.excitation_ev)&(samples[i]<probability)
            energy[collision]-=MODEL.excitation_ev
        fraction=float(np.mean(energy>=MODEL.retarding_voltage))
        # Smooth extraction/collection efficiency, not extra energy after the grid.
        extraction=1-np.exp(-MODEL.effective_voltage(float(voltage))/5)
        values.append(fraction*extraction);fractions.append(fraction)
    values=np.asarray(values)
    # Mild display smoothing of Monte Carlo sampling noise only.
    padded=np.pad(values,(2,2),mode='edge')
    values=np.convolve(padded,np.array([1,2,3,2,1])/9,mode='valid')
    minima=[]
    for n in range(3):
        mask=(voltages>5.7+4.9*n)&(voltages<7.3+4.9*n)
        indices=np.flatnonzero(mask)
        minima.append(int(indices[np.argmin(values[indices])]))
    return {'voltage':voltages,'current':values,'detected_fraction':np.asarray(fractions),
            'minima_indices':minima,'source':'seeded illustrative transport model; not measured data','seed':1914}

def current_at(voltage):
    curve=current_curve()
    return float(np.interp(voltage,curve['voltage'],curve['current']))
