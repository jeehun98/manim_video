"""Verify production arithmetic, independent Fourier matrix, and all supplied caption bounds."""
import json
from pathlib import Path
import numpy as np
from math import gcd
from .physics_model import *
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
assert modular_sequence()==[1,2,4,8,1,2,4,8]
r=multiplicative_order(2,15);assert r==4
assert all(pow(2,x,15)!=1 for x in range(1,r))
assert 2**r-1==15 and (2**(r//2)-1)*(2**(r//2)+1)==15
assert factors_from_period(2,15,r)==(3,5)
for a,m,bad_period in [(14,15,2),(2,15,3)]:
    try:factors_from_period(a,m,bad_period)
    except ValueError:pass
    else:raise AssertionError('Unsuitable period accepted')
before,after=qft_example();assert np.allclose(before,[1/np.sqrt(2),0,0,0,1/np.sqrt(2),0,0,0])
F=qft_matrix();assert np.allclose(F.conj().T@F,np.eye(8))
assert np.allclose(after,np.fft.ifft(before)*np.sqrt(8))
assert np.allclose(np.abs(after)**2,[.25,0,.25,0,.25,0,.25,0])
assert np.isclose(np.vdot(before,before),1) and np.isclose(np.vdot(after,after),1)
assert [toy_period_candidate(k) for k in [0,2,4,6]]==[None,4,None,4]
sentences=DATA['sentences'];scenes=DATA['scenes']
assert len(sentences)==31 and len(scenes)==20
for rows in [sentences,scenes]:
    assert all(s['start']==(rows[i-1]['end'] if i else 0) and s['end']>s['start'] for i,s in enumerate(rows))
    assert rows[-1]['end']==161
assert sum((s['end']-s['start'])*60 for s in scenes)==9660
blocks=(HERE/'captions.srt').read_text(encoding='utf-8').strip().split('\n\n');assert len(blocks)==31
def seconds(value):
    h,m,v=value.split(':');s,ms=v.split(',');return int(h)*3600+int(m)*60+int(s)+int(ms)/1000
for s,block in zip(sentences,blocks):
    lines=block.splitlines();a,b=lines[1].split(' --> ')
    assert (seconds(a),seconds(b))==(s['start'],s['end'])
    assert ' '.join(lines[2:])==s['text']
report={'duration':161,'fps':60,'frames':9660,'sentences':31,'scenes':20,'srt_matches':True,
        'sequence':modular_sequence(),'minimal_order':r,
        'factors':[3,5],'qft_unitary':True,'qft_probabilities':(np.abs(after)**2).tolist(),
        'measurement_successes':[2,6],'measurement_inconclusive':[0,4],
        'model_scope':'Q=8 conditional input-register illustration; actual Shor uses a larger register and continued fractions',
        'grover_scope':'one marked item, black-box unstructured search, bounded-error oracle queries'}
(HERE/'verification_data.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Arithmetic, order, gcd conditions, normalized QFT, success/failure measurements and 31 caption boundaries: passed')
