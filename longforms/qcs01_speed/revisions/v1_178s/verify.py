"""Reproducible checks for the mathematical and timing data used on screen."""
import json
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'script.json').read_text(encoding='utf-8'))
report={'mathematics':[]}
for n,steps in [(4,1),(64,6)]:
    s=np.ones(n)/np.sqrt(n)
    oracle=np.eye(n);oracle[-1,-1]=-1
    diffusion=2*np.outer(s,s)-np.eye(n)
    assert np.allclose(oracle.T@oracle,np.eye(n))
    assert np.allclose(diffusion.T@diffusion,np.eye(n))
    state=s.copy();states=[state.copy()]
    for _ in range(steps):
        state=oracle@state;states.append(state.copy())
        state=diffusion@state;states.append(state.copy())
    assert all(np.isclose(np.vdot(x,x),1) for x in states)
    assert np.isclose(abs(state[-1])**2,np.sin((2*steps+1)*np.arcsin(1/np.sqrt(n)))**2)
    if n==4:assert np.allclose(state,[0,0,0,1])
    # Compare independently constructed matrices against the exact production function.
    from longforms.qcs01_speed.direction import grover_states
    assert np.allclose(states,grover_states(n,n-1,steps))
    report['mathematics'].append({'N':n,'iterations':steps,'unitary':True,'all_snapshots_normalized':True,
                                 'target_probability':float(abs(state[-1])**2)})
sentences=DATA['sentences'];scenes=DATA['scenes']
assert len(sentences)==34 and len(scenes)==18
assert all(s['start']==(sentences[i-1]['end'] if i else 0) and s['end']>s['start'] for i,s in enumerate(sentences))
assert all(s['start']==(scenes[i-1]['end'] if i else 0) and s['end']>s['start'] for i,s in enumerate(scenes))
assert sentences[-1]['end']==scenes[-1]['end']==178
assert sum((s['end']-s['start'])*60 for s in scenes)==10680
srt=(HERE/'captions.srt').read_text(encoding='utf-8')
blocks=srt.strip().split('\n\n')
assert len(blocks)==34
for s,b in zip(sentences,blocks):
    ls=b.splitlines();a,z=ls[1].split(' --> ')
    # Timestamps have millisecond precision, all supplied boundaries are integral seconds.
    def parse(v):
        h,m,tail=v.split(':');sec,ms=tail.split(',');return int(h)*3600+int(m)*60+int(sec)+int(ms)/1000
    assert parse(a)==s['start'] and parse(z)==s['end']
    assert ' '.join(ls[2:])==s['text']
report['timing']={'sentences':34,'scenes':18,'duration':178,'frames':10680,'continuous':True,'srt_matches':True}
(HERE/'verification_data.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Math, production data, 34 SRT boundaries and 10680-frame timeline: passed')
