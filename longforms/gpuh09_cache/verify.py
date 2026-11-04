import json,subprocess
from pathlib import Path
from cache_model import CASES
P=Path(__file__).resolve().parent
m=json.loads((P/'manifest.json').read_text(encoding='utf-8'));c=json.loads((P/'timing.json').read_text(encoding='utf-8'));d=json.loads((P/'cuda_trace.json').read_text())
assert len(m)==14 and len(c)==31 and m[0]['start']==0 and m[-1]['end']==169
assert all(a['end']==b['start'] for a,b in zip(m,m[1:])) and all(a['end']==b['start'] for a,b in zip(c,c[1:]))
assert d['N']==256 and d['A5']==6 and d['B5']==12 and not d['measured_cache_hits']
assert {r['kernel'] for r in d['runs']}=={'readArray','readL2Policy','sharedRead'}
for r in d['runs']:assert r['count']==256 and r['values']==[2*(i+1) for i in range(256)]
# Independently verify request termination and bypass conditions, rather than assuming every load reaches DRAM.
for name,e in CASES.items():
 assert e['request'][0]=='Warp' and e['response'][-1]=='Register' and e['response'][0]==e['source']
 if e['l1'] is True:assert e['source']=='L1' and 'L2' not in e['request'] and 'DRAM' not in e['request']
 elif e['l2'] is True:assert e['source']=='L2' and 'DRAM' not in e['request']
 else:assert e['source']=='DRAM' and 'DRAM' in e['request']
 if e['l1'] is None:assert 'L1' not in e['request']+e['response']
report={'cues':31,'shots':14,'cuda':'three kernels / 768 output values passed','cache_model':'assumed independent cases; no measured hits, latency, or policy effects','outputs':[],'states':{}}
for layout in ['shorts','longform']:
 traces=list(P.glob(f'states_{layout}_*.json'));case_names=[];partitions=[];shared_store=0;reuse=0
 for trace in traces:
  for e in json.loads(trace.read_text(encoding='utf-8')):
   if e['kind']=='cache_case':
    expected=CASES[e['case']]
    assert all(e[k]==expected[k] for k in ['request','response','status','source']) and e['value']==6 and e['conceptual'];case_names.append(e['case'])
   elif e['kind']=='resource_partition':assert 0<e['ratio']<1 and not e['actual_supported_configuration'] and not e['automatic_shared_l1_copy'];partitions.append(e['ratio'])
   elif e['kind']=='shared_store':assert e['source']=='Register' and e['destination']=='Shared' and e['explicit'] and e['value']==6;shared_store+=1
   elif e['kind']=='cross_sm_reuse':assert e['source']=='L2' and e['sms']==[0,1] and e['value']==6 and e['unchanged_input'] and e['residency_assumed'] and not e['dram_access'];reuse+=1
 report['states'][layout]={'traces':len(traces),'cache_cases':case_names,'conceptual_partitions':partitions,'explicit_shared_stores':shared_store,'cross_sm_reuse':reuse}
 for f in P.glob(f'geometry_{layout}_*.json'):
  for g in json.loads(f.read_text()):
   fw,fh=(9,16) if layout=='shorts' else (16,9)
   assert g['left']>-fw/2+.15 and g['right']<fw/2-.15 and g['bottom']>-fh/2+.15 and g['top']<fh/2-.15,(f,g)
 f=P.parents[1]/'exports'/f'gpuh09_cache_169s_{layout}_final.mp4'
 if f.exists():
  assert len(traces)==14 and set(case_names)==set(CASES) and partitions==[.5,.75] and shared_store==1 and reuse==1
  streams=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(f)]))['streams'];assert len(streams)==1
  v=streams[0];assert float(v['duration'])==169 and int(v['nb_frames'])==5070 and v['r_frame_rate']=='30/1'
  assert (v['width'],v['height'])==((1080,1920) if layout=='shorts' else (1920,1080))
  report['outputs'].append(dict(path=str(f),duration=169,frames=5070,audio=False))
(P/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False))
