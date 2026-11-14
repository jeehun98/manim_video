"""Render the continuous portrait composition and verify its delivered stream."""
import argparse,hashlib,json,os,subprocess,sys,shutil
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)],text=True))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');args=ap.parse_args()
 data=json.loads((HERE/'timing.json').read_text(encoding='utf-8'))
 for key in ['sentences','scenes']:
  assert data[key][0]['start']==0 and data[key][-1]['end']==159
  for a,b in zip(data[key],data[key][1:]):assert a['end']==b['start']
 source=[s for s in (HERE/'narration_source.txt').read_text(encoding='utf-8').splitlines() if s]
 assert all(s['text']==source[2*i] and s['end']==int(source[2*i+1]) for i,s in enumerate(data['sentences']))
 from math_checks import validate
 validate(HERE)
 mode='preview' if args.preview else 'final';media=ROOT/'media/egeom01'/mode;media.mkdir(parents=True,exist_ok=True)
 deps=[HERE/'scene.py',HERE/'script.json',ROOT/'episodes/log01_ratio_area/scene.py',ROOT/'longforms/qcs01_speed/direction.py',ROOT/'longforms/qcs01_speed/layouts.py',ROOT/'quantum_series/shared/theme.py']
 digest=hashlib.sha256(b''.join(p.read_bytes() for p in deps)+mode.encode()).hexdigest()
 stamp=media/'source.json';old=json.loads(stamp.read_text()) if stamp.exists() else {}
 if old.get('sha256')!=digest or not Path(old.get('clip','missing')).exists():
  env=os.environ.copy();env.update(QCS_PREVIEW=str(int(args.preview)),QCS_LAYOUT='shorts',QCS_AUDIT_DIR=str(media/'audit'),PYTHONIOENCODING='utf-8')
  with (media/'render.log').open('w',encoding='utf-8') as log:
   r=subprocess.run([sys.executable,'-m','manim','render',str(HERE/'scene.py'),'EAreaGeometry','--media_dir',str(media),'--verbosity','WARNING','--progress_bar','none','--disable_caching'],cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
  if r.returncode:print((media/'render.log').read_text(encoding='utf-8')[-6500:]);raise SystemExit(r.returncode)
  clip=max((media/'videos').rglob('EAreaGeometry.mp4'),key=lambda p:p.stat().st_mtime)
  stamp.write_text(json.dumps(dict(sha256=digest,clip=str(clip))),encoding='utf-8')
 else:clip=Path(old['clip'])
 out=ROOT/'exports'/('egeom01_short'+('_preview' if args.preview else '')+'.mp4');out.parent.mkdir(exist_ok=True);shutil.copy2(clip,out)
 result=probe(out);v=next(s for s in result['streams'] if s['codec_type']=='video')
 wh=(360,640) if args.preview else (1080,1920)
 assert (v['width'],v['height'])==wh
 assert v['r_frame_rate']=='60/1' and int(v['nb_frames'])==9540
 assert abs(float(result['format']['duration'])-159)<.02
 records=json.loads((media/'audit/EAreaGeometry_captions.json').read_text())
 assert set(r['sentence'] for r in records)==set(range(1,35))
 for r in records:assert abs(r['at']-data['sentences'][r['sentence']-1]['start'])<=1/60+.00001,r
 subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
 report=dict(output=str(out),duration=159,width=wh[0],height=wh[1],fps=60,frames=9540,audio='not supplied; silent',sha256=digest,caption_boundaries='34 supplied sentence ends; within 1 frame',geometry='frame and caption band checks on every frame',math='e from area root, normalization, reciprocal slope, coordinate swap, exponential derivative passed',decode='passed')
 (HERE/('render_report_'+mode+'.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(out)
if __name__=='__main__':main()
