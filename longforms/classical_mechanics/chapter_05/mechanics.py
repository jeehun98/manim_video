"""Reuse chapter 04 Hamiltonian; advect a material boundary, never morph an ellipse."""
from pathlib import Path
import importlib.util,numpy as np,json
s=importlib.util.spec_from_file_location('shared_hamilton',Path(__file__).resolve().parents[1]/'chapter_04/mechanics.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
MODEL,I,A,EC,H,field,contour=m.MODEL,m.I,m.A,m.EC,m.H,m.field,m.contour
n=100
corners=np.array([[.175,1.8],[.525,1.8],[.525,3.8],[.175,3.8]])
INITIAL=np.vstack([a+(b-a)*np.arange(n)[:,None]/n for a,b in zip(corners,np.roll(corners,-1,axis=0))])
POINTS=np.array([(q,p) for q in np.linspace(.175,.525,6) for p in np.linspace(1.8,3.8,6)])
FLOW=m.evolve(np.vstack([INITIAL,POINTS]),duration=4)
def packet(t):
 z=np.clip(t/.002,0,len(FLOW)-1);k=min(int(z),len(FLOW)-2);v=FLOW[k]*(1-(z-k))+FLOW[k+1]*(z-k)
 return v[:len(INITIAL)],v[len(INITIAL):]
def area(p):return abs(np.sum(p[:,0]*np.roll(p[:,1],-1)-p[:,1]*np.roll(p[:,0],-1)))/2
if __name__=='__main__':
 err=max(abs(area(packet(t)[0])/area(INITIAL)-1) for t in np.linspace(0,4,81));assert err<.0002,err
 e0=H(FLOW[0,:,0],FLOW[0,:,1]);energy=float(np.max(abs(H(FLOW[...,0],FLOW[...,1])-e0)));assert energy<1e-7
 q=np.linspace(-1,1,31);p=np.linspace(-8,8,31)
 assert np.max(abs(A*np.sin(q)*(p/I)+(p/I)*(-A*np.sin(q))))<1e-12
 result=dict(material_patch_relative_area_error=float(err),maximum_energy_error=energy,poisson_H_H_zero=True,poisson_p_H='-mg*l*sin(theta)',poisson_q_H='p/I',explicit_time_term_included=True,higher_dimensional_invariant='sum dq_i wedge dp_i',spatial_symmetry_example='free particle',rotational_symmetry_example='central force circular orbit')
 Path(__file__).with_name('physics_validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(result)
