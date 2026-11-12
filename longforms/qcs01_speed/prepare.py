"""Reproduce approved script assets; times below are supplied by the user."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
LINES='''일반적인 컴퓨터는 0과 1로 정보를 표현합니다.
3
양자컴퓨터 역시 0과 1을 이용하지만, 정보를 표현하는 방식에는 중요한 차이가 있습니다.
9
일반적인 비트는 0 또는 1의 상태를 갖지만, 양자컴퓨터의 큐비트는 두 상태가 중첩된 상태로 존재할 수 있습니다.
16
이를 수학적으로 표현하면, 0과 1에 각각 확률 진폭을 부여한 형태가 됩니다.
21
여러 큐비트를 결합하면, 중첩할 수 있는 계산 기저 상태의 수는 지수적으로 증가합니다.
26
큐비트가 하나라면 두 개, 두 개라면 네 개, 세 개라면 여덟 개입니다.
31
20개의 큐비트는 약 100만 개의 계산 기저 상태에 대한 진폭을 하나의 양자 상태로 표현할 수 있습니다.
37
그렇다면 양자컴퓨터는 이 모든 경우의 수를 동시에 계산하기 때문에 빠른 것일까요?
42
정확히는 그렇지 않습니다.
44
수많은 상태를 중첩하더라도, 측정하면 일반적으로 그중 하나의 결과만 얻을 수 있습니다.
49
따라서 중첩만으로 원하는 정답을 찾아낼 수는 없습니다.
52
여기서 중요한 것이 양자 간섭입니다.
55
파동은 마루와 마루가 겹치면 강화되고, 마루와 골이 겹치면 상쇄됩니다.
59
양자컴퓨터에서도 하나의 결과에 기여하는 여러 경로의 확률 진폭이 서로 더해질 수 있습니다.
65
확률 진폭은 양수와 음수, 나아가 복소수의 값을 가질 수 있어 서로 강화되거나 상쇄될 수 있습니다.
72
그리고 합쳐진 진폭의 크기를 제곱하면, 그 결과가 관측될 확률이 됩니다.
77
양자 알고리즘은 이 원리를 이용합니다.
79
대표적인 예가 그로버 알고리즘입니다.
82
정렬되지 않은 수많은 항목 중 하나의 정답을 찾는다고 생각해 보겠습니다.
86
일반적인 컴퓨터는 항목을 하나씩 확인해야 하지만, 양자컴퓨터는 여러 후보가 중첩된 상태에 연산을 적용할 수 있습니다.
93
먼저 양자컴퓨터는 정답을 판별하는 연산을 이용해, 정답에 해당하는 진폭의 부호만 뒤집습니다.
99
이때는 아직 정답을 측정할 확률이 높아지지 않습니다.
102
하지만 이어서 진폭들을 평균을 기준으로 반사시키는 연산을 적용하면, 정답의 진폭은 커지고 다른 후보의 진폭은 작아집니다.
109
예를 들어 네 개의 후보가 있다면, 처음에는 각각 25퍼센트의 확률로 관측됩니다.
114
하지만 정답의 진폭에 음수 부호를 붙이고, 평균을 기준으로 반사시키면 정답의 확률은 100퍼센트가 됩니다.
121
단 한 번의 반복으로 정답을 찾아낼 수 있는 것입니다.
124
이 두 연산을 반복하면 정답을 측정할 확률을 점차 높일 수 있습니다.
129
즉, 정답이 무엇인지 미리 알아내는 것이 아니라, 정답을 구별할 수 있는 규칙을 이용해 정답의 확률을 높이는 것입니다.
136
그 결과 모든 항목을 하나씩 확인하지 않고도 높은 확률로 정답을 찾을 수 있습니다.
141
일반적인 검색에는 최악의 경우 N개에 비례하는 조회가 필요하지만, 그로버 알고리즘은 약 루트 N에 비례하는 조회만으로 정답을 찾을 수 있습니다.
151
예를 들어 항목이 100만 개라면, 일반적인 검색은 최대 100만 번의 확인이 필요하지만, 양자 알고리즘은 약 1,000번 규모의 조회로 해결할 수 있습니다.
160
물론 실제 연산 수와 실행시간은 이보다 복잡합니다.
163
결국 양자컴퓨터가 빠를 수 있는 이유는 단순히 많은 상태를 중첩하기 때문이 아닙니다.
168
중첩된 상태에 연산을 적용하고, 간섭을 이용해 정답을 찾는 데 필요한 조회 횟수를 줄일 수 있기 때문입니다.
175'''.splitlines()
BOUNDS=[0,9,16,21,31,37,44,52,59,65,77,86,91,93,102,109,124,141,160,168,175]
TITLES=['0과 1로 표현하는 정보','비트와 큐비트','확률 진폭으로 표현하는 중첩','큐비트가 늘어나면?','20큐비트와 백만 개의 기저 상태','동시에 계산하면 빠를까?','측정하면 하나의 결과','파동의 강화와 상쇄','하나의 결과, 여러 기여','진폭과 확률의 차이','그로버: 네 후보 중 정답 찾기','중첩된 후보 전체에 연산하기','초기 진폭과 관측 확률','오라클: 정답의 부호만 반전','확산: 평균을 기준으로 반사','25%에서 100%로','정답을 구별하는 규칙','검색 횟수의 차이','중첩만으로 빠른 것은 아니다','간섭으로 조회 횟수를 줄인다']
sentences=[];start=0
for i in range(0,len(LINES),2):
    end=int(LINES[i+1]);sentences.append({'start':start,'end':end,'text':LINES[i]});start=end
scenes=[{'id':f'{i+1:02}','class':f'Shot{i+1:02}','start':a,'end':b,'title':TITLES[i]} for i,(a,b) in enumerate(zip(BOUNDS,BOUNDS[1:]))]
data={'title':'양자컴퓨터는 왜 빠를까?','duration':175,'revision':'v2_175s','timing_source':'사용자 제공 수정 확정 대본 및 문장 종료 시각 (2026-11-07)','sentences':sentences,'scenes':scenes}
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
(HERE/'narration.md').write_text('# 양자컴퓨터는 왜 빠를까?\n\n사용자 제공 수정 확정 대본 · 총 175초\n\n'+'\n\n'.join(f"{s['start']}–{s['end']}초\n\n{s['text']}" for s in sentences)+'\n',encoding='utf-8')
tts=[]
for sentence in sentences:
    s=sentence['text']
    for a,b in [('1,024','천이십사'),('1,000','천'),('100만','백만'),('20개','스무 개'),('10개','열 개'),('√N','루트 엔'),('루트 N','루트 엔'),('N개','엔 개'),('25퍼센트','이십오 퍼센트'),('100퍼센트','백 퍼센트'),('0과 1','영과 일'),('0 또는 1','영 또는 일')]:s=s.replace(a,b)
    tts.append(s)
(HERE/'tts_script.txt').write_text('\n\n'.join(tts)+'\n',encoding='utf-8')
for i,scene in enumerate(scenes):
    folder=HERE/'scenes'/scene['id'];folder.mkdir(parents=True,exist_ok=True)
    (folder/'scene.py').write_text('import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[4]))\nfrom longforms.qcs01_speed.direction import QCSScene\n\nclass '+scene['class']+'(QCSScene):\n    shot='+str(i)+'\n',encoding='utf-8')
    original='\n\n'.join(s['text'] for s in sentences if s['end']>scene['start'] and s['start']<scene['end'])
    (folder/'script.txt').write_text(original+'\n',encoding='utf-8')
    (folder/'spec.md').write_text(f"# {scene['id']} · {scene['title']}\n\n## 목적과 주장\n\n{scene['title']}를 도형의 변화로 설명한다.\n\n## 확정 대본과 길이\n\n{scene['start']}–{scene['end']}초, {(scene['end']-scene['start'])*60}프레임. 사용자 제공 문장 종료 시각을 유지한다.\n\n{original}\n\n## 화면과 애니메이션\n\n첨부 콘티 SCENE {i+1:02}, direction.py의 s{i+1:02}. 쇼츠는 중앙·상하, 가로형은 별도 좌표·차트 축 간격 및 좌우 비교 배치. 하단은 내레이션 자막 전용이다.\n\n## 연결과 정확성\n\n앞 장면: {TITLES[i-1] if i else '없음'}. 종료 시 본문의 설명 결과를 유지한다. 다음 장면: {TITLES[i+1] if i<len(TITLES)-1 else '조회 횟수 감소라는 결론으로 완결'}. 예고나 엔드카드를 추가하지 않는다.\n진폭·확률·그로버 연산의 조건은 brief.md와 verify.py를 따른다.\n",encoding='utf-8')
    scene['directory']='scenes/'+scene['id']
    scene['duration_seconds']=scene['end']-scene['start']
    details={
      '13':'시작·종료 진폭은 [0.5,0.5,0.5,0.5]. 네 막대 아래의 관측 확률은 각각 25%. 91–93초는 86–93초 문장 내부의 화면 변화이며 자막은 문장 전체 시각을 유지한다.',
      '14':'93–94.5초 초기 상태 유지. 94.5초 이후 마지막 진폭을 0.5 exp(iφ)로 회전시켜 부호를 반전한다. 막대는 실수부임을 명시한다. 99초에 부호 반전과 확률 증가가 다름을 강조한다. 종료 상태 [0.5,0.5,0.5,-0.5], 관측 확률은 각 25%.',
      '15':'시작 [0.5,0.5,0.5,-0.5]. 평균 0.25 점선을 표시하고 aᵢ′=2ā-aᵢ를 도입한다. 104.5–105.9초 끝점들이 평균선 반대편의 같은 거리로 이동하는 작도를 보여준다. 이 점 이동은 중간 계산 상태가 아님을 명시한다. 실제 상태 막대는 연산 결과 [0,0,0,1]로 갱신한다.',
      '16':'109–114초 각 25%의 초기 관측 확률. 114초에 실수부 진폭으로 전환하고 오라클→확산을 재현한다. 119초에 관측 확률 표시로 전환한다. 121초에 반복 한 번이 오라클 1회+확산 1회임을 표시한다. 종료는 정답 확률 100%.',
      '17':'4개 후보 예를 무한 반복하지 않는다. N=64의 실제 그로버 반복 1–6회를 시연한다. 129초 이후 오라클 판별 규칙이 위상을 바꾸는 블랙박스를 표시한다. 내부에 정답 위치를 표시하지 않는다. 과도한 반복은 확률을 낮출 수 있음을 표시한다.',
      '20':'168–170초 동일한 네 진폭으로 오라클→확산 결과를 재현한다. 이후 도형을 축소하고 더 적은 조회라는 결론을 강조한다. standalone의 마지막 0.5초에는 본문 도형만 페이드하며 내레이션 자막과 175초 전체 길이는 보존한다. join은 동일한 본문을 유지한다.'}
    if scene['id'] in details:
        with (folder/'spec.md').open('a',encoding='utf-8') as out:out.write('\n## 상세 타이밍·시작과 종료 상태\n\n'+details[scene['id']]+'\n')
(HERE/'master_script.md').write_text((HERE/'narration.md').read_text(encoding='utf-8'),encoding='utf-8')
# JSON is valid YAML 1.2, keeping this manifest dependency-free.
(HERE/'scenes.yaml').write_text(json.dumps({'id':'qcs01','title':data['title'],
    'video':{'layouts':{'longform':[1920,1080],'shorts':[1080,1920]},'fps':60,'duration_seconds':175},
    'scenes':scenes},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert len(sentences)==34 and sentences[-1]['end']==175
assert all(s['start']==(sentences[i-1]['end'] if i else 0) for i,s in enumerate(sentences))
