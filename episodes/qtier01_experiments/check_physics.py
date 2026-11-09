"""Numerical consistency checks for schematic experiments; no fabricated observations."""
import itertools,json
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent
d=json.loads((P/'script.json').read_text(encoding='utf-8'))
assert d['duration']==167 and len(d['sentences'])==40
raw=[x.strip() for x in (P/'narration_source.txt').read_text(encoding='utf-8').splitlines() if x.strip()]
for i,s in enumerate(d['sentences']):assert s['text']==raw[2*i].replace('**','') and s['end']==int(raw[2*i+1])
for key in ['sentences','scenes']:
    a=d[key];assert a[0]['start']==0 and a[-1]['end']==167
    assert all(x['end']==y['start'] for x,y in zip(a,a[1:]))
expected={'S':['전자 이중슬릿','벨 부등식'],'A':['광전효과','슈테른–게를라흐','전자 회절'],'B':['프랑크–헤르츠','콤프턴 산란'],'C':['흑체복사','양자 지우개']}
for tier,names in expected.items():assert [e['name'] for e in d['experiments'] if e['tier']==tier]==names
local=[]
for a0,a1,b0,b1 in itertools.product([-1,1],repeat=4):local.append(abs(a0*b0+a0*b1+a1*b0-a1*b1))
assert max(local)==2
E=lambda a,b:np.cos(2*(a-b))
quantum=E(0,np.pi/8)+E(0,-np.pi/8)+E(np.pi/4,np.pi/8)-E(np.pi/4,-np.pi/8)
assert np.isclose(quantum,2*np.sqrt(2))
x=np.linspace(-3,3,5001);envelope=np.exp(-x*x/3)
plus=envelope*(1+np.cos(7*x))/2;minus=envelope*(1-np.cos(7*x))/2
assert np.max(abs(plus+minus-envelope))<1e-14
assert min(plus.min(),minus.min())>=0
theta=np.pi/3;ep=1/(1+1*(1-np.cos(theta)))
recoil=np.array([1-ep*np.cos(theta),-ep*np.sin(theta)])
assert np.isclose(1+1,ep+np.sqrt(1+np.dot(recoil,recoil)))
assert np.allclose(np.array([1.,0]),ep*np.array([np.cos(theta),np.sin(theta)])+recoil)
report=dict(timing='40 exact sentence ends; continuous 0–167s',tiers=expected,CHSH_local_bound=max(local),CHSH_quantum_theory=float(quantum),CHSH_display='theoretical illustration, not 1972 measured data',eraser_complementary_conditionals_sum_to_unfringed_total='passed',Compton_energy_momentum_conservation='passed',Compton_scattered_energy_ratio=float(ep),historical_distinctions=['1900 Planck hypothesis, 1905 Einstein explanation','1961 electron double slit; later single-electron buildup distinguished','1972 Freedman–Clauser; no claim all loopholes closed','1992 polarization quantum eraser; conditional results distinguished'],sources=['https://doi.org/10.1103/PhysRevA.45.7729','https://doi.org/10.1103/PhysRevLett.28.938','https://www.unicamp.br/~chibeni/textosdidaticos/jonsson-electron-diffraction-ajp-1974.pdf'])
(P/'physics_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('Narration, timings, ranks, CHSH, conditional eraser, Compton: passed')
