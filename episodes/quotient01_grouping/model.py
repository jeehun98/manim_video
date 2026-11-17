"""D4 has eight elements here; rotations C4 form its index-two normal subgroup."""
import numpy as np
I=np.eye(2,dtype=int)
R=np.array([[0,-1],[1,0]])
S=np.array([[1,0],[0,-1]])
ROTATIONS=[np.linalg.matrix_power(R,k) for k in range(4)]
REFLECTIONS=[np.linalg.matrix_power(R,k)@S for k in range(4)]
D4=ROTATIONS+REFLECTIONS
VERTICES=np.array([[-1,-1],[1,-1],[1,1],[-1,1]],dtype=float)
def parity(n):return n%2
def quotient_add(a,b):return (a+b)%2
def symmetry_class(m):return 0 if round(np.linalg.det(m))==1 else 1
def name(m):
    for i,x in enumerate(D4):
        if np.array_equal(m,x):return ('e','r','r²','r³','s','rs','r²s','r³s')[i]
    raise ValueError('Not a square symmetry')
