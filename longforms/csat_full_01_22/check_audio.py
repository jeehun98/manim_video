"""Verify numbering and audio alignment against the supplied MP3s in the final film."""
from pathlib import Path
import json,subprocess
import numpy as np
from scipy.signal import correlate
HERE=Path(__file__).resolve().parent
if (HERE/'verification.json').exists():
 data=json.loads((HERE/'verification.json').read_text(encoding='utf-8'))
else:
 import math
 root=HERE.parents[1];offset=0;chapters=[]
 for r in json.loads((root/'media/csat_audio_durations.json').read_text()):
  chapters.append(dict(number=r['number'],audio=str(root/'exports'/f"수능_{r['number']}.mp3"),start_seconds=offset/30))
  offset+=math.ceil(max(r['video'],r['audio'])*30-1e-8)
 data=dict(output=str(root/'exports/csat_full_01_22_longform.mp4'),chapters=chapters)
final=Path(data['output'])
def sample(p,start):
 raw=subprocess.check_output(['ffmpeg','-v','error','-ss',f'{start:.9f}','-i',str(p),'-t','3','-vn','-ac','1','-ar','16000','-f','f32le','pipe:1'])
 return np.frombuffer(raw,dtype=np.float32).astype(np.float64)
results=[]
for c in data['chapters']:
 original=sample(c['audio'],10);joined=sample(final,c['start_seconds']+10);n=min(len(original),len(joined));original=original[:n];joined=joined[:n]
 original-=original.mean();joined-=joined.mean()
 corr=correlate(joined,original,mode='full',method='fft');mid=n-1;window=corr[mid-1600:mid+1601];index=int(window.argmax());lag=index-1600
 similarity=float(window[index]/np.sqrt(np.dot(original,original)*np.dot(joined,joined)))
 assert similarity>.90,(c['number'],similarity,lag/16000)
 assert abs(lag/16000)<.08,(c['number'],lag/16000)
 results.append(dict(number=c['number'],correlation=similarity,offset_seconds=lag/16000))
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_chapters','-of','json',str(final)]))
assert len(probe['chapters'])==22
for chapter,expected in zip(probe['chapters'],data['chapters']):assert abs(float(chapter['start_time'])-expected['start_seconds'])<.002
(HERE/'audio_alignment.json').write_text(json.dumps(dict(all22passed=True,chapters=results,chapter_metadata='22 exact starts verified'),indent=2),encoding='utf-8')
print('22/22 audio matches passed; largest measured offset:',max(abs(v['offset_seconds']) for v in results),'seconds')
