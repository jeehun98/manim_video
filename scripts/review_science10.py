"""Sample the encoded video at cue interiors and verify delivery metadata."""
import json
import sys
from pathlib import Path
import av
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
mode='final' if '--final' in sys.argv else 'preview'
video=ROOT/'exports'/('science10.mp4' if mode=='final' else 'science10_preview.mp4')
timing=json.loads((ROOT/'episodes/science10_cosmic_void/timing.json').read_text(encoding='utf-8'))
targets=[(c['start_frame']+int((c['end_frame']-c['start_frame'])*.82))/30 for c in timing['cues']]
container=av.open(str(video));stream=container.streams.video[0]
assert (stream.width,stream.height)==((1080,1920) if mode=='final' else (360,640))
assert len(container.streams.audio)==0
sheet=Image.new('RGB',(5*216,2*404),'#080E1B');draw=ImageDraw.Draw(sheet)
index=0;count=0
for frame in container.decode(stream):
    count+=1
    if index<len(targets) and float(frame.time)>=targets[index]:
        thumbnail=frame.to_image().resize((216,384))
        x=(index%5)*216;y=(index//5)*404
        sheet.paste(thumbnail,(x,y));draw.text((x+4,y+384),f'{index+1}: {frame.time:.2f}s',fill='white')
        index+=1
assert index==10
assert count==round(timing['duration']*30),(count,timing['duration'])
assert abs(float(stream.duration*stream.time_base)-timing['duration'])<.05
sheet.save(ROOT/'exports'/f'science10_{mode}_review.jpg')
print(json.dumps(dict(mode=mode,width=stream.width,height=stream.height,frames=count,
                     duration=float(stream.duration*stream.time_base),audio=0),indent=2))
