"""Single post-concat caption track with half-open, non-overlapping ASS events."""
import argparse,json,subprocess,textwrap
from pathlib import Path
ROOT=Path(__file__).resolve().parent
W=ROOT.parents[3]
def ass_time(t):
 cs=round(t*100)
 return f'{cs//360000}:{cs//6000%60:02}:{cs//100%60:02}.{cs%100:02}'
def create_ass(layout):
 rows=json.loads((ROOT/'narration_timing.json').read_text(encoding='utf-8'))
 assert all(a['end']==b['start'] for a,b in zip(rows,rows[1:]))
 short=layout=='shorts';width,height=(1080,1920) if short else (1920,1080)
 x,y=(540,1608) if short else (960,912)
 header=f'''[Script Info]
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,Malgun Gothic,48,&H00FAF3ED,&H00FAF3ED,&H0023140B,&H0023140B,0,0,0,0,100,100,0,0,1,0,0,5,80,80,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
 events=[]
 for r in rows:
  body=r'\N'.join(textwrap.wrap(r['text'],width=24 if short else 48))
  events.append(f'Dialogue: 0,{ass_time(r["start"])},{ass_time(r["end"])},Caption,,0,0,0,,{{\\pos({x},{y})}}{body}')
 path=ROOT/f'captions_{layout}.ass';path.write_text(header+'\n'.join(events)+'\n',encoding='utf-8');return path
def burn(source,target,layout,preview=False,clear_legacy=True):
 ass=create_ass(layout);short=layout=='shorts'
 # This band is reserved solely for narration, below the notes and above progress.
 # It also cleans captions from legacy per-scene renders, allowing safe rebuilds.
 filters=[]
 if clear_legacy:
  y,h=((1430/1920,330/1920) if short else (820/1080,185/1080))
  filters.append(f'drawbox=x=0:y=ih*{y}:w=iw:h=ih*{h}:color=0x0B1423:t=fill')
 filters.append(f'ass={ass.name}')
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(Path(source).resolve()),'-an','-vf',','.join(filters),'-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(Path(target).resolve())],cwd=ROOT,check=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--layout',choices=['shorts','longform'],required=True);p.add_argument('--preview',action='store_true');a=p.parse_args()
 suffix=a.layout+('_preview' if a.preview else '_final')
 source=W/'exports'/f'minimal04_v2_158s_{suffix}.mp4'
 target=source.with_name(source.stem+'_caption_fixed.mp4')
 burn(source,target,a.layout,a.preview);print(target)
