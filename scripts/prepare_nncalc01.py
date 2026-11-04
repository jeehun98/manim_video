"""Generate assets from user-provided sentence ends, never estimated timing."""
import importlib.util
import json
import textwrap
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT/'episodes/nncalc01_same_answers'
spec=importlib.util.spec_from_file_location('nncalc_content',FOLDER/'content.py')
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)

def stamp(seconds):
    ms=round(seconds*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'

def main():
    allcues=[];start=0
    for i,(end,spoken) in enumerate(c.LINES):
        assert end>start
        allcues.append(dict(index=i,start=start,end=end,text=c.screen_text(spoken),spoken=spoken))
        start=end
    assert start==c.DURATION
    chapters=[];tts=[];md=[f'# 신경망 내부의 계산 01 — {c.TITLE}','','시리즈: 신경망 내부의 계산 — 표현에서 알고리즘까지','',
        '사용자 확정 대본·문장 종료 시각 기준 164초. 16:9. 숫자는 누적 종료 시각이며 낭독하지 않는다.','']
    for i,(title,first,last) in enumerate(c.CHAPTERS,1):
        cues=allcues[first:last+1]
        chapters.append(dict(index=i,title=title,start=cues[0]['start'],end=cues[-1]['end'],cues=cues,text=' '.join(q['text'] for q in cues)))
        tts.append(' '.join(q['spoken'] for q in cues))
        md.extend([f'## {i:02}. {title} · {cues[0]["start"]}–{cues[-1]["end"]}초',''])
        for q in cues:md.extend([q['text'],f'<!-- 누적 종료 {q["end"]}초 -->',''])
    payload=dict(episode='nncalc01',revision='v3_user_timed_landscape',duration=c.DURATION,
        timing_basis='user_provided_cumulative_sentence_end_times',audio_file_supplied=False,
        aspect_ratio='16:9',resolution=[1920,1080],preview_resolution=[640,360],fps=30,
        measured_audio_sync=False,segments=chapters,cues=allcues)
    (FOLDER/'narration.md').write_text('\n'.join(md),encoding='utf-8')
    (FOLDER/'tts_script.txt').write_text('\n\n'.join(tts)+'\n',encoding='utf-8')
    (FOLDER/'timing.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    srt=[]
    for i,q in enumerate(allcues,1):
        lines=textwrap.fill(q['text'],width=57,break_long_words=False,break_on_hyphens=False)
        srt.append(f'{i}\n{stamp(q["start"])} --> {stamp(q["end"])}\n{lines}\n')
    (FOLDER/'captions.srt').write_text('\n'.join(srt),encoding='utf-8')
    shorts_srt=[]
    for i,q in enumerate(allcues,1):
        lines=textwrap.fill(q['text'],width=29,break_long_words=False,break_on_hyphens=False)
        shorts_srt.append(f'{i}\n{stamp(q["start"])} --> {stamp(q["end"])}\n{lines}\n')
    (FOLDER/'captions_shorts.srt').write_text('\n'.join(shorts_srt),encoding='utf-8')
    (FOLDER/'draft_status.json').write_text(json.dumps(dict(revision=payload['revision'],phase='production',
        script_approved=True,speech_timing_provided_for_this_revision=True,duration_seconds=c.DURATION,
        timing_basis=payload['timing_basis'],audio_file_supplied=False),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'{len(allcues)} user-timed cues; {len(chapters)} scenes; {start} seconds; landscape 16:9')

if __name__=='__main__':main()
