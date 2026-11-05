"""Check the assembled chapters against source frames and audio at every boundary."""
from pathlib import Path
import json,subprocess
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];OUT=ROOT/'exports/quantum_long_1_13_full.mp4';QA=ROOT/'media/quantum_full_01_13/qa'
def call(args):return subprocess.check_output(['ffmpeg','-v','error']+args)
def frame(path,time):
 raw=call(['-ss',f'{time:.9f}','-i',str(path),'-frames:v','1','-vf','scale=320:180','-pix_fmt','rgb24','-f','rawvideo','-']);return np.frombuffer(raw,dtype=np.uint8).reshape(180,320,3)
def audio(path,time):return np.frombuffer(call(['-ss',f'{time:.9f}','-i',str(path),'-t','2','-map','0:a:0','-ar','44100','-ac','1','-f','f32le','-']),dtype=np.float32).astype(float)
def main():
 manifest=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'));meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-show_chapters','-of','json',str(OUT)]));v=next(s for s in meta['streams'] if s['codec_type']=='video');a=next(s for s in meta['streams'] if s['codec_type']=='audio')
 assert (v['width'],v['height'],v['r_frame_rate'])==(1920,1080,'30/1') and int(v['nb_frames'])==manifest['frames']
 assert v['start_time']==a['start_time']=='0.000000' and abs(float(meta['format']['duration'])-manifest['duration_seconds'])<.002
 assert len(meta['chapters'])==13
 rows=[];canvas=Image.new('RGB',(1280,816))
 for n,item in enumerate(manifest['episodes']):
  chapter=meta['chapters'][n];assert abs(float(chapter['start_time'])-item['start_seconds'])<.002 and abs(float(chapter['end_time'])-item['start_seconds']-item['duration_seconds'])<.002
  source=frame(item['video_input'],1.01);joined=frame(OUT,item['start_seconds']+1.01);difference=float(np.abs(source.astype(float)-joined).mean());assert difference<.1,(item['episode'],difference)
  original=audio(item['source'],5);result=audio(OUT,item['start_seconds']+5);scores=[]
  for lag in range(-16,17):
   x=original[max(0,lag):len(original)+min(0,lag)];y=result[max(0,-lag):len(result)-max(0,lag)];length=min(len(x),len(y));x=x[:length];y=y[:length];scores.append(float(np.dot(x,y)/np.sqrt(np.dot(x,x)*np.dot(y,y))))
  best=int(np.argmax(scores))-16;correlation=max(scores);assert correlation>.98 and abs(best)<16,(item['episode'],correlation,best)
  canvas.paste(Image.fromarray(joined),((n%4)*320,(n//4)*204));ImageDraw.Draw(canvas).text(((n%4)*320+5,(n//4)*204+183),f"EP{n+1} @ {item['start_seconds']:.3f}s",fill='white')
  rows.append({'episode':item['episode'],'frame_mean_absolute_pixel_difference':difference,'audio_correlation':correlation,'audio_lag_ms':best/44.1})
 canvas.save(QA/'joined_chapters_contact.png')
 report={'output':str(OUT),'duration_seconds':manifest['duration_seconds'],'frames':int(v['nb_frames']),'resolution':[v['width'],v['height']],'fps':v['r_frame_rate'],'audio_duration':a['duration'],'chapters':meta['chapters'],'source_comparisons':rows,'full_decode':'pending separate full-file check'}
 (HERE/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('PASS: 13 chapter frames, 13 audio alignments, metadata and duration')
if __name__=='__main__':main()
