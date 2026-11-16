import numpy as np
K=M=OMEGA=AMPLITUDE=1.0

def potential(q):
 q=np.asarray(q);return .5*q*q+.12*q**3+.08*q**4
def force(q):
 q=np.asarray(q);return -q-.36*q*q-.32*q**3
def quadratic(q):return .5*np.asarray(q)**2
def scaled(u,epsilon):return potential(epsilon*np.asarray(u))/epsilon**2
def displacement(t):return AMPLITUDE*np.cos(OMEGA*np.asarray(t))
def velocity(t):return -AMPLITUDE*OMEGA*np.sin(OMEGA*np.asarray(t))
def acceleration(t):return -OMEGA**2*displacement(t)
def lc_energies(t):return np.cos(np.asarray(t))**2,np.sin(np.asarray(t))**2
