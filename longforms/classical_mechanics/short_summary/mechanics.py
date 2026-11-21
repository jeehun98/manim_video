"""Shared longform physics, with one stationary-action check for the short."""
from pathlib import Path
import importlib.util,numpy as np,json
s=importlib.util.spec_from_file_location('classical_quantum_shared',Path(__file__).resolve().parents[1]/'chapter_06/mechanics.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
MODEL,I,A,EC,H,field,contour,packet,INITIAL,X,psi,rho=m.MODEL,m.I,m.A,m.EC,m.H,m.field,m.contour,m.packet,m.INITIAL,m.X,m.psi,m.rho
HISTORY_T=np.linspace(0,2,1001)
HISTORY_Q=np.interp(HISTORY_T,MODEL.times,MODEL.states[:,0]);HISTORY_W=np.interp(HISTORY_T,MODEL.times,MODEL.states[:,1])
def action(e):
 q=HISTORY_Q+e*np.sin(np.pi*HISTORY_T/2);w=HISTORY_W+e*np.pi/2*np.cos(np.pi*HISTORY_T/2)
 return np.trapezoid(.5*I*w*w-A*(1-np.cos(q)),HISTORY_T)
if __name__=='__main__':
 derivative=(action(.0001)-action(-.0001))/.0002;assert abs(derivative)<.0002,derivative
 prior=json.loads((Path(__file__).resolve().parents[1]/'chapter_05/physics_validation.json').read_text(encoding='utf-8'))
 quantum=json.loads((Path(__file__).resolve().parents[1]/'chapter_06/physics_validation.json').read_text(encoding='utf-8'))
 report=dict(shared_classical=prior,shared_quantum=quantum,stationary_action_first_variation=float(derivative),action_not_zero=float(action(0)),canonical_momentum='p_theta=I*omega, I=m*l^2',same_model_for_energy_path_phase_and_vector_field=True)
 Path(__file__).with_name('physics_validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('PASS stationary action derivative',derivative)
