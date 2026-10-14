"""Reproducible nearest-neighbor spacings; no Wigner-surmise substitution."""
from pathlib import Path
import hashlib
import json
import re
import numpy as np
from scipy.linalg import eigvalsh
from scipy.special import roots_legendre
from scipy.interpolate import CubicSpline

HERE=Path(__file__).resolve().parent
BASE=267653395647
SEED=20261013


def gue_gap_density(grid, order=48):
    # E(s)=det(I-K) on (0,s), K(x,y)=sinc(x-y); p(s)=E''(s).
    z,w=roots_legendre(order)
    empty=[]
    for s in grid:
        nodes=(z+1)*s/2
        weights=w*s/2
        kernel=np.sinc(nodes[:,None]-nodes[None,:])
        matrix=np.eye(order)-np.sqrt(weights[:,None]*weights[None,:])*kernel
        sign,logdet=np.linalg.slogdet(matrix)
        empty.append(max(0,float(sign*np.exp(logdet))))
    p=CubicSpline(grid,empty)(grid,2)
    p=np.maximum(p,0);p[0]=0
    return p


def main():
    source=HERE/'zeros3.txt'
    lines=source.read_text(encoding='ascii').splitlines()
    offsets=np.array([float(line) for line in lines if re.fullmatch(r'\s*\d+\.\d+\s*',line)])
    assert len(offsets)==10000 and np.all(np.diff(offsets)>0)
    # Subtract offsets, not full heights: preserve precision in the small gaps.
    density=np.log((BASE+(offsets[1:]+offsets[:-1])/2)/(2*np.pi))/(2*np.pi)
    zero_gaps=np.diff(offsets)*density
    zero_scale=float(zero_gaps.mean());zero_gaps/=zero_scale
    rng=np.random.default_rng(SEED)
    gaps=[];sample=None
    n=160;ensembles=100;lo=32;hi=128
    for _ in range(ensembles):
        a=(rng.normal(size=(n,n))+1j*rng.normal(size=(n,n)))/np.sqrt(2)
        h=(a+a.conj().T)/np.sqrt(2*n)
        assert np.allclose(h,h.conj().T)
        ev=eigvalsh(h)[lo:hi]
        # Semicircle CDF unfolding, with the spectral edges discarded.
        cdf=.5+(ev*np.sqrt(np.maximum(4-ev*ev,0))+4*np.arcsin(ev/2))/(4*np.pi)
        unfolded=n*cdf
        gaps.extend(np.diff(unfolded))
        if sample is None:sample=ev.copy()
    gue_gaps=np.array(gaps);gue_scale=float(gue_gaps.mean());gue_gaps/=gue_scale
    edges=np.linspace(0,3,21)
    zh=np.histogram(zero_gaps,edges)[0]/(len(zero_gaps)*np.diff(edges))
    gh=np.histogram(gue_gaps,edges)[0]/(len(gue_gaps)*np.diff(edges))
    grid=np.linspace(0,4,401)
    theory=gue_gap_density(grid,48)
    refined=gue_gap_density(grid,64)
    mass=float(np.trapezoid(theory,grid));mean=float(np.trapezoid(grid*theory,grid))
    assert abs(mass-1)<.003 and abs(mean-1)<.003
    assert np.max(np.abs(theory-refined))<1e-6
    # Small point rows use actual sampled gaps. Their positions are illustrative windows.
    zrow=zero_gaps[100:109];grow=gue_gaps[100:109]
    payload=dict(
        metadata=dict(source_url='https://www-users.cse.umn.edu/~odlyzko/zeta_tables/zeros3',
            source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
            zero_indices=['1000000000001','1000000010000'],zero_count=10000,
            zero_gap_count=len(zero_gaps),base_height=BASE,offset_range=[float(offsets[0]),float(offsets[-1])],
            zero_mean_before_rescale=zero_scale,gue_gap_count=len(gue_gaps),gue_matrices=ensembles,
            gue_matrix_size=n,gue_bulk_indices=[lo,hi],seed=SEED,gue_mean_before_rescale=gue_scale,
            theory='bulk sine-kernel Fredholm determinant, Gauss-Legendre Nystrom; cubic-spline second derivative',
            theory_order=48,theory_grid_step=.01,theory_mass=mass,theory_mean=mean,
            theory_refinement_max_error=float(np.max(np.abs(theory-refined))),
            zero_small_gap_fraction=float(np.mean(zero_gaps<.3)),
            gue_small_gap_fraction=float(np.mean(gue_gaps<.3)),poisson_small_gap_fraction=float(1-np.exp(-.3))),
        edges=edges.tolist(),zero_hist=zh.tolist(),gue_hist=gh.tolist(),theory_x=grid.tolist(),theory_y=theory.tolist(),
        zero_offsets=offsets[:12].tolist(),zero_row=zrow.tolist(),gue_row=grow.tolist(),
        energy_sample=sample[:12].tolist(),raw_zero_gaps=np.diff(offsets)[:8].tolist(),
        normalized_zero_gaps=zero_gaps[:8].tolist())
    (HERE/'spacing_data.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(payload['metadata'],indent=2))


if __name__=='__main__':main()
