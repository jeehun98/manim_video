"""Illustrative probabilities; not measurements of human interpretation."""
import numpy as np
LABELS=['책','컵','휴대폰','기타']
PRIOR=np.array([.25,.30,.20,.25])
POSTERIOR=np.array([.85,.08,.05,.02])
UNIFORM=np.full(4,.25)
# One possible likelihood for a gesture observation, chosen to yield the storyboard posterior.
LIKELIHOOD=.2*POSTERIOR/PRIOR

def validate(values):
 p=np.asarray(values,dtype=float)
 assert p.ndim==1 and np.all(p>=0) and np.isclose(p.sum(),1)
 return p

def entropy(values):
 p=validate(values);q=p[p>0]
 return float(-np.sum(q*np.log2(q)))

def interpolate(start,end,t):
 assert 0<=t<=1
 return validate((1-t)*validate(start)+t*validate(end))

def bayes_update(prior,likelihood):
 weights=validate(prior)*np.asarray(likelihood,dtype=float)
 assert np.all(weights>=0) and weights.sum()>0
 return validate(weights/weights.sum())
