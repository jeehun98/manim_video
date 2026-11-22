"""Exact Gaussian convolution of bounded positive step data on R."""
import numpy as np
from scipy.special import erf
K=.65
INTERVALS=[(-3.4,-2.8,37),(-2.4,-2.12,75),(-1.65,-.75,44),(-.35,.25,12),(.65,1.45,63),(1.85,2.65,29),(3.0,3.45,46)]
X=np.linspace(-4.5,4.5,241)
def initial(x):
 x=np.asarray(x);v=np.full_like(x,20.,dtype=float)
 for a,b,h in INTERVALS:v+=h*((x>=a)&(x<b))
 return v
def solution(x,t):
 if t<=0:return initial(x)
 x=np.asarray(x);v=np.full_like(x,20.,dtype=float);s=np.sqrt(4*K*t)
 for a,b,h in INTERVALS:v+=h*.5*(erf((x-a)/s)-erf((x-b)/s))
 return v
def slope(x,t):
 x=np.asarray(x);v=np.zeros_like(x,dtype=float);s=np.sqrt(4*K*t)
 for a,b,h in INTERVALS:v+=h/(np.sqrt(np.pi)*s)*(np.exp(-((x-a)/s)**2)-np.exp(-((x-b)/s)**2))
 return v
def step_points():
 xs=[-4.5];ys=[20.]
 for a,b,h in INTERVALS:xs.extend([a,a,b,b]);ys.extend([20,20+h,20+h,20])
 xs.append(4.5);ys.append(20);return np.array(xs),np.array(ys)
def kernel(z,t):return np.exp(-np.asarray(z)**2/(4*K*t))/np.sqrt(4*np.pi*K*t)
def lower(x,y,t1,t2):return float(solution(x,t1)*np.sqrt(t1/t2)*np.exp(-(x-y)**2/(4*K*(t2-t1))))
RNG=np.random.default_rng(20261122);T=.45;N=160
PATHS=np.c_[np.zeros(1200),np.cumsum(RNG.normal(0,np.sqrt(2*K*T/N),(1200,N)),axis=1)]
ENDPOINTS=PATHS[:,-1]
