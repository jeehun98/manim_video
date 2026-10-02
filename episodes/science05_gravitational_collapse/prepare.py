"""Deterministic softened gravity illustration, not a precision halo simulation."""
from pathlib import Path
import numpy as np

def generate():
    rng=np.random.default_rng(81)
    n=72;mass=1/n;eps=.065;dt=.003
    directions=rng.normal(size=(n,3));directions/=np.linalg.norm(directions,axis=1)[:,None]
    pos=directions*rng.random(n)[:,None]**(1/3)
    pos[:,0]*=1.08;pos[:,1]*=.95;pos-=pos.mean(axis=0)
    vel=rng.normal(scale=.08,size=(n,3));vel-=vel.mean(axis=0)
    def force(p):
        delta=p[None,:,:]-p[:,None,:]
        r2=np.sum(delta*delta,axis=2)+eps*eps
        np.fill_diagonal(r2,np.inf)
        return mass*np.sum(delta/r2[:,:,None]**1.5,axis=1)
    def quantities(p,v):
        delta=p[None,:,:]-p[:,None,:];r2=np.sum(delta*delta,axis=2)+eps*eps
        np.fill_diagonal(r2,np.inf)
        potential=-.5*mass*mass*np.sum(1/np.sqrt(r2))
        kinetic=.5*mass*np.sum(v*v)
        individual=.5*np.sum(v*v,axis=1)-mass*np.sum(1/np.sqrt(r2),axis=1)
        return kinetic,potential,individual
    positions=[];velocities=[];energies=[];radii=[];times=[]
    acc=force(pos)
    for step in range(8001):
        if step%10==0:
            k,u,_=quantities(pos,vel)
            positions.append(pos.copy());velocities.append(vel.copy());energies.append((k,u))
            radii.append(np.median(np.linalg.norm(pos-pos.mean(axis=0),axis=1)));times.append(step*dt)
        if step==8000:break
        next_pos=pos+vel*dt+.5*acc*dt*dt
        next_acc=force(next_pos);vel+=.5*(acc+next_acc)*dt;pos=next_pos;acc=next_acc
    _,_,individual=quantities(pos,vel)
    np.savez_compressed(Path(__file__).with_name('collapse_data.npz'),positions=positions,velocities=velocities,
                        energies=energies,radii=radii,times=times,bound=individual<0,softening=eps)
    energy=np.array(energies)
    print('Energy drift:',np.ptp(energy.sum(axis=1))/abs(energy[0].sum()))
    print('Bound particles:',sum(individual<0),'/',n)
    print('Minimum radius time:',times[np.argmin(radii)],'initial/min/final radii:',radii[0],min(radii),np.mean(radii[-200:]))
    print('Late mean 2K/|U|:',2*energy[-200:,0].mean()/abs(energy[-200:,1].mean()))

if __name__=='__main__':generate()
