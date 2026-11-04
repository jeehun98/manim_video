"""Same signed diagonal matrix for EVD/SVD; explicitly separate loss and approximation examples."""
import numpy as np
A=np.diag([-2.,1.]);P=np.eye(2);D=A.copy();U=np.diag([-1.,1.]);SIGMA=np.diag([2.,1.]);V=np.eye(2)
LOSS=np.diag([2.,0.])
BLOCK=np.array([[2.,3.],[0.,1.]])
ub,sb,vtb=np.linalg.svd(BLOCK)
def block(m,i):
    out=np.zeros((10,10));out[2*i:2*i+2,2*i:2*i+2]=m;return out
ORIGINAL=sum(block(BLOCK,i) for i in range(5))
COMPONENTS=[block(sb[0]*np.outer(ub[:,0],vtb[0]),i) for i in range(5)]+[block(sb[1]*np.outer(ub[:,1],vtb[1]),i) for i in range(5)]
APPROX=sum(COMPONENTS[:5]);ERROR=float(np.linalg.norm(ORIGINAL-APPROX,'fro'))
RESULTS=[('01','이름','EVD'),('02','분해 조건','SVD'),('03','분해 구조','EVD'),('04','고윳값 vs 특이값','SVD'),('05','미래 예측','EVD'),('06','복원 정확도','SVD'),('07','역변환','SVD')]
def verify():
    assert np.allclose(P@D@np.linalg.inv(P),A) and np.allclose(U@SIGMA@V.T,A)
    assert np.allclose(U.T@U,np.eye(2)) and np.allclose(V.T@V,np.eye(2))
    assert np.allclose(A@V[:,0],2*U[:,0]) and np.allclose(A@V[:,1],U[:,1])
    assert np.all(np.diag(SIGMA)>=0) and np.allclose(np.linalg.svd(A,compute_uv=False),[2,1])
    for n in range(5):assert np.allclose(np.linalg.matrix_power(A,n)@np.array([1.,0.]),[(-2.)**n,0.])
    assert np.linalg.matrix_rank(A)==2 and np.linalg.matrix_rank(LOSS)==1
    assert np.allclose(sum(COMPONENTS),ORIGINAL) and np.linalg.matrix_rank(APPROX)==5
    assert np.isclose(ERROR**2,5*sb[1]**2)
    assert sum(w=='EVD' for _,_,w in RESULTS)==3 and sum(w=='SVD' for _,_,w in RESULTS)==4
    return dict(status='passed',A=A.tolist(),P=P.tolist(),D=D.tolist(),U=U.tolist(),Sigma=SIGMA.tolist(),V=V.tolist(),repeated_eigencomponent=[1,-2,4,-8],separate_loss_matrix=LOSS.tolist(),rank5_error=ERROR,evd_wins=3,svd_wins=4)
if __name__=='__main__':
    import json
    from pathlib import Path
    Path(__file__).with_name('math_verification.json').write_text(json.dumps(verify(),indent=2),encoding='utf-8')
    print('Signed eigenvalue, nonnegative SVD, same exact output, powers, separate loss case, rank-five approximation and final score: passed.')
