"""Assemble the five approved visual acts without changing their pacing."""
from pathlib import Path
from fractions import Fraction
import json,re
import av
R=Path(__file__).resolve().parent;W=R.parents[1];E=W/'exports'
names=['svd01_distinguish_inputs','svd02_direction_map','svd03_read_and_reassemble','svd04_inverse_sensitivity','svd05_lost_information'];durations=[133,154,152,176,251]
paths=[E/f'svd0{i}.mp4' for i in range(1,5)]+[E/'svd05_lost_information_251s_1080p30.mp4']
outpath=E/'svd_longform_866s_1080p30.mp4';clock=Fraction(1,15360);offset=0;reference=None;chapters=[]
with av.open(str(paths[0])) as template,av.open(str(outpath),'w',options={'movflags':'+faststart'}) as dest:
 out=dest.add_stream_from_template(template.streams.video[0]);out.time_base=clock
 for name,path,duration in zip(names,paths,durations):
  chapters.append({'act':name,'start_seconds':offset//30,'duration_seconds':duration,'source':str(path)})
  count=0
  with av.open(str(path)) as source:
   st=source.streams.video[0];params=(st.width,st.height,st.average_rate,st.codec_context.extradata)
   if reference is None:reference=params
   assert params==reference and st.frames==duration*30,(path,params)
   for packet in source.demux(st):
    if packet.pts is None or packet.dts is None:continue
    packet.pts=(round(packet.pts*packet.time_base*30)+offset)*512
    packet.dts=(round(packet.dts*packet.time_base*30)+offset)*512
    packet.duration=512;packet.time_base=clock;packet.stream=out;dest.mux(packet);count+=1
  assert count==duration*30;offset+=count
assert offset==25980
def stamp(seconds):
 ms=round(seconds*1000);return f'{ms//3600000:02d}:{ms%3600000//60000:02d}:{ms%60000//1000:02d},{ms%1000:03d}'
rows=[];timeoffset=0
for name,duration in zip(names,durations):
 for s in json.loads((W/'longforms'/name/'timing.json').read_text(encoding='utf-8'))['sentences']:
  rows.append(f"{len(rows)+1}\n{stamp(s['start']+timeoffset)} --> {stamp(s['end']+timeoffset)}\n{s['text']}")
 timeoffset+=duration
outpath.with_suffix('.srt').write_text('\n\n'.join(rows)+'\n',encoding='utf-8')
count=0;last=None
with av.open(str(outpath)) as c:
 st=c.streams.video[0];assert st.frames==25980 and float(st.duration*st.time_base)==866
 for f in c.decode(video=0):
  assert last is None or f.pts>last;last=f.pts;count+=1
assert count==25980
report={'output':str(outpath),'duration_seconds':866,'fps':30,'decoded_frames':count,'resolution':[1920,1080],'audio':'silent visual master; no act 5 audio supplied','chapters':chapters,'subtitles':len(rows),'pacing':'all five approved durations preserved; no retiming'}
(R/'qa/combined_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False))
