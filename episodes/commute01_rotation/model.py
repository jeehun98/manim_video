"""Active, right-handed world-axis rotations acting on column vectors."""
import numpy as np
RX=np.array([[1,0,0],[0,0,-1],[0,1,0]],dtype=float)
RY=np.array([[0,0,1],[0,1,0],[-1,0,0]],dtype=float)
R2=np.array([[0,-1],[1,0]],dtype=float)
NORMAL=np.array([0.,0.,1.])
EYE=np.array([5.,-7.,5.]);EYE/=np.linalg.norm(EYE)
RIGHT=np.cross([0,0,1],EYE);RIGHT/=np.linalg.norm(RIGHT)
UP=np.cross(EYE,RIGHT)
PROJECTION=np.array([RIGHT,UP])

def rotation(axis,theta):
    c,s=np.cos(theta),np.sin(theta)
    if axis=='X':return np.array([[1,0,0],[0,c,-s],[0,s,c]])
    if axis=='Y':return np.array([[c,0,s],[0,1,0],[-s,0,c]])
    raise ValueError(axis)

def project(points,origin,scale):
    xy=np.asarray(points)@PROJECTION.T*scale
    return np.column_stack((xy,np.zeros(len(xy))))+origin
