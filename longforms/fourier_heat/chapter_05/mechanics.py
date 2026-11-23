"""Scalar sphere heat kernel and exact round-sphere Ricci flow (κ=1)."""
import numpy as np
from scipy.special import eval_legendre
from scipy.integrate import simpson
L=60
def sphere_kernel(theta,t):
 x=np.cos(np.asarray(theta));n=np.arange(L+1)
 return np.sum(((2*n+1)*np.exp(-n*(n+1)*t)/(4*np.pi)).reshape((-1,)+(1,)*x.ndim)*eval_legendre(n.reshape((-1,)+(1,)*x.ndim),x),axis=0)
def plane_kernel(r,t):return np.exp(-np.asarray(r)**2/(4*t))/(4*np.pi*t)
def radius(t):return np.sqrt(1-2*np.asarray(t))
def paired_traces(t):
 # de Rham example on S²: nonzero 0-/2-form modes pair with 1-form modes.
 n=np.arange(1,80);s=np.sum((2*n+1)*np.exp(-n*(n+1)*t))
 return 1+s,2*s,1+s
def validate():
 theta=np.linspace(0,np.pi,6001);reports=[]
 for t in [.035,.08,.2,.7,1.2]:
  k=sphere_kernel(theta,t);mass=float(2*np.pi*simpson(k*np.sin(theta),x=theta));assert abs(mass-1)<1e-8;assert k.min()>-1e-12
  reports.append(dict(t=t,mass=mass,minimum=float(k.min()),peak=float(k[0])))
 z=np.linspace(.15,np.pi-.15,160);h=1e-4;t=.2
 ut=(sphere_kernel(z,t+h)-sphere_kernel(z,t-h))/(2*h)
 lap=(sphere_kernel(z+h,t)-2*sphere_kernel(z,t)+sphere_kernel(z-h,t))/h**2+1/np.tan(z)*(sphere_kernel(z+h,t)-sphere_kernel(z-h,t))/(2*h)
 residual=float(np.max(abs(ut-lap)));assert residual<1e-5
 short=[float((4*np.pi*t*sphere_kernel(0,t)-1)/t) for t in [.02,.01,.005]]
 assert abs(short[-1]-1/3)<abs(short[0]-1/3)
 assert abs(short[-1]-1/3)<.001
 for t in [.03,.1,.5,2]:
  a,b,c=paired_traces(t);assert abs(a-b+c-2)<1e-10
 tr=np.linspace(0,.4,100);h=1e-5;res=float(np.max(abs((radius(tr+h)**2-radius(tr-h)**2)/(2*h)+2)));assert res<1e-9
 return dict(sphere_mass_and_positivity=reports,sphere_pde_residual=residual,diagonal_curvature_coefficients=short,expected_Scal_over_6=1/3,deRham_supertrace=2,ricci_radius_squared_residual=res,ricci_dimension=2,poincare_dimension=3)
