"""Conditional entropy as the part not already supplied by side information."""
import math

CODE={'A':'00','B':'01','C':'10','D':'11'}
GROUP={'A':'left','B':'left','C':'right','D':'right'}
MESSAGE='B'
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
DISPLAY=[
 '보낼 결과는 B입니다. 받는 사람은 아직 무엇인지 모릅니다.',
 '네 결과가 같은 확률이면 두 비트로 구별합니다. B는 01을 보냅니다.',
 '이번에는 받는 사람이 이미 왼쪽 그룹이라고 알고 있습니다. A나 B만 남습니다.',
 '첫 비트 0은 이미 아는 내용입니다. 이것까지 다시 보낼 필요는 없습니다.',
 '남은 1만 보내면, A가 아닌 B라는 것을 완전히 복원합니다.',
 '결과 B는 그대로입니다. 줄인 것은 받는 사람에게 다시 설명해야 하는 부분입니다.',
 '왼쪽도 오른쪽도 한 비트가 남습니다. 이 평균이 조건부 엔트로피입니다.',
 '원래 2비트에서 남은 1비트를 뺀 값. 이 절약분이 상호정보량입니다.',
 '단서가 없으면 둘 다 보냅니다. B를 이미 안다면 새로 보낼 비트는 없습니다.',
 'X도 새로 보내면 총 두 비트입니다. 이미 아는 부분만 생략한 겁니다.',
 '핵심은 평균적으로 아낀 비트입니다. 매번 줄어든다는 뜻은 아닙니다.',
 '새 관측 없이 가공만 해도, 원본에 대한 정보를 더 만들 수 있을까요?',
]
REPLACEMENTS=[('01','영 일'),('2','이'),('1','일'),('0','영'),('X','엑스'),('Y','와이'),('A','에이'),('B','비'),('D','디')]
SPOKEN=[]
for text in DISPLAY:
    for original,spoken in REPLACEMENTS: text=text.replace(original,spoken)
    SPOKEN.append(text)
CUES=[];frames=0
for i,(display,spoken) in enumerate(zip(DISPLAY,SPOKEN)):
    core_minimum=[4,5,5,6,5,4]
    seconds=max(core_minimum[i] if i<6 else 3,len(''.join(spoken.split()))/7+.18*(spoken.count('.')+spoken.count('?')))
    if i==len(DISPLAY)-1: seconds+=.5
    n=round(seconds*30)
    CUES.append((frames/30,(frames+n)/30,display,spoken));frames+=n
DURATION=frames/30
