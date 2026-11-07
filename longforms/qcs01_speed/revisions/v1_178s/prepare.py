"""Reproduce approved script assets; times below are supplied by the user."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
LINES='''일반적인 컴퓨터는 0과 1로 정보를 표현합니다.
3
양자컴퓨터 역시 0과 1을 이용하지만, 정보를 표현하는 방식에는 중요한 차이가 있습니다.
8
일반적인 비트는 0 또는 1의 상태를 갖지만, 양자컴퓨터의 큐비트는 두 상태가 중첩된 상태로 존재할 수 있습니다.
16
이를 수학적으로 표현하면, 0과 1에 각각 확률 진폭을 부여한 형태가 됩니다.
21
그리고 여러 큐비트를 결합하면, 표현할 수 있는 상태의 수는 지수적으로 증가합니다.
25
예를 들어 큐비트가 하나라면 두 개의 상태, 두 개라면 네 개, 세 개라면 여덟 개의 계산 기저 상태를 중첩할 수 있습니다.
33
큐비트가 10개라면 1,024개, 20개라면 약 100만 개의 상태에 대한 확률 진폭을 하나의 양자 상태로 표현할 수 있습니다.
41
그렇다면 양자컴퓨터는 이 모든 경우의 수를 동시에 계산하기 때문에 빠른 것일까요?
46
정확히는 그렇지 않습니다.
48
양자컴퓨터가 여러 상태를 중첩할 수 있다고 해서, 그 상태들에 담긴 정보를 모두 읽어낼 수 있는 것은 아닙니다.
54
양자 상태를 측정하면, 일반적으로 가능한 결과 중 하나만 관측됩니다.
58
따라서 단순히 많은 상태를 중첩하는 것만으로는 원하는 정답을 얻을 수 없습니다.
63
여기서 중요한 역할을 하는 것이 바로 양자 간섭입니다.
67
파동은 서로 겹칠 때 강화되거나 상쇄될 수 있습니다.
71
예를 들어 두 파동의 마루가 겹치면 진폭이 커지지만, 마루와 골이 겹치면 서로 상쇄됩니다.
76
양자컴퓨터에서도 이와 비슷한 현상이 나타납니다.
80
하나의 결과에 도달하는 데 여러 양자적 경로가 기여할 수 있고, 각 경로의 확률 진폭은 서로 더해집니다.
86
이때 확률 진폭은 단순한 확률과 달리 양수와 음수, 나아가 복소수의 값을 가질 수 있습니다.
93
따라서 같은 결과에 기여하는 진폭들이 서로 강화되거나 상쇄될 수 있습니다.
97
그리고 어떤 결과가 실제로 관측될 확률은, 이렇게 합쳐진 진폭의 크기를 제곱해서 결정됩니다.
103
양자 알고리즘은 이 원리를 이용합니다.
105
양자 연산을 통해 상태들의 진폭과 상대적인 위상을 조절하고, 원하는 결과의 진폭은 커지도록, 다른 결과의 진폭은 작아지도록 만드는 것입니다.
115
결국 중요한 것은 수많은 상태를 동시에 표현하는 것만이 아닙니다.
119
그 상태들이 서로 어떻게 간섭하도록 만드는지가 정답을 찾을 확률을 결정합니다.
124
대표적인 예가 그로버 알고리즘입니다.
126
정렬되지 않은 N개의 항목에서 조건에 맞는 하나를 찾는다고 생각해 보겠습니다.
131
일반적인 방법은 최악의 경우 N개에 비례하는 횟수만큼 항목을 확인해야 합니다.
136
하지만 그로버 알고리즘은 양자 간섭을 이용해 약 √N에 비례하는 횟수의 조회만으로 정답을 찾을 수 있습니다.
143
예를 들어 항목이 100만 개라면, 일반적인 검색에는 최대 100만 번의 확인이 필요할 수 있지만, 양자 알고리즘은 약 1,000번 규모의 조회로 문제를 해결할 수 있습니다.
153
물론 실제 필요한 연산 수와 실행시간은 이보다 복잡합니다.
157
중요한 것은 양자컴퓨터가 단순히 모든 경우의 수를 동시에 확인하기 때문에 빠른 것이 아니라는 점입니다.
163
중첩된 상태를 어떻게 변환하고, 어떤 결과를 강화할 수 있는지가 속도 향상을 결정합니다.
169
그런데 여기서 새로운 의문이 생깁니다.
171
이러한 양자 간섭을 이용할 수 있다면, 양자컴퓨터는 모든 문제에서 기존 컴퓨터보다 빠를 수 있을까요?
178'''.splitlines()
BOUNDS=[0,8,16,25,41,48,63,71,80,93,103,105,115,124,131,143,157,169,178]
TITLES=['0과 1로 표현하는 정보','비트와 큐비트','확률 진폭으로 표현하는 중첩','큐비트가 늘어나면?','모든 답을 동시에 얻을까?','측정하면 하나의 결과','양자 간섭의 직관','강화와 상쇄','하나의 결과, 여러 기여','진폭을 먼저 더한다','확률은 진폭 크기의 제곱','양자 연산이 진폭을 바꾼다','간섭으로 정답 확률을 높인다','그로버 알고리즘','검색 방식의 차이','백만 개 중 하나를 찾는다면','속도 향상을 만드는 것','모든 문제에서 빠를까?']
sentences=[];start=0
for i in range(0,len(LINES),2):
    end=int(LINES[i+1]);sentences.append({'start':start,'end':end,'text':LINES[i]});start=end
scenes=[{'id':f'{i+1:02}','class':f'Shot{i+1:02}','start':a,'end':b,'title':TITLES[i]} for i,(a,b) in enumerate(zip(BOUNDS,BOUNDS[1:]))]
data={'title':'양자컴퓨터는 왜 빠를까?','duration':178,'timing_source':'사용자 제공 확정 대본 및 문장 종료 시각 (2026-11-07)','sentences':sentences,'scenes':scenes}
(HERE/'script.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(HERE/'timing.json').write_text(json.dumps({'fps':60,**data},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def wrap(s,n=32):
    out=[];line=''
    for w in s.split():
        if line and len(line)+len(w)+1>n:out.append(line);line=w
        else:line=(line+' '+w).strip()
    return '\n'.join(out+[line])
(HERE/'captions.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(s['start'])} --> {stamp(s['end'])}\n{wrap(s['text'])}" for i,s in enumerate(sentences))+'\n',encoding='utf-8')
(HERE/'narration.md').write_text('# 양자컴퓨터는 왜 빠를까?\n\n사용자 제공 확정 대본 · 총 178초\n\n'+'\n\n'.join(f"{s['start']}–{s['end']}초\n\n{s['text']}" for s in sentences)+'\n',encoding='utf-8')
tts=[]
for sentence in sentences:
    s=sentence['text']
    for a,b in [('1,024','천이십사'),('1,000','천'),('100만','백만'),('20개','스무 개'),('10개','열 개'),('√N','루트 엔'),('N개','엔 개'),('0과 1','영과 일'),('0 또는 1','영 또는 일')]:s=s.replace(a,b)
    tts.append(s)
(HERE/'tts_script.txt').write_text('\n\n'.join(tts)+'\n',encoding='utf-8')
for i,scene in enumerate(scenes):
    folder=HERE/'scenes'/scene['id'];folder.mkdir(parents=True,exist_ok=True)
    (folder/'scene.py').write_text('import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[4]))\nfrom longforms.qcs01_speed.direction import QCSScene\n\nclass '+scene['class']+'(QCSScene):\n    shot='+str(i)+'\n',encoding='utf-8')
    original='\n\n'.join(s['text'] for s in sentences if scene['start']<=s['start']<scene['end'])
    (folder/'script.txt').write_text(original+'\n',encoding='utf-8')
    (folder/'spec.md').write_text(f"# {scene['id']} · {scene['title']}\n\n## 목적과 주장\n\n{scene['title']}를 도형의 변화로 설명한다.\n\n## 확정 대본과 길이\n\n{scene['start']}–{scene['end']}초, {(scene['end']-scene['start'])*60}프레임. 사용자 제공 문장 종료 시각을 유지한다.\n\n{original}\n\n## 화면과 애니메이션\n\n첨부 콘티 SCENE {i+1:02}, direction.py의 s{i+1:02}. 쇼츠는 중앙·상하, 가로형은 별도 좌표·차트 축 간격 및 좌우 비교 배치. 하단은 내레이션 자막 전용이다.\n\n## 연결과 정확성\n\n앞 장면: {TITLES[i-1] if i else '없음'}. 종료 시 본문의 설명 결과를 유지한다. 다음 장면: {TITLES[i+1] if i<17 else '마지막 물리학적 질문으로 완결'}. 예고나 엔드카드를 추가하지 않는다.\n진폭·확률·그로버 연산의 조건은 brief.md와 verify.py를 따른다.\n",encoding='utf-8')
    scene['directory']='scenes/'+scene['id']
    scene['duration_seconds']=scene['end']-scene['start']
(HERE/'master_script.md').write_text((HERE/'narration.md').read_text(encoding='utf-8'),encoding='utf-8')
# JSON is valid YAML 1.2, keeping this manifest dependency-free.
(HERE/'scenes.yaml').write_text(json.dumps({'id':'qcs01','title':data['title'],
    'video':{'layouts':{'longform':[1920,1080],'shorts':[1080,1920]},'fps':60,'duration_seconds':178},
    'scenes':scenes},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert len(sentences)==34 and sentences[-1]['end']==178
assert all(s['start']==(sentences[i-1]['end'] if i else 0) for i,s in enumerate(sentences))
