"""Inspect all fifteen cue interiors and verify encoded delivery metadata."""
import json
import sys
from pathlib import Path
import av
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[1]
mode='final' if '--final' in sys.argv else 'preview'
filename='science20.mp4' if mode=='final' else 'science20_preview.mp4'
data=json.loads((ROOT/'episodes/science20_superluminal_expansion/timing.json').read_text(encoding='utf-8'))
ends=[8,17,25,32,38,48,57,69,76,85,94,104,112,121,132]
assert [c['end_frame'] for c in data['cues']]==[t*30 for t in ends]
assert all(a['end_frame']==b['start_frame'] for a,b in zip(data['cues'],data['cues'][1:]))
targets=[(c['start_frame']+.83*(c['end_frame']-c['start_frame']))/30 for c in data['cues']]
container=av.open(str(ROOT/'exports'/filename));stream=container.streams.video[0]
assert (stream.width,stream.height)==((1080,1920) if mode=='final' else (360,640))
assert len(container.streams.audio)==0
sheet=Image.new('RGB',(5*216,3*404),'#080E1B');draw=ImageDraw.Draw(sheet)
index=0;count=0
for frame in container.decode(stream):
    count+=1
    if index<len(targets) and float(frame.time)>=targets[index]:
        x=index%5*216;y=index//5*404
        sheet.paste(frame.to_image().resize((216,384)),(x,y))
        draw.text((x+4,y+384),f'{index+1}: {frame.time:.2f}s',fill='white');index+=1
        if mode=='final' and index==15:
            frame.to_image().save(ROOT/'exports/science20_thumbnail.png')
assert index==15
assert count==3960,count
assert abs(float(stream.duration*stream.time_base)-132)<.05
sheet.save(ROOT/'exports'/f'science20_{mode}_review.jpg')
print(dict(mode=mode,width=stream.width,height=stream.height,frames=count,
           duration=float(stream.duration*stream.time_base),audio=0))
