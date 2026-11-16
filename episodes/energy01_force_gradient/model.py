import numpy as np
WEIGHT=10.0

def gravity_potential(h):return WEIGHT*np.asarray(h)
def gravity_force(h):return np.zeros_like(np.asarray(h),dtype=float)-WEIGHT
def potential(x,offset=0):return .5*np.asarray(x)**2+offset
def slope(x):return np.asarray(x)
def force(x):return -slope(x)
def tangent(x,a,offset=0):return potential(a,offset)+slope(a)*(np.asarray(x)-a)
