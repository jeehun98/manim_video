import json,subprocess
from pathlib import Path
from dram_model import BankModel
P=Path(__file__).resolve().parent
m=json.loads((P/'manifest.json').read_text(encoding='utf-8'));c=json.loads((P/'timing.json').read_text(encoding='utf-8'));d=json.loads((P/'cuda_trace.json').read_text())
assert len(m)==14 and len(c)==34 and m[0]['start']==0 and m[-1]['end']==164
assert all(a['end']==b['start'] for a,b in zip(m,m[1:])) and all(a['end']==b['start'] for a,b in zip(c,c[1:]))
assert d['N']==256 and d['A5']==6 and d['B5']==12 and not d['measured_dram_state'] and d['values']==[2*(i+1) for i in range(256)]
bank=BankModel();events=[bank.read(1,2),bank.read(1,5),bank.read(3,2)]
assert [e['commands'] for e in events]==[['ACTIVATE','READ'],['READ'],['PRECHARGE','ACTIVATE','READ']]
report={'cues':34,'shots':14,'cuda':'readData all256 output values passed','dram_model':'one active row per bank; illustrative mapping and command ordering; no measured timing','outputs':[],'states':{}}
for layout in ['shorts','longform']:
 traces=list(P.glob(f'states_{layout}_*.json'));reads=[];packaging=[];returned=0;computed=0;controllers=0
 for trace in traces:
  for e in json.loads(trace.read_text(encoding='utf-8')):
   if e['kind']=='bank_read':
    assert e['read_value_source']=='Row Buffer'
    state=e['before']
    for cmd in e['commands']:
     if cmd=='PRECHARGE':assert state is not None;state=None
     elif cmd=='ACTIVATE':assert state is None;state=e['row']
     else:assert cmd=='READ' and state==e['row']
    assert state==e['after'] and 0<=e['row']<4 and 0<=e['col']<8 and e['conceptual'];reads.append(e)
   elif e['kind']=='packaging':
    assert not e['memory_on_gpu_die'] and not e['performance_ranking'];packaging.append(e['technology'])
    if e['technology']=='HBM':assert e['stacked_dram'] and e['wide_interface'] and e['diagram']=='same_package_example'
   elif e['kind']=='load_return':assert e['route']==['DRAM','Controller','L2','L1','Register'] and e['value']==6;returned+=1
   elif e['kind']=='compute':assert e['input']*e['multiplier']==e['result']==12;computed+=1
   elif e['kind']=='controller_request':assert not e['virtual_translation_only_here'];controllers+=1
 for e,expected in zip(reads,events):assert all(e[k]==expected[k] for k in expected)
 report['states'][layout]={'traces':len(traces),'reads':reads,'packaging':packaging,'load_returns':returned,'computed':computed,'controller_requests':controllers}
 for f in P.glob(f'geometry_{layout}_*.json'):
  for g in json.loads(f.read_text()):
   fw,fh=(9,16) if layout=='shorts' else (16,9)
   assert g['left']>-fw/2+.15 and g['right']<fw/2-.15 and g['bottom']>-fh/2+.15 and g['top']<fh/2-.15,(f,g)
 f=P.parents[1]/'exports'/f'gpuh10_dram_164s_{layout}_final.mp4'
 if f.exists():
  assert len(traces)==14 and len(reads)==3 and set(packaging)=={'GDDR','HBM'} and returned==computed==controllers==1
  streams=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(f)]))['streams'];assert len(streams)==1
  v=streams[0];assert float(v['duration'])==164 and int(v['nb_frames'])==4920 and v['r_frame_rate']=='30/1'
  assert (v['width'],v['height'])==((1080,1920) if layout=='shorts' else (1920,1080));report['outputs'].append(dict(path=str(f),duration=164,frames=4920,audio=False))
(P/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print('PASS',json.dumps({k:v for k,v in report.items() if k!='states'},ensure_ascii=False))
