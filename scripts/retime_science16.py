"""Allocate science16's draft duration by spoken character count, without audio."""
import argparse,json,re,textwrap
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];EPISODE=ROOT/'episodes/science16_chiral_amplification'
def weight(t):return sum(c.isalnum() for c in t)
def stamp(f):
 m=round(f*1000/30);return f'{m//3600000:02d}:{m//60000%60:02d}:{m//1000%60:02d},{m%1000:03d}'
def main():
 p=argparse.ArgumentParser();p.add_argument('--duration',type=float,default=145);p.add_argument('--end-times',help='comma-separated cumulative cue end times in seconds');a=p.parse_args();src=(EPISODE/'narration.md').read_text(encoding='utf-8');title=src.split('\n',1)[0]
 d=[s.strip() for s in re.findall(r'## [^\n]+\n\s*([^#]+)',src)];w=[weight(s) for s in d]
 if a.end_times:
  ends=[float(x) for x in a.end_times.split(',')]
  if len(ends)!=len(d) or any(b<=a for a,b in zip([0]+ends[:-1],ends)):raise SystemExit(f'expected {len(d)} strictly increasing end times')
  e=[0]+[round(x*30) for x in ends];method='measured TTS cue boundaries'
 else:
  total=round(a.duration*30);e=[round(total*sum(w[:i])/sum(w)) for i in range(len(d)+1)];method='character weighted draft'
 total=e[-1];cues=[dict(start_frame=x,end_frame=y,characters=z,text=t) for x,y,z,t in zip(e,e[1:],w,d)];(EPISODE/'timing.json').write_text(json.dumps(dict(duration=total/30,fps=30,method=method,cues=cues),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (EPISODE/'narration.md').write_text(title+'\n\n'+'\n\n'.join(f'## {x/30:.2f}–{y/30:.2f}초\n\n{t}' for x,y,t in zip(e,e[1:],d))+'\n',encoding='utf-8');(EPISODE/'tts_script.txt').write_text('\n\n'.join(d)+'\n',encoding='utf-8')
 out=[]
 for c in cues:
  ps=re.split(r'(?<=[.?,])\s+',c['text']);pw=[weight(s) for s in ps];sp=c['end_frame']-c['start_frame'];b=[c['start_frame']+round(sp*sum(pw[:i])/sum(pw)) for i in range(len(ps)+1)]
  for x,y,t in zip(b,b[1:],ps):out.append(f'{len(out)+1}\n{stamp(x)} --> {stamp(y)}\n'+'\n'.join(textwrap.wrap(t,29,break_long_words=False))+'\n')
 (EPISODE/'captions.srt').write_text('\n'.join(out),encoding='utf-8')
if __name__=='__main__':main()
