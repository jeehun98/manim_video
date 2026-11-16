import json,hashlib
import numpy as np
from model import *

def validate(folder):
 digest=hashlib.sha256((folder/'model.py').read_bytes()+(folder/'math_checks.py').read_bytes()).hexdigest();out=folder/'math_validation.json'
 if out.exists() and json.loads(out.read_text()).get('sha256')==digest:return
 assert np.isclose(P.sum(),1) and np.all(P>0)
 assert abs(P[0]-.30102999566)<1e-10 and abs(P[-1]-.04575749056)<1e-10
 assert np.isclose(growth(1),1.1) and np.isclose(growth(2),1.21) and np.isclose(growth(3),1.331)
 assert np.isclose(growth(TWO_TIME),2) and np.isclose(growth(NINE_TIME,9),10)
 assert np.isclose(travel(10,20),TWO_TIME) and np.isclose(travel(90,100),NINE_TIME)
 assert round(TWO_TIME,1)==7.3 and round(NINE_TIME,1)==1.1
 assert np.array_equal(first_digit([1532,8.41,729,.0046,92.7,18300]),[1,8,7,4,9,1])
 for t in [1,2,5,10]:assert np.allclose(occupancy(t),P)
 for t in [.2,.8,1.5,3.7]:assert np.isclose(occupancy(t).sum(),1)
 for clustered in [False,True]:
  x=sample(cluster=clustered);assert np.ptp(np.log10(x))>8
  if clustered:assert np.isclose(probabilities(x)[3],1)
  else:assert np.max(abs(probabilities(x)-P))<2/len(x)
 out.write_text(json.dumps({'sha256':digest,'status':'passed','growth_times_days':{'1_to_2':TWO_TIME,'9_to_10':NINE_TIME,'1_to_10':DECADE_TIME},'probabilities':P.tolist(),'checks':['positive digit probabilities telescope to one','daily growth values and continuous first passage times','same ratio at every decade','leading significant digit ignores leading zeroes','continuous time occupancy over complete log cycles','log-fraction-uniform synthetic data approximates theory','wide-spread counterexample concentrated on leading digit four']},indent=2),encoding='utf-8')
