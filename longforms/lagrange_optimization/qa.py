"""Render representative exact-time frames and audit all text event states."""
from pathlib import Path
import json,os,subprocess,sys,argparse,math
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;W=R.parents[1]
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--only');parser.add_argument('--audit-only',action='store_true');args=parser.parse_args()
 from visuals import OptimizationScene
 scene=OptimizationScene();scene.audit=[]
 manifest=json.loads((R/'manifest.json').read_text(encoding='utf-8'));lines=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines'];scene.lines=lines
 all_audit=[]
 for m in manifest:
  scene.index=int(m['id']);scene.rec=m;scene.start=m['start'];scene.end=scene.start+m['duration_seconds'];scene.last=None
  from manim import VGroup
  scene.caption=VGroup();scene.labels=VGroup();scene.prepare()
  for t in sorted(set([scene.start]+[x['start'] for x in lines if scene.start<=x['start']<scene.end]+[x for x in range(scene.start,scene.end,3)])):
   scene.update_text(t)
   g=scene.geometry(t)
   for item in g:
    if not len(item.get_all_points()):continue
    b=[float(item.get_left()[0]),float(item.get_right()[0]),float(item.get_bottom()[1]),float(item.get_top()[1])]
    assert b[0]>=-6.8 and b[1]<=6.8 and b[2]>=-2.76 and b[3]<=3.15,('geometry',scene.index,t,b)
  all_audit.extend(scene.audit);scene.audit=[];scene.clear()
 (R/'layout_check.json').write_text(json.dumps(dict(passed=True,records=all_audit),ensure_ascii=False,indent=2),encoding='utf-8');print('PASS: all text events and sampled geometry bounds',flush=True)
 if args.audit_only:return
 out=W/'media/lagrange_optimization/qa';out.mkdir(parents=True,exist_ok=True)
 samples=[(2,46),(4,83),(5,105),(6,126),(6,134),(10,203),(10,208),(11,228),(14,307),(15,334),(17,384),(19,412)]
 if args.only:samples=[s for s in samples if s[0] in [int(x) for x in args.only.split(',')]]
 frames=[]
 for i,t in samples:
  d=out/f'{i:02d}_{t}';log=out/f'{i:02d}_{t}.log'
  with log.open('w',encoding='utf-8') as f:
   result=subprocess.run([sys.executable,'-m','manim','-s','--resolution','1280,720','--verbosity','ERROR','--progress_bar','none','--media_dir',str(d),str(R/f'scenes/{i:02d}/scene.py'),f'Shot{i:02d}'],cwd=W,env={**os.environ,'LAGRANGE_SNAPSHOT':str(t),'PYTHONIOENCODING':'utf-8'},stdout=f,stderr=subprocess.STDOUT)
  if result.returncode:raise RuntimeError(log.read_text(encoding='utf-8',errors='replace')[-3000:])
  img=next(d.rglob(f'Shot{i:02d}_ManimCE*.png'));frames.append((img,i,t));print('SNAPSHOT',i,t,flush=True)
 sheet=Image.new('RGB',(1280*3,760*math.ceil(len(samples)/3)),'#0C1420');draw=ImageDraw.Draw(sheet)
 for n,(p,i,t) in enumerate(frames):
  x=n%3*1280;y=n//3*760;sheet.paste(Image.open(p).convert('RGB'),(x,y+40));draw.text((x+15,y+12),f'Scene {i:02d} / {t}s',fill='white')
 name='contact_revised.png' if args.only else 'contact.png';sheet.save(out/name);print(out/name,flush=True)
if __name__=='__main__':main()
