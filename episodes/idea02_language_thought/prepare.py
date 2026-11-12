"""Approved narration and supplied sentence ends, not estimated timing."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
RAW='''우리는 인공지능이 수학 문제를 해결할 때, 그 과정을 언어로 설명하는 모습을 쉽게 볼 수 있습니다.
5
식을 정리하고, 공식을 적용하고, 단계별로 답을 찾아가는 것입니다.
10
그런데 여기서 한 가지 궁금증이 생겼습니다.
13
인공지능이 수학을 이해하는 과정에도 이러한 언어적 설명이 반드시 필요할까요?
18
예를 들어 '미분'이라는 개념을 생각해 보겠습니다.
20
우리는 미분을 순간변화율을 구하는 연산이라고 설명합니다.
24
하지만 미분에는 선형성이나 곱의 미분법, 연쇄 법칙과 같은 여러 수학적 성질도 존재합니다.
30
그렇다면 미분의 정의를 말로 설명할 수 있다는 사실만으로, 이러한 성질을 새로운 문제에서도 정확하게 활용할 수 있다고 말할 수 있을까요?
38
물론 인공지능은 관련된 수식과 예제도 함께 학습합니다.
41
하지만 어떤 개념을 언어로 정확하게 설명하는 것과, 그 개념에 포함된 관계를 새로운 문제에 활용하는 것은 서로 다른 능력일 수 있습니다.
50
실제로 일부 언어모델을 평가한 연구에서는, 풀이 구조를 유지한 채 문제의 숫자를 바꾸거나 풀이에 필요하지 않은 정보를 덧붙였을 때도 정답률이 달라지는 현상이 관찰되었습니다.
61
또 다른 연구에서는 세 자리 덧셈에 오답을 낸 경우에도, 별도로 학습한 분석기를 통해 모델의 내부 표현에서 정답에 관한 정보를 읽어낼 수 있었습니다.
70
이는 모델 내부에 형성된 정보와 최종적으로 출력되는 답이 반드시 일치하지는 않을 수 있음을 보여줍니다.
77
여기서 처음의 질문을 조금 바꿔볼 수 있습니다.
80
우리가 보는 언어적 설명은 인공지능이 실제로 계산하는 방식과 얼마나 일치할까요?
85
언어모델은 문장을 입력받고 다음 토큰을 예측하지만, 내부에서는 수많은 숫자로 이루어진 벡터 표현을 계산합니다.
91
우리가 읽는 문장이 내부의 모든 연산을 그대로 보여주는 것은 아닙니다.
96
다만 중간에 생성한 설명이 이후 풀이를 돕는 역할을 할 수도 있습니다.
101
그렇다면 언어가 추론에 도움이 되는가와, 모든 수학적 관계를 반드시 언어로 풀어 써야 하는가는 서로 다른 질문이 아닐까요?
108
예를 들어 여러 함수에 미분을 적용하면서, 함수를 더한 뒤 미분한 결과와 각각 미분한 뒤 더한 결과가 같다는 관계를 학습하게 할 수는 없을까요?
117
모델이 '선형성'이라는 이름을 먼저 배우지 않더라도, 반복되는 관계를 알아보고 새로운 함수에 적용하도록 하는 것입니다.
125
물론 이러한 방식이 기존 언어모델보다 더 우수할 것이라는 보장은 없습니다.
129
자연어 역시 복잡한 개념과 관계를 표현할 수 있는 강력한 도구이기 때문입니다.
134
하지만 여기서 구분해 볼 필요가 있는 것은, 수학적 관계를 처리하는 방식과 그 결과를 사람에게 전달하는 방식입니다.
141
어쩌면 우리가 인공지능에게 요구해 온 언어적 설명은, 수학적 이해를 확인하는 하나의 창일지도 모릅니다.
147
그렇다면 인공지능의 수학적 이해를 평가할 때, 설명의 정확성과 함께 무엇을 살펴봐야 할까요?
155
표현이 달라져도 같은 관계를 알아보고, 새로운 문제에 정확하게 활용할 수 있는지도 확인해야 하지 않을까요?
160'''.splitlines()
BOUNDS=[0,18,38,50,61,77,108,125,141,160]
TITLES=['설명하는 방식 = 계산하는 방식?', '미분을 설명하고, 활용한다는 것', '설명과 새로운 문제의 활용', '같은 풀이 구조, 달라지는 정답률', '내부 정보와 최종 출력 사이', '문장과 내부 계산은 어떻게 연결될까?', '이름보다 먼저 관계를 배운다면', '처리하는 방식과 전달하는 방식', '수학적 이해를 어떻게 확인할까?']
DETAILS=[
 '0–5 방정식과 언어 풀이,5–10 식 정리→규칙→결과,10–13 질문 전환,13–18 설명과 계산의 일치 여부를 물음표로. 등호를 사실로 단정하지 않는다.',
 '18–20 미분,20–24 곡선 위 점과 실제 도함수 기울기의 접선 이동.24–30 선형성·곱·연쇄 법칙.30–38 정의 설명→새 문제 적용은 자동 보장되지 않음. 정의가 수학적으로 불충분하다는 주장 금지.',
 '38–41 정의·공식·예제,41–50 학습 사례→새 문제 일반화. 설명과 활용을 별도 평가. 언어모델이 수식도 학습한다는 점 보존.',
 '50–61 GSM-Symbolic(2024): 숫자 변경·무관 정보 추가와 성능 변화. 임의 문장제는 개념 예시, 가짜 정답률/개별 정오 판정 없음. 출처 arXiv:2410.05229.',
 '61–70 세자리247+386과 내부 벡터,오답 출력 경로와 별도 학습 Probe 경로를 분리.70–77 내부 정보와 출력은 불일치 가능. 숫자와 벡터는 개념도이며 항상 복원·완성 정답 저장 주장 금지. EMNLP2025 Sun et al. 출처.',
 '77–85 언어 설명/벡터 계산 비교,85–91 단어 단위 개념 토큰→수치 블록→출력 후보,91–96 내부 전체 연산의 기록이 아님,96–101 중간 설명이 후속 문맥에 재입력,101–108 도움과 필수 여부의 질문을 구분. 토큰화와 값은 실제 측정이 아닌 개념도.',
 '108–117 합한 뒤 미분 vs 각각 미분 후 합의 두 경로를 동일 결과로 연결.117–125 세 함수 사례→공통 관계→새 함수 e^x+cos x. 충분히 미분 가능한 실수 함수, 관계 발견과 일반 증명 구분. IDEA/CONCEPT 표시.',
 '125–129 비교 우위 미보장,129–134 자연어도 강력한 표현,134–141 관계 처리↔사람 전달 양방향. 어느 쪽도 우월한 체크표시 금지.',
 '141–147 관계 그래프를 보는 창 비유,147–155 설명의 정확성+관계 일반화 두 평가,155–160 다른 표현의 같은 미분 관계와 마지막 질문. 예고·복습·별도 엔드카드 없음.'
]
sentences=[];start=0
for i in range(0,len(RAW),2):
 end=int(RAW[i+1]);sentences.append(dict(start=start,end=end,text=RAW[i]));start=end
scenes=[dict(id=f'{i+1:02}',**{'class':f'Shot{i+1:02}'},start=a,end=b,title=TITLES[i]) for i,(a,b) in enumerate(zip(BOUNDS,BOUNDS[1:]))]
data=dict(title='AI는 반드시 언어로 생각해야 할까?',revision='v1_160s',duration=160,timing_source='사용자 제공 문장 종료 시각',sentences=sentences,scenes=scenes)
for name,obj in [('script.json',data),('timing.json',dict(fps=60,**data))]:(HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def stamp(t):return f'00:{t//60:02}:{t%60:02},000'
def wrap(s,n=26):
 lines=[];line=''
 for w in s.split():
  if line and len(line)+len(w)+1>n:lines.append(line);line=w
  else:line=(line+' '+w).strip()
 return '\n'.join(lines+[line])
(HERE/'captions.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(s['start'])} --> {stamp(s['end'])}\n{wrap(s['text'])}" for i,s in enumerate(sentences))+'\n',encoding='utf-8')
(HERE/'narration.md').write_text('# AI는 반드시 언어로 생각해야 할까?\n\n사용자 확정 대본 · 160초\n\n'+'\n\n'.join(f"{s['start']}–{s['end']}초\n\n{s['text']}" for s in sentences)+'\n',encoding='utf-8')
(HERE/'tts_script.txt').write_text('\n\n'.join(s['text'] for s in sentences)+'\n',encoding='utf-8')
for i,s in enumerate(scenes):
 folder=HERE/'scenes'/s['id'];folder.mkdir(parents=True,exist_ok=True)
 (folder/'scene.py').write_text('import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parents[4]))\nfrom episodes.idea02_language_thought.direction import IdeaTwoScene\n\nclass '+s['class']+'(IdeaTwoScene):\n    shot='+str(i)+'\n',encoding='utf-8')
 (folder/'spec.md').write_text(f"# {s['title']}\n\n{s['start']}–{s['end']}秒 · {(s['end']-s['start'])*60}프레임\n\n{DETAILS[i]}\n\n확정 대본·자막 경계:script.json. 무음. 하단 자막 안전영역 분리.\n".replace('秒','초'),encoding='utf-8')
(HERE/'brief.md').write_text('# 제작 기준\n\n27문장 확정 대본과 사용자 종료시각, 총160초·9600프레임. 콘티의 약180초 배치는 사용하지 않고 문장 시각에 맞춘다.9:16,1080×1920,60fps. 무음·전체 내레이션 자막.1편과 qcs 공통 타이밍·자막·검사 도구 재사용.\n\n실제 연구는 GSM-Symbolic https://arxiv.org/abs/2410.05229 와 Probing for Arithmetic Errors https://aclanthology.org/2025.emnlp-main.411/ 이며 이전 대본 검토에서 확인한 결과를 재사용. 새 연구조사 없음. 수치 예시는 실제 실험 데이터가 아닌 개념도,프로브는 별도 학습한 분석기. 정답 저장·항상 복원 주장 없음.\n\n미분 법칙은 충분히 미분 가능한 실수 함수에 적용. 선형성은 상수배와 덧셈,핵심 경로는 덧셈 보존. 합성법칙의 평가점 명시. 관계학습은108초부터 IDEA/CONCEPT로 분리,사례가 일반 증명이라는 주장 없음. 벡터와 단어 토큰은 개념도. 자연어 도움과 필수성을 구분.\n\n배경#0B1020,언어#60A5FA,벡터#A78BFA,관계#2DD4BF,불일치#F59E0B. 별도 엔드카드·예고·복습 없음.\n',encoding='utf-8')
assert len(sentences)==27 and sentences[-1]['end']==160
