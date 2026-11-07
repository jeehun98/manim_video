"""Exact toy order-finding and QFT data; this is not a full implementation of Shor."""
from math import gcd
from fractions import Fraction
import numpy as np

def modular_sequence(a=2,modulus=15,count=8):
    return [pow(a,x,modulus) for x in range(count)]

def multiplicative_order(a,modulus):
    if gcd(a,modulus)!=1:raise ValueError('Coprime base required')
    value=1
    for r in range(1,modulus+1):
        value=value*a%modulus
        if value==1:return r
    raise ValueError('Order not found')

def factors_from_period(a,modulus,r):
    if gcd(a,modulus)!=1 or r%2 or pow(a,r,modulus)!=1:raise ValueError('Unsuitable period')
    half=pow(a,r//2,modulus)
    if half in [1,modulus-1]:raise ValueError('Trivial square root; retry')
    factors=(gcd(half-1,modulus),gcd(half+1,modulus))
    if not all(1<p<modulus for p in factors):raise ValueError('Nontrivial factors required')
    return factors

def periodic_input_state(size=8,output=1):
    # Conditional input-register state after selecting function-register value 1.
    # Values of f are NOT themselves treated as amplitudes.
    state=np.array([float(value==output) for value in modular_sequence(count=size)],dtype=complex)
    return state/np.linalg.norm(state)

def qft_matrix(size=8):
    j=np.arange(size)
    return np.exp(2j*np.pi*np.outer(j,j)/size)/np.sqrt(size)

def qft_example():
    state=periodic_input_state();result=qft_matrix()@state
    result[np.abs(result)<1e-12]=0
    return state,result

def toy_period_candidate(measurement,size=8):
    """Exact fractions for this Q=8 illustration; real order finding uses continued fractions."""
    candidate=Fraction(measurement,size).denominator
    return candidate if candidate>1 and pow(2,candidate,15)==1 else None
