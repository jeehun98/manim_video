import json,sys
from fractions import Fraction as F
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parents[1]))
from episodes.lagrange01_constraint_value.direction import cartesian,level

d=json.loads((P/'script.json').read_text(encoding='utf-8'))
raw=[s.strip() for s in (P/'narration_source.txt').read_text(encoding='utf-8').splitlines() if s.strip()]
assert len(d['sentences'])==38 and d['duration']==160
for i,s in enumerate(d['sentences']):assert s['text']==raw[2*i] and s['end']==int(raw[2*i+1])
for key in ['sentences','scenes']:
    a=d[key];assert a[0]['start']==0 and a[-1]['end']==160
    assert all(x['end']==y['start'] for x,y in zip(a,a[1:]))
x=np.linspace(0,10,10001);A=x*(10-x)
assert np.allclose(A,25-(x-5)**2) and A.max()==25
gf=np.array([5.,5.]);gg=np.array([2.,2.]);tangent=np.array([1.,-1.])
assert np.allclose(gf,2.5*gg) and np.dot(gf,tangent)==0 and np.dot(gg,tangent)==0
assert tangent@np.array([[0,1],[1,0]])@tangent==-2
per=F(201,10);area=per*per/16;delta=area-25;slope=delta/(per-20)
assert area==F(40401,1600) and delta==F(401,1600) and slope==F(401,160)
assert F(20,8)==F(5,2)
for v in [F(20),per,F(24)]:
    side=v/4;lam=v/8
    assert 4*side==v and side*side==v*v/16 and side==2*lam
axes,_=cartesian()
ux=axes.c2p(1,0)-axes.c2p(0,0);uy=axes.c2p(0,1)-axes.c2p(0,0)
assert np.isclose(np.linalg.norm(ux),np.linalg.norm(uy)) and np.isclose(np.dot(ux,uy),0)
c=level(axes,25);point=axes.c2p(5,5)
assert np.min(np.linalg.norm(c.get_all_points()-point,axis=1))<1e-10
report=dict(source_text_and_38_end_times='exact',continuity='0–160s; 10 scenes; no gaps or overlaps',maximum_identity='A=25−(x−5)² ≤25',optimum=[5,5],gradient_f=gf.tolist(),gradient_g=gg.tolist(),lambda_at_P20=2.5,tangency_slopes=[-1,-1],tangent_second_derivative=-2,axes_equal_scale='passed',sampled_level_curve_includes_exact_contact='passed',P_new=float(per),side_new=float(per/4),A_new=float(area),delta_A=float(delta),finite_difference_ratio=float(slope),instantaneous_ratio=2.5,normalization='g=2x+2y=P; L=f−λ(g−P)',sources=['https://math.mit.edu/~djk/18_022/chapter04/section03.html','https://faculty.arts.ubc.ca/pschrimpf/526/optimization-526.pdf'])
(P/'math_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('Maximum, tangency, vector ratio, axis scale, exact sensitivity and narration timing: passed')
