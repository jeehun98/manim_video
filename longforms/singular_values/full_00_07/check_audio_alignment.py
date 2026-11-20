"""Check source narration alignment in each paired chapter and the assembled film."""
from pathlib import Path
import json,subprocess,numpy as np
from scipy.signal import correlate,correlation_lags
HERE=Path(__file__).resolve().parent
report=json.loads((HERE/'verification.json').read_text(encoding='utf-8'))
def audio(path,start,duration=2):
 raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(start),'-i',str(path),'-t',str(duration),'-vn','-ac','1','-ar','16000','-f','f32le','-'])
 return np.frombuffer(raw,dtype=np.float32).astype(float)
def alignment(reference,actual):
 n=min(len(reference),len(actual));a=reference[:n];b=actual[:n];corr=correlate(b,a,mode='full',method='fft');lags=correlation_lags(n,n);mask=np.abs(lags)<=1600;ix=np.argmax(corr[mask]);lag=int(lags[mask][ix]);score=float(corr[mask][ix]/np.sqrt(np.dot(a,a)*np.dot(b,b)))
 a1=a[:n-lag] if lag>=0 else a[-lag:];b1=b[lag:] if lag>=0 else b[:n+lag];score=float(np.dot(a1,b1)/np.sqrt(np.dot(a1,a1)*np.dot(b1,b1)));assert score>.97,(score,lag);assert abs(lag)/16000<.05,(score,lag)
 return dict(correlation=score,lag_seconds=lag/16000)
checks=[]
for c in report['chapters']:
 for t in [2.,c['source_video_duration']-3.]:
  reference=audio(c['audio'],t);pair=alignment(reference,audio(c['output'],t));full=alignment(reference,audio(report['output'],c['start_seconds']+t));checks.append(dict(chapter=c['number'],local_seconds=t,paired=pair,full=full))
(HERE/'audio_alignment.json').write_text(json.dumps(dict(passed=True,checks=checks),indent=2),encoding='utf-8')
print('PASS: 16 source-audio windows align in paired chapters and full film')
