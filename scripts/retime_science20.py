"""Apply user-supplied cumulative speech endpoints, without estimating scene lengths."""
import json
import re
import textwrap
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT/'episodes/science20_superluminal_expansion'
ENDS=[8,17,25,32,38,48,57,69,76,85,94,104,112,121,132]

def stamp(frame):
    ms=round(frame*1000/30)
    return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'

def weight(s): return sum(c.isalnum() for c in s)

def main():
    source=(FOLDER/'narration.md').read_text(encoding='utf-8')
    sections=re.findall(r'^## ([^\n]+)\n\n(.*?)(?=\n## |\Z)',source,re.M|re.S)
    assert len(sections)==len(ENDS)==15
    boundaries=[0]+[round(t*30) for t in ENDS]
    cues=[dict(start_frame=a,end_frame=b,title=title,text=body.strip())
          for a,b,(title,body) in zip(boundaries,boundaries[1:],sections)]
    data=dict(duration=132,fps=30,method='user-provided cumulative narration endpoints',
              end_seconds=ENDS,subtitle_sentence_timing='character-proportional within measured scene boundaries',cues=cues)
    (FOLDER/'timing.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    title=source.splitlines()[0]
    (FOLDER/'narration.md').write_text(title+'\n\n상태: 대본 확정 · 사용자 제공 종료 시각 반영 · 전체 132초.\n\n'+'\n\n'.join(
        f"## {c['title']}\n\n{c['text']}" for c in cues)+'\n',encoding='utf-8')
    spoken=[];subtitles=[]
    for cue in cues:
        s=cue['text']
        for a,b in [('HD로','에이치와 디의 곱으로'),('H','에이치'),('D','디'),('c','씨'),('1%','일 퍼센트')]:s=s.replace(a,b)
        spoken.append(s)
        sentences=re.split(r'(?<=[.!?])\s+',cue['text'])
        sizes=[weight(s) for s in sentences];span=cue['end_frame']-cue['start_frame']
        edges=[cue['start_frame']+round(span*sum(sizes[:i])/sum(sizes)) for i in range(len(sizes)+1)]
        for a,b,s in zip(edges,edges[1:],sentences):
            subtitles.append(f'{len(subtitles)+1}\n{stamp(a)} --> {stamp(b)}\n'+
                             '\n'.join(textwrap.wrap(s,width=29,break_long_words=False,break_on_hyphens=False))+'\n')
    (FOLDER/'tts_script.txt').write_text('\n\n'.join(spoken)+'\n',encoding='utf-8')
    (FOLDER/'captions.srt').write_text('\n'.join(subtitles),encoding='utf-8')
    print('15 cues: durations',[(b-a)/30 for a,b in zip(boundaries,boundaries[1:])],'; total 132 seconds / 3960 frames')

if __name__=='__main__':main()
