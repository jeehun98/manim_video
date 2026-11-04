"""Dimensionless, fixed-centre repulsive trajectories; numerical RK4, no hand-drawn bends."""
from dataclasses import dataclass
from functools import lru_cache
import numpy as np

@dataclass(frozen=True)
class CoulombModel:
    strength: float=.12
    energy: float=.5
    diffuse_radius: float=1.8

    def acceleration(self,r,distribution='point'):
        distance=float(np.linalg.norm(r))
        if distribution=='diffuse' and distance<self.diffuse_radius:
            return self.strength*r/self.diffuse_radius**3
        return self.strength*r/distance**3

    def potential(self,r,distribution='point'):
        radius=np.linalg.norm(r,axis=-1)
        if distribution=='diffuse':
            a=self.diffuse_radius
            return np.where(radius<a,self.strength*(3-(radius/a)**2)/(2*a),self.strength/np.maximum(radius,1e-12))
        return self.strength/radius

MODEL=CoulombModel()

@lru_cache(maxsize=96)
def trajectory(impact_parameter,distribution='point',dt=.008):
    if distribution not in ('point','diffuse'):raise ValueError(distribution)
    r=np.array([-7.,float(impact_parameter)])
    v=np.array([np.sqrt(2*(MODEL.energy-float(MODEL.potential(r,distribution)))),0.])
    state=np.r_[r,v]
    history=[state.copy()]
    def derivative(s):return np.r_[s[2:],MODEL.acceleration(s[:2],distribution)]
    for step in range(7000):
        k1=derivative(state);k2=derivative(state+dt*k1/2)
        k3=derivative(state+dt*k2/2);k4=derivative(state+dt*k3)
        state=state+dt*(k1+2*k2+2*k3+k4)/6
        history.append(state.copy())
        if step>750 and np.linalg.norm(state[:2])>9 and np.dot(state[:2],state[2:])>0:break
    else:raise RuntimeError('Trajectory did not leave the scattering region')
    result=np.asarray(history)
    result.setflags(write=False)
    return result

def display_segment(impact_parameter,distribution='point'):
    values=trajectory(impact_parameter,distribution)
    r=values[:,:2]
    # Start at a common incoming x and stop at the first exit from the viewport.
    entry=np.flatnonzero(r[:,0]>=-4.8)[0]
    outside=(abs(r[:,0])>4.8)|(abs(r[:,1])>2.65)
    exits=np.flatnonzero(outside & (np.arange(len(r))>entry))
    end=int(exits[0]) if len(exits) else len(r)-1
    return values[entry:end+1]

def scattering_angle(impact_parameter,distribution='point'):
    v=trajectory(impact_parameter,distribution)[-1,2:]
    return float(np.degrees(np.arctan2(v[1],v[0])))
