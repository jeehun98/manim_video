"""Exact periodic Fourier example; all plotted quantities come from here."""
import numpy as np
K=np.array([1.,3.,5.]);A=np.array([1.,.5,.25]);KAPPA=.12
TAU=2*np.pi
def component(x,j,t=0):return A[j]*np.exp(-KAPPA*K[j]**2*t)*np.sin(K[j]*np.asarray(x))
def solution(x,t=0):return sum(component(x,j,t) for j in range(3))
def square_partial(x,n):return 4/np.pi*sum(np.sin((2*j+1)*np.asarray(x))/(2*j+1) for j in range(n))
def product_integral(x,m=1,n=3):
 x=np.asarray(x)
 return x/2-np.sin(2*m*x)/(4*m) if m==n else .5*(np.sin((m-n)*x)/(m-n)-np.sin((m+n)*x)/(m+n))
def validate():
 x=np.linspace(0,TAU,30001)
 gram=np.array([[np.trapezoid(np.sin(m*x)*np.sin(n*x),x) for n in K] for m in K])
 coeff=np.array([np.trapezoid(solution(x)*np.sin(k*x),x)/np.pi for k in K])
 assert np.allclose(gram,np.eye(3)*np.pi,atol=1e-12)
 assert np.allclose(coeff,A,atol=1e-12)
 h=1e-4;t=.5;z=x[::20]
 ut=(solution(z,t+h)-solution(z,t-h))/(2*h)
 uxx=(solution(z+h,t)-2*solution(z,t)+solution(z-h,t))/h**2
 residual=float(np.max(abs(ut-KAPPA*uxx)));assert residual<1e-5
 assert np.allclose(solution(0,t),solution(TAU,t),atol=1e-12)
 assert abs(sum(A*K*np.exp(-KAPPA*K*K*t))-sum(A*K*np.exp(-KAPPA*K*K*t)*np.cos(K*TAU)))<1e-12
 energies=[float(np.trapezoid(solution(x,t)**2,x)) for t in [0,.2,1,3]]
 assert all(a>b for a,b in zip(energies,energies[1:]))
 assert abs(np.trapezoid(solution(x,2),x))<1e-12
 err=[float(np.trapezoid((square_partial(x,n)-np.sign(np.sin(x)))**2,x)) for n in [1,3,10,30]]
 assert all(a>b for a,b in zip(err,err[1:]))
 return dict(gram=gram.tolist(),coefficients=coeff.tolist(),pde_max_residual=residual,periodic_boundaries=True,energies=energies,square_partial_L2_error=err)
