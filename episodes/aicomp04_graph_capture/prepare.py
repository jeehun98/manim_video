"""Derive narration, pronunciation script, timing and subtitles from approved text."""
import json
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENDS = [6, 17, 26, 34, 38, 45, 52, 60, 64, 74, 80, 89, 96, 100, 110, 115, 123, 131, 136, 143, 152]
spoken = ROOT.joinpath('approved_segments.txt').read_text(encoding='utf-8-sig').splitlines()
assert len(spoken) == len(ENDS) == 21 and all(a < b for a,b in zip([0]+ENDS,ENDS))
mapping = {'에이아이':'AI','렐루':'ReLU','파이토치 에프엑스':'PyTorch FX','파이토치':'PyTorch','토치 컴파일':'torch.compile','토치 다이나모':'TorchDynamo','심볼릭 트레이싱':'Symbolic Tracing','트레이싱':'Tracing','그래프 브레이크':'Graph Break','영보다':'0보다'}

display = []
for line in spoken:
    for a,b in mapping.items(): line=line.replace(a,b)
    display.append(line)
ROOT.joinpath('tts_script.txt').write_text('\n\n'.join(spoken)+'\n',encoding='utf-8')
heads={0:'01 · 프로그램 전체가 하나의 그래프일까?',1:'02 · 계산 관계',3:'03 · Graph Capture',4:'04 · FX Symbolic Tracing',9:'05 · 서로 다른 포착 방식',10:'06 · 데이터 의존 조건 분기',12:'07 · Graph Break',14:'08 · Runtime Execution',16:'09 · 지원 범위',18:'10 · 프로그램과 포착 범위'}
out=['# 파이썬 신경망은 어떻게 계산 그래프가 될까? — Tracing과 Graph Break | AI 컴파일러 04','사용자 확정 21개 발화 구간·152초. 실제 음원은 미제공이며 종료 시각을 기준으로 제작한다.']
for i,line in enumerate(display):
    if i in heads: out.append('## '+heads[i])
    out.append(line)
ROOT.joinpath('narration.md').write_text('\n\n'.join(out)+'\n',encoding='utf-8')
segments=[dict(start=s,end=e,text=t) for s,e,t in zip([0]+ENDS[:-1],ENDS,display)]
ROOT.joinpath('timing.json').write_text(json.dumps(dict(duration_seconds=152,basis='user-provided cumulative utterance end times; audio not supplied',sentence_end_seconds=ENDS,scene_end_seconds=[6,26,34,64,74,89,100,115,131,152],segments=segments),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def stamp(s):
    ms=round(s*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
# Split each supplied utterance into readable subtitle units within its exact bounds.
subs=[]
for seg in segments:
    chunks=textwrap.wrap(seg['text'],width=43,break_long_words=False,break_on_hyphens=False)
    units=['\n'.join(chunks[i:i+2]) for i in range(0,len(chunks),2)]
    weight=sum(len(x) for x in units);cursor=seg['start']
    for j,unit in enumerate(units):
        end=seg['end'] if j==len(units)-1 else cursor+(seg['end']-seg['start'])*len(unit)/weight
        subs.append(f'{len(subs)+1}\n{stamp(cursor)} --> {stamp(end)}\n{unit}\n');cursor=end
ROOT.joinpath('captions.srt').write_text('\n'.join(subs),encoding='utf-8')
print('Prepared 21 utterances, 152 seconds,',len(subs),'subtitle cues')
