import json,subprocess
from pathlib import Path
P=Path(__file__).resolve().parent
m=json.loads((P/'manifest.json').read_text(encoding='utf-8'));c=json.loads((P/'timing.json').read_text(encoding='utf-8'));d=json.loads((P/'cuda_trace.json').read_text())
assert len(m)==17 and len(c)==33 and m[0]['start']==0 and m[-1]['end']==160
assert all(a['end']==b['start'] for a,b in zip(m,m[1:]))
assert all(a['end']==b['start'] for a,b in zip(c,c[1:]))
assert d['neighbor']==[100+(t+1)%128 for t in range(128)]
A=list(range(1,17));expect=[sum(A[r*4+k]*A[k*4+col] for k in range(4)) for r in range(4) for col in range(4)]
assert d['gemm']==expect and [expect[x] for x in [0,1,4,5]]==[90,100,202,228]
assert len({x%32 for x in [0,1,2,3]})==4 and len({x%32 for x in [0,32,64,96]})==1
assert len(set([0,32,64,96]))==4 and 64//8==8 and 64//16==4
report={'cues':33,'shots':17,'cuda':'all128 neighbor and16 GEMM verified','source_element_requests':{'naive':32,'tiled':16,'measured_dram':False},'videos':[]}
for layout in ['shorts','longform']:
 f=P.parents[1]/'exports'/f'gpuh07_shared_memory_160s_{layout}_final.mp4'
 if not f.exists():continue
 streams=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(f)]))['streams'];assert len(streams)==1
 v=streams[0];assert float(v['duration'])==160 and int(v['nb_frames'])==4800 and v['r_frame_rate']=='30/1'
 assert (v['width'],v['height'])==((1080,1920) if layout=='shorts' else (1920,1080))
 report['videos'].append({'path':str(f),'duration':160,'frames':4800,'audio':False})
(P/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False))
