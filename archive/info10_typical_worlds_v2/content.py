"""Exact finite Bernoulli examples, asymptotic typicality, and Gaussian radial mass."""
import math
from fractions import Fraction
import numpy as np
from scipy.stats import binom,chi
P_H=.9
N=100
H=-P_H*math.log2(P_H)-(1-P_H)*math.log2(1-P_H)
MODE_PROB=P_H**N
ONE_TEN=P_H**90*(1-P_H)**10
TEN_COUNT=math.comb(100,10)
TEN_MASS=TEN_COUNT*ONE_TEN
BAND_MASS=sum(math.comb(N,k)*P_H**(N-k)*(1-P_H)**k for k in range(5,16))
BAND_COUNT=sum(math.comb(N,k) for k in range(5,16))
GAUSSIAN_D=100
SHELL_MASS=float(chi.cdf(12,100)-chi.cdf(8,100))
rng=np.random.default_rng(10)
EXAMPLES=[]
for _ in range(4):
    sequence=np.array(list('H'*90+'T'*10));rng.shuffle(sequence);EXAMPLES.append(''.join(sequence))
# Distances are actual 100-D norms; display angles are schematic, not a 2-D projection.
RADII=np.linalg.norm(rng.normal(size=(160,100)),axis=1)
ANGLES=rng.uniform(0,2*math.pi,len(RADII))

def typical(n,k,epsilon):
    information=-(n-k)*math.log2(.9)-k*math.log2(.1)
    return abs(information/n-H)<=epsilon

def interval(sequence):
    lo,hi=Fraction(0),Fraction(1)
    for symbol in sequence:
        cut=lo+(hi-lo)*Fraction(9,10)
        if symbol=='H':hi=cut
        else:lo=cut
    return lo,hi

def encode(sequence):
    lo,hi=interval(sequence)
    for length in range(1,4*len(sequence)+3):
        denominator=1<<length
        number=(lo.numerator*denominator+lo.denominator-1)//lo.denominator
        if Fraction(number+1,denominator)<=hi:
            return format(number,f'0{length}b')
    raise ValueError('No code found')

def decode(code,n=100):
    point=Fraction(2*int(code,2)+1,1<<(len(code)+1))
    lo,hi=Fraction(0),Fraction(1);out=[]
    for _ in range(n):
        cut=lo+(hi-lo)*Fraction(9,10)
        if point<cut:out.append('H');hi=cut
        else:out.append('T');lo=cut
    return ''.join(out)

# A real 47-bit arithmetic prefix, not a promise for every 100-symbol message.
DEMO='HHTHHHHHTHHHTHHHHHHHHHHHHHHHHHHHHHHHHTHHHHHHTHHHHHHHHHHHHHHTHHHHHHHTHHHHHHHHHHHHHHHHHHHHHHTHHTHTHHHH'
CODE=encode(DEMO)
assert len(DEMO)==100 and DEMO.count('T')==10
assert len(CODE)==47 and decode(CODE)==DEMO
RAW=''.join('0' if c=='H' else '1' for c in DEMO)

DISPLAY=[
 '100비트를 47비트로 보내도, 같은 결과를 복원할 수 있을까요?',
 '앞면이 90퍼센트인 동전을 100번 던졌습니다. 하나씩 적으면 100비트입니다.',
 '같은 번호표를 쓰면, 이 줄은 47비트만 보내도 그대로 복원됩니다.',
 '뒷면 열 개의 위치마다 다른 줄입니다. 그런 줄만 약 17조 개입니다.',
 '정확히 열 개만 모으면 확률은 13퍼센트. 주변까지 모으면 대부분의 확률이 담깁니다.',
 '긴 데이터에서는 전형적인 후보들이 거의 모든 확률을 차지합니다. 여기에 번호를 붙입니다.',
 '이 동전의 엔트로피는 약 0.469비트. 100개당 평균 한계로 환산하면 약 47비트입니다.',
 '긴 묶음으로 보내면, 기호당 평균 길이가 이 한계에 가까워집니다.',
 '엔트로피는 후보 수의 증가율입니다. 후보가 많아질수록 번호도 길어집니다.',
 '예외도 버리지 않습니다. 같은 데이터를 복원하되, 주로 만나는 줄에 짧은 번호를 줍니다.',
 '전부 앞면인 줄은 하나로서는 가장 유력합니다. 하지만 중요한 건 많은 줄을 모은 확률입니다.',
 '고차원에서도 밀도는 원점에서 최고지만, 샘플 대부분은 바깥 껍질에 모입니다.',
 '압축의 핵심은, 실제로 만나는 세계들을 짧은 번호로 구별하는 것입니다.',
]
READINGS=[('100','백'),('47','사십칠'),('90','구십'),('13','십삼'),('17','십칠'),('0.469','영 점 사육구')]
SPOKEN=[]
for text in DISPLAY:
    for a,b in READINGS:text=text.replace(a,b)
    SPOKEN.append(text)
DISPLAY[3]=DISPLAY[3].replace('열 개','10개')
DISPLAY[4]=DISPLAY[4].replace('열 개','10개')
CUES=[];frames=0
for i,(display,spoken) in enumerate(zip(DISPLAY,SPOKEN)):
    duration=max(3.5,len(''.join(spoken.split()))/7+.18*(spoken.count('.')+spoken.count('?')))
    if i==len(DISPLAY)-1:duration+=.5
    count=round(duration*30)
    CUES.append((frames/30,(frames+count)/30,display,spoken));frames+=count
DURATION=frames/30
