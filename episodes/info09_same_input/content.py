"""Finite deterministic processing with explicit provenance collisions."""
import math
from collections import defaultdict
SYMBOLS='ABCD'
P={s:.25 for s in SYMBOLS}
F={'A':0,'B':0,'C':1,'D':1}
COORDS={'A':(0,0),'B':(1,1),'C':(0,1),'D':(1,0)}

def steps(y):
    return (y,5*y,5*y+3,(5*y+3)**2,(5*y+3)**2+8)

def g(y):
    return steps(y)[-1]

def partition(mapping):
    groups=defaultdict(list)
    for s in SYMBOLS: groups[mapping[s]].append(s)
    return dict(groups)

def entropy(p):
    return -sum(a*math.log2(a) for a in p if a>0)

def information(mapping):
    # Since the displayed mapping is deterministic, I(X;mapping(X))=H(mapping(X)).
    masses=defaultdict(float)
    for s,p in P.items():masses[mapping[s]]+=p
    return entropy(masses.values())

PRESERVED={s:g(F[s]) for s in SYMBOLS}
MERGED={s:17 for s in SYMBOLS}
VALUES=(information({s:s for s in SYMBOLS}),information(F),information(PRESERVED),information(MERGED))
DISPLAY=[
 'A와 B를 같은 0으로 바꿨다면, 계산만으로 다시 구분할 수 있을까요?',
 '네 상태를 두 그룹으로 가공합니다. A와 B는 0, C와 D는 1이 됩니다.',
 '0만 받으면 A인지 B인지 알 수 없습니다. 둘의 구분이 이미 합쳐졌기 때문입니다.',
 '이번에는 곱하고 더하고 제곱해봅니다. 0은 3, 9, 17로 바뀝니다.',
 'A에서 온 0도, B에서 온 0도 같은 계산을 거쳐 17이 됩니다.',
 '숫자는 커졌지만, A와 B를 가를 단서는 생기지 않았습니다.',
 '0은 17로, 1은 72로 바꾸면 구분은 남습니다. 그룹은 여전히 둘입니다.',
 '두 그룹마저 같은 결과로 합치면, 그 구분도 사라집니다.',
 '원본에 대한 정보는 1비트로 유지되거나 0으로 줄었습니다. 늘지는 않았습니다.',
 '이 관계가 데이터 처리 부등식입니다. 뒤의 계산은 앞의 값만 사용합니다.',
 '신경망도 특징을 보기 쉽게 바꿀 수 있습니다. 더 유용해져도 새 관측이 생긴 것은 아닙니다.',
 '그렇다면 어떤 구분을 버리고, 어떤 구분을 남겨야 할까요?',
]
READINGS=[('72','칠십이'),('17','십칠'),('9','구'),('3','삼'),('1','일'),('0','영'),('A','에이'),('B','비'),('C','씨'),('D','디')]
SPOKEN=[]
for text in DISPLAY:
    for a,b in READINGS:text=text.replace(a,b)
    SPOKEN.append(text)
CUES=[];frames=0
for i,(display,spoken) in enumerate(zip(DISPLAY,SPOKEN)):
    minimum=5 if i in (3,4) else 3
    seconds=max(minimum,len(''.join(spoken.split()))/7+.18*(spoken.count('.')+spoken.count('?')))
    if i==len(DISPLAY)-1:seconds+=.5
    n=round(seconds*30)
    CUES.append((frames/30,(frames+n)/30,display,spoken));frames+=n
DURATION=frames/30
