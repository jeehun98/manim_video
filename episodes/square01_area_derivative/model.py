import numpy as np

def area(x):return np.asarray(x)**2
def gain(x,dx):return 2*np.asarray(x)*dx+dx**2
def secant(x,dx):return 2*np.asarray(x)+dx
def derivative(x):return 2*np.asarray(x)
def potential(q,k=1):return .5*k*np.asarray(q)**2
def force(q,k=1):return -k*np.asarray(q)
