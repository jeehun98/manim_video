"""Hydrogen approximation in Bohr radii and representative Hartree=27.2 eV."""
from dataclasses import dataclass
from functools import lru_cache
import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.special import eval_genlaguerre,factorial
EV_PER_HARTREE=27.2
@dataclass(frozen=True)
class AtomicState:
 n:int
 l:int=0
 m:int=0
 @property
 def energy_ev(self):return -13.6/self.n**2
STATES=[AtomicState(1),AtomicState(2),AtomicState(2,1),AtomicState(3)]
def standing(u,t,mode=1):return np.sin(mode*np.pi*np.asarray(u))*np.cos(mode*t)
def potential(r):return -1/np.asarray(r)
def psi_slice(x,z,n=1,l=0):
 r=np.sqrt(x*x+z*z);rho=2*r/n
 norm=np.sqrt((2/n)**3*factorial(n-l-1)/(2*n*factorial(n+l)))
 radial=norm*np.exp(-rho/2)*rho**l*eval_genlaguerre(n-l-1,2*l+1,rho)
 if l==0:return radial/np.sqrt(4*np.pi)
 if l==1:return radial*np.sqrt(3/(4*np.pi))*np.divide(z,r,out=np.zeros_like(r),where=r>0)
 raise ValueError('Only s and p_z illustrated')
@lru_cache(maxsize=4)
def solve_radial(l=0,count=4,points=8000,rmax=120.):
 dr=rmax/(points+1);r=dr*np.arange(1,points+1)
 diagonal=1/dr**2-1/r+l*(l+1)/(2*r*r)
 off=np.full(points-1,-.5/dr**2)
 energies,vectors=eigh_tridiagonal(diagonal,off,select='i',select_range=(0,count-1))
 return r,energies*EV_PER_HARTREE,vectors/np.sqrt(dr)
