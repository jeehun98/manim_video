"""Allocate science14's draft duration by spoken character count, without audio."""
import argparse,json,re,textwrap
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];EPISODE=ROOT/'episodes/science14_attosecond_pulses'
def weight(text): return sum(c.isalnum() for c in text)
def stamp(frame):
    ms=round(frame*1000/30);return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--duration',type=float,default=120);a=p.parse_args()
    if a.duration<=0 or a.duration>=180:p.error('Duration must be between 0 and 180 seconds.')
    source=(EPISODE/'narration.md').read_text(encoding='utf-8');title=source.split('\n',1)[0]
    dialogue=[s.strip() for s in re.findall(r'## [^\n]+\n\s*([^#]+)',source)]
    if len(dialogue)!=15:raise ValueError('Expected exactly fifteen scene dialogues.')
    weights=[weight(s) for s in dialogue];total=round(a.duration*30)
    edges=[round(total*sum(weights[:i])/sum(weights)) for i in range(16)]
    cues=[dict(start_frame=x,end_frame=y,characters=w,text=t) for x,y,w,t in zip(edges,edges[1:],weights,dialogue)]
    data=dict(duration=total/30,fps=30,method='alphanumeric characters; excludes spaces and punctuation',cues=cues)
    (EPISODE/'timing.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (EPISODE/'narration.md').write_text(title+'\n\n'+'\n\n'.join(f'## {x/30:.2f}–{y/30:.2f}초\n\n{t}' for x,y,t in zip(edges,edges[1:],dialogue))+'\n',encoding='utf-8')
    (EPISODE/'tts_script.txt').write_text('\n\n'.join(dialogue)+'\n',encoding='utf-8')
    entries=[]
    for cue in cues:
        parts=re.split(r'(?<=[.?,])\s+',cue['text']);ws=[weight(s) for s in parts];span=cue['end_frame']-cue['start_frame']
        bounds=[cue['start_frame']+round(span*sum(ws[:i])/sum(ws)) for i in range(len(parts)+1)]
        for x,y,t in zip(bounds,bounds[1:],parts):
            lines='\n'.join(textwrap.wrap(t,width=29,break_long_words=False,break_on_hyphens=False))
            entries.append(f'{len(entries)+1}\n{stamp(x)} --> {stamp(y)}\n{lines}\n')
    (EPISODE/'captions.srt').write_text('\n'.join(entries),encoding='utf-8')
    for i,c in enumerate(cues,1):print(f"{i}: {c['start_frame']/30:.2f}-{c['end_frame']/30:.2f}s")
if __name__=='__main__':main()
