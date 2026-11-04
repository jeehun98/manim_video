"""Idealized one-photon threshold, not a yield or surface-scattering simulation."""
from dataclasses import dataclass, replace

H_EV_S=4.135667696e-15
C=299792458.
LOW_FREQUENCY=C/(700e-9)
HIGH_FREQUENCY=C/(450e-9)
WORK_FUNCTION_EV=2.2

@dataclass(frozen=True)
class PhotoelectricModel:
    frequency: float=HIGH_FREQUENCY
    intensity: float=1.0
    work_function: float=WORK_FUNCTION_EV

    def __post_init__(self):
        if self.frequency<=0 or self.intensity<0 or self.work_function<=0:
            raise ValueError('Nonphysical frequency, intensity, or work function')

    @property
    def energy_ev(self):return H_EV_S*self.frequency
    @property
    def threshold_frequency(self):return self.work_function/H_EV_S
    @property
    def can_emit(self):return self.intensity>0 and self.energy_ev>=self.work_function
    @property
    def maximum_kinetic_energy_ev(self):return max(0.,self.energy_ev-self.work_function)
    @property
    def relative_number_flux(self):
        # With intensity measured in a common arbitrary power unit, this is
        # proportional to number / area / time. Intensity is not itself a count.
        return self.intensity/self.energy_ev

    def changed(self,**kwargs):return replace(self,**kwargs)
