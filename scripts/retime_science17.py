"""Allocate science17 draft timing and regenerate narration, TTS and captions."""
import argparse,json,re,textwrap
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];EP=ROOT/'episodes/science17_why_chiral_nobel'
def weight(t):return sum(c.isalnum() for c in t)
def stamp(f):
 m=round(f*1000/30);return f'{m//3600000:02d}:{m//60000%60:02d}:{m//1000%60:02d},{m%1000:03d}'
def main():
 p=argparse.ArgumentParser();p.add_argument('--duration',type=float,default=126);p.add_argument('--end-times');a=p.parse_args();src=(EP/'narration.md').read_text(encoding='utf-8');title=src.split('\n',1)[0]
 parts=[s.strip() for s in re.findall(r'## [^\n]+\n\s*([^#]+)',src)];weights=[weight(s) for s in parts]
 if a.end_times:
  ends=[float(x) for x in a.end_times.split(',')]
  if len(ends)!=len(parts):raise SystemExit(f'expected {len(parts)} end times')
  frames=[0]+[round(x*30) for x in ends];method='measured TTS cue boundaries'
 else:
  total=round(a.duration*30);frames=[round(total*sum(weights[:i])/sum(weights)) for i in range(len(parts)+1)];method='character weighted draft'
 cues=[dict(start_frame=x,end_frame=y,characters=w,text=t) for x,y,w,t in zip(frames,frames[1:],weights,parts)]
 (EP/'timing.json').write_text(json.dumps(dict(duration=frames[-1]/30,fps=30,method=method,cues=cues),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (EP/'narration.md').write_text(title+'\n\n'+'\n\n'.join(f'## {x/30:.2f}–{y/30:.2f}초\n\n{t}' for x,y,t in zip(frames,frames[1:],parts))+'\n',encoding='utf-8')
 (EP/'tts_script.txt').write_text('\n\n'.join(parts)+'\n',encoding='utf-8');out=[]
 for cue in cues:
  sentences=re.split(r'(?<=[.?!])\s+',cue['text']);sw=[weight(s) for s in sentences];span=cue['end_frame']-cue['start_frame'];bounds=[cue['start_frame']+round(span*sum(sw[:i])/sum(sw)) for i in range(len(sentences)+1)]
  for x,y,t in zip(bounds,bounds[1:],sentences):out.append(f'{len(out)+1}\n{stamp(x)} --> {stamp(y)}\n'+'\n'.join(textwrap.wrap(t,29,break_long_words=False))+'\n')
 (EP/'captions.srt').write_text('\n'.join(out),encoding='utf-8')
if __name__=='__main__':main()
