from pathlib import Path
import json,numpy as np
R=Path(__file__).resolve().parent
angles=np.linspace(0,np.pi,1001);z=np.exp(1j*angles)
assert np.allclose(abs(z),1)
assert np.all(np.diff(np.unwrap(np.angle(z)))>0)
assert np.all(z.imag>=-1e-14)
assert np.allclose([z[0].real,z[0].imag],[1,0])
assert np.allclose([z[-1].real,z[-1].imag],[-1,0])
assert np.isclose(np.cos(np.pi),-1) and np.isclose(np.sin(np.pi),0)
assert np.isclose(np.exp(1j*np.pi)+1,0)
for a in [-5,-1,0,1,100]:assert a+0==a and a*1==a
assert np.isclose(1j*1,1j) and np.isclose(1j*1j,-1)
timing=json.loads((R/'timing.json').read_text(encoding='utf-8'));lines=timing['lines']
assert len(lines)==36 and lines[0]['start']==0 and lines[-1]['end']==143
assert all(a['end']==b['start'] for a,b in zip(lines,lines[1:]))
manifest=json.loads((R/'manifest.json').read_text(encoding='utf-8'))
assert sum(m['duration_seconds'] for m in manifest)==143
assert all(m['start'] in [x['start'] for x in lines] for m in manifest)
(R/'math_verification.json').write_text(json.dumps(dict(passed=True,samples=1001,checks=['unit radius','upper counterclockwise half-turn','endpoints 1 and -1','cos pi and sin pi','adding 1 to both sides','identity elements','i multiplication','36 exact sentence timings','11 scene durations']),indent=2),encoding='utf-8')
print('PASS: half-turn, identity, 36 sentence timings and 143-second scene coverage')
