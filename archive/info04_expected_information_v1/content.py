"""Expected future self-information: narration and frame-aligned estimated cues."""
import math
PROBABILITIES=(.5,.25,.25)
INFORMATION=tuple(-math.log2(p) for p in PROBABILITIES)
ENTROPY=sum(p*i for p,i in zip(PROBABILITIES,INFORMATION))
def entropy(probabilities):
    return -sum(p*math.log2(p) for p in probabilities if p>0)
TEXT=[
'결과를 보기 전에도, 정보량을 말할 수 있을까요?',
'A의 확률은 0.5, B와 C는 각각 0.25. 아직 결과는 모릅니다.',
'A를 보면 1 bit, B나 C를 보면 2 bits를 얻습니다.',
'최대인 2도, 가장 흔한 1도 충분하지 않습니다. 실제로 받을 값은 결과에 달렸습니다.',
'앞으로 얻을 정보량도 확률변수입니다. 이번에는 1 아니면 2입니다.',
'같은 분포에서 독립적으로 반복 관측하면, 어떤 때는 1, 어떤 때는 2를 얻습니다.',
'평균을 내려면, 각 정보량에 그 결과의 확률을 곱합니다.',
'계산하면 1.5 bits. 한 번에 1.5를 받는다는 뜻이 아니라, 받을 정보량의 기대값입니다.',
'이 기대값이 엔트로피입니다. 결과를 보기 전에 계산하는, 평균 자기정보량이죠.',
'결과가 확실하면 엔트로피는 0. 네 결과가 균등하면, 항상 2 bits를 받아 평균도 2입니다.',
'한 결과의 정보량은 I(x). 앞으로 얻을 정보량의 기대값은 H(X)입니다.',
'그런데 결과가 네 개여도 엔트로피는 다릅니다. 왜 고르게 퍼질수록 커질까요?',
]
REPLACEMENTS=[('1.5 bits','일 점 오 비트'),('2 bits','이 비트'),('1 bit','일 비트'),('0.25','영 점 이 오'),('0.5','영 점 오'),('I(x)','아이 엑스'),('H(X)','에이치 엑스'),('A','에이'),('B','비'),('C','씨'),('0','영'),('1','일'),('2','이')]
SPOKEN=[]
for text in TEXT:
    for old,new in REPLACEMENTS:text=text.replace(old,new)
    SPOKEN.append(text)
CUES=[]
frames=0
for i,(display,spoken) in enumerate(zip(TEXT,SPOKEN)):
    length=max(2.6,len(''.join(spoken.split()))/7.0+.18*(spoken.count('.')+spoken.count('?')))+(.5 if i==len(TEXT)-1 else 0)
    n=round(length*30);CUES.append((frames/30,(frames+n)/30,display,spoken));frames+=n
DURATION=frames/30
