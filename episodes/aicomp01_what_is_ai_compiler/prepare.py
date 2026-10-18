"""Derive narration, pronunciation script, timing and subtitles from approved text."""
import json
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENDS = [6,13,19,26,32,38,45,52,60,68,74,79,86,94,98,101,106,113,120,131,143,151,161]
spoken = ROOT.joinpath('approved_segments.txt').read_text(encoding='utf-8-sig').splitlines()
assert len(spoken) == len(ENDS) == 23 and all(a < b for a,b in zip([0]+ENDS,ENDS))
mapping = {'에이아이':'AI','렐루':'ReLU','씨피유':'CPU','지피유':'GPU','엑스엘에이':'XLA','파이토치':'PyTorch','토치 컴파일':'torch.compile','토치 다이나모':'TorchDynamo','토치 인덕터':'TorchInductor'}
display = []
for line in spoken:
    for a,b in mapping.items(): line=line.replace(a,b)
    display.append(line)
ROOT.joinpath('tts_script.txt').write_text('\n\n'.join(spoken)+'\n',encoding='utf-8')
heads={0:'도입 · 왜 별도의 이름이 있을까?',2:'실행 명령과 수학적 구조',4:'행렬곱에서 여러 층의 계산으로',11:'텐서의 의미와 변환 조건',15:'신경망 프로그램에서 실행 코드로',21:'결론 · 무엇에 특화되는가?'}
out=['# AI 컴파일러란 무엇일까?','사용자 확정 23개 발화 구간·161초. 실제 음원 파일은 미제공이며 종료 시각을 기준으로 제작한다.']
for i,line in enumerate(display):
    if i in heads: out.append('## '+heads[i])
    out.append(line)
ROOT.joinpath('narration.md').write_text('\n\n'.join(out)+'\n',encoding='utf-8')
segments=[dict(start=s,end=e,text=t) for s,e,t in zip([0]+ENDS[:-1],ENDS,display)]
ROOT.joinpath('timing.json').write_text(json.dumps(dict(duration_seconds=161,basis='user-provided cumulative utterance end times; audio not supplied',sentence_end_seconds=ENDS,segments=segments),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
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
print('Prepared 23 utterances, 161 seconds,',len(subs),'subtitle cues')
