"""Uniform inextensible chain: exact continuous candidates and projected dynamics."""
from pathlib import Path
from functools import lru_cache
import json
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
B=.8;A=1.;R=float(np.cosh(B));L=float(2*np.sinh(B));P=Path(__file__).resolve().parent
def height(x,alpha=0,beta=None):
    beta=coefficient(float(alpha)) if beta is None else beta
    return np.cosh(x)+alpha*np.sin(np.pi*x/B)+beta*np.cos(np.pi*x/(2*B))
def slope(x,alpha=0,beta=None):
    beta=coefficient(float(alpha)) if beta is None else beta
    return np.sinh(x)+alpha*np.pi/B*np.cos(np.pi*x/B)-beta*np.pi/(2*B)*np.sin(np.pi*x/(2*B))
@lru_cache(maxsize=4096)
def coefficient(alpha):
    if abs(alpha)<1e-12:return 0.
    def f(beta):return quad(lambda x:np.sqrt(1+slope(x,alpha,beta)**2),-B,B,epsabs=1e-12,epsrel=1e-12)[0]-L
    return float(brentq(f,0,.25,xtol=1e-13))
def integrals(alpha):
    beta=coefficient(alpha)
    length=quad(lambda x:np.sqrt(1+slope(x,alpha,beta)**2),-B,B,epsabs=1e-12)[0]
    energy=quad(lambda x:height(x,alpha,beta)*np.sqrt(1+slope(x,alpha,beta)**2),-B,B,epsabs=1e-12)[0]
    return dict(alpha=alpha,beta=beta,length=length,energy=energy,left=float(height(-B,alpha,beta)),right=float(height(B,alpha,beta)))
def equal_arc_nodes(alpha,n=33):
    x=np.linspace(-B,B,20001);y=height(x,alpha)
    arc=np.r_[0,np.cumsum(np.sqrt(np.diff(x)**2+np.diff(y)**2))]
    xi=np.interp(np.linspace(0,arc[-1],n),arc,x)
    return np.c_[xi,np.zeros(n),height(xi,alpha)]
def generate():
    n=33;ell=L/(n-1);dt=1/240;steps=3360
    q=equal_arc_nodes(.1,n);weights=np.ones(n);weights[[0,-1]]=0
    pins=q[[0,-1]].copy();groups=[np.arange(0,n-1,2),np.arange(1,n-1,2)]
    def project(q,iterations):
        for _ in range(iterations):
            for idx in groups:
                d=q[idx+1]-q[idx];dist=np.linalg.norm(d,axis=1)
                corr=d*((dist-ell)/(dist*(weights[idx]+weights[idx+1])))[:,None]
                q[idx]+=weights[idx,None]*corr;q[idx+1]-=weights[idx+1,None]*corr
        q[[0,-1]]=pins
    project(q,3000);v=np.zeros_like(q);m=np.full(n,ell);m[[0,-1]]*=.5
    frames=[];times=[];us=[];ks=[];res=[]
    for k in range(steps+1):
        if k%4==0:
            frames.append(q.copy());times.append(k*dt);us.append(float(m@q[:,2]));ks.append(float(.5*np.sum(m[:,None]*v*v)));res.append(float(np.max(np.abs(np.linalg.norm(np.diff(q,axis=0),axis=1)-ell))))
        if k==steps:break
        old=q.copy();v[:,2]-=dt;v*=np.exp(-1.1*dt);q+=dt*v;q[[0,-1]]=pins
        project(q,100);v=(q-old)/dt;v[[0,-1]]=0
    frames=np.array(frames);np.savez_compressed(P/'dynamics.npz',positions=frames,times=times,U=us,K=ks,segment_error=res)
    data=dict(a=A,b=B,R=R,length=L,mass_per_length=1,gravity=1,energy_reference='y=0; same reference and total mass for all candidates',candidates=[integrals(a) for a in [0,.07,-.1,.12]],dynamics=dict(nodes=n,segment_length=ell,dt=dt,projection_iterations=100,drag=1.1,seconds=steps*dt,max_segment_error=max(res),max_endpoint_error=float(np.max(np.abs(frames[:,[0,-1]]-pins))),initial_mechanical_energy=us[0]+ks[0],final_mechanical_energy=us[-1]+ks[-1],potential_increase_steps=int(np.sum(np.diff(us)>1e-7)),max_positive_mechanical_increment=float(np.max(np.diff(np.array(us)+ks))),final_speed=float(np.max(np.linalg.norm(v,axis=1))),note='PBD distance constraints; numerical dissipation included, not a fluid or rigid-link contact simulation'),catenoid=dict(a=1,height=1.6,R=R,stable_branch=.8*np.tanh(.8)))
    (P/'geometry.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(data,ensure_ascii=False,indent=2))
if __name__=='__main__':generate()
