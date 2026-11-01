"""Exact data summaries and numerical checks of normal-model likelihood identities."""
import json
from pathlib import Path
import numpy as np
A=np.array([1.,2.,3.,4.,5.]);B=np.array([0.,0.,3.,6.,6.]);VAR=4.
def density(x,mu,var=VAR):return np.exp(-.5*(np.asarray(x)-mu)**2/var)/np.sqrt(2*np.pi*var)
def log_likelihood(x,mu,var=VAR):
 x=np.asarray(x);return -.5*len(x)*np.log(2*np.pi*var)-np.sum((x-mu)**2)/(2*var)
def relative_likelihood(x,mu,var=VAR):return np.exp(log_likelihood(x,mu,var)-log_likelihood(x,float(np.mean(x)),var))
def relative_formula(n,mean,mu,var=VAR):return np.exp(-n*(np.asarray(mu)-mean)**2/(2*var))
def summaries(x):return dict(n=len(x),sum=float(np.sum(x)),mean=float(np.mean(x)),sum_squares=float(np.dot(x,x)),centered_sum_squares=float(np.sum((x-np.mean(x))**2)))
def verify():
 sa,sb=summaries(A),summaries(B)
 assert sa['sum']==sb['sum']==15 and sa['mean']==sb['mean']==3
 assert sa['sum_squares']==55 and sb['sum_squares']==81
 assert sa['centered_sum_squares']==10 and sb['centered_sum_squares']==36
 mus=np.linspace(-2,8,401)
 ra=np.array([relative_likelihood(A,m) for m in mus]);rb=np.array([relative_likelihood(B,m) for m in mus]);formula=relative_formula(5,3,mus)
 assert np.allclose(ra,rb,atol=1e-14) and np.allclose(ra,formula,atol=1e-14)
 errors=[]
 for x in [A,B]:
  for mu in mus:
   left=np.sum((x-mu)**2);right=np.sum(x*x)-2*mu*np.sum(x)+len(x)*mu**2
   errors.append(abs(left-right));assert abs(left-right)<1e-10
 logratios=np.array([log_likelihood(B,m)-log_likelihood(A,m) for m in mus]);assert np.allclose(logratios,-26/(2*VAR))
 # Once variance is unknown the ratio depends on it, so the mean cannot distinguish
 # these samples' information about the two-parameter normal family.
 vr=[1.,4.,9.];ratios=[float(np.exp(log_likelihood(B,3,v)-log_likelihood(A,3,v))) for v in vr];assert len(set(ratios))==3
 report=dict(data_A=sa,data_B=sb,known_variance=VAR,relative_curve_max_error=float(np.max(abs(ra-rb))),relative_formula_max_error=float(np.max(abs(ra-formula))),expansion_max_error=float(max(errors)),absolute_B_to_A_ratio=float(np.exp(-26/(2*VAR))),absolute_likelihood_at_mu3=dict(A=float(np.exp(log_likelihood(A,3))),B=float(np.exp(log_likelihood(B,3)))),unknown_variance_ratios=dict(zip(map(str,vr),ratios)),symbolic_relative_curve='exp[-n*(mu-xbar)^2/(2*sigma^2)]',minimality='For fixed n and known variance, L(x;mu)/L(y;mu) is independent of mu iff sum(x)=sum(y).')
 (Path(__file__).resolve().parent/'math_verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');return report
if __name__=='__main__':print(json.dumps(verify(),ensure_ascii=False,indent=2))
