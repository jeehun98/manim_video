"""Render both aspect ratios, validate durations, and concatenate independent scenes."""
import argparse,json,subprocess,sys,shutil,os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parents[1]
def run(args,env=None):subprocess.run(args,check=True,cwd=WORKSPACE,env=env)
def main():
 p=argparse.ArgumentParser();p.add_argument('--preview',action='store_true');p.add_argument('--layout',choices=['shorts','longform','both'],default='both');p.add_argument('--scene',type=int);p.add_argument('--jobs',type=int,default=3);p.add_argument('--concat-only',action='store_true');a=p.parse_args()
 manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'));fps=15 if a.preview else 30
 for layout in (['shorts','longform'] if a.layout=='both' else [a.layout]):
  resolution=('360,640' if layout=='shorts' else '854,480') if a.preview else ('1080,1920' if layout=='shorts' else '1920,1080')
  suffix=layout+('_preview' if a.preview else '_final');env=os.environ.copy();env['EIGEN_LAYOUT']=layout
  files=[ROOT/m['directory']/f'visual_{suffix}.mp4' for m in manifest]
  def render(pair):
   m,target=pair
   if a.concat_only or (a.scene and int(m['id'])!=a.scene):return
   media=WORKSPACE/'media'/f'eigen01_{suffix}'/m['id']
   run([sys.executable,'-m','manim','--resolution',resolution,'--fps',str(fps),'--verbosity','ERROR','--progress_bar','none','--media_dir',str(media),str(ROOT/m['directory']/'scene.py'),m['class']],env)
   candidates=list(media.rglob(m['class']+'.mp4'));assert len(candidates)==1,candidates;shutil.copy2(candidates[0],target)
   normalized=target.with_name(target.stem+'_clock.mp4')
   run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(target),'-an','-vf',f'tpad=stop_mode=clone:stop_duration=0.2,fps={fps}','-frames:v',str(m['duration_seconds']*fps),'-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',str(normalized)])
   normalized.replace(target)
   info=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=nb_read_frames,width,height','-of','json',str(target)]))['streams'][0]
   assert int(info['nb_read_frames'])==m['duration_seconds']*fps,(target,info)
   print('VERIFIED',suffix,m['id'],flush=True)
  with ThreadPoolExecutor(max_workers=a.jobs) as pool:list(pool.map(render,zip(manifest,files)))
  if a.scene:continue
  concat=ROOT/f'concat_{suffix}.txt';concat.write_text('\n'.join("file '"+f.as_posix()+"'" for f in files)+'\n',encoding='utf-8')
  exports=WORKSPACE/'exports';exports.mkdir(exist_ok=True);out=exports/f'eigen01_119s_{suffix}.mp4'
  run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(out)])
  info=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=nb_read_frames,width,height,duration','-of','json',str(out)]))['streams'][0]
  assert int(info['nb_read_frames'])==119*fps,info
  assert abs(float(info['duration'])-119)<.001,info
  shutil.copy2(ROOT/'captions.srt',out.with_suffix('.srt'));print('COMPLETE',out,info,flush=True)
if __name__=='__main__':main()
