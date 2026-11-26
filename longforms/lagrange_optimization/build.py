"""Render, hash-cache, concatenate and verify the 426-second silent film."""
import argparse,hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parent;W=R.parents[1]
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(p)]))
def main():
 p=argparse.ArgumentParser();p.add_argument('--preview',action='store_true');p.add_argument('--scene',type=int);a=p.parse_args()
 fps=15 if a.preview else 30;wh=(854,480) if a.preview else (1920,1080);kind='preview' if a.preview else 'final'
 manifest=json.loads((R/'manifest.json').read_text(encoding='utf-8'));timing=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines']
 assert timing[0]['start']==0 and timing[-1]['end']==426
 assert all(x['start']<x['end'] for x in timing) and all(x['end']==y['start'] for x,y in zip(timing,timing[1:]))
 assert sum(m['duration_seconds'] for m in manifest)==426
 media=W/'media'/'lagrange_optimization'/kind;media.mkdir(parents=True,exist_ok=True);targets=[];reports=[]
 for m in manifest:
  d=R/m['directory'];target=media/f"{m['id']}.mp4";targets.append(target)
  if a.scene and int(m['id'])!=a.scene:continue
  digest=hashlib.sha256(b''.join((R/f).read_bytes() for f in ['visuals.py','timing.json','manifest.json','build.py'])+(d/'scene.py').read_bytes()+str((fps,wh)).encode()).hexdigest();stamp=target.with_suffix('.sha256')
  if not target.exists() or not stamp.exists() or stamp.read_text()!=digest:
   log=media/f"{m['id']}.log"
   with log.open('w',encoding='utf-8') as f:
    result=subprocess.run([sys.executable,'-m','manim','--resolution',f'{wh[0]},{wh[1]}','--fps',str(fps),'--verbosity','ERROR','--progress_bar','none','--disable_caching','--media_dir',str(media/m['id']),str(d/'scene.py'),m['class_name']],cwd=W,env={**os.environ,'PYTHONIOENCODING':'utf-8'},stdout=f,stderr=subprocess.STDOUT)
   if result.returncode:raise RuntimeError(log.read_text(encoding='utf-8',errors='replace')[-6000:])
   candidates=list((media/m['id']).rglob(m['class_name']+'.mp4'));assert len(candidates)==1,candidates
   shutil.copyfile(candidates[0],target);stamp.write_text(digest)
  info=probe(target)['streams'][0]
  assert int(info['nb_read_frames'])==m['duration_seconds']*fps,(m,info)
  assert (info['width'],info['height'])==wh and info['avg_frame_rate']==f'{fps}/1'
  audit=json.loads((d/'layout_audit.json').read_text(encoding='utf-8'));assert audit
  reports.append(dict(scene_id=m['id'],sha256=digest,frames=int(info['nb_read_frames']),duration=float(info['duration'])))
  print('VERIFIED',kind,m['id'],flush=True)
 if a.scene:return
 concat=media/'concat.txt';concat.write_text('\n'.join("file '"+t.as_posix()+"'" for t in targets),encoding='utf-8')
 out=W/'exports'/f'lagrange_optimization_426s_{kind}.mp4';out.parent.mkdir(exist_ok=True)
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(out)],check=True)
 data=probe(out);video=data['streams'][0]
 assert len(data['streams'])==1 and int(video['nb_read_frames'])==426*fps and abs(float(video['duration'])-426)<.001
 (R/f'verification_{kind}.json').write_text(json.dumps(dict(output=str(out),silent=True,sentence_end_times=[x['end'] for x in timing],video=video,scenes=reports),ensure_ascii=False,indent=2),encoding='utf-8')
 shutil.copyfile(R/'captions.srt',out.with_suffix('.srt'));print('COMPLETE',out,flush=True)
if __name__=='__main__':main()
