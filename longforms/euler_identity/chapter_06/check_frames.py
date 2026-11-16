"""Inspect representative final frames and compare unchanged chapter bridges."""
from pathlib import Path
import json,subprocess
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;W=R.parents[2]
MEDIA=W/'media/euler_identity_ch06';REVIEW=MEDIA/'review';REVIEW.mkdir(parents=True,exist_ok=True)
SHOTS=[('01',0),('02',8.5),('03',10.5),('03',14),('04',5),('04',9.5),('05',2),('05',6),('06',15),('07',9),('08',14),('09',6),('10',9),('10',13),('11',8.8)]
def frame(clip,t,path):
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(t),'-i',str(clip),'-frames:v','1',str(path)],check=True)
images=[]
manifest=json.loads((R/'manifest.json').read_text(encoding='utf-8'))
for sid,t in SHOTS:
    clip=MEDIA/'final'/f'{sid}.mp4';out=REVIEW/f'{sid}_{t:04.1f}.png'
    if not out.exists() or out.stat().st_mtime<clip.stat().st_mtime:frame(clip,t,out)
    m=manifest[int(sid)-1];images.append((out,f"{m['start']+t:.1f}s · Scene {sid}"))
for batch in range((len(images)+5)//6):
    sheet=Image.new('RGB',(1536,930),'#172030');d=ImageDraw.Draw(sheet)
    for k,(path,label) in enumerate(images[batch*6:batch*6+6]):
        x=(k%2)*768;y=(k//2)*310
        im=Image.open(path).convert('RGB');im.thumbnail((768,280));sheet.paste(im,(x+(768-im.width)//2,y+25));d.text((x+12,y+6),label,fill='white')
    sheet.save(REVIEW/f'contact_sheet_{batch+1}.jpg',quality=93)
# Compare only the picture region: narration captions necessarily differ.
old=REVIEW/'chapter05_end.png';frame(W/'media/euler_identity_ch05/final/18.mp4',6.983333,old)
a=np.asarray(Image.open(old).convert('RGB').crop((0,0,1920,875)),dtype=float)
b=np.asarray(Image.open(REVIEW/'01_00.0.png').convert('RGB').crop((0,0,1920,875)),dtype=float)
error=float(np.mean(abs(a-b)));assert error<2,error
report=json.loads((R/'verification_final.json').read_text(encoding='utf-8'))
report['chapter05_bridge']={'passed':True,'mean_pixel_error':error}
report['math_verification']=json.loads((R/'math_verification.json').read_text(encoding='utf-8'))
seen=set()
for scene in report['scenes']:
    sid=scene['scene_id'];scene['sha256']=(MEDIA/'final'/f'{sid}.sha256').read_text()
    m=manifest[int(sid)-1]
    audit=json.loads((R/m['directory']/'layout_audit.json').read_text(encoding='utf-8'))
    seen.update(x['line'] for x in audit)
assert seen==set(range(1,37)),seen
report['caption_coverage']={'passed':True,'lines':36}
report['keyframes']=[dict(path=str(p),label=s) for p,s in images]
(R/'verification_final.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS: 15 keyframes extracted, chapter 05 bridge pixel error',error)
