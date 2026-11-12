"""Deterministic samples and normalized amplitude models; illustrative, not measured."""
from functools import lru_cache
import numpy as np
from scipy.special import ndtr
SEED=1926
SIGMA=.9
@lru_cache(maxsize=1)
def samples():
 rng=np.random.default_rng(SEED)
 return np.column_stack([rng.normal(0,SIGMA,3000),rng.normal(0,.45,3000)])
def density(x):return np.exp(-np.asarray(x)**2/(2*SIGMA**2))/(np.sqrt(2*np.pi)*SIGMA)
def psi(x):return np.sqrt(density(x))*np.exp(2j*np.asarray(x))
def histogram(n,bins=24):
 edges=np.linspace(-4,4,bins+1);counts,_=np.histogram(samples()[:n,0],edges)
 return edges,counts,counts/(n*np.diff(edges))
def angular_amplitudes():return np.array([.3,.7,1.,.65,.4,.8,.45])*np.exp(1j*np.array([0,.2,.4,.9,1.5,2,2.7]))
def angular_probabilities():
 a=angular_amplitudes();return abs(a)**2/np.sum(abs(a)**2)
def interferometer(phase):
 z=np.exp(1j*phase);return np.array([(1+z)/2,(1-z)/2])
