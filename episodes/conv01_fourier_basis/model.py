import numpy as np
C=np.array([.25,.5,.25]);TAU=1/24;OMEGA=6*np.pi
FREQ=np.array([1,3,6]);AMP=np.array([1,.5,.25]);N=24
RAW=np.array([0,.2,.1,.4,.1,1.5,.2,.4,-.3,-.1,.2,-1.1,-.3,.2,.4,-.2,.3,1.2,.2,.1,0])
def response(omega):return np.sum(C*np.exp(-1j*omega*TAU*np.arange(3)))
def mixture(t):return sum(a*np.sin(2*np.pi*f*t) for f,a in zip(FREQ,AMP))
def circular(f,g):return sum(g[k]*np.roll(f,k) for k in range(len(g)))
def numerical_example():
 t=np.arange(N)/N;f=mixture(t);g=np.zeros(N);g[:3]=C
 return t,f,g,circular(f,g),np.fft.ifft(np.fft.fft(f)*np.fft.fft(g))
def matrices(n=6):
 g=np.zeros(n);g[:3]=C;Cmat=np.array([[g[(i-j)%n] for j in range(n)] for i in range(n)])
 k=np.arange(n);W=np.exp(-2j*np.pi*np.outer(k,k)/n);D=np.diag(np.fft.fft(g))
 return Cmat,W,D
