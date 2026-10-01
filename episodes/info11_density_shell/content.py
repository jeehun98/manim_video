"""Actual Gaussian distances and exact radial probabilities, separate from schematic geometry."""
import math
import numpy as np
from scipy.stats import chi
D=100
COUNT=2000
rng=np.random.default_rng(11)
SAMPLES=rng.normal(size=(COUNT,D))
RADII=np.linalg.norm(SAMPLES,axis=1)
ANGLES=np.random.default_rng(111).uniform(0,2*math.pi,160)
BINS=np.linspace(0,15,61)
HIST,_=np.histogram(RADII,bins=BINS)
MASS_8_12=float(chi.cdf(12,D)-chi.cdf(8,D))
EMPIRICAL_8_12=int(np.count_nonzero((RADII>=8)&(RADII<=12)))
INNER_AREA=math.pi*.25**2
OUTER_AREA=math.pi*(1.75**2-1.5**2)
INNER_MASS=1-math.exp(-.25**2/2)
OUTER_MASS=math.exp(-1.5**2/2)-math.exp(-1.75**2/2)
AVG_DENSITY_RATIO=(OUTER_MASS/OUTER_AREA)/(INNER_MASS/INNER_AREA)
DISPLAY=[
 '가우시안의 밀도는 중심에서 가장 높습니다. 샘플도 중심에 가장 많이 모일까요?',
 '차원을 높여도 밀도가 가장 높은 곳은 원점입니다. 그런데 실제 샘플은 어떨까요?',
 '100차원에서 2000개를 뽑아 거리를 재봤습니다. 대부분 0이 아니라 10 근처입니다.',
 '각 좌표의 제곱은 평균적으로 1씩 기여합니다. 100개를 더하면 거리의 제곱은 약 100, 거리는 약 10입니다.',
 '거리 10에 있는 한 점의 밀도는 원점보다 낮습니다. 그런데 왜 그곳에서 샘플을 더 많이 만날까요?',
 '폭이 같은 영역을 비교해보죠. 중심의 작은 원보다 바깥 고리에 훨씬 많은 공간이 있습니다.',
 '작은 칸의 밀도와 크기를 곱해서 더합니다. 칸당 밀도가 낮아도, 그런 칸이 많으면 전체 확률은 커집니다.',
 '고차원에서는 같은 거리 폭에 들어가는 공간이, 바깥으로 갈수록 훨씬 빠르게 늘어납니다.',
 '밀도는 줄고, 공간량은 늘어납니다. 둘을 곱한 거리 분포는 10 근처에서 가장 높습니다.',
 '100차원에서는 거리 8부터 12까지의 영역에, 전체 확률의 약 99.5퍼센트가 담깁니다.',
 '전형적인 샘플은 최고 밀도의 한 점이 아니라, 확률이 모인 이 껍질에서 만납니다.',
 '생성모델에서도 최고 밀도와 전형적인 샘플은 다를 수 있습니다. 한 점보다 영역 전체의 확률을 봐야 합니다.',
]
READINGS=[('2000','이천'),('100','백'),('99.5','구십구 점 오'),('12','열두'),('10','십'),('8','여덟'),('0','영'),('1','일')]
SPOKEN=[]
for v in DISPLAY:
    for a,b in READINGS:v=v.replace(a,b)
    SPOKEN.append(v)
CUES=[];frames=0
for i,(text,spoken) in enumerate(zip(DISPLAY,SPOKEN)):
    duration=max(3.5,len(''.join(spoken.split()))/7+.18*(spoken.count('.')+spoken.count('?')))
    if i==len(DISPLAY)-1:duration+=.5
    count=round(duration*30)
    CUES.append((frames/30,(frames+count)/30,text,spoken));frames+=count
DURATION=frames/30
