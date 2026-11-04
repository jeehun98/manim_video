"""Create script, captions and timing from the approved 33 user-timed lines."""
import importlib.util
import json
import textwrap
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT/'episodes/nncalc05_sparse_autoencoders'
spec=importlib.util.spec_from_file_location('superposition_content',FOLDER/'content.py')
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
def screen(s):
    return s

def pronunciation(s):
    return (s.replace('Sparse Autoencoder','스파스 오토인코더')
        .replace('Towards Monosemanticity','투워즈 모노시맨티시티').replace('Base64','베이스 육십사'))

def stamp(t):
    ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'
def main():
    cues=[];start=0
    for i,(end,spoken) in enumerate(c.LINES):
        assert end>start;cues.append(dict(index=i,start=start,end=end,spoken=spoken,text=screen(spoken)));start=end
    assert start==c.DURATION
    md=[f'# 신경망 내부의 계산 05 — {c.TITLE} — Sparse Autoencoders','',f'사용자 수정 확정 대본·{len(cues)}개 누적 종료 시각 기준 {c.DURATION}초. 일반·쇼츠 동일 발화.','']
    segments=[];tts=[]
    for i,(title,first,last) in enumerate(c.CHAPTERS,1):
        subset=cues[first:last+1]
        segments.append(dict(index=i,title=title,start=subset[0]['start'],end=subset[-1]['end'],cues=subset))
        tts.extend(pronunciation(q['spoken']) for q in subset)
        md.extend([f'## {i:02}. {title} · {subset[0]["start"]}–{subset[-1]["end"]}초',''])
        for q in subset:md.extend([q['text'],f'<!-- 누적 종료 {q["end"]}초 -->',''])
    data=dict(episode='nncalc05',duration=c.DURATION,fps=30,timing_basis='user_provided_cumulative_sentence_end_times',
        script_approved=True,audio_file_supplied=False,measured_audio_sync=False,segments=segments,cues=cues)
    (FOLDER/'narration.md').write_text('\n'.join(md),encoding='utf-8')
    (FOLDER/'tts_script.txt').write_text('\n\n'.join(tts)+'\n',encoding='utf-8')
    (FOLDER/'timing.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for name,width in [('captions.srt',60),('captions_shorts.srt',29)]:
        blocks=[]
        for i,q in enumerate(cues,1):
            lines=textwrap.fill(q['text'],width=width,break_long_words=False,break_on_hyphens=False)
            blocks.append(f'{i}\n{stamp(q["start"])} --> {stamp(q["end"])}\n{lines}\n')
        (FOLDER/name).write_text('\n'.join(blocks),encoding='utf-8')
    print(f'{len(cues)} user-timed cues; {len(segments)} scenes; {start}s')
if __name__=='__main__':main()
