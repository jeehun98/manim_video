"""Execute all shot timelines without video encoding; enforce safe visual bounds."""
import importlib.util
import json
import os
from pathlib import Path
import sys
from manim import tempconfig
import manimpango
import numpy as np

HERE=Path(__file__).resolve().parent
sys.stdout.reconfigure(encoding='utf-8')
os.environ['EULER_AUDIT']=str(HERE.parents[1]/'media/euler01/layout_audit')
spec=importlib.util.spec_from_file_location('euler_scene',HERE/'scene.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
assert m.FONT in manimpango.list_fonts()
print('Numerical model:',m.motion.validate())
clock=[10.]
rig=m.RotatingPoint(lambda:clock[0],small=True)
sine=m.WaveTrace(rig);cosine=m.WaveTrace(rig,'cos')
for t in np.linspace(10,139,121):
    clock[0]=float(t);rig.sync();sine.sync();cosine.sync()
    x,y=m.motion.coordinates(t)
    np.testing.assert_allclose(rig.point.get_center()[1],sine.dot.get_center()[1],atol=1e-6)
    np.testing.assert_allclose((cosine.dot.get_center()[1]-cosine.cy)/rig.r,x,atol=1e-6)
print('Circle and rendered wave-tip phase: 121 times verified.')
with tempconfig(dict(dry_run=True,skip_animations=True,write_to_movie=False,save_last_frame=False,disable_caching=True,progress_bar='none',verbosity='ERROR')):
    for s in m.DATA['scenes']:
        shot=getattr(m,s['cls'])();shot.render()
        assert abs(shot.time-(s['end']-s['start']))<1/60+.0001
        for record in shot.audit:
            sentence=m.DATA['segments'][record['sentence']-1]
            expected=max(s['start'],sentence['start'])
            if expected<s['end']:assert abs(record['at']-expected)<1/60+.0001,(s['id'],record,expected)
        print(f'Layout and timing OK: {s["id"]:02}',flush=True)
for s in m.DATA['segments']:
    caption=m.text(m.wrap(s['text']),-6.2,size=25,width=7.5)
    assert caption.get_bottom()[1]>-7.5 and caption.get_top()[1]<-5.05
assert len((HERE/'tts_script.txt').read_text(encoding='utf-8').strip().split('\n\n'))==12
print('36 captions, 12 timelines, font, frame and caption safe zones verified.')
