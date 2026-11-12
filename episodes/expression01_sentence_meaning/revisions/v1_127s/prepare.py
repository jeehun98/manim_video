"""Use the user's approved words and actual sentence endpoints."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
RAW='''누군가 여러분에게 이렇게 말한다고 생각해 보겠습니다.
3
"그거 거기 놓아줘."
4
이 문장만 읽으면 무엇을 어디에 놓으라는 것인지 알기 어렵습니다.
8
하지만 같은 방에 있는 사람이 책을 가리키고, 책상 위를 손짓한다면 어떨까요?
13
우리는 별다른 설명 없이도 그 말을 이해할 수 있습니다.
16
그런데 여기서 한 가지 의문이 생깁니다.
19
책이라는 물건도, 책상이라는 장소도 문장에는 등장하지 않았습니다.
24
그렇다면 우리는 문장에 없는 정보를 어디에서 가져온 걸까요?
27
우리가 말을 이해할 때 사용하는 정보는 문장 안에만 존재하지 않습니다.
31
상대방의 손짓과 시선, 주변의 상황, 그리고 이전에 공유했던 경험까지 해석에 영향을 줍니다.
37
이번에는 조금 다른 상황을 생각해 보겠습니다.
40
친구가 여러분에게 이렇게 말합니다.
42
"우리 지난번에 갔던 곳으로 가자."
44
이 문장에는 구체적인 장소의 이름이나 주소가 없습니다.
48
하지만 두 사람이 함께 방문했던 장소가 하나뿐이라면, 어디를 말하는지 쉽게 알아들을 수 있겠죠.
53
반대로 함께 방문한 장소가 여러 곳이라면 추가적인 설명이 필요할 수도 있습니다.
58
같은 문장이라도 이미 공유하고 있는 정보에 따라 이해하기 쉬울 수도, 어려울 수도 있는 것입니다.
64
이처럼 언어는 모든 정보를 문장 안에 직접 기록하지 않아도 작동합니다.
69
단어와 문장 구조는 해석의 단서를 제공하고, 우리는 문장 밖의 정보를 이용해 그 의미를 구체화합니다.
74
이것은 일종의 정보 압축과도 비슷합니다.
77
매번 모든 상황을 처음부터 설명하는 대신, 서로 알고 있는 정보를 활용해 짧은 표현으로 의사소통하는 것입니다.
83
물론 이것이 문장 자체에는 의미가 없다는 뜻은 아닙니다.
87
"놓아줘"라는 말에는 어떤 행동을 요청한다는 의미가 있고, "거기"라는 말은 특정한 장소를 가리킨다는 사실도 공유하고 있습니다.
94
다만 그 장소가 정확히 어디인지는 문장만으로 정해지지 않을 수 있습니다.
99
결국 문장을 이해한다는 것은 적혀 있는 단어를 읽는 것만이 아니라, 그 표현이 사용된 상황과 연결하는 과정이기도 합니다.
106
우리가 일상에서 사용하는 짧은 문장 뒤에는 생각보다 많은 지식과 경험이 작동하고 있는 셈입니다.
112
문장은 유한하지만, 그 문장을 해석하는 데에는 문장 밖의 세계도 참여합니다.
117
그렇다면 여기서 또 다른 질문이 생깁니다.
119
같은 문장을 읽더라도, 각자가 가지고 있는 경험과 지식이 다르다면 어떨까요?
124
우리는 정말 같은 의미를 이해하고 있는 걸까요?
127'''.splitlines()
BOUNDS=[0,8,16,27,37,48,64,83,99,117,127]
TITLES=['문장 하나만 주어진다면', '같은 문장에 상황을 더하면', '문장에 없던 정보는 어디에서?', '해석에는 여러 정보가 참여한다', '우리 지난번에 갔던 곳으로 가자', '같은 문장, 다른 공유 경험', '짧은 표현과 공유된 정보', '문장 자체에도 의미가 있다', '문장 밖의 세계도 참여한다', '우리는 같은 의미를 이해할까?']
DETAILS=[
'0–3 말풍선 도입,3–4 원문 문장 표시,4–8 그거/거기의 미확정 대상과 장소. 주황색은 미확정, 파란색은 문장. 문장과 상황을 구별.',
'8–13 문장 그대로 유지,책·책상과 손짓 화살표 추가.13–16 책을 책상 위로 옮겨 그거=책,거기=책상 해석. 문장 단어를 책/책상으로 치환하지 않는다.',
'16–19 질문,19–24 책/책상이 문장에 없다는 사실 강조,24–27 문장과 외부 상황이라는 별도 입력을 해석에 연결. 외부 정보가 문장 내부에 저장되는 연출 금지.',
'27–31 문장 입력,31–37 손짓·시선·상황·공유 경험을 별도 초록 노드로 해석에 결합. 실제 뇌 모델이 아닌 개념도.',
'37–42 친구 인물 둘,42–44 동일한 장소 문장,44–48 구체 장소명·주소 없음을 빈칸과 후보 카페·식당·공원으로 표시.',
'48–53 공유 장소1개,53–58 공유 장소여러개,58–64 비교.각 화면비에 독립 배치. 여러 후보는 문장과 추가 정보만으로 특정하기 어렵다는 예시이며 시간·현저성 등 다른 단서 가능성을 부정하지 않는다.',
'64–74 짧은 표현+상황/지식→구체적 해석,74–83 긴 상황설명→짧은 문장과 공유정보가 함께 남는다. 정보 압축은 비유이며 완전 가역복원 주장 금지.',
'83–87 원문 복귀,87–94 그거 대상지시/거기 장소지시/놓아줘 행동요청 분리,94–99 장소역할과 구체장소를 구분. 규약적 의미가 없다는 결론 금지.',
'99–106 문장과 상황 연결,106–112 책·책상·카페·공유지식 회수,112–117 작은 문장 뒤 큰 관계망. 삶의 모든 기억을 항상 쓰거나 실제 내부를 측정했다는 주장 없음.',
'117–119 문장,119–124 동일문장이 서로 다른 경험망 두개와 연결,124–127 질문으로 종료. 개인차를 깊이 설명하지 않으며 다음편 예고·별도 엔드카드 없음.'
]
sentences=[];start=0
for i in range(0,len(RAW),2):
 end=int(RAW[i+1]);sentences.append(dict(start=start,end=end,text=RAW[i]));start=end
scenes=[dict(id=f'{i+1:02}',**{'class':f'Shot{i+1:02}'},start=a,end=b,title=TITLES[i]) for i,(a,b) in enumerate(zip(BOUNDS,BOUNDS[1:]))]
data=dict(title='문장 안에는 의미가 얼마나 들어 있을까?',revision='v1_127s',duration=127,timing_source='사용자 제공 문장 종료 시각',sentences=sentences,scenes=scenes)
for name,obj in [('script.json',data),('timing.json',dict(fps=60,**data))]:(HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def wrap(s,n=26):
 lines=[];line=''
 for w in s.split():
  if line and len(line)+len(w)+1>n:lines.append(line);line=w
  else:line=(line+' '+w).strip()
 return '\n'.join(lines+[line])
(HERE/'captions.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(s['start'])} --> {stamp(s['end'])}\n{wrap(s['text'])}" for i,s in enumerate(sentences))+'\n',encoding='utf-8')
(HERE/'narration.md').write_text('# 문장 안에는 의미가 얼마나 들어 있을까?'+'\n\n사용자 확정 대본 · 127초\n\n'+'\n\n'.join(f"{s['start']}–{s['end']}초\n\n{s['text']}" for s in sentences)+'\n',encoding='utf-8')
(HERE/'tts_script.txt').write_text('\n\n'.join(s['text'] for s in sentences)+'\n',encoding='utf-8')
for i,s in enumerate(scenes):
 folder=HERE/'scenes'/s['id'];folder.mkdir(parents=True,exist_ok=True)
 (folder/'scene.py').write_text('import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[4]))\nfrom episodes.expression01_sentence_meaning.direction import ExpressionScene\n\nclass '+s['class']+'(ExpressionScene):\n    shot='+str(i)+'\n',encoding='utf-8')
 (folder/'spec.md').write_text(f"# {s['title']}\n\n{s['start']}–{s['end']}초 · {(s['end']-s['start'])*60}프레임\n\n{DETAILS[i]}\n\n쇼츠와 가로는 같은 애니메이션 로직,화면비별 독립 위치/폭/배치 사용. 확정대본과 자막경계는 script.json. 무음.\n",encoding='utf-8')
(HERE/'brief.md').write_text('# 제작 기준\n\n확정30문장,127초·7620프레임,60fps. 첨부 콘티의 예상155초/장면시각보다 사용자 실제 문장끝 시각을 우선. 세로1080×1920와 가로1920×1080을 같은 로직과 별도 레이아웃으로 제작. 무음·전체 내레이션 자막. 기존 qcs의 타이밍/자막/렌더검사 재사용.\n\n문장은 단서와 관습적 의미를 제공하며,지시대상 구체화에 문맥·공유지식이 참여한다. 동일한 문장 유지,정보압축은 비유로 한정,완전복원과 언어 무의미 주장 없음. 개인차는 끝의 질문만 제시. 복습·예고·별도 엔드카드 없음.\n\n배경#0B1020,문장#60A5FA,문맥#34D399,미확정#FBBF24. 책·책상·장소는 코드 벡터도형,한글 Malgun Gothic. 세로 하단과 가로 하단 자막영역 분리.\n',encoding='utf-8')
assert len(sentences)==30 and sentences[-1]['end']==127
