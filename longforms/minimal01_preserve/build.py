"""Render independent scenes and verify the 154-second dual-layout outputs."""
import argparse,json,subprocess,sys,shutil,os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from caption_pass import burn
ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parents[1]
def run(args,env=None):subprocess.run(args,check=True,cwd=WORKSPACE,env=env)
def probe(path):
 return json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=nb_read_frames,width,height,duration,r_frame_rate','-of','json',str(path)]))['streams'][0]
def main():
 p=argparse.ArgumentParser();p.add_argument('--preview',action='store_true');p.add_argument('--layout',choices=['shorts','longform','both'],default='both');p.add_argument('--scene',type=int);p.add_argument('--jobs',type=int,default=3);p.add_argument('--concat-only',action='store_true');a=p.parse_args()
 manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'));fps=15 if a.preview else 30
 reports={}
 for layout in (['shorts','longform'] if a.layout=='both' else [a.layout]):
  res=('360,640' if layout=='shorts' else '854,480') if a.preview else ('1080,1920' if layout=='shorts' else '1920,1080')
  suffix=layout+('_preview' if a.preview else '_final');env=os.environ.copy();env['MINIMAL_LAYOUT']=layout
  files=[ROOT/m['directory']/f'visual_{suffix}.mp4' for m in manifest]
  def render(pair):
   m,target=pair
   if a.concat_only or (a.scene and int(m['id'])!=a.scene):return
   media=WORKSPACE/'media'/f'minimal01_{suffix}'/m['id']
   run([sys.executable,'-m','manim','--resolution',res,'--fps',str(fps),'--verbosity','ERROR','--progress_bar','none','--disable_caching','--media_dir',str(media),str(ROOT/m['directory']/'scene.py'),m['class']],env)
   candidates=list(media.rglob(m['class']+'.mp4'));assert len(candidates)==1,candidates
   shutil.copy2(candidates[0],target)
   # Normalize sub-frame rounding only; all semantic events are already at their supplied times.
   normalized=target.with_name(target.stem+'_clock.mp4')
   run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(target),'-an','-vf',f'tpad=stop_mode=clone:stop_duration=0.1,fps={fps}','-frames:v',str(m['duration_seconds']*fps),'-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',str(normalized)])
   normalized.replace(target);info=probe(target)
   assert int(info['nb_read_frames'])==m['duration_seconds']*fps,(target,info)
   print('VERIFIED',suffix,m['id'],flush=True)
  with ThreadPoolExecutor(max_workers=a.jobs) as pool:list(pool.map(render,zip(manifest,files)))
  if a.scene:continue
  concat=ROOT/f'concat_{suffix}.txt';concat.write_text('\n'.join("file '"+f.as_posix()+"'" for f in files)+'\n',encoding='utf-8')
  out=WORKSPACE/'exports'/f'minimal01_154s_{suffix}.mp4';out.parent.mkdir(exist_ok=True)
  raw=out.with_name(out.stem+'_uncaptioned.mp4')
  run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(raw)])
  burn(raw,out,layout,a.preview)
  info=probe(out);assert int(info['nb_read_frames'])==154*fps,info;assert abs(float(info['duration'])-154)<.001,info
  assert [int(info['width']),int(info['height'])]==list(map(int,res.split(','))),info
  shutil.copy2(ROOT/'captions.srt',out.with_suffix('.srt'));reports[layout]=dict(path=str(out),**info)
  print('COMPLETE',out,info,flush=True)
 if reports:(ROOT/('verification_preview.json' if a.preview else 'verification_final.json')).write_text(json.dumps(reports,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':main()
