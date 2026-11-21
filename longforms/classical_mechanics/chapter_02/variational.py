"""Admissible endpoint-fixed histories, L(t), and numerical signed actions."""
from pathlib import Path
import sys,numpy as np
sys.path.append(str(Path(__file__).resolve().parents[1]/'chapter_01'))
from physics import PendulumModel
MODEL=PendulumModel()
DURATION=1.2
TIME=np.linspace(0,DURATION,2401)
THETA=np.interp(TIME,MODEL.times,MODEL.states[:,0]);OMEGA=np.interp(TIME,MODEL.times,MODEL.states[:,1])
LENGTH=MODEL.length;G=MODEL.g
EPS=np.linspace(-.35,.35,281)
def history(epsilon=0,mode=1,times=TIME):
 th=np.interp(times,TIME,THETA);om=np.interp(times,TIME,OMEGA)
 phase=mode*np.pi*times/DURATION
 return th+epsilon*np.sin(phase),om+epsilon*mode*np.pi/DURATION*np.cos(phase)
def energies(th,om):return .5*LENGTH**2*om**2,G*LENGTH*(1-np.cos(th))
def lagrangian(epsilon=0,mode=1,times=TIME):
 th,om=history(epsilon,mode,times);T,V=energies(th,om);return T-V
def action(epsilon=0,mode=1):return float(np.trapezoid(lagrangian(epsilon,mode),TIME))
ACTIONS={k:np.array([action(e,k) for e in EPS]) for k in (1,2,3)}
S0=action()
def action_at(e,mode=1):return float(np.interp(e,EPS,ACTIONS[mode]))
if __name__=='__main__':
 import json
 errors=[]
 for mode in (1,2,3):
  h=1e-4;derivative=(action(h,mode)-action(-h,mode))/(2*h)
  assert abs(derivative)<2e-5,(mode,derivative)
  for e in [-.35,.35]:
   th,om=history(e,mode);assert np.max(abs(th[[0,-1]]-THETA[[0,-1]]))<1e-12
  errors.append(dict(mode=mode,first_variation=derivative))
 assert abs(S0)>.01
 energy=MODEL.energy();err=float(np.max(abs(energy-energy[0]))/energy[0]);assert err<1e-7
 report=dict(time_interval=DURATION,action_at_actual_history=S0,endpoint_preserved=True,variations=errors,relative_energy_error=err,quadrature='2401 points, signed trapezoid',conditions='fixed times and positions; virtual velocities derived from the varied histories')
 Path(__file__).with_name('physics_validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(report)
