"""Probe the movie, inspect frames and verify distributions and gradient direction."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[2]
final='--final' in sys.argv
video=ROOT/'exports'/('paradox06.mp4' if final else 'paradox06_preview.mp4')
folder=ROOT/'media'/'paradox06'/('review_final' if final else 'review_preview')
folder.mkdir(parents=True,exist_ok=True)
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)],text=True))
s=next(s for s in info['streams'] if s['codec_type']=='video')
assert (s['width'],s['height'])==((1080,1920) if final else (360,640))
assert s['r_frame_rate']=='30/1'
assert abs(float(info['format']['duration'])-121)<.05
assert not any(s['codec_type']=='audio' for s in info['streams'])
times=[3,11,16,24,27,30,37,44,50,56,61,66,71,77,81,85,89,95,101,106,111,115,120]
sheet=Image.new('RGB',(1440,4020),'#091119');draw=ImageDraw.Draw(sheet)
for i,sec in enumerate(times):
    path=folder/f'{sec:03}.png'
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(sec),'-i',str(video),'-frames:v','1',str(path)],check=True)
    im=Image.open(path).convert('RGB');im.thumbnail((360,640))
    x,y=i%4*360,i//4*670
    sheet.paste(im,(x,y+30));draw.text((x+10,y+8),f'{sec} s',fill='white')
sheet.save(folder/'contact_sheet.jpg')
spec=importlib.util.spec_from_file_location('ban_scene',Path(__file__).with_name('scene.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
scene=m.BornAgainNetworks()
for i in range(25):
    panel=scene.panel(i)
    assert panel.get_left()[0]>-4.1 and panel.get_right()[0]<4.1,(i,'horizontal bounds')
    assert panel.get_top()[1]<4.6 and panel.get_bottom()[1]>-5,(i,'vertical bounds')
for p in [m.TEACHER,m.STUDENT,m.Q_FIXED,m.P_HIGH,m.P_LOW]:
    assert np.all(p>0) and np.isclose(p.sum(),1)
losses=[m.kl(m.TEACHER,q) for q in [m.STUDENT,np.array([.6,.25,.15]),m.TEACHER]]
assert losses[0]>losses[1]>losses[2] and abs(losses[-1])<1e-12
assert np.allclose(m.Q_FIXED-m.P_HIGH,[-.35,.22,.13])
assert np.allclose(m.Q_FIXED-m.P_LOW,[.05,-.05,0])
def softmax(z):
    a=np.exp(z-np.max(z));return a/a.sum()
z=np.log(m.Q_FIXED);eps=1e-6
for p in [m.P_HIGH,m.P_LOW]:
    numeric=[]
    for j in range(3):
        dz=np.zeros(3);dz[j]=eps
        ce=lambda zz:-np.dot(p,np.log(softmax(zz)))
        numeric.append((ce(z+dz)-ce(z-dz))/(2*eps))
    assert np.allclose(numeric,m.Q_FIXED-p,atol=1e-7)
    stepped=softmax(z-.05*(m.Q_FIXED-p))
    assert (stepped[0]>m.Q_FIXED[0]) if p is m.P_HIGH else (stepped[0]<m.Q_FIXED[0])
net=m.network()
assert [len(layer) for layer in net[1:]]==[3,4,3] and len(net[0])==24
assert np.isclose(m.TEACHER_ERROR-m.STUDENT_ERROR,1.0)
timing=json.loads(Path(__file__).with_name('timing.json').read_text(encoding='utf-8'))
assert timing['sentence_end_seconds']==[5,8,14,18,21,26,28,32,40,46,51,53,58,62,67,73,79,83,91,97,103,108,112,117,121]
assert len(Path(__file__).with_name('tts_script.txt').read_text(encoding='utf-8').strip().split('\n\n'))==25
print(json.dumps(dict(video=str(video),duration=info['format']['duration'],width=s['width'],height=s['height'],fps=s['r_frame_rate'],contact_sheet=str(folder/'contact_sheet.jpg'),checks='25 panel bounds; matched topology; probability sums; KL decrease; finite-difference q-p; gradient step direction; paper error-rate difference; exact 25 boundaries'),indent=2))
