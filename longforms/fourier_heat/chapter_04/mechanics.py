"""One reproducible dataset, exact heat semigroup and risk-neutral GBM example."""
from functools import lru_cache
import numpy as np
from scipy.special import ndtr
KAPPA=1.;DT=.01;N=4096;X0=.6;HEAT_T=.8
RATE=.04;SIGMA=.2;STRIKE=100.;S0=100.;MATURITY=1.
def f(x):
 x=np.asarray(x);return 40+18*np.cos(x)+9*np.sin(2*x)+5*np.cos(4*x)
def f2(x):return -18*np.cos(x)-36*np.sin(2*x)-80*np.cos(4*x)
def heat(x,t):return 40+18*np.exp(-KAPPA*t)*np.cos(x)+9*np.exp(-4*KAPPA*t)*np.sin(2*x)+5*np.exp(-16*KAPPA*t)*np.cos(4*x)
def density(y,t,x=0):return np.exp(-(np.asarray(y)-x)**2/(4*KAPPA*t))/np.sqrt(4*np.pi*KAPPA*t)
def potential(x):return .15+.06*np.sin(x)
def call(s,remaining):
 s=np.asarray(s,dtype=float)
 if remaining<=0:return np.maximum(s-STRIKE,0)
 d1=(np.log(s/STRIKE)+(RATE+.5*SIGMA**2)*remaining)/(SIGMA*np.sqrt(remaining));d2=d1-SIGMA*np.sqrt(remaining)
 return s*ndtr(d1)-STRIKE*np.exp(-RATE*remaining)*ndtr(d2)
def transformed(x,tau):
 q=2*RATE/SIGMA**2;a=(1-q)/2;b=-(q+1)**2/4
 return np.exp(-a*np.asarray(x)-b*tau)*call(STRIKE*np.exp(x),2*tau/SIGMA**2)/STRIKE
@lru_cache(maxsize=1)
def dataset():
 rng=np.random.default_rng(20261124)
 walk=np.concatenate([np.zeros((N,1)),np.cumsum(rng.normal(0,np.sqrt(2*KAPPA*DT),(N,160)),axis=1)],axis=1)
 planar=np.concatenate([np.zeros((8,1,2)),np.cumsum(rng.normal(0,np.sqrt(2*KAPPA*.01),(8,190,2)),axis=1)],axis=1)
 z=rng.normal(0,np.sqrt(1/96),(N,96));b=np.concatenate([np.zeros((N,1)),np.cumsum(z,axis=1)],axis=1);time=np.linspace(0,1,97)
 stock=S0*np.exp((RATE-.5*SIGMA**2)*time+SIGMA*b)
 endpoints=X0+walk[:,80];values=f(endpoints);means=np.cumsum(values)/np.arange(1,N+1)
 local=X0+walk[:,:81];weights=np.exp(-np.trapezoid(potential(local),dx=DT,axis=1));weighted=values*weights
 payoff=np.maximum(stock[:,-1]-STRIKE,0);discounted=np.exp(-RATE)*payoff
 return dict(walk=walk,planar=planar,stock=stock,time=time,endpoints=endpoints,values=values,means=means,weights=weights,weighted=weighted,payoff=payoff,discounted=discounted)
def walk_at(t,indices=None):
 w=dataset()['walk'] if indices is None else dataset()['walk'][indices];u=np.clip(t/DT,0,160);k=min(159,int(u));a=u-k
 return (1-a)*w[:,k]+a*w[:,k+1]
def validate():
 d=dataset();stats=[]
 for t in [.3,.8,1.4]:
  v=walk_at(t);mean=float(v.mean());var=float(v.var());assert abs(mean)<5*np.sqrt(2*KAPPA*t/N);assert abs(var/(2*KAPPA*t)-1)<.09
  stats.append(dict(t=t,mean=mean,variance=var,theoretical_variance=2*KAPPA*t))
 x=np.linspace(-3,3,51);h=1e-4;t=.4
 res=float(np.max(abs((heat(x,t+h)-heat(x,t-h))/(2*h)-KAPPA*(heat(x+h,t)-2*heat(x,t)+heat(x-h,t))/h**2)));assert res<2e-5
 y=np.linspace(-15,15,30001);quad=float(np.trapezoid(f(y)*density(y,HEAT_T,X0),y));exact=float(heat(X0,HEAT_T));assert abs(quad-exact)<1e-9
 estimate=float(d['values'].mean());se=float(d['values'].std(ddof=1)/np.sqrt(N));assert abs(estimate-exact)<4*se
 assert np.all((d['weights']>=np.exp(-.21*HEAT_T)-1e-12)&(d['weights']<=np.exp(-.09*HEAT_T)+1e-12))
 errors=[]
 for dt in [.02,.005,.00125]:
  a=np.sqrt(2*KAPPA*dt);approx=(.5*(f(X0-a)+f(X0+a))-f(X0))/dt;errors.append(float(abs(approx-KAPPA*f2(X0))))
 assert errors[2]<errors[1]<errors[0]
 price=float(call(S0,1));mc=float(d['discounted'].mean());mcse=float(d['discounted'].std(ddof=1)/np.sqrt(N));assert abs(mc-price)<4*mcse
 assert abs(float(np.mean(d['stock'][:,-1]))-S0*np.exp(RATE))<4*float(d['stock'][:,-1].std(ddof=1))/np.sqrt(N)
 z=np.array([-.2,0,.2]);tau=.012;hx=1e-4;ht=1e-6
 tr=(transformed(z,tau+ht)-transformed(z,tau-ht))/(2*ht)-(transformed(z+hx,tau)-2*transformed(z,tau)+transformed(z-hx,tau))/hx**2
 transform_error=float(np.max(abs(tr)));assert transform_error<1e-4
 return dict(brownian_marginals=stats,heat_pde_residual=res,heat_exact=exact,gaussian_convolution=quad,sample_mean=estimate,standard_error=se,taylor_generator_errors=errors,feynman_kac_weight_range=[float(d['weights'].min()),float(d['weights'].max())],black_scholes_exact=price,discounted_GBM_estimate=mc,discounted_GBM_standard_error=mcse,heat_transform_residual=transform_error)
