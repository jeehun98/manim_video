"""Persist the approved narration and supplied sentence boundaries."""
import json
import shutil
from pathlib import Path

HERE=Path(__file__).resolve().parent
LINES='''4|인공지능 산업의 경쟁 중심이 학습에서 추론으로 이동하고 있습니다.
9|그런데 AI를 학습시킬 때와 우리가 AI에게 질문할 때, GPU는 같은 일을 할까요?
15|사실 학습과 추론은 같은 신경망을 사용하지만, 수행하는 연산과 해결해야 할 문제가 다릅니다.
19|학습은 데이터를 이용해 모델의 가중치를 바꾸는 과정입니다.
25|모델이 예측한 결과와 정답의 차이를 계산하고, 역전파를 통해 기울기를 구한 뒤 가중치를 수정합니다.
32|즉, 순전파뿐 아니라 역전파와 가중치 갱신까지 반복하며 막대한 양의 행렬 연산을 수행합니다.
38|반면 우리가 일상적으로 사용하는 ChatGPT 같은 언어모델 서비스는 주로 추론을 수행합니다.
44|사용자가 프롬프트를 입력하면, 이미 학습된 모델이 그 입력을 바탕으로 답변을 생성합니다.
48|이때는 역전파나 가중치 갱신 없이, 주로 순전파 연산을 수행합니다.
50|여기서 중요한 차이가 있습니다.
55|일반적인 추론에서는 대화를 아무리 많이 나누더라도 모델의 가중치 자체는 바뀌지 않습니다.
61|그렇다면 AI는 어떻게 이전 대화를 기억하고, 새로운 질문에 활용할 수 있을까요?
66|모델이 다시 학습하는 것이 아니라, 이전 대화가 다음 입력의 문맥으로 제공되기 때문입니다.
70|하지만 대화가 길어질수록 처리해야 할 문맥도 늘어납니다.
75|이전 내용을 매번 처음부터 계산한다면 매우 비효율적이겠죠.
81|그래서 언어모델은 이전 토큰에서 계산한 Key와 Value를 저장하고, 다음 토큰을 생성할 때 재사용합니다.
83|이것이 KV Cache입니다.
88|모델의 가중치는 그대로인데, 대화가 길어질수록 필요한 계산 상태는 증가할 수 있는 것입니다.
91|여기서 추론은 다시 두 단계로 나뉩니다.
97|사용자의 프롬프트를 처리하는 Prefill 단계에서는 여러 토큰의 연산을 병렬로 수행합니다.
104|반면 답변을 생성하는 Decode 단계에서는 토큰을 하나씩 만들면서 모델의 가중치와 기존 KV Cache를 사용합니다.
112|특히 한 번에 처리하는 요청이 적을 때는 GPU의 계산 능력보다 메모리에서 데이터를 읽어오는 속도가 병목이 되기도 합니다.
118|GPU가 계산을 못 해서 느린 것이 아니라, 계산에 필요한 데이터를 기다리느라 느려지는 것입니다.
123|여기에 수많은 사용자가 동시에 접속하면, 각 사용자의 문맥 상태까지 관리해야 합니다.
133|이 때문에 추론 단계의 GPU와 CUDA 최적화에서는 단순한 연산 속도뿐 아니라 메모리 접근, 데이터 이동, 실행 지연시간을 줄이는 방법도 중요해집니다.
138|최근 AI 반도체에서 HBM의 용량과 대역폭이 주목받는 이유 중 하나입니다.
145|결국 학습과 추론은 같은 GPU를 사용하더라도, 연산의 구조와 최적화해야 할 병목이 서로 다릅니다.
149|따라서 GPU 최적화는 단순히 연산을 더 빠르게 만드는 문제가 아닙니다.
155|어떤 연산이 반복되고, 어떤 데이터가 재사용되며, 어디에서 시간이 소요되는지를 먼저 이해해야 합니다.
161|최적화는 빠르게 만드는 방법을 찾기 전에, 무엇이 느린지 이해하는 것에서 시작되기 때문입니다.'''

def stamp(t):
    return f'{int(t)//3600:02}:{int(t)//60%60:02}:{int(t)%60:02},000'

def main():
    segments=[];start=0
    for line in LINES.splitlines():
        end,text=line.split('|',1);end=int(end)
        segments.append(dict(id=len(segments)+1,start=start,end=end,text=text));start=end
    boundaries=[0,9,32,55,66,75,88,104,118,123,138,161]
    titles=['같은 GPU, 다른 일?','학습은 가중치를 바꾼다','추론은 가중치를 사용한다','기억과 학습은 다르다','길어지는 문맥, 반복되는 계산','KV Cache: 계산 결과 재사용','Prefill과 Decode','계산보다 데이터가 늦다면','공유하는 모델, 요청별 상태','데이터 이동도 최적화한다','무엇이 느린지 먼저 이해하라']
    scenes=[dict(id=i+1,start=a,end=b,title=titles[i],cls=f'Shot{i+1:02}') for i,(a,b) in enumerate(zip(boundaries,boundaries[1:]))]
    (HERE/'timing.json').write_text(json.dumps(dict(duration=161,fps=30,audio=None,timing_source='user supplied sentence end seconds',segments=segments,scenes=scenes),ensure_ascii=False,indent=2),encoding='utf-8')
    (HERE/'narration.md').write_text('# 학습과 추론, GPU가 해결하는 서로 다른 문제\n\n사용자 확정 대본 · 문장 종료 시각 기준 · 총 161초\n\n'+'\n\n'.join(f'[{s["start"]:03}–{s["end"]:03}s] {s["text"]}' for s in segments)+'\n',encoding='utf-8')
    pronunciation={'ChatGPT':'챗지피티','GPU':'지피유','CUDA':'쿠다','HBM':'에이치비엠','KV Cache':'케이브이 캐시','Prefill':'프리필','Decode':'디코드','Key':'키','Value':'밸류','AI':'에이아이'}
    paragraphs=[]
    for scene in scenes:
        text='\n'.join(s['text'] for s in segments if scene['start']<=s['start']<scene['end'])
        for a,b in pronunciation.items():text=text.replace(a,b)
        paragraphs.append(text)
    (HERE/'tts_script.txt').write_text('\n\n'.join(paragraphs)+'\n',encoding='utf-8')
    (HERE/'captions.srt').write_text('\n\n'.join(f'{s["id"]}\n{stamp(s["start"])} --> {stamp(s["end"])}\n{s["text"]}' for s in segments)+'\n',encoding='utf-8')
    source=Path('C:/Users/as042/.codex/attachments/8da881f8-6ad8-4471-9a07-6110ca62613e/붙여넣은 텍스트.txt')
    if source.exists():shutil.copyfile(source,HERE/'storyboard_original.md')

if __name__=='__main__':main()
