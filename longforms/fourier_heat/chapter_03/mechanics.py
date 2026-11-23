"""Analytic periodic heat evolution, its derivatives and a real Harnack bound."""
import numpy as np
from scipy.special import erf
KAPPA=.4;PERIOD=2*np.pi
def initial(x):
 x=(np.asarray(x)+np.pi)%PERIOD-np.pi
 block=100*((x>-1.6)&(x<-.5)).astype(float)
 block=np.where(np.isclose(x,-1.6,atol=1e-12)|np.isclose(x,-.5,atol=1e-12),50,block)
 return block+85*np.maximum(0,1-np.abs(x-1.2)/.55)
def _H(z,t,order=0):
 s=np.sqrt(4*KAPPA*t);e=np.exp(-(z/s)**2)
 if order==0:return .5*z*(1+erf(z/s))+np.sqrt(KAPPA*t/np.pi)*e
 if order==1:return .5*(1+erf(z/s))
 if order==2:return e/(s*np.sqrt(np.pi))
 if order==3:return -2*z*e/(s**3*np.sqrt(np.pi))
 raise ValueError(order)
def _step(z,t,order=0):
 s=np.sqrt(4*KAPPA*t);e=np.exp(-(z/s)**2)/(s*np.sqrt(np.pi))
 if order==0:return .5*(1+erf(z/s))
 if order==1:return e
 if order==2:return -2*z/s**2*e
 if order==3:return (4*z*z/s**4-2/s**2)*e
 raise ValueError(order)
def temperature(x,t,order=0):
 x=np.asarray(x,dtype=float)
 if t<=0:
  if order:raise ValueError('Discontinuous initial data have no classical derivative')
  return initial(x)
 out=np.zeros_like(x)
 # Images beyond ±3 have negligible tails for the displayed t<=4, κ=.4.
 for j in range(-3,4):
  z=x-j*PERIOD
  out+=100*(_step(z+1.6,t,order)-_step(z+.5,t,order))
  out+=85/.55*(_H(z-.65,t,order)-2*_H(z-1.2,t,order)+_H(z-1.75,t,order))
 return out
def mode_coeff(n):
 mean=(110+85*.55)/PERIOD
 if n==0:return mean,0.
 an=100*(np.sin(-.5*n)-np.sin(-1.6*n))/(np.pi*n)
 bn=100*(np.cos(-1.6*n)-np.cos(-.5*n))/(np.pi*n)
 amp=85*.55/np.pi*np.sinc(n*.55/(2*np.pi))**2
 return an+amp*np.cos(n*1.2),bn+amp*np.sin(n*1.2)
def mode(x,n,t=0):
 a,b=mode_coeff(n);return (a*np.cos(n*np.asarray(x))+b*np.sin(n*np.asarray(x)))*np.exp(-KAPPA*n*n*t)
def kernel(x,t):return np.exp(-np.asarray(x)**2/(4*KAPPA*t))/np.sqrt(4*np.pi*KAPPA*t)
def harnack(x,y,t1,t2):
 assert 0<t1<t2
 C=np.sqrt(t2/t1)*np.exp((x-y)**2/(4*KAPPA*(t2-t1)))
 a=float(kernel(x,t1));b=float(kernel(y,t2));return dict(x=x,y=y,t1=t1,t2=t2,C=float(C),A=a,B=b,lower=a/float(C))
def validate():
 x=np.linspace(-np.pi,np.pi,6001);energies=[];ranges=[];means=[]
 for t in [.015,.05,.2,1,3.5]:
  u=temperature(x,t);assert u.min()>-1e-8 and u.max()<100+1e-8
  ranges.append([float(u.min()),float(u.max())]);means.append(float(np.trapezoid(u,x)/PERIOD));energies.append(float(np.trapezoid(u*u,x)))
 assert np.ptp(means)<1e-8
 assert all(a>b for a,b in zip(energies,energies[1:]))
 h=1e-4;z=np.linspace(-3,3,401);t=.3
 ut=(temperature(z,t+h)-temperature(z,t-h))/(2*h)
 residual=float(np.max(abs(ut-KAPPA*temperature(z,t,2))));assert residual<2e-5
 derr=[]
 for d in [1,2,3]:
  numeric=(temperature(z+h,t,d-1)-temperature(z-h,t,d-1))/(2*h)
  err=float(np.max(abs(numeric-temperature(z,t,d))));assert err<1e-4;derr.append(err)
 assert np.allclose(temperature(-np.pi,.3),temperature(np.pi,.3),atol=1e-9)
 assert np.allclose(temperature(-np.pi,.3,1),temperature(np.pi,.3,1),atol=1e-9)
 spectral=mode_coeff(0)[0]+sum(mode(z,n,.3) for n in range(1,65))
 spectral_error=float(np.max(abs(spectral-temperature(z,.3))));assert spectral_error<1e-9
 cases=[harnack(a,b,t1,t2) for a in [-1,0,1] for b in [-2,-1.2,0,1.2,2] for t1,t2 in [(.3,.8),(.6,1.6),(1,2)]]
 assert all(c['B']+1e-12>=c['lower'] for c in cases)
 return dict(pde_max_residual=residual,derivative_errors=derr,spectral_kernel_error=spectral_error,temperature_ranges=ranges,mean_temperature=means[0],energy_decreases=True,harnack_cases=len(cases),displayed_harnack=harnack(0,1.2,.6,1.6))
