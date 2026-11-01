import json,subprocess
from pathlib import Path
P=Path(__file__).resolve().parent
m=json.loads((P/'manifest.json').read_text(encoding='utf-8'));c=json.loads((P/'timing.json').read_text(encoding='utf-8'));d=json.loads((P/'cuda_trace.json').read_text())
assert len(m)==16 and len(c)==37 and m[0]['start']==0 and m[-1]['end']==191
assert all(a['end']==b['start'] for a,b in zip(m,m[1:])) and all(a['end']==b['start'] for a,b in zip(c,c[1:]))
expected=[(i%4+1)+(i%4+5) for i in range(512)];expected[133]=11
assert d['C']==expected and d['N']==512 and d['blockSize']==128 and d['gridSize']==4 and d['shared_bytes']==0 and not d['measured_mapping_or_cache']
s=d['selected'];assert s['i']==s['block']*128+s['thread']==133 and s['warp']==s['thread']//32==0 and s['lane']==s['thread']%32==5 and s['A']+s['B']==s['C']==11
assert '__shared__' not in (P/'vector_add.cu').read_text(encoding='utf-8')
traces=list(P.glob('states_longform_*.json'));cases=stores=results=identities=0;issues=[]
for trace in traces:
 for e in json.loads(trace.read_text(encoding='utf-8')):
  if e['kind']=='identity':assert e['block']==1 and e['thread']==5 and e['i']==133 and e['warp']==0 and e['lane']==5 and e['assumed_sm']==1 and not e['mapping_guaranteed'] and not e['shared_used'];identities+=1
  elif e['kind']=='flow':assert not e['shared_in_route']
  elif e['kind']=='mapping':assert e['block']==1 and e['sm']==1 and e['assumed']
  elif e['kind']=='issue':assert 0<=e['warp']<4 and not e['simultaneous_all_warps'];issues.append(e['warp'])
  elif e['kind']=='load_cases':assert e['inputs']==['A[133]','B[133]'] and not e['third_load'] and e['A']==4 and e['B']==7;cases+=1
  elif e['kind']=='store':assert e['A']+e['B']==e['C']==11 and not e['dram_completion_claimed'];stores+=1
  elif e['kind']=='parallel_results':assert e['threads']==512 and e['blocks']==4 and e['per_block']==128 and not e['all_same_instant'];results+=1
for f in P.glob('geometry_longform_*.json'):
 for g in json.loads(f.read_text()):assert g['left']>-7.85 and g['right']<7.85 and g['bottom']>-4.35 and g['top']<4.35,(f,g)
report=dict(cues=37,shots=16,cuda='all512 outputs; Shared0; selected4+7=11',traces=len(traces),identities=identities,load_cases=cases,stores=stores,parallel_results=results,warp_issues=issues,outputs=[])
f=P.parents[1]/'exports'/'gpuh11_integrated_191s_longform_final.mp4'
if f.exists():
 assert len(traces)==identities==16 and cases==stores==results==1
 streams=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(f)]))['streams'];assert len(streams)==1
 v=streams[0];assert float(v['duration'])==191 and int(v['nb_frames'])==5730 and v['r_frame_rate']=='30/1' and (v['width'],v['height'])==(1920,1080)
 report['outputs'].append(dict(path=str(f),duration=191,frames=5730,audio=False,width=1920,height=1080))
(P/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print('PASS',json.dumps(report,ensure_ascii=False))
