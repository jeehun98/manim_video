"""Extract a contact sheet and record video metadata for visual review."""
from pathlib import Path
import sys,json
import av
from PIL import Image,ImageDraw

path=Path(sys.argv[1]); target=path.with_suffix('.contact.jpg')
manifest=json.loads(Path(__file__).with_name('manifest.json').read_text(encoding='utf-8'))
times=[];offset=0
for scene in manifest:
    duration=scene['duration_seconds'] if scene['duration_seconds'] is not None else scene['storyboard_seconds']
    times.extend([offset+duration*.25,offset+duration*.85]);offset+=duration
sheet=Image.new('RGB',(1280,4*386),'#081622'); draw=ImageDraw.Draw(sheet)
with av.open(str(path)) as video:
    s=video.streams.video[0]
    metadata={'width':s.width,'height':s.height,'fps':str(s.average_rate),'frames':s.frames,'duration_seconds':float(s.duration*s.time_base),'audio_streams':len(video.streams.audio),'codec':s.codec_context.name}
    for i,t in enumerate(times):
        video.seek(int(t/s.time_base),stream=s,backward=True)
        frame=next(f for f in video.decode(s) if float(f.pts*f.time_base)>=t)
        im=frame.to_image();im.thumbnail((640,360))
        x=i%2*640;y=i//2*386
        if y+386>sheet.height:
            enlarged=Image.new('RGB',(1280,y+386),'#081622'); enlarged.paste(sheet,(0,0));sheet=enlarged;draw=ImageDraw.Draw(sheet)
        sheet.paste(im,(x,y));draw.text((x+8,y+362),f'{t}s',fill='white')
sheet.save(target)
path.with_suffix('.metadata.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
print(metadata); print(target)
