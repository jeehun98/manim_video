"""Nonlinear pendulum, exact energy contours, and its regular Legendre transform."""
from pathlib import Path
import sys,numpy as np
sys.path.append(str(Path(__file__).resolve().parents[1]/'chapter_01'))
from physics import PendulumModel
MODEL=PendulumModel();I=MODEL.length**2;G=MODEL.g;ELL=MODEL.length
j=np.where(MODEL.states[:-1,0]*MODEL.states[1:,0]<0)[0][0]
a,b=MODEL.states[j:j+2,0];QUARTER=MODEL.times[j]+MODEL.dt*a/(a-b);PERIOD=4*QUARTER
FIXED_THETA=.35;V0=G*ELL*(1-np.cos(FIXED_THETA))
def V(theta):return G*ELL*(1-np.cos(theta))
def lagrangian(theta,omega):return .5*I*np.asarray(omega)**2-V(theta)
def momentum(omega):return I*np.asarray(omega)
def hamiltonian(theta,p):return np.asarray(p)**2/(2*I)+V(theta)
def contour(amplitude=.65,canonical=True):
 th=np.linspace(-amplitude,amplitude,161);p=np.sqrt(np.maximum(2*I*(V(amplitude)-V(th)),0));p=p if canonical else p/I
 return np.concatenate([th,th[::-1]]),np.concatenate([p,-p[::-1]])
if __name__=='__main__':
 import json
 w=np.linspace(-1.6,1.6,201);p=momentum(w);L=lagrangian(FIXED_THETA,w);H=hamiltonian(FIXED_THETA,p)
 eps=1e-5;slope=(lagrangian(FIXED_THETA,w+eps)-lagrangian(FIXED_THETA,w-eps))/(2*eps)
 assert np.max(abs(slope-p))<1e-8
 assert np.max(abs((p*w-L)-H))<1e-12
 assert np.max(abs((L-p*w)+H))<1e-12
 assert np.max(abs(p/I-w))<1e-12
 for amp in [.35,.65,.95,1.1]:
  th,q=contour(amp);assert np.max(abs(hamiltonian(th,q)-V(amp)))<1e-12
 e=MODEL.energy();assert np.max(abs(e-e[0]))/e[0]<1e-7
 report=dict(momentum_equals_L_velocity_derivative=True,legendre_identity=True,tangent_intercept_equals_negative_H=True,invertible_velocity_hessian=I,exact_nonlinear_energy_contours=True,period_seconds=PERIOD,initial_angle=.65,angular_momentum_scale=I)
 Path(__file__).with_name('physics_validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(report)
