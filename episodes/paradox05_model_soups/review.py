"""Review timing, selected video frames and interpolation geometry."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[2]
final='--final' in sys.argv
video=ROOT/'exports'/('paradox05.mp4' if final else 'paradox05_preview.mp4')
folder=ROOT/'media'/'paradox05'/('review_final' if final else 'review_preview')
folder.mkdir(parents=True,exist_ok=True)
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)],text=True))
s=next(s for s in info['streams'] if s['codec_type']=='video')
assert (s['width'],s['height'])==((1080,1920) if final else (360,640))
assert s['r_frame_rate']=='30/1'
assert abs(float(info['format']['duration'])-118)<.05
assert not any(s['codec_type']=='audio' for s in info['streams'])
times=[3,9,14,18,23,28,34,45,51,56,60,65,70,75,79,87,93,99,106,111,117]
sheet=Image.new('RGB',(1440,4020),'#091119');draw=ImageDraw.Draw(sheet)
for i,sec in enumerate(times):
    path=folder/f'{sec:03}.png'
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(sec),'-i',str(video),'-frames:v','1',str(path)],check=True)
    im=Image.open(path).convert('RGB');im.thumbnail((360,640))
    x,y=i%4*360,i//4*670
    sheet.paste(im,(x,y+30));draw.text((x+10,y+8),f'{sec} s',fill='white')
sheet.save(folder/'contact_sheet.jpg')
spec=importlib.util.spec_from_file_location('soups_scene',Path(__file__).with_name('scene.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
scene=m.ModelSoupsGeometry()
for i in range(25):
    if i in m.SURFACE_SCENES:continue
    p=scene.panel(i)
    assert p.get_left()[0]>-4.1 and p.get_right()[0]<4.1,(i,'horizontal bounds')
    assert p.get_top()[1]<4.6 and p.get_bottom()[1]>-5,(i,'vertical bounds')
assert np.allclose(m.theta(0),m.A) and np.allclose(m.theta(1),m.B)
assert np.allclose(m.theta(.5),(m.A+m.B)/2)
assert np.allclose(np.vstack([m.A,m.B,m.EXTRAS]).mean(axis=0),m.theta(.5))
grid=np.linspace(0,1,501)
assert np.max(m.low_loss(grid))<.35 and m.barrier(.5)>.8
assert np.isclose(m.barrier(0),m.low_loss(0)) and np.isclose(m.barrier(1),m.low_loss(1))
for lam in grid:
    assert np.isclose(m.low_loss(lam),m.landscape(*m.theta(lam)))
descent=np.array([m.landscape(*((1-u)*m.START+u*m.A)) for u in grid])
assert np.all(np.diff(descent)<=1e-10)
# A nonlinear one-parameter predictor gives a concrete counterexample to equality.
predict=lambda w:np.maximum(0,w)
assert not np.isclose(predict((-1+1)/2),(predict(-1)+predict(1))/2)
timing=json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))
assert timing['sentence_end_seconds']==[5,11,15,20,24,29,37,39,43,47,53,58,61,67,71,76,80,83,89,95,101,104,108,112,118]
assert len(Path(__file__).with_name('tts_script.txt').read_text(encoding='utf-8').strip().split('\n\n'))==25
print(json.dumps(dict(video=str(video),duration=info['format']['duration'],width=s['width'],height=s['height'],fps=s['r_frame_rate'],contact_sheet=str(folder/'contact_sheet.jpg'),checks='2D panel bounds; straight parameter midpoint; barrier/valley endpoints; 2D/3D slice consistency; descending path; parameter vs output average; 25 exact boundaries'),indent=2))
