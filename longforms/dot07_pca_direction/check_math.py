"""Verify the numerical claims independently of rendered labels."""
import json
import numpy as np
from visuals import DATA,MEAN,COV,TOTAL,OPT,EVAL,P
errors=dict(center=float(np.max(np.abs(DATA.mean(axis=0)))),energy=0.,orthogonality=0.,variance=0.,unit=0.,sign=0.)
samples=[]
for angle in np.linspace(0,np.pi,361):
    u=np.array([np.cos(angle),np.sin(angle)]);c=DATA@u;p=c[:,None]*u;r=DATA-p
    e=float(np.sum(r*r));v=float(np.sum(c*c))
    errors['energy']=max(errors['energy'],abs(e+v-TOTAL));errors['orthogonality']=max(errors['orthogonality'],float(np.max(np.abs(r@u))))
    errors['variance']=max(errors['variance'],abs(float(np.var(c))-float(u@COV@u)));errors['unit']=max(errors['unit'],abs(np.linalg.norm(u)-1))
    errors['sign']=max(errors['sign'],float(np.max(np.abs(p-((DATA@(-u))[:,None]*(-u))))));samples.append((e,v))
u=np.array([np.cos(OPT),np.sin(OPT)]);v=float(np.sum((DATA@u)**2));e=TOTAL-v
assert max(errors.values())<1e-10,errors
assert e<=min(x[0] for x in samples)+1e-10 and v>=max(x[1] for x in samples)-1e-10
assert EVAL[-1]>EVAL[0] and np.allclose((DATA+MEAN)-DATA,MEAN)
report=dict(points=16,total=TOTAL,covariance=COV.tolist(),eigenvalues=EVAL.tolist(),optimal_degrees=float(np.degrees(OPT)),optimal_error=e,optimal_preserved=v,optimal_variance=v/16,max_errors=errors)
(P/'qa_math.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
