"""Render each independent scene and verify exact frame counts in both layouts."""
import os,sys,json,subprocess,argparse,shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
R=Path(__file__).resolve().parent;W=R.parents[1]
def run(args):subprocess.run(args,cwd=W,check=True,stdout=subprocess.DEVNULL)
def probe(p):
 return json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=width,height,r_frame_rate,nb_read_frames,duration','-of','json',str(p)]))['streams'][0]
def main():
 p=argparse.ArgumentParser();p.add_argument('--preview',action='store_true');p.add_argument('--layout',choices=['longform','shorts','both'],default='both');p.add_argument('--scene',type=int);p.add_argument('--jobs',type=int,default=2);p.add_argument('--resume',action='store_true');a=p.parse_args()
 manifest=json.loads((R/'manifest.json').read_text(encoding='utf-8'));fps=15 if a.preview else 30;reports={}
 for layout in (['longform','shorts'] if a.layout=='both' else [a.layout]):
  wh=((360,640) if layout=='shorts' else (640,360)) if a.preview else ((1080,1920) if layout=='shorts' else (1920,1080))
  suffix=layout+('_preview' if a.preview else '_final');env=os.environ.copy();env['GPUI_LAYOUT']=layout;env['PYTHONIOENCODING']='utf-8'
  targets=[R/m['directory']/f'visual_{suffix}.mp4' for m in manifest]
  def render(pair):
   m,target=pair
   if a.scene and int(m['id'])!=a.scene:return
   if a.resume and target.exists() and int(probe(target)['nb_read_frames'])==m['duration_seconds']*fps:return
   media=W/'media'/f'gpui06_{suffix}'/m['id'];log=R/m['directory']/f'render_{suffix}.log'
   with log.open('w',encoding='utf-8') as f:
    result=subprocess.run([sys.executable,'-m','manim','--resolution',f'{wh[0]},{wh[1]}','--fps',str(fps),'--verbosity','ERROR','--progress_bar','none','--disable_caching','--media_dir',str(media),str(R/m['directory']/'scene.py'),m['class']],cwd=W,env=env,stdout=f,stderr=subprocess.STDOUT)
   if result.returncode:raise RuntimeError(f'Render failed: {log}\n'+log.read_text(encoding='utf-8',errors='replace')[-3500:])
   raw=media/'videos'/'scene'/f'{wh[1]}p{fps}'/(m['class']+'.mp4')
   if not raw.exists():
    matches=list(media.rglob(m['class']+'.mp4'));assert len(matches)==1,matches;raw=matches[0]
   frames=m['duration_seconds']*fps
   run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(raw),'-an','-vf',f'tpad=stop_mode=clone:stop_duration=0.04,fps={fps}','-frames:v',str(frames),'-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',str(target)])
   info=probe(target);assert int(info['nb_read_frames'])==frames,info
   print('VERIFIED',suffix,m['id'],flush=True)
  with ThreadPoolExecutor(max_workers=a.jobs) as pool:list(pool.map(render,zip(manifest,targets)))
  if a.scene:continue
  concat=R/f'concat_{suffix}.txt';concat.write_text('\n'.join("file '"+t.as_posix()+"'" for t in targets)+'\n',encoding='utf-8')
  out=W/'exports'/f'gpui06_memory_140s_{suffix}.mp4';out.parent.mkdir(exist_ok=True)
  run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(out)])
  info=probe(out);assert int(info['nb_read_frames'])==140*fps,info
  assert abs(float(info['duration'])-140)<.001,info
  assert (int(info['width']),int(info['height']))==wh,info
  # Distinct basename prevents players from automatically drawing a second SRT
  # track on top of the captions already burned into the video.
  shutil.copy2(R/'captions.srt',out.with_name(out.stem+'_captions.srt'));reports[layout]=dict(path=str(out),**info)
  print('COMPLETE',out,flush=True)
 if reports:
  report=R/('verification_preview.json' if a.preview else 'verification_final.json')
  previous=json.loads(report.read_text(encoding='utf-8')) if report.exists() else {}
  previous.update(reports);report.write_text(json.dumps(previous,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':main()
