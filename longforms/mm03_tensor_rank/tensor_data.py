import numpy as np

U=np.array([[1,0,0,1],[0,0,1,1],[1,0,0,0],[0,0,0,1],[1,1,0,0],[-1,0,1,0],[0,1,0,-1]],dtype=int)
V=np.array([[1,0,0,1],[1,0,0,0],[0,1,0,-1],[-1,0,1,0],[0,0,0,1],[1,1,0,0],[0,0,1,1]],dtype=int)
W=np.array([[1,0,0,1],[0,0,1,-1],[0,1,0,1],[1,0,1,0],[-1,1,0,0],[0,0,0,1],[1,0,0,0]],dtype=int)
PAIRS=[(0,0,0),(1,2,0),(0,1,1),(1,3,1),(2,0,2),(3,2,2),(2,1,3),(3,3,3)]
TARGET=np.zeros((4,4,4),dtype=int)
for i,j,k in PAIRS:TARGET[i,j,k]=1
TERMS=np.einsum('si,sj,sk->sijk',U,V,W)
X=np.array([1,2,3,4]);Y=np.array([5,6,7,8])
PRODUCTS=(U@X)*(V@Y)

