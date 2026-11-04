import json,subprocess
from pathlib import Path
P=Path(__file__).resolve().parent
m=json.loads((P/'manifest.json').read_text(encoding='utf-8'));c=json.loads((P/'timing.json').read_text(encoding='utf-8'));d=json.loads((P/'cuda_trace.json').read_text())
assert len(m)==14 and len(c)==30 and m[0]['start']==0 and m[-1]['end']==165
assert all(a['end']==b['start'] for a,b in zip(m,m[1:])) and all(a['end']==b['start'] for a,b in zip(c,c[1:]))
assert d['C5']==66 and d['vector_count']==256 and d['base_alignment']==32 and not d['measured_traffic']
for p,count in zip(d['patterns'],[4,32,4]):
 expected=[31-l if p['reverse'] else l*p['stride'] for l in range(32)]
 assert p['indices']==expected and p['values']==[i+1 for i in expected]
 assert len({4*i//32 for i in expected})==p['modeled_sectors']==count
report={'cues':30,'shots':14,'cuda':'all256 vectorAdd and all32 values for three patterns passed','sector_model':'aligned base, active32, float32, 32B sectors; no measured traffic or timing','outputs':[],'states':{}}
for layout in ['shorts','longform']:
 traces=list(P.glob(f'states_{layout}_*.json'));patterns=0;links=0
 for trace in traces:
  for event in json.loads(trace.read_text(encoding='utf-8')):
   if event['kind']=='pattern':
    ids=event['indices'];sectors=sorted({x//8 for x in ids});assert event['sectors']==sectors and event['sector_footprint']==len(sectors)*32 and event['useful_bytes']==128;patterns+=1
   elif event['kind']=='lane_links':
    for a in event['links']:assert a['byte']==a['word']*4 and a['sector']==a['word']//8
    links+=len(event['links'])
 report['states'][layout]={'traces':len(traces),'patterns':patterns,'exact_lane_links':links}
 for f in P.glob(f'geometry_{layout}_*.json'):
  for g in json.loads(f.read_text()):
   fw,fh=(9,16) if layout=='shorts' else (16,9)
   assert g['left']>-fw/2+.15 and g['right']<fw/2-.15 and g['bottom']>-fh/2+.15 and g['top']<fh/2-.15,(f,g)
 f=P.parents[1]/'exports'/f'gpuh08_global_memory_165s_{layout}_final.mp4'
 if f.exists():
  assert len(traces)==14, (layout, len(traces))
  streams=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(f)]))['streams'];assert len(streams)==1
  v=streams[0];assert float(v['duration'])==165 and int(v['nb_frames'])==4950 and v['r_frame_rate']=='30/1'
  assert (v['width'],v['height'])==((1080,1920) if layout=='shorts' else (1920,1080))
  report['outputs'].append(dict(path=str(f),duration=165,frames=4950,audio=False))
(P/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False))
