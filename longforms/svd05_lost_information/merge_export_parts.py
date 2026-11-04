"""Join the user's narrated svd_part_1..5 exports, preserving complete durations."""
from pathlib import Path
from fractions import Fraction
import json,subprocess
import av
R=Path(__file__).resolve().parent;W=R.parents[1];E=W/'exports'
files=[E/f'svd_part_{i}.mp4' for i in range(1,6)]
total_frames=0;chapters=[]
for i,p in enumerate(files,1):
 with av.open(str(p)) as c:
  s=c.streams.video[0]
  assert (s.width,s.height,s.average_rate)==(1920,1080,30)
  assert len(c.streams.audio)==1 and c.streams.audio[0].codec_context.sample_rate==44100
  chapters.append({'part':i,'source':str(p),'start_seconds':total_frames/30,'duration_seconds':s.frames/30})
  total_frames+=s.frames
duration=Fraction(total_frames,30)
concat=R/'concat_narrated_parts.txt'
concat.write_text('\n'.join("file '"+str(p).replace('\\','/')+"'" for p in files)+'\n',encoding='utf-8')
metadata=R/'narrated_chapters.ffmeta';rows=[';FFMETADATA1','title=SVD — 행렬은 어떤 차이를 남기고, 어떤 차이를 잃는가?']
offset=0
for ch in chapters:
 end=offset+round(ch['duration_seconds']*30)
 rows+=['[CHAPTER]','TIMEBASE=1/30',f'START={offset}',f'END={end}',f"title=SVD {ch['part']}부"]
 offset=end
metadata.write_text('\n'.join(rows)+'\n',encoding='utf-8')
output=E/'svd_longform.mp4'
# Preserve video packets. Fill only timestamp gaps in the existing audio, including
# each source's silent tail; do not speed up or shorten any source clip.
subprocess.run(['ffmpeg','-hide_banner','-loglevel','warning','-y','-f','concat','-safe','0','-i',str(concat),'-f','ffmetadata','-i',str(metadata),'-map','0:v:0','-map','0:a:0','-map_metadata','1','-map_chapters','1','-c:v','copy','-af','aresample=async=1:first_pts=0,apad','-c:a','aac','-b:a','192k','-t',f'{float(duration):.9f}','-movflags','+faststart',str(output)],check=True,cwd=W)
video_count=0;audio_samples=0;previous={}
with av.open(str(output)) as c:
 v=c.streams.video[0];a=c.streams.audio[0]
 assert v.frames==total_frames and v.average_rate==30
 assert abs(float(v.duration*v.time_base)-float(duration))<1e-6
 assert abs(float(a.duration*a.time_base)-float(duration))<.001
 for packet in c.demux(v,a):
  for frame in packet.decode():
   kind=packet.stream.type
   if kind in previous:assert frame.pts>previous[kind]
   previous[kind]=frame.pts
   if kind=='video':video_count+=1
   else:audio_samples+=frame.samples
assert video_count==total_frames
report={'output':str(output),'duration_seconds':float(duration),'resolution':[1920,1080],'fps':30,'decoded_video_frames':video_count,'audio_codec':'AAC','sample_rate':44100,'decoded_audio_samples':audio_samples,'parts':chapters,'processing':'video stream copied without re-encoding; original timing and trailing pauses preserved; audio timestamp gaps filled with silence and encoded continuously'}
(E/'svd_longform_info.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False),flush=True)
