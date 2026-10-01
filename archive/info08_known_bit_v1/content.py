"""Conditional entropy as the part not already supplied by side information."""
import math
from random import Random

CODE={'A':'00','B':'01','C':'10','D':'11'}
GROUP={'A':'left','B':'left','C':'right','D':'right'}
symbols=list('ABCD'*4)
Random(8).shuffle(symbols)
MESSAGE=''.join(symbols)
FULL=''.join(CODE[s] for s in MESSAGE)
SIDE=''.join(CODE[s][0] for s in MESSAGE)
RESIDUAL=''.join(CODE[s][1] for s in MESSAGE)

def restore(full):
    if len(full)%2: raise ValueError('Two-bit words required')
    inverse={v:k for k,v in CODE.items()}
    return ''.join(inverse[full[i:i+2]] for i in range(0,len(full),2))

def restore_with_side(side,residual):
    if len(side)!=len(residual): raise ValueError('Side information must align')
    return restore(''.join(a+b for a,b in zip(side,residual)))

def entropy(probabilities):
    return -sum(p*math.log2(p) for p in probabilities if p)

def measures(joint):
    """Return H(Y), H(Y|X), I(X;Y) for a finite joint PMF."""
    if abs(sum(joint.values())-1)>1e-12 or any(p<0 for p in joint.values()):
        raise ValueError('Normalized nonnegative joint distribution required')
    px,py={},{}
    for (x,y),p in joint.items():
        px[x]=px.get(x,0)+p;py[y]=py.get(y,0)+p
    hy=entropy(py.values())
    conditional=sum(p*-math.log2(p/px[x]) for (x,y),p in joint.items() if p)
    return hy,conditional,hy-conditional

PARTIAL={(GROUP[y],y):.25 for y in 'ABCD'}
INDEPENDENT={(x,y):.125 for x in ('left','right') for y in 'ABCD'}
PERFECT={(y,y):.25 for y in 'ABCD'}
# Illustrative model, not empirical weather statistics.
WEATHER={('rain','use'):.45,('rain','no'):.05,('clear','use'):.05,('clear','no'):.45}
WEATHER_H,WEATHER_CONDITIONAL,WEATHER_MI=measures(WEATHER)

DISPLAY=[
 '받는 쪽이 X를 알면, 같은 데이터도 절반의 비트로 보낼 수 있습니다.',
 '네 결과가 같은 확률이면, 각각 두 비트로 표현합니다.',
 'X는 어느 쪽인지 알려줍니다. 왼쪽이라면 A나 B입니다.',
 '첫 비트는 이미 알고 있으니, 마지막 한 비트만 보냅니다.',
 '두 방식 모두 같은 원본이 그대로 복원됩니다.',
 '왼쪽도 오른쪽도 한 비트가 남습니다. 이 평균이 조건부 엔트로피입니다.',
 '원래 2비트에서 남은 1비트를 뺀 값. 이 절약분이 상호정보량입니다.',
 'X가 독립이면 여전히 2비트. 반대로 Y를 완전히 알려주면 남는 비트는 0입니다.',
 '날씨를 알면 우산의 후보는 그대로여도 확률이 바뀝니다. 평균 비트도 줄어듭니다.',
 'X까지 보내면 총 32비트. 이미 알고 있는 부분만 생략한 겁니다.',
 '핵심은 평균적으로 아낀 비트입니다. 매번 줄어든다는 뜻은 아닙니다.',
 '그렇다면 새 관측 없이 가공만 해도, 원본에 대한 정보를 더 만들 수 있을까요?',
]
REPLACEMENTS=[('32','삼십이'),('16','열여섯'),('2','이'),('1','일'),('0','영'),('X','엑스'),('Y','와이'),('A','에이'),('B','비'),('D','디')]
SPOKEN=[]
for text in DISPLAY:
    for original,spoken in REPLACEMENTS: text=text.replace(original,spoken)
    SPOKEN.append(text)
CUES=[];frames=0
for i,(display,spoken) in enumerate(zip(DISPLAY,SPOKEN)):
    seconds=max(3,len(''.join(spoken.split()))/7+.18*(spoken.count('.')+spoken.count('?')))
    if i==len(DISPLAY)-1: seconds+=.5
    n=round(seconds*30)
    CUES.append((frames/30,(frames+n)/30,display,spoken));frames+=n
DURATION=frames/30
