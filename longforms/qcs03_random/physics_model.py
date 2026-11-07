"""Explicit illustrative data; not measurements of a quantum circuit."""
import numpy as np

def random_bits(seed=2008,n=64):
    return np.random.default_rng(seed).integers(0,2,n)

def oracle(state,bits):
    state=np.asarray(state,dtype=complex).reshape(len(bits),2)
    out=np.empty_like(state)
    for i,b in enumerate(bits):
        for target in range(2):out[i,target^int(b)]=state[i,target]
    return out.reshape(-1)

def growth(t):return t*t,2**t

def degree_bound(queries):return 2*queries

EXACT=.70
ESTIMATE=.68
ERROR=abs(EXACT-ESTIMATE)
