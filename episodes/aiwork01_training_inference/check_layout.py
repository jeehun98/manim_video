"""Execute all shot timelines without video encoding; enforce safe visual bounds."""
import importlib.util
import json
import os
from pathlib import Path
import sys
from manim import tempconfig
import manimpango

HERE=Path(__file__).resolve().parent
sys.stdout.reconfigure(encoding='utf-8')
os.environ['AIWORK_AUDIT']=str(HERE.parents[1]/'media/aiwork01/layout_audit')
spec=importlib.util.spec_from_file_location('aiwork_scene',HERE/'scene.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
assert m.FONT in manimpango.list_fonts()
with tempconfig(dict(dry_run=True,skip_animations=True,write_to_movie=False,save_last_frame=False,disable_caching=True,progress_bar='none',verbosity='ERROR')):
    for s in m.DATA['scenes']:
        shot=getattr(m,s['cls'])();shot.render()
        assert abs(shot.time-(s['end']-s['start']))<1/30+.0001
        for record in shot.audit:
            sentence=m.DATA['segments'][record['sentence']-1]
            expected=max(s['start'],sentence['start'])
            if expected<s['end']:assert abs(record['at']-expected)<1/30+.0001,(s['id'],record,expected)
        print(f'Layout and timing OK: {s["id"]:02}',flush=True)
for s in m.DATA['segments']:
    caption=m.text(m.wrap(s['text']),-6.2,size=25,width=7.5)
    assert caption.get_bottom()[1]>-7.5 and caption.get_top()[1]<-5.05
assert len((HERE/'tts_script.txt').read_text(encoding='utf-8').strip().split('\n\n'))==11
print('30 captions, 11 timelines, font, frame and caption safe zones verified.')
