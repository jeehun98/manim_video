"""Reuse established pendulum/quantum models; add exact Kepler and canonical weights."""
from pathlib import Path
import importlib.util,numpy as np,json,hashlib
s=importlib.util.spec_from_file_location('shared_connection_models',Path(__file__).resolve().parents[1]/'chapter_06/mechanics.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
MODEL,I,A,EC,H,field,contour,packet,INITIAL,X,psi,rho=m.MODEL,m.I,m.A,m.EC,m.H,m.field,m.contour,m.packet,m.INITIAL,m.X,m.psi,m.rho
HISTORY_T=np.linspace(0,2,101);HISTORY_Q=np.interp(HISTORY_T,MODEL.times,MODEL.states[:,0]);HISTORY_W=np.interp(HISTORY_T,MODEL.times,MODEL.states[:,1])
ENERGIES=np.arange(4,dtype=float)
def probabilities(kbt=1):
 weights=np.exp(-ENERGIES/kbt);return weights/weights.sum()
def orbit(t,e=.4,a=1.,mu=1.):
 n=np.sqrt(mu/a**3);M=np.asarray(t)*n;E=np.array(M,dtype=float)
 for _ in range(10):E-=(E-e*np.sin(E)-M)/(1-e*np.cos(E))
 q=np.stack([a*(np.cos(E)-e),a*np.sqrt(1-e*e)*np.sin(E)],axis=-1)
 vel=np.stack([-a*np.sin(E)*n/(1-e*np.cos(E)),a*np.sqrt(1-e*e)*np.cos(E)*n/(1-e*np.cos(E))],axis=-1)
 return q,vel
if __name__=='__main__':
 t=np.linspace(0,2*np.pi,1001);q,v=orbit(t);r=np.linalg.norm(q,axis=-1);energy=.5*np.sum(v*v,axis=-1)-1/r
 assert np.max(abs(energy+.5))<1e-12
 angular=q[:,0]*v[:,1]-q[:,1]*v[:,0];assert np.ptp(angular)<1e-12
 dt=1e-5;qp,vp=orbit(t+dt);qm,vm=orbit(t-dt)
 assert np.max(abs((qp-qm)/(2*dt)-v))<1e-8
 assert np.max(abs((vp-vm)/(2*dt)+q/r[:,None]**3))<1e-8
 for temp in [.2,1,2,10]:
  p=probabilities(temp);assert np.all(p>0) and abs(p.sum()-1)<1e-12 and np.all(np.diff(p)<0)
  assert np.allclose(p[1:]/p[:-1],np.exp(-1/temp))
 root=Path(__file__).resolve().parent
 result=dict(kepler_energy_error=float(np.max(abs(energy+.5))),kepler_angular_momentum_constant=True,hamilton_equations_verified=True,canonical_probabilities=probabilities().tolist(),canonical_normalized=True,canonical_conditions='four distinct microstates E=0,1,2,3; kB*T=1; thermal equilibrium at fixed temperature',shared_pendulum_and_quantum='unchanged chapter06 model',shared_validation=json.loads((root/'../chapter_06/physics_validation.json').read_text(encoding='utf-8')))
 (root/'physics_validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print('PASS exact Kepler Hamiltonian flow and normalized canonical probabilities')
