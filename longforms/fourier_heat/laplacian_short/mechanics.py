"""Analytic constant-coefficient heat models; separate explicit boundary conditions."""
import numpy as np
ALPHA=.12
X=np.linspace(0,1,121)
def insulated(x,t=0):return 50+25*np.exp(-ALPHA*np.pi**2*t)*np.cos(np.pi*x)+8*np.exp(-ALPHA*9*np.pi**2*t)*np.cos(3*np.pi*x)
def slope(x):return -25*np.pi*np.sin(np.pi*x)-24*np.pi*np.sin(3*np.pi*x)
def steady(x):return 80-60*x
def component(x,n,t=0):return {1:40,3:12,5:5}[n]*np.exp(-ALPHA*(n*np.pi)**2*t)*np.sin(n*np.pi*x)
def fourier(x,t=0):return sum(component(x,n,t) for n in [1,3,5])
def validate():
 x=np.linspace(.01,.99,101);h=1e-4;t=.3
 dt=(insulated(x,t+h)-insulated(x,t-h))/(2*h);dxx=(insulated(x+h,t)-2*insulated(x,t)+insulated(x-h,t))/h**2
 assert np.max(abs(dt-ALPHA*dxx))<.001
 assert abs(slope(0))+abs(slope(1))<1e-10
 assert abs(np.trapezoid(insulated(X,0),X)-np.trapezoid(insulated(X,1),X))<1e-10
 for n in [1,3,5]:
  dxx=(component(x+h,n,t)-2*component(x,n,t)+component(x-h,n,t))/h**2
  assert np.max(abs(dxx+(n*np.pi)**2*component(x,n,t)))<.001
 assert np.max(abs(fourier(np.array([0.,1.]),t)))<1e-10
 assert np.max(abs((steady(x+h)-2*steady(x)+steady(x-h))/h**2))<.001
 return dict(analytic_heat_equation=True,insulated_mean_conserved=True,steady_flux=60,sine_boundary_zero=True,modal_eigenvalues=[-(n*np.pi)**2 for n in [1,3,5]])

