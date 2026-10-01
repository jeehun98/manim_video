"""Entropy viewed through binary distinction trees; estimated speech timing."""
import math
PROBABILITIES=(.5,.25,.125,.125)
DEPTHS=(1,2,3,3)
CODES=('0','10','110','111')
ENTROPY=-sum(p*math.log2(p) for p in PROBABILITIES)
AVERAGE_DEPTH=sum(p*d for p,d in zip(PROBABILITIES,DEPTHS))
TEXT=[
'여덟 세계 중, 실제는 하나입니다. 몇 번 물어야 찾을까요?',
'예, 아니오로 후보를 절반씩 나눕니다. 여덟에서 넷, 둘, 하나.',
'최적으로 나누면 세 번. 3 bits는 세 번의 구분 깊이입니다.',
'로그를 다시 읽어봅시다. 가능성을 반으로 줄이는 횟수를 셉니다.',
'그런데 네 결과의 확률이 서로 다르다면, 질문도 바꿔야 할까요?',
'모두 같은 깊이에 놓으면 두 번씩 묻습니다. 가장 흔한 A도 두 번입니다.',
'대신 A인지 먼저 묻습니다. A는 한 번, B는 두 번, C와 D는 세 번에 찾습니다.',
'이제 평균 질문 수는 1.75번. 결과는 그대로인데, 질문의 구조가 달라졌습니다.',
'각 경로의 깊이는 마이너스 로그 확률과 같습니다. 이 예시의 평균 깊이가 엔트로피입니다.',
'다만 항상 같지는 않습니다. 일반 분포에서 엔트로피는 평균 질문 수의 하한입니다.',
'엔트로피를 현실 하나를 특정하는 데 필요한, 평균 구분의 한계로 읽어보세요.',
'이 경로를 0과 1로 적으면 코드가 됩니다. 구분의 깊이가 저장 공간으로 이어집니다.',
]
REPLACEMENTS=[('1.75','일 점 칠 오'),('3 bits','삼 비트'),('A','에이'),('B','비'),('C','씨'),('D','디'),('0','영'),('1','일')]
SPOKEN=[]
for text in TEXT:
    for old,new in REPLACEMENTS:text=text.replace(old,new)
    SPOKEN.append(text)
CUES=[]
frames=0
for i,(display,spoken) in enumerate(zip(TEXT,SPOKEN)):
    seconds=max(2.6,len(''.join(spoken.split()))/7.0+.18*(spoken.count('.')+spoken.count('?')))+(.5 if i==len(TEXT)-1 else 0)
    n=round(seconds*30);CUES.append((frames/30,(frames+n)/30,display,spoken));frames+=n
DURATION=frames/30
