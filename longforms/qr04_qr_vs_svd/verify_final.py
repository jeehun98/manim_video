"""Validate both deliverables and save representative frames for visual review."""
import json,subprocess,argparse
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw

P=Path(__file__).resolve().parent
WORK=next(p for p in P.parents if (p/'scripts/render.py').exists())
QA=P/'qa';QA.mkdir(exist_ok=True)
TIMES=[2,7,11,16,22,27,31,37,44,49,52,55,60,65,69,73,76,80,84,88,93,97,101,104,106,107]
report=[]
parser=argparse.ArgumentParser();parser.add_argument('--layout',choices=['shorts','longform','both'],default='both');args=parser.parse_args()
for layout in (['shorts','longform'] if args.layout=='both' else [args.layout]):
    path=WORK/'exports'/f'qr04_qr_vs_svd_108s_{layout}_final.mp4'
    data=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(path)]))
    video=next(s for s in data['streams'] if s['codec_type']=='video')
    expected=(1080,1920) if layout=='shorts' else (1920,1080)
    assert (video['width'],video['height'])==expected
    assert video['r_frame_rate']=='30/1'
    assert int(video['nb_read_frames'])==3240
    assert abs(float(video['duration'])-108)<.001
    assert not any(s['codec_type']=='audio' for s in data['streams'])
    frames=[]
    for t in TIMES:
        target=QA/f'{layout}_{t:02}.png'
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(t),'-i',str(path),'-frames:v','1',str(target)],check=True)
        im=Image.open(target).convert('RGB');im.thumbnail((270,480) if layout=='shorts' else (480,270))
        tile=Image.new('RGB',(im.width,im.height+26),'#172033');tile.paste(im,(0,26));ImageDraw.Draw(tile).text((8,6),f'{t}s',fill='white');frames.append(tile)
    cols=4 if layout=='shorts' else 3;w,h=frames[0].size;rows=(len(frames)+cols-1)//cols
    contact=Image.new('RGB',(cols*w,rows*h),'#172033')
    for i,im in enumerate(frames):contact.paste(im,((i%cols)*w,(i//cols)*h))
    contact.save(QA/f'contact_{layout}.jpg',quality=90)
    report.append(dict(layout=layout,file=str(path),width=video['width'],height=video['height'],fps=30,frames=3240,duration=108,audio='not supplied; silent',samples=TIMES))
(P/('verification.json' if args.layout=='both' else f'verification_{args.layout}.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
