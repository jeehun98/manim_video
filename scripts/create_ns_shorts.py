"""Create uncropped 9:16 versions of acts whose actual duration is <=180s."""
from pathlib import Path
import json,subprocess
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'exports'/'shorts'
rows=json.loads((OUT/'selection.json').read_text())
filters='[0:v]split=2[bg][fg];[bg]scale=270:480:force_original_aspect_ratio=increase,crop=270:480,boxblur=12:2,eq=brightness=-0.10,scale=1080:1920,setsar=1[back];[fg]scale=1080:-2,setsar=1[front];[back][front]overlay=(W-w)/2:(H-h)/2,format=yuv420p[v]'
for r in rows:
 if not r['selected']:continue
 p=ROOT/r['file'];output=OUT/f"ns_{r['act']}_shorts_1080x1920.mp4"
 with (OUT/f"ns_{r['act']}_render.log").open('w') as log:
  subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','warning','-i',str(p),'-filter_complex',filters,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','20','-c:a','copy','-movflags','+faststart',str(output)],stdout=log,stderr=log,check=True)
 print('Created',output.name,flush=True)
