import math
import numpy as np

def derivative(a,k):
 return float(np.sin(a+k*np.pi/2))
def coefficients(a,n):
 return np.array([derivative(a,k)/math.factorial(k) for k in range(n+1)])
def polynomial(x,a,n):
 return np.polynomial.polynomial.polyval(np.asarray(x)-a,coefficients(a,n))
def sin_error_bound(x,n):
 return np.abs(np.asarray(x))**(n+1)/math.factorial(n+1)
