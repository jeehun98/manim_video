"""Exact inverse, nullspace, Moore-Penrose and least-squares checks for the storyboard."""
import numpy as np
A1=np.diag([2.,.5]);A2=np.diag([2.,0.]);A1_INV=np.diag([.5,2.]);A2_PLUS=np.diag([.5,0.])
XA=np.array([.6,.8]);XB=np.array([.6,-.8]);B=np.array([1.2,0.]);XSTAR=np.array([.6,0.])
B_OFF=np.array([1.2,.8]);PROJECTED=np.array([1.2,0.])
def verify():
    assert np.allclose(A1_INV@A1,np.eye(2))
    assert np.allclose(A2@XA,B) and np.allclose(A2@XB,B)
    assert np.allclose(A2_PLUS,np.linalg.pinv(A2))
    assert np.allclose(A2_PLUS@B,XSTAR) and np.allclose(A2_PLUS@B_OFF,XSTAR)
    assert np.allclose(A2@XSTAR,PROJECTED)
    assert np.linalg.matrix_rank(A2)==1
    assert np.allclose(A2@A2_PLUS@A2,A2) and np.allclose(A2_PLUS@A2@A2_PLUS,A2_PLUS)
    assert np.allclose((A2@A2_PLUS).T,A2@A2_PLUS) and np.allclose((A2_PLUS@A2).T,A2_PLUS@A2)
    for t in np.linspace(-3,3,121):
        x=np.array([.6,t]);assert np.allclose(A2@x,B)
        assert np.linalg.norm(x)>=np.linalg.norm(XSTAR)-1e-12
    # Inconsistent output: no vertical output is reachable; residual is perpendicular to range(A2).
    residual=B_OFF-PROJECTED
    assert np.allclose(A2.T@residual,0) and np.isclose(np.linalg.norm(residual),.8)
    # Sampled unit circle maps exactly to the ellipse and to finite segment [-2,2].
    points=np.array([[np.cos(t),np.sin(t)] for t in np.linspace(0,2*np.pi,101)])
    transformed=points@A1.T
    assert np.allclose((transformed[:,0]/2)**2+(transformed[:,1]/.5)**2,1)
    flat=points@A2.T;assert np.allclose(flat[:,1],0) and np.max(abs(flat[:,0]))<=2+1e-12
    return dict(status='passed',A1=A1.tolist(),A1_inverse=A1_INV.tolist(),A2=A2.tolist(),A2_pseudoinverse=A2_PLUS.tolist(),original_inputs=[XA.tolist(),XB.tolist()],common_output=B.tolist(),selected_input=XSTAR.tolist(),inconsistent_output=B_OFF.tolist(),least_squares_projection=PROJECTED.tolist(),least_squares_residual=.8,moore_penrose_conditions=4,solution_line_samples=121)
if __name__=='__main__':
    import json
    from pathlib import Path
    Path(__file__).with_name('math_verification.json').write_text(json.dumps(verify(),indent=2),encoding='utf-8')
    print('Inverse, both overlapping inputs, all Moore-Penrose conditions, minimum norm and least squares: passed.')
