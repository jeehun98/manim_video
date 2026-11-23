"""Add a classical_mechanics-style contextual header to the verified base film.

Only the new header is rendered; unchanged, source-verified scene videos are
reused. Run --preview to inspect representative header composites before export.
"""
import argparse, hashlib, json, shutil, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
R=Path(__file__).resolve().parent;W=R.parents[2]
MEDIA=W/'media/heat_ch01/guidance'
BASE=W/'exports/heat_ch01_169s_longform_final.mp4'
OUT=W/'exports/heat_ch01_169s_longform_guided.mp4'
SECTIONS=[
 (0,19,'뜨거운 물체에서 시작한 질문'),
 (19,38,'물리 현상 속의 공통 구조'),
 (38,55,'확률과 금융으로 확장'),
 (55,87,'기하학과 위상수학으로 확장'),
 (87,119,'열방정식의 두 가지 출발점'),
 (119,145,'방정식과 해의 의미'),
 (145,169,'복잡한 분포에서 푸리에 해석으로'),
]
def run(cmd):subprocess.run(cmd,cwd=W,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def verify_base():
 report=R/'verification_final.json'
 good=BASE.exists() and report.exists()
 if good:
  data=json.loads(report.read_text(encoding='utf-8'))
  manifest=json.loads((R/'manifest.json').read_text(encoding='utf-8'))
  for m,record in zip(manifest,data['scenes'],strict=True):
   digest=hashlib.sha256(b''.join((R/f).read_bytes() for f in ['visuals.py','timing.json','manifest.json','build.py'])+(R/m['directory']/'scene.py').read_bytes()+str((30,(1920,1080))).encode()).hexdigest()
   good=good and digest==record['sha256']
 if not good:subprocess.run([sys.executable,str(R/'build.py')],cwd=W,check=True)
def headers():
 MEDIA.mkdir(parents=True,exist_ok=True)
 font=Path('C:/Windows/Fonts/malgun.ttf')
 small=ImageFont.truetype(str(font),22);large=ImageFont.truetype(str(font),27)
 records=[]
 for i,(start,end,title) in enumerate(SECTIONS,1):
  im=Image.new('RGB',(1920,78),'#0B1020');d=ImageDraw.Draw(im)
  left='CHAPTER 01  /  HEAT EQUATION'
  d.text((96,38),left,font=small,fill='#8799B6',anchor='lm')
  d.text((1824,38),title,font=large,fill='#EDF3FA',anchor='rm')
  lb=d.textbbox((96,38),left,font=small,anchor='lm');rb=d.textbbox((1824,38),title,font=large,anchor='rm')
  assert lb[2]+70<rb[0] and min(lb[1],rb[1])>=12 and max(lb[3],rb[3])<65
  d.line((96,73,1824,73),fill='#283348',width=1)
  file=MEDIA/f'header_{i:02}.png';im.save(file)
  records.append(dict(start=start,end=end,text=title,file=str(file),left_bbox=lb,right_bbox=rb))
 assert SECTIONS[0][0]==0 and SECTIONS[-1][1]==169
 assert all(a[1]==b[0] for a,b in zip(SECTIONS,SECTIONS[1:]))
 # The existing body title starts below y=78px (top of the subtitle free band).
 audit=json.loads((R/'validation.json').read_text(encoding='utf-8'))['representative_audits']
 assert all((4-a['top'])*135>78 for a in audit if a['kind']=='label')
 return records
def previews(records):
 for t in [8,46,72,105,124,164]:
  p=MEDIA/f'preview_{t:03}.png';raw=MEDIA/'frame.png'
  run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(t),'-i',str(BASE),'-frames:v','1',str(raw)])
  im=Image.open(raw).convert('RGB');r=next(x for x in records if x['start']<=t<x['end'])
  im.paste(Image.open(r['file']),(0,0));im.resize((960,540)).save(p)
 raw.unlink(missing_ok=True)
def main():
 p=argparse.ArgumentParser();p.add_argument('--preview',action='store_true');a=p.parse_args()
 verify_base();records=headers()
 if a.preview:previews(records);print('HEADER PREVIEWS',MEDIA);return
 base_hash=sha(BASE);digest=hashlib.sha256((base_hash+sha(Path(__file__))+json.dumps(SECTIONS,ensure_ascii=False)).encode()).hexdigest()
 stamp=MEDIA/'output.sha256'
 if not OUT.exists() or not stamp.exists() or stamp.read_text()!=digest:
  concat=MEDIA/'headers.ffconcat'
  concat.write_text('ffconcat version 1.0\n'+''.join(f"file '{Path(r['file']).as_posix()}'\nduration {r['end']-r['start']}\n" for r in records)+f"file '{Path(records[-1]['file']).as_posix()}'\n",encoding='utf-8')
  run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(BASE),'-f','concat','-safe','0','-i',str(concat),'-filter_complex','[1:v]fps=30[head];[0:v][head]overlay=0:0:shortest=1[v]','-map','[v]','-an','-t','169','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT)])
  stamp.write_text(digest)
 info=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(OUT)]))
 assert len(info['streams'])==1
 v=info['streams'][0]
 assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_read_frames']))==(1920,1080,'30/1',5070)
 assert abs(float(v['duration'])-169)<.001
 shutil.copyfile(R/'captions.srt',OUT.with_name(OUT.stem+'_captions.srt'))
 (R/'verification_guided.json').write_text(json.dumps(dict(output=str(OUT),base_sha256=base_hash,input_sha256=digest,video=v,silent=True,header_pixel_bounds=[0,0,1920,78],sections=records,unchanged_sentence_end_times=json.loads((R/'timing.json').read_text(encoding='utf-8'))['lines']),ensure_ascii=False,indent=2),encoding='utf-8')
 print('COMPLETE',OUT)
if __name__=='__main__':main()
