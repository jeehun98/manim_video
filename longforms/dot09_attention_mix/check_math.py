"""Validate single-query and row-wise attention and its distinction from projection."""
import json
import numpy as np
from visuals import Q,KEYS,VALUES,SCORES,SCALED,ALPHA,OUTPUT,P
assert np.array_equal(SCORES,[3,2]);assert np.allclose(SCALED,[3/np.sqrt(2),2/np.sqrt(2)])
assert np.all(ALPHA>0) and abs(ALPHA.sum()-1)<1e-12
assert np.allclose(ALPHA,[.6697615493266569,.3302384506733431])
assert [round(x,2) for x in OUTPUT]==[2.68,.66]
assert np.allclose(OUTPUT,ALPHA[0]*VALUES[0]+ALPHA[1]*VALUES[1])
assert not np.allclose(ALPHA,SCORES/SCORES.sum())
assert np.isclose(Q@(2*KEYS[0]),2*SCORES[0])
assert np.isclose((Q@KEYS[0])/(np.linalg.norm(Q)*np.linalg.norm(KEYS[0])),(Q@(2*KEYS[0]))/(np.linalg.norm(Q)*np.linalg.norm(2*KEYS[0])))
# Softmax over keys independently for every query row, including extreme scores.
queries=np.array([[2.,1.],[-1.,3.],[2000.,-1000.]])
scores=queries@KEYS.T/np.sqrt(KEYS.shape[1]);ex=np.exp(scores-scores.max(axis=1,keepdims=True));weights=ex/ex.sum(axis=1,keepdims=True)
out=weights@VALUES
assert np.allclose(weights.sum(axis=1),1) and np.isfinite(out).all()
assert np.allclose(out[0],OUTPUT)
u=np.array([1.,1.])/np.sqrt(2);projection=(Q@u)*u
assert abs((Q-projection)@u)<1e-12
assert abs((Q-OUTPUT)@u)>1e-3
report=dict(query=Q.tolist(),keys=KEYS.tolist(),values=VALUES.tolist(),raw_scores=SCORES.tolist(),key_dimension=2,scaled_scores=SCALED.tolist(),weights=ALPHA.tolist(),weighted_values=[(ALPHA[i]*VALUES[i]).tolist() for i in range(2)],output=OUTPUT.tolist(),display_output=[round(x,2) for x in OUTPUT],weight_sum=float(ALPHA.sum()),score_ratio=(SCORES/SCORES.sum()).tolist(),rowwise_weights=weights.tolist(),projection=projection.tolist(),projection_residual_dot=float((Q-projection)@u),attention_residual_dot_same_direction=float((Q-OUTPUT)@u),same_angle_doubled_key_score=float(Q@(2*KEYS[0])))
(P/'qa_math.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
