"""Render, normalize frame rounding, concatenate and verify both layouts."""
import os,sys,json,subprocess,shutil,argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
R=Path(__file__).resolve().parent;W=R.parents[1]
def run(args,env=None):subprocess.run(args,cwd=W,env=env,check=True,stdout=subprocess.DEVNULL)
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=width,height,r_frame_rate,nb_read_frames,duration','-of','json',str(p)]))['streams'][0]
def main():
 p=argparse.ArgumentParser();p.add_argument('--preview',action='store_true');p.add_argument('--layout',choices=['longform','shorts','both'],default='both');p.add_argument('--scene',type=int);p.add_argument('--jobs',type=int,default=2);p.add_argument('--concat-only',action='store_true');p.add_argument('--resume',action='store_true');a=p.parse_args()
 manifest=json.loads((R/'manifest.json').read_text(encoding='utf-8'));fps=15 if a.preview else 60;reports={}
 for layout in (['longform','shorts'] if a.layout=='both' else [a.layout]):
  res=('480,854' if layout=='shorts' else '854,480') if a.preview else ('1080,1920' if layout=='shorts' else '1920,1080')
  suffix=layout+('_preview' if a.preview else '_final');env=os.environ.copy();env['INTRINSIC_LAYOUT']=layout
  targets=[R/m['directory']/f'visual_{suffix}.mp4' for m in manifest]
  def render(pair):
   m,target=pair
   if a.concat_only or a.scene and int(m['id'])!=a.scene:return
   if a.resume and target.exists():
    info=probe(target)
    if int(info['nb_read_frames'])==m['duration_seconds']*fps:return
   media=W/'media'/f'minimal_nn03_{suffix}'/m['id']
   log=R/m['directory']/f'render_{suffix}.log'
   with log.open('w',encoding='utf-8') as f:
    subprocess.run([sys.executable,'-m','manim','--resolution',res,'--fps',str(fps),'--verbosity','ERROR','--progress_bar','none','--disable_caching','--media_dir',str(media),str(R/m['directory']/'scene.py'),m['class']],cwd=W,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
   found=list(media.rglob(m['class']+'.mp4'));assert len(found)==1,found
   raw=found[0];frames=m['duration_seconds']*fps
   run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(raw),'-an','-vf',f'tpad=stop_mode=clone:stop_duration=0.05,fps={fps}','-frames:v',str(frames),'-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',str(target)])
   info=probe(target);assert int(info['nb_read_frames'])==frames,(m,info)
   print('VERIFIED',suffix,m['id'],flush=True)
  with ThreadPoolExecutor(max_workers=a.jobs) as pool:list(pool.map(render,zip(manifest,targets)))
  if a.scene:continue
  concat=R/f'concat_{suffix}.txt';concat.write_text('\n'.join("file '"+t.as_posix()+"'" for t in targets)+'\n',encoding='utf-8')
  out=W/'exports'/f'minimal_nn03_impact_156s_{suffix}.mp4';out.parent.mkdir(exist_ok=True)
  run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(out)])
  info=probe(out);assert int(info['nb_read_frames'])==156*fps,info
  assert abs(float(info['duration'])-156)<.001,info
  assert [int(info['width']),int(info['height'])]==list(map(int,res.split(','))),info
  shutil.copy2(R/'captions.srt',out.with_suffix('.srt'));reports[layout]=dict(path=str(out),**info)
  print('COMPLETE',out,info,flush=True)
 if reports:(R/('verification_preview.json' if a.preview else 'verification_final.json')).write_text(json.dumps(reports,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':main()
