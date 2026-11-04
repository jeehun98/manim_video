"""One exact 10x10 example, fixed blockwise bases for repeated eigen/singular values."""
import numpy as np
B=np.array([[2.,3.],[0.,1.]])
P=np.array([[1.,-3.],[0.,1.]])
E1=np.array([[2.,6.],[0.,0.]])
E2=B-E1
UB,SB,VTB=np.linalg.svd(B)
S1=SB[0]*np.outer(UB[:,0],VTB[0]);S2=SB[1]*np.outer(UB[:,1],VTB[1])
def block(m,i):
    a=np.zeros((10,10));a[2*i:2*i+2,2*i:2*i+2]=m;return a
A=sum(block(B,i) for i in range(5))
E_COMPONENTS=[block(E1,i) for i in range(5)]+[block(E2,i) for i in range(5)]
S_COMPONENTS=[block(S1,i) for i in range(5)]+[block(S2,i) for i in range(5)]
E5=sum(E_COMPONENTS[:5]);S5=sum(S_COMPONENTS[:5])
MIXED=sum(S_COMPONENTS[i] for i in [0,1,2,5,6])
E_ERR=float(np.linalg.norm(A-E5,'fro'));S_ERR=float(np.linalg.norm(A-S5,'fro'));M_ERR=float(np.linalg.norm(A-MIXED,'fro'))
SINGULARS=np.repeat(SB,5)

def verify():
    assert np.allclose(B,P@np.diag([2.,1.])@np.linalg.inv(P))
    assert np.allclose(E1+E2,B) and np.allclose(S1+S2,B)
    assert np.allclose(sum(E_COMPONENTS),A) and np.allclose(sum(S_COMPONENTS),A)
    assert np.linalg.matrix_rank(A)==10 and np.linalg.matrix_rank(E5)==5 and np.linalg.matrix_rank(S5)==5
    assert all(np.linalg.matrix_rank(c)==1 for c in E_COMPONENTS+S_COMPONENTS)
    gram=np.array([[np.vdot(x,y) for y in S_COMPONENTS] for x in S_COMPONENTS])
    assert np.allclose(gram,np.diag(SINGULARS**2))
    assert np.isclose(E_ERR**2,50.) and np.isclose(S_ERR**2,5*SB[1]**2)
    assert S_ERR<E_ERR and S_ERR<M_ERR
    # Every subset obeys Pythagoras; top five reach the Frobenius tail bound.
    from itertools import combinations
    errs=[]
    for inds in combinations(range(10),5):
        approx=sum(S_COMPONENTS[i] for i in inds)
        e=float(np.linalg.norm(A-approx,'fro')**2)
        assert np.isclose(e,sum(SINGULARS[i]**2 for i in range(10) if i not in inds))
        errs.append(e)
    assert np.isclose(min(errs),S_ERR**2)
    # Best rank-five residual for the full matrix independently checked by NumPy SVD.
    u,s,vt=np.linalg.svd(A);assert np.allclose((u[:,:5]*s[:5])@vt[:5],S5)
    return dict(matrix=A.tolist(),evd_5=E5.tolist(),svd_5=S5.tolist(),block_singular_values=SB.tolist(),evd_error=E_ERR,svd_error=S_ERR,mixed_error=M_ERR,evd_squared_error=E_ERR**2,svd_squared_error=S_ERR**2,evd_block_inner_product=float(np.vdot(E1,E2)),svd_block_inner_product=float(np.vdot(S1,S2)),subset_checks=len(errs),status='passed')
if __name__=='__main__':
    import json
    from pathlib import Path
    report=verify();Path(__file__).with_name('math_verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(f'Passed: EVD error {E_ERR:.6f}, SVD error {S_ERR:.6f}, all 252 five-component SVD subsets.')
