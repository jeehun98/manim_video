"""Build episode 02 script assets from exact user-provided sentence ends."""
import importlib.util
import json
import re
import textwrap
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT/'episodes/nncalc02_induction_heads'
spec=importlib.util.spec_from_file_location('nncalc02_content',FOLDER/'content.py')
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)

def screen(s):
    s=s.replace('에이','A')
    for spoken,letter in [('비','B'),('씨','C'),('디','D')]:
        s=re.sub(spoken+r'(?=[가를에이,\.\s])',letter,s)
    return s.replace('인덕션 헤드','Induction Head').replace('트랜스포머','Transformer').replace('어텐션','Attention')
def stamp(t):
    ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'
def main():
    cues=[];start=0
    for i,(end,spoken) in enumerate(c.LINES):
        assert end>start
        cues.append(dict(index=i,start=start,end=end,text=screen(spoken),spoken=spoken));start=end
    assert start==c.DURATION
    md=[f'# 신경망 내부의 계산 02 — {c.TITLE} — Induction Heads','','사용자 확정 대본 및 33개 누적 종료 시각 기준 165초. 일반용·쇼츠용 동일 발화.','']
    segments=[];tts=[]
    for i,(title,first,last) in enumerate(c.CHAPTERS,1):
        subset=cues[first:last+1]
        segments.append(dict(index=i,title=title,start=subset[0]['start'],end=subset[-1]['end'],cues=subset))
        tts.append(' '.join(q['spoken'] for q in subset))
        md.extend([f'## {i:02}. {title} · {subset[0]["start"]}–{subset[-1]["end"]}초',''])
        for q in subset:md.extend([q['text'],f'<!-- 누적 종료 {q["end"]}초 -->',''])
    data=dict(episode='nncalc02',duration=c.DURATION,fps=30,timing_basis='user_provided_cumulative_sentence_end_times',
              script_approved=True,audio_file_supplied=False,measured_audio_sync=False,segments=segments,cues=cues)
    (FOLDER/'narration.md').write_text('\n'.join(md),encoding='utf-8')
    (FOLDER/'tts_script.txt').write_text('\n\n'.join(tts)+'\n',encoding='utf-8')
    (FOLDER/'timing.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for name,width in [('captions.srt',60),('captions_shorts.srt',29)]:
        out=[]
        for i,q in enumerate(cues,1):
            wrapped=textwrap.fill(q['text'],width=width,break_long_words=False,break_on_hyphens=False)
            out.append(f'{i}\n{stamp(q["start"])} --> {stamp(q["end"])}\n{wrapped}\n')
        (FOLDER/name).write_text('\n'.join(out),encoding='utf-8')
    print(f'{len(cues)} exact user-timed cues, {len(segments)} scenes, {start}s')
if __name__=='__main__':main()
