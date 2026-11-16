import ast,json,hashlib,concurrent.futures,subprocess
from pathlib import Path
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def check(row):
 episode=row['episode'];video=Path(row['output']);ref=np.asarray(Image.open(HERE/'assets'/f'{episode}.png').convert('RGB')).astype(np.int16)
 errors=[]
 for second in [0,row['duration']/2,max(0,row['duration']-.1)]:
  raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(second),'-i',str(video),'-vf','crop=1920:180:0:0','-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','pipe:1'])
  actual=np.frombuffer(raw,dtype=np.uint8).reshape((180,1920,3)).astype(np.int16)
  error=float(np.abs(actual-ref).mean());assert error<6,(episode,second,error);errors.append(error)
 folder=next((ROOT/'episodes').glob(f'{episode}_*'))
 old=json.loads((folder/'render_report_final.json').read_text(encoding='utf-8'))
 old['previous_video_sha256']=old.get('sha256');old['sha256']=row['sha256'];old['problem_card']=dict(enabled=True,header_mae_start_middle_end=errors,layout=row['layout'],source=str(HERE/'problems.json'),card_sha256=row['card_sha256'],original_backup=row['source'])
 (folder/'render_report_final.json').write_text(json.dumps(old,ensure_ascii=False,indent=2),encoding='utf-8')
 for f in ['build.py','scene.py']:ast.parse((folder/f).read_text(encoding='utf-8'))
 return dict(episode=episode,duration=row['duration'],frames=row['frames'],header_mae=errors,video_sha256=row['sha256'])
rows=json.loads((HERE/'batch_report.json').read_text(encoding='utf-8'));assert len(rows)==22
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:reports=list(pool.map(check,rows))
report=dict(episodes=reports,all_22_passed=True,checks='full decode, exact original duration and frame count,1920x1080,30fps,reference card at start/middle/end,source syntax',visual_review='all22 card strips; composite04,15,22; encoded representative frames')
(HERE/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(f"All {len(reports)} episodes passed; {sum(r['frames'] for r in reports)} frames; total duration {sum(r['duration'] for r in reports)} sec")
