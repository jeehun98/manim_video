"""Real inner products, Taylor polynomials, and Fourier examples."""
import math
import numpy as np
from scipy.integrate import quad
U=np.array([1.,1.]);V=np.array([1.,-1.]);TRANSFORM=np.diag([2.,1.])
def gram(w=1.):return np.diag([float(w),1.])
def inner(u,v,w=1.):return float(np.asarray(u)@gram(w)@np.asarray(v))
def norm(u,w=1.):return float(np.sqrt(inner(u,u,w)))
def angle(u=U,v=V,w=1.):return float(np.degrees(np.arccos(np.clip(inner(u,v,w)/(norm(u,w)*norm(v,w)),-1,1))))
def taylor(x,n):
 x=np.asarray(x);out=np.ones_like(x,dtype=float);term=np.ones_like(x,dtype=float)
 for k in range(1,n+1):term=term*x/k;out+=term
 return out
def error_bound(n):return math.e/math.factorial(n+1)
def l2_error(n):return float(np.sqrt(quad(lambda x:(math.exp(x)-float(taylor(x,n)))**2,0,1,epsabs=1e-15)[0]))
def projection(u,v,w=1.):return inner(u,v,w)/inner(v,v,w)*np.asarray(v)
