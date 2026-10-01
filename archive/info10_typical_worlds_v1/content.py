"""Exact finite Bernoulli examples, asymptotic typicality, and Gaussian radial mass."""
import math
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

DISPLAY=[
 '가장 확률 높은 결과를 찾으면, 압축의 핵심도 보일까요?',
 '앞면은 90퍼센트. 전부 앞면이 제일 유력하지만, 백 번 이어질 확률은 아주 작습니다.',
 '실제 결과는 앞면 아흔 개 근처입니다. 뒷면의 위치마다 다른 데이터열이 됩니다.',
 '뒷면 열 개인 줄만 십칠조 개. 하나는 드물어도, 합치면 확률이 13퍼센트입니다.',
 '주변까지 모으면 대부분의 확률이 담깁니다. 이것이 전형적인 결과들의 집합입니다.',
 '핵심은 가장 유력한 한 줄이 아니라, 확률질량이 모이는 많은 줄입니다.',
 '길어지면 이 집합이 거의 전체 확률을 차지합니다. 작은 확률의 후보가 많이 모여야 합니다.',
 '그 많은 후보에 번호를 붙이면, 번호의 길이가 엔 에이치 비트가 됩니다.',
 '기호당 한계는 엔트로피. 드문 예외도 따로 표현해 무손실로 보냅니다.',
 '전체 가능한 줄 중, 전형적인 후보들의 구별에 비트를 집중합니다.',
 '고차원에선 원점의 밀도가 최고지만, 샘플 대부분은 바깥 껍질에 있습니다.',
 '점의 밀도가 낮아져도 공간이 커집니다. 많은 점을 모은 껍질의 질량은 커질 수 있습니다.',
 '높은 밀도와 전형적인 샘플은 다릅니다. 엔트로피는 구별할 전형적인 세계의 수를 결정합니다.',
]
READINGS=[('90','구십'),('13','십삼')]
SPOKEN=[]
for text in DISPLAY:
    for a,b in READINGS:text=text.replace(a,b)
    SPOKEN.append(text)
DISPLAY[1]=DISPLAY[1].replace('백 번','100번')
DISPLAY[2]=DISPLAY[2].replace('아흔 개','90개')
DISPLAY[3]=DISPLAY[3].replace('열 개인','10개인').replace('십칠조 개','약 17조 개')
DISPLAY[7]=DISPLAY[7].replace('엔 에이치 비트','nH 비트')
CUES=[];frames=0
for i,(display,spoken) in enumerate(zip(DISPLAY,SPOKEN)):
    duration=max(3.5,len(''.join(spoken.split()))/7+.18*(spoken.count('.')+spoken.count('?')))
    if i==len(DISPLAY)-1:duration+=.5
    count=round(duration*30)
    CUES.append((frames/30,(frames+count)/30,display,spoken));frames+=count
DURATION=frames/30
