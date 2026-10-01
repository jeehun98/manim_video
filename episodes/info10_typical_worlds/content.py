"""Finite coin examples and a shared four-entry codebook for the compression lesson."""
import math
import numpy as np
from scipy.stats import binom
P_H=.9
N=100
H=-P_H*math.log2(P_H)-(1-P_H)*math.log2(1-P_H)
ONE_TEN=P_H**90*(1-P_H)**10
TEN_COUNT=math.comb(100,10)
TEN_MASS=TEN_COUNT*ONE_TEN
BAND_MASS=float(binom.cdf(15,100,.1)-binom.cdf(4,100,.1))
BAND_COUNT=sum(math.comb(100,k) for k in range(5,16))
rng=np.random.default_rng(10)
EXAMPLES=[]
for _ in range(4):
    seq=np.array(list('H'*90+'T'*10));rng.shuffle(seq);EXAMPLES.append(''.join(seq))
TOY=['00000000','00100000','00001000','00000010']
TOY_CODES=[format(i,'02b') for i in range(4)]
DISPLAY=[
 '100비트 문자열은 모두 몇 개일까요? 가능한 줄은 2의 100제곱 개입니다.',
 '하지만 앞면이 90퍼센트라면, 모든 줄이 똑같이 자주 나오지는 않습니다.',
 '특정 위치에 뒷면 10개가 나올 확률은 작습니다. 그런 줄 약 17조 개를 합치면 13퍼센트입니다.',
 '10개뿐 아니라 5개부터 15개까지 모으면, 확률은 약 94퍼센트가 됩니다.',
 '긴 데이터에선 거의 모든 확률이 전형적인 집합에 모입니다. 모든 줄에 똑같이 긴 표현이 필요할까요?',
 '작은 예로 보겠습니다. 양쪽이 같은 후보 4개의 목록을 알고 있다고 해보죠.',
 '두 번째 줄 대신 01을 보내면, 받는 사람은 목록에서 같은 줄을 복원합니다.',
 '4개를 구별하려면 2비트. 1비트는 번호가 두 개뿐이라 후보들이 겹칩니다.',
 '8개라면 3비트입니다. 후보가 몇 개인지가 번호의 길이를 결정합니다.',
 '긴 데이터의 전형적인 후보는 대략 2의 nH제곱 개. 번호에는 약 nH비트가 필요합니다.',
 '이 동전은 기호당 약 0.469비트. 긴 데이터의 한계를 100개당 환산하면 약 47비트입니다.',
 '드문 줄도 버리지 않습니다. 이런 경우에는 더 긴 표현으로 보냅니다.',
 '엔트로피가 압축 한계인 이유는, 전형적인 후보의 수가 번호의 길이를 결정하기 때문입니다.',
]
READINGS=[('0.469','영 점 사육구'),('2의','이의'),('100','백'),('90','구십'),('17','십칠'),('13','십삼'),('94','구십사'),('15','열다섯'),('10','열'),('01','영 일'),('47','사십칠'),('nH','엔 에이치'),('8','여덟'),('5','다섯'),('4','네'),('3','세'),('2','두'),('1','한')]
SPOKEN=[]
for text in DISPLAY:
    for a,b in READINGS:text=text.replace(a,b)
    SPOKEN.append(text)
CUES=[];frames=0
for i,(display,spoken) in enumerate(zip(DISPLAY,SPOKEN)):
    duration=max(3.5,len(''.join(spoken.split()))/7+.18*(spoken.count('.')+spoken.count('?')))
    if i==len(DISPLAY)-1:duration+=.5
    count=round(duration*30)
    CUES.append((frames/30,(frames+count)/30,display,spoken));frames+=count
DURATION=frames/30
