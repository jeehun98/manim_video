"""Verified mathematical examples and an illustrative three-state spectrum."""
import numpy as np
A=np.array([[1,1],[0,1]],dtype=int)
B=np.array([[1,0],[1,1]],dtype=int)
AB=A@B
BA=B@A
ENERGIES=np.array([0.,1.,3.])
# Frequencies in units where the illustrative energy unit divided by h is 1.
TRANSITIONS=[(1,0,.9),(2,1,.3),(2,0,.55)]
def frequency(high,low):return ENERGIES[high]-ENERGIES[low]
def product_terms(matrix,row=0,column=2):
 matrix=np.asarray(matrix)
 return np.array([matrix[row,k]*matrix[k,column] for k in range(matrix.shape[1])])
