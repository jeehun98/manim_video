"""Unnormalized forward DFT and independently evaluated radix-2 DIT."""
import numpy as np
N=8
ORDER=[0,4,2,6,1,5,3,7]
def signal(t):return np.cos(2*np.pi*np.asarray(t)/8)+.5*np.cos(6*np.pi*np.asarray(t)/8)
SAMPLES=signal(np.arange(N))
def dft(x):
 x=np.asarray(x,dtype=complex);n=len(x)
 return np.exp(-2j*np.pi*np.outer(np.arange(n),np.arange(n))/n)@x
def pairs(n,stage):
 half=1<<stage;block=2*half
 return [(start+j,start+j+half,np.exp(-2j*np.pi*j/block)) for start in range(0,n,block) for j in range(half)]
def fft_stages(x):
 n=len(x);bits=n.bit_length()-1;assert n==1<<bits
 order=[int(f'{i:0{bits}b}'[::-1],2) for i in range(n)]
 a=np.asarray(x,dtype=complex)[order].copy();stages=[a.copy()]
 for stage in range(bits):
  for i,j,w in pairs(n,stage):
   e=a[i];t=w*a[j];a[i]=e+t;a[j]=e-t
  stages.append(a.copy())
 return stages
