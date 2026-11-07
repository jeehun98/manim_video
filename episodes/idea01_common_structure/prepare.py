"""Preserve the supplied narration and actual sentence boundaries."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
RAW='''우리는 수학적 성질을 설명할 때 수많은 수식과 기호를 사용합니다.
4
그런데 서로 다른 수식들이 실제로는 동일한 구조를 표현하고 있다면 어떨까요?
8
그리고 그 구조를 나타내는 데 필요한 최소한의 표현이 존재한다면 어떨까요?
13
예를 들어, x제곱 빼기 6x 더하기 8이라는 식을 생각해 보겠습니다.
18
이 식을 인수분해하면 x 빼기 2와 x 빼기 4의 곱으로 나타낼 수 있습니다.
23
이제 두 근이 2와 4라는 사실을 쉽게 확인할 수 있습니다.
26
이번에는 완전제곱식으로 바꿔보겠습니다.
29
x 빼기 3의 제곱에서 1을 뺀 형태에서는 최솟값과 대칭축이 드러납니다.
33
세 수식은 모두 동일한 함수를 나타냅니다.
36
새로운 정보를 추가한 것도 아니지만, 표현을 바꾸자 서로 다른 성질이 드러난 것입니다.
41
그렇다면 이 세 표현을 각각 독립적으로 다루는 대신, 공통된 하나의 수학적 구조로 연결할 수 있지 않을까요?
48
그리고 그 구조에서 필요한 성질에 따라 적절한 표현을 만들어낼 수는 없을까요?
53
이러한 생각은 더 복잡한 수학으로도 이어집니다.
56
예를 들어 푸리에 변환은 시간에 따라 변하는 신호를 주파수의 관점에서 표현합니다.
61
이때 시간 영역의 미분 연산은 주파수 영역에서 곱셈으로 바뀌기도 합니다.
65
같은 대상을 다루고 있지만, 표현 공간에 따라 연산의 모습과 문제를 해결하는 방식이 달라지는 것입니다.
71
그렇다면 우리가 사용하는 수식은 수학적 대상 그 자체라기보다, 특정한 성질을 드러내기 위한 표현 중 하나일 수도 있습니다.
79
여기서 한 가지 궁금증이 생깁니다.
82
서로 다른 표현들에서 변하지 않는 관계만을 추출한다면, 그 관계들을 더 작은 공통 구조로 나타낼 수 있을까요?
88
나아가 서로 다른 수학적 대상에서도 반복되는 관계를 발견한다면 어떨까요?
93
그 관계에 붙여진 이름이나 공식을 미리 알지 못하더라도, 공통된 패턴을 인식하고 새로운 문제에 적용할 가능성이 있을 것입니다.
101
이러한 관점은 인공지능의 수학적 추론 방식에도 적용해 볼 수 있습니다.
105
수식을 단순히 기호의 나열로 학습하는 것이 아니라, 여러 표현 사이의 관계와 그 안에서 유지되는 성질을 학습하는 것입니다.
112
물론 모든 수학적 대상을 하나의 최소 표현으로 나타낼 수 있다는 뜻은 아닙니다.
117
어떤 성질을 보존하려는지에 따라 필요한 표현도 달라질 수 있습니다.
121
결국 처음의 질문으로 돌아오게 됩니다.
124
수학적 대상을 이해하는 데 필요한 것은 수많은 수식 자체일까요?
128
아니면 그 수식들이 공유하는 구조와 관계일까요?
131
만약 후자를 직접 표현하고 학습할 수 있다면, 수학을 다루는 새로운 방식도 생각해 볼 수 있지 않을까요?
136'''.splitlines()
BOUNDS=[0,13,41,53,79,101,121,136]
TITLES=['다른 수식, 같은 구조?', '같은 함수에서 드러나는 다른 성질', '질문에 따라 표현을 선택한다면', '표현이 바뀌면 연산도 달라진다', '이름보다 먼저, 반복되는 관계', '관계를 학습하는 AI를 상상한다면', '수식 너머의 공통 구조']
DETAILS=[
 '0–4 수식 격자, 4–8 교환 관계, 8–13 관계 그래프와 최소 표현 물음표. 실수 덧셈 예시.',
 '13–18 일반형과 고정 포물선, 18–26 인수분해와 근2·4,26–33 완전제곱과 대칭축3·최솟값-1,33–41 세 표현을 같은 그래프로 연결. 그래프 재생성 금지.',
 '41–48 같은 함수 f에 세 표현 연결,48–53 근/최솟값에 따라 표현 점등. 최소 표현의 증명이 아닌 개념도.',
 '53–61 사인파 합성,61–65 시간/주파수 및 미분/곱셈,65–71 대응 강조,71–79 동일 신호의 두 관찰 창. 양의 주파수 진폭은 개념도. 주기 신호의 항등식은 푸리에 급수/분포의 의미. 지수항 exp(-iωt), 적절한 조건.',
 '79–82 유지되는 관계 질문,82–88 동일 함수의 연결 추출,88–93 수·스칼라·행렬의 분배 패턴,93–101 일반 규칙으로 추출하고 새로운 식에 적용한 뒤 분배법칙 이름. 행렬은 크기가 맞아야 하며 교환법칙을 암시하지 않는다.',
 '101–105 구조 입력,105–112 기호 나열→관계 그래프,112–117 과한 압축에서 관계 소실 후 복구,117–121 보존 목적에 따른 두 표현. 실제 AI 내부 설명이 아닌 사고 실험.',
 '121–128 세 수식 복귀,128–131 연결선 강조,131–136 확장하는 관계 그래프와 열린 질문. 별도 엔드카드·예고 없음.'
]
sentences=[];start=0
for i in range(0,len(RAW),2):
 end=int(RAW[i+1]);sentences.append(dict(start=start,end=end,text=RAW[i]));start=end
scenes=[dict(id=f'{i+1:02}',**{'class':f'Shot{i+1:02}'},start=a,end=b,title=TITLES[i]) for i,(a,b) in enumerate(zip(BOUNDS,BOUNDS[1:]))]
data=dict(title='수식에 숨겨진 공통 구조를 찾는다면?',revision='v1_136s',duration=136,timing_source='사용자 제공 문장 종료 시각',sentences=sentences,scenes=scenes)
for name,obj in [('script.json',data),('timing.json',dict(fps=60,**data))]:
 (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def wrap(s,n=26):
 lines=[];line=''
 for w in s.split():
  if line and len(line)+len(w)+1>n:lines.append(line);line=w
  else:line=(line+' '+w).strip()
 return '\n'.join(lines+[line])
(HERE/'captions.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(s['start'])} --> {stamp(s['end'])}\n{wrap(s['text'])}" for i,s in enumerate(sentences))+'\n',encoding='utf-8')
(HERE/'narration.md').write_text('# 수식에 숨겨진 공통 구조를 찾는다면?\n\n사용자 제공 확정 대본 · 136초\n\n'+'\n\n'.join(f"{s['start']}–{s['end']}초\n\n{s['text']}" for s in sentences)+'\n',encoding='utf-8')
tts=[]
for s in sentences:
 t=s['text']
 for a,b in [('x제곱','엑스 제곱'),('6x','육 엑스'),('x 빼기','엑스 빼기'),('8이라는','팔이라는'),('2와 4','이와 사'),('2와','이와'),('4의','사의'),('3의','삼의'),('1을','일을')]:t=t.replace(a,b)
 tts.append(t)
(HERE/'tts_script.txt').write_text('\n\n'.join(tts)+'\n',encoding='utf-8')
for i,s in enumerate(scenes):
 folder=HERE/'scenes'/s['id'];folder.mkdir(parents=True,exist_ok=True)
 (folder/'scene.py').write_text('import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[4]))\nfrom episodes.idea01_common_structure.direction import IdeaScene\n\nclass '+s['class']+'(IdeaScene):\n    shot='+str(i)+'\n',encoding='utf-8')
 (folder/'spec.md').write_text(f"# {s['title']}\n\n{s['start']}–{s['end']}초 · {(s['end']-s['start'])*60}프레임\n\n{DETAILS[i]}\n\n대본과 문장별 자막 경계는 script.json 참조. 무음. 하단 자막 영역을 분리한다.\n",encoding='utf-8')
(HERE/'brief.md').write_text('# 제작 기준\n\n사용자 제공 콘티·확정 대본과 29개 문장 종료 시각을 보존. 총136초,9:16,1080×1920,60fps. 음원 미제공으로 무음·전체 내레이션 자막. 최근 qcs 시리즈의 독립 씬, 공통 자막/타이밍, 소스 해시 및 프레임 검사를 재사용. 요청한 세로 영상만 렌더.\n\n같은 함수의 재표현과 서로 다른 대상의 공통 분배 패턴을 구별. 최소 표현은 질문이지 보편적 존재 주장이 아니다. AI는 사고 실험으로 명시. 푸리에 미분 대응은 e^{-iωt} 관례와 적절한 조건 아래 성립하며 주기 신호는 급수/분포로 해석. 양의 주파수 진폭 개념도는 전체 복소 스펙트럼이 아니다.\n\n배경#0B1020,수식#E5E7EB,대상#60A5FA,관계#2DD4BF,관찰#F59E0B. 포물선은 같은 씬 안에서 고정. 별도 엔드카드/복습/예고 없음.\n',encoding='utf-8')
assert len(sentences)==29 and sentences[-1]['end']==136
