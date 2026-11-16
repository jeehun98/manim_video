import argparse,os,sys,subprocess,json,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def run(cmd,log):
 with log.open('w',encoding='utf-8') as f:
  result=subprocess.run(cmd,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,env=ENV)
 if result.returncode:raise RuntimeError(f'Failed; see {log}')
p=argparse.ArgumentParser();p.add_argument('--preview',action='store_true');p.add_argument('--shots',nargs='*',type=int);p.add_argument('--assemble-only',action='store_true');a=p.parse_args()
ENV=os.environ.copy();ENV['CSAT07_PREVIEW']='1' if a.preview else '0'
mode='preview' if a.preview else 'final';media=ROOT/'media'/'csat07'/mode;media.mkdir(parents=True,exist_ok=True)
shots=a.shots or list(range(1,22));classes=[f'Shot{i:02d}' for i in shots]
if not a.assemble_only:run([sys.executable,'-m','manim','render',str(HERE/'scene.py'),*classes,'--media_dir',str(media),'--disable_caching'],media/'render.log')
clips=[next((media/'videos').rglob(f'Shot{i:02d}.mp4')) for i in shots]
if a.shots:
 print('\n'.join(map(str,clips)));sys.exit()
listing=media/'concat.txt';listing.write_text('\n'.join("file '"+str(c).replace('\\','/')+"'" for c in clips),encoding='utf-8')
out=ROOT/'exports'/('csat07'+('_preview' if a.preview else '')+'.mp4');out.parent.mkdir(exist_ok=True)
run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(listing),'-vf','setpts=N/(30*TB)','-r','30','-fps_mode','cfr','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-an','-movflags','+faststart',str(out)],media/'concat.log')
if not a.preview:
 run([sys.executable,str(ROOT/'episodes/csat_series/problem_cards/apply.py'),'--video',str(out),'--episode','csat07'],media/'problem_card.log')
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(out)]))
v=probe['streams'][0];assert int(v['nb_read_frames'])==4680;assert v['width']==(640 if a.preview else 1920);assert v['height']==(360 if a.preview else 1080);assert abs(float(probe['format']['duration'])-156)<.034
run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],media/'decode.log')
report=dict(output=str(out),duration=probe['format']['duration'],width=v['width'],height=v['height'],fps=v['r_frame_rate'],frames=v['nb_read_frames'],audio='not supplied; silent',decode='passed',sha256=hashlib.sha256(out.read_bytes()).hexdigest(),sentences=32,caption_timing='supplied starts/ends; 30 fps boundaries',geometry='per-frame content bounds and caption band assertions',math='a=-3; fp=3(x+1)(x-1); signs=+,-,+; max=(-1,11); min=(1,7); cubic counterexample')
report['problem_card'] = {'enabled':not a.preview,'layout':'upper 1920x180 strip; lesson 1600x900 at (160,180)','source':'episodes/csat_series/problem_cards/problems.json'}
(HERE/f'render_report_{mode}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(out)
