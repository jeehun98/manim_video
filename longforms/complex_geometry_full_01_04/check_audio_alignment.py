"""Check each delivered voice against its numbered original at the chapter start."""
from pathlib import Path
import json,subprocess
import numpy as np
from scipy.signal import correlate,correlation_lags
HERE=Path(__file__).resolve().parent

def samples(path,start):
 raw=subprocess.check_output(['ffmpeg','-v','error','-ss',f'{start:.9f}','-i',str(path),'-t','4','-vn','-ar','48000','-ac','1','-f','f32le','pipe:1'])
 return np.frombuffer(raw,dtype='<f4').astype(float)

def compare(reference,actual):
 size=min(len(reference),len(actual));r=reference[:size];a=actual[:size]
 r-=np.mean(r);a-=np.mean(a)
 corr=correlate(a,r,mode='full',method='fft');lags=correlation_lags(len(a),len(r));keep=abs(lags)<=2400
 lag=int(lags[keep][np.argmax(corr[keep])])
 if lag>=0:x,y=a[lag:],r[:len(r)-lag]
 else:x,y=a[:len(a)+lag],r[-lag:]
 similarity=float(np.dot(x,y)/np.sqrt(np.dot(x,x)*np.dot(y,y)))
 assert abs(lag)<=48,(lag,similarity)
 assert similarity>.97,(lag,similarity)
 return dict(offset_samples=lag,offset_ms=lag/48,normalized_correlation=similarity)

def main():
 report=json.loads((HERE/'verification.json').read_text(encoding='utf-8'));checks=[]
 for c in report['chapters']:
  original=samples(c['audio'],3)
  voiced=compare(original.copy(),samples(c['output'],3))
  final=compare(original.copy(),samples(report['output'],c['start_seconds']+3))
  checks.append(dict(number=c['number'],voiced_part=voiced,joined_chapter=final))
 result=dict(status='passed',method='4-second decoded PCM windows at +3 seconds; cross-correlation with each numbered original; <=1ms offset and >0.97 correlation required',chapters=checks)
 (HERE/'audio_alignment.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
