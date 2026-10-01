import math
from fractions import Fraction
from random import Random
P,Q=(.75,.25),(.5,.5)
BASE=-sum(p*math.log2(p) for p in P)
TOTAL=1.
EXTRA=TOTAL-BASE
REVERSE=sum(q*math.log2(q/p) for p,q in zip(P,Q))
tail=list('A'*744+'B'*248)
Random(7).shuffle(tail)
MESSAGE='AABAAABA'+''.join(tail)

def encode(message,weights):
    """Shortest dyadic cell contained in the exact arithmetic interval."""
    d=sum(weights); lo,hi,den=0,1,1
    for symbol in message:
        span=hi-lo
        a=0 if symbol=='A' else weights[0]
        b=weights[0] if symbol=='A' else d
        lo,hi=d*lo+a*span,d*lo+b*span
        den*=d
    length=0
    while True:
        scale=1<<length
        k=(lo*scale+den-1)//den
        if (k+1)*den<=hi*scale:
            return format(k,f'0{length}b') if length else ''
        length+=1

def decode(bits,weights,count):
    value=Fraction(2*int(bits or '0',2)+1,1<<(len(bits)+1))
    cut=Fraction(weights[0],sum(weights)); out=[]
    for _ in range(count):
        if value<cut:
            out.append('A'); value/=cut
        else:
            out.append('B'); value=(value-cut)/(1-cut)
    return ''.join(out)

BITS_P,BITS_Q=encode(MESSAGE,(3,1)),encode(MESSAGE,(1,1))
TEXT=[
 '똑같은 천 개의 데이터를 보냈는데, 한쪽은 백팔십칠 비트를 더 썼습니다.',
 '실제로는 에이가 네 번 중 세 번. 내 모델은 둘이 반반이라고 가정합니다.',
 '에이 칠백오십 개, 비 이백오십 개. 이 같은 데이터열을 두 확률표로 묶어 인코딩합니다.',
 '실제 확률표로는 팔백십삼 비트. 반반인 표로는 천 비트. 둘 다 원본이 그대로 복원됩니다.',
 '달라진 것은 데이터가 아니라, 데이터를 표현할 때 사용한 확률표입니다.',
 '실제 코드에는 마무리 비트도 붙습니다. 이를 제외한 이상적 차이는 약 백팔십구 비트입니다.',
 '기호 하나당 일 비트에서 영 점 팔일일 비트를 뺀 값. 이 평균 추가분이 케이엘입니다.',
 '비만 보면 반반인 모델이 오히려 짧습니다. 하지만 더 자주 나오는 에이에서 그 이상을 더 씁니다.',
 '거꾸로 반반인 세계에서 데이터를 받으면, 평균내는 빈도가 바뀌어 케이엘도 달라집니다.',
 '모델이 실제 확률과 같아지면 추가분은 영. 원래 필요한 표현까지 사라지지는 않습니다.',
 '그렇다면 다른 변수를 하나 알려주면, 보내야 할 비트는 얼마나 줄어들까요?',
]
SPOKEN=TEXT
DISPLAY=[
 '똑같은 1000개의 데이터를 보냈는데, 한쪽은 187비트를 더 썼습니다.',
 '실제로는 A가 네 번 중 세 번. 내 모델은 둘이 반반이라고 가정합니다.',
 'A 750개, B 250개. 이 같은 데이터열을 두 확률표로 묶어 인코딩합니다.',
 '실제 확률표로는 813비트. 반반인 표로는 1000비트. 둘 다 원본이 그대로 복원됩니다.',
 TEXT[4],
 '실제 코드에는 마무리 비트도 붙습니다. 이를 제외한 이상적 차이는 약 189비트입니다.',
 '기호 하나당 1비트에서 0.811비트를 뺀 값. 이 평균 추가분이 KL입니다.',
 'B만 보면 반반인 모델이 오히려 짧습니다. 하지만 더 자주 나오는 A에서 그 이상을 더 씁니다.',
 '거꾸로 반반인 세계에서 데이터를 받으면, 평균내는 빈도가 바뀌어 KL도 달라집니다.',
 '모델이 실제 확률과 같아지면 추가분은 0. 원래 필요한 표현까지 사라지지는 않습니다.',
 TEXT[10],
]
CUES=[]; frames=0
for i,text in enumerate(TEXT):
    seconds=max(3,len(''.join(text.split()))/7+.18*(text.count('.')+text.count('?')))
    if i==len(TEXT)-1: seconds+=.5
    count=round(seconds*30)
    CUES.append((frames/30,(frames+count)/30,DISPLAY[i],text)); frames+=count
DURATION=frames/30
