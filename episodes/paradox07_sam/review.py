"""Inspect the movie and verify equal-radius comparison and the SAM update origin."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[2]
final='--final' in sys.argv
video=ROOT/'exports'/('paradox07.mp4' if final else 'paradox07_preview.mp4')
folder=ROOT/'media'/'paradox07'/('review_final' if final else 'review_preview')
folder.mkdir(parents=True,exist_ok=True)
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)],text=True))
s=next(s for s in info['streams'] if s['codec_type']=='video')
assert (s['width'],s['height'])==((1080,1920) if final else (360,640))
assert s['r_frame_rate']=='30/1'
assert abs(float(info['format']['duration'])-108)<.05
assert not any(s['codec_type']=='audio' for s in info['streams'])
times=[3,11,18,25,28,33,41,46,50,55,58,63,68,74,78,84,89,93,99,104,107]
sheet=Image.new('RGB',(1440,4020),'#091119');draw=ImageDraw.Draw(sheet)
for i,sec in enumerate(times):
    path=folder/f'{sec:03}.png'
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(sec),'-i',str(video),'-frames:v','1',str(path)],check=True)
    im=Image.open(path).convert('RGB');im.thumbnail((360,640))
    x,y=i%4*360,i//4*670
    sheet.paste(im,(x,y+30));draw.text((x+10,y+8),f'{sec} s',fill='white')
sheet.save(folder/'contact_sheet.jpg')
spec=importlib.util.spec_from_file_location('sam_scene',Path(__file__).with_name('scene.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
scene=m.SharpnessAwareMinimization()
for i in range(25):
    panel=scene.panel(i)
    assert panel.get_left()[0]>-4.1 and panel.get_right()[0]<4.1,(i,'horizontal bounds')
    assert panel.get_top()[1]<4.6 and panel.get_bottom()[1]>-5,(i,'vertical bounds')
assert np.all(np.linalg.eigvalsh(m.H)>0)
assert np.isclose(np.linalg.norm(m.EPS),m.RHO)
assert np.allclose(m.ADV,m.THETA+m.EPS)
assert m.loss(m.ADV)>m.loss(m.THETA)
assert np.allclose(m.NEW,m.THETA-m.ETA*m.grad(m.ADV))
assert not np.allclose(m.NEW,m.ADV-m.ETA*m.grad(m.ADV))
assert m.loss(m.NEW)<m.loss(m.THETA) and m.loss(m.SGD_NEW)<m.loss(m.THETA)
exact=m.exact_probe()
assert np.isclose(np.linalg.norm(exact-m.THETA),m.RHO)
assert m.loss(exact)>=m.loss(m.ADV)-1e-8
assert not np.allclose(exact,m.ADV,atol=1e-3)
delta=1e-6
for point in [m.THETA,m.ADV]:
    finite=[]
    for j in range(2):
        d=np.zeros(2);d[j]=delta
        finite.append((m.loss(point+d)-m.loss(point-d))/(2*delta))
    assert np.allclose(finite,m.grad(point),atol=1e-7)
assert m.sharp(0)<m.wide(0)
assert m.sharp(m.VALLEY_RHO)>m.wide(m.VALLEY_RHO)
assert np.isclose(m.sharp(m.VALLEY_RHO),.5455)
assert np.isclose(m.wide(m.VALLEY_RHO),.315125)
p=m.neighborhood('update');ax=p[0]
assert np.isclose(np.linalg.norm(ax.c2p(1,0)-ax.c2p(0,0)),np.linalg.norm(ax.c2p(0,1)-ax.c2p(0,0)))
assert np.allclose(p.update_arrow.get_start(),ax.c2p(*m.THETA),atol=.03)
assert np.allclose(p.update_arrow.get_end(),ax.c2p(*m.NEW),atol=.03)
timing=json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))
assert timing['sentence_end_seconds']==[5,8,13,15,22,26,29,35,37,43,48,52,56,59,65,69,72,76,80,85,91,94,101,105,108]
assert len(Path(__file__).with_name('tts_script.txt').read_text(encoding='utf-8').strip().split('\n\n'))==25
print(json.dumps(dict(video=str(video),duration=info['format']['duration'],width=s['width'],height=s['height'],fps=s['r_frame_rate'],contact_sheet=str(folder/'contact_sheet.jpg'),checks='25 panel bounds; same-radius valley reversal; normalized perturbation; finite-difference gradients; exact vs approximate probe; original-theta update arrow; 25 exact narration boundaries'),indent=2))
