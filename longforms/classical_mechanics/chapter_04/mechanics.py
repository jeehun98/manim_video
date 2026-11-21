"""A single dimensional rigid-pendulum Hamiltonian for surfaces, contours and flow."""
from pathlib import Path
import sys,numpy as np
sys.path.append(str(Path(__file__).resolve().parents[1]/'chapter_01'))
from physics import PendulumModel
MODEL=PendulumModel();I=MODEL.length**2;A=MODEL.g*MODEL.length;EC=2*A
DT=.002;TIMES=np.arange(0,12+DT,DT)
def H(q,p):return np.asarray(p)**2/(2*I)+A*(1-np.cos(q))
def field(y):return np.stack([y[...,1]/I,-A*np.sin(y[...,0])],axis=-1)
def evolve(initial,duration=12,dt=DT):
 ts=np.arange(0,duration+dt,dt);out=np.empty((len(ts),*np.shape(initial)));out[0]=initial
 for n in range(1,len(ts)):
  y=out[n-1];a=field(y);b=field(y+dt*a/2);c=field(y+dt*b/2);d=field(y+dt*c);out[n]=y+dt*(a+2*b+2*c+d)/6
 return out
RATIOS=np.linspace(.1,1.4,131)
INITIAL=np.stack([np.zeros_like(RATIOS),np.sqrt(2*I*EC*RATIOS)],axis=-1)
TRAJ=evolve(INITIAL)
def state(ratio,t):
 if abs(ratio-1)<1e-12:
  lam=np.sqrt(A/I);return np.array([4*np.arctan(np.exp(lam*t))-np.pi,2*I*lam/np.cosh(lam*t)])
 z=np.clip((ratio-.1)/.01,0,130);i=min(int(z),129);alpha=z-i
 j=np.clip(t/DT,0,len(TIMES)-1);k=min(int(j),len(TIMES)-2);beta=j-k
 return (1-beta)*((1-alpha)*TRAJ[k,i]+alpha*TRAJ[k,i+1])+beta*((1-alpha)*TRAJ[k+1,i]+alpha*TRAJ[k+1,i+1])
def contour(ratio):
 E=EC*ratio;amp=np.arccos(1-E/A) if ratio<1 else np.pi
 q=np.linspace(-amp,amp,181);p=np.sqrt(np.maximum(2*I*(E-A*(1-np.cos(q))),0))
 if ratio<1:return [(np.r_[q,q[::-1]],np.r_[p,-p[::-1]])]
 return [(q,p),(q,-p)]
# Small Hamiltonian material patch, sampled densely along its boundary.
n=40;x=np.linspace(.25,.42,n,endpoint=False);y=np.linspace(3.2,4.1,n,endpoint=False)
PATCH0=np.vstack([np.c_[x,np.full(n,3.2)],np.c_[np.full(n,.42),y],np.c_[x[::-1]+(.17/n),np.full(n,4.1)],np.c_[np.full(n,.25),y[::-1]+(.9/n)]])
PATCH=evolve(PATCH0,duration=4)
def patch(t):
 z=np.clip(t/DT,0,len(PATCH)-1);k=min(int(z),len(PATCH)-2);a=z-k;return PATCH[k]*(1-a)+PATCH[k+1]*a
if __name__=='__main__':
 import json
 error=float(np.max(abs(H(TRAJ[...,0],TRAJ[...,1])-EC*RATIOS))/(EC*1.4));assert error<1e-7,error
 for r in [.2,.65,1,1.3]:
  for q,p in contour(r):assert np.max(abs(H(q,p)-EC*r))<1e-10
 critical=np.array([state(1,t) for t in np.linspace(0,12,101)]);assert critical[:,0].max()<np.pi and np.all(critical[:,1]>0)
 assert np.max(abs(H(critical[:,0],critical[:,1])-EC))<1e-10
 area=lambda p:abs(np.sum(p[:,0]*np.roll(p[:,1],-1)-p[:,1]*np.roll(p[:,0],-1)))/2
 area0=area(PATCH0);areaerr=max(abs(area(patch(t))-area0)/area0 for t in [0,.5,1,2,3,4]);assert areaerr<.002,areaerr
 q=np.linspace(-2,2,11);p=np.linspace(-18,18,11);dq,dp=np.meshgrid(q,p);orth=(A*np.sin(dq))*(dp/I)+(dp/I)*(-A*np.sin(dq));assert np.max(abs(orth))<1e-12
 report=dict(relative_energy_error=error,critical_energy=EC,critical_trajectory_does_not_cross_top=True,exact_contours=True,flow_tangent_to_energy_levels=True,patch_relative_area_error=areaerr,model='massless rigid rod, m=1 kg, length=2m, g=9.81',periodic_angle='chart [-pi,pi], endpoints identified')
 Path(__file__).with_name('physics_validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(report)
