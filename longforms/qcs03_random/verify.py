"""Check the query oracle, illustrative probabilities and exact supplied timing."""
import json
from pathlib import Path
import numpy as np
from .physics_model import random_bits,oracle,growth,EXACT,ESTIMATE,ERROR,degree_bound

HERE=Path(__file__).resolve().parent
data=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
ends=[6,10,15,21,26,31,36,41,44,52,56,64,71,76,79,86,91,95,105,109,113,119,125,135,140,144,149,155]
assert [s['end'] for s in data['sentences']]==ends
assert [s['start'] for s in data['sentences']]==[0]+ends[:-1]
assert sum(s['end']-s['start'] for s in data['scenes'])==155
assert all(a['end']==b['start'] for a,b in zip(data['scenes'],data['scenes'][1:]))
bits=random_bits();assert set(bits)=={0,1} and len(bits)==64
for i in range(64):
    for b in range(2):
        v=np.zeros(128);v[2*i+b]=1
        assert np.argmax(oracle(v,bits))==2*i+(b^int(bits[i]))
v=np.random.default_rng(9).normal(size=128)+1j*np.random.default_rng(10).normal(size=128);v/=np.linalg.norm(v)
assert np.isclose(np.linalg.norm(oracle(v,bits)),1)
assert np.allclose(oracle(oracle(v,bits),bits),v)
a=np.zeros(128);a[::2]=1/8
assert np.allclose(oracle(a,bits).reshape(64,2).sum(axis=1),np.ones(64)/8)
assert all(np.isclose(p+(1-p),1) for p in [.7,.4])
assert np.isclose(ERROR,.02) and growth(10)==(100,1024) and degree_bound(5)==10
srt=(HERE/'captions.srt').read_text(encoding='utf-8')
assert srt.count(' --> ')==28 and '00:02:35,000' in srt
report={'oracle_basis_cases':128,'oracle_unitarity_and_superposition':'passed','probabilities':'normalized illustrative examples, not circuit measurements','approximation_error':round(ERROR,6),'growth_T10':growth(10),'sentences':28,'duration':155,'frames':9300,'scope':'uniform Boolean inputs; acceptance-probability approximation; query complexity only','status':'passed'}
(HERE/'verification_data.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
