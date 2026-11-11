import json,sys
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P.parents[1]))
from episodes.legendre01_tangent_duality.direction import full_axes,pair_axes,tangent,map_values
d=json.loads((P/'script.json').read_text(encoding='utf-8'))
raw=[s.strip() for s in (P/'narration_source.txt').read_text(encoding='utf-8').splitlines() if s.strip()]
assert len(d['sentences'])==35 and d['duration']==157
for i,s in enumerate(d['sentences']):assert s['text']==raw[2*i] and s['end']==int(raw[2*i+1])
for key in ['sentences','scenes']:
    rows=d[key];assert rows[0]['start']==0 and rows[-1]['end']==157
    assert all(a['end']==b['start'] for a,b in zip(rows,rows[1:]))
X=np.linspace(-5,5,1001)
for a in np.linspace(-2,2,81):
    p=2*a;b=-a*a
    assert np.isclose(p*a+b,a*a)
    assert np.allclose(X*X-(p*X+b),(X-a)**2)
    assert np.isclose(p*a-a*a,p*p/4)
    assert np.allclose(map_values(p,True),(a,a*a))
    assert np.allclose(map_values(a),(p,a*a))
    assert np.all(p*X-X*X<=p*p/4+1e-12)
    assert np.all(a*X-X*X/4<=a*a+1e-12)
    assert np.isclose(a*(2*a)-(2*a)**2/4,a*a)
axes,_=full_axes()
assert np.isclose(np.linalg.norm(axes.c2p(1,0)-axes.c2p(0,0)),np.linalg.norm(axes.c2p(0,1)-axes.c2p(0,0)))
for ax,reverse,values in [(axes,False,np.linspace(-2,2,81)),(pair_axes(2),True,np.linspace(-4,4,81))]:
    for z in values:
        t=tangent(ax,z,reverse)
        for point in [t.get_start(),t.get_end()]:
            u,v=ax.p2c(point)[:2];m=z/2 if reverse else 2*z;b=-z*z/4 if reverse else -z*z
            assert abs(v-(m*u+b))<1e-10
            assert ax.x_range[0]-1e-10<=u<=ax.x_range[1]+1e-10
            assert ax.y_range[0]-1e-10<=v<=ax.y_range[1]+1e-10
report=dict(narration='35 exact sentences and supplied ends',continuity='0–157s; 12 scenes',contact_and_intercept='Y=2aX−a²; p=2a; b=−a²; passed',Fenchel_Young_identity='x²+p²/4−px=(x−p/2)² ≥0',conjugate='sup_x(px−x²)=p²/4 at x=p/2',biconjugate='sup_p(xp−p²/4)=x² at p=2x',forward_inverse_mapping='passed for 81 sampled contacts',tangent_clipping='correct equation and both endpoint bounds; passed',full_graph_axis_equal_units='passed',condition='example smooth strictly convex; general f**=f for proper closed convex functions',thermodynamic_sign='F=U−TS is minus the S-conjugate of U at fixed V',source='https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf, section 3.3')
(P/'math_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('Tangent, intercept, conjugate, inverse, axis units, clipping and narration times: passed')
