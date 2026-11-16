import numpy as np
DIGITS=np.arange(1,10)
P=np.log10(1+1/DIGITS)
STEP=np.log10(1.1)
TWO_TIME=np.log(2)/np.log(1.1)
NINE_TIME=np.log(10/9)/np.log(1.1)
DECADE_TIME=1/STEP

def growth(t,start=1):return start*1.1**np.asarray(t)
def travel(a,b):return np.log(b/a)/np.log(1.1)
def mantissa(x):return np.mod(np.log10(np.asarray(x)),1)
def first_digit(x):return np.clip(np.floor(10**mantissa(x)+1e-11).astype(int),1,9)
def sample(n=9000,cluster=False):
 u=(np.arange(n)+.5)/n
 if cluster:u=np.log10(4)+u*np.log10(5/4)
 k=np.arange(n)%9-3
 return 10**(k+u)
def probabilities(values):return np.bincount(first_digit(values),minlength=10)[1:10]/len(values)
def occupancy(cycles):
 if cycles<=1e-9:return np.zeros(9)
 k=np.floor(cycles);r=cycles-k;lo=np.log10(DIGITS);hi=np.log10(DIGITS+1)
 return (k*(hi-lo)+np.clip(r-lo,0,hi-lo))/cycles
