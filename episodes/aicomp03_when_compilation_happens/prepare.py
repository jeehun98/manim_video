"""Derive narration, pronunciation script, timing and subtitles from approved text."""
import json
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENDS = [5, 10, 17, 23, 30, 39, 43, 51, 61, 68, 74, 81, 89, 95, 103, 109, 119, 126, 132, 142]
spoken = ROOT.joinpath('approved_segments.txt').read_text(encoding='utf-8-sig').splitlines()
assert len(spoken) == len(ENDS) == 20 and all(a < b for a,b in zip([0]+ENDS,ENDS))
mapping = {'에이아이':'AI','렐루':'ReLU','씨피유':'CPU','지피유':'GPU','엑스엘에이':'XLA','파이토치':'PyTorch','토치 컴파일':'torch.compile','토치 다이나모':'TorchDynamo','토치 인덕터':'TorchInductor','이거 실행':'Eager 실행','에이오티':'AOT','제이아이티':'JIT','런타임 디스패치':'Runtime Dispatch','배치 크기 팔':'배치 크기 8','육십사':'64'}
display = []
for line in spoken:
    for a,b in mapping.items(): line=line.replace(a,b)
    display.append(line)
ROOT.joinpath('tts_script.txt').write_text('\n\n'.join(spoken)+'\n',encoding='utf-8')
heads={0:'도입 · 실행할 때마다 만들까?',2:'실행 전에 준비하는 AOT',6:'실행 과정에서 만드는 JIT',9:'두 번째 호출과 코드 재사용',12:'준비된 코드 중에서 고르기',17:'결론 · 생성, 선택, 실행의 시간'}
out=['# AI 컴파일러는 언제 코드를 만들까? — AOT, JIT와 Runtime Dispatch | AI 컴파일러 03','사용자 확정 20개 발화 구간·142초. 실제 음원은 미제공이며 종료 시각을 기준으로 제작한다.']
for i,line in enumerate(display):
    if i in heads: out.append('## '+heads[i])
    out.append(line)
ROOT.joinpath('narration.md').write_text('\n\n'.join(out)+'\n',encoding='utf-8')
segments=[dict(start=s,end=e,text=t) for s,e,t in zip([0]+ENDS[:-1],ENDS,display)]
ROOT.joinpath('timing.json').write_text(json.dumps(dict(duration_seconds=142,basis='user-provided cumulative utterance end times; audio not supplied',sentence_end_seconds=ENDS,segments=segments),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
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
print('Prepared 20 utterances, 142 seconds,',len(subs),'subtitle cues')
