"""Render independent fixed-time scenes and join on one exact frame clock."""
import argparse,json,subprocess,sys,shutil
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parents[1]
def run(args):subprocess.run(args,check=True,cwd=WORKSPACE)
def main():
 p=argparse.ArgumentParser();p.add_argument('--preview',action='store_true');p.add_argument('--scene',type=int);p.add_argument('--concat-only',action='store_true');p.add_argument('--jobs',type=int,default=3);a=p.parse_args()
 manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'));fps=15 if a.preview else 30
 resolution='854,480' if a.preview else '1920,1080';suffix='preview' if a.preview else '1080p30'
 files=[ROOT/m['directory']/f'visual_{suffix}.mp4' for m in manifest]
 def render(pair):
  m,target=pair
  if a.concat_only or (a.scene and int(m['id'])!=a.scene):return
  media=WORKSPACE/'media'/f'svd01_{suffix}'/m['id']
  run([sys.executable,'-m','manim','--resolution',resolution,'--fps',str(fps),'--verbosity','ERROR','--progress_bar','none','--media_dir',str(media),str(ROOT/m['directory']/'scene.py'),m['class']])
  candidates=list(media.rglob(m['class']+'.mp4'))
  if len(candidates)!=1:raise RuntimeError(candidates)
  shutil.copy2(candidates[0],target);print('RENDERED',m['id'],suffix,flush=True)
 with ThreadPoolExecutor(max_workers=a.jobs) as pool:list(pool.map(render,zip(manifest,files)))
 if a.scene:return
 for path,m in zip(files,manifest):
  normalized=path.with_name(path.stem+'_normalized.mp4')
  run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(path),'-an','-vf',f'tpad=stop_mode=clone:stop_duration=1,fps={fps}','-frames:v',str(round(m['duration_seconds']*fps)),'-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-x264-params',f'keyint={fps}:min-keyint={fps}:scenecut=0',str(normalized)])
  normalized.replace(path)
 (ROOT/f'concat_{suffix}.txt').write_text('\n'.join("file '"+str(f).replace('\\','/')+"'" for f in files)+'\n',encoding='utf-8')
 exports=WORKSPACE/'exports';exports.mkdir(exist_ok=True);output=exports/f'svd01_distinguish_inputs_133s_{suffix}.mp4'
 import av
 offset=0;clock=Fraction(1,fps*512)
 with av.open(str(files[0])) as template,av.open(str(output),'w',options={'movflags':'+faststart'}) as dest:
  out=dest.add_stream_from_template(template.streams.video[0]);out.time_base=clock;reference=None
  for path,m in zip(files,manifest):
   count=0
   with av.open(str(path)) as source:
    stream=source.streams.video[0];parameters=(stream.width,stream.height,stream.codec_context.name,stream.codec_context.extradata)
    if reference is None:reference=parameters
    assert parameters==reference,path
    assert stream.frames==m['duration_seconds']*fps,(path,stream.frames)
    for packet in source.demux(stream):
     if packet.pts is None or packet.dts is None:continue
     packet.pts=(round(packet.pts*packet.time_base*fps)+offset)*512
     packet.dts=(round(packet.dts*packet.time_base*fps)+offset)*512
     packet.duration=512;packet.time_base=clock;packet.stream=out;dest.mux(packet);count+=1
   assert count==m['duration_seconds']*fps;offset+=count
 shutil.copy2(ROOT/'captions.srt',output.with_suffix('.srt'))
 with av.open(str(output)) as c:
  s=c.streams.video[0];assert s.frames==133*fps;assert s.average_rate==fps;assert (s.width,s.height)==tuple(map(int,resolution.split(',')))
  assert abs(float(s.duration*s.time_base)-133)<1e-6
  print(f'OK: {output}; {s.frames} frames; {fps} fps; 133 seconds',flush=True)
if __name__=='__main__':main()
