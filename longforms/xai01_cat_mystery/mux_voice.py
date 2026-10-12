from pathlib import Path
from fractions import Fraction
import av,numpy as np,json,re
ROOT=Path.cwd();E=ROOT/'exports';P=ROOT/'longforms/xai01_cat_mystery'
TB=Fraction(1,90000); SR=48000

def load_audio(path):
 chunks=[];r=av.AudioResampler(format='fltp',layout='mono',rate=SR)
 with av.open(str(path)) as c:
  for f in c.decode(audio=0):
   chunks.extend(x.to_ndarray() for x in r.resample(f))
  chunks.extend(x.to_ndarray() for x in r.resample(None))
 return np.concatenate(chunks,axis=1)

def mux(target,chapters):
 template=av.open(str(chapters[0]['video']))
 with av.open(str(target),'w',options={'movflags':'+faststart'}) as out:
  vs=out.add_stream_from_template(template.streams.video[0]);vs.time_base=TB
  aus=out.add_stream('aac',rate=SR);aus.layout='mono';aus.bit_rate=192000
  events=[];offset=0
  for ch in chapters:
   duration=Fraction(ch['samples'],SR)
   with av.open(str(ch['video'])) as c:
    s=c.streams.video[0];frames=s.frames
    for packet in c.demux(s):
     if packet.pts is None:continue
     ptsframe=round(packet.pts*packet.time_base*60);dtsframe=round(packet.dts*packet.time_base*60)
     packet.pts=round((Fraction(offset,SR)+duration*ptsframe/frames)/TB)
     packet.dts=round((Fraction(offset,SR)+duration*dtsframe/frames)/TB)
     packet.duration=round(duration/frames/TB);packet.time_base=TB;packet.stream=vs
     events.append(packet)
   offset+=ch['samples']
  audio=np.concatenate([ch['audio'] for ch in chapters],axis=1)
  for start in range(0,audio.shape[1],4096):
   f=av.AudioFrame.from_ndarray(audio[:,start:start+4096],format='fltp',layout='mono')
   f.sample_rate=SR;f.time_base=Fraction(1,SR);f.pts=start
   events.extend(aus.encode(f))
  events.extend(aus.encode(None))
  events.sort(key=lambda x: x.dts*x.time_base)
  for packet in events:out.mux(packet)
 template.close()

def ms(s):
 h,m,sec,milli=map(int,re.split('[:,]',s));return ((h*60+m)*60+sec)*1000+milli

def stamp(t):
 t=round(t);return f'{t//3600000:02}:{t//60000%60:02}:{t//1000%60:02},{t%1000:03}'

chapters=[];allsubs=[];offset=0
for i,old in enumerate([111,146,154,193,226],1):
 a=load_audio(E/f'xai_{i}.mp3');n=a.shape[1];duration=n/SR
 ch={'video':E/f'xai01_act{i:02}_1080p60.mp4','audio':a,'samples':n}
 chapters.append(ch)
 name=f'xai01_act{i:02}_voiced_1080p60'
 print('MUX',i,duration,flush=True);mux(E/f'{name}.mp4',[ch])
 subs=[]
 for block in re.split(r'\n\s*\n',(E/f'xai01_act{i:02}_1080p60.srt').read_text(encoding='utf-8-sig').strip()):
  rows=block.splitlines();start,end=rows[1].split(' --> ')
  start=ms(start)*duration/old;end=ms(end)*duration/old
  body='\n'.join(rows[2:])
  subs.append(f'{len(subs)+1}\n{stamp(start)} --> {stamp(end)}\n{body}')
  allsubs.append(f'{len(allsubs)+1}\n{stamp(start+offset)} --> {stamp(end+offset)}\n{body}')
 (E/f'{name}.srt').write_text('\n\n'.join(subs)+'\n',encoding='utf-8');offset+=duration*1000
print('FULL',offset/1000,flush=True)
mux(E/'xai01_full_voiced_1080p60.mp4',chapters)
(E/'xai01_full_voiced_1080p60.srt').write_text('\n\n'.join(allsubs)+'\n',encoding='utf-8')
report={'audio_seconds':[x['samples']/SR for x in chapters],'total_seconds':offset/1000,'method':'Original voice speed; proportional video timestamp scaling; no video recompression; continuous AAC for full audio'}
(P/'voiced_render_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('COMPLETE',flush=True)
