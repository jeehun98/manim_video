"""Apply the measured science15 TTS cue boundaries and rebuild text timing files."""
import json,re,textwrap
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];EPISODE=ROOT/'episodes/science15_hopfield_memory'
EDGES_SECONDS=(0,8,15,23,33,41,51,60,68,75,83,93,102,110,120,129,139,151)
def weight(text): return sum(c.isalnum() for c in text)
def stamp(frame):
    ms=round(frame*1000/30);return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
def main():
    source=(EPISODE/'narration.md').read_text(encoding='utf-8');title=source.split('\n',1)[0]
    dialogue=[s.strip() for s in re.findall(r'## [^\n]+\n\s*([^#]+)',source)]
    if len(dialogue)!=17:raise ValueError('Expected exactly seventeen scene dialogues.')
    weights=[weight(s) for s in dialogue];edges=[round(second*30) for second in EDGES_SECONDS]
    cues=[dict(start_frame=x,end_frame=y,characters=w,text=t) for x,y,w,t in zip(edges,edges[1:],weights,dialogue)]
    data=dict(duration=edges[-1]/30,fps=30,method='measured TTS cue boundaries supplied by the user',cues=cues)
    (EPISODE/'timing.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (EPISODE/'narration.md').write_text(title+'\n\n'+'\n\n'.join(f'## {x/30:.2f}–{y/30:.2f}초\n\n{t}' for x,y,t in zip(edges,edges[1:],dialogue))+'\n',encoding='utf-8')
    (EPISODE/'tts_script.txt').write_text('\n\n'.join(dialogue)+'\n',encoding='utf-8')
    entries=[]
    for cue in cues:
        parts=re.split(r'(?<=[.?,])\s+',cue['text']);ws=[weight(s) for s in parts];span=cue['end_frame']-cue['start_frame']
        bounds=[cue['start_frame']+round(span*sum(ws[:i])/sum(ws)) for i in range(len(parts)+1)]
        for x,y,t in zip(bounds,bounds[1:],parts):
            lines='\n'.join(textwrap.wrap(t,width=29,break_long_words=False,break_on_hyphens=False));entries.append(f'{len(entries)+1}\n{stamp(x)} --> {stamp(y)}\n{lines}\n')
    (EPISODE/'captions.srt').write_text('\n'.join(entries),encoding='utf-8')
    for i,c in enumerate(cues,1):print(f"{i}: {c['start_frame']/30:.2f}-{c['end_frame']/30:.2f}s")
if __name__=='__main__':main()
